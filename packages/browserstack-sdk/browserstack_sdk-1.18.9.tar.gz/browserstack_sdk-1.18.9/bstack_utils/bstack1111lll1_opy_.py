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
import requests
import logging
from urllib.parse import urlparse
from datetime import datetime
from bstack_utils.constants import bstack1l1111l1l1_opy_ as bstack1l111111l1_opy_
from bstack_utils.helper import bstack1ll11111ll_opy_, bstack1ll111ll1_opy_, bstack1l11111ll1_opy_, bstack1l111l1111_opy_, bstack1ll11ll1ll_opy_, get_host_info, bstack1l111l111l_opy_, bstack1111l1lll_opy_, bstack1l1l1ll111_opy_
from browserstack_sdk._version import __version__
logger = logging.getLogger(__name__)
@bstack1l1l1ll111_opy_(class_method=False)
def _11lllllll1_opy_(driver, bstack1l1ll11ll1_opy_):
  response = {}
  try:
    caps = driver.capabilities
    response = {
        bstack11l1ll_opy_ (u"ࠧࡰࡵࡢࡲࡦࡳࡥࠨශ"): caps.get(bstack11l1ll_opy_ (u"ࠨࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࡑࡥࡲ࡫ࠧෂ"), None),
        bstack11l1ll_opy_ (u"ࠩࡲࡷࡤࡼࡥࡳࡵ࡬ࡳࡳ࠭ස"): bstack1l1ll11ll1_opy_.get(bstack11l1ll_opy_ (u"ࠪࡳࡸ࡜ࡥࡳࡵ࡬ࡳࡳ࠭හ"), None),
        bstack11l1ll_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡤࡴࡡ࡮ࡧࠪළ"): caps.get(bstack11l1ll_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡔࡡ࡮ࡧࠪෆ"), None),
        bstack11l1ll_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸ࡟ࡷࡧࡵࡷ࡮ࡵ࡮ࠨ෇"): caps.get(bstack11l1ll_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡗࡧࡵࡷ࡮ࡵ࡮ࠨ෈"), None)
    }
  except Exception as error:
    logger.debug(bstack11l1ll_opy_ (u"ࠨࡇࡻࡧࡪࡶࡴࡪࡱࡱࠤ࡮ࡴࠠࡧࡧࡷࡧ࡭࡯࡮ࡨࠢࡳࡰࡦࡺࡦࡰࡴࡰࠤࡩ࡫ࡴࡢ࡫࡯ࡷࠥࡽࡩࡵࡪࠣࡩࡷࡸ࡯ࡳࠢ࠽ࠤࠬ෉") + str(error))
  return response
def bstack1ll1lll111_opy_(config):
  return config.get(bstack11l1ll_opy_ (u"ࠩࡤࡧࡨ࡫ࡳࡴ࡫ࡥ࡭ࡱ࡯ࡴࡺ්ࠩ"), False) or any([p.get(bstack11l1ll_opy_ (u"ࠪࡥࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࠪ෋"), False) == True for p in config[bstack11l1ll_opy_ (u"ࠫࡵࡲࡡࡵࡨࡲࡶࡲࡹࠧ෌")]])
def bstack1lll111lll_opy_(config, bstack11111111_opy_):
  try:
    if not bstack1ll111ll1_opy_(config):
      return False
    bstack1l1111ll1l_opy_ = config.get(bstack11l1ll_opy_ (u"ࠬࡧࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽࠬ෍"), False)
    bstack1l11111lll_opy_ = config[bstack11l1ll_opy_ (u"࠭ࡰ࡭ࡣࡷࡪࡴࡸ࡭ࡴࠩ෎")][bstack11111111_opy_].get(bstack11l1ll_opy_ (u"ࠧࡢࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿࠧා"), None)
    if bstack1l11111lll_opy_ != None:
      bstack1l1111ll1l_opy_ = bstack1l11111lll_opy_
    bstack11llllll11_opy_ = os.getenv(bstack11l1ll_opy_ (u"ࠨࡄࡖࡣࡆ࠷࠱࡚ࡡࡍ࡛࡙࠭ැ")) is not None and len(os.getenv(bstack11l1ll_opy_ (u"ࠩࡅࡗࡤࡇ࠱࠲࡛ࡢࡎ࡜࡚ࠧෑ"))) > 0 and os.getenv(bstack11l1ll_opy_ (u"ࠪࡆࡘࡥࡁ࠲࠳࡜ࡣࡏ࡝ࡔࠨි")) != bstack11l1ll_opy_ (u"ࠫࡳࡻ࡬࡭ࠩී")
    return bstack1l1111ll1l_opy_ and bstack11llllll11_opy_
  except Exception as error:
    logger.debug(bstack11l1ll_opy_ (u"ࠬࡋࡸࡤࡧࡳࡸ࡮ࡵ࡮ࠡ࡫ࡱࠤࡻ࡫ࡲࡪࡨࡼ࡭ࡳ࡭ࠠࡵࡪࡨࠤࡆࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࠤࡸ࡫ࡳࡴ࡫ࡲࡲࠥࡽࡩࡵࡪࠣࡩࡷࡸ࡯ࡳࠢ࠽ࠤࠬු") + str(error))
  return False
