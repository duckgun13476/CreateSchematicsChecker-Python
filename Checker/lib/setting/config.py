import toml
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
except toml.TomlDecodeError as e:
    import traceback,time,sys
    print(f"INFO     配置文件解析发生异常，错误见下↓")
    print(f"-----------------------")
    print(f"ERROR    {e}")
    print(f"-----------------------")
    print(f"INFO     如何看懂报错： [line 18 column 1 char 418]   此处错误发生在第18行")
    print(r"INFO     常见错误： ")
    print(r"INFO     1.路径配置错误：windows内路径配置必须使用// 而不能使用反斜杠 ")
    print(r"INFO     因此 ：C:\Users\123 是错误的 而 C://Users//123 是正确的")
    print(f"-----------------------")
    print(r"ERROR    因配置出现问题 CSC将在60秒后退出")
    time.sleep(60)
    sys.exit("error occur")
except Exception as e:
    print(f"ERROR    {e}")
    import traceback,time,sys
    traceback.print_exc()
    time.sleep(30)
    sys.exit("error occur")

## 基础配置
try:
    # dev setting
    rule_path = r"rule/standard.yml"
    replace_schematic_path = r"rule/chanhuishu.nbt"
    schematic_sha_path = r"save/schematics.yml"



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

    uuid= config_toml.get('path').get('uuid')



    if None in [schematics_path, log_path, schematics_packet_size,
                check_frequency, fast_handle, count_block, kill_entity,
                ban_tags, ban_entity, ban_block,
                smtp_enable, email_receive, smtp_port, smtp_server,
                smtp_sender_email, smtp_password,uuid]:
        print("ERROR    配置文件异常，将使用重新生成的文件！")

    print("INFO     配置加载成功！")


except Exception as e:
    print(f"ERROR    {e}")
    import traceback,time,sys
    traceback.print_exc()
    time.sleep(30)
    sys.exit("error occur")





