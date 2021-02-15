# This is a sample Python script.

import threading as _threading

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.

class MockAPI:
    def __init__(self, api_key=''):
        self.api_key = api_key

    def intraday(self, symbol, output_format="csv"):
        if symbol == 'XOM':
            return [['price', 'volume'], [46.12, 20190], [51.1, 3102]]
        if symbol == 'CXW':
            return [['price', 'volume'], [6.12, 9190], [5.1, 6102]]
        return [['price', 'volume'], [256.12, 9190], [255.1, 6102]]

    def endofday(self, symbol, from_date, to_date):
        if symbol == "XOM":
            return [['begin', 'high', 'low', 'end'], [46.12, 54.54, 34.23, 45.1], [45.2, 46.44, 42.23, 43.1]]
        if symbol == "AAPL":
            return [['begin', 'high', 'low', 'end'], [146.12, 154.54, 134.23, 145.1], [145.2, 146.44, 142.23, 143.1]]
        return [['begin', 'high', 'low', 'end'], [6.12, 7.54, 5.23, 6.1], [7.2, 12.44, 3.23, 5.1]]

class RateLimitDecor:
    """
       Most APIs have quota and limits on requests. This class
        wraps an API provider class to ensure conformance.

        The rate is `limit` over `every`, where limit is the number of
        invocation allowed every `every` seconds.
        limit(4, 60) creates a decorator that limit the total API calls
        to 4 per minute. If not specified, every defaults to 1 second.
    """
    def limit_decor(self, fn):
        def wrapper(*args, **kwargs):
            self.semaphore.acquire()
            try:
                return fn(*args, **kwargs)
            finally:                   # ensure semaphore release
                timer = _threading.Timer(self.every, self.semaphore.release)
                timer.setDaemon(True)  # allows the timer to be canceled on exit
                timer.start()
        return wrapper

    def __init__(self, impl, limit, every=1):
        self.impl = impl
        self.limit = limit
        self.every = every
        self.semaphore = _threading.Semaphore(limit)

        for name in dir(impl):
            if name.startswith("_"):
                continue
            attr = getattr(impl, name)
            if not callable(attr):
                continue
            # invokable public API methods
            setattr(self, name, self.limit_decor(attr))


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    actor = MockAPI('aerae%4r')
    print('Mock API token = "{}"'.format(actor.api_key))
    rmActor = RateLimitDecor(actor, 5, 30)

    print(rmActor.endofday('XOM', 12, 32))

    print(rmActor.intraday('XOM'))

    print(rmActor.intraday('AAPL'))

    print(rmActor.endofday('XOM', 22, 42))

    print(rmActor.intraday('AAPL'))

    print(rmActor.intraday('XOM'))

    print(rmActor.endofday('CXW', 12, 32)) 
