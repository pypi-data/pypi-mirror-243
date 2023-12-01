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
import datetime
import threading
from uuid import uuid4
from itertools import zip_longest
from collections import OrderedDict
from robot.libraries.BuiltIn import BuiltIn
from browserstack_sdk.bstack1l1l11lll1_opy_ import RobotHandler
from bstack_utils.capture import bstack1l11ll1lll_opy_
from bstack_utils.bstack1l1l1l111l_opy_ import bstack1l11llllll_opy_, bstack1l11ll1ll1_opy_, bstack1l1l111ll1_opy_
from bstack_utils.bstack1ll11ll1l1_opy_ import bstack11l1ll11_opy_
from bstack_utils.constants import *
from bstack_utils.helper import bstack11111l11_opy_, bstack1ll11111ll_opy_, Result, \
    bstack1l1l1ll111_opy_
class bstack_robot_listener:
    ROBOT_LISTENER_API_VERSION = 2
    store = {
        bstack11l1ll_opy_ (u"ࠪࡧࡺࡸࡲࡦࡰࡷࡣ࡭ࡵ࡯࡬ࡡࡸࡹ࡮ࡪࠧ೫"): [],
        bstack11l1ll_opy_ (u"ࠫ࡬ࡲ࡯ࡣࡣ࡯ࡣ࡭ࡵ࡯࡬ࡵࠪ೬"): [],
        bstack11l1ll_opy_ (u"ࠬࡺࡥࡴࡶࡢ࡬ࡴࡵ࡫ࡴࠩ೭"): []
    }
    bstack1l11ll11ll_opy_ = []
    @staticmethod
    def bstack1l1l1l1lll_opy_(log):
        if not (log[bstack11l1ll_opy_ (u"࠭࡭ࡦࡵࡶࡥ࡬࡫ࠧ೮")] and log[bstack11l1ll_opy_ (u"ࠧ࡮ࡧࡶࡷࡦ࡭ࡥࠨ೯")].strip()):
            return
        active = bstack11l1ll11_opy_.bstack1l1l1111l1_opy_()
        log = {
            bstack11l1ll_opy_ (u"ࠨ࡮ࡨࡺࡪࡲࠧ೰"): log[bstack11l1ll_opy_ (u"ࠩ࡯ࡩࡻ࡫࡬ࠨೱ")],
            bstack11l1ll_opy_ (u"ࠪࡸ࡮ࡳࡥࡴࡶࡤࡱࡵ࠭ೲ"): datetime.datetime.utcnow().isoformat() + bstack11l1ll_opy_ (u"ࠫ࡟࠭ೳ"),
            bstack11l1ll_opy_ (u"ࠬࡳࡥࡴࡵࡤ࡫ࡪ࠭೴"): log[bstack11l1ll_opy_ (u"࠭࡭ࡦࡵࡶࡥ࡬࡫ࠧ೵")],
        }
        if active:
            if active[bstack11l1ll_opy_ (u"ࠧࡵࡻࡳࡩࠬ೶")] == bstack11l1ll_opy_ (u"ࠨࡪࡲࡳࡰ࠭೷"):
                log[bstack11l1ll_opy_ (u"ࠩ࡫ࡳࡴࡱ࡟ࡳࡷࡱࡣࡺࡻࡩࡥࠩ೸")] = active[bstack11l1ll_opy_ (u"ࠪ࡬ࡴࡵ࡫ࡠࡴࡸࡲࡤࡻࡵࡪࡦࠪ೹")]
            elif active[bstack11l1ll_opy_ (u"ࠫࡹࡿࡰࡦࠩ೺")] == bstack11l1ll_opy_ (u"ࠬࡺࡥࡴࡶࠪ೻"):
                log[bstack11l1ll_opy_ (u"࠭ࡴࡦࡵࡷࡣࡷࡻ࡮ࡠࡷࡸ࡭ࡩ࠭೼")] = active[bstack11l1ll_opy_ (u"ࠧࡵࡧࡶࡸࡤࡸࡵ࡯ࡡࡸࡹ࡮ࡪࠧ೽")]
        bstack11l1ll11_opy_.bstack1l1l1l11ll_opy_([log])
    def __init__(self):
        self.messages = Messages()
        self._1l1l11ll11_opy_ = None
        self._1l11l1lll1_opy_ = None
        self._1l1l111l11_opy_ = OrderedDict()
        self.bstack1l11l11ll1_opy_ = bstack1l11ll1lll_opy_(self.bstack1l1l1l1lll_opy_)
    @bstack1l1l1ll111_opy_(class_method=True)
    def start_suite(self, name, attrs):
        self.messages.bstack1l1l11l11l_opy_()
        if not self._1l1l111l11_opy_.get(attrs.get(bstack11l1ll_opy_ (u"ࠨ࡫ࡧࠫ೾")), None):
            self._1l1l111l11_opy_[attrs.get(bstack11l1ll_opy_ (u"ࠩ࡬ࡨࠬ೿"))] = {}
        bstack1l1l1llll1_opy_ = bstack1l1l111ll1_opy_(
                bstack1l11l1ll11_opy_=attrs.get(bstack11l1ll_opy_ (u"ࠪ࡭ࡩ࠭ഀ")),
                name=name,
                bstack1l1l1l11l1_opy_=bstack1ll11111ll_opy_(),
                file_path=os.path.relpath(attrs[bstack11l1ll_opy_ (u"ࠫࡸࡵࡵࡳࡥࡨࠫഁ")], start=os.getcwd()) if attrs.get(bstack11l1ll_opy_ (u"ࠬࡹ࡯ࡶࡴࡦࡩࠬം")) != bstack11l1ll_opy_ (u"࠭ࠧഃ") else bstack11l1ll_opy_ (u"ࠧࠨഄ"),
                framework=bstack11l1ll_opy_ (u"ࠨࡔࡲࡦࡴࡺࠧഅ")
            )
        threading.current_thread().current_suite_id = attrs.get(bstack11l1ll_opy_ (u"ࠩ࡬ࡨࠬആ"), None)
        self._1l1l111l11_opy_[attrs.get(bstack11l1ll_opy_ (u"ࠪ࡭ࡩ࠭ഇ"))][bstack11l1ll_opy_ (u"ࠫࡹ࡫ࡳࡵࡡࡧࡥࡹࡧࠧഈ")] = bstack1l1l1llll1_opy_
    @bstack1l1l1ll111_opy_(class_method=True)
    def end_suite(self, name, attrs):
        messages = self.messages.bstack1l1l1l1ll1_opy_()
        self._1l11ll11l1_opy_(messages)
        for bstack1l1l11l1l1_opy_ in self.bstack1l11ll11ll_opy_:
            bstack1l1l11l1l1_opy_[bstack11l1ll_opy_ (u"ࠬࡺࡥࡴࡶࡢࡶࡺࡴࠧഉ")][bstack11l1ll_opy_ (u"࠭ࡨࡰࡱ࡮ࡷࠬഊ")].extend(self.store[bstack11l1ll_opy_ (u"ࠧࡨ࡮ࡲࡦࡦࡲ࡟ࡩࡱࡲ࡯ࡸ࠭ഋ")])
            bstack11l1ll11_opy_.bstack1l1l11llll_opy_(bstack1l1l11l1l1_opy_)
        self.bstack1l11ll11ll_opy_ = []
        self.store[bstack11l1ll_opy_ (u"ࠨࡩ࡯ࡳࡧࡧ࡬ࡠࡪࡲࡳࡰࡹࠧഌ")] = []
    @bstack1l1l1ll111_opy_(class_method=True)
    def start_test(self, name, attrs):
        self.bstack1l11l11ll1_opy_.start()
        if not self._1l1l111l11_opy_.get(attrs.get(bstack11l1ll_opy_ (u"ࠩ࡬ࡨࠬ഍")), None):
            self._1l1l111l11_opy_[attrs.get(bstack11l1ll_opy_ (u"ࠪ࡭ࡩ࠭എ"))] = {}
        driver = bstack11111l11_opy_(threading.current_thread(), bstack11l1ll_opy_ (u"ࠫࡧࡹࡴࡢࡥ࡮ࡗࡪࡹࡳࡪࡱࡱࡈࡷ࡯ࡶࡦࡴࠪഏ"), None)
        bstack1l1l1l111l_opy_ = bstack1l1l111ll1_opy_(
            bstack1l11l1ll11_opy_=attrs.get(bstack11l1ll_opy_ (u"ࠬ࡯ࡤࠨഐ")),
            name=name,
            bstack1l1l1l11l1_opy_=bstack1ll11111ll_opy_(),
            file_path=os.path.relpath(attrs[bstack11l1ll_opy_ (u"࠭ࡳࡰࡷࡵࡧࡪ࠭഑")], start=os.getcwd()),
            scope=RobotHandler.bstack1l11l1ll1l_opy_(attrs.get(bstack11l1ll_opy_ (u"ࠧࡴࡱࡸࡶࡨ࡫ࠧഒ"), None)),
            framework=bstack11l1ll_opy_ (u"ࠨࡔࡲࡦࡴࡺࠧഓ"),
            tags=attrs[bstack11l1ll_opy_ (u"ࠩࡷࡥ࡬ࡹࠧഔ")],
            hooks=self.store[bstack11l1ll_opy_ (u"ࠪ࡫ࡱࡵࡢࡢ࡮ࡢ࡬ࡴࡵ࡫ࡴࠩക")],
            bstack1l11l1l1l1_opy_=bstack11l1ll11_opy_.bstack1l11ll111l_opy_(driver) if driver and driver.session_id else {},
            meta={},
            code=bstack11l1ll_opy_ (u"ࠦࢀࢃࠠ࡝ࡰࠣࡿࢂࠨഖ").format(bstack11l1ll_opy_ (u"ࠧࠦࠢഗ").join(attrs[bstack11l1ll_opy_ (u"࠭ࡴࡢࡩࡶࠫഘ")]), name) if attrs[bstack11l1ll_opy_ (u"ࠧࡵࡣࡪࡷࠬങ")] else name
        )
        self._1l1l111l11_opy_[attrs.get(bstack11l1ll_opy_ (u"ࠨ࡫ࡧࠫച"))][bstack11l1ll_opy_ (u"ࠩࡷࡩࡸࡺ࡟ࡥࡣࡷࡥࠬഛ")] = bstack1l1l1l111l_opy_
        threading.current_thread().current_test_uuid = bstack1l1l1l111l_opy_.bstack1l11lllll1_opy_()
        threading.current_thread().current_test_id = attrs.get(bstack11l1ll_opy_ (u"ࠪ࡭ࡩ࠭ജ"), None)
        self.bstack1l1l1ll1ll_opy_(bstack11l1ll_opy_ (u"࡙ࠫ࡫ࡳࡵࡔࡸࡲࡘࡺࡡࡳࡶࡨࡨࠬഝ"), bstack1l1l1l111l_opy_)
    @bstack1l1l1ll111_opy_(class_method=True)
    def end_test(self, name, attrs):
        self.bstack1l11l11ll1_opy_.reset()
        bstack1l11lll1ll_opy_ = bstack1l1l11l111_opy_.get(attrs.get(bstack11l1ll_opy_ (u"ࠬࡹࡴࡢࡶࡸࡷࠬഞ")), bstack11l1ll_opy_ (u"࠭ࡳ࡬࡫ࡳࡴࡪࡪࠧട"))
        self._1l1l111l11_opy_[attrs.get(bstack11l1ll_opy_ (u"ࠧࡪࡦࠪഠ"))][bstack11l1ll_opy_ (u"ࠨࡶࡨࡷࡹࡥࡤࡢࡶࡤࠫഡ")].stop(time=bstack1ll11111ll_opy_(), duration=int(attrs.get(bstack11l1ll_opy_ (u"ࠩࡨࡰࡦࡶࡳࡦࡦࡷ࡭ࡲ࡫ࠧഢ"), bstack11l1ll_opy_ (u"ࠪ࠴ࠬണ"))), result=Result(result=bstack1l11lll1ll_opy_, exception=attrs.get(bstack11l1ll_opy_ (u"ࠫࡲ࡫ࡳࡴࡣࡪࡩࠬത")), bstack1l11llll1l_opy_=[attrs.get(bstack11l1ll_opy_ (u"ࠬࡳࡥࡴࡵࡤ࡫ࡪ࠭ഥ"))]))
        self.bstack1l1l1ll1ll_opy_(bstack11l1ll_opy_ (u"࠭ࡔࡦࡵࡷࡖࡺࡴࡆࡪࡰ࡬ࡷ࡭࡫ࡤࠨദ"), self._1l1l111l11_opy_[attrs.get(bstack11l1ll_opy_ (u"ࠧࡪࡦࠪധ"))][bstack11l1ll_opy_ (u"ࠨࡶࡨࡷࡹࡥࡤࡢࡶࡤࠫന")], True)
        self.store[bstack11l1ll_opy_ (u"ࠩࡷࡩࡸࡺ࡟ࡩࡱࡲ࡯ࡸ࠭ഩ")] = []
        threading.current_thread().current_test_uuid = None
        threading.current_thread().current_test_id = None
    @bstack1l1l1ll111_opy_(class_method=True)
    def start_keyword(self, name, attrs):
        self.messages.bstack1l1l11l11l_opy_()
        current_test_id = bstack11111l11_opy_(threading.current_thread(), bstack11l1ll_opy_ (u"ࠪࡧࡺࡸࡲࡦࡰࡷࡣࡹ࡫ࡳࡵࡡ࡬ࡨࠬപ"), None)
        bstack1l1l1ll1l1_opy_ = current_test_id if bstack11111l11_opy_(threading.current_thread(), bstack11l1ll_opy_ (u"ࠫࡨࡻࡲࡳࡧࡱࡸࡤࡺࡥࡴࡶࡢ࡭ࡩ࠭ഫ"), None) else bstack11111l11_opy_(threading.current_thread(), bstack11l1ll_opy_ (u"ࠬࡩࡵࡳࡴࡨࡲࡹࡥࡳࡶ࡫ࡷࡩࡤ࡯ࡤࠨബ"), None)
        if attrs.get(bstack11l1ll_opy_ (u"࠭ࡴࡺࡲࡨࠫഭ"), bstack11l1ll_opy_ (u"ࠧࠨമ")).lower() in [bstack11l1ll_opy_ (u"ࠨࡵࡨࡸࡺࡶࠧയ"), bstack11l1ll_opy_ (u"ࠩࡷࡩࡦࡸࡤࡰࡹࡱࠫര")]:
            hook_type = bstack1l1l11ll1l_opy_(attrs.get(bstack11l1ll_opy_ (u"ࠪࡸࡾࡶࡥࠨറ")), bstack11111l11_opy_(threading.current_thread(), bstack11l1ll_opy_ (u"ࠫࡨࡻࡲࡳࡧࡱࡸࡤࡺࡥࡴࡶࡢࡹࡺ࡯ࡤࠨല"), None))
            bstack1l11l1l1ll_opy_ = bstack1l11ll1ll1_opy_(
                bstack1l11l1ll11_opy_=bstack1l1l1ll1l1_opy_ + bstack11l1ll_opy_ (u"ࠬ࠳ࠧള") + attrs.get(bstack11l1ll_opy_ (u"࠭ࡴࡺࡲࡨࠫഴ"), bstack11l1ll_opy_ (u"ࠧࠨവ")).lower(),
                name=bstack11l1ll_opy_ (u"ࠨ࡝ࡾࢁࡢࠦࡻࡾࠩശ").format(hook_type, attrs.get(bstack11l1ll_opy_ (u"ࠩ࡮ࡻࡳࡧ࡭ࡦࠩഷ"), bstack11l1ll_opy_ (u"ࠪࠫസ"))) if hook_type in [bstack11l1ll_opy_ (u"ࠫࡇࡋࡆࡐࡔࡈࡣࡆࡒࡌࠨഹ"), bstack11l1ll_opy_ (u"ࠬࡇࡆࡕࡇࡕࡣࡆࡒࡌࠨഺ")] else bstack11l1ll_opy_ (u"࠭ࡻࡾ഻ࠩ").format(attrs.get(bstack11l1ll_opy_ (u"ࠧ࡬ࡹࡱࡥࡲ࡫഼ࠧ"), bstack11l1ll_opy_ (u"ࠨࠩഽ"))),
                bstack1l1l1l11l1_opy_=bstack1ll11111ll_opy_(),
                file_path=os.path.relpath(attrs.get(bstack11l1ll_opy_ (u"ࠩࡶࡳࡺࡸࡣࡦࠩാ")), start=os.getcwd()),
                framework=bstack11l1ll_opy_ (u"ࠪࡖࡴࡨ࡯ࡵࠩി"),
                tags=attrs[bstack11l1ll_opy_ (u"ࠫࡹࡧࡧࡴࠩീ")],
                scope=RobotHandler.bstack1l11l1ll1l_opy_(attrs.get(bstack11l1ll_opy_ (u"ࠬࡹ࡯ࡶࡴࡦࡩࠬു"), None)),
                hook_type=hook_type,
                meta={}
            )
            threading.current_thread().current_hook_uuid = bstack1l11l1l1ll_opy_.bstack1l11lllll1_opy_()
            threading.current_thread().current_hook_id = bstack1l1l1ll1l1_opy_ + bstack11l1ll_opy_ (u"࠭࠭ࠨൂ") + attrs.get(bstack11l1ll_opy_ (u"ࠧࡵࡻࡳࡩࠬൃ"), bstack11l1ll_opy_ (u"ࠨࠩൄ")).lower()
            self.store[bstack11l1ll_opy_ (u"ࠩࡦࡹࡷࡸࡥ࡯ࡶࡢ࡬ࡴࡵ࡫ࡠࡷࡸ࡭ࡩ࠭൅")] = [bstack1l11l1l1ll_opy_.bstack1l11lllll1_opy_()]
            if bstack11111l11_opy_(threading.current_thread(), bstack11l1ll_opy_ (u"ࠪࡧࡺࡸࡲࡦࡰࡷࡣࡹ࡫ࡳࡵࡡࡸࡹ࡮ࡪࠧെ"), None):
                self.store[bstack11l1ll_opy_ (u"ࠫࡹ࡫ࡳࡵࡡ࡫ࡳࡴࡱࡳࠨേ")].append(bstack1l11l1l1ll_opy_.bstack1l11lllll1_opy_())
            else:
                self.store[bstack11l1ll_opy_ (u"ࠬ࡭࡬ࡰࡤࡤࡰࡤ࡮࡯ࡰ࡭ࡶࠫൈ")].append(bstack1l11l1l1ll_opy_.bstack1l11lllll1_opy_())
            if bstack1l1l1ll1l1_opy_:
                self._1l1l111l11_opy_[bstack1l1l1ll1l1_opy_ + bstack11l1ll_opy_ (u"࠭࠭ࠨ൉") + attrs.get(bstack11l1ll_opy_ (u"ࠧࡵࡻࡳࡩࠬൊ"), bstack11l1ll_opy_ (u"ࠨࠩോ")).lower()] = { bstack11l1ll_opy_ (u"ࠩࡷࡩࡸࡺ࡟ࡥࡣࡷࡥࠬൌ"): bstack1l11l1l1ll_opy_ }
            bstack11l1ll11_opy_.bstack1l1l1ll1ll_opy_(bstack11l1ll_opy_ (u"ࠪࡌࡴࡵ࡫ࡓࡷࡱࡗࡹࡧࡲࡵࡧࡧ്ࠫ"), bstack1l11l1l1ll_opy_)
        else:
            bstack1l1l1ll11l_opy_ = {
                bstack11l1ll_opy_ (u"ࠫ࡮ࡪࠧൎ"): uuid4().__str__(),
                bstack11l1ll_opy_ (u"ࠬࡺࡥࡹࡶࠪ൏"): bstack11l1ll_opy_ (u"࠭ࡻࡾࠢࡾࢁࠬ൐").format(attrs.get(bstack11l1ll_opy_ (u"ࠧ࡬ࡹࡱࡥࡲ࡫ࠧ൑")), attrs.get(bstack11l1ll_opy_ (u"ࠨࡣࡵ࡫ࡸ࠭൒"), bstack11l1ll_opy_ (u"ࠩࠪ൓"))) if attrs.get(bstack11l1ll_opy_ (u"ࠪࡥࡷ࡭ࡳࠨൔ"), []) else attrs.get(bstack11l1ll_opy_ (u"ࠫࡰࡽ࡮ࡢ࡯ࡨࠫൕ")),
                bstack11l1ll_opy_ (u"ࠬࡹࡴࡦࡲࡢࡥࡷ࡭ࡵ࡮ࡧࡱࡸࠬൖ"): attrs.get(bstack11l1ll_opy_ (u"࠭ࡡࡳࡩࡶࠫൗ"), []),
                bstack11l1ll_opy_ (u"ࠧࡴࡶࡤࡶࡹ࡫ࡤࡠࡣࡷࠫ൘"): bstack1ll11111ll_opy_(),
                bstack11l1ll_opy_ (u"ࠨࡴࡨࡷࡺࡲࡴࠨ൙"): bstack11l1ll_opy_ (u"ࠩࡳࡩࡳࡪࡩ࡯ࡩࠪ൚"),
                bstack11l1ll_opy_ (u"ࠪࡨࡪࡹࡣࡳ࡫ࡳࡸ࡮ࡵ࡮ࠨ൛"): attrs.get(bstack11l1ll_opy_ (u"ࠫࡩࡵࡣࠨ൜"), bstack11l1ll_opy_ (u"ࠬ࠭൝"))
            }
            if attrs.get(bstack11l1ll_opy_ (u"࠭࡬ࡪࡤࡱࡥࡲ࡫ࠧ൞"), bstack11l1ll_opy_ (u"ࠧࠨൟ")) != bstack11l1ll_opy_ (u"ࠨࠩൠ"):
                bstack1l1l1ll11l_opy_[bstack11l1ll_opy_ (u"ࠩ࡮ࡩࡾࡽ࡯ࡳࡦࠪൡ")] = attrs.get(bstack11l1ll_opy_ (u"ࠪࡰ࡮ࡨ࡮ࡢ࡯ࡨࠫൢ"))
            threading.current_thread().current_step_uuid = bstack1l1l1ll11l_opy_[bstack11l1ll_opy_ (u"ࠫ࡮ࡪࠧൣ")]
            self._1l1l111l11_opy_[self._1l11lll11l_opy_()][bstack11l1ll_opy_ (u"ࠬࡺࡥࡴࡶࡢࡨࡦࡺࡡࠨ൤")].add_step(bstack1l1l1ll11l_opy_)
    @bstack1l1l1ll111_opy_(class_method=True)
    def end_keyword(self, name, attrs):
        messages = self.messages.bstack1l1l1l1ll1_opy_()
        self._1l11ll11l1_opy_(messages)
        current_test_id = bstack11111l11_opy_(threading.current_thread(), bstack11l1ll_opy_ (u"࠭ࡣࡶࡴࡵࡩࡳࡺ࡟ࡵࡧࡶࡸࡤ࡯ࡤࠨ൥"), None)
        bstack1l1l1ll1l1_opy_ = current_test_id if current_test_id else bstack11111l11_opy_(threading.current_thread(), bstack11l1ll_opy_ (u"ࠧࡤࡷࡵࡶࡪࡴࡴࡠࡵࡸ࡭ࡹ࡫࡟ࡪࡦࠪ൦"), None)
        bstack1l11l11lll_opy_ = bstack1l1l11l111_opy_.get(attrs.get(bstack11l1ll_opy_ (u"ࠨࡵࡷࡥࡹࡻࡳࠨ൧")), bstack11l1ll_opy_ (u"ࠩࡶ࡯࡮ࡶࡰࡦࡦࠪ൨"))
        bstack1l1l1l1111_opy_ = attrs.get(bstack11l1ll_opy_ (u"ࠪࡱࡪࡹࡳࡢࡩࡨࠫ൩"))
        if bstack1l11l11lll_opy_ != bstack11l1ll_opy_ (u"ࠫࡸࡱࡩࡱࡲࡨࡨࠬ൪") and not attrs.get(bstack11l1ll_opy_ (u"ࠬࡳࡥࡴࡵࡤ࡫ࡪ࠭൫")) and self._1l1l11ll11_opy_:
            bstack1l1l1l1111_opy_ = self._1l1l11ll11_opy_
        bstack1l1l111l1l_opy_ = Result(result=bstack1l11l11lll_opy_, exception=bstack1l1l1l1111_opy_, bstack1l11llll1l_opy_=[bstack1l1l1l1111_opy_])
        if attrs.get(bstack11l1ll_opy_ (u"࠭ࡴࡺࡲࡨࠫ൬"), bstack11l1ll_opy_ (u"ࠧࠨ൭")).lower() in [bstack11l1ll_opy_ (u"ࠨࡵࡨࡸࡺࡶࠧ൮"), bstack11l1ll_opy_ (u"ࠩࡷࡩࡦࡸࡤࡰࡹࡱࠫ൯")]:
            bstack1l1l1ll1l1_opy_ = current_test_id if current_test_id else bstack11111l11_opy_(threading.current_thread(), bstack11l1ll_opy_ (u"ࠪࡧࡺࡸࡲࡦࡰࡷࡣࡸࡻࡩࡵࡧࡢ࡭ࡩ࠭൰"), None)
            if bstack1l1l1ll1l1_opy_:
                bstack1l1l1lll1l_opy_ = bstack1l1l1ll1l1_opy_ + bstack11l1ll_opy_ (u"ࠦ࠲ࠨ൱") + attrs.get(bstack11l1ll_opy_ (u"ࠬࡺࡹࡱࡧࠪ൲"), bstack11l1ll_opy_ (u"࠭ࠧ൳")).lower()
                self._1l1l111l11_opy_[bstack1l1l1lll1l_opy_][bstack11l1ll_opy_ (u"ࠧࡵࡧࡶࡸࡤࡪࡡࡵࡣࠪ൴")].stop(time=bstack1ll11111ll_opy_(), duration=int(attrs.get(bstack11l1ll_opy_ (u"ࠨࡧ࡯ࡥࡵࡹࡥࡥࡶ࡬ࡱࡪ࠭൵"), bstack11l1ll_opy_ (u"ࠩ࠳ࠫ൶"))), result=bstack1l1l111l1l_opy_)
                bstack11l1ll11_opy_.bstack1l1l1ll1ll_opy_(bstack11l1ll_opy_ (u"ࠪࡌࡴࡵ࡫ࡓࡷࡱࡊ࡮ࡴࡩࡴࡪࡨࡨࠬ൷"), self._1l1l111l11_opy_[bstack1l1l1lll1l_opy_][bstack11l1ll_opy_ (u"ࠫࡹ࡫ࡳࡵࡡࡧࡥࡹࡧࠧ൸")])
        else:
            bstack1l1l1ll1l1_opy_ = current_test_id if current_test_id else bstack11111l11_opy_(threading.current_thread(), bstack11l1ll_opy_ (u"ࠬࡩࡵࡳࡴࡨࡲࡹࡥࡨࡰࡱ࡮ࡣ࡮ࡪࠧ൹"), None)
            if bstack1l1l1ll1l1_opy_:
                current_step_uuid = bstack11111l11_opy_(threading.current_thread(), bstack11l1ll_opy_ (u"࠭ࡣࡶࡴࡵࡩࡳࡺ࡟ࡴࡶࡨࡴࡤࡻࡵࡪࡦࠪൺ"), None)
                self._1l1l111l11_opy_[bstack1l1l1ll1l1_opy_][bstack11l1ll_opy_ (u"ࠧࡵࡧࡶࡸࡤࡪࡡࡵࡣࠪൻ")].bstack1l11l11l1l_opy_(current_step_uuid, duration=int(attrs.get(bstack11l1ll_opy_ (u"ࠨࡧ࡯ࡥࡵࡹࡥࡥࡶ࡬ࡱࡪ࠭ർ"), bstack11l1ll_opy_ (u"ࠩ࠳ࠫൽ"))), result=bstack1l1l111l1l_opy_)
    def log_message(self, message):
        try:
            if message.get(bstack11l1ll_opy_ (u"ࠪ࡬ࡹࡳ࡬ࠨൾ"), bstack11l1ll_opy_ (u"ࠫࡳࡵࠧൿ")) == bstack11l1ll_opy_ (u"ࠬࡿࡥࡴࠩ඀"):
                return
            self.messages.push(message)
            bstack1l11l1l11l_opy_ = []
            if bstack11l1ll11_opy_.bstack1l1l1111l1_opy_():
                bstack1l11l1l11l_opy_.append({
                    bstack11l1ll_opy_ (u"࠭ࡴࡪ࡯ࡨࡷࡹࡧ࡭ࡱࠩඁ"): bstack1ll11111ll_opy_(),
                    bstack11l1ll_opy_ (u"ࠧ࡮ࡧࡶࡷࡦ࡭ࡥࠨං"): message.get(bstack11l1ll_opy_ (u"ࠨ࡯ࡨࡷࡸࡧࡧࡦࠩඃ")),
                    bstack11l1ll_opy_ (u"ࠩ࡯ࡩࡻ࡫࡬ࠨ඄"): message.get(bstack11l1ll_opy_ (u"ࠪࡰࡪࡼࡥ࡭ࠩඅ")),
                    **bstack11l1ll11_opy_.bstack1l1l1111l1_opy_()
                })
                if len(bstack1l11l1l11l_opy_) > 0:
                    bstack11l1ll11_opy_.bstack1l1l1l11ll_opy_(bstack1l11l1l11l_opy_)
        except Exception as err:
            pass
    def close(self):
        bstack11l1ll11_opy_.bstack1l1l111111_opy_()
    def _1l11lll11l_opy_(self):
        for bstack1l11l1ll11_opy_ in reversed(self._1l1l111l11_opy_):
            bstack1l1l111lll_opy_ = bstack1l11l1ll11_opy_
            data = self._1l1l111l11_opy_[bstack1l11l1ll11_opy_][bstack11l1ll_opy_ (u"ࠫࡹ࡫ࡳࡵࡡࡧࡥࡹࡧࠧආ")]
            if isinstance(data, bstack1l11ll1ll1_opy_):
                if not bstack11l1ll_opy_ (u"ࠬࡋࡁࡄࡊࠪඇ") in data.bstack1l1l1111ll_opy_():
                    return bstack1l1l111lll_opy_
            else:
                return bstack1l1l111lll_opy_
    def _1l11ll11l1_opy_(self, messages):
        try:
            bstack1l1l11111l_opy_ = BuiltIn().get_variable_value(bstack11l1ll_opy_ (u"ࠨࠤࡼࡎࡒࡋࠥࡒࡅࡗࡇࡏࢁࠧඈ")) in (bstack1l1l11l1ll_opy_.DEBUG, bstack1l1l11l1ll_opy_.TRACE)
            for message, bstack1l11ll1l11_opy_ in zip_longest(messages, messages[1:]):
                name = message.get(bstack11l1ll_opy_ (u"ࠧ࡮ࡧࡶࡷࡦ࡭ࡥࠨඉ"))
                level = message.get(bstack11l1ll_opy_ (u"ࠨ࡮ࡨࡺࡪࡲࠧඊ"))
                if level == bstack1l1l11l1ll_opy_.FAIL:
                    self._1l1l11ll11_opy_ = name or self._1l1l11ll11_opy_
                    self._1l11l1lll1_opy_ = bstack1l11ll1l11_opy_.get(bstack11l1ll_opy_ (u"ࠤࡰࡩࡸࡹࡡࡨࡧࠥඋ")) if bstack1l1l11111l_opy_ and bstack1l11ll1l11_opy_ else self._1l11l1lll1_opy_
        except:
            pass
    @classmethod
    def bstack1l1l1ll1ll_opy_(self, event: str, bstack1l11l1l111_opy_: bstack1l11llllll_opy_, bstack1l11lll1l1_opy_=False):
        if event == bstack11l1ll_opy_ (u"ࠪࡘࡪࡹࡴࡓࡷࡱࡊ࡮ࡴࡩࡴࡪࡨࡨࠬඌ"):
            bstack1l11l1l111_opy_.set(hooks=self.store[bstack11l1ll_opy_ (u"ࠫࡹ࡫ࡳࡵࡡ࡫ࡳࡴࡱࡳࠨඍ")])
        if event == bstack11l1ll_opy_ (u"࡚ࠬࡥࡴࡶࡕࡹࡳ࡙࡫ࡪࡲࡳࡩࡩ࠭ඎ"):
            event = bstack11l1ll_opy_ (u"࠭ࡔࡦࡵࡷࡖࡺࡴࡆࡪࡰ࡬ࡷ࡭࡫ࡤࠨඏ")
        if bstack1l11lll1l1_opy_:
            bstack1l1l1lll11_opy_ = {
                bstack11l1ll_opy_ (u"ࠧࡦࡸࡨࡲࡹࡥࡴࡺࡲࡨࠫඐ"): event,
                bstack1l11l1l111_opy_.bstack1l11l1llll_opy_(): bstack1l11l1l111_opy_.bstack1l11llll11_opy_(event)
            }
            self.bstack1l11ll11ll_opy_.append(bstack1l1l1lll11_opy_)
        else:
            bstack11l1ll11_opy_.bstack1l1l1ll1ll_opy_(event, bstack1l11l1l111_opy_)
