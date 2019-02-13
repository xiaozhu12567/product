import tornado.websocket
import tornado.escape
import uuid
from pycket.session import SessionMixin

from .main import AuthBaseHandler

class RoomHandler(AuthBaseHandler):
    """
    聊天室页面
    """
    def get(self, *args, **kwargs):
        self.render('room.html', messages=ChatSocketHandler.history)


class ChatSocketHandler(tornado.websocket.WebSocketHandler, SessionMixin):
    """
    处理响应websocket连接
    """
    waiters = set()     # 等待接收用户信息
    history = []        # 历史消息列表
    history_size = 200  # 消息列表大小

    def get_current_user(self):
        return self.session.get('user', None)

    def open(self, *args, **kwargs):
        """新的websocket连接打开，自动调用"""
        print("new ws connection: %s" % self)
        ChatSocketHandler.waiters.add(self)

    def on_close(self):
        """websocket连接断开，自动调用"""
        print("close ws connection: %s" % self)
        ChatSocketHandler.waiters.remove(self)

    def on_message(self, message):
        """客户端发送消息时，自动调用"""
        print("got message:%s" % message)
        parsed = tornado.escape.json_decode(message)    # 将json转换成python字典
        chat = {
            'id': str(uuid.uuid4()),
            'body': parsed['body'],
        }
        msg = {
            'html': tornado.escape.to_basestring(
                self.render_string('message.html', message=chat, user=self.current_user)
            ),
            'id': chat['id']
        }

        ChatSocketHandler.update_history(msg)
        ChatSocketHandler.send_updates(msg)

    @classmethod        # 定一个类方法
    def send_updates(cls, msg):
        """给每个等待接受的用户发新的消息"""
        for w in ChatSocketHandler.waiters:
            w.write_message(msg)

    @classmethod
    def update_history(cls, msg):
        """
        更新消息列表，加入新的消息
        :param msg:
        :return:
        """
        cls.history.append(msg)
        if len(cls.history) > cls.history_size:
            cls.history = cls.history[-cls.history_size]