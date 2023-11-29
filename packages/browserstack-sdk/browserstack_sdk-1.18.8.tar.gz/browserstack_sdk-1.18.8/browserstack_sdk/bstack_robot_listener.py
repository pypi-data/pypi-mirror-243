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
import datetime
import threading
from uuid import uuid4
from itertools import zip_longest
from collections import OrderedDict
from robot.libraries.BuiltIn import BuiltIn
from browserstack_sdk.bstack1l1l1lll1l_opy_ import RobotHandler
from bstack_utils.capture import bstack1l1ll1111l_opy_
from bstack_utils.bstack1l11l1l1ll_opy_ import bstack1l1l111111_opy_, bstack1l11ll1l11_opy_, bstack1l1l1llll1_opy_
from bstack_utils.bstack1l1ll111_opy_ import bstack1l11l11l_opy_
from bstack_utils.constants import *
from bstack_utils.helper import bstack1111l11l_opy_, bstack1llllll11l_opy_, Result, \
    bstack1l11ll1ll1_opy_
class bstack_robot_listener:
    ROBOT_LISTENER_API_VERSION = 2
    store = {
        bstack11l1l1l_opy_ (u"ࠬࡩࡵࡳࡴࡨࡲࡹࡥࡨࡰࡱ࡮ࡣࡺࡻࡩࡥࠩം"): [],
        bstack11l1l1l_opy_ (u"࠭ࡧ࡭ࡱࡥࡥࡱࡥࡨࡰࡱ࡮ࡷࠬഃ"): [],
        bstack11l1l1l_opy_ (u"ࠧࡵࡧࡶࡸࡤ࡮࡯ࡰ࡭ࡶࠫഄ"): []
    }
    bstack1l11l1l1l1_opy_ = []
    @staticmethod
    def bstack1l1l1ll1ll_opy_(log):
        if not (log[bstack11l1l1l_opy_ (u"ࠨ࡯ࡨࡷࡸࡧࡧࡦࠩഅ")] and log[bstack11l1l1l_opy_ (u"ࠩࡰࡩࡸࡹࡡࡨࡧࠪആ")].strip()):
            return
        active = bstack1l11l11l_opy_.bstack1l1l11l1l1_opy_()
        log = {
            bstack11l1l1l_opy_ (u"ࠪࡰࡪࡼࡥ࡭ࠩഇ"): log[bstack11l1l1l_opy_ (u"ࠫࡱ࡫ࡶࡦ࡮ࠪഈ")],
            bstack11l1l1l_opy_ (u"ࠬࡺࡩ࡮ࡧࡶࡸࡦࡳࡰࠨഉ"): datetime.datetime.utcnow().isoformat() + bstack11l1l1l_opy_ (u"࡚࠭ࠨഊ"),
            bstack11l1l1l_opy_ (u"ࠧ࡮ࡧࡶࡷࡦ࡭ࡥࠨഋ"): log[bstack11l1l1l_opy_ (u"ࠨ࡯ࡨࡷࡸࡧࡧࡦࠩഌ")],
        }
        if active:
            if active[bstack11l1l1l_opy_ (u"ࠩࡷࡽࡵ࡫ࠧ഍")] == bstack11l1l1l_opy_ (u"ࠪ࡬ࡴࡵ࡫ࠨഎ"):
                log[bstack11l1l1l_opy_ (u"ࠫ࡭ࡵ࡯࡬ࡡࡵࡹࡳࡥࡵࡶ࡫ࡧࠫഏ")] = active[bstack11l1l1l_opy_ (u"ࠬ࡮࡯ࡰ࡭ࡢࡶࡺࡴ࡟ࡶࡷ࡬ࡨࠬഐ")]
            elif active[bstack11l1l1l_opy_ (u"࠭ࡴࡺࡲࡨࠫ഑")] == bstack11l1l1l_opy_ (u"ࠧࡵࡧࡶࡸࠬഒ"):
                log[bstack11l1l1l_opy_ (u"ࠨࡶࡨࡷࡹࡥࡲࡶࡰࡢࡹࡺ࡯ࡤࠨഓ")] = active[bstack11l1l1l_opy_ (u"ࠩࡷࡩࡸࡺ࡟ࡳࡷࡱࡣࡺࡻࡩࡥࠩഔ")]
        bstack1l11l11l_opy_.bstack1l11llll1l_opy_([log])
    def __init__(self):
        self.messages = Messages()
        self._1l11lll1l1_opy_ = None
        self._1l11l1lll1_opy_ = None
        self._1l1ll11111_opy_ = OrderedDict()
        self.bstack1l1l1lll11_opy_ = bstack1l1ll1111l_opy_(self.bstack1l1l1ll1ll_opy_)
    @bstack1l11ll1ll1_opy_(class_method=True)
    def start_suite(self, name, attrs):
        self.messages.bstack1l11l1ll11_opy_()
        if not self._1l1ll11111_opy_.get(attrs.get(bstack11l1l1l_opy_ (u"ࠪ࡭ࡩ࠭ക")), None):
            self._1l1ll11111_opy_[attrs.get(bstack11l1l1l_opy_ (u"ࠫ࡮ࡪࠧഖ"))] = {}
        bstack1l1l1l111l_opy_ = bstack1l1l1llll1_opy_(
                bstack1l1l1ll11l_opy_=attrs.get(bstack11l1l1l_opy_ (u"ࠬ࡯ࡤࠨഗ")),
                name=name,
                bstack1l1l1l1ll1_opy_=bstack1llllll11l_opy_(),
                file_path=os.path.relpath(attrs[bstack11l1l1l_opy_ (u"࠭ࡳࡰࡷࡵࡧࡪ࠭ഘ")], start=os.getcwd()) if attrs.get(bstack11l1l1l_opy_ (u"ࠧࡴࡱࡸࡶࡨ࡫ࠧങ")) != bstack11l1l1l_opy_ (u"ࠨࠩച") else bstack11l1l1l_opy_ (u"ࠩࠪഛ"),
                framework=bstack11l1l1l_opy_ (u"ࠪࡖࡴࡨ࡯ࡵࠩജ")
            )
        threading.current_thread().current_suite_id = attrs.get(bstack11l1l1l_opy_ (u"ࠫ࡮ࡪࠧഝ"), None)
        self._1l1ll11111_opy_[attrs.get(bstack11l1l1l_opy_ (u"ࠬ࡯ࡤࠨഞ"))][bstack11l1l1l_opy_ (u"࠭ࡴࡦࡵࡷࡣࡩࡧࡴࡢࠩട")] = bstack1l1l1l111l_opy_
    @bstack1l11ll1ll1_opy_(class_method=True)
    def end_suite(self, name, attrs):
        messages = self.messages.bstack1l11ll1lll_opy_()
        self._1l1l11ll11_opy_(messages)
        for bstack1l1l11111l_opy_ in self.bstack1l11l1l1l1_opy_:
            bstack1l1l11111l_opy_[bstack11l1l1l_opy_ (u"ࠧࡵࡧࡶࡸࡤࡸࡵ࡯ࠩഠ")][bstack11l1l1l_opy_ (u"ࠨࡪࡲࡳࡰࡹࠧഡ")].extend(self.store[bstack11l1l1l_opy_ (u"ࠩࡪࡰࡴࡨࡡ࡭ࡡ࡫ࡳࡴࡱࡳࠨഢ")])
            bstack1l11l11l_opy_.bstack1l1l1l1111_opy_(bstack1l1l11111l_opy_)
        self.bstack1l11l1l1l1_opy_ = []
        self.store[bstack11l1l1l_opy_ (u"ࠪ࡫ࡱࡵࡢࡢ࡮ࡢ࡬ࡴࡵ࡫ࡴࠩണ")] = []
    @bstack1l11ll1ll1_opy_(class_method=True)
    def start_test(self, name, attrs):
        self.bstack1l1l1lll11_opy_.start()
        if not self._1l1ll11111_opy_.get(attrs.get(bstack11l1l1l_opy_ (u"ࠫ࡮ࡪࠧത")), None):
            self._1l1ll11111_opy_[attrs.get(bstack11l1l1l_opy_ (u"ࠬ࡯ࡤࠨഥ"))] = {}
        driver = bstack1111l11l_opy_(threading.current_thread(), bstack11l1l1l_opy_ (u"࠭ࡢࡴࡶࡤࡧࡰ࡙ࡥࡴࡵ࡬ࡳࡳࡊࡲࡪࡸࡨࡶࠬദ"), None)
        bstack1l11l1l1ll_opy_ = bstack1l1l1llll1_opy_(
            bstack1l1l1ll11l_opy_=attrs.get(bstack11l1l1l_opy_ (u"ࠧࡪࡦࠪധ")),
            name=name,
            bstack1l1l1l1ll1_opy_=bstack1llllll11l_opy_(),
            file_path=os.path.relpath(attrs[bstack11l1l1l_opy_ (u"ࠨࡵࡲࡹࡷࡩࡥࠨന")], start=os.getcwd()),
            scope=RobotHandler.bstack1l1l1l1lll_opy_(attrs.get(bstack11l1l1l_opy_ (u"ࠩࡶࡳࡺࡸࡣࡦࠩഩ"), None)),
            framework=bstack11l1l1l_opy_ (u"ࠪࡖࡴࡨ࡯ࡵࠩപ"),
            tags=attrs[bstack11l1l1l_opy_ (u"ࠫࡹࡧࡧࡴࠩഫ")],
            hooks=self.store[bstack11l1l1l_opy_ (u"ࠬ࡭࡬ࡰࡤࡤࡰࡤ࡮࡯ࡰ࡭ࡶࠫബ")],
            bstack1l11lllll1_opy_=bstack1l11l11l_opy_.bstack1l1l1ll1l1_opy_(driver) if driver and driver.session_id else {},
            meta={},
            code=bstack11l1l1l_opy_ (u"ࠨࡻࡾࠢ࡟ࡲࠥࢁࡽࠣഭ").format(bstack11l1l1l_opy_ (u"ࠢࠡࠤമ").join(attrs[bstack11l1l1l_opy_ (u"ࠨࡶࡤ࡫ࡸ࠭യ")]), name) if attrs[bstack11l1l1l_opy_ (u"ࠩࡷࡥ࡬ࡹࠧര")] else name
        )
        self._1l1ll11111_opy_[attrs.get(bstack11l1l1l_opy_ (u"ࠪ࡭ࡩ࠭റ"))][bstack11l1l1l_opy_ (u"ࠫࡹ࡫ࡳࡵࡡࡧࡥࡹࡧࠧല")] = bstack1l11l1l1ll_opy_
        threading.current_thread().current_test_uuid = bstack1l11l1l1ll_opy_.bstack1l1l11l11l_opy_()
        threading.current_thread().current_test_id = attrs.get(bstack11l1l1l_opy_ (u"ࠬ࡯ࡤࠨള"), None)
        self.bstack1l11l1ll1l_opy_(bstack11l1l1l_opy_ (u"࠭ࡔࡦࡵࡷࡖࡺࡴࡓࡵࡣࡵࡸࡪࡪࠧഴ"), bstack1l11l1l1ll_opy_)
    @bstack1l11ll1ll1_opy_(class_method=True)
    def end_test(self, name, attrs):
        self.bstack1l1l1lll11_opy_.reset()
        bstack1l11lll111_opy_ = bstack1l11ll1111_opy_.get(attrs.get(bstack11l1l1l_opy_ (u"ࠧࡴࡶࡤࡸࡺࡹࠧവ")), bstack11l1l1l_opy_ (u"ࠨࡵ࡮࡭ࡵࡶࡥࡥࠩശ"))
        self._1l1ll11111_opy_[attrs.get(bstack11l1l1l_opy_ (u"ࠩ࡬ࡨࠬഷ"))][bstack11l1l1l_opy_ (u"ࠪࡸࡪࡹࡴࡠࡦࡤࡸࡦ࠭സ")].stop(time=bstack1llllll11l_opy_(), duration=int(attrs.get(bstack11l1l1l_opy_ (u"ࠫࡪࡲࡡࡱࡵࡨࡨࡹ࡯࡭ࡦࠩഹ"), bstack11l1l1l_opy_ (u"ࠬ࠶ࠧഺ"))), result=Result(result=bstack1l11lll111_opy_, exception=attrs.get(bstack11l1l1l_opy_ (u"࠭࡭ࡦࡵࡶࡥ࡬࡫഻ࠧ")), bstack1l1l1l1l11_opy_=[attrs.get(bstack11l1l1l_opy_ (u"ࠧ࡮ࡧࡶࡷࡦ࡭ࡥࠨ഼"))]))
        self.bstack1l11l1ll1l_opy_(bstack11l1l1l_opy_ (u"ࠨࡖࡨࡷࡹࡘࡵ࡯ࡈ࡬ࡲ࡮ࡹࡨࡦࡦࠪഽ"), self._1l1ll11111_opy_[attrs.get(bstack11l1l1l_opy_ (u"ࠩ࡬ࡨࠬാ"))][bstack11l1l1l_opy_ (u"ࠪࡸࡪࡹࡴࡠࡦࡤࡸࡦ࠭ി")], True)
        self.store[bstack11l1l1l_opy_ (u"ࠫࡹ࡫ࡳࡵࡡ࡫ࡳࡴࡱࡳࠨീ")] = []
        threading.current_thread().current_test_uuid = None
        threading.current_thread().current_test_id = None
    @bstack1l11ll1ll1_opy_(class_method=True)
    def start_keyword(self, name, attrs):
        self.messages.bstack1l11l1ll11_opy_()
        current_test_id = bstack1111l11l_opy_(threading.current_thread(), bstack11l1l1l_opy_ (u"ࠬࡩࡵࡳࡴࡨࡲࡹࡥࡴࡦࡵࡷࡣ࡮ࡪࠧു"), None)
        bstack1l1l1lllll_opy_ = current_test_id if bstack1111l11l_opy_(threading.current_thread(), bstack11l1l1l_opy_ (u"࠭ࡣࡶࡴࡵࡩࡳࡺ࡟ࡵࡧࡶࡸࡤ࡯ࡤࠨൂ"), None) else bstack1111l11l_opy_(threading.current_thread(), bstack11l1l1l_opy_ (u"ࠧࡤࡷࡵࡶࡪࡴࡴࡠࡵࡸ࡭ࡹ࡫࡟ࡪࡦࠪൃ"), None)
        if attrs.get(bstack11l1l1l_opy_ (u"ࠨࡶࡼࡴࡪ࠭ൄ"), bstack11l1l1l_opy_ (u"ࠩࠪ൅")).lower() in [bstack11l1l1l_opy_ (u"ࠪࡷࡪࡺࡵࡱࠩെ"), bstack11l1l1l_opy_ (u"ࠫࡹ࡫ࡡࡳࡦࡲࡻࡳ࠭േ")]:
            hook_type = bstack1l11l1l111_opy_(attrs.get(bstack11l1l1l_opy_ (u"ࠬࡺࡹࡱࡧࠪൈ")), bstack1111l11l_opy_(threading.current_thread(), bstack11l1l1l_opy_ (u"࠭ࡣࡶࡴࡵࡩࡳࡺ࡟ࡵࡧࡶࡸࡤࡻࡵࡪࡦࠪ൉"), None))
            bstack1l11ll11l1_opy_ = bstack1l11ll1l11_opy_(
                bstack1l1l1ll11l_opy_=bstack1l1l1lllll_opy_ + bstack11l1l1l_opy_ (u"ࠧ࠮ࠩൊ") + attrs.get(bstack11l1l1l_opy_ (u"ࠨࡶࡼࡴࡪ࠭ോ"), bstack11l1l1l_opy_ (u"ࠩࠪൌ")).lower(),
                name=bstack11l1l1l_opy_ (u"ࠪ࡟ࢀࢃ࡝ࠡࡽࢀ്ࠫ").format(hook_type, attrs.get(bstack11l1l1l_opy_ (u"ࠫࡰࡽ࡮ࡢ࡯ࡨࠫൎ"), bstack11l1l1l_opy_ (u"ࠬ࠭൏"))) if hook_type in [bstack11l1l1l_opy_ (u"࠭ࡂࡆࡈࡒࡖࡊࡥࡁࡍࡎࠪ൐"), bstack11l1l1l_opy_ (u"ࠧࡂࡈࡗࡉࡗࡥࡁࡍࡎࠪ൑")] else bstack11l1l1l_opy_ (u"ࠨࡽࢀࠫ൒").format(attrs.get(bstack11l1l1l_opy_ (u"ࠩ࡮ࡻࡳࡧ࡭ࡦࠩ൓"), bstack11l1l1l_opy_ (u"ࠪࠫൔ"))),
                bstack1l1l1l1ll1_opy_=bstack1llllll11l_opy_(),
                file_path=os.path.relpath(attrs.get(bstack11l1l1l_opy_ (u"ࠫࡸࡵࡵࡳࡥࡨࠫൕ")), start=os.getcwd()),
                framework=bstack11l1l1l_opy_ (u"ࠬࡘ࡯ࡣࡱࡷࠫൖ"),
                tags=attrs[bstack11l1l1l_opy_ (u"࠭ࡴࡢࡩࡶࠫൗ")],
                scope=RobotHandler.bstack1l1l1l1lll_opy_(attrs.get(bstack11l1l1l_opy_ (u"ࠧࡴࡱࡸࡶࡨ࡫ࠧ൘"), None)),
                hook_type=hook_type,
                meta={}
            )
            threading.current_thread().current_hook_uuid = bstack1l11ll11l1_opy_.bstack1l1l11l11l_opy_()
            threading.current_thread().current_hook_id = bstack1l1l1lllll_opy_ + bstack11l1l1l_opy_ (u"ࠨ࠯ࠪ൙") + attrs.get(bstack11l1l1l_opy_ (u"ࠩࡷࡽࡵ࡫ࠧ൚"), bstack11l1l1l_opy_ (u"ࠪࠫ൛")).lower()
            self.store[bstack11l1l1l_opy_ (u"ࠫࡨࡻࡲࡳࡧࡱࡸࡤ࡮࡯ࡰ࡭ࡢࡹࡺ࡯ࡤࠨ൜")] = [bstack1l11ll11l1_opy_.bstack1l1l11l11l_opy_()]
            if bstack1111l11l_opy_(threading.current_thread(), bstack11l1l1l_opy_ (u"ࠬࡩࡵࡳࡴࡨࡲࡹࡥࡴࡦࡵࡷࡣࡺࡻࡩࡥࠩ൝"), None):
                self.store[bstack11l1l1l_opy_ (u"࠭ࡴࡦࡵࡷࡣ࡭ࡵ࡯࡬ࡵࠪ൞")].append(bstack1l11ll11l1_opy_.bstack1l1l11l11l_opy_())
            else:
                self.store[bstack11l1l1l_opy_ (u"ࠧࡨ࡮ࡲࡦࡦࡲ࡟ࡩࡱࡲ࡯ࡸ࠭ൟ")].append(bstack1l11ll11l1_opy_.bstack1l1l11l11l_opy_())
            if bstack1l1l1lllll_opy_:
                self._1l1ll11111_opy_[bstack1l1l1lllll_opy_ + bstack11l1l1l_opy_ (u"ࠨ࠯ࠪൠ") + attrs.get(bstack11l1l1l_opy_ (u"ࠩࡷࡽࡵ࡫ࠧൡ"), bstack11l1l1l_opy_ (u"ࠪࠫൢ")).lower()] = { bstack11l1l1l_opy_ (u"ࠫࡹ࡫ࡳࡵࡡࡧࡥࡹࡧࠧൣ"): bstack1l11ll11l1_opy_ }
            bstack1l11l11l_opy_.bstack1l11l1ll1l_opy_(bstack11l1l1l_opy_ (u"ࠬࡎ࡯ࡰ࡭ࡕࡹࡳ࡙ࡴࡢࡴࡷࡩࡩ࠭൤"), bstack1l11ll11l1_opy_)
        else:
            bstack1l11ll1l1l_opy_ = {
                bstack11l1l1l_opy_ (u"࠭ࡩࡥࠩ൥"): uuid4().__str__(),
                bstack11l1l1l_opy_ (u"ࠧࡵࡧࡻࡸࠬ൦"): bstack11l1l1l_opy_ (u"ࠨࡽࢀࠤࢀࢃࠧ൧").format(attrs.get(bstack11l1l1l_opy_ (u"ࠩ࡮ࡻࡳࡧ࡭ࡦࠩ൨")), attrs.get(bstack11l1l1l_opy_ (u"ࠪࡥࡷ࡭ࡳࠨ൩"), bstack11l1l1l_opy_ (u"ࠫࠬ൪"))) if attrs.get(bstack11l1l1l_opy_ (u"ࠬࡧࡲࡨࡵࠪ൫"), []) else attrs.get(bstack11l1l1l_opy_ (u"࠭࡫ࡸࡰࡤࡱࡪ࠭൬")),
                bstack11l1l1l_opy_ (u"ࠧࡴࡶࡨࡴࡤࡧࡲࡨࡷࡰࡩࡳࡺࠧ൭"): attrs.get(bstack11l1l1l_opy_ (u"ࠨࡣࡵ࡫ࡸ࠭൮"), []),
                bstack11l1l1l_opy_ (u"ࠩࡶࡸࡦࡸࡴࡦࡦࡢࡥࡹ࠭൯"): bstack1llllll11l_opy_(),
                bstack11l1l1l_opy_ (u"ࠪࡶࡪࡹࡵ࡭ࡶࠪ൰"): bstack11l1l1l_opy_ (u"ࠫࡵ࡫࡮ࡥ࡫ࡱ࡫ࠬ൱"),
                bstack11l1l1l_opy_ (u"ࠬࡪࡥࡴࡥࡵ࡭ࡵࡺࡩࡰࡰࠪ൲"): attrs.get(bstack11l1l1l_opy_ (u"࠭ࡤࡰࡥࠪ൳"), bstack11l1l1l_opy_ (u"ࠧࠨ൴"))
            }
            if attrs.get(bstack11l1l1l_opy_ (u"ࠨ࡮࡬ࡦࡳࡧ࡭ࡦࠩ൵"), bstack11l1l1l_opy_ (u"ࠩࠪ൶")) != bstack11l1l1l_opy_ (u"ࠪࠫ൷"):
                bstack1l11ll1l1l_opy_[bstack11l1l1l_opy_ (u"ࠫࡰ࡫ࡹࡸࡱࡵࡨࠬ൸")] = attrs.get(bstack11l1l1l_opy_ (u"ࠬࡲࡩࡣࡰࡤࡱࡪ࠭൹"))
            threading.current_thread().current_step_uuid = bstack1l11ll1l1l_opy_[bstack11l1l1l_opy_ (u"࠭ࡩࡥࠩൺ")]
            self._1l1ll11111_opy_[self._1l1l111lll_opy_()][bstack11l1l1l_opy_ (u"ࠧࡵࡧࡶࡸࡤࡪࡡࡵࡣࠪൻ")].add_step(bstack1l11ll1l1l_opy_)
    @bstack1l11ll1ll1_opy_(class_method=True)
    def end_keyword(self, name, attrs):
        messages = self.messages.bstack1l11ll1lll_opy_()
        self._1l1l11ll11_opy_(messages)
        current_test_id = bstack1111l11l_opy_(threading.current_thread(), bstack11l1l1l_opy_ (u"ࠨࡥࡸࡶࡷ࡫࡮ࡵࡡࡷࡩࡸࡺ࡟ࡪࡦࠪർ"), None)
        bstack1l1l1lllll_opy_ = current_test_id if current_test_id else bstack1111l11l_opy_(threading.current_thread(), bstack11l1l1l_opy_ (u"ࠩࡦࡹࡷࡸࡥ࡯ࡶࡢࡷࡺ࡯ࡴࡦࡡ࡬ࡨࠬൽ"), None)
        bstack1l1l1l11ll_opy_ = bstack1l11ll1111_opy_.get(attrs.get(bstack11l1l1l_opy_ (u"ࠪࡷࡹࡧࡴࡶࡵࠪൾ")), bstack11l1l1l_opy_ (u"ࠫࡸࡱࡩࡱࡲࡨࡨࠬൿ"))
        bstack1l11l1llll_opy_ = attrs.get(bstack11l1l1l_opy_ (u"ࠬࡳࡥࡴࡵࡤ࡫ࡪ࠭඀"))
        if bstack1l1l1l11ll_opy_ != bstack11l1l1l_opy_ (u"࠭ࡳ࡬࡫ࡳࡴࡪࡪࠧඁ") and not attrs.get(bstack11l1l1l_opy_ (u"ࠧ࡮ࡧࡶࡷࡦ࡭ࡥࠨං")) and self._1l11lll1l1_opy_:
            bstack1l11l1llll_opy_ = self._1l11lll1l1_opy_
        bstack1l1l11l111_opy_ = Result(result=bstack1l1l1l11ll_opy_, exception=bstack1l11l1llll_opy_, bstack1l1l1l1l11_opy_=[bstack1l11l1llll_opy_])
        if attrs.get(bstack11l1l1l_opy_ (u"ࠨࡶࡼࡴࡪ࠭ඃ"), bstack11l1l1l_opy_ (u"ࠩࠪ඄")).lower() in [bstack11l1l1l_opy_ (u"ࠪࡷࡪࡺࡵࡱࠩඅ"), bstack11l1l1l_opy_ (u"ࠫࡹ࡫ࡡࡳࡦࡲࡻࡳ࠭ආ")]:
            bstack1l1l1lllll_opy_ = current_test_id if current_test_id else bstack1111l11l_opy_(threading.current_thread(), bstack11l1l1l_opy_ (u"ࠬࡩࡵࡳࡴࡨࡲࡹࡥࡳࡶ࡫ࡷࡩࡤ࡯ࡤࠨඇ"), None)
            if bstack1l1l1lllll_opy_:
                bstack1l1l111l1l_opy_ = bstack1l1l1lllll_opy_ + bstack11l1l1l_opy_ (u"ࠨ࠭ࠣඈ") + attrs.get(bstack11l1l1l_opy_ (u"ࠧࡵࡻࡳࡩࠬඉ"), bstack11l1l1l_opy_ (u"ࠨࠩඊ")).lower()
                self._1l1ll11111_opy_[bstack1l1l111l1l_opy_][bstack11l1l1l_opy_ (u"ࠩࡷࡩࡸࡺ࡟ࡥࡣࡷࡥࠬඋ")].stop(time=bstack1llllll11l_opy_(), duration=int(attrs.get(bstack11l1l1l_opy_ (u"ࠪࡩࡱࡧࡰࡴࡧࡧࡸ࡮ࡳࡥࠨඌ"), bstack11l1l1l_opy_ (u"ࠫ࠵࠭ඍ"))), result=bstack1l1l11l111_opy_)
                bstack1l11l11l_opy_.bstack1l11l1ll1l_opy_(bstack11l1l1l_opy_ (u"ࠬࡎ࡯ࡰ࡭ࡕࡹࡳࡌࡩ࡯࡫ࡶ࡬ࡪࡪࠧඎ"), self._1l1ll11111_opy_[bstack1l1l111l1l_opy_][bstack11l1l1l_opy_ (u"࠭ࡴࡦࡵࡷࡣࡩࡧࡴࡢࠩඏ")])
        else:
            bstack1l1l1lllll_opy_ = current_test_id if current_test_id else bstack1111l11l_opy_(threading.current_thread(), bstack11l1l1l_opy_ (u"ࠧࡤࡷࡵࡶࡪࡴࡴࡠࡪࡲࡳࡰࡥࡩࡥࠩඐ"), None)
            if bstack1l1l1lllll_opy_:
                current_step_uuid = bstack1111l11l_opy_(threading.current_thread(), bstack11l1l1l_opy_ (u"ࠨࡥࡸࡶࡷ࡫࡮ࡵࡡࡶࡸࡪࡶ࡟ࡶࡷ࡬ࡨࠬඑ"), None)
                self._1l1ll11111_opy_[bstack1l1l1lllll_opy_][bstack11l1l1l_opy_ (u"ࠩࡷࡩࡸࡺ࡟ࡥࡣࡷࡥࠬඒ")].bstack1l1l111l11_opy_(current_step_uuid, duration=int(attrs.get(bstack11l1l1l_opy_ (u"ࠪࡩࡱࡧࡰࡴࡧࡧࡸ࡮ࡳࡥࠨඓ"), bstack11l1l1l_opy_ (u"ࠫ࠵࠭ඔ"))), result=bstack1l1l11l111_opy_)
    def log_message(self, message):
        try:
            if message.get(bstack11l1l1l_opy_ (u"ࠬ࡮ࡴ࡮࡮ࠪඕ"), bstack11l1l1l_opy_ (u"࠭࡮ࡰࠩඖ")) == bstack11l1l1l_opy_ (u"ࠧࡺࡧࡶࠫ඗"):
                return
            self.messages.push(message)
            bstack1l1l1l1l1l_opy_ = []
            if bstack1l11l11l_opy_.bstack1l1l11l1l1_opy_():
                bstack1l1l1l1l1l_opy_.append({
                    bstack11l1l1l_opy_ (u"ࠨࡶ࡬ࡱࡪࡹࡴࡢ࡯ࡳࠫ඘"): bstack1llllll11l_opy_(),
                    bstack11l1l1l_opy_ (u"ࠩࡰࡩࡸࡹࡡࡨࡧࠪ඙"): message.get(bstack11l1l1l_opy_ (u"ࠪࡱࡪࡹࡳࡢࡩࡨࠫක")),
                    bstack11l1l1l_opy_ (u"ࠫࡱ࡫ࡶࡦ࡮ࠪඛ"): message.get(bstack11l1l1l_opy_ (u"ࠬࡲࡥࡷࡧ࡯ࠫග")),
                    **bstack1l11l11l_opy_.bstack1l1l11l1l1_opy_()
                })
                if len(bstack1l1l1l1l1l_opy_) > 0:
                    bstack1l11l11l_opy_.bstack1l11llll1l_opy_(bstack1l1l1l1l1l_opy_)
        except Exception as err:
            pass
    def close(self):
        bstack1l11l11l_opy_.bstack1l1l1l11l1_opy_()
    def _1l1l111lll_opy_(self):
        for bstack1l1l1ll11l_opy_ in reversed(self._1l1ll11111_opy_):
            bstack1l1l11l1ll_opy_ = bstack1l1l1ll11l_opy_
            data = self._1l1ll11111_opy_[bstack1l1l1ll11l_opy_][bstack11l1l1l_opy_ (u"࠭ࡴࡦࡵࡷࡣࡩࡧࡴࡢࠩඝ")]
            if isinstance(data, bstack1l11ll1l11_opy_):
                if not bstack11l1l1l_opy_ (u"ࠧࡆࡃࡆࡌࠬඞ") in data.bstack1l1l11ll1l_opy_():
                    return bstack1l1l11l1ll_opy_
            else:
                return bstack1l1l11l1ll_opy_
    def _1l1l11ll11_opy_(self, messages):
        try:
            bstack1l1l1111ll_opy_ = BuiltIn().get_variable_value(bstack11l1l1l_opy_ (u"ࠣࠦࡾࡐࡔࡍࠠࡍࡇ࡙ࡉࡑࢃࠢඟ")) in (bstack1l11llllll_opy_.DEBUG, bstack1l11llllll_opy_.TRACE)
            for message, bstack1l11lll1ll_opy_ in zip_longest(messages, messages[1:]):
                name = message.get(bstack11l1l1l_opy_ (u"ࠩࡰࡩࡸࡹࡡࡨࡧࠪච"))
                level = message.get(bstack11l1l1l_opy_ (u"ࠪࡰࡪࡼࡥ࡭ࠩඡ"))
                if level == bstack1l11llllll_opy_.FAIL:
                    self._1l11lll1l1_opy_ = name or self._1l11lll1l1_opy_
                    self._1l11l1lll1_opy_ = bstack1l11lll1ll_opy_.get(bstack11l1l1l_opy_ (u"ࠦࡲ࡫ࡳࡴࡣࡪࡩࠧජ")) if bstack1l1l1111ll_opy_ and bstack1l11lll1ll_opy_ else self._1l11l1lll1_opy_
        except:
            pass
    @classmethod
    def bstack1l11l1ll1l_opy_(self, event: str, bstack1l1l11lll1_opy_: bstack1l1l111111_opy_, bstack1l11lll11l_opy_=False):
        if event == bstack11l1l1l_opy_ (u"࡚ࠬࡥࡴࡶࡕࡹࡳࡌࡩ࡯࡫ࡶ࡬ࡪࡪࠧඣ"):
            bstack1l1l11lll1_opy_.set(hooks=self.store[bstack11l1l1l_opy_ (u"࠭ࡴࡦࡵࡷࡣ࡭ࡵ࡯࡬ࡵࠪඤ")])
        if event == bstack11l1l1l_opy_ (u"ࠧࡕࡧࡶࡸࡗࡻ࡮ࡔ࡭࡬ࡴࡵ࡫ࡤࠨඥ"):
            event = bstack11l1l1l_opy_ (u"ࠨࡖࡨࡷࡹࡘࡵ࡯ࡈ࡬ࡲ࡮ࡹࡨࡦࡦࠪඦ")
        if bstack1l11lll11l_opy_:
            bstack1l1l1ll111_opy_ = {
                bstack11l1l1l_opy_ (u"ࠩࡨࡺࡪࡴࡴࡠࡶࡼࡴࡪ࠭ට"): event,
                bstack1l1l11lll1_opy_.bstack1l11l1l11l_opy_(): bstack1l1l11lll1_opy_.bstack1l1l11llll_opy_(event)
            }
            self.bstack1l11l1l1l1_opy_.append(bstack1l1l1ll111_opy_)
        else:
            bstack1l11l11l_opy_.bstack1l11l1ll1l_opy_(event, bstack1l1l11lll1_opy_)
