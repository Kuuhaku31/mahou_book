import sys

from helps import 打印帮助信息


# 启动类，用于解析命令行参数并检查模式是否有效
class 启动:
    def __init__(己):

        print("正在解析命令行参数...")

        # 初始化成员变量
        己.程序运行模式: str = None
        己.circ文件地址: str = None
        己.像素库的路径: str = None
        己.circ标签名称: str = None
        己.库的标签名称: str = None
        己.图片文件地址: str = None
        己.像素偏移向量: tuple[int, int] = None
        己.要删原先像素: bool = False

        # 解析命令行参数
        参数列表 = sys.argv[1:]
        索 = 0
        while 索 < len(参数列表):
            if 参数列表[索] == "-m" and 索 + 1 < len(参数列表):
                己.程序运行模式 = 参数列表[索 + 1]
                索 += 2

            elif 参数列表[索] == "-t" and 索 + 1 < len(参数列表):
                己.circ文件地址 = 参数列表[索 + 1]
                索 += 2

            elif 参数列表[索] == "-rep" and 索 + 1 < len(参数列表):
                己.像素库的路径 = 参数列表[索 + 1]
                索 += 2

            elif 参数列表[索] == "-lc" and 索 + 1 < len(参数列表):
                己.circ标签名称 = 参数列表[索 + 1]
                索 += 2

            elif 参数列表[索] == "-lr" and 索 + 1 < len(参数列表):
                己.库的标签名称 = 参数列表[索 + 1]
                索 += 2

            elif 参数列表[索] == "-p" and 索 + 1 < len(参数列表):
                己.图片文件地址 = 参数列表[索 + 1]
                索 += 2

            elif 参数列表[索] == "-pos" and 索 + 1 < len(参数列表):
                try:
                    pos_str = 参数列表[索 + 1]
                    己.像素偏移向量 = tuple(map(int, pos_str.split(",")))
                except ValueError:
                    己.像素偏移向量 = (0, 0)
                索 += 2

            elif 参数列表[索] == "-rm_cur":
                己.要删原先像素 = True
                索 += 1

            elif 参数列表[索] in ("-h", "--help"):
                打印帮助信息()
                sys.exit(0)

            else:
                print(f"未知参数: {参数列表[索]}")
                打印帮助信息()
                sys.exit(1)

        # 检查是否提供了必要的参数
        if 己.程序运行模式 == "del":
            if not 己.circ文件地址 or not 己.circ标签名称:
                print("del 模式启动失败，必须需提供的参数: -t -lc")
                己.程序运行模式 = None

        elif 己.程序运行模式 == "add":
            if not 己.circ文件地址 or not 己.circ标签名称 or not 己.图片文件地址:
                print("add 模式启动失败，必须需提供的参数: -t -lc -p")
                己.程序运行模式 = None

        elif 己.程序运行模式 == "conv":
            if not 己.circ文件地址 or not 己.像素库的路径 or not 己.circ标签名称:
                print("转换模式启动失败: 请提供 -t、-rep 和 -lc 参数")
                己.程序运行模式 = None

        elif 己.程序运行模式 == "load":
            if not 己.circ文件地址 or not 己.像素库的路径 or not 己.circ标签名称:
                print("加载模式启动失败: 请提供 -t、-rep 和 -lc 参数")
                己.程序运行模式 = None

        elif 己.程序运行模式 == "store":
            if not 己.circ文件地址 or not 己.像素库的路径 or not 己.circ标签名称 or not 己.库的标签名称:
                print("存储 模式启动失败，必须需提供的参数: -t -rep -lc -lr")
                己.程序运行模式 = None

        elif 己.程序运行模式 == "去图":
            # if not 己.circ文件地址 or not 己.源:
            #     print("去图模式启动失败: 请提供 -t 和 -s 参数")
            己.程序运行模式 = None

        elif 己.程序运行模式 == "":
            print("未指定模式，请使用 -m 参数指定")
            己.程序运行模式 = None

        else:
            print(f"未知模式: {己.程序运行模式}")
            己.程序运行模式 = None

        print("命令行参数解析完成")
        # 打印解析结果
        print(f"程序运行模式: {己.程序运行模式}")
        print(f"circ文件地址: {己.circ文件地址}")
        print(f"像素库的路径: {己.像素库的路径}")
        print(f"circ标签名称: {己.circ标签名称}")
        print(f"库的标签名称: {己.库的标签名称}")
        print(f"图片文件地址: {己.图片文件地址}")
        print(f"像素偏移向量: {己.像素偏移向量}")
        print(f"要删原先像素: {己.要删原先像素}")

        print("启动完成\n")
