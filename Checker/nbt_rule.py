from nbt import nbt
import os


from Checker.rule_handler import load_rule,extract_rules
from Checker.lib.sugar import timer
# about to delete
def generate_paths(path):
    # 初始化路径结果
    paths = []

    def generate(current_path, index):
        # 如果到达路径末尾，添加当前路径到结果
        if index == len(path):
            paths.append(current_path)
            return

        element = path[index]

        if isinstance(element, int):
            # 对于每个数字，生成对应的路径
            for j in range(element):
                generate(current_path + [j], index + 1)
        else:
            # 不是数字，继续添加到当前路径
            generate(current_path + [element], index + 1)

    # 开始生成路径
    generate([], 0)

    return paths

def read_nbt_value(nbt_data, path):
    # 将路径分割为各个部分
    keys = path.split('.')

    current_data = nbt_data

    for key in keys:
        # 尝试获取当前键的值



        if isinstance(current_data, nbt.TAG_Compound):
            current_data = current_data.get(key)
            print(current_data,key)
        elif isinstance(current_data, nbt.TAG_List):
            # 如果当前数据是列表，尝试解析列表中的每个元素
            try:

                index = int(key)  # 尝试将键转换为整数（列表索引）
                current_data = current_data[index]
            except (ValueError, IndexError):
                print(current_data,key,'VIerror')
                return None  # 如果键无效，返回 None
        else:
            return None  # 如果当前数据不是字典或列表，返回 None

    return current_data

def get_nbt_value(nbt, path):
    """根据给定路径获取 NBT 值."""
    for key in path:
        print("key",key)
        if isinstance(key,int):
            nbt_list = []
            for num in range(0, key):
                print("num",num)
                nbt_list.append(nbt[num])
            # print("type",type(nbt_list))
            nbt = nbt_list
            print("int")
        else:
            if isinstance(nbt,list):
                list_nbt = []
                for nbt_item in nbt:
                    print("nbt_item",nbt_item)
                    list_nbt.append(nbt_item[key])
                    nbt = list_nbt
            else:
                nbt = nbt[key]  # 逐级访问
    return nbt

def check_nbt_with_rule(rule,in_nbt):
    if rule.get('Univariate'):
        for s_rule in rule['Univariate']:
            print(s_rule, rule['Univariate'][s_rule])
            path = []
            s_rule = s_rule.split('.')
            pick_data = in_nbt
            for s_rule_a in s_rule[1:]:
                if isinstance(pick_data, list) or isinstance(pick_data, nbt.TAG_List):
                    if isinstance(pick_data, nbt.TAG_List):
                        path.append(len(pick_data))
                    path.append(s_rule_a)
                    pick_data_save = []
                    for s_rule_b in pick_data:
                        pick_data_save.append(s_rule_b.get(s_rule_a))
                    pick_data = pick_data_save
                else:
                    pick_data = pick_data.get(s_rule_a)
                    path.append(s_rule_a)


                if s_rule_a == s_rule[-1]:
                    path = generate_paths(path)
                    print("path",path)
                    try:
                        for s_path in path:
                            out_nbt = in_nbt
                            for path_f in s_path:
                                if path_f == s_path[-1]:
                                    out_nbt[path_f] = nbt.TAG_Int(123234)
                                out_nbt = out_nbt[path_f]

                            print("nbt",out_nbt)


                    except Exception as e:
                        print(1,e)

                    if isinstance(pick_data, list):
                        for list_data in pick_data:
                            print(s_rule_a,list_data)
                    else:
                        print(s_rule_a,pick_data)

    print("------")



@timer
def rule_check(source_path_1):
    # 加载 NBT 文件
    try:
        source_nbt = nbt.NBTFile(source_path_1)
    except Exception as e:
        print(f"无法读取文件 {source_path_1}，错误: {e}")
        # 删除文件
        if os.path.exists(source_path_1):
            os.remove(source_path_1)
            print(f"文件 {source_path_1} 已删除。")
        return None
    # 加载规则
    config = load_rule()
    block_rule,palette_rule = extract_rules(config)


    # for rule in palette_rule:
       #  print(rule)


    match_rule = 'blocks.path.value'
    keys = match_rule.split('.')
    print('keys',keys[1:])

    # 检查主线程
    for block in source_nbt.get('blocks'):


        block_nbt = block.get('nbt')
        if block_nbt is not None:
            print(type(block['nbt']['id']))
            # block['nbt']['id']=nbt.TAG_String('minecraft:block')
            block_id = block_nbt.get('id')

            # print(block_id,"---")
            for rule in block_rule:
                # print(block_id,rule.get('block'))
                if str(block_id) == rule.get('block'):
                    print(f"检测到匹配：{rule['name']}   {rule['block']}")
                    check_nbt_with_rule(rule,block_nbt)
                    # print(block)

    for palette in source_nbt.get('palette'):
        pass
        # print(palette)
    source_nbt.write_file(source_path_1)

    return
"""    for rule in rules.get('rules'):
        print(rule)
        print(f"规则：{rule.get('name')}| 方块：{rule.get('block')}")
        paths = rule.get('Univariate')
        for path in paths:
            print(f"[路径: {path} ]-[值: {paths.get(path)}]")
            print(path)
            print(source_nbt)
            print(read_nbt_value(source_nbt, path))
"""

"""
    # 访问 blocks 标签
    # print(source_nbt)

    print(source_nbt.get("blocks"))
    for block in source_nbt["blocks"]:
        print(block)
    print(source_nbt["palette"])"""


"""    blocks = source_nbt["blocks"]
    belt_change_count = 0
    # 遍历每个方块条目
    for block in blocks:
        # 检查 nbt 中的 id 是否为 create:belt
        if "nbt" in block and block["nbt"] is not None:
            if "id" in block["nbt"] and block["nbt"]["id"].value == "create:belt":
                # 读取 Length 的值
                if "Length" in block["nbt"]:
                    length_value = block["nbt"]["Length"].value

                    # 如果 Length 大于 30，则替换为 20
                    if length_value > 30:
                        block["nbt"]["Length"] = nbt.TAG_Int(4)  # 修改 Length 值为 20
                        # print(length_value)
                        belt_change_count += 1
    # 保存修改后的 NBT 文件
    source_nbt.write_file(source_path_1)  # 替换为保存路径
    if belt_change_count == 0:
        return "未发现异常"
    else:
        return f"传送带异常调整结果：{belt_change_count}"""



if __name__ == '__main__':
    source_path = '../schematics/uploaded/csy12345/exp_2.nbt'  # 替换为你的 NBT 文件路径
    rule_check(source_path)