class Messages:
    def __init__(self):
        self._1l11ll111l_opy_ = []
    def bstack1l11l1ll11_opy_(self):
        self._1l11ll111l_opy_.append([])
    def bstack1l11ll1lll_opy_(self):
        return self._1l11ll111l_opy_.pop() if self._1l11ll111l_opy_ else list()
    def push(self, message):
        self._1l11ll111l_opy_[-1].append(message) if self._1l11ll111l_opy_ else self._1l11ll111l_opy_.append([message])
class bstack1l11llllll_opy_:
    FAIL = bstack11l1l1l_opy_ (u"ࠪࡊࡆࡏࡌࠨඨ")
    ERROR = bstack11l1l1l_opy_ (u"ࠫࡊࡘࡒࡐࡔࠪඩ")
    WARNING = bstack11l1l1l_opy_ (u"ࠬ࡝ࡁࡓࡐࠪඪ")
    bstack1l11ll11ll_opy_ = bstack11l1l1l_opy_ (u"࠭ࡉࡏࡈࡒࠫණ")
    DEBUG = bstack11l1l1l_opy_ (u"ࠧࡅࡇࡅ࡙ࡌ࠭ඬ")
    TRACE = bstack11l1l1l_opy_ (u"ࠨࡖࡕࡅࡈࡋࠧත")
    bstack1l1l1111l1_opy_ = [FAIL, ERROR]
