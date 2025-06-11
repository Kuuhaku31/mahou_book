# Logisim Draw

import os
import re
import sys

from helps import 打印帮助信息, 打印模式启动失败信息
from PIL import Image
from tqdm import tqdm


# 返回一个字符串，保存解析出的像素信息
def 解析图像文件(图片地址: str, dx: int, dy: int) -> str:

    image = Image.open(图片地址)  # 打开图像文件
    image = image.convert("RGB")  # 确保图像是RGB模式
    宽, 高 = image.size  # 获取图像的宽和高

    pixels = list(image.getdata())  # 获取所有像素信息（返回值是一个二维列表或迭代器）
    pixels_2d = [pixels[i * 宽 : (i + 1) * 宽] for i in range(高)]  # 重新组织成二维形式（按行排列）

    像素信息: str = ""
    for y in tqdm(range(高), desc="处理图像行数"):  # 遍历每个像素点，添加进度条
        for x in range(宽):

            r, g, b = pixels_2d[y][x]  # 获取当前像素的颜色
            color = (r << 16) | (g << 8) | b  # 将RGB颜色转换为16进制整数
            hex_color = f"#{color:06x}"  # 将颜色转换为16进制字符串

            # 添加到输出结果中
            像素信息 += f'<rect fill="{hex_color}" height="1" stroke="none" width="1" x="{x+dx}" y="{y+dy}"/>\n'

    return 像素信息


# 确认目标 HTML 文件是否存在，不会创建文件
# 如果文件存在，返回 文件地址，否则返回 空字符串
def 确认目标html文件存在(像素库的文件夹路径: str, 目标circuit名称: str) -> str:
    文件地址 = os.path.join(像素库的文件夹路径, f"{目标circuit名称}.html")
    return 文件地址 if os.path.exists(文件地址) and 文件地址.endswith(".html") else ""


# 确保目标 HTML 文件存在，如果不存在则创建，并返回文件地址
def 确保目标html文件存在(像素库的文件夹路径: str, 目标circuit名称: str) -> str:
    # 确保输出目录存在
    if not os.path.exists(像素库的文件夹路径):
        os.makedirs(像素库的文件夹路径)

    # 确保文件夹路径存在
    if not os.path.isdir(像素库的文件夹路径):
        print(f"错误: {像素库的文件夹路径} 不是一个有效的文件夹路径")
        return ""

    # 确保文件地址是一个有效的 HTML 文件路径
    文件地址 = os.path.join(像素库的文件夹路径, f"{目标circuit名称}.html")
    if not 文件地址.endswith(".html"):
        print(f"错误: {文件地址} 不是一个有效的 HTML 文件路径")
        return ""

    # 如果文件不存在，则创建一个空文件
    if not os.path.exists(文件地址):
        with open(文件地址, "w", encoding="utf-8") as f:
            f.write("")

    return 文件地址


# 将像素信息保存到 HTML 文件
# 第一行保存 circuit标签名称
# 第二行保存像素信息
def 保存像素信息到html文件(库文件夹路径: str, 像素信息: str, circuit标签名称: str) -> None:

    # 确保输出目录存在
    文件地址 = 确保目标html文件存在(库文件夹路径, circuit标签名称)
    if not 文件地址:
        return

    # 写入文件
    with open(文件地址, "w", encoding="utf-8") as f:
        f.write(circuit标签名称)
        f.write("\n")
        f.write(像素信息)
    print(f"像素信息已保存到 {文件地址}")


