import traceback,os
from nbt import nbt
from Checker import nbt_rule
import config
from Checker.lib.sugar import timer
from Checker.lib.log_color import log,write_log
from Checker.lib.file_size_io import wait_for_file_transfer_complete
from Checker.lib.hash_map_handler import calculate_md5
from Checker.lib.rule_handler import save_md5,load_rule,extract_rules
from Checker.lib import file_handle

log_directory = 'logs'  # 日志文件夹
os.makedirs(log_directory, exist_ok=True)  # 创建日志文件夹（如果不存在）
log_file_path = os.path.join(log_directory, 'my_log_file.txt')  # 日志文件完整路径




def nbt_loader(name, file):
    log.warning(f"{config.schematics_path}/{name}/{file}")
    file_data = nbt.NBTFile(f"{config.schematics_path}/{name}/{file}")
    return file_data


@timer
def count_block_ids(data):
    block_count = {}  # 用于存储每个 ID 的计数
    total_count = 0
    if 'blocks' in data:
        blocks = data['blocks']
        for block in blocks:
            if 'state' in block:
                block_id =str(data['palette'][nbt_rule.nbt_int(block.get('state'))].get('Name'))
                if block_id in block_count:
                    block_count[block_id] += 1  # 增加计数
                else:
                    block_count[block_id] = 1  # 初始化计数
                total_count += 1
    return block_count,total_count

def check_handler(player_name, filename):
    problem_path = f"save/problem_schematic/{player_name}/{filename}"
    is_cheat_schematic,hash_md5 = main_check(player_name, filename)
    if is_cheat_schematic:
        # 移动文件到异常蓝图
        file_handle.move_file(f'save/{filename}', problem_path)
        log.error(f"筛查到异常蓝图: {player_name}/{filename}")
        write_log(f"↑↑↑↑|{hash_md5}|异常蓝图:{player_name}/{filename}")
        file_handle.copy_file_to_year_folder("rule/chanhuishu.nbt", f"{config.schematics_path}/{player_name}")
        os.rename(f"{config.schematics_path}/{player_name}/chanhuishu.nbt", f"{config.schematics_path}/{player_name}/{filename}")
        log.info(f"触发蓝图替换")
    else:
        file_handle.move_file(f'save/{filename}', f"{config.schematics_path}/{player_name}/{filename}")

def delete_file(file_path):
    try:
        # 检查文件是否存在
        if os.path.exists(file_path):
            os.remove(file_path)  # 删除文件
            log.debug(f"文件 {file_path} 已成功删除。")
        else:
            log.debug(f"文件 {file_path} 不存在。")
    except Exception as e:
        log.error(f"删除文件时发生错误: {e}")

def main_check(name, file):

    check_result = 1
    dead = False  # whether is cheat schematic
    source_path = f"{config.schematics_path}/{name}/{file}"
    check_path = f'save/{file}'

    complete = wait_for_file_transfer_complete(source_path)
    if complete:
        file_handle.move_file(source_path, check_path)
        file_handle.copy_file_to_year_folder(check_path, f"save/backup/{name}")
        blue_print_path = check_path



        try:
            global_rule = load_rule(convert_to_string=True)
            block_rule, palette_rule, redundant_rule = extract_rules(global_rule)
        except Exception as e:
            log.error(f"Failed to load rule: {e}")
            global_rule = None

        # log.info("进入检查")
        hash_trust = load_rule(path="rule/schematics.yml")
        hash_cal = calculate_md5(blue_print_path)
        if hash_trust is not None and hash_trust['md5_hashes'] is not None:
            for hash_item in hash_trust['md5_hashes']:
                hash_item=hash_item.split("|")
                if hash_item[0] == hash_cal:
                    if hash_item[1]==str(global_rule.get('version')):
                        log.info(f"检查到指纹历史:[{name}|{file}]")
                        # log.debug(hash_item)
                        if hash_item[2] == "True":
                            write_log("相同的文件md5，查看历史日志获得蓝图问题")
                            return True,hash_cal
                        else:
                            return False,hash_cal
        else:
            delete_file("rule/schematics.yml")
                # log.debug(hash_item)
        # log.info(hash_cal)


    if complete:   # 检查文件是否传输完成
        if config.count_block:
            # 统计方块信息
            data = nbt_loader(name, file)
            block_statistics,total_count = count_block_ids(data)
            log.info(f"方块信息统计:[玩家|{name}][{file}][{total_count} 方块]")
            for block_id, count in block_statistics.items():
                log.info(f"ID: {block_id}, 数量: {count}")


        interesting = []
        for rule in global_rule.get('rules'):
            interesting.append(rule.get('block'))
        str_result = nbt_rule.str_check(blue_print_path, interesting, config.ban_tags, config.ban_block)
        if str_result == -1:
            log.error("包含异常标签，蓝图为创造蓝图或篡改蓝图！")
            write_log("包含异常标签，蓝图为创造蓝图或篡改蓝图！")
            dead = True
        elif str_result == 0:
            pass
            # log.info("没有发现问题")
        else:
            try:

                check_result = nbt_rule.rule_check(blue_print_path, block_rule, palette_rule, redundant_rule, nbt_config=global_rule)
                if check_result >= 1:
                    log.warning(f"替换规则触发次数： {check_result}")
                if check_result == -1:
                    dead = True

            except Exception as e:
                if "has no attribute" in str(e):
                    log.error("无法读取标签，蓝图可能被篡改")
                    dead = True
                else:
                    log.error(f"执行rule_check 发生异常 {e}")
                    traceback.print_exc()

    path_md5 = r"rule/schematics.yml"
    if check_result < 1:  # 触发替换规则的蓝图不会记录指纹，因为下次再见到仍然需要替换，无法降低耗时
        save_md5(path_md5,f"{hash_cal}|{global_rule['version']}|{dead}")
    return dead,hash_cal


if __name__ == '__main__':
    name = "Daybreak2486"
    file = "kongqi.nbt"
    is_cheat = check_handler(name, file)
    log.info(is_cheat)
