import os
import shutil
from datetime import datetime

from PIL import Image
from PIL.ExifTags import TAGS


def 获取照片拍摄时间(photo_path):
    """优先从 EXIF 获取拍摄时间，失败则返回 None"""
    try:
        image = Image.open(photo_path)
        exif_data = image._getexif()
        if not exif_data:
            return None
        for tag, value in exif_data.items():
            tag_name = TAGS.get(tag, tag)
            if tag_name == "DateTimeOriginal":
                return datetime.strptime(value, "%Y:%m:%d %H:%M:%S")
    except Exception as e:
        print(f"[EXIF失败] {photo_path} → {e}")
    return None


def 获取文件创建时间(file_path):
    """返回文件创建时间（Linux 上可能是最后更改时间）"""
    try:
        timestamp = os.path.getctime(file_path)
        return datetime.fromtimestamp(timestamp)
    except Exception as e:
        print(f"[创建时间失败] {file_path} → {e}")
        return None


def 按时间分类照片_递归(source_dir, target_dir):
    if not os.path.exists(target_dir):
        os.makedirs(target_dir)

    支持扩展名 = {".jpg", ".jpeg", ".png", ".heic", ".JPG", ".JPEG", ".PNG"}

    for root, _, files in os.walk(source_dir):
        for filename in files:
            _, ext = os.path.splitext(filename)
            if ext.lower() not in 支持扩展名:
                continue

            文件路径 = os.path.join(root, filename)
            拍摄时间 = 获取照片拍摄时间(文件路径)
            if not 拍摄时间:
                拍摄时间 = 获取文件创建时间(文件路径)

            if 拍摄时间:
                子文件夹名 = 拍摄时间.strftime("%Y-%m")
            else:
                子文件夹名 = "未知时间"

            目标文件夹 = os.path.join(target_dir, 子文件夹名)
            os.makedirs(目标文件夹, exist_ok=True)

            目标路径 = os.path.join(目标文件夹, filename)

            # 防止重名覆盖
            if os.path.exists(目标路径):
                base, ext = os.path.splitext(filename)
                i = 1
                while os.path.exists(目标路径):
                    新文件名 = f"{base}_{i}{ext}"
                    目标路径 = os.path.join(目标文件夹, 新文件名)
                    i += 1

            # shutil.move(文件路径, 目标路径)
            # print(f"✅ 已移动: {文件路径} → {目标路径}")

            shutil.copy2(文件路径, 目标路径)
            print(f"✅ 已复制: {文件路径} → {目标路径}")


# 示例用法
source_folder = "D:/OneDrive/Pictures"
target_folder = "D:/def/sp-"


按时间分类照片_递归(source_folder, target_folder)