def bstack1l11llll11_opy_(bstack1l1l111ll1_opy_):
    if not bstack1l1l111ll1_opy_:
        return None
    if bstack1l1l111ll1_opy_.get(bstack11l1l1l_opy_ (u"ࠩࡷࡩࡸࡺ࡟ࡥࡣࡷࡥࠬථ"), None):
        return getattr(bstack1l1l111ll1_opy_[bstack11l1l1l_opy_ (u"ࠪࡸࡪࡹࡴࡠࡦࡤࡸࡦ࠭ද")], bstack11l1l1l_opy_ (u"ࠫࡺࡻࡩࡥࠩධ"), None)
    return bstack1l1l111ll1_opy_.get(bstack11l1l1l_opy_ (u"ࠬࡻࡵࡪࡦࠪන"), None)
def bstack1l11l1l111_opy_(hook_type, current_test_uuid):
    if hook_type.lower() not in [bstack11l1l1l_opy_ (u"࠭ࡳࡦࡶࡸࡴࠬ඲"), bstack11l1l1l_opy_ (u"ࠧࡵࡧࡤࡶࡩࡵࡷ࡯ࠩඳ")]:
        return
    if hook_type.lower() == bstack11l1l1l_opy_ (u"ࠨࡵࡨࡸࡺࡶࠧප"):
        if current_test_uuid is None:
            return bstack11l1l1l_opy_ (u"ࠩࡅࡉࡋࡕࡒࡆࡡࡄࡐࡑ࠭ඵ")
        else:
            return bstack11l1l1l_opy_ (u"ࠪࡆࡊࡌࡏࡓࡇࡢࡉࡆࡉࡈࠨබ")
    elif hook_type.lower() == bstack11l1l1l_opy_ (u"ࠫࡹ࡫ࡡࡳࡦࡲࡻࡳ࠭භ"):
        if current_test_uuid is None:
            return bstack11l1l1l_opy_ (u"ࠬࡇࡆࡕࡇࡕࡣࡆࡒࡌࠨම")
        else:
            return bstack11l1l1l_opy_ (u"࠭ࡁࡇࡖࡈࡖࡤࡋࡁࡄࡊࠪඹ")