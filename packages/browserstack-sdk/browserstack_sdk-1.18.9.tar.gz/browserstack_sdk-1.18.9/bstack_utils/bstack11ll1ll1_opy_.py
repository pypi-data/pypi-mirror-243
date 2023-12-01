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
import re
from bstack_utils.bstack1l11l11l1_opy_ import bstack111l1lll1l_opy_
def bstack111ll11lll_opy_(fixture_name):
    if fixture_name.startswith(bstack11l1ll_opy_ (u"ࠧࡠࡺࡸࡲ࡮ࡺ࡟ࡴࡧࡷࡹࡵࡥࡦࡶࡰࡦࡸ࡮ࡵ࡮ࡠࡨ࡬ࡼࡹࡻࡲࡦࠩጹ")):
        return bstack11l1ll_opy_ (u"ࠨࡵࡨࡸࡺࡶ࠭ࡧࡷࡱࡧࡹ࡯࡯࡯ࠩጺ")
    elif fixture_name.startswith(bstack11l1ll_opy_ (u"ࠩࡢࡼࡺࡴࡩࡵࡡࡶࡩࡹࡻࡰࡠ࡯ࡲࡨࡺࡲࡥࡠࡨ࡬ࡼࡹࡻࡲࡦࠩጻ")):
        return bstack11l1ll_opy_ (u"ࠪࡷࡪࡺࡵࡱ࠯ࡰࡳࡩࡻ࡬ࡦࠩጼ")
    elif fixture_name.startswith(bstack11l1ll_opy_ (u"ࠫࡤࡾࡵ࡯࡫ࡷࡣࡹ࡫ࡡࡳࡦࡲࡻࡳࡥࡦࡶࡰࡦࡸ࡮ࡵ࡮ࡠࡨ࡬ࡼࡹࡻࡲࡦࠩጽ")):
        return bstack11l1ll_opy_ (u"ࠬࡺࡥࡢࡴࡧࡳࡼࡴ࠭ࡧࡷࡱࡧࡹ࡯࡯࡯ࠩጾ")
    elif fixture_name.startswith(bstack11l1ll_opy_ (u"࠭࡟ࡹࡷࡱ࡭ࡹࡥࡴࡦࡣࡵࡨࡴࡽ࡮ࡠࡨࡸࡲࡨࡺࡩࡰࡰࡢࡪ࡮ࡾࡴࡶࡴࡨࠫጿ")):
        return bstack11l1ll_opy_ (u"ࠧࡵࡧࡤࡶࡩࡵࡷ࡯࠯ࡰࡳࡩࡻ࡬ࡦࠩፀ")
def bstack111ll1111l_opy_(fixture_name):
    return bool(re.match(bstack11l1ll_opy_ (u"ࠨࡠࡢࡼࡺࡴࡩࡵࡡࠫࡷࡪࡺࡵࡱࡾࡷࡩࡦࡸࡤࡰࡹࡱ࠭ࡤ࠮ࡦࡶࡰࡦࡸ࡮ࡵ࡮ࡽ࡯ࡲࡨࡺࡲࡥࠪࡡࡩ࡭ࡽࡺࡵࡳࡧࡢ࠲࠯࠭ፁ"), fixture_name))
def bstack111l1llll1_opy_(fixture_name):
    return bool(re.match(bstack11l1ll_opy_ (u"ࠩࡡࡣࡽࡻ࡮ࡪࡶࡢࠬࡸ࡫ࡴࡶࡲࡿࡸࡪࡧࡲࡥࡱࡺࡲ࠮ࡥ࡭ࡰࡦࡸࡰࡪࡥࡦࡪࡺࡷࡹࡷ࡫࡟࠯ࠬࠪፂ"), fixture_name))
def bstack111ll1l11l_opy_(fixture_name):
    return bool(re.match(bstack11l1ll_opy_ (u"ࠪࡢࡤࡾࡵ࡯࡫ࡷࡣ࠭ࡹࡥࡵࡷࡳࢀࡹ࡫ࡡࡳࡦࡲࡻࡳ࠯࡟ࡤ࡮ࡤࡷࡸࡥࡦࡪࡺࡷࡹࡷ࡫࡟࠯ࠬࠪፃ"), fixture_name))
