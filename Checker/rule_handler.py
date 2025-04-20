import yaml

def load_rule(convert_to_string=False):
    path = r"rule/standard.yml"

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

    # 读取 YAML 文件
    with open(path, 'r', encoding='utf-8') as file:
        config = yaml.load(file, Loader=CustomLoader)
        return config


def extract_rules(config):
    # 初始化两个空列表
    blocks_rules = []
    palette_rules = []
    redundant_rules = []
    # 遍历每一个规则
    for rule in config['rules']:
        # 获取 Univariate 字典
        univariate = rule.get('Univariate', {})

        # 检查 Univariate 中的键
        for key in univariate.keys():
            if key.startswith('blocks.'):
                blocks_rules.append(rule)  # 添加完整的规则字典
                break  # 找到后可以跳出内层循环
            elif key.startswith('palette'):
                palette_rules.append(rule)  # 添加完整的规则字典
                break  # 找到后可以跳出内层循环

        if rule.get('Redundant') is not None:
            redundant_rules.append(rule)
    return blocks_rules, palette_rules, redundant_rules


if __name__ == '__main__':
    config = load_rule()
    # 访问特定规则
    for rule in config['rules']:
        print(rule)


