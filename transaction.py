import datetime


class Transaction:
    def __init__(self,
                 payer,
                 payee,
                 points):
        self.payer = payer
        self.payee = payee
        self.points = points
        self.timestamp = datetime.datetime.now()

    # 复写print
    def __repr__(self):
        return str(self.payer) + " pay " + str(self.payee) + " " + str(self.points) + " points at " + \
               str(self.timestamp)


t1 = Transaction("taotao", "xjj", 0.00001)
print(t1)
