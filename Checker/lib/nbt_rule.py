import json
from collections import Counter
import traceback
from nbt import nbt

from Checker.lib.log_color import log, write_log
from Checker.lib.math.func import has_duplicates, remove_element, count_elements
from Checker.lib.math.nbt_hook import safe_get_array, nbt_int
from Checker.lib.nbt_matcher.nbt_str import str_check
from Checker.lib.rule_handler import load_rule
from Checker.lib.setting.config_gen import config
ban_block:list = config.ban_block
ban_entity:list = config.ban_entity


# about to delete
def generate_paths(path):
    # 初始化路径结果
    paths = []

    def generate(current_path, index):
        # 如果到达路径末尾, 添加当前路径到结果
        if index == len(path):
            paths.append(current_path)
            return
        element = path[index]
        if isinstance(element, int):
            # 对于每个数字, 生成对应的路径
            for j in range(element):
                generate(current_path + [j], index + 1)
        else:
            # 不是数字, 继续添加到当前路径
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
        elif isinstance(current_data, nbt.TAG_List):
            # 如果当前数据是列表, 尝试解析列表中的每个元素
            try:

                index = int(key)  # 尝试将键转换为整数（列表索引）
                current_data = current_data[index]
            except (ValueError, IndexError):
                return None  # 如果键无效, 返回 None
        else:
            return None  # 如果当前数据不是字典或列表, 返回 None

    return current_data


def get_nbt_value(nbt, path):
    """根据给定路径获取 NBT 值."""
    for key in path:
        if isinstance(key, int):
            nbt_list = []
            for num in range(0, key):
                nbt_list.append(nbt[num])
            nbt = nbt_list
        else:
            if isinstance(nbt, list):
                list_nbt = []
                for nbt_item in nbt:
                    list_nbt.append(nbt_item[key])
                    nbt = list_nbt
            else:
                try:
                    nbt = nbt[key]  # 逐级访问
                except Exception as e:
                    if "does not exist" in str(e):
                        log.debug(f"数据包 {nbt} 没有找到标签 {key}")
                        return None
                    else:
                        log.error(e)
    return nbt


def check_nbt_with_block(rule, in_nbt, count_153=0):

    def handle_data(s_rule_a, pick_data):
        count_15 = 0
        if isinstance(ss_rule_value, list):
            if isinstance(out_nbt, nbt.TAG_Int_Array):
                # log.info(f"使用兼容规则")
                for self_value in out_nbt:
                    if nbt_int(self_value) > int(ss_rule_value[1]) or nbt_int(self_value)<int(ss_rule_value[0]):
                        log.error(f"旧版的篡改蓝图")
                        return -1
            else:
                # print(type(out_nbt))
                if int(str(out_nbt[path_f])) > ss_rule_value[1]:
                    log.warning(f"根据规则 {rule['name']} 设置 {s_rule_a}:{out_nbt[path_f]} 上限为 {ss_rule_value[1]}")
                    count_15 += 1
                    out_nbt[path_f] = nbt.TAG_Int(ss_rule_value[1])
                if int(str(out_nbt[path_f])) < ss_rule_value[0]:
                    log.warning(f"根据规则 {rule['name']} 设置 {s_rule_a}:{out_nbt[path_f]} 下限为 {ss_rule_value[0]}")
                    count_15 += 1
                    out_nbt[path_f] = nbt.TAG_Int(ss_rule_value[0])

            # print("value", ss_rule_value, "|", s_rule_a, pick_data)
        return count_15

    if rule.get('Univariate'):
        for ss_rule, ss_rule_value in rule['Univariate'].items():
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
                        if isinstance(s_rule_b, nbt.TAG_Int_Array):
                            pick_data_save.append(s_rule_b)
                        else:
                            pick_data_save.append(s_rule_b.get(s_rule_a))
                    pick_data = pick_data_save
                else:
                    pick_data = pick_data.get(s_rule_a)
                    path.append(s_rule_a)
                if s_rule_a == s_rule[-1]:
                    path = generate_paths(path)
                    try:
                        for index, s_path in enumerate(path):
                            out_nbt = in_nbt
                            for path_f in s_path:
                                if path_f == s_path[-1]:
                                    if isinstance(pick_data, list):
                                        count_153 += handle_data(s_rule_a, pick_data[index])
                                    else:
                                        count_153 += handle_data(s_rule_a, pick_data)

                                if isinstance(out_nbt, nbt.TAG_Int_Array):
                                    pass
                                else:
                                    out_nbt = out_nbt[path_f]
                            # print("nbt",out_nbt)
                    except Exception as e:
                        log.error("E004, %s", e)

    # log.info("------")
    return count_153


