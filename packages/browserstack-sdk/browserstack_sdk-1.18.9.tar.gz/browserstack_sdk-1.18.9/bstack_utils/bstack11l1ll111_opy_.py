# coding: UTF-8
import sys
bstack1lllll1_opy_ = sys.version_info [0] == 2
bstack1111l1l_opy_ = 2048
bstack11l1l11_opy_ = 7
def bstack11l1ll_opy_ (bstack11l1l1l_opy_):
    global bstack1ll1l1_opy_
    bstack1llll1l_opy_ = ord (bstack11l1l1l_opy_ [-1])
    bstack1ll1_opy_ = bstack11l1l1l_opy_ [:-1]
    bstack11111l_opy_ = bstack1llll1l_opy_ % len (bstack1ll1_opy_)
    bstack111l11_opy_ = bstack1ll1_opy_ [:bstack11111l_opy_] + bstack1ll1_opy_ [bstack11111l_opy_:]
    if bstack1lllll1_opy_:
        bstack1l1ll1_opy_ = unicode () .join ([unichr (ord (char) - bstack1111l1l_opy_ - (bstack1llllll1_opy_ + bstack1llll1l_opy_) % bstack11l1l11_opy_) for bstack1llllll1_opy_, char in enumerate (bstack111l11_opy_)])
    else:
        bstack1l1ll1_opy_ = str () .join ([chr (ord (char) - bstack1111l1l_opy_ - (bstack1llllll1_opy_ + bstack1llll1l_opy_) % bstack11l1l11_opy_) for bstack1llllll1_opy_, char in enumerate (bstack111l11_opy_)])
    return eval (bstack1l1ll1_opy_)
class bstack1l1l111l_opy_:
    def __init__(self, handler):
        self._111l11ll1l_opy_ = None
        self.handler = handler
        self._111l11lll1_opy_ = self.bstack111l1l1111_opy_()
        self.patch()
    def patch(self):
        self._111l11ll1l_opy_ = self._111l11lll1_opy_.execute
        self._111l11lll1_opy_.execute = self.bstack111l11llll_opy_()
    def bstack111l11llll_opy_(self):
        def execute(this, driver_command, *args, **kwargs):
            response = self._111l11ll1l_opy_(this, driver_command, *args, **kwargs)
            self.handler(driver_command, response)
            return response
        return execute
    def reset(self):
        self._111l11lll1_opy_.execute = self._111l11ll1l_opy_
    @staticmethod
    def bstack111l1l1111_opy_():
        from selenium.webdriver.remote.webdriver import WebDriver
        return WebDriver