
from contextlib import contextmanager
import shelve
import platformdirs
from pathlib import Path
from functools import wraps
from typing import Callable

cache_dir= Path(platformdirs.user_cache_dir("pyzettel"))


@contextmanager
def open_cache(cache_name: str, cache_dir: Path = cache_dir):
    cache_dir.mkdir(parents=True, exist_ok=True)
    try:
        with shelve.open(cache_dir / cache_name) as cache:
            yield cache
    finally:
        pass
    

def use_cache(cache_name: str, cache_dir: Path = cache_dir, ignore_case: bool = True):
    def decorator(func):
        @wraps(func)
        def wrapper(key: str, *args,  **kwargs) -> Callable[..., str]:
            if ignore_case:
                key = key.lower()
            with open_cache(cache_name, cache_dir) as cache:
                if key in cache:
                    return cache[key]
                res = func(key, *args, **kwargs)
                if res:
                    cache[key] = res
                return res
        return wrapper
    return decorator