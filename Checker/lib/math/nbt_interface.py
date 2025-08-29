import os

from anyio.streams import file
from nbt import nbt

from Checker.lib.log_color import log


def path_get_nbt(name, file):
    source_path_1 = f"{name}/{file}"
    # 加载 NBT 文件
    try:
        source_nbt = nbt.NBTFile(source_path_1)
        return source_nbt
    except UnicodeDecodeError as e:
        log.error(f"无法读取文件nbt {source_path_1}, 编码错误: {e} 可能是损坏的蓝图或不兼容的蓝图！")
    except nbt.MalformedFileError as e:
        log.error(f"无法读取文件nbt {source_path_1}, NBT格式错误: {e} 可能是损坏的蓝图或不兼容的蓝图！")
    except Exception as e:
        log.error(f"无法读取文件nbt {source_path_1}, 错误: {e} ")

    # 删除文件
    if os.path.exists(source_path_1):
        log.warning(f"由于蓝图文件无法读取，为防止漏洞蓝图进入服务器，CSC将会自动移除: {source_path_1}")
        # os.remove(source_path_1)   # 替代不安全的删除为存档，保证后期检查
        return None

    return None


if __name__ == '__main__':
    data = nbt.NBTFile("怖冥工坊V3.0.nbt")
    intest =  1

    is_in_check = 0
    blocks = data['blocks']
    for block in blocks:
        str_block = str(block.pretty_tree())
        count = str_block.count('minecraft:kelp')
        if count != 0:
            is_in_check += 1
            if is_in_check == intest:
                data =  block['nbt']

                def handle_fanc_menu(in_data):
                    if in_data.get('Filter') is not None:
                        Filter = in_data['Filter']
                        filter_id = Filter.get('id')
                        print(str(filter_id))
                    print("---------------------------")
                    return

                if data.get('top_right') is not None:
                    handle_fanc_menu(data['top_right'])
                    handle_fanc_menu(data['top_left'])
                    handle_fanc_menu(data['bottom_right'])
                    handle_fanc_menu(data['bottom_left'])

