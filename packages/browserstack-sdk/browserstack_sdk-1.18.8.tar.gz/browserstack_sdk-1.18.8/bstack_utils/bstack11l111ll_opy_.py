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
import re
from bstack_utils.bstack111ll1l111_opy_ import bstack111ll1111l_opy_
def bstack111ll111l1_opy_(fixture_name):
    if fixture_name.startswith(bstack11l1l1l_opy_ (u"ࠫࡤࡾࡵ࡯࡫ࡷࡣࡸ࡫ࡴࡶࡲࡢࡪࡺࡴࡣࡵ࡫ࡲࡲࡤ࡬ࡩࡹࡶࡸࡶࡪ࠭ፋ")):
        return bstack11l1l1l_opy_ (u"ࠬࡹࡥࡵࡷࡳ࠱࡫ࡻ࡮ࡤࡶ࡬ࡳࡳ࠭ፌ")
    elif fixture_name.startswith(bstack11l1l1l_opy_ (u"࠭࡟ࡹࡷࡱ࡭ࡹࡥࡳࡦࡶࡸࡴࡤࡳ࡯ࡥࡷ࡯ࡩࡤ࡬ࡩࡹࡶࡸࡶࡪ࠭ፍ")):
        return bstack11l1l1l_opy_ (u"ࠧࡴࡧࡷࡹࡵ࠳࡭ࡰࡦࡸࡰࡪ࠭ፎ")
    elif fixture_name.startswith(bstack11l1l1l_opy_ (u"ࠨࡡࡻࡹࡳ࡯ࡴࡠࡶࡨࡥࡷࡪ࡯ࡸࡰࡢࡪࡺࡴࡣࡵ࡫ࡲࡲࡤ࡬ࡩࡹࡶࡸࡶࡪ࠭ፏ")):
        return bstack11l1l1l_opy_ (u"ࠩࡷࡩࡦࡸࡤࡰࡹࡱ࠱࡫ࡻ࡮ࡤࡶ࡬ࡳࡳ࠭ፐ")
    elif fixture_name.startswith(bstack11l1l1l_opy_ (u"ࠪࡣࡽࡻ࡮ࡪࡶࡢࡸࡪࡧࡲࡥࡱࡺࡲࡤ࡬ࡵ࡯ࡥࡷ࡭ࡴࡴ࡟ࡧ࡫ࡻࡸࡺࡸࡥࠨፑ")):
        return bstack11l1l1l_opy_ (u"ࠫࡹ࡫ࡡࡳࡦࡲࡻࡳ࠳࡭ࡰࡦࡸࡰࡪ࠭ፒ")
def bstack111ll11l11_opy_(fixture_name):
    return bool(re.match(bstack11l1l1l_opy_ (u"ࠬࡤ࡟ࡹࡷࡱ࡭ࡹࡥࠨࡴࡧࡷࡹࡵࢂࡴࡦࡣࡵࡨࡴࡽ࡮ࠪࡡࠫࡪࡺࡴࡣࡵ࡫ࡲࡲࢁࡳ࡯ࡥࡷ࡯ࡩ࠮ࡥࡦࡪࡺࡷࡹࡷ࡫࡟࠯ࠬࠪፓ"), fixture_name))
def bstack111ll11ll1_opy_(fixture_name):
    return bool(re.match(bstack11l1l1l_opy_ (u"࠭࡞ࡠࡺࡸࡲ࡮ࡺ࡟ࠩࡵࡨࡸࡺࡶࡼࡵࡧࡤࡶࡩࡵࡷ࡯ࠫࡢࡱࡴࡪࡵ࡭ࡧࡢࡪ࡮ࡾࡴࡶࡴࡨࡣ࠳࠰ࠧፔ"), fixture_name))
def bstack111ll1l1ll_opy_(fixture_name):
    return bool(re.match(bstack11l1l1l_opy_ (u"ࠧ࡟ࡡࡻࡹࡳ࡯ࡴࡠࠪࡶࡩࡹࡻࡰࡽࡶࡨࡥࡷࡪ࡯ࡸࡰࠬࡣࡨࡲࡡࡴࡵࡢࡪ࡮ࡾࡴࡶࡴࡨࡣ࠳࠰ࠧፕ"), fixture_name))
