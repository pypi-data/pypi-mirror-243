import os
import re
import sys
import subprocess
import requests
import tkinter as tk
from tkinter import messagebox


class CheackUpdates:
    def __init__(self):
        self.os_type = sys.platform
        self.root = tk.Tk()
        self.url = f"https://pypi.org/pypi/turcar/json"

    def is_windows(self):
        return self.os_type.startswith('win')

    def is_linux(self):
        return self.os_type.startswith('linux')

    def is_mac(self):
        return self.os_type.startswith('darwin')

    # 检查版本
    def cheack_version(self):
        response = requests.get(self.url)
        if response.status_code == 200:
            data = response.json()
            # 获取项目最新版本
            version = data["info"]["version"]
            # 获取当前脚本所在目录
            current_dir = os.path.dirname(os.path.abspath(__file__))
            # 指定要获取内容的文件名
            file_name = "VERSION"
            # 拼接文件路径
            file_path = os.path.join(current_dir, file_name)
            # 空校验
            if os.path.exists(file_path):
                # 打开文件并读取内容
                with open(file_path, 'r') as file:
                    content = file.read()
                    # print(f"File: {file_name}")
                    print(f"VERSION: {content}")
                    if version != content:
                        # 创建一个确认更新的弹窗
                        root = self.root
                        root.withdraw()  # 隐藏主窗口
                        result = messagebox.askokcancel("确认更新", "发现新版本，是否更新？")
                        if result:
                            # 处理更新脚本中的版本号
                            update_bash("turcar-update.bash", version)
                            # 执行更新脚本
                            # bash_command = '/turcar-update.bash'
                            # execute_bash_command(bash_command)
                            # 更新成功后本地版本号更新
                            with open(file_name, 'w') as wr_file:
                                wr_file.write(version)
                            print("更新成功")
                        else:
                            print("取消更新")
                        # root.destroy()

            return version
        else:
            return None


# 更新脚本中的版本号
def update_bash(filename, new_version):
    """
    更新脚本中的版本号

    Args:
        filename: 要更新的脚本文件名
        new_version: 新的版本号，格式为 x.x.x
    """
    # 使用正则表达式匹配并替换版本号
    with open(filename, 'r') as file:
        content = file.read()
        new_content = re.sub(r'(VERSION=)\d+\.\d+\.\d+', r'\g<1>' + new_version, content)

    # 将更新后的内容写回脚本文件
    with open(filename, 'w') as file:
        file.write(new_content)


# 执行 Bash 命令
def execute_bash_command(command):
    """
    执行 Bash 命令

    Args:
        command: 要执行的 Bash 命令
    """
    subprocess.run(command, shell=True)
