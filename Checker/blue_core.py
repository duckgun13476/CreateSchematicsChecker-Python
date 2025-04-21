from Checker.lib.package_handler import handle_package
handle_package()
import config
from datetime import datetime
from nbt_func import check_handler
import os, time
from lib.sugar import timer
from lib.log_color import log
import threading
from Checker import nbt_rule
from Checker.rule_handler import load_rule
from Checker.api_shulker import version_handler_in

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
    log.info(f"已同步 [{player_name}|{filename}] 的代码修改时间为: {file_mod_time}")


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
        print(f"已在运行: {player_name} - {filename}")


@timer
def run_main():

    nbt_files_dict = search_nbt_files()  # 获取所有 NBT 文件信息
    # log.info(nbt_files_dict)  # 打印 NBT 文件字典

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
    log.info("当前代码修改时间：")  # 使用格式化字符串
    for player_name, code_mod_times in code_mod_times.items():
        log.info(player_name + ": " + str(code_mod_times))


    turn = 0
    total_count = 0
    while True:
        last_count = total_count
        turn += 1
        post: int = 0
        time.sleep(config.check_frequency)  # 每隔？秒检查一次
        nbt_files_dict = search_nbt_files()  # 获取所有 NBT 文件信息
        total_count = 0
        for player, nbt_files in nbt_files_dict.items():
            total_count += len(nbt_files)
        if total_count != last_count:
            log.info(f"[变动检查]找到的nbt文件数量[{total_count}]")
            post += 1
            if post > 10:
                post = 0
                log.info("定时更新规则————")
                update_version = int(version_handler_in())
                local_version = int(load_rule().get('version'))
                if update_version > local_version:
                    log.info("检测到规则更新！！")
                else:
                    pass

        if turn >= 100/config.check_frequency:
            turn = 0
            log.info(f"[活跃提示]蓝图数量[{total_count}]")

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

                if abs((file_mod_time_1 - code_mod_time_1).total_seconds()) < 10:
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
            log.error(e)
            time.sleep(1)