def bstack111ll1l1l1_opy_(fixture_name):
    if fixture_name.startswith(bstack11l1l1l_opy_ (u"ࠨࡡࡻࡹࡳ࡯ࡴࡠࡵࡨࡸࡺࡶ࡟ࡧࡷࡱࡧࡹ࡯࡯࡯ࡡࡩ࡭ࡽࡺࡵࡳࡧࠪፖ")):
        return bstack11l1l1l_opy_ (u"ࠩࡶࡩࡹࡻࡰ࠮ࡨࡸࡲࡨࡺࡩࡰࡰࠪፗ"), bstack11l1l1l_opy_ (u"ࠪࡆࡊࡌࡏࡓࡇࡢࡉࡆࡉࡈࠨፘ")
    elif fixture_name.startswith(bstack11l1l1l_opy_ (u"ࠫࡤࡾࡵ࡯࡫ࡷࡣࡸ࡫ࡴࡶࡲࡢࡱࡴࡪࡵ࡭ࡧࡢࡪ࡮ࡾࡴࡶࡴࡨࠫፙ")):
        return bstack11l1l1l_opy_ (u"ࠬࡹࡥࡵࡷࡳ࠱ࡲࡵࡤࡶ࡮ࡨࠫፚ"), bstack11l1l1l_opy_ (u"࠭ࡂࡆࡈࡒࡖࡊࡥࡁࡍࡎࠪ፛")
    elif fixture_name.startswith(bstack11l1l1l_opy_ (u"ࠧࡠࡺࡸࡲ࡮ࡺ࡟ࡵࡧࡤࡶࡩࡵࡷ࡯ࡡࡩࡹࡳࡩࡴࡪࡱࡱࡣ࡫࡯ࡸࡵࡷࡵࡩࠬ፜")):
        return bstack11l1l1l_opy_ (u"ࠨࡶࡨࡥࡷࡪ࡯ࡸࡰ࠰ࡪࡺࡴࡣࡵ࡫ࡲࡲࠬ፝"), bstack11l1l1l_opy_ (u"ࠩࡄࡊ࡙ࡋࡒࡠࡇࡄࡇࡍ࠭፞")
    elif fixture_name.startswith(bstack11l1l1l_opy_ (u"ࠪࡣࡽࡻ࡮ࡪࡶࡢࡸࡪࡧࡲࡥࡱࡺࡲࡤࡳ࡯ࡥࡷ࡯ࡩࡤ࡬ࡩࡹࡶࡸࡶࡪ࠭፟")):
        return bstack11l1l1l_opy_ (u"ࠫࡹ࡫ࡡࡳࡦࡲࡻࡳ࠳࡭ࡰࡦࡸࡰࡪ࠭፠"), bstack11l1l1l_opy_ (u"ࠬࡇࡆࡕࡇࡕࡣࡆࡒࡌࠨ፡")
    return None, None
def bstack111ll11lll_opy_(hook_name):
    if hook_name in [bstack11l1l1l_opy_ (u"࠭ࡳࡦࡶࡸࡴࠬ።"), bstack11l1l1l_opy_ (u"ࠧࡵࡧࡤࡶࡩࡵࡷ࡯ࠩ፣")]:
        return hook_name.capitalize()
    return hook_name
