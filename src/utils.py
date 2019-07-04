import io
import functools
from datetime import datetime


def force_async(fn):
    '''
    turns a sync function to async function using threads
    '''
    from concurrent.futures import ThreadPoolExecutor
    import asyncio
    pool = ThreadPoolExecutor()

    @functools.wraps(fn)
    def wrapper(*args, **kwargs):
        future = pool.submit(fn, *args, **kwargs)
        return asyncio.wrap_future(future)  # make it awaitable

    return wrapper


def force_sync(fn):
    '''
    turn an async function to sync function
    '''
    import asyncio

    @functools.wraps(fn)
    def wrapper(*args, **kwargs):
        res = fn(*args, **kwargs)
        if asyncio.iscoroutine(res):
            return asyncio.get_event_loop().run_until_complete(res)
        return res

    return wrapper


def is_date_valid(date_text):
    try:
        datetime.strptime(date_text, '%d.%m.%Y')
    except ValueError:
        return False
    return True


def create_file_like_object(data):
    _file = io.BytesIO()
    _file.write(data)
    _file.seek(0)
    return _file
