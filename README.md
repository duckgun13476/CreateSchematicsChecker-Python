# CreateSchematicsChecker-Python

## A simple python script for checking Minecraft mod Create to check cheating Schematics

---

~~玩bug蓝图的熊孩子的对策杀手（bushi~~



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


# 使用方法

1. **下载脚本的 ZIP 文件**
    - 点击release下载脚本的最新 ZIP 文件。

2. **解压缩 ZIP 文件**
    - 找到下载的 ZIP 文件，右键点击并选择“解压缩”或使用解压缩软件进行解压。

3. **下载 Python 解释器**
    - 这里有两种情况可以选择：
    - 1.使用Microsoft直接安装
      - 在脚本根目录Shift+右键打开命令窗口，输入python，弹出安装
      - 直接在微软商店搜索python
    
    - 2.前往 [Python 官方网站](https://www.python.org/downloads/) 下载适合你操作系统的 Python 解释器。
   
4. **安装 Python**
    - 按照安装向导的指示完成 Python 的安装。

5. **修改 `start.bat` 文件（如果使用微软商店安装不需要执行此步）**
    - 如果在官网下载，则需要将开头的python3指定为python.exe的绝对路径
    - 找到解压缩后的文件夹，打开 `start.bat` 文件。
    - 将文件中的 `python3` 修改为 Python 的绝对路径。
    - 安装并找到python.exe后，查看属性可以得到例如下面的绝对路径：
      ```
      C:\Python39\python.exe
      ```
6. **配置config**
    - 使用编辑器编辑config文件
    - 根据自己需求设置检查蓝图的路径，要精确到/upload，例如：
      ```
      C:\abc\bcd\MC\schematic\upload
      ```
    - 根据服务器设置配置上传的包大小
      - 默认值为1024
    - 设置蓝图白名单黑名单
      - 默认配置已经添加了会造成异常的所有方块 
7. **启动脚本**
    - 双击 `start.bat` 文件以启动脚本。
8. **自定义规则和其他内容**
    - 日志文件在 `log` 文件夹内，每次上传的蓝图都保存在`save`文件夹下。
    - 规则文件一般情况下不需要改变，如果需要，则需要满足下列的设置：
    - 规则配置demo如下，可以根据自己需求适当配置：
      ```
      - name: 机械动力：弹射置物台
          block: create:weighted_ejector
          Univariate:
            blocks.nbt.HorizontalDistance: [1,32]
            blocks.nbt.Powered: [0,1]
      - name: 机械动力：剪贴板
          block: create:clipboard
          Redundant:
            blocks.nbt.Item.tag: BlockEntityTag
      ```
    - `Univariate`  为单变量，针对蓝图的特定路径检测，如果不在范围内，则会调整至上下限
    - `Redundant`  为针对一个位置是否有此标签的检查，如果发现了此标签，将会直接删除蓝图，并存进异常蓝图文件夹
   


## 致谢
特别感谢 crackun24 提供的部分代码，以及他在项目中提供的帮助。


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



