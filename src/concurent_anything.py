from collections.abc import Collection
from typing import Callable
from multiprocessing import cpu_count

from functools import partial

import concurrent.futures


class _ConcurrentParent:
    def __init__(self, iterable: Collection, function: Callable, args_tuple: tuple = None, kwargs_dict: dict = None,
                 exception_dict={}, item_param_name: str = None):
        """
        The _ConcurrentParent class is a private class that holds all of our common code for threading
         and multiprocessing. To use it, your function must accept the item as it's first argument.
        :param iterable: Any python iterable you want to call concurrency on
        :param function: The function you want to call on each item in the iterable
        :param args_tuple: Tuple containing the ordered arguments that pass to the function
        :param kwargs_dict: Dictionary containing the keyword arguments that pass to the function
        :param exception_dict: A dictionary of exceptions and functions to handle them.
        """
        self.iterable = iterable
        self.function = function
        self.args_tuple = args_tuple
        self.kwargs_dict = kwargs_dict
        self.exception_dict = exception_dict
        self.item_param_name = item_param_name

    def _process_future(self, future: concurrent.futures, log_function: Callable = print):
        """
        Function for processing any individual future from self.futures
        :param future: the future object to be processed
        :param log_function: The default way of managing an error not in the exception difficulty. Defaults to printing
        to standard out
        :return:
        """
        try:
            return future.result()

        except Exception as e:
            self.exception_dict.get(e, log_function(e))

    def _concurrent_function(self, metafunction, max_workers):
        """
        This is the general construct of the process and thread pool executors
        :param metafunction: This is a placeholder to be used by our child class
        :param max_workers: The max workers used in the operation
        :return:
        """

        with metafunction(max_workers) as executor:
            # todo: test all iterations of this

            if self.args_tuple and self.kwargs_dict:  # args and kwargs
                futures = {executor.submit(self.function, item, *self.args_tuple, **self.kwargs_dict): item for item in
                            self.iterable}

            elif self.args_tuple:  # args no kwargs
                futures = {executor.submit(self.function, item, *self.args_tuple): item for item in
                            self.iterable}

            elif self.kwargs_dict:  # no args kwargs
                futures = {executor.submit(self.function, item, **self.kwargs_dict): item for item in
                            self.iterable}

                print(self.kwargs_dict)

            else:  # no args no kwargs
                futures = {executor.submit(self.function, item): item for item in
                            self.iterable}

            return [self._process_future(future) for future in concurrent.futures.as_completed(futures)]


class ThreadAnything(_ConcurrentParent):
    def __init__(self, iterable: Collection, function: Callable, args_tuple: tuple = None, kwargs_dict: dict = None,
                 exception_dict={}):
        """
        Child class for threading
        :param iterable: Any python iterable you want to call concurrency on
        :param function: The function you want to call on each item in the iterable
        :param args_tuple: Tuple containing the ordered arguments that pass to the function
        :param kwargs_dict: Dictionary containing the keyword arguments that pass to the function
        """
        super().__init__(iterable, function, args_tuple, kwargs_dict, exception_dict)

    def thread_anything(self, max_workers=10):
        """
        executes the concurrent_function from the parent class passing the ThreadPoolExecutor to it
        :param max_workers: The max workers used in the operation, default value of 10
        :return:
        """
        return self._concurrent_function(concurrent.futures.ThreadPoolExecutor, max_workers=max_workers)

    def __call__(self, max_workers=10):
        return self.thread_anything(max_workers=max_workers)


class MultiProcessAnything(_ConcurrentParent):
    def __init__(self, iterable: Collection, function: Callable, args_tuple: tuple = None, kwargs_dict: dict = None,
                 exception_dict={}):
        """
        Child class for MultiProcessing
        :param iterable: Any python iterable you want to call concurrency on
        :param function: The function you want to call on each item in the iterable
        :param args_tuple: Tuple containing the ordered arguments that pass to the function
        :param kwargs_dict: Dictionary containing the keyword arguments that pass to the function
        """
        super().__init__(iterable, function, args_tuple, kwargs_dict, exception_dict)

    def multiprocess_anything(self, max_workers=cpu_count() - 1):
        """
        executes the concurrent_function from the parent class passing the ProcessPoolExecutor to it
        :param max_workers: defaults to 1 less then available CPU cores on the machine
        :return:
        """
        return self._concurrent_function(concurrent.futures.ProcessPoolExecutor, max_workers=max_workers)

    def __call__(self, max_workers=10):
        return self.multiprocess_anything(max_workers=max_workers)
