import time


class IterationLimitReached(Exception):
    """Custom exception to raise when the process has reached the number of iterations limit."""
    def __init__(self):
        super().__init__('[ERROR]: The limit of iterations has been reached.')

class IterationTimeout(Exception):
    """Custom exception to raise when an iteration timeout occurs."""
    def __init__(self):
        super().__init__('[ERROR]: Iterator time out.')

class IteratorValidator:
    """
    @version 0.1.0
    
    Container for different generators, to validate the number of iterations to execute, either by the number of repetitions or by
    the elapsed time, while providing also the waiting mechanism in this last one.
    """

    @staticmethod
    def iterator_with_counter(max_iterations: int):
        """
        @param {int} max_iterations The upper limit for the number of iterations.

        Generator to keep track of the number of iterations, if the limit is reached, and exception is raised.
        """
        iterations = 0
        while True:
            yield iterations
            if iterations == max_iterations:
                raise IterationLimitReached()
            else: iterations += 1

    @staticmethod
    def iterator_with_timeout(timeout: float, sleep_time: float = 0.1):
        """
        @param {float} timeout The upper limit for the time to wait (in seconds) before raising a timeout exception.
        @param {float} sleep_time The sleep time between iterations (in seconds, by default 0.1s).

        Generator to keep track of the elapsed time of the process, when the process times out an exception is raised.
        It also executes the times.sleep function, so there is no need to worry about it at the caller side. 
        """
        elapsed_time = 0
        while True:
            time.sleep(sleep_time)
            yield elapsed_time
            if elapsed_time >= timeout:
                raise IterationTimeout()
            else: elapsed_time += sleep_time