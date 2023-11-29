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
import requests
import logging
from urllib.parse import urlparse
from datetime import datetime
from bstack_utils.constants import bstack1l111l1ll1_opy_ as bstack1l111111l1_opy_
from bstack_utils.helper import bstack1llllll11l_opy_, bstack1ll11ll11_opy_, bstack1l1111llll_opy_, bstack1l111111ll_opy_, bstack1lll1l1ll_opy_, get_host_info, bstack1l11111l11_opy_, bstack1ll11l1111_opy_, bstack1l11ll1ll1_opy_
from browserstack_sdk._version import __version__
logger = logging.getLogger(__name__)
@bstack1l11ll1ll1_opy_(class_method=False)
def _1l111l111l_opy_(driver, bstack1l1lll1111_opy_):
  response = {}
  try:
    caps = driver.capabilities
    response = {
        bstack11l1l1l_opy_ (u"ࠧࡰࡵࡢࡲࡦࡳࡥࠨූ"): caps.get(bstack11l1l1l_opy_ (u"ࠨࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࡑࡥࡲ࡫ࠧ෗"), None),
        bstack11l1l1l_opy_ (u"ࠩࡲࡷࡤࡼࡥࡳࡵ࡬ࡳࡳ࠭ෘ"): bstack1l1lll1111_opy_.get(bstack11l1l1l_opy_ (u"ࠪࡳࡸ࡜ࡥࡳࡵ࡬ࡳࡳ࠭ෙ"), None),
        bstack11l1l1l_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡤࡴࡡ࡮ࡧࠪේ"): caps.get(bstack11l1l1l_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡔࡡ࡮ࡧࠪෛ"), None),
        bstack11l1l1l_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸ࡟ࡷࡧࡵࡷ࡮ࡵ࡮ࠨො"): caps.get(bstack11l1l1l_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡗࡧࡵࡷ࡮ࡵ࡮ࠨෝ"), None)
    }
  except Exception as error:
    logger.debug(bstack11l1l1l_opy_ (u"ࠨࡇࡻࡧࡪࡶࡴࡪࡱࡱࠤ࡮ࡴࠠࡧࡧࡷࡧ࡭࡯࡮ࡨࠢࡳࡰࡦࡺࡦࡰࡴࡰࠤࡩ࡫ࡴࡢ࡫࡯ࡷࠥࡽࡩࡵࡪࠣࡩࡷࡸ࡯ࡳࠢ࠽ࠤࠬෞ") + str(error))
  return response
def bstack1ll1ll11_opy_(config):
  return config.get(bstack11l1l1l_opy_ (u"ࠩࡤࡧࡨ࡫ࡳࡴ࡫ࡥ࡭ࡱ࡯ࡴࡺࠩෟ"), False) or any([p.get(bstack11l1l1l_opy_ (u"ࠪࡥࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࠪ෠"), False) == True for p in config[bstack11l1l1l_opy_ (u"ࠫࡵࡲࡡࡵࡨࡲࡶࡲࡹࠧ෡")]])
def bstack1lll11l11_opy_(config, bstack1111l11l1_opy_):
  try:
    if not bstack1ll11ll11_opy_(config):
      return False
    bstack1l1111l1ll_opy_ = config.get(bstack11l1l1l_opy_ (u"ࠬࡧࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽࠬ෢"), False)
    bstack1l111l11ll_opy_ = config[bstack11l1l1l_opy_ (u"࠭ࡰ࡭ࡣࡷࡪࡴࡸ࡭ࡴࠩ෣")][bstack1111l11l1_opy_].get(bstack11l1l1l_opy_ (u"ࠧࡢࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿࠧ෤"), None)
    if bstack1l111l11ll_opy_ != None:
      bstack1l1111l1ll_opy_ = bstack1l111l11ll_opy_
    bstack1l1111lll1_opy_ = os.getenv(bstack11l1l1l_opy_ (u"ࠨࡄࡖࡣࡆ࠷࠱࡚ࡡࡍ࡛࡙࠭෥")) is not None and len(os.getenv(bstack11l1l1l_opy_ (u"ࠩࡅࡗࡤࡇ࠱࠲࡛ࡢࡎ࡜࡚ࠧ෦"))) > 0 and os.getenv(bstack11l1l1l_opy_ (u"ࠪࡆࡘࡥࡁ࠲࠳࡜ࡣࡏ࡝ࡔࠨ෧")) != bstack11l1l1l_opy_ (u"ࠫࡳࡻ࡬࡭ࠩ෨")
    return bstack1l1111l1ll_opy_ and bstack1l1111lll1_opy_
  except Exception as error:
    logger.debug(bstack11l1l1l_opy_ (u"ࠬࡋࡸࡤࡧࡳࡸ࡮ࡵ࡮ࠡ࡫ࡱࠤࡻ࡫ࡲࡪࡨࡼ࡭ࡳ࡭ࠠࡵࡪࡨࠤࡆࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࠤࡸ࡫ࡳࡴ࡫ࡲࡲࠥࡽࡩࡵࡪࠣࡩࡷࡸ࡯ࡳࠢ࠽ࠤࠬ෩") + str(error))
  return False
