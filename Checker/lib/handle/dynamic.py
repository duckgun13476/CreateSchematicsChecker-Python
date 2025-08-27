from RestrictedPython import compile_restricted
from RestrictedPython.PrintCollector import PrintCollector

# 使用 PrintCollector 来捕获输出
_print_ = PrintCollector()

# 定义一个沙箱环境
sandbox_globals = {
    '_print_': _print_,
}
def foo():
    return None

print(foo())
# 用户代码字符串
code_string = """
import sys
def foo():
    global debug_inner
    debug_inner = 'bar'
    return 24
sys.exit(1)
result = foo()
"""
print(foo())
# 编译受限制的代码
compiled_code = compile_restricted(code_string, '<string>', 'exec')
print(foo())
# 执行受限制的代码
exec(compiled_code, sandbox_globals)
print(foo())
# 从沙箱环境中获取结果
result = sandbox_globals.get('result', None)
print(foo())
# 输出结果
print(str(_print_))  # 捕获的输出
print(result)        # 应该输出: 24
print(sandbox_globals.get('debug_inner'))  # 应该输出: 'bar'
