import toml

from Checker.lib.math.func import generate_random_string


def export_toml(data, filename):
    """将字典导出为 TOML 文件"""
    with open(filename, "w", encoding="utf-8") as f:  # 指定 UTF-8 编码
        toml.dump(data, f)  # 使用 dump 直接写入文件
    print(f"INFO     配置文件已生成：{filename}")

def import_toml(filename):
    """从 TOML 文件导入数据"""
    with open(filename, "r", encoding="utf-8") as f:  # 指定 UTF-8 编码
        config = toml.load(f)  # 使用 load 读取文件
    return config

def add_comment_to_toml(filename, variable, comment):
    """在匹配的变量上方添加注释"""
    try:
        with open(filename, "r", encoding="utf-8") as f:
            lines = f.readlines()
        with open(filename, "w", encoding="utf-8") as f:
            for line in lines:
                if variable in line:
                    f.write(f"# {comment}\n")
                f.write(line)
    except Exception as e:
        print(f"添加注释发生错误：{e}")

def add_comment_to_toml_r(filename, variable, comment):
    """在匹配的变量行的最右侧添加注释"""
    try:
        with open(filename, "r", encoding="utf-8") as f:
            lines = f.readlines()

        with open(filename, "w", encoding="utf-8") as f:
            for line in lines:
                if variable in line:
                    # 在行尾添加注释
                    line = line.rstrip() + f"  # {comment}\n"
                f.write(line)
    except Exception as e:
        print(f"添加注释发生错误：{e}")

def format_toml(filename):
    """整理 TOML 文件格式，使数组元素换行并缩进"""
    try:
        with open(filename, "r", encoding="utf-8") as f:
            lines = f.readlines()
        formatted_lines = []
        for line in lines:
            if "=" in line and ("[" in line and "]" in line):
                key, value = line.split("=", 1)
                key = key.strip()
                value = value.strip()
                if value.startswith("[") and value.endswith("]"):
                    array_content = value[1:-1].strip()
                    elements = [elem.strip() for elem in array_content.split(",") if elem.strip()]
                    formatted_array = ",\n    ".join(elements)
                    formatted_line = f"{key} = [\n    {formatted_array}\n]\n"
                    formatted_lines.append(formatted_line)
                else:
                    formatted_lines.append(line)
            else:
                formatted_lines.append(line)
        with open(filename, "w", encoding="utf-8") as f:
            f.writelines(formatted_lines)
    except Exception as e:
        print(f"文件整理发生错误：{e}")