def bstack111l1lllll_opy_(fixture_name):
    if fixture_name.startswith(bstack11l1ll_opy_ (u"ࠫࡤࡾࡵ࡯࡫ࡷࡣࡸ࡫ࡴࡶࡲࡢࡪࡺࡴࡣࡵ࡫ࡲࡲࡤ࡬ࡩࡹࡶࡸࡶࡪ࠭ፄ")):
        return bstack11l1ll_opy_ (u"ࠬࡹࡥࡵࡷࡳ࠱࡫ࡻ࡮ࡤࡶ࡬ࡳࡳ࠭ፅ"), bstack11l1ll_opy_ (u"࠭ࡂࡆࡈࡒࡖࡊࡥࡅࡂࡅࡋࠫፆ")
    elif fixture_name.startswith(bstack11l1ll_opy_ (u"ࠧࡠࡺࡸࡲ࡮ࡺ࡟ࡴࡧࡷࡹࡵࡥ࡭ࡰࡦࡸࡰࡪࡥࡦࡪࡺࡷࡹࡷ࡫ࠧፇ")):
        return bstack11l1ll_opy_ (u"ࠨࡵࡨࡸࡺࡶ࠭࡮ࡱࡧࡹࡱ࡫ࠧፈ"), bstack11l1ll_opy_ (u"ࠩࡅࡉࡋࡕࡒࡆࡡࡄࡐࡑ࠭ፉ")
    elif fixture_name.startswith(bstack11l1ll_opy_ (u"ࠪࡣࡽࡻ࡮ࡪࡶࡢࡸࡪࡧࡲࡥࡱࡺࡲࡤ࡬ࡵ࡯ࡥࡷ࡭ࡴࡴ࡟ࡧ࡫ࡻࡸࡺࡸࡥࠨፊ")):
        return bstack11l1ll_opy_ (u"ࠫࡹ࡫ࡡࡳࡦࡲࡻࡳ࠳ࡦࡶࡰࡦࡸ࡮ࡵ࡮ࠨፋ"), bstack11l1ll_opy_ (u"ࠬࡇࡆࡕࡇࡕࡣࡊࡇࡃࡉࠩፌ")
    elif fixture_name.startswith(bstack11l1ll_opy_ (u"࠭࡟ࡹࡷࡱ࡭ࡹࡥࡴࡦࡣࡵࡨࡴࡽ࡮ࡠ࡯ࡲࡨࡺࡲࡥࡠࡨ࡬ࡼࡹࡻࡲࡦࠩፍ")):
        return bstack11l1ll_opy_ (u"ࠧࡵࡧࡤࡶࡩࡵࡷ࡯࠯ࡰࡳࡩࡻ࡬ࡦࠩፎ"), bstack11l1ll_opy_ (u"ࠨࡃࡉࡘࡊࡘ࡟ࡂࡎࡏࠫፏ")
    return None, None
def bstack111ll111ll_opy_(hook_name):
    if hook_name in [bstack11l1ll_opy_ (u"ࠩࡶࡩࡹࡻࡰࠨፐ"), bstack11l1ll_opy_ (u"ࠪࡸࡪࡧࡲࡥࡱࡺࡲࠬፑ")]:
        return hook_name.capitalize()
    return hook_name
