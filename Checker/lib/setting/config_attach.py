import copy
from Checker.lib.setting.config_interface import import_toml, export_toml, info_comment, format_toml


def merge_config(exist, standard):
    merged = copy.deepcopy(exist)

    def recursive_merge(e, s):
        for key, value in s.items():
            if key not in e:
                e[key] = value
            else:
                # 如果是字典，递归处理
                if isinstance(value, dict) and isinstance(e[key], dict):
                    recursive_merge(e[key], value)
                # 如果是数组，合并缺失项
                elif isinstance(value, list) and isinstance(e[key], list):
                    for item in value:
                        if item not in e[key]:
                            e[key].append(item)
                # 如果是标量，保留 exist 的值，不覆盖
                else:
                    pass  # 可以根据需要决定是否覆盖

    recursive_merge(merged, standard)
    return merged


def update_config(exist, standard):
    # result = 'result.toml'
    exist_config = import_toml(exist)
    standard_config = import_toml(standard)

    merged_config = merge_config(exist_config, standard_config)
    export_toml(merged_config, exist)
    format_toml(exist)
    info_comment(exist)



if __name__ == '__main__':

    update_config('2.toml', 'config.toml')