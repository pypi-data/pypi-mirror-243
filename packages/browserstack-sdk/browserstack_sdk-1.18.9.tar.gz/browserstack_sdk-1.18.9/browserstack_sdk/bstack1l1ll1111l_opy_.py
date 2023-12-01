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
import json
import logging
logger = logging.getLogger(__name__)
class bstack1l1ll111l1_opy_:
    def bstack1l1ll111ll_opy_():
        bstack1l1ll11111_opy_ = {}
        try:
            bstack1l1l1lllll_opy_ = json.loads(os.environ[bstack11l1ll_opy_ (u"ࠬࡉࡕࡓࡔࡈࡒ࡙ࡥࡐࡍࡃࡗࡊࡔࡘࡍࡠࡆࡄࡘࡆ࠭೘")])
            bstack1ll1l11l1l_opy_ = os.environ.get(bstack11l1ll_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤࡏࡓࡠࡃࡓࡔࡤࡇࡕࡕࡑࡐࡅ࡙ࡋࠧ೙"))
            if bstack1ll1l11l1l_opy_ is not None and eval(bstack1ll1l11l1l_opy_):
                bstack1l1ll11111_opy_[bstack11l1ll_opy_ (u"ࠢࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࡐࡤࡱࡪࠨ೚")] = bstack1l1l1lllll_opy_[bstack11l1ll_opy_ (u"ࠣࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࡑࡥࡲ࡫ࠢ೛")]
                bstack1l1ll11111_opy_[bstack11l1ll_opy_ (u"ࠤࡧࡩࡻ࡯ࡣࡦࡐࡤࡱࡪࠨ೜")] = bstack1l1l1lllll_opy_[bstack11l1ll_opy_ (u"ࠥࡨࡪࡼࡩࡤࡧࡑࡥࡲ࡫ࠢೝ")]
                bstack1l1ll11111_opy_[bstack11l1ll_opy_ (u"ࠦࡵࡲࡡࡵࡨࡲࡶࡲ࡜ࡥࡳࡵ࡬ࡳࡳࠨೞ")] = bstack1l1l1lllll_opy_[bstack11l1ll_opy_ (u"ࠧࡶ࡬ࡢࡶࡩࡳࡷࡳࡖࡦࡴࡶ࡭ࡴࡴࠢ೟")]
            else:
                bstack1l1ll11111_opy_[bstack11l1ll_opy_ (u"ࠨ࡯ࡴࠤೠ")] = bstack1l1l1lllll_opy_[bstack11l1ll_opy_ (u"ࠢࡰࡵࠥೡ")]
                bstack1l1ll11111_opy_[bstack11l1ll_opy_ (u"ࠣࡱࡶ࡚ࡪࡸࡳࡪࡱࡱࠦೢ")] = bstack1l1l1lllll_opy_[bstack11l1ll_opy_ (u"ࠤࡲࡷ࡛࡫ࡲࡴ࡫ࡲࡲࠧೣ")]
                bstack1l1ll11111_opy_[bstack11l1ll_opy_ (u"ࠥࡦࡷࡵࡷࡴࡧࡵࡒࡦࡳࡥࠣ೤")] = bstack1l1l1lllll_opy_[bstack11l1ll_opy_ (u"ࠦࡧࡸ࡯ࡸࡵࡨࡶࡓࡧ࡭ࡦࠤ೥")]
                bstack1l1ll11111_opy_[bstack11l1ll_opy_ (u"ࠧࡨࡲࡰࡹࡶࡩࡷ࡜ࡥࡳࡵ࡬ࡳࡳࠨ೦")] = bstack1l1l1lllll_opy_[bstack11l1ll_opy_ (u"ࠨࡢࡳࡱࡺࡷࡪࡸࡖࡦࡴࡶ࡭ࡴࡴࠢ೧")]
            bstack1l1ll11111_opy_[bstack11l1ll_opy_ (u"ࠢࡤࡷࡶࡸࡴࡳࡖࡢࡴ࡬ࡥࡧࡲࡥࡴࠤ೨")] = bstack1l1l1lllll_opy_.get(bstack11l1ll_opy_ (u"ࠣࡥࡸࡷࡹࡵ࡭ࡗࡣࡵ࡭ࡦࡨ࡬ࡦࡵࠥ೩"), None)
        except Exception as error:
            logger.error(bstack11l1ll_opy_ (u"ࠤࡈࡼࡨ࡫ࡰࡵ࡫ࡲࡲࠥࡽࡨࡪ࡮ࡨࠤ࡬࡫ࡴࡵ࡫ࡱ࡫ࠥࡩࡵࡳࡴࡨࡲࡹࠦࡰ࡭ࡣࡷࡪࡴࡸ࡭ࠡࡦࡤࡸࡦࡀࠠࠣ೪") +  str(error))
        return bstack1l1ll11111_opy_