import requests
from Checker.lib.log_color import log

BASE_URL = "https://api.starrylandmc.xyz/nbt_filter"

def get_latest_version():
    """获取最新的文件版本信息"""
    response = requests.get(f"{BASE_URL}/get_latest_version")
    if response.status_code == 200:
        return response.json()
    else:
        return {"code": response.status_code, "msg": "请求失败"}

def get_latest_rule():
    """获取最新的规则文件"""
    response = requests.get(f"{BASE_URL}/get_latest_rule")
    if response.status_code == 200:
        return response.json()
    else:
        return {"code": response.status_code, "msg": "请求失败"}

def update_latest_rule(data, secret=None):
    """更新最新的规则文件"""
    params = {}
    if secret:
        params['secret'] = secret
    response = requests.post(f"{BASE_URL}/post_latest_rule", params=params, data=data)
    if response.status_code == 200:
        return response.json()
    else:
        return {"code": response.status_code, "msg": "请求失败"}


def version_handler_in():
    try:
        version_info = get_latest_version().get('version')
        if version_info is None:
            version_info = 0
    except Exception as e:
        version_info = 0
        if "Connection aborted" in str(e):
            log.error("暂时无法获取到版本信息")
        else:
            log.error(e)
    return version_info

# 示例用法
if __name__ == "__main__":
    # 获取最新版本信息

    print("最新版本信息:", version_handler_in())


"""    # 获取最新规则文件
    rule_info = get_latest_rule()
    print("最新规则文件:", rule_info)

    # 更新最新规则文件
    new_rule_data = "这里是新的规则文件的内容"  # 替换为实际规则文件内容
    update_response = update_latest_rule(new_rule_data, secret="你的密钥")  # 可选的密钥
    print("更新规则文件的响应:", update_response)
"""