def check_nbt_with_palette(rule, in_nbt):
    count_14 = 0
    for key, word in rule.get('Univariate').items():
        key = key.split('.')
        for key_item in key[2:]:
            if str(in_nbt.get(key[1]).get(key_item)) != word:
                in_nbt[key[1]][key_item] = nbt.TAG_String(word)
                log.warning(f"根据规则 {rule['name']} 设置值为 {word}")
                write_log(f"根据规则 {rule['name']} 设置值为 {word}")
                count_14 += 1
    return count_14


def find_max_same_element_count(array):
    count_map = Counter(tuple(row) for row in array)
    if not count_map:
        return 0
    else:
        return max(count_map.values())


def handle_filter(ban_count, Filter_nbt):
    if Filter_nbt.get('tag') is not None:
        if Filter_nbt.get('tag').get('Items') is not None:
            match = Filter_nbt.get('tag').get('Items').get('Items')
            for match_item in match:
                if str(match_item.get('id')) in ban_block:
                    match_item['id'] = nbt.TAG_String('minecraft:air')
                    ban_count += 1
                elif str(match_item.get('id')) == "create:filter":

                    match_shadow = match_item.get('tag').get('Items').get('Items')
                    for shadow_item in match_shadow:

                        if str(shadow_item.get('id')) in ban_block:
                            shadow_item['id'] = nbt.TAG_String('minecraft:air')
                            ban_count += 1
                        elif str(shadow_item.get('id')) == "create:filter":
                            log.error("过滤器迭代匹配")
                            write_log("过滤器迭代匹配")
                            return -1, ban_count
    return 0, ban_count


