## 基础配置
schematics_path = r'C:\Users\123\PycharmProjects\CreateSchematicsChecker-Python\schematics\kongyu\uploaded'  # 蓝图路径

log_path = r'logs/application.log'  # 日志路径

check_frequency = 0.5  # 针对文件的扫描频率 单位为秒（扫描文件名性能开销非常小）

schematics_packet_size = 1024  # 蓝图的上传默认包大小默认为1024（用于外置脚本识别是否传输完成） 位于 create>server>Schematics 配置下


## 蓝图全局黑名单
# 此功能会使用文本匹配以实现最快速的清除，对于不满足规则的隐藏nbt有奇效（老东西真能藏）
fast_handle = True  # 对于找到的禁用方块是否快速清除，建议开启
count_block = False  # 统计方块信息（这会些许拖慢检查速度）

ban_tags = ["AttributeModifiers", "Enchantments"]
ban_block = ["create:creative_crate", "create:creative_fluid_tank", "create:creative_motor",
             "create:creative_blaze_cake","create:handheld_worldshaper",
             "minecraft:command_block",
             "minecraft:kelp" # 这可以阻止动态结构放置含水方块，从而阻止绝大部分gt刷石机（因为它们非常非常卡）
             ]
kill_entity = True  # 是否清理蓝图的实体（这可以阻止所有的创造实体和实体的所有潜在复制漏洞，但会导致创造模式打印的蓝图不再包含实体）
ban_entity = ['minecraft:armor_stand']
# "create:clipboard",
