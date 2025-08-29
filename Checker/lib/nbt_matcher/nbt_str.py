from Checker.lib.log_color import log
from Checker.lib.setting.config import kill_entity, ban_entity


def str_check(data, interest, tags, blocks):
    count_to_clear = 0
    have_entity = False

    datas_str = str(data.pretty_tree())  # 将 NBT 数据转换为字符串
    item_count = 0

    if kill_entity:
        if str(data.get('entities')) == '[]':
            pass
        else:
            data['entities'].clear()
            # datas_str = str(data.pretty_tree())
            log.info("提示: 根据规则清理了实体参数。")
            have_entity = True
    else:
        for entity in ban_entity:
            if entity in datas_str:
                count_to_clear += datas_str.count(entity)

                log.warning(f"警告: 找到禁止 ID 实体, 包含{entity}")

    block_count = 0
    palette_count = 0
    all_to_clear = 0
    block_data = data['blocks']
    palette_data = data['palette']


    for data_item in block_data:
        block_count += 1
        data_str = str(data_item.pretty_tree())
        if data_item.get('nbt') is not None:
            block_id = str(data_item['nbt'].get('id'))
        else:
            block_id = None
        for tag in tags:
            if tag in data_str:
                if tag == "Enchantments":
                    if data_str.count("Enchantments") == data_str.count("StoredEnchantments"):
                        continue
                log.error(f"警告: 在第[{block_count}]个方块 id [{block_id}]找到异常 NBT 标签, 包含{tag}")
                return -1, all_to_clear, data, have_entity
        for item in blocks:
            if item in data_str:
                count_to_clear = data_str.count(item)
                if item == "minecraft:kelp":
                    count_to_clear -= data_str.count('minecraft:kelp_plant')
                if count_to_clear > 0:
                    all_to_clear += count_to_clear
                    log.warning(f"警告: 在第[{block_count}]个方块 id [{block_id}]找到禁止 ID 物品, 包含{item}")


        for index in interest:
            if index in data_str:
                item_count += 1


    for palette in palette_data:
        palette_count += 1
        block_id = str(palette.get('Name'))
        if block_id in blocks:
            log.warning(f"警告: 在第[{palette_count}]个着色器方块 id [{block_id}]找到禁止 ID 物品, 包含{block_id}")
            all_to_clear += 1
        if block_id in interest:
            item_count += 1


    if all_to_clear > 0:
        # log.info("写入nbt中。。")
        pass
        # data = nbt.NBTFile
    if item_count != 0:
        log.info(f"信息: 总共找到了{item_count}个需要检查的物品!")
    return item_count, all_to_clear, data, have_entity

