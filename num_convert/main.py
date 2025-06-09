# 进制转换程序
import sys


def convert_number(原始数字: str, 目标进制: int) -> str:

    原始进制 = 10  # 默认原始进制为十进制

    if 原始数字.startswith("0b"):
        原始进制 = 2
        原始数字 = 原始数字[2:]
    elif 原始数字.startswith("0o"):
        原始进制 = 8
        原始数字 = 原始数字[2:]
    elif 原始数字.startswith("0x"):
        原始进制 = 16
        原始数字 = 原始数字[2:]

    # 将原始数值转换为十进制整数
    try:
        decimal_number = int(原始数字, 原始进制)
    except ValueError:
        return "无效的输入，请检查数字和进制是否匹配。"

    # 将十进制转换为目标进制
    if 目标进制 == 2:
        return bin(decimal_number)
    elif 目标进制 == 8:
        return oct(decimal_number)
    elif 目标进制 == 10:
        return str(decimal_number)
    elif 目标进制 == 16:
        return hex(decimal_number).upper()  # 去掉 '0x' 并转大写
    else:
        return "目标进制不支持。"


# 示例交互
if __name__ == "__main__":

    # 获取启动参数
    if len(sys.argv) < 2:
        print("用法: python main.py <数字> <目标进制（默认十进制）>")
        print("目标进制: -b (二进制), -o (八进制), -d (十进制), -x (十六进制)")
        sys.exit(1)

    输入 = sys.argv[1]
    目标进制 = None

    # 解析目标进制
    if len(sys.argv) > 2:
        if sys.argv[2] == "-b":
            目标进制 = 2
        elif sys.argv[2] == "-o":
            目标进制 = 8
        elif sys.argv[2] == "-d":
            目标进制 = 10
        elif sys.argv[2] == "-x":
            目标进制 = 16

    if 目标进制 is None:
        目标进制 = 10  # 默认目标进制为十进制

    result = convert_number(输入, 目标进制)
    print(f"转换结果为：{result}")
