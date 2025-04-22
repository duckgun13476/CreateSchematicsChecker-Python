import yaml
from Checker.lib.log_color import log
import os

def save_md5(path_md5, data):
    """将 MD5 哈希值保存到 YAML 文件中"""
    # 检查文件是否存在
    if os.path.exists(path_md5):
        with open(path_md5, 'r') as md5_file:
            existing_data = yaml.safe_load(md5_file)
            if existing_data is None:
                existing_data = {}  # 如果文件为空，初始化为空字典
    else:
        existing_data = {}

    # 输出调试信息
    # 检查现有数据的类型
    if not isinstance(existing_data, dict):
        # 重命名现有文件
        new_file_name = path_md5.replace('.yml', '_1.yml')
        os.rename(path_md5, new_file_name)
        print(f"现有文件格式不正确，已重命名为: {new_file_name}")

        # 初始化新的数据结构
        existing_data = {'md5_hashes': []}

    # 如果 'md5_hashes' 键不存在，则初始化它
    if 'md5_hashes' not in existing_data:
        log.info("未找到存储，已创建")
        existing_data['md5_hashes'] = []

    # 添加新的 MD5 哈希值
    if existing_data['md5_hashes'] is None:
        existing_data['md5_hashes'] = []
    existing_data['md5_hashes'].append(data)

    # 将更新后的数据写入 YAML 文件
    with open(path_md5, 'w') as md5_file:
        yaml.dump(existing_data, md5_file)

def load_rule(convert_to_string=False, path=r"rule/standard.yml"):
    # 自定义 Loader
    class CustomLoader(yaml.SafeLoader):
        pass

    # 自定义布尔构造函数
    def bool_constructor(loader, node):
        value = loader.construct_scalar(node)
        if convert_to_string:
            return value  # 保持为字符串
        else:
            return value.lower() == 'true'  # 转换为布尔值

    # 注册自定义构造函数
    CustomLoader.add_constructor('tag:yaml.org,2002:bool', bool_constructor)

    # 检查文件是否存在，如果不存在则创建一个带有默认内容的 YAML 文件
    if not os.path.exists(path):
        if path == r"rule/schematics.yml":
            existing_data = {'md5_hashes': []}
            with open(path, 'w', encoding='utf-8') as file:
                yaml.dump(existing_data, file, allow_unicode=True)  # 写入初始内容
        else:
            log.error("文件不存在")
    # 读取 YAML 文件
    with open(path, 'r', encoding='utf-8') as file:
        config = yaml.load(file, Loader=CustomLoader)
        return config


def extract_rules(config):
    try:
        # 初始化两个空列表
        blocks_rules = []
        palette_rules = []
        redundant_rules = []
        # 遍历每一个规则
        for rule_23 in config['rules']:
            # 获取 Univariate 字典
            univariate = rule_23.get('Univariate', {})

            # 检查 Univariate 中的键
            for key in univariate.keys():
                if key.startswith('blocks.'):
                    blocks_rules.append(rule_23)  # 添加完整的规则字典
                    break  # 找到后可以跳出内层循环
                elif key.startswith('palette'):
                    palette_rules.append(rule_23)  # 添加完整的规则字典
                    break  # 找到后可以跳出内层循环

            if rule_23.get('Redundant') is not None:
                redundant_rules.append(rule_23)
    except Exception as e:
        log.error(f"fail in extract rule:{e}")
        return None, None,None

    return blocks_rules, palette_rules, redundant_rules


if __name__ == '__main__':
    config = load_rule()
    # 访问特定规则
    for rule in config['rules']:
        print(rule)