def bstack111ll1l1l1_opy_(hook_name):
    if hook_name in [bstack11l1ll_opy_ (u"ࠫࡸ࡫ࡴࡶࡲࡢࡪࡺࡴࡣࡵ࡫ࡲࡲࠬፒ"), bstack11l1ll_opy_ (u"ࠬࡹࡥࡵࡷࡳࡣࡲ࡫ࡴࡩࡱࡧࠫፓ")]:
        return bstack11l1ll_opy_ (u"࠭ࡂࡆࡈࡒࡖࡊࡥࡅࡂࡅࡋࠫፔ")
    elif hook_name in [bstack11l1ll_opy_ (u"ࠧࡴࡧࡷࡹࡵࡥ࡭ࡰࡦࡸࡰࡪ࠭ፕ"), bstack11l1ll_opy_ (u"ࠨࡵࡨࡸࡺࡶ࡟ࡤ࡮ࡤࡷࡸ࠭ፖ")]:
        return bstack11l1ll_opy_ (u"ࠩࡅࡉࡋࡕࡒࡆࡡࡄࡐࡑ࠭ፗ")
    elif hook_name in [bstack11l1ll_opy_ (u"ࠪࡸࡪࡧࡲࡥࡱࡺࡲࡤ࡬ࡵ࡯ࡥࡷ࡭ࡴࡴࠧፘ"), bstack11l1ll_opy_ (u"ࠫࡹ࡫ࡡࡳࡦࡲࡻࡳࡥ࡭ࡦࡶ࡫ࡳࡩ࠭ፙ")]:
        return bstack11l1ll_opy_ (u"ࠬࡇࡆࡕࡇࡕࡣࡊࡇࡃࡉࠩፚ")
    elif hook_name in [bstack11l1ll_opy_ (u"࠭ࡴࡦࡣࡵࡨࡴࡽ࡮ࡠ࡯ࡲࡨࡺࡲࡥࠨ፛"), bstack11l1ll_opy_ (u"ࠧࡵࡧࡤࡶࡩࡵࡷ࡯ࡡࡦࡰࡦࡹࡳࠨ፜")]:
        return bstack11l1ll_opy_ (u"ࠨࡃࡉࡘࡊࡘ࡟ࡂࡎࡏࠫ፝")
    return hook_name
def bstack111ll11l11_opy_(node, scenario):
    if hasattr(node, bstack11l1ll_opy_ (u"ࠩࡦࡥࡱࡲࡳࡱࡧࡦࠫ፞")):
        parts = node.nodeid.rsplit(bstack11l1ll_opy_ (u"ࠥ࡟ࠧ፟"))
        params = parts[-1]
        return bstack11l1ll_opy_ (u"ࠦࢀࢃࠠ࡜ࡽࢀࠦ፠").format(scenario.name, params)
    return scenario.name
def bstack111ll1l111_opy_(node):
    try:
        examples = []
        if hasattr(node, bstack11l1ll_opy_ (u"ࠬࡩࡡ࡭࡮ࡶࡴࡪࡩࠧ፡")):
            examples = list(node.callspec.params[bstack11l1ll_opy_ (u"࠭࡟ࡱࡻࡷࡩࡸࡺ࡟ࡣࡦࡧࡣࡪࡾࡡ࡮ࡲ࡯ࡩࠬ።")].values())
        return examples
    except:
        return []
def bstack111ll11ll1_opy_(feature, scenario):
    return list(feature.tags) + list(scenario.tags)
def bstack111ll11111_opy_(report):
    try:
        status = bstack11l1ll_opy_ (u"ࠧࡧࡣ࡬ࡰࡪࡪࠧ፣")
        if report.passed or (report.failed and hasattr(report, bstack11l1ll_opy_ (u"ࠣࡹࡤࡷࡽ࡬ࡡࡪ࡮ࠥ፤"))):
            status = bstack11l1ll_opy_ (u"ࠩࡳࡥࡸࡹࡥࡥࠩ፥")
        elif report.skipped:
            status = bstack11l1ll_opy_ (u"ࠪࡷࡰ࡯ࡰࡱࡧࡧࠫ፦")
        bstack111l1lll1l_opy_(status)
    except:
        pass
def bstack111l1111_opy_(status):
    try:
        bstack111ll111l1_opy_ = bstack11l1ll_opy_ (u"ࠫ࡫ࡧࡩ࡭ࡧࡧࠫ፧")
        if status == bstack11l1ll_opy_ (u"ࠬࡶࡡࡴࡵࡨࡨࠬ፨"):
            bstack111ll111l1_opy_ = bstack11l1ll_opy_ (u"࠭ࡰࡢࡵࡶࡩࡩ࠭፩")
        elif status == bstack11l1ll_opy_ (u"ࠧࡴ࡭࡬ࡴࡵ࡫ࡤࠨ፪"):
            bstack111ll111l1_opy_ = bstack11l1ll_opy_ (u"ࠨࡵ࡮࡭ࡵࡶࡥࡥࠩ፫")
        bstack111l1lll1l_opy_(bstack111ll111l1_opy_)
    except:
        pass
def bstack111ll11l1l_opy_(item=None, report=None, summary=None, extra=None):
    return