import json

from bson import ObjectId
from flask import Flask
from flask import request
from geventwebsocket.handler import WebSocketHandler
from geventwebsocket.websocket import WebSocket
from gevent.pywsgi import WSGIServer

from settings import Mongo_DB
from thirdpart_api.baidu_api import text2audio
from redis_msg import set_redis

ws_app = Flask(__name__)

user_socket_dict = {}


@ws_app.route("/app/<app_id>")
def app(app_id):
    user_socket = request.environ.get("wsgi.websocket")  # type: WebSocket
    if user_socket:
        user_socket_dict[app_id] = user_socket
    print(user_socket_dict)
    while 1:
        user_msg = user_socket.receive()
        print(user_msg)  # {to_user:"toy_id",chat:"asdf.mp3",from_user:""}
        msg_dict = json.loads(user_msg)
        toy_socket = user_socket_dict.get(msg_dict.get("to_user"))
        msg_dict["chat"] = _get_xxtx(msg_dict.get("to_user"), msg_dict.get("from_user"))
        toy_socket.send(json.dumps(msg_dict))
        set_redis(msg_dict.get("to_user"), msg_dict.get("from_user"))


@ws_app.route("/toy/<toy_id>")
def toy(toy_id):
    user_socket = request.environ.get("wsgi.websocket")  # type: WebSocket
    if user_socket:
        user_socket_dict[toy_id] = user_socket
    print(user_socket_dict)
    while 1:
        user_msg = user_socket.receive()
        print(user_msg)  # {to_user:"toy_id",music:"asdf.mp3"}
        msg_dict = json.loads(user_msg)
        toy_socket = user_socket_dict.get(msg_dict.get("to_user"))
        toy_socket.send(user_msg)
        set_redis(msg_dict.get("to_user"), msg_dict.get("from_user"))


def _get_xxtx(to_user, from_user):
    to_user_info = Mongo_DB.toys.find_one({"_id": ObjectId(to_user)})
    for friend in to_user_info.get("friend_list"):
        if friend.get("friend_id") == from_user:
            xxtx_str = f"你有来自{friend.get('friend_nick')}的新消息"
            filename = text2audio(xxtx_str)
            return filename

    xxtx_str = f"你有来自陌生人的消息"
    filename = text2audio(xxtx_str)
    return filename


if __name__ == '__main__':
    http_serv = WSGIServer(("0.0.0.0", 3721), ws_app,
                           handler_class=WebSocketHandler)
    http_serv.serve_forever()
