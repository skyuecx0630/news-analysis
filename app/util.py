from datetime import datetime


def track_duration(func):
    def wrapper_function(*args, **kwargs):
        start = datetime.now()
        result = func(*args, **kwargs)
        duration = (datetime.now() - start).total_seconds()
        print(f"{func.__name__}: {duration}s")
        return result

    return wrapper_function


if __name__ == "__main__":
    @track_duration
    def hello(msg):
        print(msg)


    hello("hello world")
