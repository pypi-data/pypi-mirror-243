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
import json
import os
import threading
from bstack_utils.config import Config
from bstack_utils.helper import bstack11ll1l1lll_opy_, bstack1l1ll11ll_opy_, bstack11111l11_opy_, bstack11ll1l1l_opy_, \
    bstack11lll1l11l_opy_
def bstack1lllll111l_opy_(bstack111l11l11l_opy_):
    for driver in bstack111l11l11l_opy_:
        try:
            driver.quit()
        except Exception as e:
            pass
def bstack1111ll1l1_opy_(driver, status, reason=bstack11l1ll_opy_ (u"ࠩࠪ፬")):
    bstack1ll1l11l1_opy_ = Config.get_instance()
    if bstack1ll1l11l1_opy_.bstack1l11l11111_opy_():
        return
    bstack1l111lll_opy_ = bstack1ll1lll1l_opy_(bstack11l1ll_opy_ (u"ࠪࡷࡪࡺࡓࡦࡵࡶ࡭ࡴࡴࡓࡵࡣࡷࡹࡸ࠭፭"), bstack11l1ll_opy_ (u"ࠫࠬ፮"), status, reason, bstack11l1ll_opy_ (u"ࠬ࠭፯"), bstack11l1ll_opy_ (u"࠭ࠧ፰"))
    driver.execute_script(bstack1l111lll_opy_)
def bstack1l1ll111l_opy_(page, status, reason=bstack11l1ll_opy_ (u"ࠧࠨ፱")):
    try:
        if page is None:
            return
        bstack1ll1l11l1_opy_ = Config.get_instance()
        if bstack1ll1l11l1_opy_.bstack1l11l11111_opy_():
            return
        bstack1l111lll_opy_ = bstack1ll1lll1l_opy_(bstack11l1ll_opy_ (u"ࠨࡵࡨࡸࡘ࡫ࡳࡴ࡫ࡲࡲࡘࡺࡡࡵࡷࡶࠫ፲"), bstack11l1ll_opy_ (u"ࠩࠪ፳"), status, reason, bstack11l1ll_opy_ (u"ࠪࠫ፴"), bstack11l1ll_opy_ (u"ࠫࠬ፵"))
        page.evaluate(bstack11l1ll_opy_ (u"ࠧࡥࠠ࠾ࡀࠣࡿࢂࠨ፶"), bstack1l111lll_opy_)
    except Exception as e:
        print(bstack11l1ll_opy_ (u"ࠨࡅࡹࡥࡨࡴࡹ࡯࡯࡯ࠢ࡬ࡲࠥࡹࡥࡵࡶ࡬ࡲ࡬ࠦࡳࡦࡵࡶ࡭ࡴࡴࠠࡴࡶࡤࡸࡺࡹࠠࡧࡱࡵࠤࡵࡲࡡࡺࡹࡵ࡭࡬࡮ࡴࠡࡽࢀࠦ፷"), e)
def bstack1ll1lll1l_opy_(type, name, status, reason, bstack11llll11_opy_, bstack1111ll111_opy_):
    bstack11l1l1ll_opy_ = {
        bstack11l1ll_opy_ (u"ࠧࡢࡥࡷ࡭ࡴࡴࠧ፸"): type,
        bstack11l1ll_opy_ (u"ࠨࡣࡵ࡫ࡺࡳࡥ࡯ࡶࡶࠫ፹"): {}
    }
    if type == bstack11l1ll_opy_ (u"ࠩࡤࡲࡳࡵࡴࡢࡶࡨࠫ፺"):
        bstack11l1l1ll_opy_[bstack11l1ll_opy_ (u"ࠪࡥࡷ࡭ࡵ࡮ࡧࡱࡸࡸ࠭፻")][bstack11l1ll_opy_ (u"ࠫࡱ࡫ࡶࡦ࡮ࠪ፼")] = bstack11llll11_opy_
        bstack11l1l1ll_opy_[bstack11l1ll_opy_ (u"ࠬࡧࡲࡨࡷࡰࡩࡳࡺࡳࠨ፽")][bstack11l1ll_opy_ (u"࠭ࡤࡢࡶࡤࠫ፾")] = json.dumps(str(bstack1111ll111_opy_))
    if type == bstack11l1ll_opy_ (u"ࠧࡴࡧࡷࡗࡪࡹࡳࡪࡱࡱࡒࡦࡳࡥࠨ፿"):
        bstack11l1l1ll_opy_[bstack11l1ll_opy_ (u"ࠨࡣࡵ࡫ࡺࡳࡥ࡯ࡶࡶࠫᎀ")][bstack11l1ll_opy_ (u"ࠩࡱࡥࡲ࡫ࠧᎁ")] = name
    if type == bstack11l1ll_opy_ (u"ࠪࡷࡪࡺࡓࡦࡵࡶ࡭ࡴࡴࡓࡵࡣࡷࡹࡸ࠭ᎂ"):
        bstack11l1l1ll_opy_[bstack11l1ll_opy_ (u"ࠫࡦࡸࡧࡶ࡯ࡨࡲࡹࡹࠧᎃ")][bstack11l1ll_opy_ (u"ࠬࡹࡴࡢࡶࡸࡷࠬᎄ")] = status
        if status == bstack11l1ll_opy_ (u"࠭ࡦࡢ࡫࡯ࡩࡩ࠭ᎅ") and str(reason) != bstack11l1ll_opy_ (u"ࠢࠣᎆ"):
            bstack11l1l1ll_opy_[bstack11l1ll_opy_ (u"ࠨࡣࡵ࡫ࡺࡳࡥ࡯ࡶࡶࠫᎇ")][bstack11l1ll_opy_ (u"ࠩࡵࡩࡦࡹ࡯࡯ࠩᎈ")] = json.dumps(str(reason))
    bstack1ll11l111l_opy_ = bstack11l1ll_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࡡࡨࡼࡪࡩࡵࡵࡱࡵ࠾ࠥࢁࡽࠨᎉ").format(json.dumps(bstack11l1l1ll_opy_))
    return bstack1ll11l111l_opy_
