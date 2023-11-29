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
class bstack11l1ll11ll_opy_:
    def __init__(self, handler):
        self._11l1ll1ll1_opy_ = {}
        self._11l1ll111l_opy_ = {}
        self.handler = handler
        self.patch()
        pass
    def patch(self):
        self._11l1ll1ll1_opy_[bstack11l1l1l_opy_ (u"࠭ࡦࡶࡰࡦࡸ࡮ࡵ࡮ࡠࡨ࡬ࡼࡹࡻࡲࡦࠩ቟")] = Module._inject_setup_function_fixture
        self._11l1ll1ll1_opy_[bstack11l1l1l_opy_ (u"ࠧ࡮ࡱࡧࡹࡱ࡫࡟ࡧ࡫ࡻࡸࡺࡸࡥࠨበ")] = Module._inject_setup_module_fixture
        self._11l1ll1ll1_opy_[bstack11l1l1l_opy_ (u"ࠨࡥ࡯ࡥࡸࡹ࡟ࡧ࡫ࡻࡸࡺࡸࡥࠨቡ")] = Class._inject_setup_class_fixture
        self._11l1ll1ll1_opy_[bstack11l1l1l_opy_ (u"ࠩࡰࡩࡹ࡮࡯ࡥࡡࡩ࡭ࡽࡺࡵࡳࡧࠪቢ")] = Class._inject_setup_method_fixture
        Module._inject_setup_function_fixture = self.bstack11l1lll1l1_opy_(bstack11l1l1l_opy_ (u"ࠪࡪࡺࡴࡣࡵ࡫ࡲࡲࡤ࡬ࡩࡹࡶࡸࡶࡪ࠭ባ"))
        Module._inject_setup_module_fixture = self.bstack11l1lll1l1_opy_(bstack11l1l1l_opy_ (u"ࠫࡲࡵࡤࡶ࡮ࡨࡣ࡫࡯ࡸࡵࡷࡵࡩࠬቤ"))
        Class._inject_setup_class_fixture = self.bstack11l1lll1l1_opy_(bstack11l1l1l_opy_ (u"ࠬࡩ࡬ࡢࡵࡶࡣ࡫࡯ࡸࡵࡷࡵࡩࠬብ"))
        Class._inject_setup_method_fixture = self.bstack11l1lll1l1_opy_(bstack11l1l1l_opy_ (u"࠭࡭ࡦࡶ࡫ࡳࡩࡥࡦࡪࡺࡷࡹࡷ࡫ࠧቦ"))
    def bstack11l1llll1l_opy_(self, bstack11l1lllll1_opy_, hook_type):
        meth = getattr(bstack11l1lllll1_opy_, hook_type, None)
        if meth is not None and fixtures.getfixturemarker(meth) is None:
            self._11l1ll111l_opy_[hook_type] = meth
            setattr(bstack11l1lllll1_opy_, hook_type, self.bstack11l1ll1111_opy_(hook_type))
    def bstack11l1llll11_opy_(self, instance, bstack11l1ll11l1_opy_):
        if bstack11l1ll11l1_opy_ == bstack11l1l1l_opy_ (u"ࠢࡧࡷࡱࡧࡹ࡯࡯࡯ࡡࡩ࡭ࡽࡺࡵࡳࡧࠥቧ"):
            self.bstack11l1llll1l_opy_(instance.obj, bstack11l1l1l_opy_ (u"ࠣࡵࡨࡸࡺࡶ࡟ࡧࡷࡱࡧࡹ࡯࡯࡯ࠤቨ"))
            self.bstack11l1llll1l_opy_(instance.obj, bstack11l1l1l_opy_ (u"ࠤࡷࡩࡦࡸࡤࡰࡹࡱࡣ࡫ࡻ࡮ࡤࡶ࡬ࡳࡳࠨቩ"))
        if bstack11l1ll11l1_opy_ == bstack11l1l1l_opy_ (u"ࠥࡱࡴࡪࡵ࡭ࡧࡢࡪ࡮ࡾࡴࡶࡴࡨࠦቪ"):
            self.bstack11l1llll1l_opy_(instance.obj, bstack11l1l1l_opy_ (u"ࠦࡸ࡫ࡴࡶࡲࡢࡱࡴࡪࡵ࡭ࡧࠥቫ"))
            self.bstack11l1llll1l_opy_(instance.obj, bstack11l1l1l_opy_ (u"ࠧࡺࡥࡢࡴࡧࡳࡼࡴ࡟࡮ࡱࡧࡹࡱ࡫ࠢቬ"))
        if bstack11l1ll11l1_opy_ == bstack11l1l1l_opy_ (u"ࠨࡣ࡭ࡣࡶࡷࡤ࡬ࡩࡹࡶࡸࡶࡪࠨቭ"):
            self.bstack11l1llll1l_opy_(instance.obj, bstack11l1l1l_opy_ (u"ࠢࡴࡧࡷࡹࡵࡥࡣ࡭ࡣࡶࡷࠧቮ"))
            self.bstack11l1llll1l_opy_(instance.obj, bstack11l1l1l_opy_ (u"ࠣࡶࡨࡥࡷࡪ࡯ࡸࡰࡢࡧࡱࡧࡳࡴࠤቯ"))
        if bstack11l1ll11l1_opy_ == bstack11l1l1l_opy_ (u"ࠤࡰࡩࡹ࡮࡯ࡥࡡࡩ࡭ࡽࡺࡵࡳࡧࠥተ"):
            self.bstack11l1llll1l_opy_(instance.obj, bstack11l1l1l_opy_ (u"ࠥࡷࡪࡺࡵࡱࡡࡰࡩࡹ࡮࡯ࡥࠤቱ"))
            self.bstack11l1llll1l_opy_(instance.obj, bstack11l1l1l_opy_ (u"ࠦࡹ࡫ࡡࡳࡦࡲࡻࡳࡥ࡭ࡦࡶ࡫ࡳࡩࠨቲ"))
    @staticmethod
    def bstack11l1lll111_opy_(hook_type, func, args):
        if hook_type in [bstack11l1l1l_opy_ (u"ࠬࡹࡥࡵࡷࡳࡣࡲ࡫ࡴࡩࡱࡧࠫታ"), bstack11l1l1l_opy_ (u"࠭ࡴࡦࡣࡵࡨࡴࡽ࡮ࡠ࡯ࡨࡸ࡭ࡵࡤࠨቴ")]:
            _11l1ll1l11_opy_(func, args[0], args[1])
            return
        _call_with_optional_argument(func, args[0])
    def bstack11l1ll1111_opy_(self, hook_type):
        def bstack11l1ll1lll_opy_(arg=None):
            self.handler(hook_type, bstack11l1l1l_opy_ (u"ࠧࡣࡧࡩࡳࡷ࡫ࠧት"))
            result = None
            exception = None
            try:
                self.bstack11l1lll111_opy_(hook_type, self._11l1ll111l_opy_[hook_type], (arg,))
                result = Result(result=bstack11l1l1l_opy_ (u"ࠨࡲࡤࡷࡸ࡫ࡤࠨቶ"))
            except Exception as e:
                result = Result(result=bstack11l1l1l_opy_ (u"ࠩࡩࡥ࡮ࡲࡥࡥࠩቷ"), exception=e)
                self.handler(hook_type, bstack11l1l1l_opy_ (u"ࠪࡥ࡫ࡺࡥࡳࠩቸ"), result)
                raise e.with_traceback(e.__traceback__)
            self.handler(hook_type, bstack11l1l1l_opy_ (u"ࠫࡦ࡬ࡴࡦࡴࠪቹ"), result)
        def bstack11l1ll1l1l_opy_(this, arg=None):
            self.handler(hook_type, bstack11l1l1l_opy_ (u"ࠬࡨࡥࡧࡱࡵࡩࠬቺ"))
            result = None
            exception = None
            try:
                self.bstack11l1lll111_opy_(hook_type, self._11l1ll111l_opy_[hook_type], (this, arg))
                result = Result(result=bstack11l1l1l_opy_ (u"࠭ࡰࡢࡵࡶࡩࡩ࠭ቻ"))
            except Exception as e:
                result = Result(result=bstack11l1l1l_opy_ (u"ࠧࡧࡣ࡬ࡰࡪࡪࠧቼ"), exception=e)
                self.handler(hook_type, bstack11l1l1l_opy_ (u"ࠨࡣࡩࡸࡪࡸࠧች"), result)
                raise e.with_traceback(e.__traceback__)
            self.handler(hook_type, bstack11l1l1l_opy_ (u"ࠩࡤࡪࡹ࡫ࡲࠨቾ"), result)
        if hook_type in [bstack11l1l1l_opy_ (u"ࠪࡷࡪࡺࡵࡱࡡࡰࡩࡹ࡮࡯ࡥࠩቿ"), bstack11l1l1l_opy_ (u"ࠫࡹ࡫ࡡࡳࡦࡲࡻࡳࡥ࡭ࡦࡶ࡫ࡳࡩ࠭ኀ")]:
            return bstack11l1ll1l1l_opy_
        return bstack11l1ll1lll_opy_
    def bstack11l1lll1l1_opy_(self, bstack11l1ll11l1_opy_):
        def bstack11l1lll11l_opy_(this, *args, **kwargs):
            self.bstack11l1llll11_opy_(this, bstack11l1ll11l1_opy_)
            self._11l1ll1ll1_opy_[bstack11l1ll11l1_opy_](this, *args, **kwargs)
        return bstack11l1lll11l_opy_