def rule_check(data, block_rule, palette_rule, redundant_rule, source_path_1, entity_handle, change_file,nbt_config=load_rule(convert_to_string=True)):
    block_nbt = None
    source_nbt = data
    modify_count = 0
    write = False
    ban_count = 0
    pos  = 0
    def handle_fanc_menu(in_data,ban_count_45,write_1):
        # 内部有Filter
        if in_data.get('Filter') is not None:
            Filter = in_data['Filter']
            filter_id = Filter.get('id')
            if str(filter_id) == "create:filter":
                is_cheat_1, ban_count_45 = handle_filter(ban_count_45, Filter)
                if is_cheat_1:
                    log.error("过深的过滤器")

            if str(filter_id) in ban_block:
                write_1 = True
                Filter['id'] = nbt.TAG_String('minecraft:air')
                ban_count_45 += 1

        return write_1,ban_count_45

    def handle_items_menu(in_data,ban_count_1,write_1):
        # 内部有Items
        if in_data.get('Items') is not None:
            Items_23 = in_data['Items']
            for item_43 in Items_23:
                item_id = item_43.get('id')

                if str(item_id) in ban_block:
                    write_1 = True
                    item_43['id'] = nbt.TAG_String('minecraft:air')
                    ban_count_1 += 1

        return write_1,ban_count_1



    if source_nbt:
        chain_parent_list = []
        chain_children_list = []
        belt_list = []
        for block in source_nbt.get('blocks'):
            pos += 1
            if block.get('nbt') is not None:
                block_nbt = block['nbt']
            else:
                # log.error(f"蓝图不包含nbt数据！来自第 {pos} 个方块")
                pass




            if block_nbt is not None:
                block_id = block_nbt.get('id')

                if str(block_id) in ban_block:
                    block_nbt['id'] = nbt.TAG_String('minecraft:air')
                    ban_count += 1


                # 红石请求器6.0
                if str(block_id) == "create:redstone_requester":
                    EncodedAddress = block_nbt.get('EncodedRequest')
                    if EncodedAddress is not None:
                        try:
                            address = block_nbt['EncodedRequest']
                            stack = address['ordered_stacks']
                            entries = stack['entries']
                            for entry in entries:
                                if str(entry['item_stack']['id']) in ban_block:
                                    entry['item_stack']['id'] = nbt.TAG_String('minecraft:air')
                                    ban_count += 1

                        except Exception as e:
                            log.error("红石请求器搜索错误")
                            traceback.print_exc()


                # 黄铜隧道
                if str(block_id) == "create:brass_tunnel":
                    write,ban_count = handle_fanc_menu(block_nbt,ban_count,write)
                    Filters = block_nbt.get('Filters')
                    if Filters is not None:
                        for filter_item in Filters:
                            write,ban_count = handle_fanc_menu(filter_item,ban_count,write)

                # 工作盆
                if str(block_id) == "create:basin":
                    write,ban_count = handle_fanc_menu(block_nbt,ban_count,write)
                    write,ban_count = handle_items_menu(block_nbt['InputItems'],ban_count,write)
                    write,ban_count = handle_items_menu(block_nbt['OutputItems'],ban_count,write)


                # 智能溜槽
                if str(block_id) == "create:smart_chute":
                    Filter_nbt = block_nbt['Filter']
                    is_cheat, ban_count = handle_filter(ban_count, Filter_nbt)
                    if is_cheat:
                        return -1, ban_count
                    write,ban_count = handle_fanc_menu(block_nbt,ban_count,write)

                # 存量转信器
                if "create:stockpile_switch" == str(block_id):
                    write,ban_count = handle_fanc_menu(block_nbt,ban_count,write)

                if "create:stockpile_switch" == str(block_id):
                    write,ban_count = handle_fanc_menu(block_nbt,ban_count,write)

                # 工具盒
                if "create:toolbox" == str(block_id):
                    if block_nbt.get('Inventory') is not None:
                        Inventory = block_nbt['Inventory']
                        Items = Inventory.get('Items')
                        if str(Items) != '[]':
                            for item in Items:
                                if str(item['id']) in ban_block:
                                    write = True
                                    item['id'] = nbt.TAG_String('minecraft:air')
                                    ban_count += 1


                # 无尽电池的修复 创意传动
                if "create_connected:kinetic_battery" == str(block_id):
                    if block_nbt.get('batteryLevel') is not None:
                        batteryLevel= block_nbt['batteryLevel']
                        if str(batteryLevel) != "0":
                            block_nbt['batteryLevel'] = nbt.TAG_Int(0)
                            write = True
                            log.warning("归零了电池的电能")


                # 1.21.1 附魔参数清理
                if "create_enchantment_industry:printer" == str(block_id):
                    if block_nbt.get('PrintingTemplate') is not None:
                        PrintingTemplate = block_nbt['PrintingTemplate']
                        if str(PrintingTemplate) != "{}":
                            PrintingTemplate.clear()
                            write = True
                            log.warning("清理了打印机的附魔参数")




                # 1.21.1 neoforge 轧机 safenbt
                if "createaddition:rolling_mill" == str(block_id):
                    try:
                        if block_nbt.get('InputInventory') is not None:
                            InputInventory = block_nbt['InputInventory']
                            if str(InputInventory.get('Items')) != "[]":
                                # log.error(f"{InputInventory.get('Items')}")
                                InputInventory['Items'].clear()
                                log.warning("清理了轧机的输入参数")
                                write = True

                        if block_nbt.get('OutputInventory') is not None:
                            OutputInventory = block_nbt['OutputInventory']
                            if str(OutputInventory.get('Items')) != "[]" :
                                # log.error(f"{OutputInventory.get('Items')}")
                                OutputInventory['Items'].clear()
                                log.warning("清理了轧机的输出参数")
                                write = True
                    except Exception as e:
                        log.error("E rolling_mill, %s", e)
                        traceback.print_exc()

                # 6.0机械动力发报机的检查
                if "create:stock_ticker" == str(block_id):
                    if block_nbt.get('Categories') is not None:
                        Categories = block_nbt['Categories']
                        for category in Categories:
                            if str(category.get('id')) == "create:filter":
                                try:
                                    components = category['components']
                                    if components.get('create:filter_items') is not None:
                                        items = components['create:filter_items']
                                        for item in items:
                                            if str(item['item']['id']) in ban_block:
                                                write = True
                                                item['item']['id'] = nbt.TAG_String('minecraft:air')
                                                ban_count += 1
                                            # log.warning(f"{str(item['item']['id'])}")
                                except Exception as e:
                                    log.error("检查发报机发生异常", e)


                # 6.0机械动力工厂仪表的检查
                if "create:factory_panel" == str(block_id):
                    data =  block_nbt


                    if data.get('top_right') is not None:
                        write,ban_count = handle_fanc_menu(data['top_right'],ban_count,write)
                        write,ban_count = handle_fanc_menu(data['top_left'],ban_count,write)
                        write,ban_count = handle_fanc_menu(data['bottom_right'],ban_count,write)
                        write,ban_count = handle_fanc_menu(data['bottom_left'],ban_count,write)

                # 伪装附属的针对检测
                if "copycats:" in str(block_id):
                    fake_id = ['minecraft:air']
                    consume_id = []
                    if block_nbt.get('material_data') is not None:
                        for item in block_nbt['material_data']:
                            item_c = block_nbt['material_data'][str(item)]
                            try:
                                material = item_c['material']['Name']
                                if material not in fake_id:
                                    fake_id.append(str(material))

                                elif material in fake_id:
                                    continue

                                consumedItem_id = item_c['consumedItem']['id']
                                consumedItem_count = item_c['consumedItem']['Count']

                                # 数量不能为0，1外的数字 id 必须在伪装列表里
                                if str(consumedItem_id) not in fake_id or int(str(consumedItem_count)) not in [0,1]:
                                    item_c['consumedItem']['id'] = nbt.TAG_String('minecraft:air')
                                    if str(consumedItem_id) not in fake_id:
                                        log.error(f"伪装图层与包含物品不符! 伪装图层是[{str(material)}] 然而包含的物品是[{str(consumedItem_id)}]")
                                    if int(str(consumedItem_count)) not in [0,1]:
                                        log.error(f"包含物品数量异常！本应是0或1 但实际是[{str(consumedItem_count)}]")
                                        return -1, ban_count
                                    write = True
                                else:
                                    consume_id.append(str(consumedItem_id))


                            except Exception as e:
                                log.error("处理copycats 发生异常, %s", e)
                                traceback.print_exc()

                        consume_id = remove_element(consume_id, 'minecraft:air')

                        if has_duplicates(consume_id):
                            log.error("伪装图层的包含物品数量异常！有问题的物品：")
                            write_log("伪装图层的包含物品数量异常！有问题的物品：")
                            count_res = count_elements(consume_id)
                            for element in count_res:
                                if count_res[element] not in [0,1]:
                                    log.error(f"id [{element}] 数量[{count_res[element]}]")
                                    write_log(f"id [{element}] 数量[{count_res[element]}]")

                            return -1, ban_count


                if str(block_id) == "create:deployer":
                    # log.warning("清理机械手标签中")
                    # print(block_nbt.get('Inventory'))
                    if str(block_nbt.get('Inventory')) != '[]':
                        block_nbt['Inventory'].clear()
                        write = True
                        # print(block_nbt.get('Inventory'))

                if str(block_id) == "create:redstone_link":
                    if str(block_nbt.get('FrequencyFirst').get('id')) is not None:
                        if str(block_nbt.get('FrequencyFirst').get('id')) in ban_block:
                            block_nbt['FrequencyFirst']['id'] = nbt.TAG_String('minecraft:air')
                            ban_count += 1
                    if str(block_nbt.get('FrequencyLast').get('id')) is not None:
                        if str(block_nbt.get('FrequencyLast').get('id')) in ban_block:
                            block_nbt['FrequencyLast']['id'] = nbt.TAG_String('minecraft:air')
                            ban_count += 1

                if str(block_id) == "create:funnel":
                    if str(block_nbt.get('Filter').get('id')) is not None:
                        if str(block_nbt.get('Filter').get('id')) in ban_block:
                            block_nbt['Filter']['id'] = nbt.TAG_String('minecraft:air')
                            ban_count += 1
                        elif str(block_nbt.get('Filter').get('id')) == "create:filter":
                            Filter_nbt = block_nbt['Filter']
                            is_cheat, ban_count = handle_filter(ban_count, Filter_nbt)
                            if is_cheat:
                                return -1, ban_count


                if str(block_id) == 'create:weighted_ejector':
                    ejector_distance = block_nbt.get('HorizontalDistance')
                    if nbt_int(ejector_distance) <= 0:
                        log.error(f"检测到弹射置物台篡改蓝图!后续规则不会执行|位于[{source_nbt.get('blocks').index(block)}]值[{ejector_distance}]")
                        write_log(f"检测到弹射置物台篡改蓝图!后续规则不会执行|位于[{source_nbt.get('blocks').index(block)}]值[{ejector_distance}]")
                        return -1, ban_count

                if str(block_id) == 'create:valve_handle':
                    degree = block_nbt.get('ScrollValue')
                    if nbt_int(degree) <= -200 or nbt_int(degree) >= 200:
                        log.error(f"检测到手轮篡改蓝图!后续规则不会执行|位于[{source_nbt.get('blocks').index(block)}]角度[{degree}]")
                        write_log(f"检测到手轮篡改蓝图!后续规则不会执行|位于[{source_nbt.get('blocks').index(block)}]角度[{degree}]")
                        return -1, ban_count

                if str(block_id) == 'create:chain_conveyor' and nbt_config.get('check_chain_conveyor') == 'true':

                    # log.info(f"执行特殊规则: 'create:chain_conveyor'来自第 {pos} 个方块")

                    X_P = nbt_int(block.get('pos')[0])
                    Y_P = nbt_int(block.get('pos')[1])
                    Z_P = nbt_int(block.get('pos')[2])


                    chain_parent_list.append([X_P, Y_P, Z_P])
                    check_same_item = []

                    for item in block_nbt.get('Connections'):
                        try:
                            X_C = safe_get_array(item,'X') + X_P
                            Y_C = safe_get_array(item,'Y') + Y_P
                            Z_C = safe_get_array(item,'Z') + Z_P
                        except AttributeError as e:
                            log.error(e)
                            log.error(f"{str(item)}")
                            log.error(f"{type(item)}")

                        if max(
                                abs( safe_get_array(item,'X') ),
                                abs(safe_get_array(item,'Z'))
                                    ) < abs(safe_get_array(item,'Y')):
                            log.error(f"检测到传动轮控制器角度被篡改, 后续规则不会执行|位于[{source_nbt.get('blocks').index(block)}]")
                            log.error(f"{item.get('X')}, {item.get('Y')},{item.get('Z')}")
                            log.error(f"水平最大值: {max(
                                abs( safe_get_array(item,'X') ),
                                abs(safe_get_array(item,'Z'))
                            )}|垂直最大值: {abs(safe_get_array(item,'Y'))}")
                            write_log(f"检测到传动轮控制器角度被篡改, 后续规则不会执行|位于[{source_nbt.get('blocks').index(block)}]")
                        chain_children_list.append([X_C, Y_C, Z_C])
                        check_same_item.append([X_C, Y_C, Z_C])
                    if not check_same_item:
                        log.debug("没有铁链连接")
                        # 等于0的时候即没有铁链连接
                    elif find_max_same_element_count(check_same_item) > 1:
                        log.error(f"检测到传动轮控制器被篡改, 后续规则不会执行|位于[{source_nbt.get('blocks').index(block)}]")
                        write_log(f"检测到传动轮控制器被篡改, 后续规则不会执行|位于[{source_nbt.get('blocks').index(block)}]")
                        return -1, ban_count

                if str(block_id) == 'create:belt':
                    if block_nbt.get('Inventory') is not None:
                        if str(block_nbt.get('Inventory').get('Items')) != '[]':
                            for belt_item in block_nbt.get('Inventory').get('Items'):
                                if str(belt_item.get('Item').get('id')) in ban_block:
                                    belt_item['Item']['id'] = nbt.TAG_String('minecraft:air')
                                    log.info("传送带含物品替换")
                                    ban_count += 1

                if str(block_id) == 'create:belt' and nbt_config.get('check_belt') == 'true':
                    # log.info(f"执行特殊规则: 'create:belt_connector'")
                    X = nbt_int(block_nbt.get('Controller')[0])
                    Y = nbt_int(block_nbt.get('Controller')[1])
                    Z = nbt_int(block_nbt.get('Controller')[2])
                    Controller = [X, Y, Z]
                    is_same = False
                    for item in belt_list:
                        if Controller == item[0]:
                            is_same = True
                            item[3] += 1
                    if not is_same:
                        belt_list.append([Controller, int(str(block_nbt.get('Length'))), block_nbt.get('Index'), 1])

                for rule in block_rule:
                    if str(block_id) == rule.get('block'):
                        # log.info(f"检测到单变量匹配: {rule['name']}   {rule['block']}")
                        modify_count += check_nbt_with_block(rule, block_nbt)
                for redundant in redundant_rule:
                    if str(block_id) == redundant.get('block'):
                        # log.info(f"检测到数据包匹配: {redundant['name']}   {redundant['block']}")
                        for key, word in redundant.get('Redundant').items():
                            key = key.split('.')[2:]
                            value = get_nbt_value(block_nbt, key)
                            if value is not None:
                                if word in value:
                                    # 旧版本的剪贴板可以包含剪贴板
                                    if str(value.get('BlockEntityTag').get("id")) == "create:clipboard":
                                        pass
                                    else:
                                        log.error(f"检测到非法nbt, 后续规则不会执行|位于[{source_nbt.get('blocks').index(block)}][{str(value.get('BlockEntityTag').get('id'))}]")
                                        write_log(f"检测到非法nbt, 后续规则不会执行|位于[{source_nbt.get('blocks').index(block)}][{str(value.get('BlockEntityTag').get('id'))}]")
                                        return -1, ban_count
                                else:
                                    pass

                block_nbt_str = str(block_nbt.pretty_tree())
                for modify_ban_block in config.ban_block:
                    if modify_ban_block in block_nbt_str:
                        log.warning(f"第[{pos}]个方块没有清理干净，包含[{modify_ban_block}]")
                        print(block_nbt_str)

        # print(chain_parent_list)
        # print(chain_children_list)

        if nbt_config.get('check_chain_conveyor') == 'true' and chain_parent_list != []:
            if nbt_config.get('conveyor_max_connection') < find_max_same_element_count(chain_children_list):
                log.info(
                    f"传动轮连接数量[{nbt_config.get('conveyor_max_connection')}]超过最大配置数量[{find_max_same_element_count(chain_children_list)}], 后续规则不会执行")
                write_log(
                    f"传动轮连接数量[{nbt_config.get('conveyor_max_connection')}]超过最大配置数量[{find_max_same_element_count(chain_children_list)}], 后续规则不会执行")

                return -1, ban_count
            for item in chain_children_list:
                if item not in chain_parent_list:
                    write_log(f"检测到传动轮被篡改, 坐标{item}没有双向配对, 后续规则不会执行")
                    log.error(f"检测到传动轮被篡改, 坐标{item}没有双向配对, 后续规则不会执行")
                    return -1, ban_count
        if nbt_config.get('check_belt') == 'true' and belt_list != []:
            for belt in belt_list:
                if belt[1] != belt[3]:
                    write_log("检测到传送带数据不完整或被篡改, 后续规则不会执行")
                    log.error("检测到传送带数据不完整或被篡改, 后续规则不会执行")
                    return -1, ban_count

        for palette in source_nbt.get('palette'):
            block_id = palette.get('Name')
            if block_id is not None:
                if str(block_id) == 'create_connected:kinetic_battery':
                    if palette.get('Properties') is not None:

                        properties = palette['Properties']
                        if str(properties['level']) != "0":
                            properties['level'] = nbt.TAG_Int(0)
                            write = True
                            log.info("归零了电池等级")



                if str(block_id) in ban_block:
                    # log.debug(type(block_nbt['id']))
                    palette['Name'] = nbt.TAG_String('minecraft:air')
                    ban_count += 1
                for rule_23 in palette_rule:
                    if str(block_id) == rule_23.get('block'):
                        modify_count += check_nbt_with_palette(rule_23, palette)

        for entity in source_nbt.get('entities'):
            entity_type = entity.get('nbt').get('id')
            if entity_type is not None:
                if str(entity_type) in ban_entity:
                    log.error(f"命中规则{entity_type}")
            else:
                log.error("没有找到ID")

        if modify_count != 0 or ban_count != 0 or entity_handle or write or change_file:
            log.info("文件被修改, 写入中。")
            source_nbt.write_file(source_path_1)
        return modify_count, ban_count
    return None



if __name__ == '__main__':
    source_path = r'/schematics/kongyu/uploaded/Daybreak2486/kongqi.nbt'  # 替换为你的 NBT 文件路径
    ban_tags = ["AttributeModifiers", "Enchantments"]
    ban_block = ["create:creative_crate", "create:creative_fluid_tank", "create:creative_motor"]
    nbt_rule = load_rule(convert_to_string=True)
    interesting = []
    # for rule in nbt_rule.get('rules', []):
     #    interesting.append(rule.get('block'))
    # str_result = str_check(source_path, interesting, ban_tags, ban_block)
    # if str_result == -1:
       #  print("dead")
    # elif str_result == 0:
       #  print("nothing")
    # else:
    #     print("in_check")
     #    rule_check(source_path, nbt_config=nbt_rule)
