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
import os
class RobotHandler():
    def __init__(self, args, logger, bstack1l111ll1ll_opy_, bstack1l111lllll_opy_):
        self.args = args
        self.logger = logger
        self.bstack1l111ll1ll_opy_ = bstack1l111ll1ll_opy_
        self.bstack1l111lllll_opy_ = bstack1l111lllll_opy_
    @staticmethod
    def version():
        import robot
        return robot.__version__
    @staticmethod
    def bstack1l11l1ll1l_opy_(bstack1l111l1l1l_opy_):
        bstack1l111l11ll_opy_ = []
        if bstack1l111l1l1l_opy_:
            tokens = str(os.path.basename(bstack1l111l1l1l_opy_)).split(bstack11l1ll_opy_ (u"ࠤࡢࠦ඼"))
            camelcase_name = bstack11l1ll_opy_ (u"ࠥࠤࠧල").join(t.title() for t in tokens)
            suite_name, bstack1l111l1ll1_opy_ = os.path.splitext(camelcase_name)
            bstack1l111l11ll_opy_.append(suite_name)
        return bstack1l111l11ll_opy_
    @staticmethod
    def bstack1l111l1l11_opy_(typename):
        if bstack11l1ll_opy_ (u"ࠦࡆࡹࡳࡦࡴࡷ࡭ࡴࡴࠢ඾") in typename:
            return bstack11l1ll_opy_ (u"ࠧࡇࡳࡴࡧࡵࡸ࡮ࡵ࡮ࡆࡴࡵࡳࡷࠨ඿")
        return bstack11l1ll_opy_ (u"ࠨࡕ࡯ࡪࡤࡲࡩࡲࡥࡥࡇࡵࡶࡴࡸࠢව")