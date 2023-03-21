from collections.abc import Collection
from typing import Callable
from multiprocessing import cpu_count

import concurrent.futures


class _ConcurrentParent:
    def __init__(self, iterable: Collection, function: Callable, args_tuple: tuple = None, kwargs_dict: dict = None):
        self.iterable = iterable
        self.function = function
        self.args_tuple = args_tuple
        self.kwargs_dict = kwargs_dict
        self.futures = {}

    def concurrent_functions(self, metafunction, max_workers):
        with metafunction(max_workers) as executor:
            self.futures = {executor.submit(self.function, item, *self.args, **self.kwargs): item for item in
                            self.iterable}


class ThreadAnything(_ConcurrentParent):
    def __init__(self, iterable: Collection, function: Callable, args_tuple: tuple = None, kwargs_dict: dict = None):
        super().__init__(self, iterable, function, args_tuple, kwargs_dict)

    def thread_anything(self, max_workers=10):
        self.concurrent_functions(concurrent.futures.ThreadPoolExecutor, max_workers=max_workers)


class MultiProcessAnything(_ConcurrentParent):
    def __init__(self, iterable: Collection, function: Callable, args_tuple: tuple = None, kwargs_dict: dict = None):
        super().__init__(self, iterable, function, args_tuple, kwargs_dict)

    def multiprocess_anything(self, max_workers=cpu_count() - 1):
        self.concurrent_functions(concurrent.futures.ProcessPoolExecutor, max_workers=max_workers)


class FutureProcessor:
    def __init__(self, futures: _ConcurrentParent.futures, exception_dict: dict = {}):
        self.futures = futures
        self.exception_dict = exception_dict

    def process_future(self, future: concurrent.futures):
        try:
            return future.result()

        except Exception as e:
            self.exception_dict.get(e, print(e))

    def process_all_futures(self):

        return [self.process_future(future) for future in self.futures]
