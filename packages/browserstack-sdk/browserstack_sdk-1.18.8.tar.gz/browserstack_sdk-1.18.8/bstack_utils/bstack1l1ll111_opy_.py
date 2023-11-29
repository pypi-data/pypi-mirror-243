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
import datetime
import json
import logging
import os
import threading
from bstack_utils.helper import bstack1l11111l11_opy_, bstack1lll1l1ll_opy_, get_host_info, bstack1l1111llll_opy_, bstack1l111111ll_opy_, bstack11ll11l11l_opy_, \
    bstack11ll1l11ll_opy_, bstack11ll1ll11l_opy_, bstack1ll11l1111_opy_, bstack11ll1l111l_opy_, bstack1111llll_opy_, bstack1l11ll1ll1_opy_
from bstack_utils.bstack111l1ll11l_opy_ import bstack111l1lll1l_opy_
from bstack_utils.bstack1l11l1l1ll_opy_ import bstack1l1l111111_opy_
bstack1111l1l1ll_opy_ = [
    bstack11l1l1l_opy_ (u"ࠪࡐࡴ࡭ࡃࡳࡧࡤࡸࡪࡪࠧᏤ"), bstack11l1l1l_opy_ (u"ࠫࡈࡈࡔࡔࡧࡶࡷ࡮ࡵ࡮ࡄࡴࡨࡥࡹ࡫ࡤࠨᏥ"), bstack11l1l1l_opy_ (u"࡚ࠬࡥࡴࡶࡕࡹࡳࡌࡩ࡯࡫ࡶ࡬ࡪࡪࠧᏦ"), bstack11l1l1l_opy_ (u"࠭ࡔࡦࡵࡷࡖࡺࡴࡓ࡬࡫ࡳࡴࡪࡪࠧᏧ"),
    bstack11l1l1l_opy_ (u"ࠧࡉࡱࡲ࡯ࡗࡻ࡮ࡇ࡫ࡱ࡭ࡸ࡮ࡥࡥࠩᏨ"), bstack11l1l1l_opy_ (u"ࠨࡖࡨࡷࡹࡘࡵ࡯ࡕࡷࡥࡷࡺࡥࡥࠩᏩ"), bstack11l1l1l_opy_ (u"ࠩࡋࡳࡴࡱࡒࡶࡰࡖࡸࡦࡸࡴࡦࡦࠪᏪ")
]
bstack1111ll11l1_opy_ = bstack11l1l1l_opy_ (u"ࠪ࡬ࡹࡺࡰࡴ࠼࠲࠳ࡨࡵ࡬࡭ࡧࡦࡸࡴࡸ࠭ࡰࡤࡶࡩࡷࡼࡡࡣ࡫࡯࡭ࡹࡿ࠮ࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠴ࡣࡰ࡯ࠪᏫ")
logger = logging.getLogger(__name__)
class bstack1l11l11l_opy_:
    bstack111l1ll11l_opy_ = None
    bs_config = None
    @classmethod
    @bstack1l11ll1ll1_opy_(class_method=True)
    def launch(cls, bs_config, bstack1111ll1111_opy_):
        cls.bs_config = bs_config
        if not cls.bstack1111l1l111_opy_():
            return
        cls.bstack1111l1lll1_opy_()
        bstack1l111l1l1l_opy_ = bstack1l1111llll_opy_(bs_config)
        bstack1l1111l11l_opy_ = bstack1l111111ll_opy_(bs_config)
        data = {
            bstack11l1l1l_opy_ (u"ࠫ࡫ࡵࡲ࡮ࡣࡷࠫᏬ"): bstack11l1l1l_opy_ (u"ࠬࡰࡳࡰࡰࠪᏭ"),
            bstack11l1l1l_opy_ (u"࠭ࡰࡳࡱ࡭ࡩࡨࡺ࡟࡯ࡣࡰࡩࠬᏮ"): bs_config.get(bstack11l1l1l_opy_ (u"ࠧࡱࡴࡲ࡮ࡪࡩࡴࡏࡣࡰࡩࠬᏯ"), bstack11l1l1l_opy_ (u"ࠨࠩᏰ")),
            bstack11l1l1l_opy_ (u"ࠩࡱࡥࡲ࡫ࠧᏱ"): bs_config.get(bstack11l1l1l_opy_ (u"ࠪࡦࡺ࡯࡬ࡥࡐࡤࡱࡪ࠭Ᏺ"), os.path.basename(os.path.abspath(os.getcwd()))),
            bstack11l1l1l_opy_ (u"ࠫࡧࡻࡩ࡭ࡦࡢ࡭ࡩ࡫࡮ࡵ࡫ࡩ࡭ࡪࡸࠧᏳ"): bs_config.get(bstack11l1l1l_opy_ (u"ࠬࡨࡵࡪ࡮ࡧࡍࡩ࡫࡮ࡵ࡫ࡩ࡭ࡪࡸࠧᏴ")),
            bstack11l1l1l_opy_ (u"࠭ࡤࡦࡵࡦࡶ࡮ࡶࡴࡪࡱࡱࠫᏵ"): bs_config.get(bstack11l1l1l_opy_ (u"ࠧࡣࡷ࡬ࡰࡩࡊࡥࡴࡥࡵ࡭ࡵࡺࡩࡰࡰࠪ᏶"), bstack11l1l1l_opy_ (u"ࠨࠩ᏷")),
            bstack11l1l1l_opy_ (u"ࠩࡶࡸࡦࡸࡴࡠࡶ࡬ࡱࡪ࠭ᏸ"): datetime.datetime.now().isoformat(),
            bstack11l1l1l_opy_ (u"ࠪࡸࡦ࡭ࡳࠨᏹ"): bstack11ll11l11l_opy_(bs_config),
            bstack11l1l1l_opy_ (u"ࠫ࡭ࡵࡳࡵࡡ࡬ࡲ࡫ࡵࠧᏺ"): get_host_info(),
            bstack11l1l1l_opy_ (u"ࠬࡩࡩࡠ࡫ࡱࡪࡴ࠭ᏻ"): bstack1lll1l1ll_opy_(),
            bstack11l1l1l_opy_ (u"࠭ࡢࡶ࡫࡯ࡨࡤࡸࡵ࡯ࡡ࡬ࡨࡪࡴࡴࡪࡨ࡬ࡩࡷ࠭ᏼ"): os.environ.get(bstack11l1l1l_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡂࡖࡋࡏࡈࡤࡘࡕࡏࡡࡌࡈࡊࡔࡔࡊࡈࡌࡉࡗ࠭ᏽ")),
            bstack11l1l1l_opy_ (u"ࠨࡨࡤ࡭ࡱ࡫ࡤࡠࡶࡨࡷࡹࡹ࡟ࡳࡧࡵࡹࡳ࠭᏾"): os.environ.get(bstack11l1l1l_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡔࡈࡖ࡚ࡔࠧ᏿"), False),
            bstack11l1l1l_opy_ (u"ࠪࡺࡪࡸࡳࡪࡱࡱࡣࡨࡵ࡮ࡵࡴࡲࡰࠬ᐀"): bstack1l11111l11_opy_(),
            bstack11l1l1l_opy_ (u"ࠫࡴࡨࡳࡦࡴࡹࡥࡧ࡯࡬ࡪࡶࡼࡣࡻ࡫ࡲࡴ࡫ࡲࡲࠬᐁ"): {
                bstack11l1l1l_opy_ (u"ࠬ࡬ࡲࡢ࡯ࡨࡻࡴࡸ࡫ࡏࡣࡰࡩࠬᐂ"): bstack1111ll1111_opy_.get(bstack11l1l1l_opy_ (u"࠭ࡦࡳࡣࡰࡩࡼࡵࡲ࡬ࡡࡱࡥࡲ࡫ࠧᐃ"), bstack11l1l1l_opy_ (u"ࠧࡑࡻࡷࡩࡸࡺࠧᐄ")),
                bstack11l1l1l_opy_ (u"ࠨࡨࡵࡥࡲ࡫ࡷࡰࡴ࡮࡚ࡪࡸࡳࡪࡱࡱࠫᐅ"): bstack1111ll1111_opy_.get(bstack11l1l1l_opy_ (u"ࠩࡩࡶࡦࡳࡥࡸࡱࡵ࡯ࡤࡼࡥࡳࡵ࡬ࡳࡳ࠭ᐆ")),
                bstack11l1l1l_opy_ (u"ࠪࡷࡩࡱࡖࡦࡴࡶ࡭ࡴࡴࠧᐇ"): bstack1111ll1111_opy_.get(bstack11l1l1l_opy_ (u"ࠫࡸࡪ࡫ࡠࡸࡨࡶࡸ࡯࡯࡯ࠩᐈ"))
            }
        }
        config = {
            bstack11l1l1l_opy_ (u"ࠬࡧࡵࡵࡪࠪᐉ"): (bstack1l111l1l1l_opy_, bstack1l1111l11l_opy_),
            bstack11l1l1l_opy_ (u"࠭ࡨࡦࡣࡧࡩࡷࡹࠧᐊ"): cls.default_headers()
        }
        response = bstack1ll11l1111_opy_(bstack11l1l1l_opy_ (u"ࠧࡑࡑࡖࡘࠬᐋ"), cls.request_url(bstack11l1l1l_opy_ (u"ࠨࡣࡳ࡭࠴ࡼ࠱࠰ࡤࡸ࡭ࡱࡪࡳࠨᐌ")), data, config)
        if response.status_code != 200:
            os.environ[bstack11l1l1l_opy_ (u"ࠩࡅࡗࡤ࡚ࡅࡔࡖࡒࡔࡘࡥࡂࡖࡋࡏࡈࡤࡉࡏࡎࡒࡏࡉ࡙ࡋࡄࠨᐍ")] = bstack11l1l1l_opy_ (u"ࠪࡪࡦࡲࡳࡦࠩᐎ")
            os.environ[bstack11l1l1l_opy_ (u"ࠫࡇ࡙࡟ࡕࡇࡖࡘࡔࡖࡓࡠࡌ࡚ࡘࠬᐏ")] = bstack11l1l1l_opy_ (u"ࠬࡴࡵ࡭࡮ࠪᐐ")
            os.environ[bstack11l1l1l_opy_ (u"࠭ࡂࡔࡡࡗࡉࡘ࡚ࡏࡑࡕࡢࡆ࡚ࡏࡌࡅࡡࡋࡅࡘࡎࡅࡅࡡࡌࡈࠬᐑ")] = bstack11l1l1l_opy_ (u"ࠢ࡯ࡷ࡯ࡰࠧᐒ")
            os.environ[bstack11l1l1l_opy_ (u"ࠨࡄࡖࡣ࡙ࡋࡓࡕࡑࡓࡗࡤࡇࡌࡍࡑ࡚ࡣࡘࡉࡒࡆࡇࡑࡗࡍࡕࡔࡔࠩᐓ")] = bstack11l1l1l_opy_ (u"ࠤࡱࡹࡱࡲࠢᐔ")
            bstack1111l11l1l_opy_ = response.json()
            if bstack1111l11l1l_opy_ and bstack1111l11l1l_opy_[bstack11l1l1l_opy_ (u"ࠪࡱࡪࡹࡳࡢࡩࡨࠫᐕ")]:
                error_message = bstack1111l11l1l_opy_[bstack11l1l1l_opy_ (u"ࠫࡲ࡫ࡳࡴࡣࡪࡩࠬᐖ")]
                if bstack1111l11l1l_opy_[bstack11l1l1l_opy_ (u"ࠬ࡫ࡲࡳࡱࡵࡘࡾࡶࡥࠨᐗ")] == bstack11l1l1l_opy_ (u"࠭ࡅࡓࡔࡒࡖࡤࡏࡎࡗࡃࡏࡍࡉࡥࡃࡓࡇࡇࡉࡓ࡚ࡉࡂࡎࡖࠫᐘ"):
                    logger.error(error_message)
                elif bstack1111l11l1l_opy_[bstack11l1l1l_opy_ (u"ࠧࡦࡴࡵࡳࡷ࡚ࡹࡱࡧࠪᐙ")] == bstack11l1l1l_opy_ (u"ࠨࡇࡕࡖࡔࡘ࡟ࡂࡅࡆࡉࡘ࡙࡟ࡅࡇࡑࡍࡊࡊࠧᐚ"):
                    logger.info(error_message)
                elif bstack1111l11l1l_opy_[bstack11l1l1l_opy_ (u"ࠩࡨࡶࡷࡵࡲࡕࡻࡳࡩࠬᐛ")] == bstack11l1l1l_opy_ (u"ࠪࡉࡗࡘࡏࡓࡡࡖࡈࡐࡥࡄࡆࡒࡕࡉࡈࡇࡔࡆࡆࠪᐜ"):
                    logger.error(error_message)
                else:
                    logger.error(error_message)
            else:
                logger.error(bstack11l1l1l_opy_ (u"ࠦࡉࡧࡴࡢࠢࡸࡴࡱࡵࡡࡥࠢࡷࡳࠥࡈࡲࡰࡹࡶࡩࡷ࡙ࡴࡢࡥ࡮ࠤ࡙࡫ࡳࡵࠢࡒࡦࡸ࡫ࡲࡷࡣࡥ࡭ࡱ࡯ࡴࡺࠢࡩࡥ࡮ࡲࡥࡥࠢࡧࡹࡪࠦࡴࡰࠢࡶࡳࡲ࡫ࠠࡦࡴࡵࡳࡷࠨᐝ"))
            return [None, None, None]
        logger.debug(bstack11l1l1l_opy_ (u"࡚ࠬࡥࡴࡶࠣࡓࡧࡹࡥࡳࡸࡤࡦ࡮ࡲࡩࡵࡻࠣࡆࡺ࡯࡬ࡥࠢࡦࡶࡪࡧࡴࡪࡱࡱࠤࡘࡻࡣࡤࡧࡶࡷ࡫ࡻ࡬ࠢࠩᐞ"))
        os.environ[bstack11l1l1l_opy_ (u"࠭ࡂࡔࡡࡗࡉࡘ࡚ࡏࡑࡕࡢࡆ࡚ࡏࡌࡅࡡࡆࡓࡒࡖࡌࡆࡖࡈࡈࠬᐟ")] = bstack11l1l1l_opy_ (u"ࠧࡵࡴࡸࡩࠬᐠ")
        bstack1111l11l1l_opy_ = response.json()
        if bstack1111l11l1l_opy_.get(bstack11l1l1l_opy_ (u"ࠨ࡬ࡺࡸࠬᐡ")):
            os.environ[bstack11l1l1l_opy_ (u"ࠩࡅࡗࡤ࡚ࡅࡔࡖࡒࡔࡘࡥࡊࡘࡖࠪᐢ")] = bstack1111l11l1l_opy_[bstack11l1l1l_opy_ (u"ࠪ࡮ࡼࡺࠧᐣ")]
            os.environ[bstack11l1l1l_opy_ (u"ࠫࡈࡘࡅࡅࡇࡑࡘࡎࡇࡌࡔࡡࡉࡓࡗࡥࡃࡓࡃࡖࡌࡤࡘࡅࡑࡑࡕࡘࡎࡔࡇࠨᐤ")] = json.dumps({
                bstack11l1l1l_opy_ (u"ࠬࡻࡳࡦࡴࡱࡥࡲ࡫ࠧᐥ"): bstack1l111l1l1l_opy_,
                bstack11l1l1l_opy_ (u"࠭ࡰࡢࡵࡶࡻࡴࡸࡤࠨᐦ"): bstack1l1111l11l_opy_
            })
        if bstack1111l11l1l_opy_.get(bstack11l1l1l_opy_ (u"ࠧࡣࡷ࡬ࡰࡩࡥࡨࡢࡵ࡫ࡩࡩࡥࡩࡥࠩᐧ")):
            os.environ[bstack11l1l1l_opy_ (u"ࠨࡄࡖࡣ࡙ࡋࡓࡕࡑࡓࡗࡤࡈࡕࡊࡎࡇࡣࡍࡇࡓࡉࡇࡇࡣࡎࡊࠧᐨ")] = bstack1111l11l1l_opy_[bstack11l1l1l_opy_ (u"ࠩࡥࡹ࡮ࡲࡤࡠࡪࡤࡷ࡭࡫ࡤࡠ࡫ࡧࠫᐩ")]
        if bstack1111l11l1l_opy_.get(bstack11l1l1l_opy_ (u"ࠪࡥࡱࡲ࡯ࡸࡡࡶࡧࡷ࡫ࡥ࡯ࡵ࡫ࡳࡹࡹࠧᐪ")):
            os.environ[bstack11l1l1l_opy_ (u"ࠫࡇ࡙࡟ࡕࡇࡖࡘࡔࡖࡓࡠࡃࡏࡐࡔ࡝࡟ࡔࡅࡕࡉࡊࡔࡓࡉࡑࡗࡗࠬᐫ")] = str(bstack1111l11l1l_opy_[bstack11l1l1l_opy_ (u"ࠬࡧ࡬࡭ࡱࡺࡣࡸࡩࡲࡦࡧࡱࡷ࡭ࡵࡴࡴࠩᐬ")])
        return [bstack1111l11l1l_opy_[bstack11l1l1l_opy_ (u"࠭ࡪࡸࡶࠪᐭ")], bstack1111l11l1l_opy_[bstack11l1l1l_opy_ (u"ࠧࡣࡷ࡬ࡰࡩࡥࡨࡢࡵ࡫ࡩࡩࡥࡩࡥࠩᐮ")], bstack1111l11l1l_opy_[bstack11l1l1l_opy_ (u"ࠨࡣ࡯ࡰࡴࡽ࡟ࡴࡥࡵࡩࡪࡴࡳࡩࡱࡷࡷࠬᐯ")]]
    @classmethod
    @bstack1l11ll1ll1_opy_(class_method=True)
    def stop(cls):
        if not cls.on():
            return
        if os.environ[bstack11l1l1l_opy_ (u"ࠩࡅࡗࡤ࡚ࡅࡔࡖࡒࡔࡘࡥࡊࡘࡖࠪᐰ")] == bstack11l1l1l_opy_ (u"ࠥࡲࡺࡲ࡬ࠣᐱ") or os.environ[bstack11l1l1l_opy_ (u"ࠫࡇ࡙࡟ࡕࡇࡖࡘࡔࡖࡓࡠࡄࡘࡍࡑࡊ࡟ࡉࡃࡖࡌࡊࡊ࡟ࡊࡆࠪᐲ")] == bstack11l1l1l_opy_ (u"ࠧࡴࡵ࡭࡮ࠥᐳ"):
            print(bstack11l1l1l_opy_ (u"࠭ࡅ࡙ࡅࡈࡔ࡙ࡏࡏࡏࠢࡌࡒࠥࡹࡴࡰࡲࡅࡹ࡮ࡲࡤࡖࡲࡶࡸࡷ࡫ࡡ࡮ࠢࡕࡉࡖ࡛ࡅࡔࡖࠣࡘࡔࠦࡔࡆࡕࡗࠤࡔࡈࡓࡆࡔ࡙ࡅࡇࡏࡌࡊࡖ࡜ࠤ࠿ࠦࡍࡪࡵࡶ࡭ࡳ࡭ࠠࡢࡷࡷ࡬ࡪࡴࡴࡪࡥࡤࡸ࡮ࡵ࡮ࠡࡶࡲ࡯ࡪࡴࠧᐴ"))
            return {
                bstack11l1l1l_opy_ (u"ࠧࡴࡶࡤࡸࡺࡹࠧᐵ"): bstack11l1l1l_opy_ (u"ࠨࡧࡵࡶࡴࡸࠧᐶ"),
                bstack11l1l1l_opy_ (u"ࠩࡰࡩࡸࡹࡡࡨࡧࠪᐷ"): bstack11l1l1l_opy_ (u"ࠪࡘࡴࡱࡥ࡯࠱ࡥࡹ࡮ࡲࡤࡊࡆࠣ࡭ࡸࠦࡵ࡯ࡦࡨࡪ࡮ࡴࡥࡥ࠮ࠣࡦࡺ࡯࡬ࡥࠢࡦࡶࡪࡧࡴࡪࡱࡱࠤࡲ࡯ࡧࡩࡶࠣ࡬ࡦࡼࡥࠡࡨࡤ࡭ࡱ࡫ࡤࠨᐸ")
            }
        else:
            cls.bstack111l1ll11l_opy_.shutdown()
            data = {
                bstack11l1l1l_opy_ (u"ࠫࡸࡺ࡯ࡱࡡࡷ࡭ࡲ࡫ࠧᐹ"): datetime.datetime.now().isoformat()
            }
            config = {
                bstack11l1l1l_opy_ (u"ࠬ࡮ࡥࡢࡦࡨࡶࡸ࠭ᐺ"): cls.default_headers()
            }
            bstack11ll1l11l1_opy_ = bstack11l1l1l_opy_ (u"࠭ࡡࡱ࡫࠲ࡺ࠶࠵ࡢࡶ࡫࡯ࡨࡸ࠵ࡻࡾ࠱ࡶࡸࡴࡶࠧᐻ").format(os.environ[bstack11l1l1l_opy_ (u"ࠢࡃࡕࡢࡘࡊ࡙ࡔࡐࡒࡖࡣࡇ࡛ࡉࡍࡆࡢࡌࡆ࡙ࡈࡆࡆࡢࡍࡉࠨᐼ")])
            bstack1111l1ll1l_opy_ = cls.request_url(bstack11ll1l11l1_opy_)
            response = bstack1ll11l1111_opy_(bstack11l1l1l_opy_ (u"ࠨࡒࡘࡘࠬᐽ"), bstack1111l1ll1l_opy_, data, config)
            if not response.ok:
                raise Exception(bstack11l1l1l_opy_ (u"ࠤࡖࡸࡴࡶࠠࡳࡧࡴࡹࡪࡹࡴࠡࡰࡲࡸࠥࡵ࡫ࠣᐾ"))
    @classmethod
    def bstack1l1l1l11l1_opy_(cls):
        if cls.bstack111l1ll11l_opy_ is None:
            return
        cls.bstack111l1ll11l_opy_.shutdown()
    @classmethod
    def bstack1lll1llll_opy_(cls):
        if cls.on():
            print(
                bstack11l1l1l_opy_ (u"࡚ࠪ࡮ࡹࡩࡵࠢ࡫ࡸࡹࡶࡳ࠻࠱࠲ࡳࡧࡹࡥࡳࡸࡤࡦ࡮ࡲࡩࡵࡻ࠱ࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬࠰ࡦࡳࡲ࠵ࡢࡶ࡫࡯ࡨࡸ࠵ࡻࡾࠢࡷࡳࠥࡼࡩࡦࡹࠣࡦࡺ࡯࡬ࡥࠢࡵࡩࡵࡵࡲࡵ࠮ࠣ࡭ࡳࡹࡩࡨࡪࡷࡷ࠱ࠦࡡ࡯ࡦࠣࡱࡦࡴࡹࠡ࡯ࡲࡶࡪࠦࡤࡦࡤࡸ࡫࡬࡯࡮ࡨࠢ࡬ࡲ࡫ࡵࡲ࡮ࡣࡷ࡭ࡴࡴࠠࡢ࡮࡯ࠤࡦࡺࠠࡰࡰࡨࠤࡵࡲࡡࡤࡧࠤࡠࡳ࠭ᐿ").format(os.environ[bstack11l1l1l_opy_ (u"ࠦࡇ࡙࡟ࡕࡇࡖࡘࡔࡖࡓࡠࡄࡘࡍࡑࡊ࡟ࡉࡃࡖࡌࡊࡊ࡟ࡊࡆࠥᑀ")]))
    @classmethod
    def bstack1111l1lll1_opy_(cls):
        if cls.bstack111l1ll11l_opy_ is not None:
            return
        cls.bstack111l1ll11l_opy_ = bstack111l1lll1l_opy_(cls.bstack1111ll1l11_opy_)
        cls.bstack111l1ll11l_opy_.start()
    @classmethod
    def bstack1l1l1l1111_opy_(cls, bstack1l1l11lll1_opy_, bstack1111l11lll_opy_=bstack11l1l1l_opy_ (u"ࠬࡧࡰࡪ࠱ࡹ࠵࠴ࡨࡡࡵࡥ࡫ࠫᑁ")):
        if not cls.on():
            return
        bstack1llll1111l_opy_ = bstack1l1l11lll1_opy_[bstack11l1l1l_opy_ (u"࠭ࡥࡷࡧࡱࡸࡤࡺࡹࡱࡧࠪᑂ")]
        bstack1111ll111l_opy_ = {
            bstack11l1l1l_opy_ (u"ࠧࡕࡧࡶࡸࡗࡻ࡮ࡔࡶࡤࡶࡹ࡫ࡤࠨᑃ"): bstack11l1l1l_opy_ (u"ࠨࡖࡨࡷࡹࡥࡓࡵࡣࡵࡸࡤ࡛ࡰ࡭ࡱࡤࡨࠬᑄ"),
            bstack11l1l1l_opy_ (u"ࠩࡗࡩࡸࡺࡒࡶࡰࡉ࡭ࡳ࡯ࡳࡩࡧࡧࠫᑅ"): bstack11l1l1l_opy_ (u"ࠪࡘࡪࡹࡴࡠࡇࡱࡨࡤ࡛ࡰ࡭ࡱࡤࡨࠬᑆ"),
            bstack11l1l1l_opy_ (u"࡙ࠫ࡫ࡳࡵࡔࡸࡲࡘࡱࡩࡱࡲࡨࡨࠬᑇ"): bstack11l1l1l_opy_ (u"࡚ࠬࡥࡴࡶࡢࡗࡰ࡯ࡰࡱࡧࡧࡣ࡚ࡶ࡬ࡰࡣࡧࠫᑈ"),
            bstack11l1l1l_opy_ (u"࠭ࡌࡰࡩࡆࡶࡪࡧࡴࡦࡦࠪᑉ"): bstack11l1l1l_opy_ (u"ࠧࡍࡱࡪࡣ࡚ࡶ࡬ࡰࡣࡧࠫᑊ"),
            bstack11l1l1l_opy_ (u"ࠨࡊࡲࡳࡰࡘࡵ࡯ࡕࡷࡥࡷࡺࡥࡥࠩᑋ"): bstack11l1l1l_opy_ (u"ࠩࡋࡳࡴࡱ࡟ࡔࡶࡤࡶࡹࡥࡕࡱ࡮ࡲࡥࡩ࠭ᑌ"),
            bstack11l1l1l_opy_ (u"ࠪࡌࡴࡵ࡫ࡓࡷࡱࡊ࡮ࡴࡩࡴࡪࡨࡨࠬᑍ"): bstack11l1l1l_opy_ (u"ࠫࡍࡵ࡯࡬ࡡࡈࡲࡩࡥࡕࡱ࡮ࡲࡥࡩ࠭ᑎ"),
            bstack11l1l1l_opy_ (u"ࠬࡉࡂࡕࡕࡨࡷࡸ࡯࡯࡯ࡅࡵࡩࡦࡺࡥࡥࠩᑏ"): bstack11l1l1l_opy_ (u"࠭ࡃࡃࡖࡢ࡙ࡵࡲ࡯ࡢࡦࠪᑐ")
        }.get(bstack1llll1111l_opy_)
        if bstack1111l11lll_opy_ == bstack11l1l1l_opy_ (u"ࠧࡢࡲ࡬࠳ࡻ࠷࠯ࡣࡣࡷࡧ࡭࠭ᑑ"):
            cls.bstack1111l1lll1_opy_()
            cls.bstack111l1ll11l_opy_.add(bstack1l1l11lll1_opy_)
        elif bstack1111l11lll_opy_ == bstack11l1l1l_opy_ (u"ࠨࡣࡳ࡭࠴ࡼ࠱࠰ࡵࡦࡶࡪ࡫࡮ࡴࡪࡲࡸࡸ࠭ᑒ"):
            cls.bstack1111ll1l11_opy_([bstack1l1l11lll1_opy_], bstack1111l11lll_opy_)
    @classmethod
    @bstack1l11ll1ll1_opy_(class_method=True)
    def bstack1111ll1l11_opy_(cls, bstack1l1l11lll1_opy_, bstack1111l11lll_opy_=bstack11l1l1l_opy_ (u"ࠩࡤࡴ࡮࠵ࡶ࠲࠱ࡥࡥࡹࡩࡨࠨᑓ")):
        config = {
            bstack11l1l1l_opy_ (u"ࠪ࡬ࡪࡧࡤࡦࡴࡶࠫᑔ"): cls.default_headers()
        }
        response = bstack1ll11l1111_opy_(bstack11l1l1l_opy_ (u"ࠫࡕࡕࡓࡕࠩᑕ"), cls.request_url(bstack1111l11lll_opy_), bstack1l1l11lll1_opy_, config)
        bstack1l11111l1l_opy_ = response.json()
    @classmethod
    @bstack1l11ll1ll1_opy_(class_method=True)
    def bstack1l11llll1l_opy_(cls, bstack1l1l1l1l1l_opy_):
        bstack1111ll1ll1_opy_ = []
        for log in bstack1l1l1l1l1l_opy_:
            bstack1111ll1l1l_opy_ = {
                bstack11l1l1l_opy_ (u"ࠬࡱࡩ࡯ࡦࠪᑖ"): bstack11l1l1l_opy_ (u"࠭ࡔࡆࡕࡗࡣࡑࡕࡇࠨᑗ"),
                bstack11l1l1l_opy_ (u"ࠧ࡭ࡧࡹࡩࡱ࠭ᑘ"): log[bstack11l1l1l_opy_ (u"ࠨ࡮ࡨࡺࡪࡲࠧᑙ")],
                bstack11l1l1l_opy_ (u"ࠩࡷ࡭ࡲ࡫ࡳࡵࡣࡰࡴࠬᑚ"): log[bstack11l1l1l_opy_ (u"ࠪࡸ࡮ࡳࡥࡴࡶࡤࡱࡵ࠭ᑛ")],
                bstack11l1l1l_opy_ (u"ࠫ࡭ࡺࡴࡱࡡࡵࡩࡸࡶ࡯࡯ࡵࡨࠫᑜ"): {},
                bstack11l1l1l_opy_ (u"ࠬࡳࡥࡴࡵࡤ࡫ࡪ࠭ᑝ"): log[bstack11l1l1l_opy_ (u"࠭࡭ࡦࡵࡶࡥ࡬࡫ࠧᑞ")],
            }
            if bstack11l1l1l_opy_ (u"ࠧࡵࡧࡶࡸࡤࡸࡵ࡯ࡡࡸࡹ࡮ࡪࠧᑟ") in log:
                bstack1111ll1l1l_opy_[bstack11l1l1l_opy_ (u"ࠨࡶࡨࡷࡹࡥࡲࡶࡰࡢࡹࡺ࡯ࡤࠨᑠ")] = log[bstack11l1l1l_opy_ (u"ࠩࡷࡩࡸࡺ࡟ࡳࡷࡱࡣࡺࡻࡩࡥࠩᑡ")]
            elif bstack11l1l1l_opy_ (u"ࠪ࡬ࡴࡵ࡫ࡠࡴࡸࡲࡤࡻࡵࡪࡦࠪᑢ") in log:
                bstack1111ll1l1l_opy_[bstack11l1l1l_opy_ (u"ࠫ࡭ࡵ࡯࡬ࡡࡵࡹࡳࡥࡵࡶ࡫ࡧࠫᑣ")] = log[bstack11l1l1l_opy_ (u"ࠬ࡮࡯ࡰ࡭ࡢࡶࡺࡴ࡟ࡶࡷ࡬ࡨࠬᑤ")]
            bstack1111ll1ll1_opy_.append(bstack1111ll1l1l_opy_)
        cls.bstack1l1l1l1111_opy_({
            bstack11l1l1l_opy_ (u"࠭ࡥࡷࡧࡱࡸࡤࡺࡹࡱࡧࠪᑥ"): bstack11l1l1l_opy_ (u"ࠧࡍࡱࡪࡇࡷ࡫ࡡࡵࡧࡧࠫᑦ"),
            bstack11l1l1l_opy_ (u"ࠨ࡮ࡲ࡫ࡸ࠭ᑧ"): bstack1111ll1ll1_opy_
        })
    @classmethod
    @bstack1l11ll1ll1_opy_(class_method=True)
    def bstack1111l1l11l_opy_(cls, steps):
        bstack1111l1llll_opy_ = []
        for step in steps:
            bstack1111l1ll11_opy_ = {
                bstack11l1l1l_opy_ (u"ࠩ࡮࡭ࡳࡪࠧᑨ"): bstack11l1l1l_opy_ (u"ࠪࡘࡊ࡙ࡔࡠࡕࡗࡉࡕ࠭ᑩ"),
                bstack11l1l1l_opy_ (u"ࠫࡱ࡫ࡶࡦ࡮ࠪᑪ"): step[bstack11l1l1l_opy_ (u"ࠬࡲࡥࡷࡧ࡯ࠫᑫ")],
                bstack11l1l1l_opy_ (u"࠭ࡴࡪ࡯ࡨࡷࡹࡧ࡭ࡱࠩᑬ"): step[bstack11l1l1l_opy_ (u"ࠧࡵ࡫ࡰࡩࡸࡺࡡ࡮ࡲࠪᑭ")],
                bstack11l1l1l_opy_ (u"ࠨ࡯ࡨࡷࡸࡧࡧࡦࠩᑮ"): step[bstack11l1l1l_opy_ (u"ࠩࡰࡩࡸࡹࡡࡨࡧࠪᑯ")],
                bstack11l1l1l_opy_ (u"ࠪࡨࡺࡸࡡࡵ࡫ࡲࡲࠬᑰ"): step[bstack11l1l1l_opy_ (u"ࠫࡩࡻࡲࡢࡶ࡬ࡳࡳ࠭ᑱ")]
            }
            if bstack11l1l1l_opy_ (u"ࠬࡺࡥࡴࡶࡢࡶࡺࡴ࡟ࡶࡷ࡬ࡨࠬᑲ") in step:
                bstack1111l1ll11_opy_[bstack11l1l1l_opy_ (u"࠭ࡴࡦࡵࡷࡣࡷࡻ࡮ࡠࡷࡸ࡭ࡩ࠭ᑳ")] = step[bstack11l1l1l_opy_ (u"ࠧࡵࡧࡶࡸࡤࡸࡵ࡯ࡡࡸࡹ࡮ࡪࠧᑴ")]
            elif bstack11l1l1l_opy_ (u"ࠨࡪࡲࡳࡰࡥࡲࡶࡰࡢࡹࡺ࡯ࡤࠨᑵ") in step:
                bstack1111l1ll11_opy_[bstack11l1l1l_opy_ (u"ࠩ࡫ࡳࡴࡱ࡟ࡳࡷࡱࡣࡺࡻࡩࡥࠩᑶ")] = step[bstack11l1l1l_opy_ (u"ࠪ࡬ࡴࡵ࡫ࡠࡴࡸࡲࡤࡻࡵࡪࡦࠪᑷ")]
            bstack1111l1llll_opy_.append(bstack1111l1ll11_opy_)
        cls.bstack1l1l1l1111_opy_({
            bstack11l1l1l_opy_ (u"ࠫࡪࡼࡥ࡯ࡶࡢࡸࡾࡶࡥࠨᑸ"): bstack11l1l1l_opy_ (u"ࠬࡒ࡯ࡨࡅࡵࡩࡦࡺࡥࡥࠩᑹ"),
            bstack11l1l1l_opy_ (u"࠭࡬ࡰࡩࡶࠫᑺ"): bstack1111l1llll_opy_
        })
    @classmethod
    @bstack1l11ll1ll1_opy_(class_method=True)
    def bstack111l1ll1l_opy_(cls, screenshot):
        cls.bstack1l1l1l1111_opy_({
            bstack11l1l1l_opy_ (u"ࠧࡦࡸࡨࡲࡹࡥࡴࡺࡲࡨࠫᑻ"): bstack11l1l1l_opy_ (u"ࠨࡎࡲ࡫ࡈࡸࡥࡢࡶࡨࡨࠬᑼ"),
            bstack11l1l1l_opy_ (u"ࠩ࡯ࡳ࡬ࡹࠧᑽ"): [{
                bstack11l1l1l_opy_ (u"ࠪ࡯࡮ࡴࡤࠨᑾ"): bstack11l1l1l_opy_ (u"࡙ࠫࡋࡓࡕࡡࡖࡇࡗࡋࡅࡏࡕࡋࡓ࡙࠭ᑿ"),
                bstack11l1l1l_opy_ (u"ࠬࡺࡩ࡮ࡧࡶࡸࡦࡳࡰࠨᒀ"): datetime.datetime.utcnow().isoformat() + bstack11l1l1l_opy_ (u"࡚࠭ࠨᒁ"),
                bstack11l1l1l_opy_ (u"ࠧ࡮ࡧࡶࡷࡦ࡭ࡥࠨᒂ"): screenshot[bstack11l1l1l_opy_ (u"ࠨ࡫ࡰࡥ࡬࡫ࠧᒃ")],
                bstack11l1l1l_opy_ (u"ࠩࡷࡩࡸࡺ࡟ࡳࡷࡱࡣࡺࡻࡩࡥࠩᒄ"): screenshot[bstack11l1l1l_opy_ (u"ࠪࡸࡪࡹࡴࡠࡴࡸࡲࡤࡻࡵࡪࡦࠪᒅ")]
            }]
        }, bstack1111l11lll_opy_=bstack11l1l1l_opy_ (u"ࠫࡦࡶࡩ࠰ࡸ࠴࠳ࡸࡩࡲࡦࡧࡱࡷ࡭ࡵࡴࡴࠩᒆ"))
    @classmethod
    @bstack1l11ll1ll1_opy_(class_method=True)
    def bstack1ll11llll1_opy_(cls, driver):
        current_test_uuid = cls.current_test_uuid()
        if not current_test_uuid:
            return
        cls.bstack1l1l1l1111_opy_({
            bstack11l1l1l_opy_ (u"ࠬ࡫ࡶࡦࡰࡷࡣࡹࡿࡰࡦࠩᒇ"): bstack11l1l1l_opy_ (u"࠭ࡃࡃࡖࡖࡩࡸࡹࡩࡰࡰࡆࡶࡪࡧࡴࡦࡦࠪᒈ"),
            bstack11l1l1l_opy_ (u"ࠧࡵࡧࡶࡸࡤࡸࡵ࡯ࠩᒉ"): {
                bstack11l1l1l_opy_ (u"ࠣࡷࡸ࡭ࡩࠨᒊ"): cls.current_test_uuid(),
                bstack11l1l1l_opy_ (u"ࠤ࡬ࡲࡹ࡫ࡧࡳࡣࡷ࡭ࡴࡴࡳࠣᒋ"): cls.bstack1l1l1ll1l1_opy_(driver)
            }
        })
    @classmethod
    def on(cls):
        if os.environ.get(bstack11l1l1l_opy_ (u"ࠪࡆࡘࡥࡔࡆࡕࡗࡓࡕ࡙࡟ࡋ࡙ࡗࠫᒌ"), None) is None or os.environ[bstack11l1l1l_opy_ (u"ࠫࡇ࡙࡟ࡕࡇࡖࡘࡔࡖࡓࡠࡌ࡚ࡘࠬᒍ")] == bstack11l1l1l_opy_ (u"ࠧࡴࡵ࡭࡮ࠥᒎ"):
            return False
        return True
    @classmethod
    def bstack1111l1l111_opy_(cls):
        return bstack1111llll_opy_(cls.bs_config.get(bstack11l1l1l_opy_ (u"࠭ࡴࡦࡵࡷࡓࡧࡹࡥࡳࡸࡤࡦ࡮ࡲࡩࡵࡻࠪᒏ"), False))
    @staticmethod
    def request_url(url):
        return bstack11l1l1l_opy_ (u"ࠧࡼࡿ࠲ࡿࢂ࠭ᒐ").format(bstack1111ll11l1_opy_, url)
    @staticmethod
    def default_headers():
        headers = {
            bstack11l1l1l_opy_ (u"ࠨࡅࡲࡲࡹ࡫࡮ࡵ࠯ࡗࡽࡵ࡫ࠧᒑ"): bstack11l1l1l_opy_ (u"ࠩࡤࡴࡵࡲࡩࡤࡣࡷ࡭ࡴࡴ࠯࡫ࡵࡲࡲࠬᒒ"),
            bstack11l1l1l_opy_ (u"ࠪ࡜࠲ࡈࡓࡕࡃࡆࡏ࠲࡚ࡅࡔࡖࡒࡔࡘ࠭ᒓ"): bstack11l1l1l_opy_ (u"ࠫࡹࡸࡵࡦࠩᒔ")
        }
        if os.environ.get(bstack11l1l1l_opy_ (u"ࠬࡈࡓࡠࡖࡈࡗ࡙ࡕࡐࡔࡡࡍ࡛࡙࠭ᒕ"), None):
            headers[bstack11l1l1l_opy_ (u"࠭ࡁࡶࡶ࡫ࡳࡷ࡯ࡺࡢࡶ࡬ࡳࡳ࠭ᒖ")] = bstack11l1l1l_opy_ (u"ࠧࡃࡧࡤࡶࡪࡸࠠࡼࡿࠪᒗ").format(os.environ[bstack11l1l1l_opy_ (u"ࠣࡄࡖࡣ࡙ࡋࡓࡕࡑࡓࡗࡤࡐࡗࡕࠤᒘ")])
        return headers
    @staticmethod
    def current_test_uuid():
        return getattr(threading.current_thread(), bstack11l1l1l_opy_ (u"ࠩࡦࡹࡷࡸࡥ࡯ࡶࡢࡸࡪࡹࡴࡠࡷࡸ࡭ࡩ࠭ᒙ"), None)
    @staticmethod
    def current_hook_uuid():
        return getattr(threading.current_thread(), bstack11l1l1l_opy_ (u"ࠪࡧࡺࡸࡲࡦࡰࡷࡣ࡭ࡵ࡯࡬ࡡࡸࡹ࡮ࡪࠧᒚ"), None)
    @staticmethod
    def bstack1l1l11l1l1_opy_():
        if getattr(threading.current_thread(), bstack11l1l1l_opy_ (u"ࠫࡨࡻࡲࡳࡧࡱࡸࡤࡺࡥࡴࡶࡢࡹࡺ࡯ࡤࠨᒛ"), None):
            return {
                bstack11l1l1l_opy_ (u"ࠬࡺࡹࡱࡧࠪᒜ"): bstack11l1l1l_opy_ (u"࠭ࡴࡦࡵࡷࠫᒝ"),
                bstack11l1l1l_opy_ (u"ࠧࡵࡧࡶࡸࡤࡸࡵ࡯ࡡࡸࡹ࡮ࡪࠧᒞ"): getattr(threading.current_thread(), bstack11l1l1l_opy_ (u"ࠨࡥࡸࡶࡷ࡫࡮ࡵࡡࡷࡩࡸࡺ࡟ࡶࡷ࡬ࡨࠬᒟ"), None)
            }
        if getattr(threading.current_thread(), bstack11l1l1l_opy_ (u"ࠩࡦࡹࡷࡸࡥ࡯ࡶࡢ࡬ࡴࡵ࡫ࡠࡷࡸ࡭ࡩ࠭ᒠ"), None):
            return {
                bstack11l1l1l_opy_ (u"ࠪࡸࡾࡶࡥࠨᒡ"): bstack11l1l1l_opy_ (u"ࠫ࡭ࡵ࡯࡬ࠩᒢ"),
                bstack11l1l1l_opy_ (u"ࠬ࡮࡯ࡰ࡭ࡢࡶࡺࡴ࡟ࡶࡷ࡬ࡨࠬᒣ"): getattr(threading.current_thread(), bstack11l1l1l_opy_ (u"࠭ࡣࡶࡴࡵࡩࡳࡺ࡟ࡩࡱࡲ࡯ࡤࡻࡵࡪࡦࠪᒤ"), None)
            }
        return None
    @staticmethod
    def bstack1l1l1ll1l1_opy_(driver):
        return {
            bstack11ll1ll11l_opy_(): bstack11ll1l11ll_opy_(driver)
        }
    @staticmethod
    def bstack1111ll11ll_opy_(exception_info, report):
        return [{bstack11l1l1l_opy_ (u"ࠧࡣࡣࡦ࡯ࡹࡸࡡࡤࡧࠪᒥ"): [exception_info.exconly(), report.longreprtext]}]
    @staticmethod
    def bstack1l111ll11l_opy_(typename):
        if bstack11l1l1l_opy_ (u"ࠣࡃࡶࡷࡪࡸࡴࡪࡱࡱࠦᒦ") in typename:
            return bstack11l1l1l_opy_ (u"ࠤࡄࡷࡸ࡫ࡲࡵ࡫ࡲࡲࡊࡸࡲࡰࡴࠥᒧ")
        return bstack11l1l1l_opy_ (u"࡙ࠥࡳ࡮ࡡ࡯ࡦ࡯ࡩࡩࡋࡲࡳࡱࡵࠦᒨ")
    @staticmethod
    def bstack1111l11ll1_opy_(func):
        def wrap(*args, **kwargs):
            if bstack1l11l11l_opy_.on():
                return func(*args, **kwargs)
            return
        return wrap
    @staticmethod
    def bstack1l1l1l1lll_opy_(test, hook_name=None):
        bstack1111ll1lll_opy_ = test.parent
        if hook_name in [bstack11l1l1l_opy_ (u"ࠫࡸ࡫ࡴࡶࡲࡢࡧࡱࡧࡳࡴࠩᒩ"), bstack11l1l1l_opy_ (u"ࠬࡺࡥࡢࡴࡧࡳࡼࡴ࡟ࡤ࡮ࡤࡷࡸ࠭ᒪ"), bstack11l1l1l_opy_ (u"࠭ࡳࡦࡶࡸࡴࡤࡳ࡯ࡥࡷ࡯ࡩࠬᒫ"), bstack11l1l1l_opy_ (u"ࠧࡵࡧࡤࡶࡩࡵࡷ࡯ࡡࡰࡳࡩࡻ࡬ࡦࠩᒬ")]:
            bstack1111ll1lll_opy_ = test
        scope = []
        while bstack1111ll1lll_opy_ is not None:
            scope.append(bstack1111ll1lll_opy_.name)
            bstack1111ll1lll_opy_ = bstack1111ll1lll_opy_.parent
        scope.reverse()
        return scope[2:]
    @staticmethod
    def bstack1111l1l1l1_opy_(hook_type):
        if hook_type == bstack11l1l1l_opy_ (u"ࠣࡄࡈࡊࡔࡘࡅࡠࡇࡄࡇࡍࠨᒭ"):
            return bstack11l1l1l_opy_ (u"ࠤࡖࡩࡹࡻࡰࠡࡪࡲࡳࡰࠨᒮ")
        elif hook_type == bstack11l1l1l_opy_ (u"ࠥࡅࡋ࡚ࡅࡓࡡࡈࡅࡈࡎࠢᒯ"):
            return bstack11l1l1l_opy_ (u"࡙ࠦ࡫ࡡࡳࡦࡲࡻࡳࠦࡨࡰࡱ࡮ࠦᒰ")
    @staticmethod
    def bstack1111lll111_opy_(bstack1ll1111l1_opy_):
        try:
            if not bstack1l11l11l_opy_.on():
                return bstack1ll1111l1_opy_
            if os.environ.get(bstack11l1l1l_opy_ (u"ࠧࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣࡗࡋࡒࡖࡐࠥᒱ"), None) == bstack11l1l1l_opy_ (u"ࠨࡴࡳࡷࡨࠦᒲ"):
                tests = os.environ.get(bstack11l1l1l_opy_ (u"ࠢࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡒࡆࡔࡘࡒࡤ࡚ࡅࡔࡖࡖࠦᒳ"), None)
                if tests is None or tests == bstack11l1l1l_opy_ (u"ࠣࡰࡸࡰࡱࠨᒴ"):
                    return bstack1ll1111l1_opy_
                bstack1ll1111l1_opy_ = tests.split(bstack11l1l1l_opy_ (u"ࠩ࠯ࠫᒵ"))
                return bstack1ll1111l1_opy_
        except Exception as exc:
            print(bstack11l1l1l_opy_ (u"ࠥࡉࡽࡩࡥࡱࡶ࡬ࡳࡳࠦࡩ࡯ࠢࡵࡩࡷࡻ࡮ࠡࡪࡤࡲࡩࡲࡥࡳ࠼ࠣࠦᒶ"), str(exc))
        return bstack1ll1111l1_opy_
    @classmethod
    def bstack1l11l1ll1l_opy_(cls, event: str, bstack1l1l11lll1_opy_: bstack1l1l111111_opy_):
        bstack1l1l1ll111_opy_ = {
            bstack11l1l1l_opy_ (u"ࠫࡪࡼࡥ࡯ࡶࡢࡸࡾࡶࡥࠨᒷ"): event,
            bstack1l1l11lll1_opy_.bstack1l11l1l11l_opy_(): bstack1l1l11lll1_opy_.bstack1l1l11llll_opy_(event)
        }
        bstack1l11l11l_opy_.bstack1l1l1l1111_opy_(bstack1l1l1ll111_opy_)