def bstack1l1lllll_opy_(bstack1l1111l111_opy_, test_tags):
  bstack1l1111l111_opy_ = os.getenv(bstack11l1l1l_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤ࡚ࡅࡔࡖࡢࡅࡈࡉࡅࡔࡕࡌࡆࡎࡒࡉࡕ࡛ࡢࡇࡔࡔࡆࡊࡉࡘࡖࡆ࡚ࡉࡐࡐࡢ࡝ࡒࡒࠧ෪"))
  if bstack1l1111l111_opy_ is None:
    return True
  bstack1l1111l111_opy_ = json.loads(bstack1l1111l111_opy_)
  try:
    include_tags = bstack1l1111l111_opy_[bstack11l1l1l_opy_ (u"ࠧࡪࡰࡦࡰࡺࡪࡥࡕࡣࡪࡷࡎࡴࡔࡦࡵࡷ࡭ࡳ࡭ࡓࡤࡱࡳࡩࠬ෫")] if bstack11l1l1l_opy_ (u"ࠨ࡫ࡱࡧࡱࡻࡤࡦࡖࡤ࡫ࡸࡏ࡮ࡕࡧࡶࡸ࡮ࡴࡧࡔࡥࡲࡴࡪ࠭෬") in bstack1l1111l111_opy_ and isinstance(bstack1l1111l111_opy_[bstack11l1l1l_opy_ (u"ࠩ࡬ࡲࡨࡲࡵࡥࡧࡗࡥ࡬ࡹࡉ࡯ࡖࡨࡷࡹ࡯࡮ࡨࡕࡦࡳࡵ࡫ࠧ෭")], list) else []
    exclude_tags = bstack1l1111l111_opy_[bstack11l1l1l_opy_ (u"ࠪࡩࡽࡩ࡬ࡶࡦࡨࡘࡦ࡭ࡳࡊࡰࡗࡩࡸࡺࡩ࡯ࡩࡖࡧࡴࡶࡥࠨ෮")] if bstack11l1l1l_opy_ (u"ࠫࡪࡾࡣ࡭ࡷࡧࡩ࡙ࡧࡧࡴࡋࡱࡘࡪࡹࡴࡪࡰࡪࡗࡨࡵࡰࡦࠩ෯") in bstack1l1111l111_opy_ and isinstance(bstack1l1111l111_opy_[bstack11l1l1l_opy_ (u"ࠬ࡫ࡸࡤ࡮ࡸࡨࡪ࡚ࡡࡨࡵࡌࡲ࡙࡫ࡳࡵ࡫ࡱ࡫ࡘࡩ࡯ࡱࡧࠪ෰")], list) else []
    excluded = any(tag in exclude_tags for tag in test_tags)
    included = len(include_tags) == 0 or any(tag in include_tags for tag in test_tags)
    return not excluded and included
  except Exception as error:
    logger.debug(bstack11l1l1l_opy_ (u"ࠨࡅࡳࡴࡲࡶࠥࡽࡨࡪ࡮ࡨࠤࡻࡧ࡬ࡪࡦࡤࡸ࡮ࡴࡧࠡࡶࡨࡷࡹࠦࡣࡢࡵࡨࠤ࡫ࡵࡲࠡࡣࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࠡࡤࡨࡪࡴࡸࡥࠡࡵࡦࡥࡳࡴࡩ࡯ࡩ࠱ࠤࡊࡸࡲࡰࡴࠣ࠾ࠥࠨ෱") + str(error))
  return False
def bstack1l1l11ll1_opy_(config, bstack1l11111lll_opy_, bstack1l1111ll11_opy_):
  bstack1l111l1l1l_opy_ = bstack1l1111llll_opy_(config)
  bstack1l1111l11l_opy_ = bstack1l111111ll_opy_(config)
  if bstack1l111l1l1l_opy_ is None or bstack1l1111l11l_opy_ is None:
    logger.error(bstack11l1l1l_opy_ (u"ࠧࡆࡺࡦࡩࡵࡺࡩࡰࡰࠣࡻ࡭࡯࡬ࡦࠢࡦࡶࡪࡧࡴࡪࡰࡪࠤࡹ࡫ࡳࡵࠢࡵࡹࡳࠦࡦࡰࡴࠣࡆࡷࡵࡷࡴࡧࡵࡗࡹࡧࡣ࡬ࠢࡄࡧࡨ࡫ࡳࡴ࡫ࡥ࡭ࡱ࡯ࡴࡺࠢࡄࡹࡹࡵ࡭ࡢࡶ࡬ࡳࡳࡀࠠࡎ࡫ࡶࡷ࡮ࡴࡧࠡࡣࡸࡸ࡭࡫࡮ࡵ࡫ࡦࡥࡹ࡯࡯࡯ࠢࡷࡳࡰ࡫࡮ࠨෲ"))
    return [None, None]
  try:
    settings = json.loads(os.getenv(bstack11l1l1l_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡕࡇࡖࡘࡤࡇࡃࡄࡇࡖࡗࡎࡈࡉࡍࡋࡗ࡝ࡤࡉࡏࡏࡈࡌࡋ࡚ࡘࡁࡕࡋࡒࡒࡤ࡟ࡍࡍࠩෳ"), bstack11l1l1l_opy_ (u"ࠩࡾࢁࠬ෴")))
    data = {
        bstack11l1l1l_opy_ (u"ࠪࡴࡷࡵࡪࡦࡥࡷࡒࡦࡳࡥࠨ෵"): config[bstack11l1l1l_opy_ (u"ࠫࡵࡸ࡯࡫ࡧࡦࡸࡓࡧ࡭ࡦࠩ෶")],
        bstack11l1l1l_opy_ (u"ࠬࡨࡵࡪ࡮ࡧࡒࡦࡳࡥࠨ෷"): config.get(bstack11l1l1l_opy_ (u"࠭ࡢࡶ࡫࡯ࡨࡓࡧ࡭ࡦࠩ෸"), os.path.basename(os.getcwd())),
        bstack11l1l1l_opy_ (u"ࠧࡴࡶࡤࡶࡹ࡚ࡩ࡮ࡧࠪ෹"): bstack1llllll11l_opy_(),
        bstack11l1l1l_opy_ (u"ࠨࡦࡨࡷࡨࡸࡩࡱࡶ࡬ࡳࡳ࠭෺"): config.get(bstack11l1l1l_opy_ (u"ࠩࡥࡹ࡮ࡲࡤࡅࡧࡶࡧࡷ࡯ࡰࡵ࡫ࡲࡲࠬ෻"), bstack11l1l1l_opy_ (u"ࠪࠫ෼")),
        bstack11l1l1l_opy_ (u"ࠫࡸࡵࡵࡳࡥࡨࠫ෽"): {
            bstack11l1l1l_opy_ (u"ࠬ࡬ࡲࡢ࡯ࡨࡻࡴࡸ࡫ࡏࡣࡰࡩࠬ෾"): bstack1l11111lll_opy_,
            bstack11l1l1l_opy_ (u"࠭ࡦࡳࡣࡰࡩࡼࡵࡲ࡬ࡘࡨࡶࡸ࡯࡯࡯ࠩ෿"): bstack1l1111ll11_opy_,
            bstack11l1l1l_opy_ (u"ࠧࡴࡦ࡮࡚ࡪࡸࡳࡪࡱࡱࠫ฀"): __version__
        },
        bstack11l1l1l_opy_ (u"ࠨࡵࡨࡸࡹ࡯࡮ࡨࡵࠪก"): settings,
        bstack11l1l1l_opy_ (u"ࠩࡹࡩࡷࡹࡩࡰࡰࡆࡳࡳࡺࡲࡰ࡮ࠪข"): bstack1l11111l11_opy_(),
        bstack11l1l1l_opy_ (u"ࠪࡧ࡮ࡏ࡮ࡧࡱࠪฃ"): bstack1lll1l1ll_opy_(),
        bstack11l1l1l_opy_ (u"ࠫ࡭ࡵࡳࡵࡋࡱࡪࡴ࠭ค"): get_host_info(),
        bstack11l1l1l_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࡅࡺࡺ࡯࡮ࡣࡷ࡭ࡴࡴࠧฅ"): bstack1ll11ll11_opy_(config)
    }
    headers = {
        bstack11l1l1l_opy_ (u"࠭ࡃࡰࡰࡷࡩࡳࡺ࠭ࡕࡻࡳࡩࠬฆ"): bstack11l1l1l_opy_ (u"ࠧࡢࡲࡳࡰ࡮ࡩࡡࡵ࡫ࡲࡲ࠴ࡰࡳࡰࡰࠪง"),
    }
    config = {
        bstack11l1l1l_opy_ (u"ࠨࡣࡸࡸ࡭࠭จ"): (bstack1l111l1l1l_opy_, bstack1l1111l11l_opy_),
        bstack11l1l1l_opy_ (u"ࠩ࡫ࡩࡦࡪࡥࡳࡵࠪฉ"): headers
    }
    response = bstack1ll11l1111_opy_(bstack11l1l1l_opy_ (u"ࠪࡔࡔ࡙ࡔࠨช"), bstack1l111111l1_opy_ + bstack11l1l1l_opy_ (u"ࠫ࠴ࡺࡥࡴࡶࡢࡶࡺࡴࡳࠨซ"), data, config)
    bstack1l11111l1l_opy_ = response.json()
    if bstack1l11111l1l_opy_[bstack11l1l1l_opy_ (u"ࠬࡹࡵࡤࡥࡨࡷࡸ࠭ฌ")]:
      parsed = json.loads(os.getenv(bstack11l1l1l_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤ࡚ࡅࡔࡖࡢࡅࡈࡉࡅࡔࡕࡌࡆࡎࡒࡉࡕ࡛ࡢࡇࡔࡔࡆࡊࡉࡘࡖࡆ࡚ࡉࡐࡐࡢ࡝ࡒࡒࠧญ"), bstack11l1l1l_opy_ (u"ࠧࡼࡿࠪฎ")))
      parsed[bstack11l1l1l_opy_ (u"ࠨࡵࡦࡥࡳࡴࡥࡳࡘࡨࡶࡸ࡯࡯࡯ࠩฏ")] = bstack1l11111l1l_opy_[bstack11l1l1l_opy_ (u"ࠩࡧࡥࡹࡧࠧฐ")][bstack11l1l1l_opy_ (u"ࠪࡷࡨࡧ࡮࡯ࡧࡵ࡚ࡪࡸࡳࡪࡱࡱࠫฑ")]
      os.environ[bstack11l1l1l_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡘࡊ࡙ࡔࡠࡃࡆࡇࡊ࡙ࡓࡊࡄࡌࡐࡎ࡚࡙ࡠࡅࡒࡒࡋࡏࡇࡖࡔࡄࡘࡎࡕࡎࡠ࡛ࡐࡐࠬฒ")] = json.dumps(parsed)
      return bstack1l11111l1l_opy_[bstack11l1l1l_opy_ (u"ࠬࡪࡡࡵࡣࠪณ")][bstack11l1l1l_opy_ (u"࠭ࡡࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾ࡚࡯࡬ࡧࡱࠫด")], bstack1l11111l1l_opy_[bstack11l1l1l_opy_ (u"ࠧࡥࡣࡷࡥࠬต")][bstack11l1l1l_opy_ (u"ࠨ࡫ࡧࠫถ")]
    else:
      logger.error(bstack11l1l1l_opy_ (u"ࠩࡈࡼࡨ࡫ࡰࡵ࡫ࡲࡲࠥࡽࡨࡪ࡮ࡨࠤࡷࡻ࡮࡯࡫ࡱ࡫ࠥࡈࡲࡰࡹࡶࡩࡷ࡙ࡴࡢࡥ࡮ࠤࡆࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࠤࡆࡻࡴࡰ࡯ࡤࡸ࡮ࡵ࡮࠻ࠢࠪท") + bstack1l11111l1l_opy_[bstack11l1l1l_opy_ (u"ࠪࡱࡪࡹࡳࡢࡩࡨࠫธ")])
      if bstack1l11111l1l_opy_[bstack11l1l1l_opy_ (u"ࠫࡲ࡫ࡳࡴࡣࡪࡩࠬน")] == bstack11l1l1l_opy_ (u"ࠬࡏ࡮ࡷࡣ࡯࡭ࡩࠦࡣࡰࡰࡩ࡭࡬ࡻࡲࡢࡶ࡬ࡳࡳࠦࡰࡢࡵࡶࡩࡩ࠴ࠧบ"):
        for bstack1l111l1111_opy_ in bstack1l11111l1l_opy_[bstack11l1l1l_opy_ (u"࠭ࡥࡳࡴࡲࡶࡸ࠭ป")]:
          logger.error(bstack1l111l1111_opy_[bstack11l1l1l_opy_ (u"ࠧ࡮ࡧࡶࡷࡦ࡭ࡥࠨผ")])
      return None, None
  except Exception as error:
    logger.error(bstack11l1l1l_opy_ (u"ࠣࡇࡻࡧࡪࡶࡴࡪࡱࡱࠤࡼ࡮ࡩ࡭ࡧࠣࡧࡷ࡫ࡡࡵ࡫ࡱ࡫ࠥࡺࡥࡴࡶࠣࡶࡺࡴࠠࡧࡱࡵࠤࡇࡸ࡯ࡸࡵࡨࡶࡘࡺࡡࡤ࡭ࠣࡅࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࠣࡅࡺࡺ࡯࡮ࡣࡷ࡭ࡴࡴ࠺ࠡࠤฝ") +  str(error))
    return None, None
def bstack1lll11l1l_opy_():
  if os.getenv(bstack11l1l1l_opy_ (u"ࠩࡅࡗࡤࡇ࠱࠲࡛ࡢࡎ࡜࡚ࠧพ")) is None:
    return {
        bstack11l1l1l_opy_ (u"ࠪࡷࡹࡧࡴࡶࡵࠪฟ"): bstack11l1l1l_opy_ (u"ࠫࡪࡸࡲࡰࡴࠪภ"),
        bstack11l1l1l_opy_ (u"ࠬࡳࡥࡴࡵࡤ࡫ࡪ࠭ม"): bstack11l1l1l_opy_ (u"࠭ࡂࡶ࡫࡯ࡨࠥࡩࡲࡦࡣࡷ࡭ࡴࡴࠠࡩࡣࡧࠤ࡫ࡧࡩ࡭ࡧࡧ࠲ࠬย")
    }
  data = {bstack11l1l1l_opy_ (u"ࠧࡦࡰࡧࡘ࡮ࡳࡥࠨร"): bstack1llllll11l_opy_()}
  headers = {
      bstack11l1l1l_opy_ (u"ࠨࡃࡸࡸ࡭ࡵࡲࡪࡼࡤࡸ࡮ࡵ࡮ࠨฤ"): bstack11l1l1l_opy_ (u"ࠩࡅࡩࡦࡸࡥࡳࠢࠪล") + os.getenv(bstack11l1l1l_opy_ (u"ࠥࡆࡘࡥࡁ࠲࠳࡜ࡣࡏ࡝ࡔࠣฦ")),
      bstack11l1l1l_opy_ (u"ࠫࡈࡵ࡮ࡵࡧࡱࡸ࠲࡚ࡹࡱࡧࠪว"): bstack11l1l1l_opy_ (u"ࠬࡧࡰࡱ࡮࡬ࡧࡦࡺࡩࡰࡰ࠲࡮ࡸࡵ࡮ࠨศ")
  }
  response = bstack1ll11l1111_opy_(bstack11l1l1l_opy_ (u"࠭ࡐࡖࡖࠪษ"), bstack1l111111l1_opy_ + bstack11l1l1l_opy_ (u"ࠧ࠰ࡶࡨࡷࡹࡥࡲࡶࡰࡶ࠳ࡸࡺ࡯ࡱࠩส"), data, { bstack11l1l1l_opy_ (u"ࠨࡪࡨࡥࡩ࡫ࡲࡴࠩห"): headers })
  try:
    if response.status_code == 200:
      logger.info(bstack11l1l1l_opy_ (u"ࠤࡅࡶࡴࡽࡳࡦࡴࡖࡸࡦࡩ࡫ࠡࡃࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࠡࡃࡸࡸࡴࡳࡡࡵ࡫ࡲࡲ࡚ࠥࡥࡴࡶࠣࡖࡺࡴࠠ࡮ࡣࡵ࡯ࡪࡪࠠࡢࡵࠣࡧࡴࡳࡰ࡭ࡧࡷࡩࡩࠦࡡࡵࠢࠥฬ") + datetime.utcnow().isoformat() + bstack11l1l1l_opy_ (u"ࠪ࡞ࠬอ"))
      return {bstack11l1l1l_opy_ (u"ࠫࡸࡺࡡࡵࡷࡶࠫฮ"): bstack11l1l1l_opy_ (u"ࠬࡹࡵࡤࡥࡨࡷࡸ࠭ฯ"), bstack11l1l1l_opy_ (u"࠭࡭ࡦࡵࡶࡥ࡬࡫ࠧะ"): bstack11l1l1l_opy_ (u"ࠧࠨั")}
    else:
      response.raise_for_status()
  except requests.RequestException as error:
    logger.error(bstack11l1l1l_opy_ (u"ࠣࡇࡻࡧࡪࡶࡴࡪࡱࡱࠤࡼ࡮ࡩ࡭ࡧࠣࡱࡦࡸ࡫ࡪࡰࡪࠤࡨࡵ࡭ࡱ࡮ࡨࡸ࡮ࡵ࡮ࠡࡱࡩࠤࡇࡸ࡯ࡸࡵࡨࡶࡘࡺࡡࡤ࡭ࠣࡅࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࠣࡅࡺࡺ࡯࡮ࡣࡷ࡭ࡴࡴࠠࡕࡧࡶࡸࠥࡘࡵ࡯࠼ࠣࠦา") + str(error))
    return {
        bstack11l1l1l_opy_ (u"ࠩࡶࡸࡦࡺࡵࡴࠩำ"): bstack11l1l1l_opy_ (u"ࠪࡩࡷࡸ࡯ࡳࠩิ"),
        bstack11l1l1l_opy_ (u"ࠫࡲ࡫ࡳࡴࡣࡪࡩࠬี"): str(error)
    }
def bstack1l11lll1_opy_(caps, options):
  try:
    bstack1l111l1l11_opy_ = caps.get(bstack11l1l1l_opy_ (u"ࠬࡨࡳࡵࡣࡦ࡯࠿ࡵࡰࡵ࡫ࡲࡲࡸ࠭ึ"), {}).get(bstack11l1l1l_opy_ (u"࠭ࡤࡦࡸ࡬ࡧࡪࡔࡡ࡮ࡧࠪื"), caps.get(bstack11l1l1l_opy_ (u"ࠧࡥࡧࡹ࡭ࡨ࡫ุࠧ"), bstack11l1l1l_opy_ (u"ࠨูࠩ")))
    if bstack1l111l1l11_opy_:
      logger.warn(bstack11l1l1l_opy_ (u"ࠤࡄࡧࡨ࡫ࡳࡴ࡫ࡥ࡭ࡱ࡯ࡴࡺࠢࡄࡹࡹࡵ࡭ࡢࡶ࡬ࡳࡳࠦࡷࡪ࡮࡯ࠤࡷࡻ࡮ࠡࡱࡱࡰࡾࠦ࡯࡯ࠢࡇࡩࡸࡱࡴࡰࡲࠣࡦࡷࡵࡷࡴࡧࡵࡷ࠳ࠨฺ"))
      return False
    browser = caps.get(bstack11l1l1l_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡒࡦࡳࡥࠨ฻"), bstack11l1l1l_opy_ (u"ࠫࠬ฼")).lower()
    if browser != bstack11l1l1l_opy_ (u"ࠬࡩࡨࡳࡱࡰࡩࠬ฽"):
      logger.warn(bstack11l1l1l_opy_ (u"ࠨࡁࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾࠦࡁࡶࡶࡲࡱࡦࡺࡩࡰࡰࠣࡻ࡮ࡲ࡬ࠡࡴࡸࡲࠥࡵ࡮࡭ࡻࠣࡳࡳࠦࡃࡩࡴࡲࡱࡪࠦࡢࡳࡱࡺࡷࡪࡸࡳ࠯ࠤ฾"))
      return False
    browser_version = caps.get(bstack11l1l1l_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡗࡧࡵࡷ࡮ࡵ࡮ࠨ฿"), caps.get(bstack11l1l1l_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡡࡹࡩࡷࡹࡩࡰࡰࠪเ")))
    if browser_version and browser_version != bstack11l1l1l_opy_ (u"ࠩ࡯ࡥࡹ࡫ࡳࡵࠩแ") and int(browser_version.split(bstack11l1l1l_opy_ (u"ࠪ࠲ࠬโ"))[0]) <= 94:
      logger.warn(bstack11l1l1l_opy_ (u"ࠦࡆࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࠤࡆࡻࡴࡰ࡯ࡤࡸ࡮ࡵ࡮ࠡࡹ࡬ࡰࡱࠦࡲࡶࡰࠣࡳࡳࡲࡹࠡࡱࡱࠤࡈ࡮ࡲࡰ࡯ࡨࠤࡧࡸ࡯ࡸࡵࡨࡶࠥࡼࡥࡳࡵ࡬ࡳࡳࠦࡧࡳࡧࡤࡸࡪࡸࠠࡵࡪࡤࡲࠥ࠿࠴࠯ࠤใ"))
      return False
    if not options is None:
      bstack1l111l11l1_opy_ = options.to_capabilities().get(bstack11l1l1l_opy_ (u"ࠬ࡭࡯ࡰࡩ࠽ࡧ࡭ࡸ࡯࡮ࡧࡒࡴࡹ࡯࡯࡯ࡵࠪไ"), {})
      if bstack11l1l1l_opy_ (u"࠭࠭࠮ࡪࡨࡥࡩࡲࡥࡴࡵࠪๅ") in bstack1l111l11l1_opy_.get(bstack11l1l1l_opy_ (u"ࠧࡢࡴࡪࡷࠬๆ"), []):
        logger.warn(bstack11l1l1l_opy_ (u"ࠣࡃࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࠡࡃࡸࡸࡴࡳࡡࡵ࡫ࡲࡲࠥࡽࡩ࡭࡮ࠣࡲࡴࡺࠠࡳࡷࡱࠤࡴࡴࠠ࡭ࡧࡪࡥࡨࡿࠠࡩࡧࡤࡨࡱ࡫ࡳࡴࠢࡰࡳࡩ࡫࠮ࠡࡕࡺ࡭ࡹࡩࡨࠡࡶࡲࠤࡳ࡫ࡷࠡࡪࡨࡥࡩࡲࡥࡴࡵࠣࡱࡴࡪࡥࠡࡱࡵࠤࡦࡼ࡯ࡪࡦࠣࡹࡸ࡯࡮ࡨࠢ࡫ࡩࡦࡪ࡬ࡦࡵࡶࠤࡲࡵࡤࡦ࠰ࠥ็"))
        return False
    return True
  except Exception as error:
    logger.debug(bstack11l1l1l_opy_ (u"ࠤࡈࡼࡨ࡫ࡰࡵ࡫ࡲࡲࠥ࡯࡮ࠡࡸࡤࡰ࡮ࡪࡡࡵࡧࠣࡥ࠶࠷ࡹࠡࡵࡸࡴࡵࡵࡲࡵࠢ࠽่ࠦ") + str(error))
    return False
def set_capabilities(caps, config):
  try:
    bstack1l11111ll1_opy_ = config.get(bstack11l1l1l_opy_ (u"ࠪࡥࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࡒࡴࡹ࡯࡯࡯ࡵ้ࠪ"), {})
    bstack1l11111ll1_opy_[bstack11l1l1l_opy_ (u"ࠫࡦࡻࡴࡩࡖࡲ࡯ࡪࡴ๊ࠧ")] = os.getenv(bstack11l1l1l_opy_ (u"ࠬࡈࡓࡠࡃ࠴࠵࡞ࡥࡊࡘࡖ๋ࠪ"))
    bstack1l1111111l_opy_ = json.loads(os.getenv(bstack11l1l1l_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤ࡚ࡅࡔࡖࡢࡅࡈࡉࡅࡔࡕࡌࡆࡎࡒࡉࡕ࡛ࡢࡇࡔࡔࡆࡊࡉࡘࡖࡆ࡚ࡉࡐࡐࡢ࡝ࡒࡒࠧ์"), bstack11l1l1l_opy_ (u"ࠧࡼࡿࠪํ"))).get(bstack11l1l1l_opy_ (u"ࠨࡵࡦࡥࡳࡴࡥࡳࡘࡨࡶࡸ࡯࡯࡯ࠩ๎"))
    caps[bstack11l1l1l_opy_ (u"ࠩࡤࡧࡨ࡫ࡳࡴ࡫ࡥ࡭ࡱ࡯ࡴࡺࠩ๏")] = True
    if bstack11l1l1l_opy_ (u"ࠪࡦࡸࡺࡡࡤ࡭࠽ࡳࡵࡺࡩࡰࡰࡶࠫ๐") in caps:
      caps[bstack11l1l1l_opy_ (u"ࠫࡧࡹࡴࡢࡥ࡮࠾ࡴࡶࡴࡪࡱࡱࡷࠬ๑")][bstack11l1l1l_opy_ (u"ࠬࡧࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽࡔࡶࡴࡪࡱࡱࡷࠬ๒")] = bstack1l11111ll1_opy_
      caps[bstack11l1l1l_opy_ (u"࠭ࡢࡴࡶࡤࡧࡰࡀ࡯ࡱࡶ࡬ࡳࡳࡹࠧ๓")][bstack11l1l1l_opy_ (u"ࠧࡢࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿࡏࡱࡶ࡬ࡳࡳࡹࠧ๔")][bstack11l1l1l_opy_ (u"ࠨࡵࡦࡥࡳࡴࡥࡳࡘࡨࡶࡸ࡯࡯࡯ࠩ๕")] = bstack1l1111111l_opy_
    else:
      caps[bstack11l1l1l_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫࠯ࡣࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࡐࡲࡷ࡭ࡴࡴࡳࠨ๖")] = bstack1l11111ll1_opy_
      caps[bstack11l1l1l_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬࠰ࡤࡧࡨ࡫ࡳࡴ࡫ࡥ࡭ࡱ࡯ࡴࡺࡑࡳࡸ࡮ࡵ࡮ࡴࠩ๗")][bstack11l1l1l_opy_ (u"ࠫࡸࡩࡡ࡯ࡰࡨࡶ࡛࡫ࡲࡴ࡫ࡲࡲࠬ๘")] = bstack1l1111111l_opy_
  except Exception as error:
    logger.debug(bstack11l1l1l_opy_ (u"ࠧࡋࡸࡤࡧࡳࡸ࡮ࡵ࡮ࠡࡹ࡫࡭ࡱ࡫ࠠࡴࡧࡷࡸ࡮ࡴࡧࠡࡃࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࠡࡃࡸࡸࡴࡳࡡࡵ࡫ࡲࡲࠥࡩࡡࡱࡣࡥ࡭ࡱ࡯ࡴࡪࡧࡶ࠲ࠥࡋࡲࡳࡱࡵ࠾ࠥࠨ๙") +  str(error))
def bstack1l1llll111_opy_(driver, bstack1l1111l1l1_opy_):
  try:
    session = driver.session_id
    if session:
      bstack11llllllll_opy_ = True
      current_url = driver.current_url
      try:
        url = urlparse(current_url)
      except Exception as e:
        bstack11llllllll_opy_ = False
      bstack11llllllll_opy_ = url.scheme in [bstack11l1l1l_opy_ (u"ࠨࡨࡵࡶࡳࠦ๚"), bstack11l1l1l_opy_ (u"ࠢࡩࡶࡷࡴࡸࠨ๛")]
      if bstack11llllllll_opy_:
        if bstack1l1111l1l1_opy_:
          logger.info(bstack11l1l1l_opy_ (u"ࠣࡕࡨࡸࡺࡶࠠࡧࡱࡵࠤࡆࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࠤࡹ࡫ࡳࡵ࡫ࡱ࡫ࠥ࡮ࡡࡴࠢࡶࡸࡦࡸࡴࡦࡦ࠱ࠤࡆࡻࡴࡰ࡯ࡤࡸࡪࠦࡴࡦࡵࡷࠤࡨࡧࡳࡦࠢࡨࡼࡪࡩࡵࡵ࡫ࡲࡲࠥࡽࡩ࡭࡮ࠣࡦࡪ࡭ࡩ࡯ࠢࡰࡳࡲ࡫࡮ࡵࡣࡵ࡭ࡱࡿ࠮ࠣ๜"))
          driver.execute_async_script(bstack11l1l1l_opy_ (u"ࠤࠥࠦࠏࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࡩ࡯࡯ࡵࡷࠤࡨࡧ࡬࡭ࡤࡤࡧࡰࠦ࠽ࠡࡣࡵ࡫ࡺࡳࡥ࡯ࡶࡶ࡟ࡦࡸࡧࡶ࡯ࡨࡲࡹࡹ࠮࡭ࡧࡱ࡫ࡹ࡮ࠠ࠮ࠢ࠴ࡡࡀࠐࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࡣࡰࡰࡶࡸࠥ࡬࡮ࠡ࠿ࠣࠬ࠮ࠦ࠽࠿ࠢࡾࠎࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࡹ࡬ࡲࡩࡵࡷ࠯ࡣࡧࡨࡊࡼࡥ࡯ࡶࡏ࡭ࡸࡺࡥ࡯ࡧࡵࠬࠬࡇ࠱࠲࡛ࡢࡘࡆࡖ࡟ࡔࡖࡄࡖ࡙ࡋࡄࠨ࠮ࠣࡪࡳ࠸ࠩ࠼ࠌࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࡣࡰࡰࡶࡸࠥ࡫ࠠ࠾ࠢࡱࡩࡼࠦࡃࡶࡵࡷࡳࡲࡋࡶࡦࡰࡷࠬࠬࡇ࠱࠲࡛ࡢࡊࡔࡘࡃࡆࡡࡖࡘࡆࡘࡔࠨࠫ࠾ࠎࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࡹ࡬ࡲࡩࡵࡷ࠯ࡦ࡬ࡷࡵࡧࡴࡤࡪࡈࡺࡪࡴࡴࠩࡧࠬ࠿ࠏࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࢃ࠻ࠋࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࡥࡲࡲࡸࡺࠠࡧࡰ࠵ࠤࡂࠦࠨࠪࠢࡀࡂࠥࢁࠊࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࡼ࡯࡮ࡥࡱࡺ࠲ࡷ࡫࡭ࡰࡸࡨࡉࡻ࡫࡮ࡵࡎ࡬ࡷࡹ࡫࡮ࡦࡴࠫࠫࡆ࠷࠱࡚ࡡࡗࡅࡕࡥࡓࡕࡃࡕࡘࡊࡊࠧ࠭ࠢࡩࡲ࠮ࡁࠊࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࡨࡧ࡬࡭ࡤࡤࡧࡰ࠮ࠩ࠼ࠌࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࢀࠎࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤ࡫ࡴࠨࠪ࠽ࠍࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠢࠣࠤ๝"))
          logger.info(bstack11l1l1l_opy_ (u"ࠥࡅࡺࡺ࡯࡮ࡣࡷࡩࠥࡺࡥࡴࡶࠣࡧࡦࡹࡥࠡࡧࡻࡩࡨࡻࡴࡪࡱࡱࠤ࡭ࡧࡳࠡࡵࡷࡥࡷࡺࡥࡥ࠰ࠥ๞"))
        else:
          driver.execute_script(bstack11l1l1l_opy_ (u"ࠦࠧࠨࠊࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࡤࡱࡱࡷࡹࠦࡥࠡ࠿ࠣࡲࡪࡽࠠࡄࡷࡶࡸࡴࡳࡅࡷࡧࡱࡸ࠭࠭ࡁ࠲࠳࡜ࡣࡋࡕࡒࡄࡇࡢࡗ࡙ࡕࡐࠨࠫ࠾ࠎࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࡼ࡯࡮ࡥࡱࡺ࠲ࡩ࡯ࡳࡱࡣࡷࡧ࡭ࡋࡶࡦࡰࡷࠬࡪ࠯࠻ࠋࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠧࠨࠢ๟"))
      return bstack1l1111l1l1_opy_
  except Exception as e:
    logger.error(bstack11l1l1l_opy_ (u"ࠧࡋࡸࡤࡧࡳࡸ࡮ࡵ࡮ࠡ࡫ࡱࠤࡸࡺࡡࡳࡶ࡬ࡲ࡬ࠦࡡࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾࠦࡡࡶࡶࡲࡱࡦࡺࡩࡰࡰࠣࡷࡨࡧ࡮ࠡࡨࡲࡶࠥࡺࡨࡪࡵࠣࡸࡪࡹࡴࠡࡥࡤࡷࡪࡀࠠࠣ๠") + str(e))
    return False
def bstack11l11lll1_opy_(driver, class_name, name, module_name, path, bstack1l1lll1111_opy_):
  try:
    bstack1l11111111_opy_ = [class_name] if not class_name is None else []
    bstack1l1111ll1l_opy_ = {
        bstack11l1l1l_opy_ (u"ࠨࡳࡢࡸࡨࡖࡪࡹࡵ࡭ࡶࡶࠦ๡"): True,
        bstack11l1l1l_opy_ (u"ࠢࡵࡧࡶࡸࡉ࡫ࡴࡢ࡫࡯ࡷࠧ๢"): {
            bstack11l1l1l_opy_ (u"ࠣࡰࡤࡱࡪࠨ๣"): name,
            bstack11l1l1l_opy_ (u"ࠤࡷࡩࡸࡺࡒࡶࡰࡌࡨࠧ๤"): os.environ.get(bstack11l1l1l_opy_ (u"ࠪࡆࡘࡥࡁ࠲࠳࡜ࡣ࡙ࡋࡓࡕࡡࡕ࡙ࡓࡥࡉࡅࠩ๥")),
            bstack11l1l1l_opy_ (u"ࠦ࡫࡯࡬ࡦࡒࡤࡸ࡭ࠨ๦"): str(path),
            bstack11l1l1l_opy_ (u"ࠧࡹࡣࡰࡲࡨࡐ࡮ࡹࡴࠣ๧"): [module_name, *bstack1l11111111_opy_, name],
        },
        bstack11l1l1l_opy_ (u"ࠨࡰ࡭ࡣࡷࡪࡴࡸ࡭ࠣ๨"): _1l111l111l_opy_(driver, bstack1l1lll1111_opy_)
    }
    driver.execute_script(bstack11l1l1l_opy_ (u"ࠢࠣࠤࠍࠤࠥࠦࠠࠡࠢࠣࠤࡨࡵ࡮ࡴࡶࠣࡧࡦࡲ࡬ࡣࡣࡦ࡯ࠥࡃࠠࡢࡴࡪࡹࡲ࡫࡮ࡵࡵ࡞ࡥࡷ࡭ࡵ࡮ࡧࡱࡸࡸ࠴࡬ࡦࡰࡪࡸ࡭ࠦ࠭ࠡ࠳ࡠ࠿ࠏࠦࠠࠡࠢࠣࠤࠥࠦࡴࡩ࡫ࡶ࠲ࡷ࡫ࡳࠡ࠿ࠣࡲࡺࡲ࡬࠼ࠌࠣࠤࠥࠦࠠࠡࠢࠣ࡭࡫ࠦࠨࡢࡴࡪࡹࡲ࡫࡮ࡵࡵ࡞࠴ࡢ࠴ࡳࡢࡸࡨࡖࡪࡹࡵ࡭ࡶࡶ࠭ࠥࢁࠊࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࡽࡩ࡯ࡦࡲࡻ࠳ࡧࡤࡥࡇࡹࡩࡳࡺࡌࡪࡵࡷࡩࡳ࡫ࡲࠩࠩࡄ࠵࠶࡟࡟ࡕࡃࡓࡣ࡙ࡘࡁࡏࡕࡓࡓࡗ࡚ࡅࡓࠩ࠯ࠤ࠭࡫ࡶࡦࡰࡷ࠭ࠥࡃ࠾ࠡࡽࠍࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࡽࡩ࡯ࡦࡲࡻ࠳ࡺࡡࡱࡖࡵࡥࡳࡹࡰࡰࡴࡷࡩࡷࡊࡡࡵࡣࠣࡁࠥ࡫ࡶࡦࡰࡷ࠲ࡩ࡫ࡴࡢ࡫࡯࠿ࠏࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࡵࡪ࡬ࡷ࠳ࡸࡥࡴࠢࡀࠤࡼ࡯࡮ࡥࡱࡺ࠲ࡹࡧࡰࡕࡴࡤࡲࡸࡶ࡯ࡳࡶࡨࡶࡉࡧࡴࡢ࠽ࠍࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࡩࡡ࡭࡮ࡥࡥࡨࡱࠨࡵࡪ࡬ࡷ࠳ࡸࡥࡴࠫ࠾ࠎࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࢀ࠭ࡀࠐࠠࠡࠢࠣࠤࠥࠦࠠࡾࠌࠣࠤࠥࠦࠠࠡࠢࠣࡧࡴࡴࡳࡵࠢࡨࠤࡂࠦ࡮ࡦࡹࠣࡇࡺࡹࡴࡰ࡯ࡈࡺࡪࡴࡴࠩࠩࡄ࠵࠶࡟࡟ࡕࡇࡖࡘࡤࡋࡎࡅࠩ࠯ࠤࢀࠦࡤࡦࡶࡤ࡭ࡱࡀࠠࡢࡴࡪࡹࡲ࡫࡮ࡵࡵ࡞࠴ࡢࠦࡽࠪ࠽ࠍࠤࠥࠦࠠࠡࠢࠣࠤࡼ࡯࡮ࡥࡱࡺ࠲ࡩ࡯ࡳࡱࡣࡷࡧ࡭ࡋࡶࡦࡰࡷࠬࡪ࠯࠻ࠋࠢࠣࠤࠥࠦࠠࠡࠢ࡬ࡪࠥ࠮ࠡࡢࡴࡪࡹࡲ࡫࡮ࡵࡵ࡞࠴ࡢ࠴ࡳࡢࡸࡨࡖࡪࡹࡵ࡭ࡶࡶ࠭ࠥࢁࠊࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࡩࡡ࡭࡮ࡥࡥࡨࡱࠨࠪ࠽ࠍࠤࠥࠦࠠࠡࠢࠣࠤࢂࠐࠠࠡࠢࠣࠦࠧࠨ๩"), bstack1l1111ll1l_opy_)
    logger.info(bstack11l1l1l_opy_ (u"ࠣࡃࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࠡࡶࡨࡷࡹ࡯࡮ࡨࠢࡩࡳࡷࠦࡴࡩ࡫ࡶࠤࡹ࡫ࡳࡵࠢࡦࡥࡸ࡫ࠠࡩࡣࡶࠤࡪࡴࡤࡦࡦ࠱ࠦ๪"))
  except Exception as bstack11lllllll1_opy_:
    logger.error(bstack11l1l1l_opy_ (u"ࠤࡄࡧࡨ࡫ࡳࡴ࡫ࡥ࡭ࡱ࡯ࡴࡺࠢࡵࡩࡸࡻ࡬ࡵࡵࠣࡧࡴࡻ࡬ࡥࠢࡱࡳࡹࠦࡢࡦࠢࡳࡶࡴࡩࡥࡴࡵࡨࡨࠥ࡬࡯ࡳࠢࡷ࡬ࡪࠦࡴࡦࡵࡷࠤࡨࡧࡳࡦ࠼ࠣࠦ๫") + str(path) + bstack11l1l1l_opy_ (u"ࠥࠤࡊࡸࡲࡰࡴࠣ࠾ࠧ๬") + str(bstack11lllllll1_opy_))