import os
from nbt import nbt
from lib.sugar import timer

# 获取当前工作目录
current_directory = os.getcwd()

@timer
def run_tick():
    # 查找所有 NBT 文件
    for filename in os.listdir(current_directory):
        if filename.endswith('.nbt'):
            file_path = os.path.join(current_directory, filename)

            # 读取 NBT 文件
            nbt_data = nbt.NBTFile(file_path)

            # 遍历 blocks 列表
            for block in nbt_data['blocks']:
                nbt_compound = block['nbt']

                # 检查条件并修改
                if (nbt_compound['Length'].value > 30 and
                        nbt_compound['id'].value == 'create:belt'):
                    nbt_compound['Length'].value = 30
                    print(f"已修改文件: {filename} 中的 Length 为 30")

            # 保存修改后的 NBT 文件
            nbt_data.write_file(file_path)

            # 打印文件名和修改后的 NBT 数据
            print(f"文件: {filename}")
            print(nbt_data.pretty_tree())
            print("\n" + "=" * 40 + "\n")


run_tick()
