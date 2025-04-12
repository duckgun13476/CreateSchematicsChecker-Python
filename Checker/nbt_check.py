from nbt import nbt
import os
# about to delete

def belt_check(source_path_1):
    # 加载 NBT 文件
    try:
        source_nbt = nbt.NBTFile(source_path_1)
    except Exception as e:
        print(f"无法读取文件 {source_path_1}，错误: {e}")
        # 删除文件
        if os.path.exists(source_path_1):
            os.remove(source_path_1)
            print(f"文件 {source_path_1} 已删除。")
    # 访问 blocks 标签
    blocks = source_nbt["blocks"]
    belt_change_count = 0
    # 遍历每个方块条目
    for block in blocks:
        # 检查 nbt 中的 id 是否为 create:belt
        if "nbt" in block and block["nbt"] is not None:
            if "id" in block["nbt"] and block["nbt"]["id"].value == "create:belt":
                # 读取 Length 的值
                if "Length" in block["nbt"]:
                    length_value = block["nbt"]["Length"].value

                    # 如果 Length 大于 30，则替换为 20
                    if length_value > 30:
                        block["nbt"]["Length"] = nbt.TAG_Int(4)  # 修改 Length 值为 20
                        # print(length_value)
                        belt_change_count += 1
    # 保存修改后的 NBT 文件
    source_nbt.write_file(source_path_1)  # 替换为保存路径
    if belt_change_count == 0:
        return "未发现异常"
    else:
        return f"传送带异常调整结果：{belt_change_count}"



if __name__ == '__main__':
    source_path = 'warn/穆糖Official/传送带破区块蓝图.nbt'  # 替换为你的 NBT 文件路径
    print(belt_check(source_path))

