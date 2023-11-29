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
class bstack11lll111l_opy_:
    def __init__(self, handler):
        self._111l1l11ll_opy_ = None
        self.handler = handler
        self._111l1l11l1_opy_ = self.bstack111l1l111l_opy_()
        self.patch()
    def patch(self):
        self._111l1l11ll_opy_ = self._111l1l11l1_opy_.execute
        self._111l1l11l1_opy_.execute = self.bstack111l1l1111_opy_()
    def bstack111l1l1111_opy_(self):
        def execute(this, driver_command, *args, **kwargs):
            response = self._111l1l11ll_opy_(this, driver_command, *args, **kwargs)
            self.handler(driver_command, response)
            return response
        return execute
    def reset(self):
        self._111l1l11l1_opy_.execute = self._111l1l11ll_opy_
    @staticmethod
    def bstack111l1l111l_opy_():
        from selenium.webdriver.remote.webdriver import WebDriver
        return WebDriver