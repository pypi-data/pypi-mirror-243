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
import sys
class bstack1l11ll1lll_opy_:
    def __init__(self, handler):
        self._11lllll11l_opy_ = sys.stdout.write
        self._11llll1ll1_opy_ = sys.stderr.write
        self.handler = handler
        self._started = False
    def start(self):
        if self._started:
            return
        self._started = True
        sys.stdout.write = self.bstack11lllll111_opy_
        sys.stdout.error = self.bstack11llll1lll_opy_
    def bstack11lllll111_opy_(self, _str):
        self._11lllll11l_opy_(_str)
        if self.handler:
            self.handler({bstack11l1ll_opy_ (u"ࠫࡱ࡫ࡶࡦ࡮ࠪ๘"): bstack11l1ll_opy_ (u"ࠬࡏࡎࡇࡑࠪ๙"), bstack11l1ll_opy_ (u"࠭࡭ࡦࡵࡶࡥ࡬࡫ࠧ๚"): _str})
    def bstack11llll1lll_opy_(self, _str):
        self._11llll1ll1_opy_(_str)
        if self.handler:
            self.handler({bstack11l1ll_opy_ (u"ࠧ࡭ࡧࡹࡩࡱ࠭๛"): bstack11l1ll_opy_ (u"ࠨࡇࡕࡖࡔࡘࠧ๜"), bstack11l1ll_opy_ (u"ࠩࡰࡩࡸࡹࡡࡨࡧࠪ๝"): _str})
    def reset(self):
        if not self._started:
            return
        self._started = False
        sys.stdout.write = self._11lllll11l_opy_
        sys.stderr.write = self._11llll1ll1_opy_