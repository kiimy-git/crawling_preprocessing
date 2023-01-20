import time
from functools import wraps

def check_time(function):
    @wraps(function)
    def measure(*args, **kwargs):
        s_time = time.time()

        res = function(*args, **kwargs)

        e_time = time.time()

        print(f"@check_time: {function.__name__} took {e_time - s_time}")

        return res

    return measure

# @check_time
# def test_f():
#     for _ in range(1000):
#         print("ss")

# if __name__  == "__main__":
#     test_f()