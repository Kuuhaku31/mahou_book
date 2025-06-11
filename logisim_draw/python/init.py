import sys

from helps import 打印帮助信息


# 启动类，用于解析命令行参数并检查模式是否有效
class 启动:
    def __init__(self):
        self.模式: str = ""
        self.目标: str = ""
        self.源: str = ""
        self.circuit名称: str = ""
        self.是否删除原先的像素信息: bool = False

    def 解析参数(self, args: list):
        i = 0
        while i < len(args):
            if args[i] == "-m" and i + 1 < len(args):
                self.模式 = args[i + 1]
                i += 2
            elif args[i] == "-t" and i + 1 < len(args):
                self.目标 = args[i + 1]
                i += 2
            elif args[i] == "-s" and i + 1 < len(args):
                self.源 = args[i + 1]
                i += 2
            elif args[i] == "-l" and i + 1 < len(args):
                self.circuit名称 = args[i + 1]
                i += 2
            elif args[i] == "-rm_current":
                self.是否删除原先的像素信息 = True
                i += 1
            elif args[i] in ("-h", "--help"):
                打印帮助信息()
                sys.exit(0)
            else:
                i += 1

    # 检查模式是否有效
    # 如果模式不合法，打印错误信息并返回 "False"
    # 如果合法，返回模式名称
    def 是否可以启动模式(self) -> str:

        if self.模式 == "del":
            if not self.目标 or not self.circuit名称:
                print("删除模式启动失败: 请提供 -t 和 -l 参数")
                return "False"
            else:
                return self.模式
        elif self.模式 == "add":
            if not self.目标 or not self.circuit名称 or not self.源:
                print("添加模式启动失败: 请提供 -t、-s 和 -l 参数")
                return "False"
            else:
                return self.模式
        elif self.模式 == "conv":
            if not self.目标 or not self.源 or not self.circuit名称:
                print("转换模式启动失败: 请提供 -t、-s 和 -l 参数")
                return "False"
            else:
                return self.模式
        elif self.模式 == "load":
            if not self.目标 or not self.源 or not self.circuit名称:
                print("加载模式启动失败: 请提供 -t、-s 和 -l 参数")
                return "False"
            else:
                return self.模式
        elif self.模式 == "store":
            if not self.目标 or not self.源 or not self.circuit名称:
                print("存储模式启动失败: 请提供 -t、-s 和 -l 参数")
                return "False"
            else:
                return self.模式
        elif self.模式 == "去图":
            if not self.目标 or not self.源:
                print("去图模式启动失败: 请提供 -t 和 -s 参数")
                return "False"
            else:
                return self.模式
        elif self.模式 == "":
            print("未指定模式，请使用 -m 参数指定")
            return "False"
        else:
            print(f"未知模式: {self.模式}")
            return "False"
