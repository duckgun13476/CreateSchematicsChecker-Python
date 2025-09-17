from pydantic import ValidationError
import toml
from pydantic import BaseModel, Field
from typing import Optional
import time
from Checker.lib.setting.config_interface import import_toml, generate_config
from Checker.lib.setting.para_set import config_path


thread_pool = []


class ConfigModel(BaseModel):
    """
    Config Model for CSC
    """
    schematics_path: str = Field(..., description="蓝图存放路径")
    log_path: str = Field(..., description="日志存放路径")
    schematics_packet_size: int = Field(..., description="蓝图上传包大小")
    check_frequency: float = Field(..., description="扫描频率，单位为秒")
    fast_handle: bool = Field(..., description="是否快速清除禁用方块")
    count_block: bool = Field(..., description="是否统计方块信息")
    kill_entity: bool = Field(..., description="是否清理蓝图的实体")
    auto_update: bool = Field(..., description="是否自动更新规则")
    clear_tag_instead_remove: bool = Field(..., description="清除方块而不是禁用蓝图")
    ban_tags: list = Field(..., description="禁止的NBT标签列表")
    ban_entity: list = Field(..., description="禁止的实体列表")
    ban_block: list = Field(..., description="禁止的方块列表")

    smtp_enable: bool = Field(False, description="是否启用SMTP发送邮件")
    email_receive: Optional[str] = Field(None, description="接收邮件的地址")
    smtp_port: Optional[int] = Field(None, description="SMTP服务器端口")
    smtp_server: Optional[str] = Field(None, description="SMTP服务器地址")
    smtp_sender_email: Optional[str] = Field(None, description="发送邮件的邮箱地址")
    smtp_password: Optional[str] = Field(None, description="发送邮件的邮箱密码")

    uuid: str = Field(..., description="唯一标识符")


try:
    config_toml = import_toml(config_path)

    # generate_config('default.toml')
    # check if legal



except FileNotFoundError:
    generate_config(config_path)
    config_toml = import_toml(config_path)
except toml.TomlDecodeError as e:
    import traceback, sys

    print("INFO     配置文件解析发生异常，错误见下↓")
    print("-----------------------")
    print(f"ERROR    {e}")
    print("-----------------------")
    print("INFO     如何看懂报错:  [line 18 column 1 char 418]   此处错误发生在第18行")
    print("INFO     常见错误:  ")
    print(r"INFO     1.路径配置错误: windows内路径配置必须使用// 而不能使用反斜杠 ")
    print(r"INFO     因此 : C:\Users\123 是错误的 而 C://Users//123 是正确的")
    print(r"INFO     如果参数缺失或者不知道哪里出错了, 可将现存文件删除并让CSC重新生成最新的配置文件")
    print(r"INFO     配置文件在根目录下 config.toml")
    print("-----------------------")
    print(r"ERROR    因配置出现问题 CSC将在60秒后退出")
    time.sleep(60)
    sys.exit("error occur")
except Exception as e:
    print(f"ERROR    {e}")
    import traceback, sys

    traceback.print_exc()
    time.sleep(30)
    sys.exit("error occur")

try:
    config = ConfigModel.model_validate({
        **config_toml.get("path", {}),
        **config_toml.get("setting", {}),
        **config_toml.get("check", {}),
        **config_toml.get("smtp", {})
    })
except ValidationError as e:
    print('ERROR    配置文件校验错误，错误见下↓')
    print("-----------------------")
    for err in e.errors():
        print(f"ERROR    参数{err.get('loc')} 应当为 {err.get('type')}, "
              f"实际收到参数为 {err.get('input')}({type(err.get('input')).__name__})")
    print("-----------------------")
    print('INFO    如何看懂报错: ')
    print("INFO    检查配置文件中对应参数字段的值是否正确")
    print("INFO    如果报错中实际收到的参数为 None(NoneType) 则可能表示该参数缺失")
    print("INFO    如果参数缺失或者不知道哪里出错了, 可将现存文件删除并让CSC重新生成最新的配置文件")
    print("-----------------------")
    print("INFO    相关可能的参数类型有: ")
    print("INFO    str_type: 字符串")
    print("INFO    int_type: 整数")
    print("INFO    float_type: 浮点数")
    print("INFO    bool_type: 布尔值(True/False)")
    print("INFO    list_type: 列表(用逗号分隔)")
    print("-----------------------")
    print(r"ERROR    因配置出现问题 CSC将在60秒后退出")
    time.sleep(60)
    sys.exit("error occur")

if config.smtp_enable:
    if None in [config.email_receive, config.smtp_port, config.smtp_server,
                config.smtp_sender_email, config.smtp_password]:
        print("ERROR    SMTP配置不完整, 请检查配置文件!")
        import sys

        print(r"ERROR    因配置出现问题 CSC将在60秒后退出")
        time.sleep(60)
        sys.exit("error occur")

# 基础配置
try:
    # dev setting
    rule_path = r"rule/standard.yml"
    replace_schematic_path = r"rule/chanhuishu.nbt"
    schematic_sha_path = r"save/schematics.yml"

    # default setting
    # schematics_path = config_toml.get('path').get('schematics_path')
    # log_path = config_toml.get('path').get('log_path')  # 日志路径
    # schematics_packet_size = config_toml.get('setting').get('schematics_packet_size')  # 蓝图上传包大小
    # check_frequency = config_toml.get('check').get('check_frequency')  # 日志路径  # 针对文件的扫描频率 单位为秒
    # fast_handle = config_toml.get('check').get('fast_handle')  # 是否快速清除禁用方块
    # count_block = config_toml.get('check').get('count_block')  # 是否统计方块信息
    # kill_entity = config_toml.get('check').get('kill_entity')  # 是否清理蓝图的实体
    # ban_tags = config_toml.get('check').get('ban_tags')
    # ban_entity = config_toml.get('check').get('ban_entity')
    # ban_block = config_toml.get('check').get('ban_block')
    #
    # smtp_enable = config_toml.get('smtp', {}).get('enable')
    # email_receive = config_toml.get('smtp', {}).get('email_receive')
    # smtp_port = config_toml.get('smtp', {}).get('smtp_port')
    # smtp_server = config_toml.get('smtp', {}).get('smtp_server')
    # smtp_sender_email = config_toml.get('smtp', {}).get('smtp_sender_email')
    # smtp_password = config_toml.get('smtp', {}).get('smtp_password')
    #
    # uuid = config_toml.get('path').get('uuid')

except Exception as e:
    print(f"ERROR    {e}")
    import traceback, sys

    traceback.print_exc()
    time.sleep(30)
    sys.exit("error occur")

print("INFO     配置加载成功！")
