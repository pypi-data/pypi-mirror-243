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
import json
import os
import threading
from bstack_utils.helper import bstack11lll1l1l1_opy_, bstack1ll1l111ll_opy_, bstack1111l11l_opy_, bstack111l1l11_opy_, \
    bstack11lll1l111_opy_
def bstack111111ll1_opy_(bstack111l11ll1l_opy_):
    for driver in bstack111l11ll1l_opy_:
        try:
            driver.quit()
        except Exception as e:
            pass
def bstack1l1lll1l1l_opy_(type, name, status, reason, bstack1l1llll11_opy_, bstack11llllll1_opy_):
    bstack11l11111_opy_ = {
        bstack11l1l1l_opy_ (u"࠭ࡡࡤࡶ࡬ࡳࡳ࠭፾"): type,
        bstack11l1l1l_opy_ (u"ࠧࡢࡴࡪࡹࡲ࡫࡮ࡵࡵࠪ፿"): {}
    }
    if type == bstack11l1l1l_opy_ (u"ࠨࡣࡱࡲࡴࡺࡡࡵࡧࠪᎀ"):
        bstack11l11111_opy_[bstack11l1l1l_opy_ (u"ࠩࡤࡶ࡬ࡻ࡭ࡦࡰࡷࡷࠬᎁ")][bstack11l1l1l_opy_ (u"ࠪࡰࡪࡼࡥ࡭ࠩᎂ")] = bstack1l1llll11_opy_
        bstack11l11111_opy_[bstack11l1l1l_opy_ (u"ࠫࡦࡸࡧࡶ࡯ࡨࡲࡹࡹࠧᎃ")][bstack11l1l1l_opy_ (u"ࠬࡪࡡࡵࡣࠪᎄ")] = json.dumps(str(bstack11llllll1_opy_))
    if type == bstack11l1l1l_opy_ (u"࠭ࡳࡦࡶࡖࡩࡸࡹࡩࡰࡰࡑࡥࡲ࡫ࠧᎅ"):
        bstack11l11111_opy_[bstack11l1l1l_opy_ (u"ࠧࡢࡴࡪࡹࡲ࡫࡮ࡵࡵࠪᎆ")][bstack11l1l1l_opy_ (u"ࠨࡰࡤࡱࡪ࠭ᎇ")] = name
    if type == bstack11l1l1l_opy_ (u"ࠩࡶࡩࡹ࡙ࡥࡴࡵ࡬ࡳࡳ࡙ࡴࡢࡶࡸࡷࠬᎈ"):
        bstack11l11111_opy_[bstack11l1l1l_opy_ (u"ࠪࡥࡷ࡭ࡵ࡮ࡧࡱࡸࡸ࠭ᎉ")][bstack11l1l1l_opy_ (u"ࠫࡸࡺࡡࡵࡷࡶࠫᎊ")] = status
        if status == bstack11l1l1l_opy_ (u"ࠬ࡬ࡡࡪ࡮ࡨࡨࠬᎋ") and str(reason) != bstack11l1l1l_opy_ (u"ࠨࠢᎌ"):
            bstack11l11111_opy_[bstack11l1l1l_opy_ (u"ࠧࡢࡴࡪࡹࡲ࡫࡮ࡵࡵࠪᎍ")][bstack11l1l1l_opy_ (u"ࠨࡴࡨࡥࡸࡵ࡮ࠨᎎ")] = json.dumps(str(reason))
    bstack111lll11l_opy_ = bstack11l1l1l_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࡠࡧࡻࡩࡨࡻࡴࡰࡴ࠽ࠤࢀࢃࠧᎏ").format(json.dumps(bstack11l11111_opy_))
    return bstack111lll11l_opy_
