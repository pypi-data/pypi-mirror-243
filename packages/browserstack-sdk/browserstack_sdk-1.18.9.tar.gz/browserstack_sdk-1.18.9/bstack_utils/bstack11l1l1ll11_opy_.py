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
from _pytest import fixtures
from _pytest.python import _call_with_optional_argument
from pytest import Module, Class
from bstack_utils.helper import Result
def _11l1ll1l11_opy_(method, this, arg):
    arg_count = method.__code__.co_argcount
    if arg_count > 1:
        method(this, arg)
    else:
        method(this)
class bstack11l1lll111_opy_:
    def __init__(self, handler):
        self._11l1l1lll1_opy_ = {}
        self._11l1lll1l1_opy_ = {}
        self.handler = handler
        self.patch()
        pass
    def patch(self):
        self._11l1l1lll1_opy_[bstack11l1ll_opy_ (u"ࠩࡩࡹࡳࡩࡴࡪࡱࡱࡣ࡫࡯ࡸࡵࡷࡵࡩࠬቍ")] = Module._inject_setup_function_fixture
        self._11l1l1lll1_opy_[bstack11l1ll_opy_ (u"ࠪࡱࡴࡪࡵ࡭ࡧࡢࡪ࡮ࡾࡴࡶࡴࡨࠫ቎")] = Module._inject_setup_module_fixture
        self._11l1l1lll1_opy_[bstack11l1ll_opy_ (u"ࠫࡨࡲࡡࡴࡵࡢࡪ࡮ࡾࡴࡶࡴࡨࠫ቏")] = Class._inject_setup_class_fixture
        self._11l1l1lll1_opy_[bstack11l1ll_opy_ (u"ࠬࡳࡥࡵࡪࡲࡨࡤ࡬ࡩࡹࡶࡸࡶࡪ࠭ቐ")] = Class._inject_setup_method_fixture
        Module._inject_setup_function_fixture = self.bstack11l1ll111l_opy_(bstack11l1ll_opy_ (u"࠭ࡦࡶࡰࡦࡸ࡮ࡵ࡮ࡠࡨ࡬ࡼࡹࡻࡲࡦࠩቑ"))
        Module._inject_setup_module_fixture = self.bstack11l1ll111l_opy_(bstack11l1ll_opy_ (u"ࠧ࡮ࡱࡧࡹࡱ࡫࡟ࡧ࡫ࡻࡸࡺࡸࡥࠨቒ"))
        Class._inject_setup_class_fixture = self.bstack11l1ll111l_opy_(bstack11l1ll_opy_ (u"ࠨࡥ࡯ࡥࡸࡹ࡟ࡧ࡫ࡻࡸࡺࡸࡥࠨቓ"))
        Class._inject_setup_method_fixture = self.bstack11l1ll111l_opy_(bstack11l1ll_opy_ (u"ࠩࡰࡩࡹ࡮࡯ࡥࡡࡩ࡭ࡽࡺࡵࡳࡧࠪቔ"))
    def bstack11l1l1llll_opy_(self, bstack11l1ll1111_opy_, hook_type):
        meth = getattr(bstack11l1ll1111_opy_, hook_type, None)
        if meth is not None and fixtures.getfixturemarker(meth) is None:
            self._11l1lll1l1_opy_[hook_type] = meth
            setattr(bstack11l1ll1111_opy_, hook_type, self.bstack11l1ll11ll_opy_(hook_type))
    def bstack11l1ll11l1_opy_(self, instance, bstack11l1ll1lll_opy_):
        if bstack11l1ll1lll_opy_ == bstack11l1ll_opy_ (u"ࠥࡪࡺࡴࡣࡵ࡫ࡲࡲࡤ࡬ࡩࡹࡶࡸࡶࡪࠨቕ"):
            self.bstack11l1l1llll_opy_(instance.obj, bstack11l1ll_opy_ (u"ࠦࡸ࡫ࡴࡶࡲࡢࡪࡺࡴࡣࡵ࡫ࡲࡲࠧቖ"))
            self.bstack11l1l1llll_opy_(instance.obj, bstack11l1ll_opy_ (u"ࠧࡺࡥࡢࡴࡧࡳࡼࡴ࡟ࡧࡷࡱࡧࡹ࡯࡯࡯ࠤ቗"))
        if bstack11l1ll1lll_opy_ == bstack11l1ll_opy_ (u"ࠨ࡭ࡰࡦࡸࡰࡪࡥࡦࡪࡺࡷࡹࡷ࡫ࠢቘ"):
            self.bstack11l1l1llll_opy_(instance.obj, bstack11l1ll_opy_ (u"ࠢࡴࡧࡷࡹࡵࡥ࡭ࡰࡦࡸࡰࡪࠨ቙"))
            self.bstack11l1l1llll_opy_(instance.obj, bstack11l1ll_opy_ (u"ࠣࡶࡨࡥࡷࡪ࡯ࡸࡰࡢࡱࡴࡪࡵ࡭ࡧࠥቚ"))
        if bstack11l1ll1lll_opy_ == bstack11l1ll_opy_ (u"ࠤࡦࡰࡦࡹࡳࡠࡨ࡬ࡼࡹࡻࡲࡦࠤቛ"):
            self.bstack11l1l1llll_opy_(instance.obj, bstack11l1ll_opy_ (u"ࠥࡷࡪࡺࡵࡱࡡࡦࡰࡦࡹࡳࠣቜ"))
            self.bstack11l1l1llll_opy_(instance.obj, bstack11l1ll_opy_ (u"ࠦࡹ࡫ࡡࡳࡦࡲࡻࡳࡥࡣ࡭ࡣࡶࡷࠧቝ"))
        if bstack11l1ll1lll_opy_ == bstack11l1ll_opy_ (u"ࠧࡳࡥࡵࡪࡲࡨࡤ࡬ࡩࡹࡶࡸࡶࡪࠨ቞"):
            self.bstack11l1l1llll_opy_(instance.obj, bstack11l1ll_opy_ (u"ࠨࡳࡦࡶࡸࡴࡤࡳࡥࡵࡪࡲࡨࠧ቟"))
            self.bstack11l1l1llll_opy_(instance.obj, bstack11l1ll_opy_ (u"ࠢࡵࡧࡤࡶࡩࡵࡷ࡯ࡡࡰࡩࡹ࡮࡯ࡥࠤበ"))
    @staticmethod
    def bstack11l1ll1ll1_opy_(hook_type, func, args):
        if hook_type in [bstack11l1ll_opy_ (u"ࠨࡵࡨࡸࡺࡶ࡟࡮ࡧࡷ࡬ࡴࡪࠧቡ"), bstack11l1ll_opy_ (u"ࠩࡷࡩࡦࡸࡤࡰࡹࡱࡣࡲ࡫ࡴࡩࡱࡧࠫቢ")]:
            _11l1ll1l11_opy_(func, args[0], args[1])
            return
        _call_with_optional_argument(func, args[0])
    def bstack11l1ll11ll_opy_(self, hook_type):
        def bstack11l1ll1l1l_opy_(arg=None):
            self.handler(hook_type, bstack11l1ll_opy_ (u"ࠪࡦࡪ࡬࡯ࡳࡧࠪባ"))
            result = None
            exception = None
            try:
                self.bstack11l1ll1ll1_opy_(hook_type, self._11l1lll1l1_opy_[hook_type], (arg,))
                result = Result(result=bstack11l1ll_opy_ (u"ࠫࡵࡧࡳࡴࡧࡧࠫቤ"))
            except Exception as e:
                result = Result(result=bstack11l1ll_opy_ (u"ࠬ࡬ࡡࡪ࡮ࡨࡨࠬብ"), exception=e)
                self.handler(hook_type, bstack11l1ll_opy_ (u"࠭ࡡࡧࡶࡨࡶࠬቦ"), result)
                raise e.with_traceback(e.__traceback__)
            self.handler(hook_type, bstack11l1ll_opy_ (u"ࠧࡢࡨࡷࡩࡷ࠭ቧ"), result)
        def bstack11l1l1ll1l_opy_(this, arg=None):
            self.handler(hook_type, bstack11l1ll_opy_ (u"ࠨࡤࡨࡪࡴࡸࡥࠨቨ"))
            result = None
            exception = None
            try:
                self.bstack11l1ll1ll1_opy_(hook_type, self._11l1lll1l1_opy_[hook_type], (this, arg))
                result = Result(result=bstack11l1ll_opy_ (u"ࠩࡳࡥࡸࡹࡥࡥࠩቩ"))
            except Exception as e:
                result = Result(result=bstack11l1ll_opy_ (u"ࠪࡪࡦ࡯࡬ࡦࡦࠪቪ"), exception=e)
                self.handler(hook_type, bstack11l1ll_opy_ (u"ࠫࡦ࡬ࡴࡦࡴࠪቫ"), result)
                raise e.with_traceback(e.__traceback__)
            self.handler(hook_type, bstack11l1ll_opy_ (u"ࠬࡧࡦࡵࡧࡵࠫቬ"), result)
        if hook_type in [bstack11l1ll_opy_ (u"࠭ࡳࡦࡶࡸࡴࡤࡳࡥࡵࡪࡲࡨࠬቭ"), bstack11l1ll_opy_ (u"ࠧࡵࡧࡤࡶࡩࡵࡷ࡯ࡡࡰࡩࡹ࡮࡯ࡥࠩቮ")]:
            return bstack11l1l1ll1l_opy_
        return bstack11l1ll1l1l_opy_
    def bstack11l1ll111l_opy_(self, bstack11l1ll1lll_opy_):
        def bstack11l1lll11l_opy_(this, *args, **kwargs):
            self.bstack11l1ll11l1_opy_(this, bstack11l1ll1lll_opy_)
            self._11l1l1lll1_opy_[bstack11l1ll1lll_opy_](this, *args, **kwargs)
        return bstack11l1lll11l_opy_