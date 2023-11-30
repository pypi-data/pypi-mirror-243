import cv2
import platform

# 获取当前操作系统
current_os = platform.system()

if current_os == "Windows":
    save_path = "D:/copy.png"
else:  # 默认为Ubuntu或其他Linux发行版
    save_path = "/home/username/copy.png"
cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)  # 打开笔记本内置摄像头
while cap.isOpened():  # 笔记本内置摄像头被打开后
    ret, frame = cap.read()  # 从摄像头中实时读取视频
    cv2.imshow("Video", frame)  # 在窗口中显示视频
    k = cv2.waitKey(1)  # 图像的刷新时间为1毫秒
    if k == ord(' '):  # 按下空格键
        cv2.imshow('img', frame)  # 显示按下空格键时摄像头视频中的图像
        cv2.imwrite(save_path, frame)  # 保存按下空格键时摄像头视频中的图像
        cap.release()  # 关闭笔记本内置摄像头
        cv2.destroyWindow("Video")  # 销毁名为Video的窗口
        break
cv2.destroyAllWindows()  # 销毁显示图像的窗口
