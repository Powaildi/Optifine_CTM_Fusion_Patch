import time
import functools

def evaluatetime(func):
    def wrapper(*args,**kwargs):
        starttime = time.time()
        result = func(*args,**kwargs)
        endtime = time.time()
        print(f"函数 {func.__name__} 用了{endtime - starttime}秒来运行")
        return result
    return wrapper