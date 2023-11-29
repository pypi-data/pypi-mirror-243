# coding: UTF-8
import sys
bstack11111l_opy_ = sys.version_info [0] == 2
bstack1lllll_opy_ = 2048
bstack1l11l_opy_ = 7
def bstack11l1l1l_opy_ (bstack1111lll_opy_):
    global bstack1lll1l1_opy_
    bstack1111111_opy_ = ord (bstack1111lll_opy_ [-1])
    bstack111_opy_ = bstack1111lll_opy_ [:-1]
    bstack11l11l1_opy_ = bstack1111111_opy_ % len (bstack111_opy_)
    bstack11l1lll_opy_ = bstack111_opy_ [:bstack11l11l1_opy_] + bstack111_opy_ [bstack11l11l1_opy_:]
    if bstack11111l_opy_:
        bstack111ll1_opy_ = unicode () .join ([unichr (ord (char) - bstack1lllll_opy_ - (bstack1l11l1_opy_ + bstack1111111_opy_) % bstack1l11l_opy_) for bstack1l11l1_opy_, char in enumerate (bstack11l1lll_opy_)])
    else:
        bstack111ll1_opy_ = str () .join ([chr (ord (char) - bstack1lllll_opy_ - (bstack1l11l1_opy_ + bstack1111111_opy_) % bstack1l11l_opy_) for bstack1l11l1_opy_, char in enumerate (bstack11l1lll_opy_)])
    return eval (bstack111ll1_opy_)
import threading
bstack111l1l1ll1_opy_ = 1000
bstack111l1l1l11_opy_ = 5
bstack111l1l1l1l_opy_ = 30
bstack111l1lll11_opy_ = 2
class bstack111l1lll1l_opy_:
    def __init__(self, handler, bstack111l1ll111_opy_=bstack111l1l1ll1_opy_, bstack111l1llll1_opy_=bstack111l1l1l11_opy_):
        self.queue = []
        self.handler = handler
        self.bstack111l1ll111_opy_ = bstack111l1ll111_opy_
        self.bstack111l1llll1_opy_ = bstack111l1llll1_opy_
        self.lock = threading.Lock()
        self.timer = None
    def start(self):
        if not self.timer:
            self.bstack111l1ll1ll_opy_()
    def bstack111l1ll1ll_opy_(self):
        self.timer = threading.Timer(self.bstack111l1llll1_opy_, self.bstack111l1lllll_opy_)
        self.timer.start()
    def bstack111l1l1lll_opy_(self):
        self.timer.cancel()
    def bstack111l1ll1l1_opy_(self):
        self.bstack111l1l1lll_opy_()
        self.bstack111l1ll1ll_opy_()
    def add(self, event):
        with self.lock:
            self.queue.append(event)
            if len(self.queue) >= self.bstack111l1ll111_opy_:
                t = threading.Thread(target=self.bstack111l1lllll_opy_)
                t.start()
                self.bstack111l1ll1l1_opy_()
    def bstack111l1lllll_opy_(self):
        if len(self.queue) <= 0:
            return
        data = self.queue[:self.bstack111l1ll111_opy_]
        del self.queue[:self.bstack111l1ll111_opy_]
        self.handler(data)
    def shutdown(self):
        self.bstack111l1l1lll_opy_()
        while len(self.queue) > 0:
            self.bstack111l1lllll_opy_()