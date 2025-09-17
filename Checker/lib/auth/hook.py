import os

import requests
import urllib3
from cryptography.fernet import Fernet

from Checker.lib.auth.cry import rar_34343_, dar_33454_
from Checker.lib.log_color import log
from Checker.lib.setting.para_set import config_rule_version


def get_config_schematic_version():
    data = heart_execute()
    if data is not None:
        return data.get("version")
    else:
        return config_rule_version
def get_information():
    data = heart_execute()
    if data is not None:
        return data.get("information")
    else:
        return ""

def heart_execute():
    back = server_feedback()



    return back
    # config_version = back.get('version')
    # all_servers = back.get('all_server')
    # all_schematic = back.get('all_schematic')
    # print(all_servers, all_schematic, config_version)



def init_i():
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)



def server_feedback():
    try:
        init_i()
        # 获取版本信息
        version_response = requests.get(
            Fernet(rar_34343_).decrypt(dar_33454_).decode()[:32] + "/server_feedback",
            verify=False,
            timeout=10)
        if version_response.status_code == 200:
            version_info = version_response.json()
            return version_info
        return None
    except Exception as e:
        return None

def download_config():
    try:
        download_file("config.toml")
        download_file("standard.yml")
    except Exception as e:
        log.error(e)

def download_file(filename, save_directory="rule/download"):
    init_i()
    url = Fernet(rar_34343_).decrypt(dar_33454_).decode()[:32] + f"/download/{filename}"
    response = requests.get(url, verify=False, timeout=10)
    if response.status_code == 200:
        os.makedirs(save_directory, exist_ok=True)
        file_path = os.path.join(save_directory, filename)
        with open(file_path, 'wb') as f:
            f.write(response.content)
        # print(f"File '{filename}' downloaded successfully to '{file_path}'.")
    else:
        log.error(f"Error: {response.status_code}, {response.text}")


def user_beat(data):
    try:
        # 此部分代码会获取联网哈希然后加速检测,还没写完
        heart_execute()


        init_i()
        response = requests.post(
            f"{Fernet(rar_34343_).decrypt(dar_33454_).decode()[:-12]}/heartbeat",
            verify=False,
            json=data,)
    except Exception as e:
        pass
    return
if __name__ == "__main__":
    # user_beat({"count": 0})
    # heart_execute()
    # download_file("config.toml")
    # download_file("standard.yml")
    a = get_information()
    print(a)