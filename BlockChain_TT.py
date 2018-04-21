from Block_TT import *


class TTBlockChain:  # 区块链
    def __init__(self):  # 初始化
        self.blockList = []  # 装载所有的区块

    def add_block(self, block):  # 增加区块
        if len(self.blockList) > 0:
            block.prev_hash = self.blockList[-1].hash
        block.seal()  # 密封 就是产生hash
        block.validate()  # 校验
        self.blockList.append(block)

    def validate(self):  # 校验
        for i, block in enumerate(self.blockList):
            try:
                block.validate()
            except InvalidBlock as ib:
                raise InvalidBlockCoin("区块校验错误,区块索引{}".format(i))

    def __repr__(self):
        return "TT_BlockCoin:{}".format(len(self.blockList))  # 获取区块长度


class InvalidBlockCoin:  # 区块链异常
    def __init__(self, *args, **kwargs):
        Exception.__init__(self, *args, **kwargs)


if __name__ == '__main__':
    try:
        t1 = Transaction("taotao", "xjj1", 12)
        t2 = Transaction("taotao", "xjj2", 123)
        t3 = Transaction("taotao", "xjj3", 12.23)
        t4 = Transaction("taotao", "xjj4", 123.23)
        t5 = Transaction("taotao", "xjj5", 155.23)
        t6 = Transaction("taotao", "xjj6", 66.23)

        m1 = TTMessage(t1)
        m2 = TTMessage(t2)
        m3 = TTMessage(t3)
        m4 = TTMessage(t4)
        m5 = TTMessage(t5)
        m6 = TTMessage(t6)

        yin1 = Block(m1, m2)
        yin1.seal()  # 工作量的矿工有打包交易的权利，一个区块可以有多个交易
        yin2 = Block(m1, m2)
        yin2.seal()
        yin3 = Block(m1, m2)
        yin3.seal()

        # 篡改整个区块链
        yin3.messageList.append(m1)

        myTTBlockChain = TTBlockChain()  # 区块链
        myTTBlockChain.add_block(yin1)
        myTTBlockChain.add_block(yin2)
        myTTBlockChain.add_block(yin3)
        myTTBlockChain.validate()
        print(myTTBlockChain)
    except Exception as e:
        print(e)
