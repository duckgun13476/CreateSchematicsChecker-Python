import yaml

def load_rule():
    path = r"rule/standard.yml"
    # 读取 YAML 文件
    with open(path, 'r', encoding='utf-8') as file:
        config = yaml.safe_load(file)
        return config


def extract_rules(config):
    # 初始化两个空列表
    blocks_rules = []
    palette_rules = []
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
    return blocks_rules, palette_rules


if __name__ == '__main__':
    config = load_rule()
    # 访问特定规则
    for rule in config['rules']:
        print(rule)


