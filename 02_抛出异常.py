# if .. raise
def divede(a, b):
    if b == 0:
        raise ValueError("除数不能为0")
    return a / b

result = divede(1, 0)
                        
# try .. except .. else .. finally
def divide(a, b):
    try: 
        return a / b
    except ZeroDivisionError:
        return "try除数不能为0"
    
result = divide(2, 0)
print(result)

# 异常类型
try:
    result = 1/2
except ZeroDivisionError as e:
    print(f"Connot divide by zero: {e}")
    
try:
    lst = [1,2,3]
    print(lst[5])
except IndexError as e:
    print(f"Index error:{e}")
    
# 以下是常用的 Python 异常类型及其对应的描述汇总：
# TimeoutError - 超时错误
# ZeroDivisionError - 除零错误
# ValueError - 值错误
# TypeError - 类型错误
# KeyError - 键错误（字典中访问不存在的键）
# IndexError - 索引错误（列表或元组索引超出范围）
# AttributeError - 属性错误（访问对象中不存在的属性）
# FileNotFoundError - 文件未找到错误
# OSError - 操作系统错误（文件或目录访问错误）
# ImportError - 导入模块错误
# ModuleNotFoundError - 模块未找到错误（Python 3.6+）
# NameError - 变量未定义错误
# RuntimeError - 运行时错误
# RecursionError - 递归错误（递归深度超过最大限制）
# OverflowError - 数值运算结果溢出错误
# ArithmeticError - 算术运算错误（基类，包含除零、溢出等错误）
# IOError - 输入输出错误（Python 3 已合并到 OSError）
# MemoryError - 内存不足错误
# NotImplementedError - 方法未实现错误
# SyntaxError - 语法错误
# IndentationError - 缩进错误
# EOFError - 输入流到达文件末尾错误