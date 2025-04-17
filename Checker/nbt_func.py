from nbt import nbt
import config
from lib.sugar import timer
from lib.log_color import log
import os,shutil
from nbt_check import belt_check
from datetime import datetime

from Checker.lib.file_size_io import wait_for_file_transfer_complete

log_directory = 'logs'  # 日志文件夹
os.makedirs(log_directory, exist_ok=True)  # 创建日志文件夹（如果不存在）
log_file_path = os.path.join(log_directory, 'my_log_file.txt')  # 日志文件完整路径


def write_log(log_message):
    with open(log_file_path, 'a', encoding='utf-8') as log_file:  # 以追加模式打开文件
        log_file.write(log_message + '\n')  # 写入内容并换行


def nbt_loader(name, file):
    log.warning(f"{config.schematics_path}/{name}/{file}")
    file_data = nbt.NBTFile(f"{config.schematics_path}/{name}/{file}")
    return file_data


@timer
def count_block_ids(data):
    block_count = {}  # 用于存储每个 ID 的计数
    total_count = 0
    if 'palette' in data:
        blocks = data['palette']

        for block in blocks:
            if 'Name' in block:
                block_id = block['Name'].value  # 获取 block 的 ID
                if block_id in block_count:
                    block_count[block_id] += 1  # 增加计数
                else:
                    block_count[block_id] = 1  # 初始化计数
                total_count += 1
    return block_count,total_count


def search_for_string_match(data, check_string_23):
    data_str = str(data.pretty_tree())  # 将 NBT 数据转换为字符串
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


def replace_item_with_air(nbt_data, item_to_check, error):
    def replace_in_palette(palette):
        for entry in palette:
            if 'Name' in entry:
                if entry['Name'].value in item_to_check:
                    log.warning(f"警告: 找到异常 ID 物品，包含 {entry['Name'].value}，将其替换为 minecraft:air")
                    # entry['id'].value = "minecraft:air"
                    entry['Name'].value = "minecraft:air"  # 替换 Name 标签的内容

    def replace_in_blocks(blocks):
        for block in blocks:
            if 'id' in block:
                if block['id'].value in item_to_check:
                    log.warning(f"警告: 找到异常 ID 物品，包含 {block['id'].value}，将其替换为 minecraft:air")
                    block['id'].value = "minecraft:air"
                    # block['Count'].value = 0  # 将数量设置为 0
            if 'nbt' in block:
                # 异常物品剔除
                if block['nbt']['id'].value in item_to_check:
                    log.warning(f"警告: 找到异常 ID 物品，包含 {block['nbt']['id'].value}，将其替换为 minecraft:air")
                    block['nbt']['id'].value = "minecraft:air"

    # 异常传送带剔除
    def handle_belt(blocks):
        for block in blocks:
            if 'nbt' in block:
                if block['nbt']['id'].value == 'create:belt':
                    if block['nbt']['Length'].value > 20:
                        log.warning(f"警告: 找到异常传送带，长度为[{block['nbt']['Length'].value}]，将其替换为 20")
                        block['nbt']['Length'].value = 20

    if not error:
        # 处理 palette 和 blocks
        if 'palette' in nbt_data:
            replace_in_palette(nbt_data['palette'])
        if 'blocks' in nbt_data:
            replace_in_blocks(nbt_data['blocks'])
        return nbt_data
    if error:
        if 'blocks' in nbt_data:
            handle_belt(nbt_data['blocks'])
        return nbt_data


def main_check(name, file):
    dead = False  # whether is cheat schematic
    blue_print_path = f"{config.schematics_path}/{name}/{file}"
    log.info("进入检查")
    complete = wait_for_file_transfer_complete(blue_print_path)
    if complete:   # 检查文件是否传输完成

        # 需要检查的标签列表
        data = nbt_loader(name, file)  # load  nbt
        block_statistics,total_count = count_block_ids(data)  # 统计 blocks 下的 entries 下的 nbt 下的 id


        # 输出统计结果
        log.info(f"方块信息统计:[{name}][{file}][{total_count} 方块]")
        belt_solve = False  # bollen para to decide whether to check

        for block_id, count in block_statistics.items():
            log.info(f"ID: {block_id}, 数量: {count}")
            if block_id in config.block_to_check:
                belt_solve = True


        tag_count, item_count = search_for_string_match(data, [config.tags_to_check, config.block_to_check])

        if tag_count or item_count or belt_solve:
            # 保存异常的蓝图
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            file_name, file_extension = os.path.splitext(file)  # 分离文件名和扩展名
            new_file_name = f"{timestamp}_{file_name}{file_extension}"  # 新的文件名
            warn_path = f"problem_schematics/{name}/{new_file_name}"  # 更新warn_path
            os.makedirs(os.path.dirname(warn_path), exist_ok=True)
            shutil.copy(blue_print_path, warn_path)
            log.info("异常蓝图已存储")


        if tag_count + item_count or belt_solve:

            # 在log文件下记录
            target_path = f"{config.schematics_path}/{name}/{file}"
            text_warn = f"记录异常蓝图:[{name}][{file}]-[tag][{tag_count}]-[item][{item_count}]-[error][{belt_solve}]"
            log.warning(text_warn)
            write_log(text_warn)

            # 这些tag根本不可能在标准蓝图下出现
            if tag_count:
                log.warning(f"玩家[{name}]的蓝图[{file}]存在异常，异常标签计数：tag[{tag_count}]")
                dead = True  # 准备忏悔，救不了了（99%是bug蓝图）
                source_path = "lib/chanhuishu.nbt"
                log.info(f"替换文件内容: {target_path}，使用源文件: {source_path}")
                try:
                    # 加载源 NBT 文件 替换问题文件
                    target_nbt = nbt.NBTFile(source_path)
                    target_nbt.write_file(target_path)
                    log.info(f"成功替换文件内容: {target_path}")
                except FileNotFoundError:
                    log.error(f"文件未找到: {source_path} 或 {target_path}")
                except Exception as e:
                    log.error(f"处理文件 {target_path} 时出错: {e}")
                return dead

            # 发现了需要检查的方块
            if item_count:
                log.warning(f"玩家[{name}]的蓝图[{file}]存在异常，白名单物品计数：item[{item_count}]")
                nbt_file = nbt.NBTFile(f"{config.schematics_path}/{name}/{file}")

                nbt_file = replace_item_with_air(nbt_file, config.block_to_check, False)
                nbt_file.write_file(f"{config.schematics_path}/{name}/{file}")
            if belt_solve:
                log.info(f"玩家[{name}]的蓝图[{file}]存在传送带，执行检查")
                path = f"{config.schematics_path}/{name}/{file}"
                log.info(belt_check(path))
            log.info("检测完毕")

    return dead


if __name__ == '__main__':
    name = "csy12345"
    file = "砂狼白子.nbt"
    main_check(name, file)
