import subprocess
import sys
import time

logo = r"""
--------------------------------------------------------------------------------------------------------------
 __   __   ___      ___  ___     __             ___  __   __         ___     __        ___  __        ___  __  
/  ` |__) |__   /\   |  |__     |__) |    |  | |__  |__) |__) | |\ |  |     /  ` |__| |__  /  ` |__/ |__  |__) 
\__, |  \ |___ /~~\  |  |___    |__) |___ \__/ |___ |    |  \ | | \|  |     \__, |  | |___ \__, |  \ |___ |  \ 
--------------------------------------------------------------------------------------------------------------

版本：{version}  问题/反馈/寻求帮助  QQ群号: 1061133894
"""


def handle_package():
    def install(package):  # fix package problem
        subprocess.check_call([sys.executable, '-m', 'pip', 'install', package])

    # 包名与导入名的映射
    package_mapping = {
        'colorlog': 'colorlog',
        'nbt': 'nbt',
        'requests': 'requests',
        'dotenv': 'python-dotenv',
        'yaml': 'pyyaml',  # 注意这里的 'yaml' 是 PyYAML 的导入名
        'cryptography': 'cryptography',
        'pydantic': 'pydantic'
    }

    for import_name, package_name in package_mapping.items():
        try:
            __import__(import_name)
        except ImportError:
            print(f"发现包缺失，安装中 {package_name}...")
            install(package_name)

    from Checker.lib.log_color import log
    log.info("环境检测正常")
    log.info(f"{logo}")
    # log.info(f"3秒后开始运行。。。。")
    time.sleep(0.5)
