import requests
import para
import yaml

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



def save_data_to_yaml(rule_info, file_path):
    """将规则数据保存到指定的 YAML 文件中"""
    try:
        # 提取 'data' 内的信息
        data_content = rule_info

        # 去除多余的空行
        data_content = "\n".join(line for line in data_content.splitlines() if line.strip())

        # 直接将内容写入 YAML 文件
        with open(file_path, 'w', encoding='utf-8') as file:
            file.write(data_content + "\n")  # 添加一个换行符以保持文件格式

        log.info(f"规则数据已保存到: {file_path}")
    except Exception as e:
        log.error(f"保存规则数据时出错: {e}")

def convert_file_to_data(file_path):
    """将文件内容读取为字符串，并将空格和换行符替换为 \n 和 \r"""
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            # 读取文件内容
            content = file.read()

        # 替换空格和换行符
        # formatted_content = content.replace(' ', '\\n').replace('\n', '\\r\n')

        # 构建符合 data 结构的字符串
        data_content = f"{content}"

        return data_content
    except Exception as e:
        log.error(f"读取文件时出错: {e}")
        return None

# 示例用法
if __name__ == "__main__":

    # 获取最新版本信息
    print("最新版本信息:", version_handler_in())
    print( float(version_handler_in())


    )



    # 更新最新规则文件

    # 获取最新规则文件
    # rule_info = get_latest_rule().get('data')
    # print("最新规则文件:", rule_info)
    # file_path = 'latest_rule.yml'
    # save_data_to_yaml(rule_info, file_path)

    # 推送最新的规则
    # rule_info = convert_file_to_data(f"rule/standard.yml")
    # update_response = update_latest_rule(rule_info, secret=para.secret)  # 可选的密钥
    # print("更新规则文件的响应:", update_response)