def bstack1l1lll1lll_opy_(url, config, logger, bstack1ll1ll1lll_opy_=False):
    hostname = bstack1ll1l111ll_opy_(url)
    is_private = bstack111l1l11_opy_(hostname)
    try:
        if is_private or bstack1ll1ll1lll_opy_:
            file_path = bstack11lll1l1l1_opy_(bstack11l1l1l_opy_ (u"ࠪ࠲ࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࠪ᎐"), bstack11l1l1l_opy_ (u"ࠫ࠳ࡨࡳࡵࡣࡦ࡯࠲ࡩ࡯࡯ࡨ࡬࡫࠳ࡰࡳࡰࡰࠪ᎑"), logger)
            if os.environ.get(bstack11l1l1l_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣࡑࡕࡃࡂࡎࡢࡒࡔ࡚࡟ࡔࡇࡗࡣࡊࡘࡒࡐࡔࠪ᎒")) and eval(
                    os.environ.get(bstack11l1l1l_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤࡒࡏࡄࡃࡏࡣࡓࡕࡔࡠࡕࡈࡘࡤࡋࡒࡓࡑࡕࠫ᎓"))):
                return
            if (bstack11l1l1l_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰࡒ࡯ࡤࡣ࡯ࠫ᎔") in config and not config[bstack11l1l1l_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱࡌࡰࡥࡤࡰࠬ᎕")]):
                os.environ[bstack11l1l1l_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡎࡒࡇࡆࡒ࡟ࡏࡑࡗࡣࡘࡋࡔࡠࡇࡕࡖࡔࡘࠧ᎖")] = str(True)
                bstack111l11ll11_opy_ = {bstack11l1l1l_opy_ (u"ࠪ࡬ࡴࡹࡴ࡯ࡣࡰࡩࠬ᎗"): hostname}
                bstack11lll1l111_opy_(bstack11l1l1l_opy_ (u"ࠫ࠳ࡨࡳࡵࡣࡦ࡯࠲ࡩ࡯࡯ࡨ࡬࡫࠳ࡰࡳࡰࡰࠪ᎘"), bstack11l1l1l_opy_ (u"ࠬࡴࡵࡥࡩࡨࡣࡱࡵࡣࡢ࡮ࠪ᎙"), bstack111l11ll11_opy_, logger)
    except Exception as e:
        pass
def bstack11l11l11l_opy_(caps, bstack111l11lll1_opy_):
    if bstack11l1l1l_opy_ (u"࠭ࡢࡴࡶࡤࡧࡰࡀ࡯ࡱࡶ࡬ࡳࡳࡹࠧ᎚") in caps:
        caps[bstack11l1l1l_opy_ (u"ࠧࡣࡵࡷࡥࡨࡱ࠺ࡰࡲࡷ࡭ࡴࡴࡳࠨ᎛")][bstack11l1l1l_opy_ (u"ࠨ࡮ࡲࡧࡦࡲࠧ᎜")] = True
        if bstack111l11lll1_opy_:
            caps[bstack11l1l1l_opy_ (u"ࠩࡥࡷࡹࡧࡣ࡬࠼ࡲࡴࡹ࡯࡯࡯ࡵࠪ᎝")][bstack11l1l1l_opy_ (u"ࠪࡰࡴࡩࡡ࡭ࡋࡧࡩࡳࡺࡩࡧ࡫ࡨࡶࠬ᎞")] = bstack111l11lll1_opy_
    else:
        caps[bstack11l1l1l_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭࠱ࡰࡴࡩࡡ࡭ࠩ᎟")] = True
        if bstack111l11lll1_opy_:
            caps[bstack11l1l1l_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮࠲ࡱࡵࡣࡢ࡮ࡌࡨࡪࡴࡴࡪࡨ࡬ࡩࡷ࠭Ꭰ")] = bstack111l11lll1_opy_
def bstack111ll1111l_opy_(bstack1l11lll111_opy_):
    bstack111l11llll_opy_ = bstack1111l11l_opy_(threading.current_thread(), bstack11l1l1l_opy_ (u"࠭ࡴࡦࡵࡷࡗࡹࡧࡴࡶࡵࠪᎡ"), bstack11l1l1l_opy_ (u"ࠧࠨᎢ"))
    if bstack111l11llll_opy_ == bstack11l1l1l_opy_ (u"ࠨࠩᎣ") or bstack111l11llll_opy_ == bstack11l1l1l_opy_ (u"ࠩࡶ࡯࡮ࡶࡰࡦࡦࠪᎤ"):
        threading.current_thread().testStatus = bstack1l11lll111_opy_
    else:
        if bstack1l11lll111_opy_ == bstack11l1l1l_opy_ (u"ࠪࡪࡦ࡯࡬ࡦࡦࠪᎥ"):
            threading.current_thread().testStatus = bstack1l11lll111_opy_