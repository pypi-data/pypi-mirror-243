# -*- coding: utf-8 -*-
# @Time    : 2023/11/28 21:13:50
# @Author  : ZMF
# @FileName: help.py
# @Software: PyCharm
# @IDE: PyCharm
# @E-Mail: ZZMF20110806@163.com
message = '''
你好, 欢迎使用STD PYTHON, 我是作者ZMF, 以下是包的使用教程:
Hello, welcome to use STD PYTHON! I'm ZMF, here is the guide:
    0.功能 Function
        你可以通过这一个包来导入所有Python自带的包
        You can import all Python built-in packages through this package
    1.导入包 Import this package
        from stdpython import *
    2.使用包 Use this package
        from stdpython import *
        a = random.randint(0, 1)
        time.sleep(1)
        print(a)
    3.帮助文档 Get this document
        from stdpython import *
        help.help()
    4.包相关信息 Information about this package
        from stdpython import *
        # 作者 Author
        information.author
        # 版本 Version
        information.version
        # 包名称 Package Name
        information.pack_name
        # 帮助文档文件名 Help-file's Name
        information.help_file
        # 包文件列表 File List
        information.files
'''

def help() -> object:
    '''

    :return: help message
    '''
    return print(message)

if __name__ == '__main__':
    print(message)