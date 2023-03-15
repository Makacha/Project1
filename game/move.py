

class Move:
    cur: (int, int)
    des: (int, int)
    type: int

    def __init__(self, cur: (int, int) = None, des: (int, int) = None, type: int = 0):
        self.cur = cur
        self.des = des
        self.type = type
