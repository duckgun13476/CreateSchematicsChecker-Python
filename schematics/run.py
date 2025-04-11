import os
import time
from lib.sugar import timer
from nbt_func import main_check
from lib.log_color import log

# 获取当前工作目录
current_directory = os.getcwd()
uploaded_directory = os.path.join(current_directory, 'uploaded')


def check_nbt_files():
    nbt_files_dict = {}  # 存储玩家名字及对应的 NBT 文件名和修改时间的字典

    # 遍历 uploaded 目录中的所有玩家文件夹
    for player_folder in os.listdir(uploaded_directory):
        player_path = os.path.join(uploaded_directory, player_folder)

        # 确保是文件夹
        if os.path.isdir(player_path):
            # 查找该玩家文件夹中的所有 NBT 文件
            nbt_files_info = []
            nbt_files = [filename for filename in os.listdir(player_path) if filename.endswith('.nbt')]

            for filename in nbt_files:
                file_path = os.path.join(player_path, filename)
                # 获取文件的修改时间
                modification_time = os.path.getmtime(file_path)
                # 将文件名和修改时间添加到列表中
                nbt_files_info.append((filename, time.ctime(modification_time)))

            if nbt_files_info:
                nbt_files_dict[player_folder] = nbt_files_info  # 将玩家名和文件信息添加到字典中
            else:
                pass

    return nbt_files_dict  # 返回包含玩家及其 NBT 文件的字典


def check_recent_nbt_files_and_execute(nbt_files_dict):
    current_time = time.time()  # 获取当前时间的时间戳

    # 遍历字典中的每个玩家及其 NBT 文件信息
    for player, files_info in nbt_files_dict.items():
        for filename, modification_time in files_info:
            # 将修改时间转换为时间戳
            mod_time_timestamp = time.mktime(time.strptime(modification_time))

            # 计算时间差
            time_difference = current_time - mod_time_timestamp
            # print(time_difference)
            # 检查时间差是否小于 5 分钟（300 秒）
            if time_difference < 300:
                # 调用 main_check 函数，只传入 player 和 filename
                # print(filename)
                main_check(player, filename)


@timer
def main_loop(previous_nbt_file1, current_nbt_files_1):
    check_recent_nbt_files_and_execute(current_nbt_files_1)
    inside_check = False
    # 检查新增的 NBT 文件
    added_files = {}
    for player, files in current_nbt_files_1.items():
        if player not in previous_nbt_file1:
            added_files[player] = files
        else:
            # 使用字典来存储文件名和修改时间
            previous_files_dict = {f[0]: f[1] for f in previous_nbt_file1[player]}
            new_files = []

            for filename, modification_time in files:
                # 如果文件名存在且修改时间不同，则视为新增
                if filename not in previous_files_dict or previous_files_dict[filename] != modification_time:
                    new_files.append((filename, modification_time))

            if new_files:
                added_files[player] = new_files
    # log.info(added_files)
    for player, files in added_files.items():
        for filename, modification_time in files:
            log.info(f"新增+ NBT 文件: {filename} (玩家: {player})")
            log.info("第一次检查")
            main_check(player, filename)
            inside_check = True

    # 检查减少的 NBT 文件
    removed_files = {}
    for player, files in previous_nbt_file1.items():
        if player not in current_nbt_files_1:
            removed_files[player] = files
        else:
            removed_files_for_player = {(f[0], f[1]) for f in files} - {(f[0], f[1]) for f in
                                                                        current_nbt_files_1[player]}
            if removed_files_for_player:
                removed_files[player] = list(removed_files_for_player)

    for player, files in removed_files.items():
        for filename, modification_time in files:
            log.info(f"减少- NBT 文件: {filename} (玩家: {player})")
            inside_check = False
    # log.info(added_files)
    # 更新之前的 NBT 文件列表
    return current_nbt_files_1,inside_check


if __name__ == '__main__':
    log.info("开始执行！")
    previous_nbt_files = check_nbt_files()  # 初始 NBT 文件列表
    while True:
        time.sleep(2)
        current_nbt_files = check_nbt_files()  # 获取当前 NBT 文件列表
        previous_nbt_files = main_loop(previous_nbt_files, current_nbt_files)
