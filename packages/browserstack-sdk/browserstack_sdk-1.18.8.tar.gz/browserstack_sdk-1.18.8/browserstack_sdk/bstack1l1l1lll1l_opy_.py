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
import os
class RobotHandler():
    def __init__(self, args, logger, bstack1l111ll1ll_opy_, bstack1l111llll1_opy_):
        self.args = args
        self.logger = logger
        self.bstack1l111ll1ll_opy_ = bstack1l111ll1ll_opy_
        self.bstack1l111llll1_opy_ = bstack1l111llll1_opy_
    @staticmethod
    def version():
        import robot
        return robot.__version__
    @staticmethod
    def bstack1l1l1l1lll_opy_(bstack1l111ll111_opy_):
        bstack1l111ll1l1_opy_ = []
        if bstack1l111ll111_opy_:
            tokens = str(os.path.basename(bstack1l111ll111_opy_)).split(bstack11l1l1l_opy_ (u"ࠤࡢࠦෑ"))
            camelcase_name = bstack11l1l1l_opy_ (u"ࠥࠤࠧි").join(t.title() for t in tokens)
            suite_name, bstack1l111l1lll_opy_ = os.path.splitext(camelcase_name)
            bstack1l111ll1l1_opy_.append(suite_name)
        return bstack1l111ll1l1_opy_
    @staticmethod
    def bstack1l111ll11l_opy_(typename):
        if bstack11l1l1l_opy_ (u"ࠦࡆࡹࡳࡦࡴࡷ࡭ࡴࡴࠢී") in typename:
            return bstack11l1l1l_opy_ (u"ࠧࡇࡳࡴࡧࡵࡸ࡮ࡵ࡮ࡆࡴࡵࡳࡷࠨු")
        return bstack11l1l1l_opy_ (u"ࠨࡕ࡯ࡪࡤࡲࡩࡲࡥࡥࡇࡵࡶࡴࡸࠢ෕")