class Messages:
    def __init__(self):
        self._1l11lll111_opy_ = []
    def bstack1l1l11l11l_opy_(self):
        self._1l11lll111_opy_.append([])
    def bstack1l1l1l1ll1_opy_(self):
        return self._1l11lll111_opy_.pop() if self._1l11lll111_opy_ else list()
    def push(self, message):
        self._1l11lll111_opy_[-1].append(message) if self._1l11lll111_opy_ else self._1l11lll111_opy_.append([message])
class bstack1l1l11l1ll_opy_:
    FAIL = bstack11l1ll_opy_ (u"ࠨࡈࡄࡍࡑ࠭එ")
    ERROR = bstack11l1ll_opy_ (u"ࠩࡈࡖࡗࡕࡒࠨඒ")
    WARNING = bstack11l1ll_opy_ (u"࡛ࠪࡆࡘࡎࠨඓ")
    bstack1l11ll1111_opy_ = bstack11l1ll_opy_ (u"ࠫࡎࡔࡆࡐࠩඔ")
    DEBUG = bstack11l1ll_opy_ (u"ࠬࡊࡅࡃࡗࡊࠫඕ")
    TRACE = bstack11l1ll_opy_ (u"࠭ࡔࡓࡃࡆࡉࠬඖ")
    bstack1l1l1l1l1l_opy_ = [FAIL, ERROR]
