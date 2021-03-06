# coding=utf-8
import hashlib

MY_SECRET = "PyTHoN3)JavaWMakY6C#Hn/VB9oXwQt8C++&Mysql/xJ89E="
# 定义私钥
def MD5(data):
    """
    :param data: 待加密数据
    :return:
    """
    my_md5 = hashlib.md5(bytes(MY_SECRET,encoding='utf-8'))
    my_md5.update(bytes(data,encoding='utf-8'))
    return my_md5.hexdigest()

def SHA256(data):
    my_sha256 = hashlib.sha256(bytes(MY_SECRET,encoding='utf-8'))
    my_sha256.update(bytes(data,encoding='utf-8'))
    return my_sha256.hexdigest()

if __name__ == "__main__":
    print(hashlib.md5(bytes("111111",encoding='utf-8')).hexdigest())
    print(MD5("111111"))
    print(SHA256("111111"))
    print(MD5("123456"))