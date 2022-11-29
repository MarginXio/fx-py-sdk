# -*- coding: utf-8 -*-
from queue import Queue
from collections import deque


class RingBuffer(deque):
    """
    python的ring buffer高性能封装
    注意：deque性能远高于封装的RingBuffer类，因此应尽量使用原始的deque对象
    为性能考虑，应注释一切代理的方法(i.e. append, get)，程序中应直接使用deque原始支持的方法
    参考：https://en.wikipedia.org/wiki/Circular_buffer
    # def append(self, x):
        # super().append(x)
    """
    def __init__(self, maxlen):
        super().__init__(maxlen=maxlen)


class WrappedQueue(Queue):
    """先进先出队列"""
    def __init__(self, max_len):
        super().__init__(max_len)

    def clear(self):
        self.queue.clear()

    def append(self, item):
        self.put_nowait(item)

    def notify_all(self):
        try:
            with self.not_empty:
                self.not_empty.notify_all()
        except Exception as e:
            print(f"WrappedQueue notify_all error：{e}")
            pass


class WrappedRingBuffer(object):
    """Ring Buffer: wrapped Deque implementation.
    Args:
        maxsize (int): maximum size of the queue. If zero, size is unboundend.
    """
    def __init__(self, maxsize=0):
        self.maxsize = maxsize
        self.actor = _DeQueActor(maxsize)

    def __len__(self):
        return self.size()

    def size(self):
        """The size of the queue."""
        return self.actor.qsize

    def qsize(self):
        """The size of the queue."""
        return self.size()

    def list(self):
        return self.actor.list()

    def empty(self):
        """Whether the queue is empty."""
        return self.actor.qsize

    def full(self):
        """Whether the queue is full."""
        return self.actor.full

    def put(self, item, block=True, timeout=None):
        """Adds an item to the queue.
        Uses polling if block=True, so there is no guarantee of order if
        multiple producers put to the same full queue.
        Raises:
            Full if the queue is full and blocking is False.
        """
        if self.maxsize <= 0:
            self.actor.put(item)
        elif not block:
            if not self.actor.put(item):
                # raise Full
                pass
        elif timeout is None:
            # Polling
            # Use a not_full condition variable or promise?
            while not self.actor.put(item):
                # Consider adding time.sleep here
                pass
        elif timeout < 0:
            raise ValueError("'timeout' must be a non-negative number")
        else:
            endtime = time.time() + timeout
            # Polling
            # Use a condition variable or switch to promise?
            success = False
            while not success and time.time() < endtime:
                success = self.actor.put(item)
            if not success:
                # raise Full
                pass

    def append(self, item):
        self.put(item)

    def get(self, block=True, timeout=None):
        """Gets an item from the queue.
        Uses polling if block=True, so there is no guarantee of order if
        multiple consumers get from the same empty queue.
        Returns:
            The next item in the queue.
        Raises:
            Empty if the queue is empty and blocking is False.
        """
        if not block:
            success, item = self.actor.get()
            if not success:
                # raise Empty
                item = None
        elif timeout is None:
            # Polling
            # Use a not_empty condition variable or return a promise?
            success, item = self.actor.get()
            while not success:
                # Consider adding time.sleep here
                success, item = self.actor.get()
        elif timeout < 0:
            raise ValueError("'timeout' must be a non-negative number")
        else:
            endtime = time.time() + timeout
            # Polling
            # Use a not_full condition variable or return a promise?
            success = False
            while not success and time.time() < endtime:
                success, item = self.actor.get()
            if not success:
                # raise Empty
                item = None
        return item

    def put_nowait(self, item):
        """Equivalent to put(item, block=False).
        Raises:
            Full if the queue is full.
        """
        return self.put(item, block=False)

    def get_nowait(self):
        """Equivalent to get(item, block=False).
        Raises:
            Empty if the queue is empty.
        """
        return self.get(block=False)

    def clear(self):
        self.actor.clear()


class _DeQueActor(object):
    def __init__(self, maxsize):
        self.maxsize = maxsize
        self._init(maxsize)

    # Override these for different queue implementations
    def _init(self, maxsize):
        self.queue = deque(maxlen=maxsize)

    def list(self):
        return self.queue

    def qsize(self):
        return self._qsize()

    def empty(self):
        return not self._qsize()

    def full(self):
        return False

    def put(self, item):
        self._put(item)
        return True

    def get(self):
        if not self._qsize():
            return False, None
        return True, self._get()

    def clear(self):
        self.queue.clear()

    def _qsize(self):
        return len(self.queue)

    def _put(self, item):
        self.queue.append(item)

    def _get(self):
        return self.queue.popleft()

