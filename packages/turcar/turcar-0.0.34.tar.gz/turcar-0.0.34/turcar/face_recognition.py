from urllib.request import urlopen

import pymysql
import threading
import json
import time
import hashlib
import base64
import requests
import urllib

# 摄像头配置
url = 'http://192.168.0.200:80/'
img = ''
bts = bytes()
is_exit = False
CAMERA_BUFFER_SIZE = 4096

# MySQL 配置
mysql_host = '180.76.235.69'
mysql_user = 'root'
mysql_password = ' a!Y)iiBTF3.t'
mysql_database = 'face-recognition'
charset = 'utf8mb4'

# 百度智能云bos
bos_host = "https://bj.bcebos.com"
access_key_id = "1ee18128a39d4b69881c222bce50e8f6"
secret_access_key = "ee6e8cfb4b5b45ee8136f7ce43eb32a3"
bucket_name = 'yinhang-prod'
# 百度智能云人脸识别
API_KEY = "bo0Tfin2s2Lc3DUVQW3DzOPb"
SECRET_KEY = "DbF0dvfAOW9aLG5Izi1EI3RsVprBwuXp"


def save_image_to_bos3(data, content_length, content_md5):
    pass
    # # 创建BceClientConfiguration
    # config = BceClientConfiguration(credentials=BceCredentials(access_key_id, secret_access_key), endpoint=bos_host)
    # # 创建 BOS 客户端配置
    # client = BosClient(config)
    # # 指定存储路径
    # file_key = "yubo/" + str(int(time.time())) + ".jpg"
    # # print(f"bucket_name:{bucket_name}\ncontent_length:{content_length}\naccess_key_id:{access_key_id}\ndata:{data}\ncontent_md5:{content_md5}")
    # client.put_object(bucket_name, file_key, data, content_length, content_md5)
    #
    # # 返回文件在 BOS 中的完整路径
    # return f"https://{bucket_name}.bj.bcebos.com/{file_key}"


def save_image_path_to_mysql(image_path):
    db_host = mysql_host
    db_user = mysql_user
    db_password = mysql_password
    db_name = mysql_database

    conn = pymysql.connect(host=db_host, user=db_user, password=db_password, database=db_name)
    cursor = conn.cursor()
    sql = "INSERT INTO t_picture(picture_path) VALUES (%s)"
    print(sql)
    cursor.execute(sql, image_path)
    conn.commit()

    cursor.close()
    conn.close()


# 人脸识别
def faceReco(image):
    url = "https://aip.baidubce.com/rest/2.0/face/v3/detect?access_token=" + get_access_token()

    # image 可以通过 get_file_content_as_base64("C:\fakepath\多人二维码.jpg",False) 方法获取
    payload = json.dumps({
        "image": image,
        "image_type": "BASE64"
    })
    headers = {
        'Content-Type': 'application/json'
    }
    response = requests.request("POST", url, headers=headers, data=payload)
    print("照片识别结果：" + response.text)
    return response


def get_file_content_as_base64(path, urlencoded=False):
    """
    获取文件base64编码
    :param path: 文件路径
    :param urlencoded: 是否对结果进行urlencoded
    :return: base64编码信息
    """
    with open(path, "rb") as f:
        content = base64.b64encode(f.read()).decode("utf8")
        if urlencoded:
            content = urllib.parse.quote_plus(content)
    return content


def get_access_token():
    """
    使用 AK，SK 生成鉴权签名（Access Token）
    :return: access_token，或是None(如果错误)
    """
    url = "https://aip.baidubce.com/oauth/2.0/token"
    params = {"grant_type": "client_credentials", "client_id": API_KEY, "client_secret": SECRET_KEY}
    return str(requests.post(url, params=params).json().get("access_token"))


def read_ip_camera():
    global url
    url = 'http://192.168.0.200:80/'
    global img
    global bts
    global is_exit

    count = 0
    last_capture_time = time.time()  # 记录上一次抓取照片的时间
    stream = urlopen(url)
    ts = b''
    img = None
    is_exit = False
    while True:
        if is_exit:
            break
        try:
            # 抓取照片的条件：满足一分钟时间间隔
            if time.time() - last_capture_time >= 3.0:
                bts += stream.read(CAMERA_BUFFER_SIZE)
                # JPEG 图像的起始和结束标记
                jpghead = bts.find(b'\xff\xd8')
                jpgend = bts.find(b'\xff\xd9')
                # 如果找到起始和结束标记，则提取 JPEG 图像的字节数据，
                # 并使用 cv2.imdecode() 函数解码为图像。
                # np.frombuffer(jpg, dtype=np.uint8) 将字节数据转换为 NumPy 数组。
                if jpghead > -1 and jpgend > -1:
                    print(f"图片数量{count}")
                    count += 1
                    jpg = bts[jpghead:jpgend + 2]
                    bts = bts[jpgend + 2:]
                    # 计算哈希值
                    md5_hash = hashlib.md5(jpg).digest()
                    content_md5 = base64.standard_b64encode(md5_hash)
                    # 将哈希值进行 base64 编码
                    content_utf8 = base64.b64encode(jpg).decode("utf8")
                    # content_utf8 = base64.standard_b64encode(md5_hash).decode('utf-8')
                    # 人脸识别，如果有人脸才保存照片
                    # face_num = faceReco(content_utf8).josn().get("result", {}).get("face_num")
                    response = faceReco(content_utf8)
                    if response is not None:
                        error_code = response.json().get("error_code")
                        print(error_code)
                        if error_code == 0:
                            image_path = save_image_to_bos3(jpg, len(jpg), content_md5)
                            print(image_path)
                            save_image_path_to_mysql(image_path)
                last_capture_time = time.time()  # 更新上一次抓取照片的时间
        except Exception as e:
            print("Error:" + str(e))
            bts = b''
            stream = urlopen(url)
            continue


if __name__ == '__main__':
    # print(get_access_token)
    t = threading.Thread(target=read_ip_camera)
    t.daemon = True
    t.start()

    count = 0
    while True:
        time.sleep(1)
        # count += 1
        # print(f"Processed {count} frames")
        # if count >= 10:
        #     is_exit = True
        #     break