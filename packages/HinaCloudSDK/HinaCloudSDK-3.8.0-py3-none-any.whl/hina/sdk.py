# coding=utf-8
import base64
import gzip
import json
import random
import threading
import time
from enum import Enum

from hina.flush_thread import AsyncFlushThread

try:
    from urllib.parse import urlparse
    import queue
    import urllib.parse as urllib
    import urllib.request as urllib2
except ImportError:
    from urlparse import urlparse
    import Queue as queue
    import urllib
    import urllib2

SDK_LIB = 'python'
SDK_VERSION = '3.8.0'
SDK_LIB_METHOD = 'code'

INSTANCE_LOCK = threading.RLock()


class HinaCloudSDK(object):
    """
    初始化一个 HinaSdk 的实例
    """
    instance = None

    def __init__(self, config):
        self._config = config

    @staticmethod
    def init(url, batch=10, enable_log=False, flush_max_time=15):
        with INSTANCE_LOCK:
            if not HinaCloudSDK.instance:
                config = _HinaConfig(url, batch, enable_log, flush_max_time)
                HinaCloudSDK.instance = HinaCloudSDK(config)
                return HinaCloudSDK.instance
            raise HinaException("不能重复初始化HinaCloudSDK")

    def register_super_properties(self, super_properties):
        """
        设置每个事件都带有的一些公共属性，当 track 的 properties 和 super properties 有相同的 key 时，将采用 track 的

        :param super_properties 公共属性
        """
        if 'H_lib' in super_properties:
            del super_properties['H_lib']
        self._config.super_properties.update(super_properties)

    def send_event(self, user_uid, event_name, data, is_login, event_time):
        """
        发送事件
        :param user_uid: 用户id
        :param event_name: 事件名称
        :param data: 属性信息
        :param is_login: 是否登录
        :param event_time: 事件的时间，13位，单位毫秒
        :return:
        """
        all_properties = self._config.super_properties.copy()
        if data:
            if 'H_lib' in data:
                del data['H_lib']
            all_properties.update(data)
        event_record = self._config.build_event_record(event_type=EventType.TRACK.value, event_name=event_name,
                                                       event_time=event_time, properties=all_properties)
        if is_login:
            event_record["account_id"] = user_uid
        else:
            event_record["anonymous_id"] = user_uid
        if self._config.batch == 1:
            # 单条发送
            records = [self._config.json_dumps(event_record)]
            self._config.send(records)
        else:
            # 批量发送，队列里插入
            try:
                self._config.queue.put_nowait(self._config.json_dumps(event_record))
            except queue.Full as e:
                raise HinaException(e)
            if self._config.queue.qsize() >= self._config.batch:
                self._config.need_flush.set()

    def bind_id(self, account_id, anonymous_id):
        """
        设置用户ID
        :param account_id: 登录ID
        :param anonymous_id: 匿名ID
        :return:
        """
        event_record = self._config.build_event_record(anonymous_id=anonymous_id, account_id=account_id,
                                                       event_type=EventType.TRACK_SIGNUP.value, event_name='H_SignUp')
        records = [self._config.json_dumps(event_record)]
        self._config.send(records)

    def user_set(self, account_id, data):
        """
        设置用户属性
        :param account_id: 用户ID
        :param data: 用户属性
        :return:
        """
        event_record = self._config.build_event_record(account_id=account_id, event_type=EventType.USER_SET.value,
                                                       properties=data)
        records = [self._config.json_dumps(event_record)]
        self._config.send(records)

    def user_set_once(self, account_id, data):
        """
        首次设置用户属性
        :param account_id: 用户ID
        :param data: 用户属性
        :return:
        """
        event_record = self._config.build_event_record(account_id=account_id, event_type=EventType.USER_SET_ONCE.value,
                                                       properties=data)
        records = [self._config.json_dumps(event_record)]
        self._config.send(records)

    def user_add(self, account_id, key, value):
        """
        对当前用户的属性做递增或者递减（数值类型的属性）
        :param account_id: 用户ID
        :param key: 用户属性KEY
        :param value: 属性值，数值型
        :return:
        """
        data = {key: value}
        event_record = self._config.build_event_record(account_id=account_id, event_type=EventType.USER_ADD.value,
                                                       properties=data)
        records = [self._config.json_dumps(event_record)]
        self._config.send(records)

    def user_unset(self, account_id, key):
        """
        取消用户属性
        :param account_id: 用户ID
        :param key: 用户属性KEY
        :return:
        """
        data = {key: True}
        event_record = self._config.build_event_record(account_id=account_id, event_type=EventType.USER_UNSET.value,
                                                       properties=data)
        records = [self._config.json_dumps(event_record)]
        self._config.send(records)

    def flush(self):
        if self._config.batch > 1:
            self._config.need_flush.set()

    def close(self):
        """
        需要退出时调用此方法
        """
        if self._config.batch > 1:
            # 关闭时首先停止发送线程
            self._config.flushing_thread.stop()
            # 循环发送，直到队列为空
            while not self._config.queue.empty():
                self._config.sync_flush()