def generate_config(config_path):
    data = {
        "path": {
            "schematics_path": r'experiment/schematics/uploaded',
            "log_path": r'logs/application.log',
            "uuid":f"{generate_random_string(8)}-{generate_random_string(8)}-{generate_random_string(8)}-{generate_random_string(8)}",
        },
        "setting": {
            "schematics_packet_size": 1024,
        },
        "check": {
            "check_frequency": 0.5,
            "fast_handle": False,
            "count_block": False,
            "kill_entity": True,
            "ban_entity": ['minecraft:armor_stand'],
            "ban_tags": ["AttributeModifiers", "Enchantments", "using_converts_to", "bundle_contents","run_command"],
            "ban_block": [
                "create:creative_crate",
                "create:creative_fluid_tank",
                "create_integrated_farming:chicken_roost", # 1.21特别添加 阻止gt机卡服
                "create:creative_motor",
                "create:creative_blaze_cake",
                "create:handheld_worldshaper",
                "minecraft:command_block",
                "minecraft:kelp"  # 这可以阻止动态结构放置含水方块, 从而阻止绝大部分gt刷石机（因为它们非常非常卡）
            ]
        },
        "smtp": {
            "enable": False,
            "email_receive": "example@qq.com",
            "smtp_server": 'smtp.qq.com',
            "smtp_port": 587,
            "smtp_sender_email": '<EMAIL>',
            "smtp_password": '<PASSWORD>',
        }
    }

    # 导出数据到 TOML 文件
    export_toml(data, config_path)
    format_toml(config_path)


    add_comment_to_toml(config_path, "[path]", "#################################")
    add_comment_to_toml(config_path, "[path]", "注意事项：：")
    add_comment_to_toml(config_path, "[path]", "")
    add_comment_to_toml(config_path, "[path]", "启动此脚本的部分功能会导致一些问题：")
    add_comment_to_toml(config_path, "[path]", "  创造模式不能打印实体、蓝图不能包含附魔标签")
    add_comment_to_toml(config_path, "[path]", "")
    add_comment_to_toml(config_path, "[path]", "1.附魔标签黑名单：因为附魔标签结构复杂，与创造蓝图的结构完全一致，因此为了根除创造蓝图，带有任何附魔标签的蓝图无法打印！")
    add_comment_to_toml(config_path, "[path]", "")
    add_comment_to_toml(config_path, "[path]", "2.剔除全部实体：因为实体的nbt标签极其复杂，无法根除全部复制漏洞，因此为了根除实体bug，只能剔除蓝图的打印实体功能")
    add_comment_to_toml(config_path, "[path]", "  但这可以阻止玩家恶意修改极长的nbt附魔标签作为过滤器导致服务器卡死！")
    add_comment_to_toml(config_path, "[path]", "")
    add_comment_to_toml(config_path, "[path]", "#################################")

    add_comment_to_toml(config_path, "uuid", "你的用户ID，自动生成不需要改，用于同步来自其他服务器的蓝图校验结果")


    add_comment_to_toml(config_path, "[path]", "路径配置")
    add_comment_to_toml(config_path, "schematics_path", "蓝图路径，可以为相对路径或绝对路径，指向upload文件夹")
    add_comment_to_toml(config_path, "schematics_path", "upload文件夹在服务器的 schematics 文件夹内")
    add_comment_to_toml(config_path, "schematics_path", "示例：服务器文件夹/schematics/uploaded")

    add_comment_to_toml(config_path, "log_path", "日志路径，默认在logs文件夹内，但可以输出到设定的路径")

    add_comment_to_toml(config_path, "[setting]", "关键配置，自动获取")
    add_comment_to_toml(config_path, "schematics_packet_size", "蓝图的上传带宽，必须和服务器一致，如果无法自动获取，将采用此处的值！")
    add_comment_to_toml(config_path, "schematics_packet_size", "默认的带宽为1024，如果你修改了服务器的配置，此处必须和服务器一致")
    add_comment_to_toml(config_path, "schematics_packet_size", "配置图形化界面在create>server>Schematics 本地toml 直接搜索 maxSchematicPacketSize 即可")

    add_comment_to_toml(config_path, "[check]", "核心配置")
    add_comment_to_toml(config_path, "check_frequency", "检查频率 默认为0.5秒")
    add_comment_to_toml(config_path, "fast_handle", "是否自动清理被禁止的方块")
    add_comment_to_toml(config_path, "count_block", "是否统计蓝图内方块信息，会占用一定性能，但可以可视化")
    add_comment_to_toml(config_path, "kill_entity", "是否剔除蓝图内的全部实体，这会导致创造打印蓝图不包含实体，但是可以杜绝全部实体相关的复制漏洞")
    add_comment_to_toml(config_path, "ban_entity", "禁止的实体，填入后将会剔除蓝图内的此实体")
    add_comment_to_toml(config_path, "ban_tags", "禁止的tag，由于nbt的递归隐藏机制，如果填入的tag在蓝图内检测到，就会将蓝图清空，因为nbt数据结构无法针对tag剔除进行修复")
    add_comment_to_toml(config_path, "ban_block", "禁止的方块，填入后将会剔除蓝图内的此类方块，如果剔除不完全，则会清空蓝图")


    add_comment_to_toml_r(config_path, "Enchantments", "附魔标签，这会阻止创造蓝图，但也会导致蓝图不能带有附魔特性，因为它们的结构相同")
    add_comment_to_toml_r(config_path, "using_converts_to", "食物标签，阻止返回复制特性")
    add_comment_to_toml_r(config_path, "bundle_contents", "存储袋标签，阻止复制特性")
    add_comment_to_toml_r(config_path, "run_command", "阻止其切换权限，阻止复制特性")

    add_comment_to_toml_r(config_path, "minecraft:kelp", "这可以阻止绝大多数gt机，他们极其卡顿！")
    add_comment_to_toml_r(config_path, "minecraft:command_block", "不多说了，这玩意是命令方块")
    add_comment_to_toml_r(config_path, "create_integrated_farming:chicken_roost", "1.21特别添加 阻止gt机卡服")

    add_comment_to_toml(config_path, "[smtp]", "实验功能，可以在发现异常蓝图后推送smtp邮箱，免费又好用，还能利用免费的推送服务！")
    add_comment_to_toml(config_path, "enable", "是否启用，true 或 false")
    add_comment_to_toml(config_path, "email_receive", "接收报警的邮箱，所有报警信息都会发送到这个邮箱！")
    add_comment_to_toml(config_path, "smtp_server", "smtp的默认根服务器，一般情况不需要改")
    add_comment_to_toml(config_path, "smtp_port", "smtp的默认服务器端口，一般情况不需要改")
    add_comment_to_toml(config_path, "smtp_sender_email", "使用哪个邮箱进行发送，报警信息会从这个邮箱发出")
    add_comment_to_toml(config_path, "smtp_password", "这个邮箱的smtp密码，需要在qq邮箱网页版获取")

if __name__ == "__main__":
    # 生成配置
    config_path = "../../../config.toml"
    generate_config(config_path)

    # 导入数据从 TOML 文件
    config = import_toml(config_path)
    print("读取的配置：", config)
