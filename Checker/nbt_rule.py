from collections import Counter
from Checker.lib.log_color import log
from nbt import nbt
import os
from Checker.rule_handler import load_rule,extract_rules
from Checker.lib.sugar import timer
from Checker import config

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
        if isinstance(key,int):
            nbt_list = []
            for num in range(0, key):
                print("num",num)
                nbt_list.append(nbt[num])
            nbt = nbt_list
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

def check_nbt_with_block(rule, in_nbt):
    def handle_data(s_rule_a,pick_data):
        if isinstance(ss_rule_value,list):
            if int(str(out_nbt[path_f])) > ss_rule_value[1]:
                print(f"根据规则 {rule['name']} 设置 {s_rule_a}:{out_nbt[path_f]} 上限为 {ss_rule_value[1]}")
                out_nbt[path_f] = nbt.TAG_Int(ss_rule_value[1])
            if int(str(out_nbt[path_f])) < ss_rule_value[0]:
                print(f"根据规则 {rule['name']} 设置 {s_rule_a}:{out_nbt[path_f]} 下限为 {ss_rule_value[0]}")
                out_nbt[path_f] = nbt.TAG_Int(ss_rule_value[0])


            print("value",ss_rule_value,"|",s_rule_a,pick_data)
        # out_nbt[path_f] = nbt.TAG_Int(1433)


    if rule.get('Univariate'):
        print("rule",rule['Univariate'])
        for ss_rule,ss_rule_value in rule['Univariate'].items():
            path = []
            s_rule = ss_rule.split('.')
            pick_data = in_nbt
            for s_rule_a in s_rule[2:]:
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
                    try:
                        for index,s_path in enumerate(path):
                            out_nbt = in_nbt
                            for path_f in s_path:
                                if path_f == s_path[-1]:
                                    # change in here
                                    if isinstance(pick_data, list):
                                        handle_data(s_rule_a,pick_data[index])
                                    else:
                                        handle_data(s_rule_a,pick_data)
                                out_nbt = out_nbt[path_f]
                            # print("nbt",out_nbt)
                    except Exception as e:
                        print("E004",e)



    print("------")

def check_nbt_with_palette(rule,in_nbt):
    for key,word in rule.get('Univariate').items():
        key = key.split('.')
        for key_item in key[2:]:
            if str(in_nbt.get(key[1]).get(key_item))!=word:
                in_nbt[key[1]][key_item] = nbt.TAG_String(word)
                print(f"根据规则 {rule['name']} 设置值为 {word}")

@timer
def path_get_nbt(source_path_1):
    # 加载 NBT 文件
    try:
        source_nbt = nbt.NBTFile(source_path_1)
        return source_nbt
    except Exception as e:
        print(f"无法读取文件 {source_path_1}，错误: {e}")
        # 删除文件
        if os.path.exists(source_path_1):
            os.remove(source_path_1)
            print(f"文件 {source_path_1} 已删除。")
        return None

def nbt_int(nbt_123):
    return int(str(nbt_123))

def find_max_same_element_count(array):
    # 使用 Counter 统计每个元素的出现次数
    count_map = Counter(tuple(row) for row in array)

    # 找到最大出现次数
    max_count = max(count_map.values())

    return max_count


