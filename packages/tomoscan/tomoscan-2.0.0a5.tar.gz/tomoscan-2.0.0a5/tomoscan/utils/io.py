import logging
import traceback
import threading
import functools
from contextlib import ExitStack, contextmanager


class SharedLockPool:
    """
    Allows to acquire locks identified by name (hashable type) recursively.
    """

    def __init__(self):
        self.__locks = {}
        self.__locks_mutex = threading.Semaphore(value=1)

    def __len__(self):
        return len(self.__locks)

    @property
    def names(self):
        return list(self.__locks.keys())

    @contextmanager
    def _modify_locks(self):
        self.__locks_mutex.acquire()
        try:
            yield self.__locks
        finally:
            self.__locks_mutex.release()

    @contextmanager
    def acquire(self, name):
        with self._modify_locks() as locks:
            lock = locks.get(name, None)
            if lock is None:
                locks[name] = lock = threading.RLock()
        lock.acquire()
        try:
            yield
        finally:
            lock.release()
            with self._modify_locks() as locks:
                if name in locks:
                    locks.pop(name)

    @contextmanager
    def acquire_context_creation(self, name, contextmngr, *args, **kwargs):
        """
        Acquire lock only during context creation.

        This can be used for example to protect the opening of a file
        but not hold the lock while the file is open.
        """
        with ExitStack() as stack:
            with self.acquire(name):
                ret = stack.enter_context(contextmngr(*args, **kwargs))
            yield ret


depreclog = logging.getLogger("nxtomo.DEPRECATION")

deprecache = set([])


def deprecated_warning(
    type_,
    name,
    reason=None,
    replacement=None,
    since_version=None,
    only_once=True,
    skip_backtrace_count=0,
):
    """
    Function to log a deprecation warning

    :param str type_: Nature of the object to be deprecated:
        "Module", "Function", "Class" ...
    :param name: Object name.
    :param str reason: Reason for deprecating this function
        (e.g. "feature no longer provided",
    :param str replacement: Name of replacement function (if the reason for
        deprecating was to rename the function)
    :param str since_version: First *silx* version for which the function was
        deprecated (e.g. "0.5.0").
    :param bool only_once: If true, the deprecation warning will only be
        generated one time for each different call locations. Default is true.
    :param int skip_backtrace_count: Amount of last backtrace to ignore when
        logging the backtrace
    """
    if not depreclog.isEnabledFor(logging.WARNING):
        # Avoid computation when it is not logged
        return

    msg = "%s %s is deprecated"
    if since_version is not None:
        msg += " since silx version %s" % since_version
    msg += "."
    if reason is not None:
        msg += " Reason: %s." % reason
    if replacement is not None:
        msg += " Use '%s' instead." % replacement
    msg += "\n%s"
    limit = 2 + skip_backtrace_count
    backtrace = "".join(traceback.format_stack(limit=limit)[0])
    backtrace = backtrace.rstrip()
    if only_once:
        data = (msg, type_, name, backtrace)
        if data in deprecache:
            return
        else:
            deprecache.add(data)
    depreclog.warning(msg, type_, name, backtrace)


def deprecated(
    func=None,
    reason=None,
    replacement=None,
    since_version=None,
    only_once=True,
    skip_backtrace_count=1,
):
    """
    Decorator that deprecates the use of a function

    :param str reason: Reason for deprecating this function
        (e.g. "feature no longer provided",
    :param str replacement: Name of replacement function (if the reason for
        deprecating was to rename the function)
    :param str since_version: First *silx* version for which the function was
        deprecated (e.g. "0.5.0").
    :param bool only_once: If true, the deprecation warning will only be
        generated one time. Default is true.
    :param int skip_backtrace_count: Amount of last backtrace to ignore when
        logging the backtrace
    """

    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            deprecated_warning(
                type_="Function",
                name=func.__name__,
                reason=reason,
                replacement=replacement,
                since_version=since_version,
                only_once=only_once,
                skip_backtrace_count=skip_backtrace_count,
            )
            return func(*args, **kwargs)

        return wrapper

    if func is not None:
        return decorator(func)
    return decorator
