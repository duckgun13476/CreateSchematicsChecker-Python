import os
import sys

# Dynamically add the parent directory to sys.path if running directly
if __name__ == "__main__" and __package__ is None:
    sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
    __package__ = "Checker"

from Checker.lib.package_handler import handle_package
handle_package()

import config
from datetime import datetime
from Checker.nbt_func import check_handler
import time
from Checker.lib.sugar import timer
from Checker.lib.log_color import log
import threading
from Checker.lib import file_handle
from Checker.lib.rule_handler import load_rule
from Checker.api_shulker import version_handler_in, get_latest_rule, save_data_to_yaml

# 用于存储正在进行的线程
active_threads = {}
# 获取当前工作目录
current_directory = os.getcwd()
uploaded_directory = os.path.join(current_directory, config.schematics_path)


def search_nbt_files():
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


def sync_code_mod_time(code_mod_times, player_name, filename, file_mod_time):
    # 同步代码修改时间
    code_mod_times[player_name][filename] = file_mod_time
    log.info("已同步 [%s|%s] 的代码修改时间为: %s", player_name, filename, file_mod_time)


def check_and_run(player_name, filename, file_mod_time, code_mod_times):
    thread_id = (player_name, filename)
    if thread_id not in active_threads:
        thread = threading.Thread(target=check_handler, args=(player_name, filename))
        active_threads[thread_id] = thread
        thread.start()
        # 同步代码修改时间
        sync_code_mod_time(code_mod_times, player_name, filename, file_mod_time)
        # 线程结束后从活动线程列表中移除
        thread.join()  # 等待线程完成
        del active_threads[thread_id]
    else:
        log.error("已在运行: %s - %s", player_name, filename)


def remove_lines_with_value(file_path, target_value):
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            lines = file.readlines()
        filtered_lines = [line for line in lines if f"|{target_value}|" not in line]
        with open(file_path, 'w', encoding='utf-8') as file:
            file.writelines(filtered_lines)
        log.info(f"已删除版本为[{target_value}]的历史检测 ，更新后的数据已保存回指纹文件！")
    except Exception as e:
        log.error(f"处理文件时出错: {e}")


def update_rule():
    log.info("检查规则更新————")
    update_version = float(version_handler_in())
    local_version = float(load_rule().get('version'))
    if update_version > local_version:
        log.info(f"检测到规则更新！！本地配置版本：[{local_version}]最新版本：[{update_version}]")
        log.info("准备下载规则文件。。。")
        rule_info = get_latest_rule().get('data')
        log.info(f"最新规则文件版本:{update_version}")
        file_handle.copy_file_to_year_folder("rule/standard.yml", "save/rule_backup")
        file_handle.delete_file("rule/standard.yml")
        save_data_to_yaml(rule_info, "rule/standard.yml")
        log.warning("由于规则更新，旧版检测可能失效或过时，旧版的检测结果将被移除！！")
        remove_lines_with_value("rule/schematics.yml",str(local_version))
        log.info("处理完毕！")
    else:
        log.info("规则已为最新")



@timer
def run_main():
    update_rule()
    time.sleep(2)
    nbt_files_dict = search_nbt_files()  # 获取所有 NBT 文件信息
    # 创建一个字典来存储代码修改时间
    code_mod_times = {player: {file_info[0]: file_info[1] for file_info in files} for player, files in
                      nbt_files_dict.items()}
    # 第一次循环：同步文件和代码的修改时间
    for player_name, files in nbt_files_dict.items():
        for file_info in files:
            filename = file_info[0]  # 获取文件名
            file_mod_time = file_info[1]  # 获取文件的修改时间
            # 同步文件修改时间和代码修改时间
            code_mod_times[player_name][filename] = file_mod_time

    log.info("第一次循环完成，已同步文件和代码的修改时间。")
    log.info(f"路径为{config.schematics_path}")
    log.info("当前代码修改时间：")  # 使用格式化字符串
    for player_name, code_mod_times in code_mod_times.items():
        log.info(player_name + ": " + str(code_mod_times))

    turn = 0
    total_count = 0
    post: int = 0
    while True:
        last_count = total_count
        turn += 1
        time.sleep(config.check_frequency)  # 每隔？秒检查一次
        nbt_files_dict = search_nbt_files()  # 获取所有 NBT 文件信息
        total_count = 0
        for player, nbt_files in nbt_files_dict.items():
            total_count += len(nbt_files)
        if total_count != last_count:
            log.info(f"[变动检查]找到的nbt文件数量[{total_count}]")
        if turn >= 100/ config.check_frequency:
            turn = 0
            log.info("[活跃提示]蓝图数量[%d][%s]", total_count, datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
            post += 1
            if post > 20:
                post = 0
                update_rule()

        # 第二次循环：进行比较
        for player_name, files in nbt_files_dict.items():
            for file_info in files:
                filename = file_info[0]  # 获取文件名
                file_mod_time = file_info[1]  # 获取文件的修改时间
                # 获取对应的代码修改时间
                if player_name not in code_mod_times:
                    code_mod_times[player_name] = {}
                    current_time = datetime.now().strftime('%a %b %d %H:%M:%S %Y')
                    code_mod_times[player_name][filename] = current_time
                    # main_check(player_name, filename)
                code_mod_time = code_mod_times[player_name].get(filename)
                # log.info(f"{code_mod_time}, {file_mod_time}")
                # 比较文件修改时间和代码修改时间
                if file_mod_time is None:
                    file_mod_time = 'Fri Nov  8 22:36:21 2024'
                if code_mod_time is None:
                    code_mod_time = 'Fri Nov  8 22:36:21 2024'

                file_mod_time_1 = datetime.strptime(file_mod_time, '%a %b %d %H:%M:%S %Y')
                code_mod_time_1 = datetime.strptime(code_mod_time, '%a %b %d %H:%M:%S %Y')

                if abs((file_mod_time_1 - code_mod_time_1).total_seconds()) < 0.5:
                    pass
                    # log.info(f"{filename} 的修改时间相同，跳过检查。")
                else:
                    check_and_run(player_name, filename, file_mod_time, code_mod_times)


if __name__ == '__main__':
    while True:
        try:
            log.info("启动主线程中")
            run_main()
        except Exception as e:
            if "The system cannot find the path" in str(e):
                log.error("蓝图路径不存在或指定错误！")
                log.info(r"提示：请确保路径为 绝对路径 Linux：/example/uploaded | Win：F:\CreateEntityControler\create\uploaded")
                time.sleep(5)
                exit("PATH NOT FOUND")
            else:
                log.error("运行主线程发生错误：%s", e)
                time.sleep(5)

