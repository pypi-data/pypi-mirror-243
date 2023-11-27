import threading


class AsyncFlushThread(threading.Thread):

    def __init__(self, sdk):
        super(AsyncFlushThread, self).__init__()
        self._sdk = sdk
        # 用于实现安全退出
        self._stop_event = threading.Event()

    def stop(self):
        """
        需要退出时调用此方法，以保证线程安全结束。
        """
        self._stop_event.set()

    def run(self):
        while True:
            # 如果 need_flush 标志位为 True，或者等待超过 flush_max_time，则继续执行
            self._sdk.need_flush.wait(self._sdk.flush_max_time)
            # 进行发送，如果成功则清除标志位
            if self._sdk.sync_flush():
                self._sdk.need_flush.clear()
            # 发现 stop 标志位时安全退出
            if self._stop_event.isSet():
                break
