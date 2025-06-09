import subprocess

import rarfile

# 测试用例
rar_file = "def.rar"
password = "141592"
密码位数 = 6


# 设定rar路径和密码
def 尝试解压(密码字符串) -> bool:
    try:
        rarfile.RarFile(rar_file).extractall(path="./o", pwd=密码字符串)
        return True
    except Exception:
        return False


def check_rar_password_unrar(rar_path, password):
    try:
        result = subprocess.run(
            ["unrar", "t", "-p" + password, rar_path], stdout=subprocess.PIPE, stderr=subprocess.PIPE, timeout=10
        )
        # unrar 返回0表示成功
        return result.returncode == 0
    except Exception as e:
        print(f"错误: {e}")
        return False


# 调用函数
if __name__ == "__main__":
    # res = 尝试解压(password)
    # print(res)

    count = 0
    while not 尝试解压(str(count).zfill(密码位数)):

        if count % 100 == 0:
            print(f"尝试密码到: {str(count).zfill(密码位数)}")

        count += 1

    print(f"密码是: {str(count).zfill(密码位数)}")