def bstack1lllllll1_opy_(url, config, logger, bstack1lll1llll_opy_=False):
    hostname = bstack1l1ll11ll_opy_(url)
    is_private = bstack11ll1l1l_opy_(hostname)
    try:
        if is_private or bstack1lll1llll_opy_:
            file_path = bstack11ll1l1lll_opy_(bstack11l1ll_opy_ (u"ࠫ࠳ࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࠫᎊ"), bstack11l1ll_opy_ (u"ࠬ࠴ࡢࡴࡶࡤࡧࡰ࠳ࡣࡰࡰࡩ࡭࡬࠴ࡪࡴࡱࡱࠫᎋ"), logger)
            if os.environ.get(bstack11l1ll_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤࡒࡏࡄࡃࡏࡣࡓࡕࡔࡠࡕࡈࡘࡤࡋࡒࡓࡑࡕࠫᎌ")) and eval(
                    os.environ.get(bstack11l1ll_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡌࡐࡅࡄࡐࡤࡔࡏࡕࡡࡖࡉ࡙ࡥࡅࡓࡔࡒࡖࠬᎍ"))):
                return
            if (bstack11l1ll_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱࡌࡰࡥࡤࡰࠬᎎ") in config and not config[bstack11l1ll_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࡍࡱࡦࡥࡱ࠭ᎏ")]):
                os.environ[bstack11l1ll_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡏࡓࡈࡇࡌࡠࡐࡒࡘࡤ࡙ࡅࡕࡡࡈࡖࡗࡕࡒࠨ᎐")] = str(True)
                bstack111l11l1l1_opy_ = {bstack11l1ll_opy_ (u"ࠫ࡭ࡵࡳࡵࡰࡤࡱࡪ࠭᎑"): hostname}
                bstack11lll1l11l_opy_(bstack11l1ll_opy_ (u"ࠬ࠴ࡢࡴࡶࡤࡧࡰ࠳ࡣࡰࡰࡩ࡭࡬࠴ࡪࡴࡱࡱࠫ᎒"), bstack11l1ll_opy_ (u"࠭࡮ࡶࡦࡪࡩࡤࡲ࡯ࡤࡣ࡯ࠫ᎓"), bstack111l11l1l1_opy_, logger)
    except Exception as e:
        pass
def bstack1ll1111111_opy_(caps, bstack111l11ll11_opy_):
    if bstack11l1ll_opy_ (u"ࠧࡣࡵࡷࡥࡨࡱ࠺ࡰࡲࡷ࡭ࡴࡴࡳࠨ᎔") in caps:
        caps[bstack11l1ll_opy_ (u"ࠨࡤࡶࡸࡦࡩ࡫࠻ࡱࡳࡸ࡮ࡵ࡮ࡴࠩ᎕")][bstack11l1ll_opy_ (u"ࠩ࡯ࡳࡨࡧ࡬ࠨ᎖")] = True
        if bstack111l11ll11_opy_:
            caps[bstack11l1ll_opy_ (u"ࠪࡦࡸࡺࡡࡤ࡭࠽ࡳࡵࡺࡩࡰࡰࡶࠫ᎗")][bstack11l1ll_opy_ (u"ࠫࡱࡵࡣࡢ࡮ࡌࡨࡪࡴࡴࡪࡨ࡬ࡩࡷ࠭᎘")] = bstack111l11ll11_opy_
    else:
        caps[bstack11l1ll_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮࠲ࡱࡵࡣࡢ࡮ࠪ᎙")] = True
        if bstack111l11ll11_opy_:
            caps[bstack11l1ll_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯࠳ࡲ࡯ࡤࡣ࡯ࡍࡩ࡫࡮ࡵ࡫ࡩ࡭ࡪࡸࠧ᎚")] = bstack111l11ll11_opy_
def bstack111l1lll1l_opy_(bstack1l11lll1ll_opy_):
    bstack111l11l1ll_opy_ = bstack11111l11_opy_(threading.current_thread(), bstack11l1ll_opy_ (u"ࠧࡵࡧࡶࡸࡘࡺࡡࡵࡷࡶࠫ᎛"), bstack11l1ll_opy_ (u"ࠨࠩ᎜"))
    if bstack111l11l1ll_opy_ == bstack11l1ll_opy_ (u"ࠩࠪ᎝") or bstack111l11l1ll_opy_ == bstack11l1ll_opy_ (u"ࠪࡷࡰ࡯ࡰࡱࡧࡧࠫ᎞"):
        threading.current_thread().testStatus = bstack1l11lll1ll_opy_
    else:
        if bstack1l11lll1ll_opy_ == bstack11l1ll_opy_ (u"ࠫ࡫ࡧࡩ࡭ࡧࡧࠫ᎟"):
            threading.current_thread().testStatus = bstack1l11lll1ll_opy_