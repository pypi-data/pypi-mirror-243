import functools
import os


def client_method(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        if os.getenv("SERVER_MODE") == "True":
            raise RuntimeError(f"client method: {func.__str__} can't be executed in server")
        return func(*args, **kwargs)
    return wrapper


def server_method(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        if os.getenv("SERVER_MODE") != "True":
            print(f"warning: method {func.__str__} only runs on the server. skipping")
            return
        return func(*args, **kwargs)
    return wrapper