def bstack1l11ll1l1l_opy_(bstack1l1l1l1l11_opy_):
    if not bstack1l1l1l1l11_opy_:
        return None
    if bstack1l1l1l1l11_opy_.get(bstack11l1ll_opy_ (u"ࠧࡵࡧࡶࡸࡤࡪࡡࡵࡣࠪ඗"), None):
        return getattr(bstack1l1l1l1l11_opy_[bstack11l1ll_opy_ (u"ࠨࡶࡨࡷࡹࡥࡤࡢࡶࡤࠫ඘")], bstack11l1ll_opy_ (u"ࠩࡸࡹ࡮ࡪࠧ඙"), None)
    return bstack1l1l1l1l11_opy_.get(bstack11l1ll_opy_ (u"ࠪࡹࡺ࡯ࡤࠨක"), None)
def bstack1l1l11ll1l_opy_(hook_type, current_test_uuid):
    if hook_type.lower() not in [bstack11l1ll_opy_ (u"ࠫࡸ࡫ࡴࡶࡲࠪඛ"), bstack11l1ll_opy_ (u"ࠬࡺࡥࡢࡴࡧࡳࡼࡴࠧග")]:
        return
    if hook_type.lower() == bstack11l1ll_opy_ (u"࠭ࡳࡦࡶࡸࡴࠬඝ"):
        if current_test_uuid is None:
            return bstack11l1ll_opy_ (u"ࠧࡃࡇࡉࡓࡗࡋ࡟ࡂࡎࡏࠫඞ")
        else:
            return bstack11l1ll_opy_ (u"ࠨࡄࡈࡊࡔࡘࡅࡠࡇࡄࡇࡍ࠭ඟ")
    elif hook_type.lower() == bstack11l1ll_opy_ (u"ࠩࡷࡩࡦࡸࡤࡰࡹࡱࠫච"):
        if current_test_uuid is None:
            return bstack11l1ll_opy_ (u"ࠪࡅࡋ࡚ࡅࡓࡡࡄࡐࡑ࠭ඡ")
        else:
            return bstack11l1ll_opy_ (u"ࠫࡆࡌࡔࡆࡔࡢࡉࡆࡉࡈࠨජ")