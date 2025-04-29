import hashlib
import os
import shutil
from datetime import datetime
from Checker.lib.log_color import log

def ensure_directory_exists(directory):
    """确保目录存在，如果不存在则创建"""
    if not os.path.exists(directory):
        os.makedirs(directory)

def move_file(src, dest):
    """将文件从A目录移动到B目录"""
    ensure_directory_exists(os.path.dirname(dest))
    if os.path.isfile(src):
        shutil.move(src, dest)
    else:
        log.error(f"源文件不存在: {src} -> {dest}")

def ensure_directory_exists(directory):
    """确保目录存在，如果不存在则创建"""
    if not os.path.exists(directory):
        os.makedirs(directory)

def calculate_md5(file_path):
    """计算文件的MD5哈希值"""
    hash_md5 = hashlib.md5()
    with open(file_path, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash_md5.update(chunk)
    return hash_md5.hexdigest()

def copy_file_to_year_folder(src, dest):
    """将文件复制到B目录的文件夹中"""
    ensure_directory_exists(dest)
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
                # 如果文件名相同但内容不同，添加日期后缀
                base_name, extension = os.path.splitext(file_name)
                new_file_name = f"{base_name}_{datetime.now().strftime('%Y%m%d_%H%M%S')}{extension}"
                target_file_path = os.path.join(dest, new_file_name)

        # 复制文件
        shutil.copy(src, target_file_path)
        # log.debug(f"文件已复制到: {target_file_path}")
    else:
        log.error(f"源文件不存在: {src}->")


def delete_file(file_path):
    """删除指定的文件"""
    if os.path.isfile(file_path):
        os.remove(file_path)
    else:
        log.error(f"文件不存在: {file_path}")




# 示例用法
if __name__ == "__main__":
    print("cats")
    # 移动文件示例
    # move_file('B/your_file.txt', 'A/your_file.txt')

    # 复制文件到年份文件夹示例
    copy_file_to_year_folder('A/your_file.txt', 'B/C')
    # os.rename('B/C/your_file.txt','B/C/your_f35le.txt')

    # 删除文件示例
    # delete_file('B/C/2025/your_file.txt')
