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
import multiprocessing
import os
import json
from browserstack_sdk.bstack1ll1ll11ll_opy_ import *
from bstack_utils.config import Config
from bstack_utils.messages import bstack1lll11ll1l_opy_
class bstack1lll11ll11_opy_:
    def __init__(self, args, logger, bstack1l111ll1ll_opy_, bstack1l111lllll_opy_):
        self.args = args
        self.logger = logger
        self.bstack1l111ll1ll_opy_ = bstack1l111ll1ll_opy_
        self.bstack1l111lllll_opy_ = bstack1l111lllll_opy_
        self._prepareconfig = None
        self.Config = None
        self.runner = None
        self.bstack1ll1111l_opy_ = []
        self.bstack1l111llll1_opy_ = None
        self.bstack1l1ll1l1l1_opy_ = []
        self.bstack1l111ll1l1_opy_ = self.bstack1ll11111l1_opy_()
        self.bstack1l1l1ll1_opy_ = -1
    def bstack1ll1ll1lll_opy_(self, bstack1l111ll111_opy_):
        self.parse_args()
        self.bstack1l11l1111l_opy_()
        self.bstack1l11l11l11_opy_(bstack1l111ll111_opy_)
    @staticmethod
    def version():
        import pytest
        return pytest.__version__
    def bstack1l11l111ll_opy_(self, arg):
        if arg in self.args:
            i = self.args.index(arg)
            self.args.pop(i + 1)
            self.args.pop(i)
    def parse_args(self):
        self.bstack1l1l1ll1_opy_ = -1
        if bstack11l1ll_opy_ (u"ࠬࡶࡡࡳࡣ࡯ࡰࡪࡲࡳࡑࡧࡵࡔࡱࡧࡴࡧࡱࡵࡱࠬඣ") in self.bstack1l111ll1ll_opy_:
            self.bstack1l1l1ll1_opy_ = self.bstack1l111ll1ll_opy_[bstack11l1ll_opy_ (u"࠭ࡰࡢࡴࡤࡰࡱ࡫࡬ࡴࡒࡨࡶࡕࡲࡡࡵࡨࡲࡶࡲ࠭ඤ")]
        try:
            bstack1l111ll11l_opy_ = [bstack11l1ll_opy_ (u"ࠧ࠮࠯ࡧࡶ࡮ࡼࡥࡳࠩඥ"), bstack11l1ll_opy_ (u"ࠨ࠯࠰ࡴࡱࡻࡧࡪࡰࡶࠫඦ"), bstack11l1ll_opy_ (u"ࠩ࠰ࡴࠬට")]
            if self.bstack1l1l1ll1_opy_ >= 0:
                bstack1l111ll11l_opy_.extend([bstack11l1ll_opy_ (u"ࠪ࠱࠲ࡴࡵ࡮ࡲࡵࡳࡨ࡫ࡳࡴࡧࡶࠫඨ"), bstack11l1ll_opy_ (u"ࠫ࠲ࡴࠧඩ")])
            for arg in bstack1l111ll11l_opy_:
                self.bstack1l11l111ll_opy_(arg)
        except Exception as exc:
            self.logger.error(str(exc))
    def get_args(self):
        return self.args
    def bstack1l11l1111l_opy_(self):
        bstack1l111llll1_opy_ = [os.path.normpath(item) for item in self.args]
        self.bstack1l111llll1_opy_ = bstack1l111llll1_opy_
        return bstack1l111llll1_opy_
    def bstack111ll111l_opy_(self):
        try:
            from _pytest.config import _prepareconfig
            from _pytest.config import Config
            from _pytest import runner
            import importlib
            bstack1l111lll1l_opy_ = importlib.find_loader(bstack11l1ll_opy_ (u"ࠬࡶࡹࡵࡧࡶࡸࡤࡹࡥ࡭ࡧࡱ࡭ࡺࡳࠧඪ"))
            self._prepareconfig = _prepareconfig
            self.Config = Config
            self.runner = runner
        except Exception as e:
            self.logger.warn(e, bstack1lll11ll1l_opy_)
    def bstack1l11l11l11_opy_(self, bstack1l111ll111_opy_):
        bstack1ll1l11l1_opy_ = Config.get_instance()
        if bstack1l111ll111_opy_:
            self.bstack1l111llll1_opy_.append(bstack11l1ll_opy_ (u"࠭࠭࠮ࡵ࡮࡭ࡵ࡙ࡥࡴࡵ࡬ࡳࡳࡔࡡ࡮ࡧࠪණ"))
            self.bstack1l111llll1_opy_.append(bstack11l1ll_opy_ (u"ࠧࡕࡴࡸࡩࠬඬ"))
        if bstack1ll1l11l1_opy_.bstack1l11l11111_opy_():
            self.bstack1l111llll1_opy_.append(bstack11l1ll_opy_ (u"ࠨ࠯࠰ࡷࡰ࡯ࡰࡔࡧࡶࡷ࡮ࡵ࡮ࡔࡶࡤࡸࡺࡹࠧත"))
            self.bstack1l111llll1_opy_.append(bstack11l1ll_opy_ (u"ࠩࡗࡶࡺ࡫ࠧථ"))
        self.bstack1l111llll1_opy_.append(bstack11l1ll_opy_ (u"ࠪ࠱ࡵ࠭ද"))
        self.bstack1l111llll1_opy_.append(bstack11l1ll_opy_ (u"ࠫࡵࡿࡴࡦࡵࡷࡣࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࡳࡰࡺ࡭ࡩ࡯ࠩධ"))
        self.bstack1l111llll1_opy_.append(bstack11l1ll_opy_ (u"ࠬ࠳࠭ࡥࡴ࡬ࡺࡪࡸࠧන"))
        self.bstack1l111llll1_opy_.append(bstack11l1ll_opy_ (u"࠭ࡣࡩࡴࡲࡱࡪ࠭඲"))
        if self.bstack1l1l1ll1_opy_ > 1:
            self.bstack1l111llll1_opy_.append(bstack11l1ll_opy_ (u"ࠧ࠮ࡰࠪඳ"))
            self.bstack1l111llll1_opy_.append(str(self.bstack1l1l1ll1_opy_))
    def bstack1l111lll11_opy_(self):
        bstack1l1ll1l1l1_opy_ = []
        for spec in self.bstack1ll1111l_opy_:
            bstack11lll11ll_opy_ = [spec]
            bstack11lll11ll_opy_ += self.bstack1l111llll1_opy_
            bstack1l1ll1l1l1_opy_.append(bstack11lll11ll_opy_)
        self.bstack1l1ll1l1l1_opy_ = bstack1l1ll1l1l1_opy_
        return bstack1l1ll1l1l1_opy_
    def bstack1ll11111l1_opy_(self):
        try:
            from pytest_bdd import reporting
            self.bstack1l111ll1l1_opy_ = True
            return True
        except Exception as e:
            self.bstack1l111ll1l1_opy_ = False
        return self.bstack1l111ll1l1_opy_
    def bstack11llllll_opy_(self, bstack1l111l1lll_opy_, bstack1ll1ll1lll_opy_):
        bstack1ll1ll1lll_opy_[bstack11l1ll_opy_ (u"ࠨࡅࡒࡒࡋࡏࡇࠨප")] = self.bstack1l111ll1ll_opy_
        multiprocessing.set_start_method(bstack11l1ll_opy_ (u"ࠩࡶࡴࡦࡽ࡮ࠨඵ"))
        if bstack11l1ll_opy_ (u"ࠪࡴࡱࡧࡴࡧࡱࡵࡱࡸ࠭බ") in self.bstack1l111ll1ll_opy_:
            bstack1ll111111l_opy_ = []
            manager = multiprocessing.Manager()
            bstack1lll1ll1ll_opy_ = manager.list()
            for index, platform in enumerate(self.bstack1l111ll1ll_opy_[bstack11l1ll_opy_ (u"ࠫࡵࡲࡡࡵࡨࡲࡶࡲࡹࠧභ")]):
                bstack1ll111111l_opy_.append(multiprocessing.Process(name=str(index),
                                                           target=bstack1l111l1lll_opy_,
                                                           args=(self.bstack1l111llll1_opy_, bstack1ll1ll1lll_opy_, bstack1lll1ll1ll_opy_)))
            i = 0
            bstack1l11l111l1_opy_ = len(self.bstack1l111ll1ll_opy_[bstack11l1ll_opy_ (u"ࠬࡶ࡬ࡢࡶࡩࡳࡷࡳࡳࠨම")])
            for t in bstack1ll111111l_opy_:
                os.environ[bstack11l1ll_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤࡖࡌࡂࡖࡉࡓࡗࡓ࡟ࡊࡐࡇࡉ࡝࠭ඹ")] = str(i)
                os.environ[bstack11l1ll_opy_ (u"ࠧࡄࡗࡕࡖࡊࡔࡔࡠࡒࡏࡅ࡙ࡌࡏࡓࡏࡢࡈࡆ࡚ࡁࠨය")] = json.dumps(self.bstack1l111ll1ll_opy_[bstack11l1ll_opy_ (u"ࠨࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࡶࠫර")][i % bstack1l11l111l1_opy_])
                i += 1
                t.start()
            for t in bstack1ll111111l_opy_:
                t.join()
            return list(bstack1lll1ll1ll_opy_)