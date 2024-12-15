def print_params_decorator(func):
    def wrapper(*args, **kwargs):
        print(f"Parameters passed to {func.__name__}: args={args}, kwargs={kwargs}")
        return func(*args, **kwargs)

    return wrapper
