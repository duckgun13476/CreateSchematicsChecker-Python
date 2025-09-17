import hashlib
import os
import shutil
from datetime import datetime

import yaml

from Checker.lib.file_size_io import resource_path
from Checker.lib.log_color import log
from Checker.lib.setting.config_gen import schematic_sha_path
from Checker.lib.setting.nbt_set import generate_nbt_file


def ensure_sha_exist():
    path = schematic_sha_path
    if not os.path.exists(path):
        # 如果文件不存在，创建目录（如果需要）
        os.makedirs(os.path.dirname(path), exist_ok=True)
        existing_data = {'md5_hashes': []}
        with open(path, 'w', encoding='utf-8') as file:
            yaml.dump(existing_data, file, allow_unicode=True)  # 写入初始内容
        print(f'INFO     文件 {path} 已创建。')
    else:
        pass


def ensure_directory_exists(directory):
    """确保目录存在, 如果不存在则创建"""
    if not os.path.exists(directory):
        os.makedirs(directory)


def move_file(src, dest):
    """将文件从A目录移动到B目录"""
    ensure_directory_exists(os.path.dirname(dest))
    if os.path.isfile(src):
        shutil.move(src, dest)
    else:
        log.error(f"源文件不存在: {src} -> {dest}")


def calculate_md5(file_path):
    """计算文件的MD5哈希值"""
    hash_md5 = hashlib.md5()
    with open(file_path, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash_md5.update(chunk)
    return hash_md5.hexdigest()


def copy_file_to_year_folder(src, dest):
    # if "rule" in src:
   #      src = resource_path(src)
    # else:
      #   pass
    """将文件复制到B目录的文件夹中"""
    ensure_directory_exists(dest)
    def handle_file(src):

        if os.path.isfile(src):
            # 源文件名和目标文件路径
            file_name = os.path.basename(src)
            target_file_path = os.path.join(dest, file_name)
            # 检查目标文件夹是否有相同名字的文件
            if os.path.isfile(target_file_path):
                # 计算MD5哈希值
                source_md5 = calculate_md5(src)
                target_md5 = calculate_md5(target_file_path)
                if source_md5 == target_md5:
                    log.debug(f"文件已存在且内容相同: {target_file_path}")
                    return
                else:
                    # 如果文件名相同但内容不同, 添加日期后缀
                    base_name, extension = os.path.splitext(file_name)
                    new_file_name = f"{base_name}_{datetime.now().strftime('%Y%m%d_%H%M%S')}{extension}"
                    target_file_path = os.path.join(dest, new_file_name)

            # 复制文件
            shutil.copy(src, target_file_path)
            # log.debug(f"文件已复制到: {target_file_path}")
        else:
            log.error(f"源文件不存在: {src}->")
    try:
        handle_file(src)
    except FileNotFoundError:
        if "chanhuishu.nbt" in src:
            generate_nbt_file(src)
            handle_file(src)


def delete_file(file_path):
    """删除指定的文件"""
    try:
        if os.path.isfile(file_path):
            os.remove(file_path)
        else:
            log.error(f"文件不存在: {file_path}")
    except Exception as e:
        log.error(f"删除文件时发生错误: {e}")


def copy_file(src, dst):
    try:
        shutil.copy(src, dst)
    except Exception as e:
        log.error(f"复制文件时发生错误:  {e}")


# 示例用法
if __name__ == "__main__":
    log.info("cats")
    # 移动文件示例
    # move_file('B/your_file.txt', 'A/your_file.txt')

    # 复制文件到年份文件夹示例
    copy_file_to_year_folder('A/your_file.txt', 'B/C')
    # os.rename('B/C/your_file.txt','B/C/your_f35le.txt')

    # 删除文件示例
    # delete_file('B/C/2025/your_file.txt')
