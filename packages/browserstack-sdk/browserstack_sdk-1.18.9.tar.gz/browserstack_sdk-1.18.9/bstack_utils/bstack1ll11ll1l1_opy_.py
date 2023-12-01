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
import datetime
import json
import logging
import os
import threading
from bstack_utils.helper import bstack1l111l111l_opy_, bstack1ll11ll1ll_opy_, get_host_info, bstack1l11111ll1_opy_, bstack1l111l1111_opy_, bstack11ll111ll1_opy_, \
    bstack11ll1ll1l1_opy_, bstack11lll11111_opy_, bstack1111l1lll_opy_, bstack11lll1111l_opy_, bstack111l1l1l1_opy_, bstack1l1l1ll111_opy_
from bstack_utils.bstack111l1l11ll_opy_ import bstack111l1ll1l1_opy_
from bstack_utils.bstack1l1l1l111l_opy_ import bstack1l11llllll_opy_
bstack1111l1llll_opy_ = [
    bstack11l1ll_opy_ (u"ࠫࡑࡵࡧࡄࡴࡨࡥࡹ࡫ࡤࠨᏞ"), bstack11l1ll_opy_ (u"ࠬࡉࡂࡕࡕࡨࡷࡸ࡯࡯࡯ࡅࡵࡩࡦࡺࡥࡥࠩᏟ"), bstack11l1ll_opy_ (u"࠭ࡔࡦࡵࡷࡖࡺࡴࡆࡪࡰ࡬ࡷ࡭࡫ࡤࠨᏠ"), bstack11l1ll_opy_ (u"ࠧࡕࡧࡶࡸࡗࡻ࡮ࡔ࡭࡬ࡴࡵ࡫ࡤࠨᏡ"),
    bstack11l1ll_opy_ (u"ࠨࡊࡲࡳࡰࡘࡵ࡯ࡈ࡬ࡲ࡮ࡹࡨࡦࡦࠪᏢ"), bstack11l1ll_opy_ (u"ࠩࡗࡩࡸࡺࡒࡶࡰࡖࡸࡦࡸࡴࡦࡦࠪᏣ"), bstack11l1ll_opy_ (u"ࠪࡌࡴࡵ࡫ࡓࡷࡱࡗࡹࡧࡲࡵࡧࡧࠫᏤ")
]
bstack1111ll111l_opy_ = bstack11l1ll_opy_ (u"ࠫ࡭ࡺࡴࡱࡵ࠽࠳࠴ࡩ࡯࡭࡮ࡨࡧࡹࡵࡲ࠮ࡱࡥࡷࡪࡸࡶࡢࡤ࡬ࡰ࡮ࡺࡹ࠯ࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠮ࡤࡱࡰࠫᏥ")
logger = logging.getLogger(__name__)
class bstack11l1ll11_opy_:
    bstack111l1l11ll_opy_ = None
    bs_config = None
    @classmethod
    @bstack1l1l1ll111_opy_(class_method=True)
    def launch(cls, bs_config, bstack1111l1l111_opy_):
        cls.bs_config = bs_config
        if not cls.bstack1111l111ll_opy_():
            return
        cls.bstack1111ll1111_opy_()
        bstack11llllllll_opy_ = bstack1l11111ll1_opy_(bs_config)
        bstack1l111111ll_opy_ = bstack1l111l1111_opy_(bs_config)
        data = {
            bstack11l1ll_opy_ (u"ࠬ࡬࡯ࡳ࡯ࡤࡸࠬᏦ"): bstack11l1ll_opy_ (u"࠭ࡪࡴࡱࡱࠫᏧ"),
            bstack11l1ll_opy_ (u"ࠧࡱࡴࡲ࡮ࡪࡩࡴࡠࡰࡤࡱࡪ࠭Ꮸ"): bs_config.get(bstack11l1ll_opy_ (u"ࠨࡲࡵࡳ࡯࡫ࡣࡵࡐࡤࡱࡪ࠭Ꮹ"), bstack11l1ll_opy_ (u"ࠩࠪᏪ")),
            bstack11l1ll_opy_ (u"ࠪࡲࡦࡳࡥࠨᏫ"): bs_config.get(bstack11l1ll_opy_ (u"ࠫࡧࡻࡩ࡭ࡦࡑࡥࡲ࡫ࠧᏬ"), os.path.basename(os.path.abspath(os.getcwd()))),
            bstack11l1ll_opy_ (u"ࠬࡨࡵࡪ࡮ࡧࡣ࡮ࡪࡥ࡯ࡶ࡬ࡪ࡮࡫ࡲࠨᏭ"): bs_config.get(bstack11l1ll_opy_ (u"࠭ࡢࡶ࡫࡯ࡨࡎࡪࡥ࡯ࡶ࡬ࡪ࡮࡫ࡲࠨᏮ")),
            bstack11l1ll_opy_ (u"ࠧࡥࡧࡶࡧࡷ࡯ࡰࡵ࡫ࡲࡲࠬᏯ"): bs_config.get(bstack11l1ll_opy_ (u"ࠨࡤࡸ࡭ࡱࡪࡄࡦࡵࡦࡶ࡮ࡶࡴࡪࡱࡱࠫᏰ"), bstack11l1ll_opy_ (u"ࠩࠪᏱ")),
            bstack11l1ll_opy_ (u"ࠪࡷࡹࡧࡲࡵࡡࡷ࡭ࡲ࡫ࠧᏲ"): datetime.datetime.now().isoformat(),
            bstack11l1ll_opy_ (u"ࠫࡹࡧࡧࡴࠩᏳ"): bstack11ll111ll1_opy_(bs_config),
            bstack11l1ll_opy_ (u"ࠬ࡮࡯ࡴࡶࡢ࡭ࡳ࡬࡯ࠨᏴ"): get_host_info(),
            bstack11l1ll_opy_ (u"࠭ࡣࡪࡡ࡬ࡲ࡫ࡵࠧᏵ"): bstack1ll11ll1ll_opy_(),
            bstack11l1ll_opy_ (u"ࠧࡣࡷ࡬ࡰࡩࡥࡲࡶࡰࡢ࡭ࡩ࡫࡮ࡵ࡫ࡩ࡭ࡪࡸࠧ᏶"): os.environ.get(bstack11l1ll_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡃࡗࡌࡐࡉࡥࡒࡖࡐࡢࡍࡉࡋࡎࡕࡋࡉࡍࡊࡘࠧ᏷")),
            bstack11l1ll_opy_ (u"ࠩࡩࡥ࡮ࡲࡥࡥࡡࡷࡩࡸࡺࡳࡠࡴࡨࡶࡺࡴࠧᏸ"): os.environ.get(bstack11l1ll_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡕࡉࡗ࡛ࡎࠨᏹ"), False),
            bstack11l1ll_opy_ (u"ࠫࡻ࡫ࡲࡴ࡫ࡲࡲࡤࡩ࡯࡯ࡶࡵࡳࡱ࠭ᏺ"): bstack1l111l111l_opy_(),
            bstack11l1ll_opy_ (u"ࠬࡵࡢࡴࡧࡵࡺࡦࡨࡩ࡭࡫ࡷࡽࡤࡼࡥࡳࡵ࡬ࡳࡳ࠭ᏻ"): {
                bstack11l1ll_opy_ (u"࠭ࡦࡳࡣࡰࡩࡼࡵࡲ࡬ࡐࡤࡱࡪ࠭ᏼ"): bstack1111l1l111_opy_.get(bstack11l1ll_opy_ (u"ࠧࡧࡴࡤࡱࡪࡽ࡯ࡳ࡭ࡢࡲࡦࡳࡥࠨᏽ"), bstack11l1ll_opy_ (u"ࠨࡒࡼࡸࡪࡹࡴࠨ᏾")),
                bstack11l1ll_opy_ (u"ࠩࡩࡶࡦࡳࡥࡸࡱࡵ࡯࡛࡫ࡲࡴ࡫ࡲࡲࠬ᏿"): bstack1111l1l111_opy_.get(bstack11l1ll_opy_ (u"ࠪࡪࡷࡧ࡭ࡦࡹࡲࡶࡰࡥࡶࡦࡴࡶ࡭ࡴࡴࠧ᐀")),
                bstack11l1ll_opy_ (u"ࠫࡸࡪ࡫ࡗࡧࡵࡷ࡮ࡵ࡮ࠨᐁ"): bstack1111l1l111_opy_.get(bstack11l1ll_opy_ (u"ࠬࡹࡤ࡬ࡡࡹࡩࡷࡹࡩࡰࡰࠪᐂ"))
            }
        }
        config = {
            bstack11l1ll_opy_ (u"࠭ࡡࡶࡶ࡫ࠫᐃ"): (bstack11llllllll_opy_, bstack1l111111ll_opy_),
            bstack11l1ll_opy_ (u"ࠧࡩࡧࡤࡨࡪࡸࡳࠨᐄ"): cls.default_headers()
        }
        response = bstack1111l1lll_opy_(bstack11l1ll_opy_ (u"ࠨࡒࡒࡗ࡙࠭ᐅ"), cls.request_url(bstack11l1ll_opy_ (u"ࠩࡤࡴ࡮࠵ࡶ࠲࠱ࡥࡹ࡮ࡲࡤࡴࠩᐆ")), data, config)
        if response.status_code != 200:
            os.environ[bstack11l1ll_opy_ (u"ࠪࡆࡘࡥࡔࡆࡕࡗࡓࡕ࡙࡟ࡃࡗࡌࡐࡉࡥࡃࡐࡏࡓࡐࡊ࡚ࡅࡅࠩᐇ")] = bstack11l1ll_opy_ (u"ࠫ࡫ࡧ࡬ࡴࡧࠪᐈ")
            os.environ[bstack11l1ll_opy_ (u"ࠬࡈࡓࡠࡖࡈࡗ࡙ࡕࡐࡔࡡࡍ࡛࡙࠭ᐉ")] = bstack11l1ll_opy_ (u"࠭࡮ࡶ࡮࡯ࠫᐊ")
            os.environ[bstack11l1ll_opy_ (u"ࠧࡃࡕࡢࡘࡊ࡙ࡔࡐࡒࡖࡣࡇ࡛ࡉࡍࡆࡢࡌࡆ࡙ࡈࡆࡆࡢࡍࡉ࠭ᐋ")] = bstack11l1ll_opy_ (u"ࠣࡰࡸࡰࡱࠨᐌ")
            os.environ[bstack11l1ll_opy_ (u"ࠩࡅࡗࡤ࡚ࡅࡔࡖࡒࡔࡘࡥࡁࡍࡎࡒ࡛ࡤ࡙ࡃࡓࡇࡈࡒࡘࡎࡏࡕࡕࠪᐍ")] = bstack11l1ll_opy_ (u"ࠥࡲࡺࡲ࡬ࠣᐎ")
            bstack1111l1l1ll_opy_ = response.json()
            if bstack1111l1l1ll_opy_ and bstack1111l1l1ll_opy_[bstack11l1ll_opy_ (u"ࠫࡲ࡫ࡳࡴࡣࡪࡩࠬᐏ")]:
                error_message = bstack1111l1l1ll_opy_[bstack11l1ll_opy_ (u"ࠬࡳࡥࡴࡵࡤ࡫ࡪ࠭ᐐ")]
                if bstack1111l1l1ll_opy_[bstack11l1ll_opy_ (u"࠭ࡥࡳࡴࡲࡶ࡙ࡿࡰࡦࠩᐑ")] == bstack11l1ll_opy_ (u"ࠧࡆࡔࡕࡓࡗࡥࡉࡏࡘࡄࡐࡎࡊ࡟ࡄࡔࡈࡈࡊࡔࡔࡊࡃࡏࡗࠬᐒ"):
                    logger.error(error_message)
                elif bstack1111l1l1ll_opy_[bstack11l1ll_opy_ (u"ࠨࡧࡵࡶࡴࡸࡔࡺࡲࡨࠫᐓ")] == bstack11l1ll_opy_ (u"ࠩࡈࡖࡗࡕࡒࡠࡃࡆࡇࡊ࡙ࡓࡠࡆࡈࡒࡎࡋࡄࠨᐔ"):
                    logger.info(error_message)
                elif bstack1111l1l1ll_opy_[bstack11l1ll_opy_ (u"ࠪࡩࡷࡸ࡯ࡳࡖࡼࡴࡪ࠭ᐕ")] == bstack11l1ll_opy_ (u"ࠫࡊࡘࡒࡐࡔࡢࡗࡉࡑ࡟ࡅࡇࡓࡖࡊࡉࡁࡕࡇࡇࠫᐖ"):
                    logger.error(error_message)
                else:
                    logger.error(error_message)
            else:
                logger.error(bstack11l1ll_opy_ (u"ࠧࡊࡡࡵࡣࠣࡹࡵࡲ࡯ࡢࡦࠣࡸࡴࠦࡂࡳࡱࡺࡷࡪࡸࡓࡵࡣࡦ࡯࡚ࠥࡥࡴࡶࠣࡓࡧࡹࡥࡳࡸࡤࡦ࡮ࡲࡩࡵࡻࠣࡪࡦ࡯࡬ࡦࡦࠣࡨࡺ࡫ࠠࡵࡱࠣࡷࡴࡳࡥࠡࡧࡵࡶࡴࡸࠢᐗ"))
            return [None, None, None]
        logger.debug(bstack11l1ll_opy_ (u"࠭ࡔࡦࡵࡷࠤࡔࡨࡳࡦࡴࡹࡥࡧ࡯࡬ࡪࡶࡼࠤࡇࡻࡩ࡭ࡦࠣࡧࡷ࡫ࡡࡵ࡫ࡲࡲ࡙ࠥࡵࡤࡥࡨࡷࡸ࡬ࡵ࡭ࠣࠪᐘ"))
        os.environ[bstack11l1ll_opy_ (u"ࠧࡃࡕࡢࡘࡊ࡙ࡔࡐࡒࡖࡣࡇ࡛ࡉࡍࡆࡢࡇࡔࡓࡐࡍࡇࡗࡉࡉ࠭ᐙ")] = bstack11l1ll_opy_ (u"ࠨࡶࡵࡹࡪ࠭ᐚ")
        bstack1111l1l1ll_opy_ = response.json()
        if bstack1111l1l1ll_opy_.get(bstack11l1ll_opy_ (u"ࠩ࡭ࡻࡹ࠭ᐛ")):
            os.environ[bstack11l1ll_opy_ (u"ࠪࡆࡘࡥࡔࡆࡕࡗࡓࡕ࡙࡟ࡋ࡙ࡗࠫᐜ")] = bstack1111l1l1ll_opy_[bstack11l1ll_opy_ (u"ࠫ࡯ࡽࡴࠨᐝ")]
            os.environ[bstack11l1ll_opy_ (u"ࠬࡉࡒࡆࡆࡈࡒ࡙ࡏࡁࡍࡕࡢࡊࡔࡘ࡟ࡄࡔࡄࡗࡍࡥࡒࡆࡒࡒࡖ࡙ࡏࡎࡈࠩᐞ")] = json.dumps({
                bstack11l1ll_opy_ (u"࠭ࡵࡴࡧࡵࡲࡦࡳࡥࠨᐟ"): bstack11llllllll_opy_,
                bstack11l1ll_opy_ (u"ࠧࡱࡣࡶࡷࡼࡵࡲࡥࠩᐠ"): bstack1l111111ll_opy_
            })
        if bstack1111l1l1ll_opy_.get(bstack11l1ll_opy_ (u"ࠨࡤࡸ࡭ࡱࡪ࡟ࡩࡣࡶ࡬ࡪࡪ࡟ࡪࡦࠪᐡ")):
            os.environ[bstack11l1ll_opy_ (u"ࠩࡅࡗࡤ࡚ࡅࡔࡖࡒࡔࡘࡥࡂࡖࡋࡏࡈࡤࡎࡁࡔࡊࡈࡈࡤࡏࡄࠨᐢ")] = bstack1111l1l1ll_opy_[bstack11l1ll_opy_ (u"ࠪࡦࡺ࡯࡬ࡥࡡ࡫ࡥࡸ࡮ࡥࡥࡡ࡬ࡨࠬᐣ")]
        if bstack1111l1l1ll_opy_.get(bstack11l1ll_opy_ (u"ࠫࡦࡲ࡬ࡰࡹࡢࡷࡨࡸࡥࡦࡰࡶ࡬ࡴࡺࡳࠨᐤ")):
            os.environ[bstack11l1ll_opy_ (u"ࠬࡈࡓࡠࡖࡈࡗ࡙ࡕࡐࡔࡡࡄࡐࡑࡕࡗࡠࡕࡆࡖࡊࡋࡎࡔࡊࡒࡘࡘ࠭ᐥ")] = str(bstack1111l1l1ll_opy_[bstack11l1ll_opy_ (u"࠭ࡡ࡭࡮ࡲࡻࡤࡹࡣࡳࡧࡨࡲࡸ࡮࡯ࡵࡵࠪᐦ")])
        return [bstack1111l1l1ll_opy_[bstack11l1ll_opy_ (u"ࠧ࡫ࡹࡷࠫᐧ")], bstack1111l1l1ll_opy_[bstack11l1ll_opy_ (u"ࠨࡤࡸ࡭ࡱࡪ࡟ࡩࡣࡶ࡬ࡪࡪ࡟ࡪࡦࠪᐨ")], bstack1111l1l1ll_opy_[bstack11l1ll_opy_ (u"ࠩࡤࡰࡱࡵࡷࡠࡵࡦࡶࡪ࡫࡮ࡴࡪࡲࡸࡸ࠭ᐩ")]]
    @classmethod
    @bstack1l1l1ll111_opy_(class_method=True)
    def stop(cls):
        if not cls.on():
            return
        if os.environ[bstack11l1ll_opy_ (u"ࠪࡆࡘࡥࡔࡆࡕࡗࡓࡕ࡙࡟ࡋ࡙ࡗࠫᐪ")] == bstack11l1ll_opy_ (u"ࠦࡳࡻ࡬࡭ࠤᐫ") or os.environ[bstack11l1ll_opy_ (u"ࠬࡈࡓࡠࡖࡈࡗ࡙ࡕࡐࡔࡡࡅ࡙ࡎࡒࡄࡠࡊࡄࡗࡍࡋࡄࡠࡋࡇࠫᐬ")] == bstack11l1ll_opy_ (u"ࠨ࡮ࡶ࡮࡯ࠦᐭ"):
            print(bstack11l1ll_opy_ (u"ࠧࡆ࡚ࡆࡉࡕ࡚ࡉࡐࡐࠣࡍࡓࠦࡳࡵࡱࡳࡆࡺ࡯࡬ࡥࡗࡳࡷࡹࡸࡥࡢ࡯ࠣࡖࡊࡗࡕࡆࡕࡗࠤ࡙ࡕࠠࡕࡇࡖࡘࠥࡕࡂࡔࡇࡕ࡚ࡆࡈࡉࡍࡋࡗ࡝ࠥࡀࠠࡎ࡫ࡶࡷ࡮ࡴࡧࠡࡣࡸࡸ࡭࡫࡮ࡵ࡫ࡦࡥࡹ࡯࡯࡯ࠢࡷࡳࡰ࡫࡮ࠨᐮ"))
            return {
                bstack11l1ll_opy_ (u"ࠨࡵࡷࡥࡹࡻࡳࠨᐯ"): bstack11l1ll_opy_ (u"ࠩࡨࡶࡷࡵࡲࠨᐰ"),
                bstack11l1ll_opy_ (u"ࠪࡱࡪࡹࡳࡢࡩࡨࠫᐱ"): bstack11l1ll_opy_ (u"࡙ࠫࡵ࡫ࡦࡰ࠲ࡦࡺ࡯࡬ࡥࡋࡇࠤ࡮ࡹࠠࡶࡰࡧࡩ࡫࡯࡮ࡦࡦ࠯ࠤࡧࡻࡩ࡭ࡦࠣࡧࡷ࡫ࡡࡵ࡫ࡲࡲࠥࡳࡩࡨࡪࡷࠤ࡭ࡧࡶࡦࠢࡩࡥ࡮ࡲࡥࡥࠩᐲ")
            }
        else:
            cls.bstack111l1l11ll_opy_.shutdown()
            data = {
                bstack11l1ll_opy_ (u"ࠬࡹࡴࡰࡲࡢࡸ࡮ࡳࡥࠨᐳ"): datetime.datetime.now().isoformat()
            }
            config = {
                bstack11l1ll_opy_ (u"࠭ࡨࡦࡣࡧࡩࡷࡹࠧᐴ"): cls.default_headers()
            }
            bstack11l1llll1l_opy_ = bstack11l1ll_opy_ (u"ࠧࡢࡲ࡬࠳ࡻ࠷࠯ࡣࡷ࡬ࡰࡩࡹ࠯ࡼࡿ࠲ࡷࡹࡵࡰࠨᐵ").format(os.environ[bstack11l1ll_opy_ (u"ࠣࡄࡖࡣ࡙ࡋࡓࡕࡑࡓࡗࡤࡈࡕࡊࡎࡇࡣࡍࡇࡓࡉࡇࡇࡣࡎࡊࠢᐶ")])
            bstack1111ll1l1l_opy_ = cls.request_url(bstack11l1llll1l_opy_)
            response = bstack1111l1lll_opy_(bstack11l1ll_opy_ (u"ࠩࡓ࡙࡙࠭ᐷ"), bstack1111ll1l1l_opy_, data, config)
            if not response.ok:
                raise Exception(bstack11l1ll_opy_ (u"ࠥࡗࡹࡵࡰࠡࡴࡨࡵࡺ࡫ࡳࡵࠢࡱࡳࡹࠦ࡯࡬ࠤᐸ"))
    @classmethod
    def bstack1l1l111111_opy_(cls):
        if cls.bstack111l1l11ll_opy_ is None:
            return
        cls.bstack111l1l11ll_opy_.shutdown()
    @classmethod
    def bstack1l1lll1l11_opy_(cls):
        if cls.on():
            print(
                bstack11l1ll_opy_ (u"࡛ࠫ࡯ࡳࡪࡶࠣ࡬ࡹࡺࡰࡴ࠼࠲࠳ࡴࡨࡳࡦࡴࡹࡥࡧ࡯࡬ࡪࡶࡼ࠲ࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭࠱ࡧࡴࡳ࠯ࡣࡷ࡬ࡰࡩࡹ࠯ࡼࡿࠣࡸࡴࠦࡶࡪࡧࡺࠤࡧࡻࡩ࡭ࡦࠣࡶࡪࡶ࡯ࡳࡶ࠯ࠤ࡮ࡴࡳࡪࡩ࡫ࡸࡸ࠲ࠠࡢࡰࡧࠤࡲࡧ࡮ࡺࠢࡰࡳࡷ࡫ࠠࡥࡧࡥࡹ࡬࡭ࡩ࡯ࡩࠣ࡭ࡳ࡬࡯ࡳ࡯ࡤࡸ࡮ࡵ࡮ࠡࡣ࡯ࡰࠥࡧࡴࠡࡱࡱࡩࠥࡶ࡬ࡢࡥࡨࠥࡡࡴࠧᐹ").format(os.environ[bstack11l1ll_opy_ (u"ࠧࡈࡓࡠࡖࡈࡗ࡙ࡕࡐࡔࡡࡅ࡙ࡎࡒࡄࡠࡊࡄࡗࡍࡋࡄࡠࡋࡇࠦᐺ")]))
    @classmethod
    def bstack1111ll1111_opy_(cls):
        if cls.bstack111l1l11ll_opy_ is not None:
            return
        cls.bstack111l1l11ll_opy_ = bstack111l1ll1l1_opy_(cls.bstack1111ll1l11_opy_)
        cls.bstack111l1l11ll_opy_.start()
    @classmethod
    def bstack1l1l11llll_opy_(cls, bstack1l11l1l111_opy_, bstack1111l1ll1l_opy_=bstack11l1ll_opy_ (u"࠭ࡡࡱ࡫࠲ࡺ࠶࠵ࡢࡢࡶࡦ࡬ࠬᐻ")):
        if not cls.on():
            return
        bstack1l1lll1l1l_opy_ = bstack1l11l1l111_opy_[bstack11l1ll_opy_ (u"ࠧࡦࡸࡨࡲࡹࡥࡴࡺࡲࡨࠫᐼ")]
        bstack1111ll11ll_opy_ = {
            bstack11l1ll_opy_ (u"ࠨࡖࡨࡷࡹࡘࡵ࡯ࡕࡷࡥࡷࡺࡥࡥࠩᐽ"): bstack11l1ll_opy_ (u"ࠩࡗࡩࡸࡺ࡟ࡔࡶࡤࡶࡹࡥࡕࡱ࡮ࡲࡥࡩ࠭ᐾ"),
            bstack11l1ll_opy_ (u"ࠪࡘࡪࡹࡴࡓࡷࡱࡊ࡮ࡴࡩࡴࡪࡨࡨࠬᐿ"): bstack11l1ll_opy_ (u"࡙ࠫ࡫ࡳࡵࡡࡈࡲࡩࡥࡕࡱ࡮ࡲࡥࡩ࠭ᑀ"),
            bstack11l1ll_opy_ (u"࡚ࠬࡥࡴࡶࡕࡹࡳ࡙࡫ࡪࡲࡳࡩࡩ࠭ᑁ"): bstack11l1ll_opy_ (u"࠭ࡔࡦࡵࡷࡣࡘࡱࡩࡱࡲࡨࡨࡤ࡛ࡰ࡭ࡱࡤࡨࠬᑂ"),
            bstack11l1ll_opy_ (u"ࠧࡍࡱࡪࡇࡷ࡫ࡡࡵࡧࡧࠫᑃ"): bstack11l1ll_opy_ (u"ࠨࡎࡲ࡫ࡤ࡛ࡰ࡭ࡱࡤࡨࠬᑄ"),
            bstack11l1ll_opy_ (u"ࠩࡋࡳࡴࡱࡒࡶࡰࡖࡸࡦࡸࡴࡦࡦࠪᑅ"): bstack11l1ll_opy_ (u"ࠪࡌࡴࡵ࡫ࡠࡕࡷࡥࡷࡺ࡟ࡖࡲ࡯ࡳࡦࡪࠧᑆ"),
            bstack11l1ll_opy_ (u"ࠫࡍࡵ࡯࡬ࡔࡸࡲࡋ࡯࡮ࡪࡵ࡫ࡩࡩ࠭ᑇ"): bstack11l1ll_opy_ (u"ࠬࡎ࡯ࡰ࡭ࡢࡉࡳࡪ࡟ࡖࡲ࡯ࡳࡦࡪࠧᑈ"),
            bstack11l1ll_opy_ (u"࠭ࡃࡃࡖࡖࡩࡸࡹࡩࡰࡰࡆࡶࡪࡧࡴࡦࡦࠪᑉ"): bstack11l1ll_opy_ (u"ࠧࡄࡄࡗࡣ࡚ࡶ࡬ࡰࡣࡧࠫᑊ")
        }.get(bstack1l1lll1l1l_opy_)
        if bstack1111l1ll1l_opy_ == bstack11l1ll_opy_ (u"ࠨࡣࡳ࡭࠴ࡼ࠱࠰ࡤࡤࡸࡨ࡮ࠧᑋ"):
            cls.bstack1111ll1111_opy_()
            cls.bstack111l1l11ll_opy_.add(bstack1l11l1l111_opy_)
        elif bstack1111l1ll1l_opy_ == bstack11l1ll_opy_ (u"ࠩࡤࡴ࡮࠵ࡶ࠲࠱ࡶࡧࡷ࡫ࡥ࡯ࡵ࡫ࡳࡹࡹࠧᑌ"):
            cls.bstack1111ll1l11_opy_([bstack1l11l1l111_opy_], bstack1111l1ll1l_opy_)
    @classmethod
    @bstack1l1l1ll111_opy_(class_method=True)
    def bstack1111ll1l11_opy_(cls, bstack1l11l1l111_opy_, bstack1111l1ll1l_opy_=bstack11l1ll_opy_ (u"ࠪࡥࡵ࡯࠯ࡷ࠳࠲ࡦࡦࡺࡣࡩࠩᑍ")):
        config = {
            bstack11l1ll_opy_ (u"ࠫ࡭࡫ࡡࡥࡧࡵࡷࠬᑎ"): cls.default_headers()
        }
        response = bstack1111l1lll_opy_(bstack11l1ll_opy_ (u"ࠬࡖࡏࡔࡖࠪᑏ"), cls.request_url(bstack1111l1ll1l_opy_), bstack1l11l1l111_opy_, config)
        bstack1l11111l1l_opy_ = response.json()
    @classmethod
    @bstack1l1l1ll111_opy_(class_method=True)
    def bstack1l1l1l11ll_opy_(cls, bstack1l11l1l11l_opy_):
        bstack1111l1ll11_opy_ = []
        for log in bstack1l11l1l11l_opy_:
            bstack1111l11lll_opy_ = {
                bstack11l1ll_opy_ (u"࠭࡫ࡪࡰࡧࠫᑐ"): bstack11l1ll_opy_ (u"ࠧࡕࡇࡖࡘࡤࡒࡏࡈࠩᑑ"),
                bstack11l1ll_opy_ (u"ࠨ࡮ࡨࡺࡪࡲࠧᑒ"): log[bstack11l1ll_opy_ (u"ࠩ࡯ࡩࡻ࡫࡬ࠨᑓ")],
                bstack11l1ll_opy_ (u"ࠪࡸ࡮ࡳࡥࡴࡶࡤࡱࡵ࠭ᑔ"): log[bstack11l1ll_opy_ (u"ࠫࡹ࡯࡭ࡦࡵࡷࡥࡲࡶࠧᑕ")],
                bstack11l1ll_opy_ (u"ࠬ࡮ࡴࡵࡲࡢࡶࡪࡹࡰࡰࡰࡶࡩࠬᑖ"): {},
                bstack11l1ll_opy_ (u"࠭࡭ࡦࡵࡶࡥ࡬࡫ࠧᑗ"): log[bstack11l1ll_opy_ (u"ࠧ࡮ࡧࡶࡷࡦ࡭ࡥࠨᑘ")],
            }
            if bstack11l1ll_opy_ (u"ࠨࡶࡨࡷࡹࡥࡲࡶࡰࡢࡹࡺ࡯ࡤࠨᑙ") in log:
                bstack1111l11lll_opy_[bstack11l1ll_opy_ (u"ࠩࡷࡩࡸࡺ࡟ࡳࡷࡱࡣࡺࡻࡩࡥࠩᑚ")] = log[bstack11l1ll_opy_ (u"ࠪࡸࡪࡹࡴࡠࡴࡸࡲࡤࡻࡵࡪࡦࠪᑛ")]
            elif bstack11l1ll_opy_ (u"ࠫ࡭ࡵ࡯࡬ࡡࡵࡹࡳࡥࡵࡶ࡫ࡧࠫᑜ") in log:
                bstack1111l11lll_opy_[bstack11l1ll_opy_ (u"ࠬ࡮࡯ࡰ࡭ࡢࡶࡺࡴ࡟ࡶࡷ࡬ࡨࠬᑝ")] = log[bstack11l1ll_opy_ (u"࠭ࡨࡰࡱ࡮ࡣࡷࡻ࡮ࡠࡷࡸ࡭ࡩ࠭ᑞ")]
            bstack1111l1ll11_opy_.append(bstack1111l11lll_opy_)
        cls.bstack1l1l11llll_opy_({
            bstack11l1ll_opy_ (u"ࠧࡦࡸࡨࡲࡹࡥࡴࡺࡲࡨࠫᑟ"): bstack11l1ll_opy_ (u"ࠨࡎࡲ࡫ࡈࡸࡥࡢࡶࡨࡨࠬᑠ"),
            bstack11l1ll_opy_ (u"ࠩ࡯ࡳ࡬ࡹࠧᑡ"): bstack1111l1ll11_opy_
        })
    @classmethod
    @bstack1l1l1ll111_opy_(class_method=True)
    def bstack1111l11l11_opy_(cls, steps):
        bstack1111l1l1l1_opy_ = []
        for step in steps:
            bstack1111l111l1_opy_ = {
                bstack11l1ll_opy_ (u"ࠪ࡯࡮ࡴࡤࠨᑢ"): bstack11l1ll_opy_ (u"࡙ࠫࡋࡓࡕࡡࡖࡘࡊࡖࠧᑣ"),
                bstack11l1ll_opy_ (u"ࠬࡲࡥࡷࡧ࡯ࠫᑤ"): step[bstack11l1ll_opy_ (u"࠭࡬ࡦࡸࡨࡰࠬᑥ")],
                bstack11l1ll_opy_ (u"ࠧࡵ࡫ࡰࡩࡸࡺࡡ࡮ࡲࠪᑦ"): step[bstack11l1ll_opy_ (u"ࠨࡶ࡬ࡱࡪࡹࡴࡢ࡯ࡳࠫᑧ")],
                bstack11l1ll_opy_ (u"ࠩࡰࡩࡸࡹࡡࡨࡧࠪᑨ"): step[bstack11l1ll_opy_ (u"ࠪࡱࡪࡹࡳࡢࡩࡨࠫᑩ")],
                bstack11l1ll_opy_ (u"ࠫࡩࡻࡲࡢࡶ࡬ࡳࡳ࠭ᑪ"): step[bstack11l1ll_opy_ (u"ࠬࡪࡵࡳࡣࡷ࡭ࡴࡴࠧᑫ")]
            }
            if bstack11l1ll_opy_ (u"࠭ࡴࡦࡵࡷࡣࡷࡻ࡮ࡠࡷࡸ࡭ࡩ࠭ᑬ") in step:
                bstack1111l111l1_opy_[bstack11l1ll_opy_ (u"ࠧࡵࡧࡶࡸࡤࡸࡵ࡯ࡡࡸࡹ࡮ࡪࠧᑭ")] = step[bstack11l1ll_opy_ (u"ࠨࡶࡨࡷࡹࡥࡲࡶࡰࡢࡹࡺ࡯ࡤࠨᑮ")]
            elif bstack11l1ll_opy_ (u"ࠩ࡫ࡳࡴࡱ࡟ࡳࡷࡱࡣࡺࡻࡩࡥࠩᑯ") in step:
                bstack1111l111l1_opy_[bstack11l1ll_opy_ (u"ࠪ࡬ࡴࡵ࡫ࡠࡴࡸࡲࡤࡻࡵࡪࡦࠪᑰ")] = step[bstack11l1ll_opy_ (u"ࠫ࡭ࡵ࡯࡬ࡡࡵࡹࡳࡥࡵࡶ࡫ࡧࠫᑱ")]
            bstack1111l1l1l1_opy_.append(bstack1111l111l1_opy_)
        cls.bstack1l1l11llll_opy_({
            bstack11l1ll_opy_ (u"ࠬ࡫ࡶࡦࡰࡷࡣࡹࡿࡰࡦࠩᑲ"): bstack11l1ll_opy_ (u"࠭ࡌࡰࡩࡆࡶࡪࡧࡴࡦࡦࠪᑳ"),
            bstack11l1ll_opy_ (u"ࠧ࡭ࡱࡪࡷࠬᑴ"): bstack1111l1l1l1_opy_
        })
    @classmethod
    @bstack1l1l1ll111_opy_(class_method=True)
    def bstack1lll11ll_opy_(cls, screenshot):
        cls.bstack1l1l11llll_opy_({
            bstack11l1ll_opy_ (u"ࠨࡧࡹࡩࡳࡺ࡟ࡵࡻࡳࡩࠬᑵ"): bstack11l1ll_opy_ (u"ࠩࡏࡳ࡬ࡉࡲࡦࡣࡷࡩࡩ࠭ᑶ"),
            bstack11l1ll_opy_ (u"ࠪࡰࡴ࡭ࡳࠨᑷ"): [{
                bstack11l1ll_opy_ (u"ࠫࡰ࡯࡮ࡥࠩᑸ"): bstack11l1ll_opy_ (u"࡚ࠬࡅࡔࡖࡢࡗࡈࡘࡅࡆࡐࡖࡌࡔ࡚ࠧᑹ"),
                bstack11l1ll_opy_ (u"࠭ࡴࡪ࡯ࡨࡷࡹࡧ࡭ࡱࠩᑺ"): datetime.datetime.utcnow().isoformat() + bstack11l1ll_opy_ (u"࡛ࠧࠩᑻ"),
                bstack11l1ll_opy_ (u"ࠨ࡯ࡨࡷࡸࡧࡧࡦࠩᑼ"): screenshot[bstack11l1ll_opy_ (u"ࠩ࡬ࡱࡦ࡭ࡥࠨᑽ")],
                bstack11l1ll_opy_ (u"ࠪࡸࡪࡹࡴࡠࡴࡸࡲࡤࡻࡵࡪࡦࠪᑾ"): screenshot[bstack11l1ll_opy_ (u"ࠫࡹ࡫ࡳࡵࡡࡵࡹࡳࡥࡵࡶ࡫ࡧࠫᑿ")]
            }]
        }, bstack1111l1ll1l_opy_=bstack11l1ll_opy_ (u"ࠬࡧࡰࡪ࠱ࡹ࠵࠴ࡹࡣࡳࡧࡨࡲࡸ࡮࡯ࡵࡵࠪᒀ"))
    @classmethod
    @bstack1l1l1ll111_opy_(class_method=True)
    def bstack111111111_opy_(cls, driver):
        current_test_uuid = cls.current_test_uuid()
        if not current_test_uuid:
            return
        cls.bstack1l1l11llll_opy_({
            bstack11l1ll_opy_ (u"࠭ࡥࡷࡧࡱࡸࡤࡺࡹࡱࡧࠪᒁ"): bstack11l1ll_opy_ (u"ࠧࡄࡄࡗࡗࡪࡹࡳࡪࡱࡱࡇࡷ࡫ࡡࡵࡧࡧࠫᒂ"),
            bstack11l1ll_opy_ (u"ࠨࡶࡨࡷࡹࡥࡲࡶࡰࠪᒃ"): {
                bstack11l1ll_opy_ (u"ࠤࡸࡹ࡮ࡪࠢᒄ"): cls.current_test_uuid(),
                bstack11l1ll_opy_ (u"ࠥ࡭ࡳࡺࡥࡨࡴࡤࡸ࡮ࡵ࡮ࡴࠤᒅ"): cls.bstack1l11ll111l_opy_(driver)
            }
        })
    @classmethod
    def on(cls):
        if os.environ.get(bstack11l1ll_opy_ (u"ࠫࡇ࡙࡟ࡕࡇࡖࡘࡔࡖࡓࡠࡌ࡚ࡘࠬᒆ"), None) is None or os.environ[bstack11l1ll_opy_ (u"ࠬࡈࡓࡠࡖࡈࡗ࡙ࡕࡐࡔࡡࡍ࡛࡙࠭ᒇ")] == bstack11l1ll_opy_ (u"ࠨ࡮ࡶ࡮࡯ࠦᒈ"):
            return False
        return True
    @classmethod
    def bstack1111l111ll_opy_(cls):
        return bstack111l1l1l1_opy_(cls.bs_config.get(bstack11l1ll_opy_ (u"ࠧࡵࡧࡶࡸࡔࡨࡳࡦࡴࡹࡥࡧ࡯࡬ࡪࡶࡼࠫᒉ"), False))
    @staticmethod
    def request_url(url):
        return bstack11l1ll_opy_ (u"ࠨࡽࢀ࠳ࢀࢃࠧᒊ").format(bstack1111ll111l_opy_, url)
    @staticmethod
    def default_headers():
        headers = {
            bstack11l1ll_opy_ (u"ࠩࡆࡳࡳࡺࡥ࡯ࡶ࠰ࡘࡾࡶࡥࠨᒋ"): bstack11l1ll_opy_ (u"ࠪࡥࡵࡶ࡬ࡪࡥࡤࡸ࡮ࡵ࡮࠰࡬ࡶࡳࡳ࠭ᒌ"),
            bstack11l1ll_opy_ (u"ࠫ࡝࠳ࡂࡔࡖࡄࡇࡐ࠳ࡔࡆࡕࡗࡓࡕ࡙ࠧᒍ"): bstack11l1ll_opy_ (u"ࠬࡺࡲࡶࡧࠪᒎ")
        }
        if os.environ.get(bstack11l1ll_opy_ (u"࠭ࡂࡔࡡࡗࡉࡘ࡚ࡏࡑࡕࡢࡎ࡜࡚ࠧᒏ"), None):
            headers[bstack11l1ll_opy_ (u"ࠧࡂࡷࡷ࡬ࡴࡸࡩࡻࡣࡷ࡭ࡴࡴࠧᒐ")] = bstack11l1ll_opy_ (u"ࠨࡄࡨࡥࡷ࡫ࡲࠡࡽࢀࠫᒑ").format(os.environ[bstack11l1ll_opy_ (u"ࠤࡅࡗࡤ࡚ࡅࡔࡖࡒࡔࡘࡥࡊࡘࡖࠥᒒ")])
        return headers
    @staticmethod
    def current_test_uuid():
        return getattr(threading.current_thread(), bstack11l1ll_opy_ (u"ࠪࡧࡺࡸࡲࡦࡰࡷࡣࡹ࡫ࡳࡵࡡࡸࡹ࡮ࡪࠧᒓ"), None)
    @staticmethod
    def current_hook_uuid():
        return getattr(threading.current_thread(), bstack11l1ll_opy_ (u"ࠫࡨࡻࡲࡳࡧࡱࡸࡤ࡮࡯ࡰ࡭ࡢࡹࡺ࡯ࡤࠨᒔ"), None)
    @staticmethod
    def bstack1l1l1111l1_opy_():
        if getattr(threading.current_thread(), bstack11l1ll_opy_ (u"ࠬࡩࡵࡳࡴࡨࡲࡹࡥࡴࡦࡵࡷࡣࡺࡻࡩࡥࠩᒕ"), None):
            return {
                bstack11l1ll_opy_ (u"࠭ࡴࡺࡲࡨࠫᒖ"): bstack11l1ll_opy_ (u"ࠧࡵࡧࡶࡸࠬᒗ"),
                bstack11l1ll_opy_ (u"ࠨࡶࡨࡷࡹࡥࡲࡶࡰࡢࡹࡺ࡯ࡤࠨᒘ"): getattr(threading.current_thread(), bstack11l1ll_opy_ (u"ࠩࡦࡹࡷࡸࡥ࡯ࡶࡢࡸࡪࡹࡴࡠࡷࡸ࡭ࡩ࠭ᒙ"), None)
            }
        if getattr(threading.current_thread(), bstack11l1ll_opy_ (u"ࠪࡧࡺࡸࡲࡦࡰࡷࡣ࡭ࡵ࡯࡬ࡡࡸࡹ࡮ࡪࠧᒚ"), None):
            return {
                bstack11l1ll_opy_ (u"ࠫࡹࡿࡰࡦࠩᒛ"): bstack11l1ll_opy_ (u"ࠬ࡮࡯ࡰ࡭ࠪᒜ"),
                bstack11l1ll_opy_ (u"࠭ࡨࡰࡱ࡮ࡣࡷࡻ࡮ࡠࡷࡸ࡭ࡩ࠭ᒝ"): getattr(threading.current_thread(), bstack11l1ll_opy_ (u"ࠧࡤࡷࡵࡶࡪࡴࡴࡠࡪࡲࡳࡰࡥࡵࡶ࡫ࡧࠫᒞ"), None)
            }
        return None
    @staticmethod
    def bstack1l11ll111l_opy_(driver):
        return {
            bstack11lll11111_opy_(): bstack11ll1ll1l1_opy_(driver)
        }
    @staticmethod
    def bstack1111ll11l1_opy_(exception_info, report):
        return [{bstack11l1ll_opy_ (u"ࠨࡤࡤࡧࡰࡺࡲࡢࡥࡨࠫᒟ"): [exception_info.exconly(), report.longreprtext]}]
    @staticmethod
    def bstack1l111l1l11_opy_(typename):
        if bstack11l1ll_opy_ (u"ࠤࡄࡷࡸ࡫ࡲࡵ࡫ࡲࡲࠧᒠ") in typename:
            return bstack11l1ll_opy_ (u"ࠥࡅࡸࡹࡥࡳࡶ࡬ࡳࡳࡋࡲࡳࡱࡵࠦᒡ")
        return bstack11l1ll_opy_ (u"࡚ࠦࡴࡨࡢࡰࡧࡰࡪࡪࡅࡳࡴࡲࡶࠧᒢ")
    @staticmethod
    def bstack1111l11l1l_opy_(func):
        def wrap(*args, **kwargs):
            if bstack11l1ll11_opy_.on():
                return func(*args, **kwargs)
            return
        return wrap
    @staticmethod
    def bstack1l11l1ll1l_opy_(test, hook_name=None):
        bstack1111l11ll1_opy_ = test.parent
        if hook_name in [bstack11l1ll_opy_ (u"ࠬࡹࡥࡵࡷࡳࡣࡨࡲࡡࡴࡵࠪᒣ"), bstack11l1ll_opy_ (u"࠭ࡴࡦࡣࡵࡨࡴࡽ࡮ࡠࡥ࡯ࡥࡸࡹࠧᒤ"), bstack11l1ll_opy_ (u"ࠧࡴࡧࡷࡹࡵࡥ࡭ࡰࡦࡸࡰࡪ࠭ᒥ"), bstack11l1ll_opy_ (u"ࠨࡶࡨࡥࡷࡪ࡯ࡸࡰࡢࡱࡴࡪࡵ࡭ࡧࠪᒦ")]:
            bstack1111l11ll1_opy_ = test
        scope = []
        while bstack1111l11ll1_opy_ is not None:
            scope.append(bstack1111l11ll1_opy_.name)
            bstack1111l11ll1_opy_ = bstack1111l11ll1_opy_.parent
        scope.reverse()
        return scope[2:]
    @staticmethod
    def bstack1111l1lll1_opy_(hook_type):
        if hook_type == bstack11l1ll_opy_ (u"ࠤࡅࡉࡋࡕࡒࡆࡡࡈࡅࡈࡎࠢᒧ"):
            return bstack11l1ll_opy_ (u"ࠥࡗࡪࡺࡵࡱࠢ࡫ࡳࡴࡱࠢᒨ")
        elif hook_type == bstack11l1ll_opy_ (u"ࠦࡆࡌࡔࡆࡔࡢࡉࡆࡉࡈࠣᒩ"):
            return bstack11l1ll_opy_ (u"࡚ࠧࡥࡢࡴࡧࡳࡼࡴࠠࡩࡱࡲ࡯ࠧᒪ")
    @staticmethod
    def bstack1111l1l11l_opy_(bstack1ll1111l_opy_):
        try:
            if not bstack11l1ll11_opy_.on():
                return bstack1ll1111l_opy_
            if os.environ.get(bstack11l1ll_opy_ (u"ࠨࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤࡘࡅࡓࡗࡑࠦᒫ"), None) == bstack11l1ll_opy_ (u"ࠢࡵࡴࡸࡩࠧᒬ"):
                tests = os.environ.get(bstack11l1ll_opy_ (u"ࠣࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡓࡇࡕ࡙ࡓࡥࡔࡆࡕࡗࡗࠧᒭ"), None)
                if tests is None or tests == bstack11l1ll_opy_ (u"ࠤࡱࡹࡱࡲࠢᒮ"):
                    return bstack1ll1111l_opy_
                bstack1ll1111l_opy_ = tests.split(bstack11l1ll_opy_ (u"ࠪ࠰ࠬᒯ"))
                return bstack1ll1111l_opy_
        except Exception as exc:
            print(bstack11l1ll_opy_ (u"ࠦࡊࡾࡣࡦࡲࡷ࡭ࡴࡴࠠࡪࡰࠣࡶࡪࡸࡵ࡯ࠢ࡫ࡥࡳࡪ࡬ࡦࡴ࠽ࠤࠧᒰ"), str(exc))
        return bstack1ll1111l_opy_
    @classmethod
    def bstack1l1l1ll1ll_opy_(cls, event: str, bstack1l11l1l111_opy_: bstack1l11llllll_opy_):
        bstack1l1l1lll11_opy_ = {
            bstack11l1ll_opy_ (u"ࠬ࡫ࡶࡦࡰࡷࡣࡹࡿࡰࡦࠩᒱ"): event,
            bstack1l11l1l111_opy_.bstack1l11l1llll_opy_(): bstack1l11l1l111_opy_.bstack1l11llll11_opy_(event)
        }
        bstack11l1ll11_opy_.bstack1l1l11llll_opy_(bstack1l1l1lll11_opy_)