@timer
def rule_check(source_path_1):
    source_nbt = path_get_nbt(source_path_1)
    if source_nbt:
        # 加载规则
        nbt_config = load_rule(convert_to_string=True)
        block_rule,palette_rule,redundant_rule = extract_rules(nbt_config)

        chain_parent_list = []
        chain_children_list = []
        belt_list = []

        for block in source_nbt.get('blocks'):

            block_nbt = block.get('nbt')
            if block_nbt is not None:
                block_id = block_nbt.get('id')


                if str(block_id) =='create:chain_conveyor' and nbt_config.get('check_chain_conveyor')=='true':
                    print(f"执行特殊规则：'create:chain_conveyor'")
                    X_P = nbt_int(block.get('pos')[0])
                    Y_P = nbt_int(block.get('pos')[1])
                    Z_P = nbt_int(block.get('pos')[2])
                    chain_parent_list.append([X_P,Y_P,Z_P])
                    check_same_item = []
                    for item in block_nbt.get('Connections'):
                        X_C = nbt_int(item.get('X')) + X_P
                        Y_C = nbt_int(item.get('Y')) + Y_P
                        Z_C = nbt_int(item.get('Z')) + Z_P
                        chain_children_list.append([X_C,Y_C,Z_C])
                        check_same_item.append([X_C,Y_C,Z_C])
                    if find_max_same_element_count(check_same_item) > 1:
                        print("检测到传动轮被篡改，后续规则不会执行")
                        return False


                if str(block_id) =='create:belt' and nbt_config.get('check_belt')=='true':
                    print(f"执行特殊规则：'create:belt_connector'")
                    X = nbt_int(block_nbt.get('Controller')[0])
                    Y = nbt_int(block_nbt.get('Controller')[1])
                    Z = nbt_int(block_nbt.get('Controller')[2])
                    Controller  = [X,Y,Z]
                    is_same = False
                    for item in belt_list:
                        if Controller ==item[0]:
                            is_same = True
                            item[3]+=1
                    if not is_same:
                        belt_list.append([Controller,int(str(block_nbt.get('Length'))),block_nbt.get('Index'),1])

                for rule in block_rule:
                    if str(block_id) == rule.get('block'):
                        print(f"检测到匹配：{rule['name']}   {rule['block']}")
                        check_nbt_with_block(rule, block_nbt)

                for redundant in redundant_rule:
                    if str(block_id) == redundant.get('block'):
                        print(f"检测到匹配：{redundant['name']}   {redundant['block']}")
                        for key,word in redundant.get('Redundant').items():
                            key = key.split('.')[2:]
                            value = get_nbt_value(block_nbt,key)
                            if word in value:
                                print("检测到非法nbt，后续规则不会执行")
                                return False

        # print(chain_parent_list)
        # print(chain_children_list)

        if nbt_config.get('check_chain_conveyor')=='true' and chain_parent_list != []:
            if nbt_config.get('conveyor_max_connection')<find_max_same_element_count(chain_children_list):
                print(f"传动轮连接数量[{nbt_config.get('conveyor_max_connection')}]超过最大配置数量[{find_max_same_element_count(chain_children_list)}]，后续规则不会执行")
                return False
            for item in chain_children_list:
                if item not in chain_parent_list:
                    print(f"检测到传动轮被篡改，坐标{item}没有双向配对，后续规则不会执行")
                    return False
        if nbt_config.get('check_belt')=='true' and belt_list != []:
            for belt in belt_list:
                if belt[1]!=belt[3]:
                    print("检测到传送带被篡改，后续规则不会执行")
                    return False

        for palette in source_nbt.get('palette'):
            block_id = palette.get('Name')
            if block_id is not None:
                for rule in palette_rule:
                    if str(block_id) == rule.get('block'):
                        check_nbt_with_palette(rule,palette)

        source_nbt.write_file(source_path_1)
        return

@timer
def str_check(source_path_1,check_string_23):
    source_nbt = path_get_nbt(source_path_1)
    data_str = str(source_nbt.pretty_tree())  # 将 NBT 数据转换为字符串
    tag_count = 0
    item_count = 0
    for tag in check_string_23[0]:
        if tag in data_str:
            log.warning(f"警告: 找到异常 NBT 标签，包含{tag}")
            tag_count += 1
    for item in check_string_23[1]:
        if item in data_str:
            log.warning(f"警告: 找到匹配 ID 物品，包含{item}")
            if config.fast_handle:
                data_str = data_str.replace(item, "minecraft:air")
            item_count += 1
    return tag_count, item_count


if __name__ == '__main__':
    source_path = '../schematics/uploaded/csy12345/20250125_155515_一键通关[原视频].nbt'  # 替换为你的 NBT 文件路径


    rule_check(source_path)

    tags_to_check = ["AttributeModifiers", "Enchantments"]
    block_to_check = ["create:creative_crate", "create:creative_fluid_tank", "create:creative_motor", "create:motor",'create:blaze_burner',
                      "create:lectern_controller","supplementaries:urn",'minecraft:kelp',"minecraft:shulker_box","minecraft:tripwire_hook"]


    # str_check(source_path,[tags_to_check,block_to_check])


