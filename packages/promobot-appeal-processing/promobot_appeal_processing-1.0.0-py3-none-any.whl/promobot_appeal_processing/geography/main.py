__all__ = ["predict_geography", "predict_geography_async", "predict_geography_many"]


import asyncio
from concurrent.futures import ProcessPoolExecutor
from typing import Iterable

from model import geography


def predict_geography(text: str) -> tuple[str]:
    """
    Extract geographical object names from the given ``text``

    Args:
        text: Appeal text

    Returns:
        Geographical names
    """
    return geography.predict(text)


async def predict_geography_async(text: str) -> tuple[str]:
    """
    Asynchronous wrapper around the ``predict_geography`` function

    Args:
        text: Appeal text

    Returns:
        Geographical names
    """
    return await asyncio.to_thread(predict_geography, text)


async def predict_geography_many(texts: Iterable[str], max_workers: int) -> tuple[tuple[str]]:
    """
    Wrapper around the ``predict_geography`` function that executes the geography name extraction tasks
    in parallel using ``max_workers`` processes

    Args:
        texts: Appeal texts
        max_workers: Maximum number of parallel processes (passed to ``asyncio.ProcessPoolExecutor``)

    Returns:
        Geographical names from all appeal texts (in respective order)
    """
    loop = asyncio.get_running_loop()
    executor = ProcessPoolExecutor(max_workers=max_workers)

    return tuple(
        await asyncio.gather(
            *(loop.run_in_executor(executor, predict_geography, text) for text in texts)
        )
    )
