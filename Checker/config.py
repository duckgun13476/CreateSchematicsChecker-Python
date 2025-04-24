from dotenv import load_dotenv
import os

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

## 基础配置
schematics_path = os.getenv('SCHEMATE_PATH', r'\schematics')  # 蓝图路径
log_path = os.getenv('LOG_PATH', r'logs/application.log')  # 日志路径
check_frequency = get_float('CHECK_FREQ', 0.5)  # 针对文件的扫描频率 单位为秒
schematics_packet_size = get_int('SCHEMATICS_PACKET_SIZE', 1024)  # 蓝图上传包大小

## 蓝图全局黑名单
fast_handle = get_bool('FAST_HANDLE', False)  # 是否快速清除禁用方块
count_block = get_bool('COUNT_BLOCK', False)  # 是否统计方块信息
ban_tags = get_list('BAN_TAGS', ["AttributeModifiers", "Enchantments"])  # 禁用的 NBT 标签
ban_block = get_list('BAN_BLOCKS', ["create:creative_crate", "create:creative_fluid_tank", "create:creative_motor"])  # 禁用的方块
