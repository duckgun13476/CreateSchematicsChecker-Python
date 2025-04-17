import yaml

path = r"rule/standard.yml"
# 读取 YAML 文件
with open(path, 'r', encoding='utf-8') as file:
    config = yaml.safe_load(file)

# 打印读取的内容
print(config)

# 访问特定规则
for rule in config['rules']:
    print(f"规则: {rule['name']}, 方块: {rule['block']}, 属性: {rule['attribute']}, 父列表: {rule['list']}, 路径: {rule['path']},值: {rule['value']}")