# 函数逻辑：
# 遍历 <appear> 标签下的所有标签
# 仅删除 height="1" 且 width="1" 的 <rect> 标签
def 清除原有像素(目标circ文件地址: str, 目标circuit名称: str) -> None:
    with open(目标circ文件地址, "r", encoding="utf-8") as f:
        html_content = f.read()

    # 找到指定circuit下的<appear>...</appear>
    pattern = rf'(<circuit\s+name="{re.escape(目标circuit名称)}"[^>]*>.*?<appear>)(.*?)(</appear>)'
    match = re.search(pattern, html_content, flags=re.DOTALL)
    if not match:
        print("未找到指定circuit或appear标签")
        return

    appear_content = match.group(2)

    # 删除 height="1" 且 width="1" 的 <rect> 标签
    appear_content = re.sub(r'<rect[^>]*height="1"[^>]*width="1"[^>]*\/>', "", appear_content)

    # 替换 appear 内容
    new_html = re.sub(pattern, rf"\1\n{appear_content}\3", html_content, flags=re.DOTALL)

    with open(目标circ文件地址, "w", encoding="utf-8") as f:
        f.write(new_html)


# 添加新像素到指定的circuit标签下的<appear>标签中
def 添加新像素(目标circ文件地址: str, 目标circuit名称: str, 新内容: str) -> None:
    with open(目标circ文件地址, "r", encoding="utf-8") as f:
        html_content = f.read()

    # 找到指定circuit下的<appear>...</appear>
    pattern = rf'(<circuit\s+name="{re.escape(目标circuit名称)}"[^>]*>.*?<appear>)(.*?)(</appear>)'
    match = re.search(pattern, html_content, flags=re.DOTALL)
    if not match:
        print("未找到指定circuit或appear标签")
        return

    appear_content = match.group(2)

    # 在 appear_content 中添加新内容
    appear_content += 新内容

    # 替换 appear 内容
    new_html = re.sub(pattern, rf"\1\n{appear_content}\3", html_content, flags=re.DOTALL)

    with open(目标circ文件地址, "w", encoding="utf-8") as f:
        f.write(new_html)


# 获取指定 circ 文件中指定 circuit 标签下的像素信息
def 获取像素信息(目标circ文件地址: str, 目标circuit名称: str) -> str:
    with open(目标circ文件地址, "r", encoding="utf-8") as f:
        html_content = f.read()

    # 找到指定circuit下的<appear>...</appear>
    pattern = rf'(<circuit\s+name="{re.escape(目标circuit名称)}"[^>]*>.*?<appear>)(.*?)(</appear>)'
    match = re.search(pattern, html_content, flags=re.DOTALL)
    if not match:
        print(f"未找到指定circuit: {目标circuit名称} 或 appear 标签")
        return ""

    return match.group(2)  # 返回 appear 标签中的内容


# 从指定的 HTML 文件加载像素信息到目标 circ 文件
def 添加像素信息_从库_到circ文件(
    目标circ文件地址: str,
    目标circuit名称: str,
    像素库的文件夹路径: str,
    是否删除原先的像素信息: bool,
) -> None:

    # 确认目标 circ 文件存在
    文件地址 = 确认目标html文件存在(像素库的文件夹路径, 目标circuit名称)
    if not 文件地址:
        print(f"错误: {像素库的文件夹路径} 中未找到 {目标circuit名称}.html 文件")
        return

    # 读取 HTML 文件内容
    with open(文件地址, "r", encoding="utf-8") as f:
        html_content = f.read()

    # 第一行是circuit标签名称
    lines = html_content.splitlines()
    if not lines or len(lines) < 2:
        print("源HTML文件格式错误，至少需要两行")
        return

    源circuit名称 = lines[0].strip()  # 第一行是circuit标签名称
    新内容 = "\n".join(lines[1:])  # 剩余行是像素信息

    # 如果需要删除原有像素信息
    if 是否删除原先的像素信息:
        清除原有像素(目标circ文件地址, 源circuit名称)

    添加新像素(目标circ文件地址, 源circuit名称, 新内容)

    print(f"已从 {文件地址} 加载像素信息到 {目标circ文件地址} 的 {目标circuit名称} 标签下")

    if 是否删除原先的像素信息:
        print(f"并且已删除 {目标circ文件地址} 中 {目标circuit名称} 标签下的原有像素信息")


