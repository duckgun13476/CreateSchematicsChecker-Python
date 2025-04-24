import os
import time
from Checker.lib.log_color import log
from config import schematics_packet_size

def wait_for_file_transfer_complete(file_path, check_interval=0.1, max_duration=120):
    """
    等待文件传输完成，通过检查文件大小的变化来判断。
    
    :param file_path: 要检查的文件路径
    :param check_interval: 每次检查之间的间隔（秒）
    :param max_duration: 最大等待时间（秒）
    :return: 文件传输是否完成的布尔值
    """
    log.debug("完整性校验")
    if os.path.getsize(file_path) % schematics_packet_size != 0:
        log.debug(f"文件已在本地~ 跳过上传检查")
        return True
    if not os.path.exists(file_path):
        log.error(f"文件 {file_path} 不存在。")
        return False
    last_size = -1
    stable_count = 0
    start_time = time.time()

    while True:
        current_size = os.path.getsize(file_path)
        if current_size > 0:
            if current_size != last_size:
                pass
            if current_size % schematics_packet_size != 0:
                log.info(f"文件传输完毕: (文件大小: {current_size} 字节 用时{time.time() - start_time:.2f}秒)")
                return True
            # 如果文件大小为数据包的整数倍，检查稳定性
            if current_size == last_size:
                stable_count += 1  # 增加稳定计数
            else:
                stable_count = 0  # 重置计数器
            last_size = current_size  # 更新上一个大小
            # 如果文件大小在2秒内没有变化
            if stable_count >= 20:  # 20 * 0.1秒 = 2秒
                log.info(f"文件传输完毕: (文件大小: {current_size} 字节 用时{time.time() - start_time})")
                return True
        else:
            # print("文件大小为 0 字节，可能正在上传中。")
            pass
        
        # 检查是否超时
        if time.time() - start_time >= max_duration:
            log.error("超出最大等待时间，文件传输未完成。")
            return False

        time.sleep(check_interval)

if __name__ == '__main__':
# 示例用法
    while True:
        result = wait_for_file_transfer_complete(r'uploaded/Pink_Candy_Cats/test.nbt')
        time.sleep(0.2)
        print("传输完成:", result)
