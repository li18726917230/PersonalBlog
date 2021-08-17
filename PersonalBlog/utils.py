import datetime
from PersonalBlog.settings import BASE_DIR
import os


def Image_save(file, dir_path):  # 第一个参数图片对象，第二个参数图片存放的路径
    if str(file).split('.')[-1] in ['jpg', 'jpeg', 'png', 'gif', 'bmp', 'webp']:
        strftime = datetime.datetime.now().strftime("%Y-%m-%d")
        dir_path = str(BASE_DIR) + '\\media\\images\\' + dir_path + '\\' + strftime
        print(dir_path)
        isExists = os.path.exists(dir_path)
        if not isExists:  # 判断当前目录是否存在 strftime 目录
            os.makedirs(dir_path)
        file_path = dir_path + "/" + str(file)
        with open(file_path, 'wb+') as f:
            f.write(file.read())
        return strftime
    return 'failure'