class _HinaConfig(object):
    def __init__(self, url, batch, enable_log, flush_max_time):
        """
        :param url: 数据接收地址
        :param batch: 批量发送的值
        :param enable_log: 是否控制台打log，会显示发送的数据
        :param flush_max_time: 自动flush的最大间隔时间，单位秒，最小5秒。
        """
        self.url = url
        self.batch = max(1, batch)
        self.enable_log = enable_log
        self.request_timeout = 10
        self.super_properties = {
            'H_lib': SDK_LIB,
            'H_lib_version': SDK_VERSION,
            "H_lib_method": SDK_LIB_METHOD,
        }
        if self.batch > 1:
            self.queue = queue.Queue()
            self.flush_max_time = max(5, flush_max_time)
            # 用于通知刷新线程应当立即进行刷新
            self.need_flush = threading.Event()
            # 初始化发送线程，并设置为 Daemon 模式
            self.flushing_thread = AsyncFlushThread(self)
            self.flushing_thread.daemon = True
            self.flushing_thread.start()

    def build_event_record(self, anonymous_id=None, account_id=None, event_type=None, event_name=None,
                           event_time=None, properties=None):
        return {
            '_track_id': self._generate_unique_id(),
            'anonymous_id': anonymous_id,
            'account_id': account_id,
            'type': event_type,
            'event': event_name,
            'time': event_time or self._now(),
            'send_time': self._now(),
            'properties': properties
        }

    def send(self, msg):
        result = False
        response = self._do_request({
            'gzip': 1,
            'data': self._encode_msg_list(msg),
        })
        ret_code = response.code
        ret_content = response.read().decode('utf8')
        if ret_code == 200 and ret_content and json.loads(ret_content).get("success"):
            result = True
            if self.enable_log:
                print('valid message: %s' % msg)
        else:
            if self.enable_log:
                print('invalid message: %s' % msg)
                print('ret_code: %s' % ret_code)
                print('ret_content: %s' % ret_content)
        if ret_code >= 300:
            print('invalid message: %s' % msg)
            print('ret_code: %s' % ret_code)
        return result

    def _do_request(self, data):
        """
        使用 urllib 发送数据给服务器，如果发生错误会抛出异常。
        """
        encoded_data = urllib.urlencode(data).encode('utf8')
        try:
            request = urllib2.Request(self.url, encoded_data)
            if self.request_timeout is not None:
                response = urllib2.urlopen(request, timeout=self.request_timeout)
            else:
                response = urllib2.urlopen(request)
        except urllib2.HTTPError as e:
            raise HinaException(e)
        return response

    def sync_flush(self):
        """
        执行一次同步发送
        """
        flush_success = True
        flush_buffer = []
        for _ in range(max(self.batch, 100)):
            if self.queue.empty():
                break
            flush_buffer.append(self.queue.get_nowait())
        if len(flush_buffer) > 0:
            flush_success = self.send(flush_buffer)
        return flush_success

    @staticmethod
    def _now():
        return int(time.time() * 1000)

    @staticmethod
    def json_dumps(data):
        return json.dumps(data, separators=(',', ':'))

    def _encode_msg(self, msg):
        return base64.b64encode(self._gzip_string(msg.encode('utf8')))

    def _encode_msg_list(self, msg_list):
        return base64.b64encode(self._gzip_string(('[' + ','.join(msg_list) + ']').encode('utf8')))

    @staticmethod
    def _gzip_string(data):
        try:
            return gzip.compress(data)
        except AttributeError:
            import StringIO

            buf = StringIO.StringIO()
            fd = gzip.GzipFile(fileobj=buf, mode="w")
            fd.write(data)
            fd.close()
            return buf.getvalue()

    def _generate_unique_id(self):
        return str(self._now()) + str(random.randint(1000, 9999))


class EventType(Enum):
    TRACK = "track"
    TRACK_SIGNUP = "track_signup"
    USER_SET = "user_set"
    USER_SET_ONCE = "user_setOnce"
    USER_ADD = "user_add"
    USER_UNSET = "user_unset"


class HinaException(Exception):
    pass
