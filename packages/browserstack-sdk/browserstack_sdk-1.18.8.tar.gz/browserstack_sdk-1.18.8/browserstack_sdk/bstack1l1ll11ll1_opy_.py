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
import json
import logging
logger = logging.getLogger(__name__)
class bstack1l1ll111l1_opy_:
    def bstack1l1ll11l11_opy_():
        bstack1l1ll111ll_opy_ = {}
        try:
            bstack1l1ll11l1l_opy_ = json.loads(os.environ[bstack11l1l1l_opy_ (u"ࠧࡄࡗࡕࡖࡊࡔࡔࡠࡒࡏࡅ࡙ࡌࡏࡓࡏࡢࡈࡆ࡚ࡁࠨ೯")])
            bstack1ll111lll1_opy_ = os.environ.get(bstack11l1l1l_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡊࡕࡢࡅࡕࡖ࡟ࡂࡗࡗࡓࡒࡇࡔࡆࠩ೰"))
            if bstack1ll111lll1_opy_ is not None and eval(bstack1ll111lll1_opy_):
                bstack1l1ll111ll_opy_[bstack11l1l1l_opy_ (u"ࠤࡳࡰࡦࡺࡦࡰࡴࡰࡒࡦࡳࡥࠣೱ")] = bstack1l1ll11l1l_opy_[bstack11l1l1l_opy_ (u"ࠥࡴࡱࡧࡴࡧࡱࡵࡱࡓࡧ࡭ࡦࠤೲ")]
                bstack1l1ll111ll_opy_[bstack11l1l1l_opy_ (u"ࠦࡩ࡫ࡶࡪࡥࡨࡒࡦࡳࡥࠣೳ")] = bstack1l1ll11l1l_opy_[bstack11l1l1l_opy_ (u"ࠧࡪࡥࡷ࡫ࡦࡩࡓࡧ࡭ࡦࠤ೴")]
                bstack1l1ll111ll_opy_[bstack11l1l1l_opy_ (u"ࠨࡰ࡭ࡣࡷࡪࡴࡸ࡭ࡗࡧࡵࡷ࡮ࡵ࡮ࠣ೵")] = bstack1l1ll11l1l_opy_[bstack11l1l1l_opy_ (u"ࠢࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࡘࡨࡶࡸ࡯࡯࡯ࠤ೶")]
            else:
                bstack1l1ll111ll_opy_[bstack11l1l1l_opy_ (u"ࠣࡱࡶࠦ೷")] = bstack1l1ll11l1l_opy_[bstack11l1l1l_opy_ (u"ࠤࡲࡷࠧ೸")]
                bstack1l1ll111ll_opy_[bstack11l1l1l_opy_ (u"ࠥࡳࡸ࡜ࡥࡳࡵ࡬ࡳࡳࠨ೹")] = bstack1l1ll11l1l_opy_[bstack11l1l1l_opy_ (u"ࠦࡴࡹࡖࡦࡴࡶ࡭ࡴࡴࠢ೺")]
                bstack1l1ll111ll_opy_[bstack11l1l1l_opy_ (u"ࠧࡨࡲࡰࡹࡶࡩࡷࡔࡡ࡮ࡧࠥ೻")] = bstack1l1ll11l1l_opy_[bstack11l1l1l_opy_ (u"ࠨࡢࡳࡱࡺࡷࡪࡸࡎࡢ࡯ࡨࠦ೼")]
                bstack1l1ll111ll_opy_[bstack11l1l1l_opy_ (u"ࠢࡣࡴࡲࡻࡸ࡫ࡲࡗࡧࡵࡷ࡮ࡵ࡮ࠣ೽")] = bstack1l1ll11l1l_opy_[bstack11l1l1l_opy_ (u"ࠣࡤࡵࡳࡼࡹࡥࡳࡘࡨࡶࡸ࡯࡯࡯ࠤ೾")]
            bstack1l1ll111ll_opy_[bstack11l1l1l_opy_ (u"ࠤࡦࡹࡸࡺ࡯࡮ࡘࡤࡶ࡮ࡧࡢ࡭ࡧࡶࠦ೿")] = bstack1l1ll11l1l_opy_.get(bstack11l1l1l_opy_ (u"ࠥࡧࡺࡹࡴࡰ࡯࡙ࡥࡷ࡯ࡡࡣ࡮ࡨࡷࠧഀ"), None)
        except Exception as error:
            logger.error(bstack11l1l1l_opy_ (u"ࠦࡊࡾࡣࡦࡲࡷ࡭ࡴࡴࠠࡸࡪ࡬ࡰࡪࠦࡧࡦࡶࡷ࡭ࡳ࡭ࠠࡤࡷࡵࡶࡪࡴࡴࠡࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࠣࡨࡦࡺࡡ࠻ࠢࠥഁ") +  str(error))
        return bstack1l1ll111ll_opy_