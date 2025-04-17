from Checker import para
## 基础配置
schematics_path = para.path  # 蓝图路径
log_path = r'logs/application.log'
check_frequency = 1  # 针对文件的扫描频率 单位为秒（扫描文件名）
schematics_packet_size = 1024  # 蓝图的上传默认包大小默认为1024（用于外置脚本识别是否传输完成） 位于 create>server>Schematics 配置下


## 蓝图全局黑名单
# 此功能会使用文本匹配以实现最快速的清除，对于不满足规则的隐藏nbt有奇效（老东西真能藏）
fast_handle = False  # 对于找到的禁用方块是否快速清除，建议开启

tags_to_check = ["AttributeModifiers", "Enchantments"]
block_to_check = ["create:creative_crate", "create:creative_fluid_tank", "create:creative_motor", "create:motor",'create:blaze_burner',
                  "create:lectern_controller","supplementaries:urn",'minecraft:kelp',"minecraft:shulker_box","minecraft:tripwire_hook"]



# "create:clipboard",