# 将指定 circ 文件的指定 circuit 标签下的像素信息存储到指定的 HTML 文件中
def 添加像素信息_从circ文件_到库(
    目标circ文件地址: str,
    目标circuit名称: str,
    像素库的文件夹路径: str,
) -> None:

    # 读取目标 circ 文件的目标 circuit 下的像素信息
    像素信息: str = 获取像素信息(目标circ文件地址, 目标circuit名称)
    if not 像素信息:
        return

    # 确保输出目录存在
    文件地址 = 确保目标html文件存在(像素库的文件夹路径, 目标circuit名称)
    if not 文件地址:
        return

    # 写入文件
    # 会覆盖掉原有的同名文件
    with open(文件地址, "w", encoding="utf-8") as f:
        f.write(目标circuit名称)
        f.write("\n")
        f.write(像素信息)

    print(f"已将 {目标circuit名称} 标签下的像素信息存储到 {文件地址}")


class 启动参数处理:
    def __init__(self):
        self.模式: str = ""
        self.目标文件地址: str = ""
        self.源文件地址: str = ""
        self.目标circuit名称: str = ""
        self.是否删除原先的像素信息: bool = False

    def 解析参数(self, args: list):
        i = 0
        while i < len(args):
            if args[i] == "-m" and i + 1 < len(args):
                self.模式 = args[i + 1]
                i += 2
            elif args[i] == "-t" and i + 1 < len(args):
                self.目标文件地址 = args[i + 1]
                i += 2
            elif args[i] == "-s" and i + 1 < len(args):
                self.源文件地址 = args[i + 1]
                i += 2
            elif args[i] == "-l" and i + 1 < len(args):
                self.目标circuit名称 = args[i + 1]
                i += 2
            elif args[i] == "-rm_current":
                self.是否删除原先的像素信息 = True
                i += 1
            elif args[i] in ("-h", "--help"):
                打印帮助信息()
                sys.exit(0)
            else:
                i += 1


# main
if __name__ == "__main__":

    参数 = 启动参数处理()
    参数.解析参数(sys.argv[1:])

    # 主逻辑
    if not 参数.模式:
        打印模式启动失败信息(参数.模式)
        sys.exit(1)

    if 参数.模式 == "del":
        if not 参数.目标文件地址 or not 参数.目标circuit名称:
            打印模式启动失败信息(参数.模式)
            sys.exit(1)

        清除原有像素(参数.目标文件地址, 参数.目标circuit名称)

    elif 参数.模式 == "add":
        if not 参数.目标文件地址 or not 参数.目标circuit名称 or not 参数.源文件地址:
            打印模式启动失败信息(参数.模式)
            sys.exit(1)

        if 参数.是否删除原先的像素信息:
            清除原有像素(参数.目标文件地址, 参数.目标circuit名称)

        像素信息 = 解析图像文件(参数.源文件地址, 50, 40)  # 这里dx, dy可根据需要调整
        添加新像素(参数.目标文件地址, 参数.目标circuit名称, 像素信息)

    elif 参数.模式 == "conv":
        if not 参数.目标文件地址 or not 参数.源文件地址 or not 参数.目标circuit名称:
            打印模式启动失败信息(参数.模式)
            sys.exit(1)

        像素信息 = 解析图像文件(参数.源文件地址, 50, 40)
        保存像素信息到html文件(参数.目标文件地址, 像素信息, 参数.目标circuit名称)

    elif 参数.模式 == "load":
        if not 参数.目标文件地址 or not 参数.源文件地址 or not 参数.目标circuit名称:
            打印模式启动失败信息(参数.模式)
            sys.exit(1)

        添加像素信息_从库_到circ文件(
            参数.目标文件地址,
            参数.目标circuit名称,
            参数.源文件地址,
            参数.是否删除原先的像素信息,
        )

    elif 参数.模式 == "store":
        if not 参数.目标文件地址 or not 参数.源文件地址 or not 参数.目标circuit名称:
            打印模式启动失败信息(参数.模式)
            sys.exit(1)

        添加像素信息_从circ文件_到库(
            参数.源文件地址,
            参数.目标circuit名称,
            参数.目标文件地址,
        )

    else:
        打印模式启动失败信息(参数.模式)
        sys.exit(1)