def bstack111ll1ll11_opy_(hook_name):
    if hook_name in [bstack11l1l1l_opy_ (u"ࠨࡵࡨࡸࡺࡶ࡟ࡧࡷࡱࡧࡹ࡯࡯࡯ࠩ፤"), bstack11l1l1l_opy_ (u"ࠩࡶࡩࡹࡻࡰࡠ࡯ࡨࡸ࡭ࡵࡤࠨ፥")]:
        return bstack11l1l1l_opy_ (u"ࠪࡆࡊࡌࡏࡓࡇࡢࡉࡆࡉࡈࠨ፦")
    elif hook_name in [bstack11l1l1l_opy_ (u"ࠫࡸ࡫ࡴࡶࡲࡢࡱࡴࡪࡵ࡭ࡧࠪ፧"), bstack11l1l1l_opy_ (u"ࠬࡹࡥࡵࡷࡳࡣࡨࡲࡡࡴࡵࠪ፨")]:
        return bstack11l1l1l_opy_ (u"࠭ࡂࡆࡈࡒࡖࡊࡥࡁࡍࡎࠪ፩")
    elif hook_name in [bstack11l1l1l_opy_ (u"ࠧࡵࡧࡤࡶࡩࡵࡷ࡯ࡡࡩࡹࡳࡩࡴࡪࡱࡱࠫ፪"), bstack11l1l1l_opy_ (u"ࠨࡶࡨࡥࡷࡪ࡯ࡸࡰࡢࡱࡪࡺࡨࡰࡦࠪ፫")]:
        return bstack11l1l1l_opy_ (u"ࠩࡄࡊ࡙ࡋࡒࡠࡇࡄࡇࡍ࠭፬")
    elif hook_name in [bstack11l1l1l_opy_ (u"ࠪࡸࡪࡧࡲࡥࡱࡺࡲࡤࡳ࡯ࡥࡷ࡯ࡩࠬ፭"), bstack11l1l1l_opy_ (u"ࠫࡹ࡫ࡡࡳࡦࡲࡻࡳࡥࡣ࡭ࡣࡶࡷࠬ፮")]:
        return bstack11l1l1l_opy_ (u"ࠬࡇࡆࡕࡇࡕࡣࡆࡒࡌࠨ፯")
    return hook_name
def bstack111ll111ll_opy_(node, scenario):
    if hasattr(node, bstack11l1l1l_opy_ (u"࠭ࡣࡢ࡮࡯ࡷࡵ࡫ࡣࠨ፰")):
        parts = node.nodeid.rsplit(bstack11l1l1l_opy_ (u"ࠢ࡜ࠤ፱"))
        params = parts[-1]
        return bstack11l1l1l_opy_ (u"ࠣࡽࢀࠤࡠࢁࡽࠣ፲").format(scenario.name, params)
    return scenario.name
def bstack111ll1ll1l_opy_(node):
    try:
        examples = []
        if hasattr(node, bstack11l1l1l_opy_ (u"ࠩࡦࡥࡱࡲࡳࡱࡧࡦࠫ፳")):
            examples = list(node.callspec.params[bstack11l1l1l_opy_ (u"ࠪࡣࡵࡿࡴࡦࡵࡷࡣࡧࡪࡤࡠࡧࡻࡥࡲࡶ࡬ࡦࠩ፴")].values())
        return examples
    except:
        return []
def bstack111ll1l11l_opy_(feature, scenario):
    return list(feature.tags) + list(scenario.tags)
def bstack111ll11l1l_opy_(report):
    try:
        status = bstack11l1l1l_opy_ (u"ࠫ࡫ࡧࡩ࡭ࡧࡧࠫ፵")
        if report.passed or (report.failed and hasattr(report, bstack11l1l1l_opy_ (u"ࠧࡽࡡࡴࡺࡩࡥ࡮ࡲࠢ፶"))):
            status = bstack11l1l1l_opy_ (u"࠭ࡰࡢࡵࡶࡩࡩ࠭፷")
        elif report.skipped:
            status = bstack11l1l1l_opy_ (u"ࠧࡴ࡭࡬ࡴࡵ࡫ࡤࠨ፸")
        bstack111ll1111l_opy_(status)
    except:
        pass
def bstack1lll11l1ll_opy_(status):
    try:
        bstack111ll11111_opy_ = bstack11l1l1l_opy_ (u"ࠨࡨࡤ࡭ࡱ࡫ࡤࠨ፹")
        if status == bstack11l1l1l_opy_ (u"ࠩࡳࡥࡸࡹࡥࡥࠩ፺"):
            bstack111ll11111_opy_ = bstack11l1l1l_opy_ (u"ࠪࡴࡦࡹࡳࡦࡦࠪ፻")
        elif status == bstack11l1l1l_opy_ (u"ࠫࡸࡱࡩࡱࡲࡨࡨࠬ፼"):
            bstack111ll11111_opy_ = bstack11l1l1l_opy_ (u"ࠬࡹ࡫ࡪࡲࡳࡩࡩ࠭፽")
        bstack111ll1111l_opy_(bstack111ll11111_opy_)
    except:
        pass
def bstack111ll1lll1_opy_(item=None, report=None, summary=None, extra=None):
    return