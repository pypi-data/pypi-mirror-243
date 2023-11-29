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
import sys
class bstack1l1ll1111l_opy_:
    def __init__(self, handler):
        self._11llllll1l_opy_ = sys.stdout.write
        self._11llllll11_opy_ = sys.stderr.write
        self.handler = handler
        self._started = False
    def start(self):
        if self._started:
            return
        self._started = True
        sys.stdout.write = self.bstack11lllll1l1_opy_
        sys.stdout.error = self.bstack11lllll1ll_opy_
    def bstack11lllll1l1_opy_(self, _str):
        self._11llllll1l_opy_(_str)
        if self.handler:
            self.handler({bstack11l1l1l_opy_ (u"ࠫࡱ࡫ࡶࡦ࡮ࠪ๭"): bstack11l1l1l_opy_ (u"ࠬࡏࡎࡇࡑࠪ๮"), bstack11l1l1l_opy_ (u"࠭࡭ࡦࡵࡶࡥ࡬࡫ࠧ๯"): _str})
    def bstack11lllll1ll_opy_(self, _str):
        self._11llllll11_opy_(_str)
        if self.handler:
            self.handler({bstack11l1l1l_opy_ (u"ࠧ࡭ࡧࡹࡩࡱ࠭๰"): bstack11l1l1l_opy_ (u"ࠨࡇࡕࡖࡔࡘࠧ๱"), bstack11l1l1l_opy_ (u"ࠩࡰࡩࡸࡹࡡࡨࡧࠪ๲"): _str})
    def reset(self):
        if not self._started:
            return
        self._started = False
        sys.stdout.write = self._11llllll1l_opy_
        sys.stderr.write = self._11llllll11_opy_