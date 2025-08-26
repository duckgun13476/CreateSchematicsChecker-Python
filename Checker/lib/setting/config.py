from dotenv import load_dotenv
import os
from Checker.lib.setting.config_interface import import_toml, generate_config

# Load environment variables from .env file
load_dotenv()

## Helper functions to parse environment variables
def get_bool(env_var, default=False):
    """Parse a boolean value from an environment variable."""
    value = os.getenv(env_var, str(default)).lower()
    return value in ['true', '1', 'True', 'yes']

def get_list(env_var, default=None, delimiter=','):
    """Parse a list from an environment variable."""
    value = os.getenv(env_var)
    if value:
        return [item.strip() for item in value.split(delimiter)]
    return default if default is not None else []

def get_int(env_var, default=0):
    """Parse an integer value from an environment variable."""
    try:
        return int(os.getenv(env_var, default))
    except ValueError:
        return default

def get_float(env_var, default=0.0):
    """Parse a float value from an environment variable."""
    try:
        return float(os.getenv(env_var, default))
    except ValueError:
        return default





config_path = "config.toml"

thread_pool = []


try:
    config_toml = import_toml(config_path)
except FileNotFoundError:
    generate_config(config_path)
    config_toml = import_toml(config_path)



## 基础配置

# dev setting
rule_path = r"Checker/rule/standard.yml"
schematic_sha_path = r"Checker/rule/schematics.yml"
replace_schematic_path = r"Checker/rule/chanhuishu.nbt"
# default setting


schematics_path = config_toml.get('path').get('schematics_path')
log_path = config_toml.get('path').get('log_path') # 日志路径
schematics_packet_size = config_toml.get('setting').get('schematics_packet_size')  # 蓝图上传包大小
check_frequency = config_toml.get('check').get('check_frequency') # 日志路径  # 针对文件的扫描频率 单位为秒
fast_handle = config_toml.get('check').get('fast_handle')  # 是否快速清除禁用方块
count_block = config_toml.get('check').get('count_block') # 是否统计方块信息
kill_entity = config_toml.get('check').get('kill_entity') # 是否清理蓝图的实体
ban_tags = config_toml.get('check').get('ban_tags')
ban_entity = config_toml.get('check').get('ban_entity')
ban_block = config_toml.get('check').get('ban_block')

smtp_enable = config_toml.get('smtp').get('enable')
email_receive = config_toml.get('smtp').get('email_receive')
smtp_port = config_toml.get('smtp').get('smtp_port')
smtp_server = config_toml.get('smtp').get('smtp_server')
smtp_sender_email = config_toml.get('smtp').get('smtp_sender_email')
smtp_password = config_toml.get('smtp').get('smtp_password')



if None in [schematics_path, log_path, schematics_packet_size,
            check_frequency, fast_handle, count_block, kill_entity,
            ban_tags, ban_entity, ban_block,
            smtp_enable, email_receive, smtp_port, smtp_server,
            smtp_sender_email, smtp_password]:
    print("ERROR    配置文件异常，将使用重新生成的文件！")

print("INFO     配置加载成功！")


