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
import multiprocessing
import os
import json
from browserstack_sdk.bstack1lllll1l11_opy_ import *
from bstack_utils.messages import bstack1l1l1111l_opy_
class bstack1ll111ll1_opy_:
    def __init__(self, args, logger, bstack1l111ll1ll_opy_, bstack1l111llll1_opy_):
        self.args = args
        self.logger = logger
        self.bstack1l111ll1ll_opy_ = bstack1l111ll1ll_opy_
        self.bstack1l111llll1_opy_ = bstack1l111llll1_opy_
        self._prepareconfig = None
        self.Config = None
        self.runner = None
        self.bstack1ll1111l1_opy_ = []
        self.bstack1l111lllll_opy_ = None
        self.bstack111111ll_opy_ = []
        self.bstack1l111lll1l_opy_ = self.bstack1l1lll11ll_opy_()
        self.bstack1ll11l1l11_opy_ = -1
    def bstack1111llll1_opy_(self, bstack1l11l11l11_opy_):
        self.parse_args()
        self.bstack1l11l111ll_opy_()
        self.bstack1l11l1111l_opy_(bstack1l11l11l11_opy_)
    @staticmethod
    def version():
        import pytest
        return pytest.__version__
    def bstack1l11l111l1_opy_(self, arg):
        if arg in self.args:
            i = self.args.index(arg)
            self.args.pop(i + 1)
            self.args.pop(i)
    def parse_args(self):
        self.bstack1ll11l1l11_opy_ = -1
        if bstack11l1l1l_opy_ (u"ࠧࡱࡣࡵࡥࡱࡲࡥ࡭ࡵࡓࡩࡷࡖ࡬ࡢࡶࡩࡳࡷࡳࠧය") in self.bstack1l111ll1ll_opy_:
            self.bstack1ll11l1l11_opy_ = self.bstack1l111ll1ll_opy_[bstack11l1l1l_opy_ (u"ࠨࡲࡤࡶࡦࡲ࡬ࡦ࡮ࡶࡔࡪࡸࡐ࡭ࡣࡷࡪࡴࡸ࡭ࠨර")]
        try:
            bstack1l11l11l1l_opy_ = [bstack11l1l1l_opy_ (u"ࠩ࠰࠱ࡩࡸࡩࡷࡧࡵࠫ඼"), bstack11l1l1l_opy_ (u"ࠪ࠱࠲ࡶ࡬ࡶࡩ࡬ࡲࡸ࠭ල"), bstack11l1l1l_opy_ (u"ࠫ࠲ࡶࠧ඾")]
            if self.bstack1ll11l1l11_opy_ >= 0:
                bstack1l11l11l1l_opy_.extend([bstack11l1l1l_opy_ (u"ࠬ࠳࠭࡯ࡷࡰࡴࡷࡵࡣࡦࡵࡶࡩࡸ࠭඿"), bstack11l1l1l_opy_ (u"࠭࠭࡯ࠩව")])
            for arg in bstack1l11l11l1l_opy_:
                self.bstack1l11l111l1_opy_(arg)
        except Exception as exc:
            self.logger.error(str(exc))
    def get_args(self):
        return self.args
    def bstack1l11l111ll_opy_(self):
        bstack1l111lllll_opy_ = [os.path.normpath(item) for item in self.args]
        self.bstack1l111lllll_opy_ = bstack1l111lllll_opy_
        return bstack1l111lllll_opy_
    def bstack1lll1l1111_opy_(self):
        try:
            from _pytest.config import _prepareconfig
            from _pytest.config import Config
            from _pytest import runner
            import importlib
            bstack1l111lll11_opy_ = importlib.find_loader(bstack11l1l1l_opy_ (u"ࠧࡱࡻࡷࡩࡸࡺ࡟ࡴࡧ࡯ࡩࡳ࡯ࡵ࡮ࠩශ"))
            self._prepareconfig = _prepareconfig
            self.Config = Config
            self.runner = runner
        except Exception as e:
            self.logger.warn(e, bstack1l1l1111l_opy_)
    def bstack1l11l1111l_opy_(self, bstack1l11l11l11_opy_):
        if bstack1l11l11l11_opy_:
            self.bstack1l111lllll_opy_.append(bstack11l1l1l_opy_ (u"ࠨ࠯࠰ࡷࡰ࡯ࡰࡔࡧࡶࡷ࡮ࡵ࡮ࡏࡣࡰࡩࠬෂ"))
            self.bstack1l111lllll_opy_.append(bstack11l1l1l_opy_ (u"ࠩࡗࡶࡺ࡫ࠧස"))
        self.bstack1l111lllll_opy_.append(bstack11l1l1l_opy_ (u"ࠪ࠱ࡵ࠭හ"))
        self.bstack1l111lllll_opy_.append(bstack11l1l1l_opy_ (u"ࠫࡵࡿࡴࡦࡵࡷࡣࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࡳࡰࡺ࡭ࡩ࡯ࠩළ"))
        self.bstack1l111lllll_opy_.append(bstack11l1l1l_opy_ (u"ࠬ࠳࠭ࡥࡴ࡬ࡺࡪࡸࠧෆ"))
        self.bstack1l111lllll_opy_.append(bstack11l1l1l_opy_ (u"࠭ࡣࡩࡴࡲࡱࡪ࠭෇"))
        if self.bstack1ll11l1l11_opy_ > 1:
            self.bstack1l111lllll_opy_.append(bstack11l1l1l_opy_ (u"ࠧ࠮ࡰࠪ෈"))
            self.bstack1l111lllll_opy_.append(str(self.bstack1ll11l1l11_opy_))
    def bstack1l11l11111_opy_(self):
        bstack111111ll_opy_ = []
        for spec in self.bstack1ll1111l1_opy_:
            bstack11111ll1l_opy_ = [spec]
            bstack11111ll1l_opy_ += self.bstack1l111lllll_opy_
            bstack111111ll_opy_.append(bstack11111ll1l_opy_)
        self.bstack111111ll_opy_ = bstack111111ll_opy_
        return bstack111111ll_opy_
    def bstack1l1lll11ll_opy_(self):
        try:
            from pytest_bdd import reporting
            self.bstack1l111lll1l_opy_ = True
            return True
        except Exception as e:
            self.bstack1l111lll1l_opy_ = False
        return self.bstack1l111lll1l_opy_
    def bstack11llll111_opy_(self, bstack1l11l11ll1_opy_, bstack1111llll1_opy_):
        bstack1111llll1_opy_[bstack11l1l1l_opy_ (u"ࠨࡅࡒࡒࡋࡏࡇࠨ෉")] = self.bstack1l111ll1ll_opy_
        multiprocessing.set_start_method(bstack11l1l1l_opy_ (u"ࠩࡶࡴࡦࡽ࡮ࠨ්"))
        if bstack11l1l1l_opy_ (u"ࠪࡴࡱࡧࡴࡧࡱࡵࡱࡸ࠭෋") in self.bstack1l111ll1ll_opy_:
            bstack11lll1ll_opy_ = []
            manager = multiprocessing.Manager()
            bstack11lllll11_opy_ = manager.list()
            for index, platform in enumerate(self.bstack1l111ll1ll_opy_[bstack11l1l1l_opy_ (u"ࠫࡵࡲࡡࡵࡨࡲࡶࡲࡹࠧ෌")]):
                bstack11lll1ll_opy_.append(multiprocessing.Process(name=str(index),
                                                           target=bstack1l11l11ll1_opy_,
                                                           args=(self.bstack1l111lllll_opy_, bstack1111llll1_opy_, bstack11lllll11_opy_)))
            i = 0
            bstack1l11l11lll_opy_ = len(self.bstack1l111ll1ll_opy_[bstack11l1l1l_opy_ (u"ࠬࡶ࡬ࡢࡶࡩࡳࡷࡳࡳࠨ෍")])
            for t in bstack11lll1ll_opy_:
                os.environ[bstack11l1l1l_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤࡖࡌࡂࡖࡉࡓࡗࡓ࡟ࡊࡐࡇࡉ࡝࠭෎")] = str(i)
                os.environ[bstack11l1l1l_opy_ (u"ࠧࡄࡗࡕࡖࡊࡔࡔࡠࡒࡏࡅ࡙ࡌࡏࡓࡏࡢࡈࡆ࡚ࡁࠨා")] = json.dumps(self.bstack1l111ll1ll_opy_[bstack11l1l1l_opy_ (u"ࠨࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࡶࠫැ")][i % bstack1l11l11lll_opy_])
                i += 1
                t.start()
            for t in bstack11lll1ll_opy_:
                t.join()
            return list(bstack11lllll11_opy_)