# Logisim Draw

import os
import re
import sys

from PIL import Image
from tqdm import tqdm

# <a>
#   <circuit name="test">
#       <appear>
#           <rect fill="#ff4d75" height="1" stroke="none" width="1" x="60" y="100"/>
#           <rect fill="#ff4d75" height="1" stroke="none" width="1" x="70" y="100"/>
#           <rect fill="#ff4d75" height="1" stroke="none" width="1" x="80" y="110"/>
#           ...
#           <rect fill="#ffffff" height="65" stroke="#000000" stroke-width="2" width="88" x="90" y="112"/>
#           <circ-port height="8" pin="140,210" width="8" x="46" y="66"/>
#           <circ-anchor facing="east" height="6" width="6" x="77" y="57"/>
#       </appear>
#   </circuit>
# </a>


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


# 将像素信息保存到 HTML 文件
# 第一行保存 circuit标签名称
# 第二行保存像素信息
def 保存像素信息到html文件(输出文件地址: str, 像素信息: str, circuit标签名称: str) -> None:

    # 确保输出目录存在
    os.makedirs(os.path.dirname(输出文件地址), exist_ok=True)

    # 写入文件
    with open(输出文件地址, "w", encoding="utf-8") as f:
        f.write(circuit标签名称)
        f.write("\n")
        f.write(像素信息)
    print(f"像素信息已保存到 {输出文件地址}")


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


# 从指定的 HTML 文件加载像素信息到目标 circ 文件
def 添加新像素_从html文件(目标circ文件地址: str, 源html文件地址: str, 是否删除原先的像素信息: bool) -> None:

    # 读取源HTML文件内容
    with open(源html文件地址, "r", encoding="utf-8") as f:
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


def 打印帮助():
    help_text = """
格式: python main.py -m <模式> -t <目标circ文件地址> -p <待加载图像地址> -l <目标标签名称>

### 参数

| 参数        | 功能                      |
| ----------- | ------------------------- |
| -m          | 指定模式                  |
| -t          | 指定目标文件地址          |
| -s          | 指定源文件地址            |
| -l          | 指定目标 circuit 标签名称 |
| -p          | 指定待加载图像地址        |
| -h --help   | 打印帮助                  |
| -rm_current | 是否删除原先的像素信息    |

### 模式

| 模式 | 功能                                           | 此模式下有效参数                                                            |
| ---- | ---------------------------------------------- | --------------------------------------------------------------------------- |
| del  | 删除指定目标 circuit 标签下的所有像素          | -t <circ 文件地址> -l <circuit 标签名称>                                    |
| add  | 将图片添加到目标 circ 文件                     | -t <circ 文件地址> -p <待加载图像地址> -l <circuit 标签名称> -rm_current    |
| conv | 将图片转换为像素信息                           | -t <保存像素信息的 html 文件地址> -p <待加载图像地址> -l <circuit 标签名称> |
| load | 从指定的 html 文件加载像素信息到目标 circ 文件 | -t <circ 文件地址> -s <待加载像素信息的 html 文件地址> -rm_current          |

"""

    print(help_text)


# main
if __name__ == "__main__":

    # 参数解析
    模式: str = ""
    目标文件地址: str = ""
    源文件地址: str = ""
    目标circuit名称: str = ""
    待加载图像地址: str = ""
    是否删除原先的像素信息: bool = False

    # 遍历参数列表，确定模式
    args = sys.argv[1:]
    i = 0
    while i < len(args):
        if args[i] == "-m" and i + 1 < len(args):
            模式 = args[i + 1]
            i += 2
        elif args[i] == "-t" and i + 1 < len(args):
            目标文件地址 = args[i + 1]
            i += 2
        elif args[i] == "-s" and i + 1 < len(args):
            源文件地址 = args[i + 1]
            i += 2
        elif args[i] == "-l" and i + 1 < len(args):
            目标circuit名称 = args[i + 1]
            i += 2
        elif args[i] == "-p" and i + 1 < len(args):
            待加载图像地址 = args[i + 1]
            i += 2
        elif args[i] == "-rm_current":
            是否删除原先的像素信息 = True
            i += 1
        elif args[i] in ("-h", "--help"):
            打印帮助()
            sys.exit(0)

        else:
            i += 1

    # 主逻辑
    if not 模式:
        print("缺少参数: -m")
        打印帮助()
        sys.exit(1)

    if 模式 == "del":
        if not 目标文件地址 or not 目标circuit名称:
            print("缺少参数: -t 或 -l")
            打印帮助()
            sys.exit(1)
        清除原有像素(目标文件地址, 目标circuit名称)

    elif 模式 == "add":
        if not 目标文件地址 or not 目标circuit名称 or not 待加载图像地址:
            print("缺少参数: -t、-l 或 -p")
            打印帮助()
            sys.exit(1)

        if 是否删除原先的像素信息:
            清除原有像素(目标文件地址, 目标circuit名称)

        像素信息 = 解析图像文件(待加载图像地址, 50, 40)  # 这里dx, dy可根据需要调整
        添加新像素(目标文件地址, 目标circuit名称, 像素信息)

    elif 模式 == "conv":
        if not 目标文件地址 or not 待加载图像地址 or not 目标circuit名称:
            print("缺少参数: -t、-p 或 -l")
            打印帮助()
            sys.exit(1)

        像素信息 = 解析图像文件(待加载图像地址, 50, 40)
        保存像素信息到html文件(目标文件地址, 像素信息, 目标circuit名称)

    elif 模式 == "load":
        if not 目标文件地址 or not 源文件地址:
            print("缺少参数: -t 或 -s")
            打印帮助()
            sys.exit(1)

        添加新像素_从html文件(目标文件地址, 源文件地址, 是否删除原先的像素信息)

    else:
        print(f"未知模式: {模式}")
        打印帮助()
        sys.exit(1)
