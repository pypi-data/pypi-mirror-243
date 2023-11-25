import asyncio
from concurrent.futures import ProcessPoolExecutor
from typing import Iterable

from .model import model
from .structures import Prediction


def predict(text: str) -> Prediction:
    """
    Synchronously predict appeal classification

    Args:
        text: Appeal text

    Returns:
        Predicted classification
    """
    return model.predict(text)


async def predict_async(text: str) -> Prediction:
    """
    Asynchronous wrapper around the ``predict`` function

    Example:
        ```py hl_lines="8"
        from fastapi import FastAPI, Body
        from promobot_appeal_processing import predict_async

        app = FastAPI()

        @app.post("/api")
        async def api(text: str = Body(embed=True)):
            return await predict_async(text)
        ```

    Args:
        text: Appeal text

    Returns:
        Predicted classification
    """
    return await asyncio.to_thread(predict, text)


async def predict_many(texts: Iterable[str], max_workers: int) -> tuple[Prediction]:
    """
    Wrapper around the ``predict`` function that executes the prediction tasks in parallel
    using ``max_workers`` processes

    Example:
        ```py hl_lines="23"
        import aiofiles
        import aiocsv
        import csv
        import io
        from charset_normalizer import from_bytes
        from dataclasses import asdict, fields
        from fastapi import FastAPI, UploadFile
        from fastapi.responses import FileResponse
        from promobot_appeal_processing import predict_many, Prediction

        app = FastAPI()

        @app.post("/file")
        async def file(file: UploadFile):
            contents = str(from_bytes(await file.read()).best()).strip()
            csv_reader = csv.DictReader(io.StringIO(contents), delimiter=";")
            rows = tuple(csv_reader)
            texts = map(lambda row: row["text"], rows)

            data = map(
                lambda row, prediction: row | asdict(prediction),
                rows,
                await predict_many(texts, max_workers=4)
            )

            async with aiofiles.open(path := "temp.csv", "w", encoding="utf-8") as out_file:
                csv_writer = aiocsv.AsyncDictWriter(
                    out_file,
                    fieldnames=[*csv_reader.fieldnames, *map(lambda field: field.name, fields(Prediction))]
                )
                await csv_writer.writeheader()

                for row in data:
                    await csv_writer.writerow(row)

            return FileResponse(
                path,
                media_type="text/csv",
                filename="predictions.csv"
            )
        ```

    Args:
        texts: Appeal texts
        max_workers: Maximum number of parallel processes (passed to ``asyncio.ProcessPoolExecutor``)

    Returns:
        Predicted classifications for all appeal texts (in respective order)
    """
    loop = asyncio.get_running_loop()
    executor = ProcessPoolExecutor(max_workers=max_workers)

    return tuple(
        await asyncio.gather(
            *(loop.run_in_executor(executor, predict, text) for text in texts)
        )
    )
