import datetime
import hashlib

from Message import TTMessage
from transaction import Transaction
from Message import InvalidMessage


class Block:
    def __init__(self, *args):
        self.messageList = []  # 存储多个交易记录
        self.timestamp = None  # 交易时间
        self.hash = None  # 自身hash
        self.prev_hash = None  # 上一块hash
        if args:
            for arg in args:
                self.add_message(arg)

    def add_message(self, message):  # 增加交易信息
        # 区分第一条和后面多条
        if len(self.messageList) > 0:
            message.link(self.messageList[-1])  # 取最后一个
        message.seal()
        message.validate()
        self.messageList.append(message)  # 追加记录
        pass

    def link(self, prev_block):  # 区块链连接
        self.prev_hash = prev_block.hash

    def seal(self):  # 密封
        self.timestamp = datetime.datetime.now()
        self.hash = self.hash_block()  # 密封当前hash

    def hash_block(self):
        return hashlib.sha256((str(self.prev_hash) +
                               str(self.timestamp) +
                               str(self.messageList[-1].hash)).encode("utf-8")).hexdigest()

    def validate(self):  # 校验
        for i, message in enumerate(self.messageList):  # 每个交易记录校验一下
            message.validate()  #每一条校验一下
            if i > 0 and message.prev_hash != self.messageList[i - 1].hash:
                raise InvalidBlock(("无效block,第{}条交易记录已经被修改".format(i) + str(self)))
        return str(self) + "数据ok"

    def __repr__(self):  # 类的对象描述
        return "money Boock =hash:{},prev_hash:{},len:{},time:{}". \
            format(self.hash, self.prev_hash, len(self.messageList), self.timestamp)


class InvalidBlock(Exception):
    def __init__(self, *args, **kwargs):
        Exception.__init__(self, *args, **kwargs)


if __name__ == "__main__":  # 只有在主模块的时候才执行
    try:
        t1 = Transaction("taotao", "xjj2", 12)
        t2 = Transaction("taotao", "xjj3", 123)
        t3 = Transaction("taotao", "xjj4", 12.23)
        t4 = Transaction("taotao", "xjj5", 123.23)

        m1 = TTMessage(t1)
        m2 = TTMessage(t2)
        m3 = TTMessage(t3)
        m4 = TTMessage(t4)

        yin = Block(m1, m2, m3, m4)  # 一次加入四条数据
        # seal 之后才会产生hash值
        yin.seal()

        m1.data = "2123"
        m2.hash = "13123"

        print(yin.validate())
    except InvalidMessage as e:  #消息被修改
        print(e)
    except InvalidBlock as e:    #区块被修改
        print(e)
