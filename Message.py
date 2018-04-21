import datetime
import hashlib
from transaction import Transaction


class TTMessage:  # 交易纪录简单实现
    def __init__(self, data):  # 初始化
        self.hash = None  # 自身hash
        self.prev_hash = None  # 上一个hash
        self.timestamp = datetime.datetime.now()  # 交易时间
        self.data = data  # 交易信息
        self.payload_hash = self.hash_payload()  # 交易数据和交易时间hash   #python 更多的风格是用下划线分隔单词

    def hash_payload(self):  # 对交易数据和时间进行hash
        return hashlib.sha256((str(self.timestamp) +
                               str(self.data)).encode("utf-8")).hexdigest()  # 取得数据的hash

    def hash_message(self):  # 对交易进行锁定,前一个hash+这次生成的hash再hash 一下
        return hashlib.sha256((str(self.prev_hash) +
                               str(self.payload_hash)).encode("utf-8")).hexdigest()

    def seal(self):  # 对前一个hash和这次生成的hash再hash 生成自身hash
        self.hash = self.hash_message()

    def validate(self):  # 数据验证
        if self.payload_hash != self.hash_payload():  # 判断是否有人修改了交易数据和交易时间
            raise InvalidMessage("交易数据或者交易时间修改了！！！" + str(self))  # 打印哪个节点哪个交易
        if self.hash != self.hash_message():  # 判断前后hash连接是否被修改了
            raise InvalidMessage("交易的hash连接被修改" + str(self))
        return  "数据正常"+str(self)

    def __repr__(self):  # 返回对象的基本信息
        mystr = "hash:{},prev_hash:{},data:{}".format(self.hash, self.prev_hash, self.data)
        return mystr

    def link(self, preMessage):  # 跟前一个message 连接起来
        self.prev_hash = preMessage.hash  # 链接


class InvalidMessage(Exception):  # 异常类
    def __init__(self, *args, **kwargs):
        Exception.__init__(self, *args, **kwargs)


if __name__ == "__main__":
    # 交易记录
    try:
        t1 = Transaction("taotao", "xjj2", 12)
        t2 = Transaction("taotao", "xjj3", 123)
        t3 = Transaction("taotao", "xjj4", 12.23)
        t4 = Transaction("taotao", "xjj5", 123.23)

        m1 = TTMessage(t1)
        m2 = TTMessage(t2)
        m3 = TTMessage(t3)
        m4 = TTMessage(t4)

        # 数据密封,密封密封之后再link
        #生成自身hash
        m1.seal()
        m2.link(m1)
        #生成自身hash
        m2.seal()
        m3.link(m2)
        # 生成自身hash
        m3.seal()
        m4.link(m3)
        # 生成自身hash
        m4.seal()

        # 篡改数据
       # m2.data = "你妹的直播平台"
       # m2.hash = "mmmm的直播平台"

        print(m1)
        print(m2)
        print(m3)
        print(m4)

        # 验证
        m1.validate()
        m2.validate()
        m3.validate()
        m4.validate()
    except InvalidMessage as e:
        print(e)
