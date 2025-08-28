# CSC 机械动力：蓝图检查

---

### ~~玩bug蓝图的熊孩子的对策杀手（bushi~~



![python](https://github.com/user-attachments/assets/eb746af3-f0f4-4710-86b4-a4ad7f176369)


---
## 概述
这是一个基于机械动力的蓝图检查脚本，使用 Python 运行。该脚本外置，不占用服务器性能，并允许自定义规则。它能够自动筛查蓝图文件夹下的所有 bug 与异常蓝图，防止任何恶意篡改 NBT 的蓝图流入 Minecraft 服务器。

## 功能
- **自动筛查**：自动检查蓝图文件夹下的所有蓝图，识别并过滤出潜在的 bug 与异常蓝图，确保服务器安全。
- **高度自定义规则**：允许用户自定义规则，以针对特定模组实现特殊的 NBT 扫描。
- **基于 MD5 的加速处理**：通过 MD5 校验加速处理，显著提高 Python 的运行速度。
- **传送带篡改校验**：使用全校验算法对 0.5.1 和 6.0.0 版本的传送带进行校验，阻止传送带蓝图的 bug 与复制、卡服、崩服特性。
- **齿轮传动轮配对校验**：在 6.0.0 版本后，基于简单匹配逻辑进行齿轮传动轮的配对校验，防止已知蓝图 bug 与复制特性。
- **多种恶意 NBT 筛查**：针对多种恶意 NBT 篡改值进行筛查，确保蓝图的安全性。
- **自动云端同步**：自动更新 NBT 检查规则，让恶意新出的bug蓝图无处可逃。
- **自动更新规则**：已实现自动更新规则功能，确保规则始终保持最新状态。

---

## 使用方法：
#### 根据您的操作系统选择合适的版本↓

### windows：
 - 下载 `blue_core31_for_windows.exe` （版本可能会变化） 。
 - 下载完毕后直接点击运行。
 - 运行后，会在本地生成config.toml，按照需求填入参数，然后重新打开即可！

### linux：
 - 下载 `blue_core31_for_linux` （版本可能会变化） 。
 - 下载到任何目录后。您需要赋予文件的执行权限（注意版本可能会变化，不要直接复制粘贴）
   ```
   chmod +x blue_core31_for_linux
      ```
 - 输入 `./blue_core31_for_linux`（版本可能会变化）启动。
 - 运行后，会在本地生成config.toml，按照需求填入参数，然后重新打开即可！

---
## 重要：您必须配置几个关键参数来保证CSC 的可以运行！因为它们是极其关键的参数！

1. 使用任意编辑器编辑`config.toml`文件, 它生成在程序的根目录。
2. 您必须按照服务器的目录和参数来配置两个参数 `schematics_path` 和 `schematics_packet_size` 如果不配置正确会导致无法运行！
3. `schematics_path` 是蓝图的本地存放路径，必须精确到 `/upload`。
   - 如果您的windows路径是 `C:\Users\123\experiment\schematics\uploaded` 那么你需要填入 `C://Users//123//experiment//schematics//uploaded` 这是因为toml配置文件的格式要求！
   - 如果您的linux路径是 `experiment/schematics/uploaded` 直接填入即可，linux不会有路径问题。
4. `schematics_packet_size` 是蓝图的上传包大小，用于脚本检测蓝图是否完整上传，必须与服务器一致！！
   - 这个数值的默认值为`1024`
   - 配置图形化界面在`create>server>Schematics` 本地toml 直接搜索 `maxSchematicPacketSize` 即可

5. **自定义规则和其他内容**
    - 日志文件在 `log` 文件夹内，每次上传的蓝图都保存在`save`文件夹下。
    - 规则文件一般情况下不需要改变，如果需要，则您只需要按照需求填入即可：
   ```toml
   # 核心配置
   [check]
   # 检查频率 默认为0.5秒
   check_frequency = 0.5
   # 是否自动清理被禁止的方块
   fast_handle = false
   # 是否统计蓝图内方块信息，会占用一定性能，但可以可视化
   count_block = false
   # 是否剔除蓝图内的全部实体，这会导致创造打印蓝图不包含实体，但是可以杜绝全部实体相关的复制漏洞
   kill_entity = true
   # 禁止的实体，填入后将会剔除蓝图内的此实体
   ban_entity = [
   "minecraft:armor_stand"
   ]
   # 禁止的tag，由于nbt的递归隐藏机制，如果填入的tag在蓝图内检测到，就会将蓝图清空，因为nbt数据结构无法针对tag剔除进行修复
   ban_tags = [
   "AttributeModifiers",
   "Enchantments",  # 附魔标签，这会阻止创造蓝图，但也会导致蓝图不能带有附魔特性，因为它们的结构相同
   "using_converts_to",  # 食物标签，阻止返回复制特性
   "bundle_contents"  # 存储袋标签，阻止复制特性
   ]
   # 禁止的方块，填入后将会剔除蓝图内的此类方块，如果剔除不完全，则会清空蓝图
   ban_block = [
   "create:creative_crate",
   "create:creative_fluid_tank",
   "create:creative_motor",
   "create:creative_blaze_cake",
   "create:handheld_worldshaper",
   "minecraft:command_block",  # 不多说了，这玩意是命令方块
   "minecraft:kelp"  # 这可以阻止绝大多数gt机，他们极其卡顿！
   ]
   
   # 实验功能，可以在发现异常蓝图后推送smtp邮箱，免费又好用，还能利用免费的推送服务！
   [smtp]
   # 是否启用，true 或 false
   enable = false
   # 接收报警的邮箱，所有报警信息都会发送到这个邮箱！
   email_receive = "example@qq.com"
   # smtp的默认根服务器，一般情况不需要改
   smtp_server = "smtp.qq.com"
   # smtp的默认服务器端口，一般情况不需要改
   smtp_port = 587
   # 使用哪个邮箱进行发送，报警信息会从这个邮箱发出
   smtp_sender_email = "<EMAIL>"
   # 这个邮箱的smtp密码，需要在qq邮箱网页版获取
   smtp_password = "<PASSWORD>"
   ```



---
其他：
如果您想要使用源码运行，那么就需要本地有解释器并按照下列步骤：

 **下载 Python 解释器**
   - 这里有两种情况可以选择：
   - 1.使用Microsoft直接安装
      - 在脚本根目录Shift+右键打开命令窗口，输入python，弹出安装
      - 直接在微软商店搜索python

   - 2.前往 [Python 官方网站](https://www.python.org/downloads/) 下载适合你操作系统的 Python 解释器。

**安装 Python**
   - 按照安装向导的指示完成 Python 的安装。


   


## 致谢
 - 特别感谢 crackun24 
   - 提供的部分代码，以及他在项目中提供的帮助。
 - 特别感谢  HTony03
   - 是这个项目的第一个贡献者，修复了一些代码潜在漏洞。
 - 特别致谢：
   - 起飞的玫瑰、恐鱼、air、crackun24、runner、CTR服主 等总计14个机械动力公益服服主，它们为这个脚本提供了检查样本和后续辅助处理。
---
 - 特别特别致谢 B站 up主 一只不屑的屑蜘蛛 
   - **如果不是这 sb 熊孩子故意用蓝图崩了作者开的公益服好几次、在不知道多少服传bug蓝图破坏服务器、在作者在b站发修复时给作者拉黑、还在b站造谣诋毁作者，也不会有这个项目，蓝图bug也不会这么快有不错的解决方案！**


## 依赖
- Minecraft
- Create

---
## 关于模组支持
相关模组正在逐步开发中，相比于模组：
### 优点：
- 脚本不区别版本，规则更新快，规则筛查更细致，检出率更高。
### 缺点：
- 解释型语言，运行速度慢，需要python解释器

---
## 更新日志
### 2025/4/1
- 默认添加清理实体功能，将默认清理蓝图内的所有实体，因为机械动力不具备任何实体检测，所以这是一个机械动力永远无法修复的创造物品蓝图获取bug

### 2025/8/13
- 默认添加 food组件的食用返回检查，防止利用此特性复制物品。
- 默认添加 机械手nbt清理，自动清理机械手的异常nbt
- 默认添加 bundle_contents组件，防止利用烧毁返回异常nbt。
- 默认启用SHA-256 替代MD5 在小文件的检查，防止潜在安全问题。

### 2025/8/28
- 添加smtp  推送提示
- 添加对机械动力：伪装板模组的 bug 检出
- 添加无法处理的蓝图上传功能，用于后续维护。
- 打包脚本，现在CSC只需要点击启动、不再需要任何外置环境配置！