def bstack1llllll111_opy_(bstack1l1111ll11_opy_, test_tags):
  bstack1l1111ll11_opy_ = os.getenv(bstack11l1ll_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤ࡚ࡅࡔࡖࡢࡅࡈࡉࡅࡔࡕࡌࡆࡎࡒࡉࡕ࡛ࡢࡇࡔࡔࡆࡊࡉࡘࡖࡆ࡚ࡉࡐࡐࡢ࡝ࡒࡒࠧ෕"))
  if bstack1l1111ll11_opy_ is None:
    return True
  bstack1l1111ll11_opy_ = json.loads(bstack1l1111ll11_opy_)
  try:
    include_tags = bstack1l1111ll11_opy_[bstack11l1ll_opy_ (u"ࠧࡪࡰࡦࡰࡺࡪࡥࡕࡣࡪࡷࡎࡴࡔࡦࡵࡷ࡭ࡳ࡭ࡓࡤࡱࡳࡩࠬූ")] if bstack11l1ll_opy_ (u"ࠨ࡫ࡱࡧࡱࡻࡤࡦࡖࡤ࡫ࡸࡏ࡮ࡕࡧࡶࡸ࡮ࡴࡧࡔࡥࡲࡴࡪ࠭෗") in bstack1l1111ll11_opy_ and isinstance(bstack1l1111ll11_opy_[bstack11l1ll_opy_ (u"ࠩ࡬ࡲࡨࡲࡵࡥࡧࡗࡥ࡬ࡹࡉ࡯ࡖࡨࡷࡹ࡯࡮ࡨࡕࡦࡳࡵ࡫ࠧෘ")], list) else []
    exclude_tags = bstack1l1111ll11_opy_[bstack11l1ll_opy_ (u"ࠪࡩࡽࡩ࡬ࡶࡦࡨࡘࡦ࡭ࡳࡊࡰࡗࡩࡸࡺࡩ࡯ࡩࡖࡧࡴࡶࡥࠨෙ")] if bstack11l1ll_opy_ (u"ࠫࡪࡾࡣ࡭ࡷࡧࡩ࡙ࡧࡧࡴࡋࡱࡘࡪࡹࡴࡪࡰࡪࡗࡨࡵࡰࡦࠩේ") in bstack1l1111ll11_opy_ and isinstance(bstack1l1111ll11_opy_[bstack11l1ll_opy_ (u"ࠬ࡫ࡸࡤ࡮ࡸࡨࡪ࡚ࡡࡨࡵࡌࡲ࡙࡫ࡳࡵ࡫ࡱ࡫ࡘࡩ࡯ࡱࡧࠪෛ")], list) else []
    excluded = any(tag in exclude_tags for tag in test_tags)
    included = len(include_tags) == 0 or any(tag in include_tags for tag in test_tags)
    return not excluded and included
  except Exception as error:
    logger.debug(bstack11l1ll_opy_ (u"ࠨࡅࡳࡴࡲࡶࠥࡽࡨࡪ࡮ࡨࠤࡻࡧ࡬ࡪࡦࡤࡸ࡮ࡴࡧࠡࡶࡨࡷࡹࠦࡣࡢࡵࡨࠤ࡫ࡵࡲࠡࡣࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࠡࡤࡨࡪࡴࡸࡥࠡࡵࡦࡥࡳࡴࡩ࡯ࡩ࠱ࠤࡊࡸࡲࡰࡴࠣ࠾ࠥࠨො") + str(error))
  return False
def bstack1ll11l1l11_opy_(config, bstack1l1111llll_opy_, bstack1l1111l11l_opy_):
  bstack11llllllll_opy_ = bstack1l11111ll1_opy_(config)
  bstack1l111111ll_opy_ = bstack1l111l1111_opy_(config)
  if bstack11llllllll_opy_ is None or bstack1l111111ll_opy_ is None:
    logger.error(bstack11l1ll_opy_ (u"ࠧࡆࡺࡦࡩࡵࡺࡩࡰࡰࠣࡻ࡭࡯࡬ࡦࠢࡦࡶࡪࡧࡴࡪࡰࡪࠤࡹ࡫ࡳࡵࠢࡵࡹࡳࠦࡦࡰࡴࠣࡆࡷࡵࡷࡴࡧࡵࡗࡹࡧࡣ࡬ࠢࡄࡧࡨ࡫ࡳࡴ࡫ࡥ࡭ࡱ࡯ࡴࡺࠢࡄࡹࡹࡵ࡭ࡢࡶ࡬ࡳࡳࡀࠠࡎ࡫ࡶࡷ࡮ࡴࡧࠡࡣࡸࡸ࡭࡫࡮ࡵ࡫ࡦࡥࡹ࡯࡯࡯ࠢࡷࡳࡰ࡫࡮ࠨෝ"))
    return [None, None]
  try:
    settings = json.loads(os.getenv(bstack11l1ll_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡕࡇࡖࡘࡤࡇࡃࡄࡇࡖࡗࡎࡈࡉࡍࡋࡗ࡝ࡤࡉࡏࡏࡈࡌࡋ࡚ࡘࡁࡕࡋࡒࡒࡤ࡟ࡍࡍࠩෞ"), bstack11l1ll_opy_ (u"ࠩࡾࢁࠬෟ")))
    data = {
        bstack11l1ll_opy_ (u"ࠪࡴࡷࡵࡪࡦࡥࡷࡒࡦࡳࡥࠨ෠"): config[bstack11l1ll_opy_ (u"ࠫࡵࡸ࡯࡫ࡧࡦࡸࡓࡧ࡭ࡦࠩ෡")],
        bstack11l1ll_opy_ (u"ࠬࡨࡵࡪ࡮ࡧࡒࡦࡳࡥࠨ෢"): config.get(bstack11l1ll_opy_ (u"࠭ࡢࡶ࡫࡯ࡨࡓࡧ࡭ࡦࠩ෣"), os.path.basename(os.getcwd())),
        bstack11l1ll_opy_ (u"ࠧࡴࡶࡤࡶࡹ࡚ࡩ࡮ࡧࠪ෤"): bstack1ll11111ll_opy_(),
        bstack11l1ll_opy_ (u"ࠨࡦࡨࡷࡨࡸࡩࡱࡶ࡬ࡳࡳ࠭෥"): config.get(bstack11l1ll_opy_ (u"ࠩࡥࡹ࡮ࡲࡤࡅࡧࡶࡧࡷ࡯ࡰࡵ࡫ࡲࡲࠬ෦"), bstack11l1ll_opy_ (u"ࠪࠫ෧")),
        bstack11l1ll_opy_ (u"ࠫࡸࡵࡵࡳࡥࡨࠫ෨"): {
            bstack11l1ll_opy_ (u"ࠬ࡬ࡲࡢ࡯ࡨࡻࡴࡸ࡫ࡏࡣࡰࡩࠬ෩"): bstack1l1111llll_opy_,
            bstack11l1ll_opy_ (u"࠭ࡦࡳࡣࡰࡩࡼࡵࡲ࡬ࡘࡨࡶࡸ࡯࡯࡯ࠩ෪"): bstack1l1111l11l_opy_,
            bstack11l1ll_opy_ (u"ࠧࡴࡦ࡮࡚ࡪࡸࡳࡪࡱࡱࠫ෫"): __version__
        },
        bstack11l1ll_opy_ (u"ࠨࡵࡨࡸࡹ࡯࡮ࡨࡵࠪ෬"): settings,
        bstack11l1ll_opy_ (u"ࠩࡹࡩࡷࡹࡩࡰࡰࡆࡳࡳࡺࡲࡰ࡮ࠪ෭"): bstack1l111l111l_opy_(),
        bstack11l1ll_opy_ (u"ࠪࡧ࡮ࡏ࡮ࡧࡱࠪ෮"): bstack1ll11ll1ll_opy_(),
        bstack11l1ll_opy_ (u"ࠫ࡭ࡵࡳࡵࡋࡱࡪࡴ࠭෯"): get_host_info(),
        bstack11l1ll_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࡅࡺࡺ࡯࡮ࡣࡷ࡭ࡴࡴࠧ෰"): bstack1ll111ll1_opy_(config)
    }
    headers = {
        bstack11l1ll_opy_ (u"࠭ࡃࡰࡰࡷࡩࡳࡺ࠭ࡕࡻࡳࡩࠬ෱"): bstack11l1ll_opy_ (u"ࠧࡢࡲࡳࡰ࡮ࡩࡡࡵ࡫ࡲࡲ࠴ࡰࡳࡰࡰࠪෲ"),
    }
    config = {
        bstack11l1ll_opy_ (u"ࠨࡣࡸࡸ࡭࠭ෳ"): (bstack11llllllll_opy_, bstack1l111111ll_opy_),
        bstack11l1ll_opy_ (u"ࠩ࡫ࡩࡦࡪࡥࡳࡵࠪ෴"): headers
    }
    response = bstack1111l1lll_opy_(bstack11l1ll_opy_ (u"ࠪࡔࡔ࡙ࡔࠨ෵"), bstack1l111111l1_opy_ + bstack11l1ll_opy_ (u"ࠫ࠴ࡺࡥࡴࡶࡢࡶࡺࡴࡳࠨ෶"), data, config)
    bstack1l11111l1l_opy_ = response.json()
    if bstack1l11111l1l_opy_[bstack11l1ll_opy_ (u"ࠬࡹࡵࡤࡥࡨࡷࡸ࠭෷")]:
      parsed = json.loads(os.getenv(bstack11l1ll_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤ࡚ࡅࡔࡖࡢࡅࡈࡉࡅࡔࡕࡌࡆࡎࡒࡉࡕ࡛ࡢࡇࡔࡔࡆࡊࡉࡘࡖࡆ࡚ࡉࡐࡐࡢ࡝ࡒࡒࠧ෸"), bstack11l1ll_opy_ (u"ࠧࡼࡿࠪ෹")))
      parsed[bstack11l1ll_opy_ (u"ࠨࡵࡦࡥࡳࡴࡥࡳࡘࡨࡶࡸ࡯࡯࡯ࠩ෺")] = bstack1l11111l1l_opy_[bstack11l1ll_opy_ (u"ࠩࡧࡥࡹࡧࠧ෻")][bstack11l1ll_opy_ (u"ࠪࡷࡨࡧ࡮࡯ࡧࡵ࡚ࡪࡸࡳࡪࡱࡱࠫ෼")]
      os.environ[bstack11l1ll_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡘࡊ࡙ࡔࡠࡃࡆࡇࡊ࡙ࡓࡊࡄࡌࡐࡎ࡚࡙ࡠࡅࡒࡒࡋࡏࡇࡖࡔࡄࡘࡎࡕࡎࡠ࡛ࡐࡐࠬ෽")] = json.dumps(parsed)
      return bstack1l11111l1l_opy_[bstack11l1ll_opy_ (u"ࠬࡪࡡࡵࡣࠪ෾")][bstack11l1ll_opy_ (u"࠭ࡡࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾ࡚࡯࡬ࡧࡱࠫ෿")], bstack1l11111l1l_opy_[bstack11l1ll_opy_ (u"ࠧࡥࡣࡷࡥࠬ฀")][bstack11l1ll_opy_ (u"ࠨ࡫ࡧࠫก")]
    else:
      logger.error(bstack11l1ll_opy_ (u"ࠩࡈࡼࡨ࡫ࡰࡵ࡫ࡲࡲࠥࡽࡨࡪ࡮ࡨࠤࡷࡻ࡮࡯࡫ࡱ࡫ࠥࡈࡲࡰࡹࡶࡩࡷ࡙ࡴࡢࡥ࡮ࠤࡆࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࠤࡆࡻࡴࡰ࡯ࡤࡸ࡮ࡵ࡮࠻ࠢࠪข") + bstack1l11111l1l_opy_[bstack11l1ll_opy_ (u"ࠪࡱࡪࡹࡳࡢࡩࡨࠫฃ")])
      if bstack1l11111l1l_opy_[bstack11l1ll_opy_ (u"ࠫࡲ࡫ࡳࡴࡣࡪࡩࠬค")] == bstack11l1ll_opy_ (u"ࠬࡏ࡮ࡷࡣ࡯࡭ࡩࠦࡣࡰࡰࡩ࡭࡬ࡻࡲࡢࡶ࡬ࡳࡳࠦࡰࡢࡵࡶࡩࡩ࠴ࠧฅ"):
        for bstack1l1111lll1_opy_ in bstack1l11111l1l_opy_[bstack11l1ll_opy_ (u"࠭ࡥࡳࡴࡲࡶࡸ࠭ฆ")]:
          logger.error(bstack1l1111lll1_opy_[bstack11l1ll_opy_ (u"ࠧ࡮ࡧࡶࡷࡦ࡭ࡥࠨง")])
      return None, None
  except Exception as error:
    logger.error(bstack11l1ll_opy_ (u"ࠣࡇࡻࡧࡪࡶࡴࡪࡱࡱࠤࡼ࡮ࡩ࡭ࡧࠣࡧࡷ࡫ࡡࡵ࡫ࡱ࡫ࠥࡺࡥࡴࡶࠣࡶࡺࡴࠠࡧࡱࡵࠤࡇࡸ࡯ࡸࡵࡨࡶࡘࡺࡡࡤ࡭ࠣࡅࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࠣࡅࡺࡺ࡯࡮ࡣࡷ࡭ࡴࡴ࠺ࠡࠤจ") +  str(error))
    return None, None
def bstack1ll1111l11_opy_():
  if os.getenv(bstack11l1ll_opy_ (u"ࠩࡅࡗࡤࡇ࠱࠲࡛ࡢࡎ࡜࡚ࠧฉ")) is None:
    return {
        bstack11l1ll_opy_ (u"ࠪࡷࡹࡧࡴࡶࡵࠪช"): bstack11l1ll_opy_ (u"ࠫࡪࡸࡲࡰࡴࠪซ"),
        bstack11l1ll_opy_ (u"ࠬࡳࡥࡴࡵࡤ࡫ࡪ࠭ฌ"): bstack11l1ll_opy_ (u"࠭ࡂࡶ࡫࡯ࡨࠥࡩࡲࡦࡣࡷ࡭ࡴࡴࠠࡩࡣࡧࠤ࡫ࡧࡩ࡭ࡧࡧ࠲ࠬญ")
    }
  data = {bstack11l1ll_opy_ (u"ࠧࡦࡰࡧࡘ࡮ࡳࡥࠨฎ"): bstack1ll11111ll_opy_()}
  headers = {
      bstack11l1ll_opy_ (u"ࠨࡃࡸࡸ࡭ࡵࡲࡪࡼࡤࡸ࡮ࡵ࡮ࠨฏ"): bstack11l1ll_opy_ (u"ࠩࡅࡩࡦࡸࡥࡳࠢࠪฐ") + os.getenv(bstack11l1ll_opy_ (u"ࠥࡆࡘࡥࡁ࠲࠳࡜ࡣࡏ࡝ࡔࠣฑ")),
      bstack11l1ll_opy_ (u"ࠫࡈࡵ࡮ࡵࡧࡱࡸ࠲࡚ࡹࡱࡧࠪฒ"): bstack11l1ll_opy_ (u"ࠬࡧࡰࡱ࡮࡬ࡧࡦࡺࡩࡰࡰ࠲࡮ࡸࡵ࡮ࠨณ")
  }
  response = bstack1111l1lll_opy_(bstack11l1ll_opy_ (u"࠭ࡐࡖࡖࠪด"), bstack1l111111l1_opy_ + bstack11l1ll_opy_ (u"ࠧ࠰ࡶࡨࡷࡹࡥࡲࡶࡰࡶ࠳ࡸࡺ࡯ࡱࠩต"), data, { bstack11l1ll_opy_ (u"ࠨࡪࡨࡥࡩ࡫ࡲࡴࠩถ"): headers })
  try:
    if response.status_code == 200:
      logger.info(bstack11l1ll_opy_ (u"ࠤࡅࡶࡴࡽࡳࡦࡴࡖࡸࡦࡩ࡫ࠡࡃࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࠡࡃࡸࡸࡴࡳࡡࡵ࡫ࡲࡲ࡚ࠥࡥࡴࡶࠣࡖࡺࡴࠠ࡮ࡣࡵ࡯ࡪࡪࠠࡢࡵࠣࡧࡴࡳࡰ࡭ࡧࡷࡩࡩࠦࡡࡵࠢࠥท") + datetime.utcnow().isoformat() + bstack11l1ll_opy_ (u"ࠪ࡞ࠬธ"))
      return {bstack11l1ll_opy_ (u"ࠫࡸࡺࡡࡵࡷࡶࠫน"): bstack11l1ll_opy_ (u"ࠬࡹࡵࡤࡥࡨࡷࡸ࠭บ"), bstack11l1ll_opy_ (u"࠭࡭ࡦࡵࡶࡥ࡬࡫ࠧป"): bstack11l1ll_opy_ (u"ࠧࠨผ")}
    else:
      response.raise_for_status()
  except requests.RequestException as error:
    logger.error(bstack11l1ll_opy_ (u"ࠣࡇࡻࡧࡪࡶࡴࡪࡱࡱࠤࡼ࡮ࡩ࡭ࡧࠣࡱࡦࡸ࡫ࡪࡰࡪࠤࡨࡵ࡭ࡱ࡮ࡨࡸ࡮ࡵ࡮ࠡࡱࡩࠤࡇࡸ࡯ࡸࡵࡨࡶࡘࡺࡡࡤ࡭ࠣࡅࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࠣࡅࡺࡺ࡯࡮ࡣࡷ࡭ࡴࡴࠠࡕࡧࡶࡸࠥࡘࡵ࡯࠼ࠣࠦฝ") + str(error))
    return {
        bstack11l1ll_opy_ (u"ࠩࡶࡸࡦࡺࡵࡴࠩพ"): bstack11l1ll_opy_ (u"ࠪࡩࡷࡸ࡯ࡳࠩฟ"),
        bstack11l1ll_opy_ (u"ࠫࡲ࡫ࡳࡴࡣࡪࡩࠬภ"): str(error)
    }
def bstack111l11l1_opy_(caps, options):
  try:
    bstack11lllll1ll_opy_ = caps.get(bstack11l1ll_opy_ (u"ࠬࡨࡳࡵࡣࡦ࡯࠿ࡵࡰࡵ࡫ࡲࡲࡸ࠭ม"), {}).get(bstack11l1ll_opy_ (u"࠭ࡤࡦࡸ࡬ࡧࡪࡔࡡ࡮ࡧࠪย"), caps.get(bstack11l1ll_opy_ (u"ࠧࡥࡧࡹ࡭ࡨ࡫ࠧร"), bstack11l1ll_opy_ (u"ࠨࠩฤ")))
    if bstack11lllll1ll_opy_:
      logger.warn(bstack11l1ll_opy_ (u"ࠤࡄࡧࡨ࡫ࡳࡴ࡫ࡥ࡭ࡱ࡯ࡴࡺࠢࡄࡹࡹࡵ࡭ࡢࡶ࡬ࡳࡳࠦࡷࡪ࡮࡯ࠤࡷࡻ࡮ࠡࡱࡱࡰࡾࠦ࡯࡯ࠢࡇࡩࡸࡱࡴࡰࡲࠣࡦࡷࡵࡷࡴࡧࡵࡷ࠳ࠨล"))
      return False
    browser = caps.get(bstack11l1ll_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡒࡦࡳࡥࠨฦ"), bstack11l1ll_opy_ (u"ࠫࠬว")).lower()
    if browser != bstack11l1ll_opy_ (u"ࠬࡩࡨࡳࡱࡰࡩࠬศ"):
      logger.warn(bstack11l1ll_opy_ (u"ࠨࡁࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾࠦࡁࡶࡶࡲࡱࡦࡺࡩࡰࡰࠣࡻ࡮ࡲ࡬ࠡࡴࡸࡲࠥࡵ࡮࡭ࡻࠣࡳࡳࠦࡃࡩࡴࡲࡱࡪࠦࡢࡳࡱࡺࡷࡪࡸࡳ࠯ࠤษ"))
      return False
    browser_version = caps.get(bstack11l1ll_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡗࡧࡵࡷ࡮ࡵ࡮ࠨส"), caps.get(bstack11l1ll_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡡࡹࡩࡷࡹࡩࡰࡰࠪห")))
    if browser_version and browser_version != bstack11l1ll_opy_ (u"ࠩ࡯ࡥࡹ࡫ࡳࡵࠩฬ") and int(browser_version.split(bstack11l1ll_opy_ (u"ࠪ࠲ࠬอ"))[0]) <= 94:
      logger.warn(bstack11l1ll_opy_ (u"ࠦࡆࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࠤࡆࡻࡴࡰ࡯ࡤࡸ࡮ࡵ࡮ࠡࡹ࡬ࡰࡱࠦࡲࡶࡰࠣࡳࡳࡲࡹࠡࡱࡱࠤࡈ࡮ࡲࡰ࡯ࡨࠤࡧࡸ࡯ࡸࡵࡨࡶࠥࡼࡥࡳࡵ࡬ࡳࡳࠦࡧࡳࡧࡤࡸࡪࡸࠠࡵࡪࡤࡲࠥ࠿࠴࠯ࠤฮ"))
      return False
    if not options is None:
      bstack1l11111111_opy_ = options.to_capabilities().get(bstack11l1ll_opy_ (u"ࠬ࡭࡯ࡰࡩ࠽ࡧ࡭ࡸ࡯࡮ࡧࡒࡴࡹ࡯࡯࡯ࡵࠪฯ"), {})
      if bstack11l1ll_opy_ (u"࠭࠭࠮ࡪࡨࡥࡩࡲࡥࡴࡵࠪะ") in bstack1l11111111_opy_.get(bstack11l1ll_opy_ (u"ࠧࡢࡴࡪࡷࠬั"), []):
        logger.warn(bstack11l1ll_opy_ (u"ࠣࡃࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࠡࡃࡸࡸࡴࡳࡡࡵ࡫ࡲࡲࠥࡽࡩ࡭࡮ࠣࡲࡴࡺࠠࡳࡷࡱࠤࡴࡴࠠ࡭ࡧࡪࡥࡨࡿࠠࡩࡧࡤࡨࡱ࡫ࡳࡴࠢࡰࡳࡩ࡫࠮ࠡࡕࡺ࡭ࡹࡩࡨࠡࡶࡲࠤࡳ࡫ࡷࠡࡪࡨࡥࡩࡲࡥࡴࡵࠣࡱࡴࡪࡥࠡࡱࡵࠤࡦࡼ࡯ࡪࡦࠣࡹࡸ࡯࡮ࡨࠢ࡫ࡩࡦࡪ࡬ࡦࡵࡶࠤࡲࡵࡤࡦ࠰ࠥา"))
        return False
    return True
  except Exception as error:
    logger.debug(bstack11l1ll_opy_ (u"ࠤࡈࡼࡨ࡫ࡰࡵ࡫ࡲࡲࠥ࡯࡮ࠡࡸࡤࡰ࡮ࡪࡡࡵࡧࠣࡥ࠶࠷ࡹࠡࡵࡸࡴࡵࡵࡲࡵࠢ࠽ࠦำ") + str(error))
    return False
def set_capabilities(caps, config):
  try:
    bstack1l11111l11_opy_ = config.get(bstack11l1ll_opy_ (u"ࠪࡥࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࡒࡴࡹ࡯࡯࡯ࡵࠪิ"), {})
    bstack1l11111l11_opy_[bstack11l1ll_opy_ (u"ࠫࡦࡻࡴࡩࡖࡲ࡯ࡪࡴࠧี")] = os.getenv(bstack11l1ll_opy_ (u"ࠬࡈࡓࡠࡃ࠴࠵࡞ࡥࡊࡘࡖࠪึ"))
    bstack1l1111111l_opy_ = json.loads(os.getenv(bstack11l1ll_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤ࡚ࡅࡔࡖࡢࡅࡈࡉࡅࡔࡕࡌࡆࡎࡒࡉࡕ࡛ࡢࡇࡔࡔࡆࡊࡉࡘࡖࡆ࡚ࡉࡐࡐࡢ࡝ࡒࡒࠧื"), bstack11l1ll_opy_ (u"ࠧࡼࡿุࠪ"))).get(bstack11l1ll_opy_ (u"ࠨࡵࡦࡥࡳࡴࡥࡳࡘࡨࡶࡸ࡯࡯࡯ูࠩ"))
    caps[bstack11l1ll_opy_ (u"ࠩࡤࡧࡨ࡫ࡳࡴ࡫ࡥ࡭ࡱ࡯ࡴࡺฺࠩ")] = True
    if bstack11l1ll_opy_ (u"ࠪࡦࡸࡺࡡࡤ࡭࠽ࡳࡵࡺࡩࡰࡰࡶࠫ฻") in caps:
      caps[bstack11l1ll_opy_ (u"ࠫࡧࡹࡴࡢࡥ࡮࠾ࡴࡶࡴࡪࡱࡱࡷࠬ฼")][bstack11l1ll_opy_ (u"ࠬࡧࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽࡔࡶࡴࡪࡱࡱࡷࠬ฽")] = bstack1l11111l11_opy_
      caps[bstack11l1ll_opy_ (u"࠭ࡢࡴࡶࡤࡧࡰࡀ࡯ࡱࡶ࡬ࡳࡳࡹࠧ฾")][bstack11l1ll_opy_ (u"ࠧࡢࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿࡏࡱࡶ࡬ࡳࡳࡹࠧ฿")][bstack11l1ll_opy_ (u"ࠨࡵࡦࡥࡳࡴࡥࡳࡘࡨࡶࡸ࡯࡯࡯ࠩเ")] = bstack1l1111111l_opy_
    else:
      caps[bstack11l1ll_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫࠯ࡣࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࡐࡲࡷ࡭ࡴࡴࡳࠨแ")] = bstack1l11111l11_opy_
      caps[bstack11l1ll_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬࠰ࡤࡧࡨ࡫ࡳࡴ࡫ࡥ࡭ࡱ࡯ࡴࡺࡑࡳࡸ࡮ࡵ࡮ࡴࠩโ")][bstack11l1ll_opy_ (u"ࠫࡸࡩࡡ࡯ࡰࡨࡶ࡛࡫ࡲࡴ࡫ࡲࡲࠬใ")] = bstack1l1111111l_opy_
  except Exception as error:
    logger.debug(bstack11l1ll_opy_ (u"ࠧࡋࡸࡤࡧࡳࡸ࡮ࡵ࡮ࠡࡹ࡫࡭ࡱ࡫ࠠࡴࡧࡷࡸ࡮ࡴࡧࠡࡃࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࠡࡃࡸࡸࡴࡳࡡࡵ࡫ࡲࡲࠥࡩࡡࡱࡣࡥ࡭ࡱ࡯ࡴࡪࡧࡶ࠲ࠥࡋࡲࡳࡱࡵ࠾ࠥࠨไ") +  str(error))
def bstack1l1l1lll1_opy_(driver, bstack11llllll1l_opy_):
  try:
    session = driver.session_id
    if session:
      bstack1l1111l1ll_opy_ = True
      current_url = driver.current_url
      try:
        url = urlparse(current_url)
      except Exception as e:
        bstack1l1111l1ll_opy_ = False
      bstack1l1111l1ll_opy_ = url.scheme in [bstack11l1ll_opy_ (u"ࠨࡨࡵࡶࡳࠦๅ"), bstack11l1ll_opy_ (u"ࠢࡩࡶࡷࡴࡸࠨๆ")]
      if bstack1l1111l1ll_opy_:
        if bstack11llllll1l_opy_:
          logger.info(bstack11l1ll_opy_ (u"ࠣࡕࡨࡸࡺࡶࠠࡧࡱࡵࠤࡆࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࠤࡹ࡫ࡳࡵ࡫ࡱ࡫ࠥ࡮ࡡࡴࠢࡶࡸࡦࡸࡴࡦࡦ࠱ࠤࡆࡻࡴࡰ࡯ࡤࡸࡪࠦࡴࡦࡵࡷࠤࡨࡧࡳࡦࠢࡨࡼࡪࡩࡵࡵ࡫ࡲࡲࠥࡽࡩ࡭࡮ࠣࡦࡪ࡭ࡩ࡯ࠢࡰࡳࡲ࡫࡮ࡵࡣࡵ࡭ࡱࡿ࠮ࠣ็"))
          driver.execute_async_script(bstack11l1ll_opy_ (u"ࠤࠥࠦࠏࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࡩ࡯࡯ࡵࡷࠤࡨࡧ࡬࡭ࡤࡤࡧࡰࠦ࠽ࠡࡣࡵ࡫ࡺࡳࡥ࡯ࡶࡶ࡟ࡦࡸࡧࡶ࡯ࡨࡲࡹࡹ࠮࡭ࡧࡱ࡫ࡹ࡮ࠠ࠮ࠢ࠴ࡡࡀࠐࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࡣࡰࡰࡶࡸࠥ࡬࡮ࠡ࠿ࠣࠬ࠮ࠦ࠽࠿ࠢࡾࠎࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࡹ࡬ࡲࡩࡵࡷ࠯ࡣࡧࡨࡊࡼࡥ࡯ࡶࡏ࡭ࡸࡺࡥ࡯ࡧࡵࠬࠬࡇ࠱࠲࡛ࡢࡘࡆࡖ࡟ࡔࡖࡄࡖ࡙ࡋࡄࠨ࠮ࠣࡪࡳ࠸ࠩ࠼ࠌࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࡣࡰࡰࡶࡸࠥ࡫ࠠ࠾ࠢࡱࡩࡼࠦࡃࡶࡵࡷࡳࡲࡋࡶࡦࡰࡷࠬࠬࡇ࠱࠲࡛ࡢࡊࡔࡘࡃࡆࡡࡖࡘࡆࡘࡔࠨࠫ࠾ࠎࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࡹ࡬ࡲࡩࡵࡷ࠯ࡦ࡬ࡷࡵࡧࡴࡤࡪࡈࡺࡪࡴࡴࠩࡧࠬ࠿ࠏࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࢃ࠻ࠋࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࡥࡲࡲࡸࡺࠠࡧࡰ࠵ࠤࡂࠦࠨࠪࠢࡀࡂࠥࢁࠊࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࡼ࡯࡮ࡥࡱࡺ࠲ࡷ࡫࡭ࡰࡸࡨࡉࡻ࡫࡮ࡵࡎ࡬ࡷࡹ࡫࡮ࡦࡴࠫࠫࡆ࠷࠱࡚ࡡࡗࡅࡕࡥࡓࡕࡃࡕࡘࡊࡊࠧ࠭ࠢࡩࡲ࠮ࡁࠊࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࡨࡧ࡬࡭ࡤࡤࡧࡰ࠮ࠩ࠼ࠌࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࢀࠎࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤ࡫ࡴࠨࠪ࠽ࠍࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠢࠣࠤ่"))
          logger.info(bstack11l1ll_opy_ (u"ࠥࡅࡺࡺ࡯࡮ࡣࡷࡩࠥࡺࡥࡴࡶࠣࡧࡦࡹࡥࠡࡧࡻࡩࡨࡻࡴࡪࡱࡱࠤ࡭ࡧࡳࠡࡵࡷࡥࡷࡺࡥࡥ࠰้ࠥ"))
        else:
          driver.execute_script(bstack11l1ll_opy_ (u"ࠦࠧࠨࠊࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࡤࡱࡱࡷࡹࠦࡥࠡ࠿ࠣࡲࡪࡽࠠࡄࡷࡶࡸࡴࡳࡅࡷࡧࡱࡸ࠭࠭ࡁ࠲࠳࡜ࡣࡋࡕࡒࡄࡇࡢࡗ࡙ࡕࡐࠨࠫ࠾ࠎࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࡼ࡯࡮ࡥࡱࡺ࠲ࡩ࡯ࡳࡱࡣࡷࡧ࡭ࡋࡶࡦࡰࡷࠬࡪ࠯࠻ࠋࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠧࠨ๊ࠢ"))
      return bstack11llllll1l_opy_
  except Exception as e:
    logger.error(bstack11l1ll_opy_ (u"ࠧࡋࡸࡤࡧࡳࡸ࡮ࡵ࡮ࠡ࡫ࡱࠤࡸࡺࡡࡳࡶ࡬ࡲ࡬ࠦࡡࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾࠦࡡࡶࡶࡲࡱࡦࡺࡩࡰࡰࠣࡷࡨࡧ࡮ࠡࡨࡲࡶࠥࡺࡨࡪࡵࠣࡸࡪࡹࡴࠡࡥࡤࡷࡪࡀ๋ࠠࠣ") + str(e))
    return False
def bstack1l1llll1l_opy_(driver, class_name, name, module_name, path, bstack1l1ll11ll1_opy_):
  try:
    bstack11lllll1l1_opy_ = [class_name] if not class_name is None else []
    bstack1l1111l111_opy_ = {
        bstack11l1ll_opy_ (u"ࠨࡳࡢࡸࡨࡖࡪࡹࡵ࡭ࡶࡶࠦ์"): True,
        bstack11l1ll_opy_ (u"ࠢࡵࡧࡶࡸࡉ࡫ࡴࡢ࡫࡯ࡷࠧํ"): {
            bstack11l1ll_opy_ (u"ࠣࡰࡤࡱࡪࠨ๎"): name,
            bstack11l1ll_opy_ (u"ࠤࡷࡩࡸࡺࡒࡶࡰࡌࡨࠧ๏"): os.environ.get(bstack11l1ll_opy_ (u"ࠪࡆࡘࡥࡁ࠲࠳࡜ࡣ࡙ࡋࡓࡕࡡࡕ࡙ࡓࡥࡉࡅࠩ๐")),
            bstack11l1ll_opy_ (u"ࠦ࡫࡯࡬ࡦࡒࡤࡸ࡭ࠨ๑"): str(path),
            bstack11l1ll_opy_ (u"ࠧࡹࡣࡰࡲࡨࡐ࡮ࡹࡴࠣ๒"): [module_name, *bstack11lllll1l1_opy_, name],
        },
        bstack11l1ll_opy_ (u"ࠨࡰ࡭ࡣࡷࡪࡴࡸ࡭ࠣ๓"): _11lllllll1_opy_(driver, bstack1l1ll11ll1_opy_)
    }
    driver.execute_script(bstack11l1ll_opy_ (u"ࠢࠣࠤࠍࠤࠥࠦࠠࠡࠢࠣࠤࡨࡵ࡮ࡴࡶࠣࡧࡦࡲ࡬ࡣࡣࡦ࡯ࠥࡃࠠࡢࡴࡪࡹࡲ࡫࡮ࡵࡵ࡞ࡥࡷ࡭ࡵ࡮ࡧࡱࡸࡸ࠴࡬ࡦࡰࡪࡸ࡭ࠦ࠭ࠡ࠳ࡠ࠿ࠏࠦࠠࠡࠢࠣࠤࠥࠦࡴࡩ࡫ࡶ࠲ࡷ࡫ࡳࠡ࠿ࠣࡲࡺࡲ࡬࠼ࠌࠣࠤࠥࠦࠠࠡࠢࠣ࡭࡫ࠦࠨࡢࡴࡪࡹࡲ࡫࡮ࡵࡵ࡞࠴ࡢ࠴ࡳࡢࡸࡨࡖࡪࡹࡵ࡭ࡶࡶ࠭ࠥࢁࠊࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࡽࡩ࡯ࡦࡲࡻ࠳ࡧࡤࡥࡇࡹࡩࡳࡺࡌࡪࡵࡷࡩࡳ࡫ࡲࠩࠩࡄ࠵࠶࡟࡟ࡕࡃࡓࡣ࡙ࡘࡁࡏࡕࡓࡓࡗ࡚ࡅࡓࠩ࠯ࠤ࠭࡫ࡶࡦࡰࡷ࠭ࠥࡃ࠾ࠡࡽࠍࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࡽࡩ࡯ࡦࡲࡻ࠳ࡺࡡࡱࡖࡵࡥࡳࡹࡰࡰࡴࡷࡩࡷࡊࡡࡵࡣࠣࡁࠥ࡫ࡶࡦࡰࡷ࠲ࡩ࡫ࡴࡢ࡫࡯࠿ࠏࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࡵࡪ࡬ࡷ࠳ࡸࡥࡴࠢࡀࠤࡼ࡯࡮ࡥࡱࡺ࠲ࡹࡧࡰࡕࡴࡤࡲࡸࡶ࡯ࡳࡶࡨࡶࡉࡧࡴࡢ࠽ࠍࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࡩࡡ࡭࡮ࡥࡥࡨࡱࠨࡵࡪ࡬ࡷ࠳ࡸࡥࡴࠫ࠾ࠎࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࢀ࠭ࡀࠐࠠࠡࠢࠣࠤࠥࠦࠠࡾࠌࠣࠤࠥࠦࠠࠡࠢࠣࡧࡴࡴࡳࡵࠢࡨࠤࡂࠦ࡮ࡦࡹࠣࡇࡺࡹࡴࡰ࡯ࡈࡺࡪࡴࡴࠩࠩࡄ࠵࠶࡟࡟ࡕࡇࡖࡘࡤࡋࡎࡅࠩ࠯ࠤࢀࠦࡤࡦࡶࡤ࡭ࡱࡀࠠࡢࡴࡪࡹࡲ࡫࡮ࡵࡵ࡞࠴ࡢࠦࡽࠪ࠽ࠍࠤࠥࠦࠠࠡࠢࠣࠤࡼ࡯࡮ࡥࡱࡺ࠲ࡩ࡯ࡳࡱࡣࡷࡧ࡭ࡋࡶࡦࡰࡷࠬࡪ࠯࠻ࠋࠢࠣࠤࠥࠦࠠࠡࠢ࡬ࡪࠥ࠮ࠡࡢࡴࡪࡹࡲ࡫࡮ࡵࡵ࡞࠴ࡢ࠴ࡳࡢࡸࡨࡖࡪࡹࡵ࡭ࡶࡶ࠭ࠥࢁࠊࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࡩࡡ࡭࡮ࡥࡥࡨࡱࠨࠪ࠽ࠍࠤࠥࠦࠠࠡࠢࠣࠤࢂࠐࠠࠡࠢࠣࠦࠧࠨ๔"), bstack1l1111l111_opy_)
    logger.info(bstack11l1ll_opy_ (u"ࠣࡃࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࠡࡶࡨࡷࡹ࡯࡮ࡨࠢࡩࡳࡷࠦࡴࡩ࡫ࡶࠤࡹ࡫ࡳࡵࠢࡦࡥࡸ࡫ࠠࡩࡣࡶࠤࡪࡴࡤࡦࡦ࠱ࠦ๕"))
  except Exception as bstack1l111l11l1_opy_:
    logger.error(bstack11l1ll_opy_ (u"ࠤࡄࡧࡨ࡫ࡳࡴ࡫ࡥ࡭ࡱ࡯ࡴࡺࠢࡵࡩࡸࡻ࡬ࡵࡵࠣࡧࡴࡻ࡬ࡥࠢࡱࡳࡹࠦࡢࡦࠢࡳࡶࡴࡩࡥࡴࡵࡨࡨࠥ࡬࡯ࡳࠢࡷ࡬ࡪࠦࡴࡦࡵࡷࠤࡨࡧࡳࡦ࠼ࠣࠦ๖") + str(path) + bstack11l1ll_opy_ (u"ࠥࠤࡊࡸࡲࡰࡴࠣ࠾ࠧ๗") + str(bstack1l111l11l1_opy_))