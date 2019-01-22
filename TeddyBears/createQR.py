import time
import hashlib
import os
from uuid import uuid4

import requests

from settings import Mongo_DB
from settings import LT_URL
from settings import QR_PATH


def create_code(count):
    qr_list = []
    for i in range(count):
        qr_code = hashlib.md5(
            f"{uuid4()}{time.time()}{uuid4()}".encode("utf8")).hexdigest()
        res = requests.get(LT_URL % qr_code)
        qr_path = os.path.join(QR_PATH, f"{qr_code}.jpg")

        with open(qr_path, "wb") as f:
            f.write(res.content)

        qr_dict = {"device_key": qr_code}
        qr_list.append(qr_dict)
        time.sleep(0.5)

    Mongo_DB.devices.insert_many(qr_list)


create_code(10)
