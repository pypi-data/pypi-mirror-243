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
import atexit
import os
import signal
import sys
import yaml
import requests
import logging
import threading
import socket
import datetime
import string
import random
import json
import collections.abc
import re
import multiprocessing
import traceback
import copy
import tempfile
from packaging import version
from browserstack.local import Local
from urllib.parse import urlparse
from bstack_utils.constants import *
from bstack_utils.percy import *
import time
import requests
def bstack1llll11l_opy_():
  global CONFIG
  headers = {
        bstack11l1l1l_opy_ (u"ࠪࡇࡴࡴࡴࡦࡰࡷ࠱ࡹࡿࡰࡦࠩࡶ"): bstack11l1l1l_opy_ (u"ࠫࡦࡶࡰ࡭࡫ࡦࡥࡹ࡯࡯࡯࠱࡭ࡷࡴࡴࠧࡷ"),
      }
  proxies = bstack1ll1l1l1l_opy_(CONFIG, bstack1lll11l111_opy_)
  try:
    response = requests.get(bstack1lll11l111_opy_, headers=headers, proxies=proxies, timeout=5)
    if response.json():
      bstack1ll1llll11_opy_ = response.json()[bstack11l1l1l_opy_ (u"ࠬ࡮ࡵࡣࡵࠪࡸ")]
      logger.debug(bstack1ll1l111_opy_.format(response.json()))
      return bstack1ll1llll11_opy_
    else:
      logger.debug(bstack11ll1llll_opy_.format(bstack11l1l1l_opy_ (u"ࠨࡒࡦࡵࡳࡳࡳࡹࡥࠡࡌࡖࡓࡓࠦࡰࡢࡴࡶࡩࠥ࡫ࡲࡳࡱࡵࠤࠧࡹ")))
  except Exception as e:
    logger.debug(bstack11ll1llll_opy_.format(e))
def bstack11l1lll1l_opy_(hub_url):
  global CONFIG
  url = bstack11l1l1l_opy_ (u"ࠢࡩࡶࡷࡴࡸࡀ࠯࠰ࠤࡺ")+  hub_url + bstack11l1l1l_opy_ (u"ࠣ࠱ࡦ࡬ࡪࡩ࡫ࠣࡻ")
  headers = {
        bstack11l1l1l_opy_ (u"ࠩࡆࡳࡳࡺࡥ࡯ࡶ࠰ࡸࡾࡶࡥࠨࡼ"): bstack11l1l1l_opy_ (u"ࠪࡥࡵࡶ࡬ࡪࡥࡤࡸ࡮ࡵ࡮࠰࡬ࡶࡳࡳ࠭ࡽ"),
      }
  proxies = bstack1ll1l1l1l_opy_(CONFIG, url)
  try:
    start_time = time.perf_counter()
    requests.get(url, headers=headers, proxies=proxies, timeout=5)
    latency = time.perf_counter() - start_time
    logger.debug(bstack1l1l11l11_opy_.format(hub_url, latency))
    return dict(hub_url=hub_url, latency=latency)
  except Exception as e:
    logger.debug(bstack11l1l1l1_opy_.format(hub_url, e))
def bstack1ll11l1l1_opy_():
  try:
    global bstack1l1ll1ll1l_opy_
    bstack1ll1llll11_opy_ = bstack1llll11l_opy_()
    bstack1lll11l11l_opy_ = []
    results = []
    for bstack111l111l_opy_ in bstack1ll1llll11_opy_:
      bstack1lll11l11l_opy_.append(bstack1ll11l1l1l_opy_(target=bstack11l1lll1l_opy_,args=(bstack111l111l_opy_,)))
    for t in bstack1lll11l11l_opy_:
      t.start()
    for t in bstack1lll11l11l_opy_:
      results.append(t.join())
    bstack1ll111111l_opy_ = {}
    for item in results:
      hub_url = item[bstack11l1l1l_opy_ (u"ࠫ࡭ࡻࡢࡠࡷࡵࡰࠬࡾ")]
      latency = item[bstack11l1l1l_opy_ (u"ࠬࡲࡡࡵࡧࡱࡧࡾ࠭ࡿ")]
      bstack1ll111111l_opy_[hub_url] = latency
    bstack1ll111ll11_opy_ = min(bstack1ll111111l_opy_, key= lambda x: bstack1ll111111l_opy_[x])
    bstack1l1ll1ll1l_opy_ = bstack1ll111ll11_opy_
    logger.debug(bstack1l11ll111_opy_.format(bstack1ll111ll11_opy_))
  except Exception as e:
    logger.debug(bstack1ll111ll1l_opy_.format(e))
from bstack_utils.messages import *
from bstack_utils.config import Config
from bstack_utils.helper import bstack1ll11l1111_opy_, bstack1llllll1l1_opy_, bstack1111l11l_opy_, bstack1ll11ll11_opy_, Notset, bstack1ll111l111_opy_, \
  bstack1lll111lll_opy_, bstack111l1llll_opy_, bstack1l1lll11l_opy_, bstack1lll1l1ll_opy_, bstack11ll1111_opy_, bstack11l111lll_opy_, bstack11llllll_opy_, \
  bstack1lll1ll1l_opy_, bstack11l11ll11_opy_, bstack1llll1111_opy_, bstack111l111l1_opy_, bstack1ll111111_opy_, bstack1llll1l1ll_opy_, \
  bstack1lll1ll111_opy_, bstack1111llll_opy_
from bstack_utils.bstack1lll11111l_opy_ import bstack11lll111l_opy_
from bstack_utils.bstack1l1ll111_opy_ import bstack1l11l11l_opy_
from bstack_utils.proxy import bstack1111l1l1l_opy_, bstack1ll1l1l1l_opy_, bstack1ll1111l_opy_, bstack1l11l111l_opy_
import bstack_utils.bstack11l1ll111_opy_ as bstack1111ll111_opy_
from browserstack_sdk.bstack1lll11lll_opy_ import *
from browserstack_sdk.bstack1lllll1l11_opy_ import *
from bstack_utils.bstack11l111ll_opy_ import bstack1lll11l1ll_opy_
bstack1llll1l1_opy_ = bstack11l1l1l_opy_ (u"࠭ࠠࠡ࠱࠭ࠤࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽ࠡࠬ࠲ࡠࡳࠦࠠࡪࡨࠫࡴࡦ࡭ࡥࠡ࠿ࡀࡁࠥࡼ࡯ࡪࡦࠣ࠴࠮ࠦࡻ࡝ࡰࠣࠤࠥࡺࡲࡺࡽ࡟ࡲࠥࡩ࡯࡯ࡵࡷࠤ࡫ࡹࠠ࠾ࠢࡵࡩࡶࡻࡩࡳࡧࠫࡠࠬ࡬ࡳ࡝ࠩࠬ࠿ࡡࡴࠠࠡࠢࠣࠤ࡫ࡹ࠮ࡢࡲࡳࡩࡳࡪࡆࡪ࡮ࡨࡗࡾࡴࡣࠩࡤࡶࡸࡦࡩ࡫ࡠࡲࡤࡸ࡭࠲ࠠࡋࡕࡒࡒ࠳ࡹࡴࡳ࡫ࡱ࡫࡮࡬ࡹࠩࡲࡢ࡭ࡳࡪࡥࡹࠫࠣ࠯ࠥࠨ࠺ࠣࠢ࠮ࠤࡏ࡙ࡏࡏ࠰ࡶࡸࡷ࡯࡮ࡨ࡫ࡩࡽ࠭ࡐࡓࡐࡐ࠱ࡴࡦࡸࡳࡦࠪࠫࡥࡼࡧࡩࡵࠢࡱࡩࡼࡖࡡࡨࡧ࠵࠲ࡪࡼࡡ࡭ࡷࡤࡸࡪ࠮ࠢࠩࠫࠣࡁࡃࠦࡻࡾࠤ࠯ࠤࡡ࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࡤ࡫ࡸࡦࡥࡸࡸࡴࡸ࠺ࠡࡽࠥࡥࡨࡺࡩࡰࡰࠥ࠾ࠥࠨࡧࡦࡶࡖࡩࡸࡹࡩࡰࡰࡇࡩࡹࡧࡩ࡭ࡵࠥࢁࡡ࠭ࠩࠪࠫ࡞ࠦ࡭ࡧࡳࡩࡧࡧࡣ࡮ࡪࠢ࡞ࠫࠣ࠯ࠥࠨࠬ࡝࡞ࡱࠦ࠮ࡢ࡮ࠡࠢࠣࠤࢂࡩࡡࡵࡥ࡫ࠬࡪࡾࠩࡼ࡞ࡱࠤࠥࠦࠠࡾ࡞ࡱࠤࠥࢃ࡜࡯ࠢࠣ࠳࠯ࠦ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࠣ࠮࠴࠭ࢀ")
bstack1llll1ll1l_opy_ = bstack11l1l1l_opy_ (u"ࠧ࡝ࡰ࠲࠮ࠥࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾ࠢ࠭࠳ࡡࡴࡣࡰࡰࡶࡸࠥࡨࡳࡵࡣࡦ࡯ࡤࡶࡡࡵࡪࠣࡁࠥࡶࡲࡰࡥࡨࡷࡸ࠴ࡡࡳࡩࡹ࡟ࡵࡸ࡯ࡤࡧࡶࡷ࠳ࡧࡲࡨࡸ࠱ࡰࡪࡴࡧࡵࡪࠣ࠱ࠥ࠹࡝࡝ࡰࡦࡳࡳࡹࡴࠡࡤࡶࡸࡦࡩ࡫ࡠࡥࡤࡴࡸࠦ࠽ࠡࡲࡵࡳࡨ࡫ࡳࡴ࠰ࡤࡶ࡬ࡼ࡛ࡱࡴࡲࡧࡪࡹࡳ࠯ࡣࡵ࡫ࡻ࠴࡬ࡦࡰࡪࡸ࡭ࠦ࠭ࠡ࠳ࡠࡠࡳࡩ࡯࡯ࡵࡷࠤࡵࡥࡩ࡯ࡦࡨࡼࠥࡃࠠࡱࡴࡲࡧࡪࡹࡳ࠯ࡣࡵ࡫ࡻࡡࡰࡳࡱࡦࡩࡸࡹ࠮ࡢࡴࡪࡺ࠳ࡲࡥ࡯ࡩࡷ࡬ࠥ࠳ࠠ࠳࡟࡟ࡲࡵࡸ࡯ࡤࡧࡶࡷ࠳ࡧࡲࡨࡸࠣࡁࠥࡶࡲࡰࡥࡨࡷࡸ࠴ࡡࡳࡩࡹ࠲ࡸࡲࡩࡤࡧࠫ࠴࠱ࠦࡰࡳࡱࡦࡩࡸࡹ࠮ࡢࡴࡪࡺ࠳ࡲࡥ࡯ࡩࡷ࡬ࠥ࠳ࠠ࠴ࠫ࡟ࡲࡨࡵ࡮ࡴࡶࠣ࡭ࡲࡶ࡯ࡳࡶࡢࡴࡱࡧࡹࡸࡴ࡬࡫࡭ࡺ࠴ࡠࡤࡶࡸࡦࡩ࡫ࠡ࠿ࠣࡶࡪࡷࡵࡪࡴࡨࠬࠧࡶ࡬ࡢࡻࡺࡶ࡮࡭ࡨࡵࠤࠬ࠿ࡡࡴࡩ࡮ࡲࡲࡶࡹࡥࡰ࡭ࡣࡼࡻࡷ࡯ࡧࡩࡶ࠷ࡣࡧࡹࡴࡢࡥ࡮࠲ࡨ࡮ࡲࡰ࡯࡬ࡹࡲ࠴࡬ࡢࡷࡱࡧ࡭ࠦ࠽ࠡࡣࡶࡽࡳࡩࠠࠩ࡮ࡤࡹࡳࡩࡨࡐࡲࡷ࡭ࡴࡴࡳࠪࠢࡀࡂࠥࢁ࡜࡯࡮ࡨࡸࠥࡩࡡࡱࡵ࠾ࡠࡳࡺࡲࡺࠢࡾࡠࡳࡩࡡࡱࡵࠣࡁࠥࡐࡓࡐࡐ࠱ࡴࡦࡸࡳࡦࠪࡥࡷࡹࡧࡣ࡬ࡡࡦࡥࡵࡹࠩ࡝ࡰࠣࠤࢂࠦࡣࡢࡶࡦ࡬࠭࡫ࡸࠪࠢࡾࡠࡳࠦࠠࠡࠢࢀࡠࡳࠦࠠࡳࡧࡷࡹࡷࡴࠠࡢࡹࡤ࡭ࡹࠦࡩ࡮ࡲࡲࡶࡹࡥࡰ࡭ࡣࡼࡻࡷ࡯ࡧࡩࡶ࠷ࡣࡧࡹࡴࡢࡥ࡮࠲ࡨ࡮ࡲࡰ࡯࡬ࡹࡲ࠴ࡣࡰࡰࡱࡩࡨࡺࠨࡼ࡞ࡱࠤࠥࠦࠠࡸࡵࡈࡲࡩࡶ࡯ࡪࡰࡷ࠾ࠥࡦࡷࡴࡵ࠽࠳࠴ࡩࡤࡱ࠰ࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫࠯ࡥࡲࡱ࠴ࡶ࡬ࡢࡻࡺࡶ࡮࡭ࡨࡵࡁࡦࡥࡵࡹ࠽ࠥࡽࡨࡲࡨࡵࡤࡦࡗࡕࡍࡈࡵ࡭ࡱࡱࡱࡩࡳࡺࠨࡋࡕࡒࡒ࠳ࡹࡴࡳ࡫ࡱ࡫࡮࡬ࡹࠩࡥࡤࡴࡸ࠯ࠩࡾࡢ࠯ࡠࡳࠦࠠࠡࠢ࠱࠲࠳ࡲࡡࡶࡰࡦ࡬ࡔࡶࡴࡪࡱࡱࡷࡡࡴࠠࠡࡿࠬࡠࡳࢃ࡜࡯࠱࠭ࠤࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽ࠡࠬ࠲ࡠࡳ࠭ࢁ")
from ._version import __version__
bstack1l1l11ll_opy_ = None
CONFIG = {}
bstack11lllll1_opy_ = {}
bstack111ll1ll1_opy_ = {}
bstack1l1ll1ll1_opy_ = None
bstack11ll11ll_opy_ = None
bstack1ll11l1ll1_opy_ = None
bstack1llll111l_opy_ = -1
bstack111lll1ll_opy_ = 0
bstack1ll1l11111_opy_ = bstack1llll1l11_opy_
bstack1ll1111l11_opy_ = 1
bstack1l1l1l1l1_opy_ = False
bstack1l1lll1l11_opy_ = False
bstack1lllll1ll1_opy_ = bstack11l1l1l_opy_ (u"ࠨࠩࢂ")
bstack11l111111_opy_ = bstack11l1l1l_opy_ (u"ࠩࠪࢃ")
bstack1lll1l111_opy_ = False
bstack11l1l1ll1_opy_ = True
bstack1l1llllll1_opy_ = bstack11l1l1l_opy_ (u"ࠪࠫࢄ")
bstack11111lll1_opy_ = []
bstack1l1ll1ll1l_opy_ = bstack11l1l1l_opy_ (u"ࠫࠬࢅ")
bstack1l1l1llll_opy_ = False
bstack11ll11ll1_opy_ = None
bstack1llll111l1_opy_ = None
bstack1lll111l_opy_ = -1
bstack1lll11l1_opy_ = os.path.join(os.path.expanduser(bstack11l1l1l_opy_ (u"ࠬࢄࠧࢆ")), bstack11l1l1l_opy_ (u"࠭࠮ࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠭ࢇ"), bstack11l1l1l_opy_ (u"ࠧ࠯ࡴࡲࡦࡴࡺ࠭ࡳࡧࡳࡳࡷࡺ࠭ࡩࡧ࡯ࡴࡪࡸ࠮࡫ࡵࡲࡲࠬ࢈"))
bstack1ll11ll111_opy_ = 0
bstack11ll1l1l1_opy_ = []
bstack1llll1l11l_opy_ = []
bstack111l11l1_opy_ = []
bstack11l11ll1_opy_ = []
bstack1lllllll1l_opy_ = bstack11l1l1l_opy_ (u"ࠨࠩࢉ")
bstack11l1l111_opy_ = bstack11l1l1l_opy_ (u"ࠩࠪࢊ")
bstack111ll11l_opy_ = False
bstack1l1l11lll_opy_ = False
bstack11l11l1l_opy_ = {}
bstack1l111l1l_opy_ = None
bstack1l1l1l1ll_opy_ = None
bstack1l11lll11_opy_ = None
bstack1l1l1l11l_opy_ = None
bstack1ll1ll111_opy_ = None
bstack1l11111ll_opy_ = None
bstack1ll111l1ll_opy_ = None
bstack1lll1lllll_opy_ = None
bstack1lll11ll1_opy_ = None
bstack1ll1lllll_opy_ = None
bstack11llll11_opy_ = None
bstack1l111lll1_opy_ = None
bstack1l11l1l11_opy_ = None
bstack1lll111l1_opy_ = None
bstack1l1l11l1l_opy_ = None
bstack11ll1l1ll_opy_ = None
bstack1ll111l11l_opy_ = None
bstack1l1111l1_opy_ = None
bstack1l111l1ll_opy_ = None
bstack1lll111l11_opy_ = bstack11l1l1l_opy_ (u"ࠥࠦࢋ")
logger = logging.getLogger(__name__)
logging.basicConfig(level=bstack1ll1l11111_opy_,
                    format=bstack11l1l1l_opy_ (u"ࠫࡡࡴࠥࠩࡣࡶࡧࡹ࡯࡭ࡦࠫࡶࠤࡠࠫࠨ࡯ࡣࡰࡩ࠮ࡹ࡝࡜ࠧࠫࡰࡪࡼࡥ࡭ࡰࡤࡱࡪ࠯ࡳ࡞ࠢ࠰ࠤࠪ࠮࡭ࡦࡵࡶࡥ࡬࡫ࠩࡴࠩࢌ"),
                    datefmt=bstack11l1l1l_opy_ (u"ࠬࠫࡈ࠻ࠧࡐ࠾࡙ࠪࠧࢍ"),
                    stream=sys.stdout)
bstack1lllll111l_opy_ = Config.get_instance()
percy = bstack1ll111l1l1_opy_()
def bstack1111ll1l1_opy_():
  global CONFIG
  global bstack1ll1l11111_opy_
  if bstack11l1l1l_opy_ (u"࠭࡬ࡰࡩࡏࡩࡻ࡫࡬ࠨࢎ") in CONFIG:
    bstack1ll1l11111_opy_ = bstack1l1lll1l_opy_[CONFIG[bstack11l1l1l_opy_ (u"ࠧ࡭ࡱࡪࡐࡪࡼࡥ࡭ࠩ࢏")]]
    logging.getLogger().setLevel(bstack1ll1l11111_opy_)
def bstack1l11l11ll_opy_():
  global CONFIG
  global bstack111ll11l_opy_
  bstack1ll1l11ll_opy_ = bstack11111l11_opy_(CONFIG)
  if (bstack11l1l1l_opy_ (u"ࠨࡵ࡮࡭ࡵ࡙ࡥࡴࡵ࡬ࡳࡳࡔࡡ࡮ࡧࠪ࢐") in bstack1ll1l11ll_opy_ and str(bstack1ll1l11ll_opy_[bstack11l1l1l_opy_ (u"ࠩࡶ࡯࡮ࡶࡓࡦࡵࡶ࡭ࡴࡴࡎࡢ࡯ࡨࠫ࢑")]).lower() == bstack11l1l1l_opy_ (u"ࠪࡸࡷࡻࡥࠨ࢒")):
    bstack111ll11l_opy_ = True
def bstack1l111ll1l_opy_():
  from appium.version import version as appium_version
  return version.parse(appium_version)
def bstack1llll1lll_opy_():
  from selenium import webdriver
  return version.parse(webdriver.__version__)
def bstack1llll11l1_opy_():
  args = sys.argv
  for i in range(len(args)):
    if bstack11l1l1l_opy_ (u"ࠦ࠲࠳ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࡨࡵ࡮ࡧ࡫ࡪࡪ࡮ࡲࡥࠣ࢓") == args[i].lower() or bstack11l1l1l_opy_ (u"ࠧ࠳࠭ࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠴ࡣࡰࡰࡩ࡭࡬ࠨ࢔") == args[i].lower():
      path = args[i + 1]
      sys.argv.remove(args[i])
      sys.argv.remove(path)
      global bstack1l1llllll1_opy_
      bstack1l1llllll1_opy_ += bstack11l1l1l_opy_ (u"࠭࠭࠮ࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱࡃࡰࡰࡩ࡭࡬ࡌࡩ࡭ࡧࠣࠫ࢕") + path
      return path
  return None
bstack11l1llll_opy_ = re.compile(bstack11l1l1l_opy_ (u"ࡲࠣ࠰࠭ࡃࡡࠪࡻࠩ࠰࠭ࡃ࠮ࢃ࠮ࠫࡁࠥ࢖"))
def bstack1ll11l1lll_opy_(loader, node):
  value = loader.construct_scalar(node)
  for group in bstack11l1llll_opy_.findall(value):
    if group is not None and os.environ.get(group) is not None:
      value = value.replace(bstack11l1l1l_opy_ (u"ࠣࠦࡾࠦࢗ") + group + bstack11l1l1l_opy_ (u"ࠤࢀࠦ࢘"), os.environ.get(group))
  return value
def bstack1ll1l11l_opy_():
  bstack1llll111ll_opy_ = bstack1llll11l1_opy_()
  if bstack1llll111ll_opy_ and os.path.exists(os.path.abspath(bstack1llll111ll_opy_)):
    fileName = bstack1llll111ll_opy_
  if bstack11l1l1l_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡆࡓࡓࡌࡉࡈࡡࡉࡍࡑࡋ࢙ࠧ") in os.environ and os.path.exists(
          os.path.abspath(os.environ[bstack11l1l1l_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡇࡔࡔࡆࡊࡉࡢࡊࡎࡒࡅࠨ࢚")])) and not bstack11l1l1l_opy_ (u"ࠬ࡬ࡩ࡭ࡧࡑࡥࡲ࡫࢛ࠧ") in locals():
    fileName = os.environ[bstack11l1l1l_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤࡉࡏࡏࡈࡌࡋࡤࡌࡉࡍࡇࠪ࢜")]
  if bstack11l1l1l_opy_ (u"ࠧࡧ࡫࡯ࡩࡓࡧ࡭ࡦࠩ࢝") in locals():
    bstack1ll1l1_opy_ = os.path.abspath(fileName)
  else:
    bstack1ll1l1_opy_ = bstack11l1l1l_opy_ (u"ࠨࠩ࢞")
  bstack11lllll1l_opy_ = os.getcwd()
  bstack1llllll1ll_opy_ = bstack11l1l1l_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫࠯ࡻࡰࡰࠬ࢟")
  bstack11l1l1lll_opy_ = bstack11l1l1l_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬࠰ࡼࡥࡲࡲࠧࢠ")
  while (not os.path.exists(bstack1ll1l1_opy_)) and bstack11lllll1l_opy_ != bstack11l1l1l_opy_ (u"ࠦࠧࢡ"):
    bstack1ll1l1_opy_ = os.path.join(bstack11lllll1l_opy_, bstack1llllll1ll_opy_)
    if not os.path.exists(bstack1ll1l1_opy_):
      bstack1ll1l1_opy_ = os.path.join(bstack11lllll1l_opy_, bstack11l1l1lll_opy_)
    if bstack11lllll1l_opy_ != os.path.dirname(bstack11lllll1l_opy_):
      bstack11lllll1l_opy_ = os.path.dirname(bstack11lllll1l_opy_)
    else:
      bstack11lllll1l_opy_ = bstack11l1l1l_opy_ (u"ࠧࠨࢢ")
  if not os.path.exists(bstack1ll1l1_opy_):
    bstack111l1l111_opy_(
      bstack111l1111l_opy_.format(os.getcwd()))
  try:
    with open(bstack1ll1l1_opy_, bstack11l1l1l_opy_ (u"࠭ࡲࠨࢣ")) as stream:
      yaml.add_implicit_resolver(bstack11l1l1l_opy_ (u"ࠢࠢࡲࡤࡸ࡭࡫ࡸࠣࢤ"), bstack11l1llll_opy_)
      yaml.add_constructor(bstack11l1l1l_opy_ (u"ࠣࠣࡳࡥࡹ࡮ࡥࡹࠤࢥ"), bstack1ll11l1lll_opy_)
      config = yaml.load(stream, yaml.FullLoader)
      return config
  except:
    with open(bstack1ll1l1_opy_, bstack11l1l1l_opy_ (u"ࠩࡵࠫࢦ")) as stream:
      try:
        config = yaml.safe_load(stream)
        return config
      except yaml.YAMLError as exc:
        bstack111l1l111_opy_(bstack111111111_opy_.format(str(exc)))
def bstack1lll1l11l_opy_(config):
  bstack1ll1lll1l_opy_ = bstack11l1111l_opy_(config)
  for option in list(bstack1ll1lll1l_opy_):
    if option.lower() in bstack1llll11111_opy_ and option != bstack1llll11111_opy_[option.lower()]:
      bstack1ll1lll1l_opy_[bstack1llll11111_opy_[option.lower()]] = bstack1ll1lll1l_opy_[option]
      del bstack1ll1lll1l_opy_[option]
  return config
def bstack1lll1ll1_opy_():
  global bstack111ll1ll1_opy_
  for key, bstack111ll1l11_opy_ in bstack11lll1111_opy_.items():
    if isinstance(bstack111ll1l11_opy_, list):
      for var in bstack111ll1l11_opy_:
        if var in os.environ and os.environ[var] and str(os.environ[var]).strip():
          bstack111ll1ll1_opy_[key] = os.environ[var]
          break
    elif bstack111ll1l11_opy_ in os.environ and os.environ[bstack111ll1l11_opy_] and str(os.environ[bstack111ll1l11_opy_]).strip():
      bstack111ll1ll1_opy_[key] = os.environ[bstack111ll1l11_opy_]
  if bstack11l1l1l_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡏࡓࡈࡇࡌࡠࡋࡇࡉࡓ࡚ࡉࡇࡋࡈࡖࠬࢧ") in os.environ:
    bstack111ll1ll1_opy_[bstack11l1l1l_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡘࡺࡡࡤ࡭ࡏࡳࡨࡧ࡬ࡐࡲࡷ࡭ࡴࡴࡳࠨࢨ")] = {}
    bstack111ll1ll1_opy_[bstack11l1l1l_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷ࡙ࡴࡢࡥ࡮ࡐࡴࡩࡡ࡭ࡑࡳࡸ࡮ࡵ࡮ࡴࠩࢩ")][bstack11l1l1l_opy_ (u"࠭࡬ࡰࡥࡤࡰࡎࡪࡥ࡯ࡶ࡬ࡪ࡮࡫ࡲࠨࢪ")] = os.environ[bstack11l1l1l_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡌࡐࡅࡄࡐࡤࡏࡄࡆࡐࡗࡍࡋࡏࡅࡓࠩࢫ")]
def bstack1ll111l1l_opy_():
  global bstack11lllll1_opy_
  global bstack1l1llllll1_opy_
  for idx, val in enumerate(sys.argv):
    if idx < len(sys.argv) and bstack11l1l1l_opy_ (u"ࠨ࠯࠰ࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬࠰࡯ࡳࡨࡧ࡬ࡊࡦࡨࡲࡹ࡯ࡦࡪࡧࡵࠫࢬ").lower() == val.lower():
      bstack11lllll1_opy_[bstack11l1l1l_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡖࡸࡦࡩ࡫ࡍࡱࡦࡥࡱࡕࡰࡵ࡫ࡲࡲࡸ࠭ࢭ")] = {}
      bstack11lllll1_opy_[bstack11l1l1l_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡗࡹࡧࡣ࡬ࡎࡲࡧࡦࡲࡏࡱࡶ࡬ࡳࡳࡹࠧࢮ")][bstack11l1l1l_opy_ (u"ࠫࡱࡵࡣࡢ࡮ࡌࡨࡪࡴࡴࡪࡨ࡬ࡩࡷ࠭ࢯ")] = sys.argv[idx + 1]
      del sys.argv[idx:idx + 2]
      break
  for key, bstack1lll11l1l1_opy_ in bstack1lll1lll1l_opy_.items():
    if isinstance(bstack1lll11l1l1_opy_, list):
      for idx, val in enumerate(sys.argv):
        for var in bstack1lll11l1l1_opy_:
          if idx < len(sys.argv) and bstack11l1l1l_opy_ (u"ࠬ࠳࠭ࠨࢰ") + var.lower() == val.lower() and not key in bstack11lllll1_opy_:
            bstack11lllll1_opy_[key] = sys.argv[idx + 1]
            bstack1l1llllll1_opy_ += bstack11l1l1l_opy_ (u"࠭ࠠ࠮࠯ࠪࢱ") + var + bstack11l1l1l_opy_ (u"ࠧࠡࠩࢲ") + sys.argv[idx + 1]
            del sys.argv[idx:idx + 2]
            break
    else:
      for idx, val in enumerate(sys.argv):
        if idx < len(sys.argv) and bstack11l1l1l_opy_ (u"ࠨ࠯࠰ࠫࢳ") + bstack1lll11l1l1_opy_.lower() == val.lower() and not key in bstack11lllll1_opy_:
          bstack11lllll1_opy_[key] = sys.argv[idx + 1]
          bstack1l1llllll1_opy_ += bstack11l1l1l_opy_ (u"ࠩࠣ࠱࠲࠭ࢴ") + bstack1lll11l1l1_opy_ + bstack11l1l1l_opy_ (u"ࠪࠤࠬࢵ") + sys.argv[idx + 1]
          del sys.argv[idx:idx + 2]
def bstack1l1ll1l1ll_opy_(config):
  bstack11lll1l1_opy_ = config.keys()
  for bstack11l11l1ll_opy_, bstack1ll1l1l11l_opy_ in bstack1ll1111l1l_opy_.items():
    if bstack1ll1l1l11l_opy_ in bstack11lll1l1_opy_:
      config[bstack11l11l1ll_opy_] = config[bstack1ll1l1l11l_opy_]
      del config[bstack1ll1l1l11l_opy_]
  for bstack11l11l1ll_opy_, bstack1ll1l1l11l_opy_ in bstack1ll1l11lll_opy_.items():
    if isinstance(bstack1ll1l1l11l_opy_, list):
      for bstack11l1l1l11_opy_ in bstack1ll1l1l11l_opy_:
        if bstack11l1l1l11_opy_ in bstack11lll1l1_opy_:
          config[bstack11l11l1ll_opy_] = config[bstack11l1l1l11_opy_]
          del config[bstack11l1l1l11_opy_]
          break
    elif bstack1ll1l1l11l_opy_ in bstack11lll1l1_opy_:
      config[bstack11l11l1ll_opy_] = config[bstack1ll1l1l11l_opy_]
      del config[bstack1ll1l1l11l_opy_]
  for bstack11l1l1l11_opy_ in list(config):
    for bstack1ll11111ll_opy_ in bstack1l1l1111_opy_:
      if bstack11l1l1l11_opy_.lower() == bstack1ll11111ll_opy_.lower() and bstack11l1l1l11_opy_ != bstack1ll11111ll_opy_:
        config[bstack1ll11111ll_opy_] = config[bstack11l1l1l11_opy_]
        del config[bstack11l1l1l11_opy_]
  bstack11lll11l_opy_ = []
  if bstack11l1l1l_opy_ (u"ࠫࡵࡲࡡࡵࡨࡲࡶࡲࡹࠧࢶ") in config:
    bstack11lll11l_opy_ = config[bstack11l1l1l_opy_ (u"ࠬࡶ࡬ࡢࡶࡩࡳࡷࡳࡳࠨࢷ")]
  for platform in bstack11lll11l_opy_:
    for bstack11l1l1l11_opy_ in list(platform):
      for bstack1ll11111ll_opy_ in bstack1l1l1111_opy_:
        if bstack11l1l1l11_opy_.lower() == bstack1ll11111ll_opy_.lower() and bstack11l1l1l11_opy_ != bstack1ll11111ll_opy_:
          platform[bstack1ll11111ll_opy_] = platform[bstack11l1l1l11_opy_]
          del platform[bstack11l1l1l11_opy_]
  for bstack11l11l1ll_opy_, bstack1ll1l1l11l_opy_ in bstack1ll1l11lll_opy_.items():
    for platform in bstack11lll11l_opy_:
      if isinstance(bstack1ll1l1l11l_opy_, list):
        for bstack11l1l1l11_opy_ in bstack1ll1l1l11l_opy_:
          if bstack11l1l1l11_opy_ in platform:
            platform[bstack11l11l1ll_opy_] = platform[bstack11l1l1l11_opy_]
            del platform[bstack11l1l1l11_opy_]
            break
      elif bstack1ll1l1l11l_opy_ in platform:
        platform[bstack11l11l1ll_opy_] = platform[bstack1ll1l1l11l_opy_]
        del platform[bstack1ll1l1l11l_opy_]
  for bstack1lll1111ll_opy_ in bstack11111l1l1_opy_:
    if bstack1lll1111ll_opy_ in config:
      if not bstack11111l1l1_opy_[bstack1lll1111ll_opy_] in config:
        config[bstack11111l1l1_opy_[bstack1lll1111ll_opy_]] = {}
      config[bstack11111l1l1_opy_[bstack1lll1111ll_opy_]].update(config[bstack1lll1111ll_opy_])
      del config[bstack1lll1111ll_opy_]
  for platform in bstack11lll11l_opy_:
    for bstack1lll1111ll_opy_ in bstack11111l1l1_opy_:
      if bstack1lll1111ll_opy_ in list(platform):
        if not bstack11111l1l1_opy_[bstack1lll1111ll_opy_] in platform:
          platform[bstack11111l1l1_opy_[bstack1lll1111ll_opy_]] = {}
        platform[bstack11111l1l1_opy_[bstack1lll1111ll_opy_]].update(platform[bstack1lll1111ll_opy_])
        del platform[bstack1lll1111ll_opy_]
  config = bstack1lll1l11l_opy_(config)
  return config
def bstack1l1ll1lll_opy_(config):
  global bstack11l111111_opy_
  if bstack11l1l1l_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࡑࡵࡣࡢ࡮ࠪࢸ") in config and str(config[bstack11l1l1l_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰࡒ࡯ࡤࡣ࡯ࠫࢹ")]).lower() != bstack11l1l1l_opy_ (u"ࠨࡨࡤࡰࡸ࡫ࠧࢺ"):
    if not bstack11l1l1l_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡖࡸࡦࡩ࡫ࡍࡱࡦࡥࡱࡕࡰࡵ࡫ࡲࡲࡸ࠭ࢻ") in config:
      config[bstack11l1l1l_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡗࡹࡧࡣ࡬ࡎࡲࡧࡦࡲࡏࡱࡶ࡬ࡳࡳࡹࠧࢼ")] = {}
    if not bstack11l1l1l_opy_ (u"ࠫࡱࡵࡣࡢ࡮ࡌࡨࡪࡴࡴࡪࡨ࡬ࡩࡷ࠭ࢽ") in config[bstack11l1l1l_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷ࡙ࡴࡢࡥ࡮ࡐࡴࡩࡡ࡭ࡑࡳࡸ࡮ࡵ࡮ࡴࠩࢾ")]:
      bstack1llllll11l_opy_ = datetime.datetime.now()
      bstack1l11ll1l_opy_ = bstack1llllll11l_opy_.strftime(bstack11l1l1l_opy_ (u"࠭ࠥࡥࡡࠨࡦࡤࠫࡈࠦࡏࠪࢿ"))
      hostname = socket.gethostname()
      bstack1llll11l1l_opy_ = bstack11l1l1l_opy_ (u"ࠧࠨࣀ").join(random.choices(string.ascii_lowercase + string.digits, k=4))
      identifier = bstack11l1l1l_opy_ (u"ࠨࡽࢀࡣࢀࢃ࡟ࡼࡿࠪࣁ").format(bstack1l11ll1l_opy_, hostname, bstack1llll11l1l_opy_)
      config[bstack11l1l1l_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡖࡸࡦࡩ࡫ࡍࡱࡦࡥࡱࡕࡰࡵ࡫ࡲࡲࡸ࠭ࣂ")][bstack11l1l1l_opy_ (u"ࠪࡰࡴࡩࡡ࡭ࡋࡧࡩࡳࡺࡩࡧ࡫ࡨࡶࠬࣃ")] = identifier
    bstack11l111111_opy_ = config[bstack11l1l1l_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡘࡺࡡࡤ࡭ࡏࡳࡨࡧ࡬ࡐࡲࡷ࡭ࡴࡴࡳࠨࣄ")][bstack11l1l1l_opy_ (u"ࠬࡲ࡯ࡤࡣ࡯ࡍࡩ࡫࡮ࡵ࡫ࡩ࡭ࡪࡸࠧࣅ")]
  return config
def bstack111l1l1l1_opy_():
  bstack1l11ll1l1_opy_ =  bstack1lll1l1ll_opy_()[bstack11l1l1l_opy_ (u"࠭ࡢࡶ࡫࡯ࡨࡤࡴࡵ࡮ࡤࡨࡶࠬࣆ")]
  return bstack1l11ll1l1_opy_ if bstack1l11ll1l1_opy_ else -1
def bstack11111lll_opy_(bstack1l11ll1l1_opy_):
  global CONFIG
  if not bstack11l1l1l_opy_ (u"ࠧࠥࡽࡅ࡙ࡎࡒࡄࡠࡐࡘࡑࡇࡋࡒࡾࠩࣇ") in CONFIG[bstack11l1l1l_opy_ (u"ࠨࡤࡸ࡭ࡱࡪࡉࡥࡧࡱࡸ࡮࡬ࡩࡦࡴࠪࣈ")]:
    return
  CONFIG[bstack11l1l1l_opy_ (u"ࠩࡥࡹ࡮ࡲࡤࡊࡦࡨࡲࡹ࡯ࡦࡪࡧࡵࠫࣉ")] = CONFIG[bstack11l1l1l_opy_ (u"ࠪࡦࡺ࡯࡬ࡥࡋࡧࡩࡳࡺࡩࡧ࡫ࡨࡶࠬ࣊")].replace(
    bstack11l1l1l_opy_ (u"ࠫࠩࢁࡂࡖࡋࡏࡈࡤࡔࡕࡎࡄࡈࡖࢂ࠭࣋"),
    str(bstack1l11ll1l1_opy_)
  )
def bstack1lllll11l1_opy_():
  global CONFIG
  if not bstack11l1l1l_opy_ (u"ࠬࠪࡻࡅࡃࡗࡉࡤ࡚ࡉࡎࡇࢀࠫ࣌") in CONFIG[bstack11l1l1l_opy_ (u"࠭ࡢࡶ࡫࡯ࡨࡎࡪࡥ࡯ࡶ࡬ࡪ࡮࡫ࡲࠨ࣍")]:
    return
  bstack1llllll11l_opy_ = datetime.datetime.now()
  bstack1l11ll1l_opy_ = bstack1llllll11l_opy_.strftime(bstack11l1l1l_opy_ (u"ࠧࠦࡦ࠰ࠩࡧ࠳ࠥࡉ࠼ࠨࡑࠬ࣎"))
  CONFIG[bstack11l1l1l_opy_ (u"ࠨࡤࡸ࡭ࡱࡪࡉࡥࡧࡱࡸ࡮࡬ࡩࡦࡴ࣏ࠪ")] = CONFIG[bstack11l1l1l_opy_ (u"ࠩࡥࡹ࡮ࡲࡤࡊࡦࡨࡲࡹ࡯ࡦࡪࡧࡵ࣐ࠫ")].replace(
    bstack11l1l1l_opy_ (u"ࠪࠨࢀࡊࡁࡕࡇࡢࡘࡎࡓࡅࡾ࣑ࠩ"),
    bstack1l11ll1l_opy_
  )
def bstack1llllll111_opy_():
  global CONFIG
  if bstack11l1l1l_opy_ (u"ࠫࡧࡻࡩ࡭ࡦࡌࡨࡪࡴࡴࡪࡨ࡬ࡩࡷ࣒࠭") in CONFIG and not bool(CONFIG[bstack11l1l1l_opy_ (u"ࠬࡨࡵࡪ࡮ࡧࡍࡩ࡫࡮ࡵ࡫ࡩ࡭ࡪࡸ࣓ࠧ")]):
    del CONFIG[bstack11l1l1l_opy_ (u"࠭ࡢࡶ࡫࡯ࡨࡎࡪࡥ࡯ࡶ࡬ࡪ࡮࡫ࡲࠨࣔ")]
    return
  if not bstack11l1l1l_opy_ (u"ࠧࡣࡷ࡬ࡰࡩࡏࡤࡦࡰࡷ࡭࡫࡯ࡥࡳࠩࣕ") in CONFIG:
    CONFIG[bstack11l1l1l_opy_ (u"ࠨࡤࡸ࡭ࡱࡪࡉࡥࡧࡱࡸ࡮࡬ࡩࡦࡴࠪࣖ")] = bstack11l1l1l_opy_ (u"ࠩࠦࠨࢀࡈࡕࡊࡎࡇࡣࡓ࡛ࡍࡃࡇࡕࢁࠬࣗ")
  if bstack11l1l1l_opy_ (u"ࠪࠨࢀࡊࡁࡕࡇࡢࡘࡎࡓࡅࡾࠩࣘ") in CONFIG[bstack11l1l1l_opy_ (u"ࠫࡧࡻࡩ࡭ࡦࡌࡨࡪࡴࡴࡪࡨ࡬ࡩࡷ࠭ࣙ")]:
    bstack1lllll11l1_opy_()
    os.environ[bstack11l1l1l_opy_ (u"ࠬࡈࡓࡕࡃࡆࡏࡤࡉࡏࡎࡄࡌࡒࡊࡊ࡟ࡃࡗࡌࡐࡉࡥࡉࡅࠩࣚ")] = CONFIG[bstack11l1l1l_opy_ (u"࠭ࡢࡶ࡫࡯ࡨࡎࡪࡥ࡯ࡶ࡬ࡪ࡮࡫ࡲࠨࣛ")]
  if not bstack11l1l1l_opy_ (u"ࠧࠥࡽࡅ࡙ࡎࡒࡄࡠࡐࡘࡑࡇࡋࡒࡾࠩࣜ") in CONFIG[bstack11l1l1l_opy_ (u"ࠨࡤࡸ࡭ࡱࡪࡉࡥࡧࡱࡸ࡮࡬ࡩࡦࡴࠪࣝ")]:
    return
  bstack1l11ll1l1_opy_ = bstack11l1l1l_opy_ (u"ࠩࠪࣞ")
  bstack1l1lllll1_opy_ = bstack111l1l1l1_opy_()
  if bstack1l1lllll1_opy_ != -1:
    bstack1l11ll1l1_opy_ = bstack11l1l1l_opy_ (u"ࠪࡇࡎࠦࠧࣟ") + str(bstack1l1lllll1_opy_)
  if bstack1l11ll1l1_opy_ == bstack11l1l1l_opy_ (u"ࠫࠬ࣠"):
    bstack1lll1l1l1l_opy_ = bstack1ll1ll111l_opy_(CONFIG[bstack11l1l1l_opy_ (u"ࠬࡨࡵࡪ࡮ࡧࡒࡦࡳࡥࠨ࣡")])
    if bstack1lll1l1l1l_opy_ != -1:
      bstack1l11ll1l1_opy_ = str(bstack1lll1l1l1l_opy_)
  if bstack1l11ll1l1_opy_:
    bstack11111lll_opy_(bstack1l11ll1l1_opy_)
    os.environ[bstack11l1l1l_opy_ (u"࠭ࡂࡔࡖࡄࡇࡐࡥࡃࡐࡏࡅࡍࡓࡋࡄࡠࡄࡘࡍࡑࡊ࡟ࡊࡆࠪ࣢")] = CONFIG[bstack11l1l1l_opy_ (u"ࠧࡣࡷ࡬ࡰࡩࡏࡤࡦࡰࡷ࡭࡫࡯ࡥࡳࣣࠩ")]
def bstack11l1lllll_opy_(bstack1ll1ll1111_opy_, bstack111ll1l1_opy_, path):
  bstack11l1ll1l1_opy_ = {
    bstack11l1l1l_opy_ (u"ࠨ࡫ࡧࡩࡳࡺࡩࡧ࡫ࡨࡶࠬࣤ"): bstack111ll1l1_opy_
  }
  if os.path.exists(path):
    bstack1ll1llll1l_opy_ = json.load(open(path, bstack11l1l1l_opy_ (u"ࠩࡵࡦࠬࣥ")))
  else:
    bstack1ll1llll1l_opy_ = {}
  bstack1ll1llll1l_opy_[bstack1ll1ll1111_opy_] = bstack11l1ll1l1_opy_
  with open(path, bstack11l1l1l_opy_ (u"ࠥࡻ࠰ࠨࣦ")) as outfile:
    json.dump(bstack1ll1llll1l_opy_, outfile)
def bstack1ll1ll111l_opy_(bstack1ll1ll1111_opy_):
  bstack1ll1ll1111_opy_ = str(bstack1ll1ll1111_opy_)
  bstack1ll1l1lll1_opy_ = os.path.join(os.path.expanduser(bstack11l1l1l_opy_ (u"ࠫࢃ࠭ࣧ")), bstack11l1l1l_opy_ (u"ࠬ࠴ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࠬࣨ"))
  try:
    if not os.path.exists(bstack1ll1l1lll1_opy_):
      os.makedirs(bstack1ll1l1lll1_opy_)
    file_path = os.path.join(os.path.expanduser(bstack11l1l1l_opy_ (u"࠭ࡾࠨࣩ")), bstack11l1l1l_opy_ (u"ࠧ࠯ࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱࠧ࣪"), bstack11l1l1l_opy_ (u"ࠨ࠰ࡥࡹ࡮ࡲࡤ࠮ࡰࡤࡱࡪ࠳ࡣࡢࡥ࡫ࡩ࠳ࡰࡳࡰࡰࠪ࣫"))
    if not os.path.isfile(file_path):
      with open(file_path, bstack11l1l1l_opy_ (u"ࠩࡺࠫ࣬")):
        pass
      with open(file_path, bstack11l1l1l_opy_ (u"ࠥࡻ࠰ࠨ࣭")) as outfile:
        json.dump({}, outfile)
    with open(file_path, bstack11l1l1l_opy_ (u"ࠫࡷ࣮࠭")) as bstack1ll1l1lll_opy_:
      bstack1l11ll1ll_opy_ = json.load(bstack1ll1l1lll_opy_)
    if bstack1ll1ll1111_opy_ in bstack1l11ll1ll_opy_:
      bstack1llll1ll_opy_ = bstack1l11ll1ll_opy_[bstack1ll1ll1111_opy_][bstack11l1l1l_opy_ (u"ࠬ࡯ࡤࡦࡰࡷ࡭࡫࡯ࡥࡳ࣯ࠩ")]
      bstack1ll1lll11l_opy_ = int(bstack1llll1ll_opy_) + 1
      bstack11l1lllll_opy_(bstack1ll1ll1111_opy_, bstack1ll1lll11l_opy_, file_path)
      return bstack1ll1lll11l_opy_
    else:
      bstack11l1lllll_opy_(bstack1ll1ll1111_opy_, 1, file_path)
      return 1
  except Exception as e:
    logger.warn(bstack1l1lll11l1_opy_.format(str(e)))
    return -1
def bstack1l11l1lll_opy_(config):
  if not config[bstack11l1l1l_opy_ (u"࠭ࡵࡴࡧࡵࡒࡦࡳࡥࠨࣰ")] or not config[bstack11l1l1l_opy_ (u"ࠧࡢࡥࡦࡩࡸࡹࡋࡦࡻࣱࠪ")]:
    return True
  else:
    return False
def bstack1ll1ll1ll_opy_(config, index=0):
  global bstack1lll1l111_opy_
  bstack11111ll1_opy_ = {}
  caps = bstack1l1l1l11_opy_ + bstack1ll1ll1ll1_opy_
  if bstack1lll1l111_opy_:
    caps += bstack1ll11l111l_opy_
  for key in config:
    if key in caps + [bstack11l1l1l_opy_ (u"ࠨࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࡶࣲࠫ")]:
      continue
    bstack11111ll1_opy_[key] = config[key]
  if bstack11l1l1l_opy_ (u"ࠩࡳࡰࡦࡺࡦࡰࡴࡰࡷࠬࣳ") in config:
    for bstack1l1111ll_opy_ in config[bstack11l1l1l_opy_ (u"ࠪࡴࡱࡧࡴࡧࡱࡵࡱࡸ࠭ࣴ")][index]:
      if bstack1l1111ll_opy_ in caps + [bstack11l1l1l_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡓࡧ࡭ࡦࠩࣵ"), bstack11l1l1l_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷ࡜ࡥࡳࡵ࡬ࡳࡳࣶ࠭")]:
        continue
      bstack11111ll1_opy_[bstack1l1111ll_opy_] = config[bstack11l1l1l_opy_ (u"࠭ࡰ࡭ࡣࡷࡪࡴࡸ࡭ࡴࠩࣷ")][index][bstack1l1111ll_opy_]
  bstack11111ll1_opy_[bstack11l1l1l_opy_ (u"ࠧࡩࡱࡶࡸࡓࡧ࡭ࡦࠩࣸ")] = socket.gethostname()
  if bstack11l1l1l_opy_ (u"ࠨࡸࡨࡶࡸ࡯࡯࡯ࣹࠩ") in bstack11111ll1_opy_:
    del (bstack11111ll1_opy_[bstack11l1l1l_opy_ (u"ࠩࡹࡩࡷࡹࡩࡰࡰࣺࠪ")])
  return bstack11111ll1_opy_
def bstack1l1l1lll_opy_(config):
  global bstack1lll1l111_opy_
  bstack11l11lll_opy_ = {}
  caps = bstack1ll1ll1ll1_opy_
  if bstack1lll1l111_opy_:
    caps += bstack1ll11l111l_opy_
  for key in caps:
    if key in config:
      bstack11l11lll_opy_[key] = config[key]
  return bstack11l11lll_opy_
def bstack1l1lll11_opy_(bstack11111ll1_opy_, bstack11l11lll_opy_):
  bstack1lll1ll11_opy_ = {}
  for key in bstack11111ll1_opy_.keys():
    if key in bstack1ll1111l1l_opy_:
      bstack1lll1ll11_opy_[bstack1ll1111l1l_opy_[key]] = bstack11111ll1_opy_[key]
    else:
      bstack1lll1ll11_opy_[key] = bstack11111ll1_opy_[key]
  for key in bstack11l11lll_opy_:
    if key in bstack1ll1111l1l_opy_:
      bstack1lll1ll11_opy_[bstack1ll1111l1l_opy_[key]] = bstack11l11lll_opy_[key]
    else:
      bstack1lll1ll11_opy_[key] = bstack11l11lll_opy_[key]
  return bstack1lll1ll11_opy_
def bstack1l1ll1llll_opy_(config, index=0):
  global bstack1lll1l111_opy_
  config = copy.deepcopy(config)
  caps = {}
  bstack11l11lll_opy_ = bstack1l1l1lll_opy_(config)
  bstack1l1111111_opy_ = bstack1ll1ll1ll1_opy_
  bstack1l1111111_opy_ += bstack1l1l1ll1_opy_
  if bstack1lll1l111_opy_:
    bstack1l1111111_opy_ += bstack1ll11l111l_opy_
  if bstack11l1l1l_opy_ (u"ࠪࡴࡱࡧࡴࡧࡱࡵࡱࡸ࠭ࣻ") in config:
    if bstack11l1l1l_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡓࡧ࡭ࡦࠩࣼ") in config[bstack11l1l1l_opy_ (u"ࠬࡶ࡬ࡢࡶࡩࡳࡷࡳࡳࠨࣽ")][index]:
      caps[bstack11l1l1l_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡎࡢ࡯ࡨࠫࣾ")] = config[bstack11l1l1l_opy_ (u"ࠧࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࡵࠪࣿ")][index][bstack11l1l1l_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡐࡤࡱࡪ࠭ऀ")]
    if bstack11l1l1l_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴ࡙ࡩࡷࡹࡩࡰࡰࠪँ") in config[bstack11l1l1l_opy_ (u"ࠪࡴࡱࡧࡴࡧࡱࡵࡱࡸ࠭ं")][index]:
      caps[bstack11l1l1l_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶ࡛࡫ࡲࡴ࡫ࡲࡲࠬः")] = str(config[bstack11l1l1l_opy_ (u"ࠬࡶ࡬ࡢࡶࡩࡳࡷࡳࡳࠨऄ")][index][bstack11l1l1l_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡖࡦࡴࡶ࡭ࡴࡴࠧअ")])
    bstack111llll1_opy_ = {}
    for bstack111l1lll_opy_ in bstack1l1111111_opy_:
      if bstack111l1lll_opy_ in config[bstack11l1l1l_opy_ (u"ࠧࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࡵࠪआ")][index]:
        if bstack111l1lll_opy_ == bstack11l1l1l_opy_ (u"ࠨࡲ࡯ࡥࡹ࡬࡯ࡳ࡯࡙ࡩࡷࡹࡩࡰࡰࠪइ"):
          try:
            bstack111llll1_opy_[bstack111l1lll_opy_] = str(config[bstack11l1l1l_opy_ (u"ࠩࡳࡰࡦࡺࡦࡰࡴࡰࡷࠬई")][index][bstack111l1lll_opy_] * 1.0)
          except:
            bstack111llll1_opy_[bstack111l1lll_opy_] = str(config[bstack11l1l1l_opy_ (u"ࠪࡴࡱࡧࡴࡧࡱࡵࡱࡸ࠭उ")][index][bstack111l1lll_opy_])
        else:
          bstack111llll1_opy_[bstack111l1lll_opy_] = config[bstack11l1l1l_opy_ (u"ࠫࡵࡲࡡࡵࡨࡲࡶࡲࡹࠧऊ")][index][bstack111l1lll_opy_]
        del (config[bstack11l1l1l_opy_ (u"ࠬࡶ࡬ࡢࡶࡩࡳࡷࡳࡳࠨऋ")][index][bstack111l1lll_opy_])
    bstack11l11lll_opy_ = update(bstack11l11lll_opy_, bstack111llll1_opy_)
  bstack11111ll1_opy_ = bstack1ll1ll1ll_opy_(config, index)
  for bstack11l1l1l11_opy_ in bstack1ll1ll1ll1_opy_ + [bstack11l1l1l_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡎࡢ࡯ࡨࠫऌ"), bstack11l1l1l_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡗࡧࡵࡷ࡮ࡵ࡮ࠨऍ")]:
    if bstack11l1l1l11_opy_ in bstack11111ll1_opy_:
      bstack11l11lll_opy_[bstack11l1l1l11_opy_] = bstack11111ll1_opy_[bstack11l1l1l11_opy_]
      del (bstack11111ll1_opy_[bstack11l1l1l11_opy_])
  if bstack1ll111l111_opy_(config):
    bstack11111ll1_opy_[bstack11l1l1l_opy_ (u"ࠨࡷࡶࡩ࡜࠹ࡃࠨऎ")] = True
    caps.update(bstack11l11lll_opy_)
    caps[bstack11l1l1l_opy_ (u"ࠩࡥࡷࡹࡧࡣ࡬࠼ࡲࡴࡹ࡯࡯࡯ࡵࠪए")] = bstack11111ll1_opy_
  else:
    bstack11111ll1_opy_[bstack11l1l1l_opy_ (u"ࠪࡹࡸ࡫ࡗ࠴ࡅࠪऐ")] = False
    caps.update(bstack1l1lll11_opy_(bstack11111ll1_opy_, bstack11l11lll_opy_))
    if bstack11l1l1l_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡓࡧ࡭ࡦࠩऑ") in caps:
      caps[bstack11l1l1l_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷ࠭ऒ")] = caps[bstack11l1l1l_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡎࡢ࡯ࡨࠫओ")]
      del (caps[bstack11l1l1l_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡏࡣࡰࡩࠬऔ")])
    if bstack11l1l1l_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡘࡨࡶࡸ࡯࡯࡯ࠩक") in caps:
      caps[bstack11l1l1l_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡢࡺࡪࡸࡳࡪࡱࡱࠫख")] = caps[bstack11l1l1l_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵ࡚ࡪࡸࡳࡪࡱࡱࠫग")]
      del (caps[bstack11l1l1l_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶ࡛࡫ࡲࡴ࡫ࡲࡲࠬघ")])
  return caps
def bstack1llllllll_opy_():
  global bstack1l1ll1ll1l_opy_
  if bstack1llll1lll_opy_() <= version.parse(bstack11l1l1l_opy_ (u"ࠬ࠹࠮࠲࠵࠱࠴ࠬङ")):
    if bstack1l1ll1ll1l_opy_ != bstack11l1l1l_opy_ (u"࠭ࠧच"):
      return bstack11l1l1l_opy_ (u"ࠢࡩࡶࡷࡴ࠿࠵࠯ࠣछ") + bstack1l1ll1ll1l_opy_ + bstack11l1l1l_opy_ (u"ࠣ࠼࠻࠴࠴ࡽࡤ࠰ࡪࡸࡦࠧज")
    return bstack1111111ll_opy_
  if bstack1l1ll1ll1l_opy_ != bstack11l1l1l_opy_ (u"ࠩࠪझ"):
    return bstack11l1l1l_opy_ (u"ࠥ࡬ࡹࡺࡰࡴ࠼࠲࠳ࠧञ") + bstack1l1ll1ll1l_opy_ + bstack11l1l1l_opy_ (u"ࠦ࠴ࡽࡤ࠰ࡪࡸࡦࠧट")
  return bstack1111lll1l_opy_
def bstack1111l1111_opy_(options):
  return hasattr(options, bstack11l1l1l_opy_ (u"ࠬࡹࡥࡵࡡࡦࡥࡵࡧࡢࡪ࡮࡬ࡸࡾ࠭ठ"))
def update(d, u):
  for k, v in u.items():
    if isinstance(v, collections.abc.Mapping):
      d[k] = update(d.get(k, {}), v)
    else:
      if isinstance(v, list):
        d[k] = d.get(k, []) + v
      else:
        d[k] = v
  return d
def bstack11ll1l11l_opy_(options, bstack1l1l1lll1_opy_):
  for bstack1l1lllll1l_opy_ in bstack1l1l1lll1_opy_:
    if bstack1l1lllll1l_opy_ in [bstack11l1l1l_opy_ (u"࠭ࡡࡳࡩࡶࠫड"), bstack11l1l1l_opy_ (u"ࠧࡦࡺࡷࡩࡳࡹࡩࡰࡰࡶࠫढ")]:
      continue
    if bstack1l1lllll1l_opy_ in options._experimental_options:
      options._experimental_options[bstack1l1lllll1l_opy_] = update(options._experimental_options[bstack1l1lllll1l_opy_],
                                                         bstack1l1l1lll1_opy_[bstack1l1lllll1l_opy_])
    else:
      options.add_experimental_option(bstack1l1lllll1l_opy_, bstack1l1l1lll1_opy_[bstack1l1lllll1l_opy_])
  if bstack11l1l1l_opy_ (u"ࠨࡣࡵ࡫ࡸ࠭ण") in bstack1l1l1lll1_opy_:
    for arg in bstack1l1l1lll1_opy_[bstack11l1l1l_opy_ (u"ࠩࡤࡶ࡬ࡹࠧत")]:
      options.add_argument(arg)
    del (bstack1l1l1lll1_opy_[bstack11l1l1l_opy_ (u"ࠪࡥࡷ࡭ࡳࠨथ")])
  if bstack11l1l1l_opy_ (u"ࠫࡪࡾࡴࡦࡰࡶ࡭ࡴࡴࡳࠨद") in bstack1l1l1lll1_opy_:
    for ext in bstack1l1l1lll1_opy_[bstack11l1l1l_opy_ (u"ࠬ࡫ࡸࡵࡧࡱࡷ࡮ࡵ࡮ࡴࠩध")]:
      options.add_extension(ext)
    del (bstack1l1l1lll1_opy_[bstack11l1l1l_opy_ (u"࠭ࡥࡹࡶࡨࡲࡸ࡯࡯࡯ࡵࠪन")])
def bstack11111ll11_opy_(options, bstack1ll11l11l_opy_):
  if bstack11l1l1l_opy_ (u"ࠧࡱࡴࡨࡪࡸ࠭ऩ") in bstack1ll11l11l_opy_:
    for bstack1l1llll1ll_opy_ in bstack1ll11l11l_opy_[bstack11l1l1l_opy_ (u"ࠨࡲࡵࡩ࡫ࡹࠧप")]:
      if bstack1l1llll1ll_opy_ in options._preferences:
        options._preferences[bstack1l1llll1ll_opy_] = update(options._preferences[bstack1l1llll1ll_opy_], bstack1ll11l11l_opy_[bstack11l1l1l_opy_ (u"ࠩࡳࡶࡪ࡬ࡳࠨफ")][bstack1l1llll1ll_opy_])
      else:
        options.set_preference(bstack1l1llll1ll_opy_, bstack1ll11l11l_opy_[bstack11l1l1l_opy_ (u"ࠪࡴࡷ࡫ࡦࡴࠩब")][bstack1l1llll1ll_opy_])
  if bstack11l1l1l_opy_ (u"ࠫࡦࡸࡧࡴࠩभ") in bstack1ll11l11l_opy_:
    for arg in bstack1ll11l11l_opy_[bstack11l1l1l_opy_ (u"ࠬࡧࡲࡨࡵࠪम")]:
      options.add_argument(arg)
def bstack1l1ll1l111_opy_(options, bstack111ll1ll_opy_):
  if bstack11l1l1l_opy_ (u"࠭ࡷࡦࡤࡹ࡭ࡪࡽࠧय") in bstack111ll1ll_opy_:
    options.use_webview(bool(bstack111ll1ll_opy_[bstack11l1l1l_opy_ (u"ࠧࡸࡧࡥࡺ࡮࡫ࡷࠨर")]))
  bstack11ll1l11l_opy_(options, bstack111ll1ll_opy_)
def bstack11l1l11l_opy_(options, bstack1l111ll1_opy_):
  for bstack111l1111_opy_ in bstack1l111ll1_opy_:
    if bstack111l1111_opy_ in [bstack11l1l1l_opy_ (u"ࠨࡶࡨࡧ࡭ࡴ࡯࡭ࡱࡪࡽࡕࡸࡥࡷ࡫ࡨࡻࠬऱ"), bstack11l1l1l_opy_ (u"ࠩࡤࡶ࡬ࡹࠧल")]:
      continue
    options.set_capability(bstack111l1111_opy_, bstack1l111ll1_opy_[bstack111l1111_opy_])
  if bstack11l1l1l_opy_ (u"ࠪࡥࡷ࡭ࡳࠨळ") in bstack1l111ll1_opy_:
    for arg in bstack1l111ll1_opy_[bstack11l1l1l_opy_ (u"ࠫࡦࡸࡧࡴࠩऴ")]:
      options.add_argument(arg)
  if bstack11l1l1l_opy_ (u"ࠬࡺࡥࡤࡪࡱࡳࡱࡵࡧࡺࡒࡵࡩࡻ࡯ࡥࡸࠩव") in bstack1l111ll1_opy_:
    options.bstack1ll1l1l1_opy_(bool(bstack1l111ll1_opy_[bstack11l1l1l_opy_ (u"࠭ࡴࡦࡥ࡫ࡲࡴࡲ࡯ࡨࡻࡓࡶࡪࡼࡩࡦࡹࠪश")]))
def bstack1ll1l1111l_opy_(options, bstack111111l1l_opy_):
  for bstack1llll11ll1_opy_ in bstack111111l1l_opy_:
    if bstack1llll11ll1_opy_ in [bstack11l1l1l_opy_ (u"ࠧࡢࡦࡧ࡭ࡹ࡯࡯࡯ࡣ࡯ࡓࡵࡺࡩࡰࡰࡶࠫष"), bstack11l1l1l_opy_ (u"ࠨࡣࡵ࡫ࡸ࠭स")]:
      continue
    options._options[bstack1llll11ll1_opy_] = bstack111111l1l_opy_[bstack1llll11ll1_opy_]
  if bstack11l1l1l_opy_ (u"ࠩࡤࡨࡩ࡯ࡴࡪࡱࡱࡥࡱࡕࡰࡵ࡫ࡲࡲࡸ࠭ह") in bstack111111l1l_opy_:
    for bstack1l1lll1ll1_opy_ in bstack111111l1l_opy_[bstack11l1l1l_opy_ (u"ࠪࡥࡩࡪࡩࡵ࡫ࡲࡲࡦࡲࡏࡱࡶ࡬ࡳࡳࡹࠧऺ")]:
      options.bstack1l11ll11l_opy_(
        bstack1l1lll1ll1_opy_, bstack111111l1l_opy_[bstack11l1l1l_opy_ (u"ࠫࡦࡪࡤࡪࡶ࡬ࡳࡳࡧ࡬ࡐࡲࡷ࡭ࡴࡴࡳࠨऻ")][bstack1l1lll1ll1_opy_])
  if bstack11l1l1l_opy_ (u"ࠬࡧࡲࡨࡵ़ࠪ") in bstack111111l1l_opy_:
    for arg in bstack111111l1l_opy_[bstack11l1l1l_opy_ (u"࠭ࡡࡳࡩࡶࠫऽ")]:
      options.add_argument(arg)
def bstack1lll111l1l_opy_(options, caps):
  if not hasattr(options, bstack11l1l1l_opy_ (u"ࠧࡌࡇ࡜ࠫा")):
    return
  if options.KEY == bstack11l1l1l_opy_ (u"ࠨࡩࡲࡳ࡬ࡀࡣࡩࡴࡲࡱࡪࡕࡰࡵ࡫ࡲࡲࡸ࠭ि") and options.KEY in caps:
    bstack11ll1l11l_opy_(options, caps[bstack11l1l1l_opy_ (u"ࠩࡪࡳࡴ࡭࠺ࡤࡪࡵࡳࡲ࡫ࡏࡱࡶ࡬ࡳࡳࡹࠧी")])
  elif options.KEY == bstack11l1l1l_opy_ (u"ࠪࡱࡴࢀ࠺ࡧ࡫ࡵࡩ࡫ࡵࡸࡐࡲࡷ࡭ࡴࡴࡳࠨु") and options.KEY in caps:
    bstack11111ll11_opy_(options, caps[bstack11l1l1l_opy_ (u"ࠫࡲࡵࡺ࠻ࡨ࡬ࡶࡪ࡬࡯ࡹࡑࡳࡸ࡮ࡵ࡮ࡴࠩू")])
  elif options.KEY == bstack11l1l1l_opy_ (u"ࠬࡹࡡࡧࡣࡵ࡭࠳ࡵࡰࡵ࡫ࡲࡲࡸ࠭ृ") and options.KEY in caps:
    bstack11l1l11l_opy_(options, caps[bstack11l1l1l_opy_ (u"࠭ࡳࡢࡨࡤࡶ࡮࠴࡯ࡱࡶ࡬ࡳࡳࡹࠧॄ")])
  elif options.KEY == bstack11l1l1l_opy_ (u"ࠧ࡮ࡵ࠽ࡩࡩ࡭ࡥࡐࡲࡷ࡭ࡴࡴࡳࠨॅ") and options.KEY in caps:
    bstack1l1ll1l111_opy_(options, caps[bstack11l1l1l_opy_ (u"ࠨ࡯ࡶ࠾ࡪࡪࡧࡦࡑࡳࡸ࡮ࡵ࡮ࡴࠩॆ")])
  elif options.KEY == bstack11l1l1l_opy_ (u"ࠩࡶࡩ࠿࡯ࡥࡐࡲࡷ࡭ࡴࡴࡳࠨे") and options.KEY in caps:
    bstack1ll1l1111l_opy_(options, caps[bstack11l1l1l_opy_ (u"ࠪࡷࡪࡀࡩࡦࡑࡳࡸ࡮ࡵ࡮ࡴࠩै")])
def bstack1ll11lllll_opy_(caps):
  global bstack1lll1l111_opy_
  if isinstance(os.environ.get(bstack11l1l1l_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡍࡘࡥࡁࡑࡒࡢࡅ࡚࡚ࡏࡎࡃࡗࡉࠬॉ")), str):
    bstack1lll1l111_opy_ = eval(os.getenv(bstack11l1l1l_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣࡎ࡙࡟ࡂࡒࡓࡣࡆ࡛ࡔࡐࡏࡄࡘࡊ࠭ॊ")))
  if bstack1lll1l111_opy_:
    if bstack1l111ll1l_opy_() < version.parse(bstack11l1l1l_opy_ (u"࠭࠲࠯࠵࠱࠴ࠬो")):
      return None
    else:
      from appium.options.common.base import AppiumOptions
      options = AppiumOptions().load_capabilities(caps)
      return options
  else:
    browser = bstack11l1l1l_opy_ (u"ࠧࡤࡪࡵࡳࡲ࡫ࠧौ")
    if bstack11l1l1l_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡐࡤࡱࡪ्࠭") in caps:
      browser = caps[bstack11l1l1l_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡑࡥࡲ࡫ࠧॎ")]
    elif bstack11l1l1l_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࠫॏ") in caps:
      browser = caps[bstack11l1l1l_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࠬॐ")]
    browser = str(browser).lower()
    if browser == bstack11l1l1l_opy_ (u"ࠬ࡯ࡰࡩࡱࡱࡩࠬ॑") or browser == bstack11l1l1l_opy_ (u"࠭ࡩࡱࡣࡧ॒ࠫ"):
      browser = bstack11l1l1l_opy_ (u"ࠧࡴࡣࡩࡥࡷ࡯ࠧ॓")
    if browser == bstack11l1l1l_opy_ (u"ࠨࡵࡤࡱࡸࡻ࡮ࡨࠩ॔"):
      browser = bstack11l1l1l_opy_ (u"ࠩࡦ࡬ࡷࡵ࡭ࡦࠩॕ")
    if browser not in [bstack11l1l1l_opy_ (u"ࠪࡧ࡭ࡸ࡯࡮ࡧࠪॖ"), bstack11l1l1l_opy_ (u"ࠫࡪࡪࡧࡦࠩॗ"), bstack11l1l1l_opy_ (u"ࠬ࡯ࡥࠨक़"), bstack11l1l1l_opy_ (u"࠭ࡳࡢࡨࡤࡶ࡮࠭ख़"), bstack11l1l1l_opy_ (u"ࠧࡧ࡫ࡵࡩ࡫ࡵࡸࠨग़")]:
      return None
    try:
      package = bstack11l1l1l_opy_ (u"ࠨࡵࡨࡰࡪࡴࡩࡶ࡯࠱ࡻࡪࡨࡤࡳ࡫ࡹࡩࡷ࠴ࡻࡾ࠰ࡲࡴࡹ࡯࡯࡯ࡵࠪज़").format(browser)
      name = bstack11l1l1l_opy_ (u"ࠩࡒࡴࡹ࡯࡯࡯ࡵࠪड़")
      browser_options = getattr(__import__(package, fromlist=[name]), name)
      options = browser_options()
      if not bstack1111l1111_opy_(options):
        return None
      for bstack11l1l1l11_opy_ in caps.keys():
        options.set_capability(bstack11l1l1l11_opy_, caps[bstack11l1l1l11_opy_])
      bstack1lll111l1l_opy_(options, caps)
      return options
    except Exception as e:
      logger.debug(str(e))
      return None
def bstack1ll1l1ll_opy_(options, bstack1ll1lll11_opy_):
  if not bstack1111l1111_opy_(options):
    return
  for bstack11l1l1l11_opy_ in bstack1ll1lll11_opy_.keys():
    if bstack11l1l1l11_opy_ in bstack1l1l1ll1_opy_:
      continue
    if bstack11l1l1l11_opy_ in options._caps and type(options._caps[bstack11l1l1l11_opy_]) in [dict, list]:
      options._caps[bstack11l1l1l11_opy_] = update(options._caps[bstack11l1l1l11_opy_], bstack1ll1lll11_opy_[bstack11l1l1l11_opy_])
    else:
      options.set_capability(bstack11l1l1l11_opy_, bstack1ll1lll11_opy_[bstack11l1l1l11_opy_])
  bstack1lll111l1l_opy_(options, bstack1ll1lll11_opy_)
  if bstack11l1l1l_opy_ (u"ࠪࡱࡴࢀ࠺ࡥࡧࡥࡹ࡬࡭ࡥࡳࡃࡧࡨࡷ࡫ࡳࡴࠩढ़") in options._caps:
    if options._caps[bstack11l1l1l_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡓࡧ࡭ࡦࠩफ़")] and options._caps[bstack11l1l1l_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡔࡡ࡮ࡧࠪय़")].lower() != bstack11l1l1l_opy_ (u"࠭ࡦࡪࡴࡨࡪࡴࡾࠧॠ"):
      del options._caps[bstack11l1l1l_opy_ (u"ࠧ࡮ࡱࡽ࠾ࡩ࡫ࡢࡶࡩࡪࡩࡷࡇࡤࡥࡴࡨࡷࡸ࠭ॡ")]
def bstack11ll111ll_opy_(proxy_config):
  if bstack11l1l1l_opy_ (u"ࠨࡪࡷࡸࡵࡹࡐࡳࡱࡻࡽࠬॢ") in proxy_config:
    proxy_config[bstack11l1l1l_opy_ (u"ࠩࡶࡷࡱࡖࡲࡰࡺࡼࠫॣ")] = proxy_config[bstack11l1l1l_opy_ (u"ࠪ࡬ࡹࡺࡰࡴࡒࡵࡳࡽࡿࠧ।")]
    del (proxy_config[bstack11l1l1l_opy_ (u"ࠫ࡭ࡺࡴࡱࡵࡓࡶࡴࡾࡹࠨ॥")])
  if bstack11l1l1l_opy_ (u"ࠬࡶࡲࡰࡺࡼࡘࡾࡶࡥࠨ०") in proxy_config and proxy_config[bstack11l1l1l_opy_ (u"࠭ࡰࡳࡱࡻࡽ࡙ࡿࡰࡦࠩ१")].lower() != bstack11l1l1l_opy_ (u"ࠧࡥ࡫ࡵࡩࡨࡺࠧ२"):
    proxy_config[bstack11l1l1l_opy_ (u"ࠨࡲࡵࡳࡽࡿࡔࡺࡲࡨࠫ३")] = bstack11l1l1l_opy_ (u"ࠩࡰࡥࡳࡻࡡ࡭ࠩ४")
  if bstack11l1l1l_opy_ (u"ࠪࡴࡷࡵࡸࡺࡃࡸࡸࡴࡩ࡯࡯ࡨ࡬࡫࡚ࡸ࡬ࠨ५") in proxy_config:
    proxy_config[bstack11l1l1l_opy_ (u"ࠫࡵࡸ࡯ࡹࡻࡗࡽࡵ࡫ࠧ६")] = bstack11l1l1l_opy_ (u"ࠬࡶࡡࡤࠩ७")
  return proxy_config
def bstack1ll1ll11l1_opy_(config, proxy):
  from selenium.webdriver.common.proxy import Proxy
  if not bstack11l1l1l_opy_ (u"࠭ࡰࡳࡱࡻࡽࠬ८") in config:
    return proxy
  config[bstack11l1l1l_opy_ (u"ࠧࡱࡴࡲࡼࡾ࠭९")] = bstack11ll111ll_opy_(config[bstack11l1l1l_opy_ (u"ࠨࡲࡵࡳࡽࡿࠧ॰")])
  if proxy == None:
    proxy = Proxy(config[bstack11l1l1l_opy_ (u"ࠩࡳࡶࡴࡾࡹࠨॱ")])
  return proxy
def bstack1lll11lll1_opy_(self):
  global CONFIG
  global bstack11llll11_opy_
  try:
    proxy = bstack1ll1111l_opy_(CONFIG)
    if proxy:
      if proxy.endswith(bstack11l1l1l_opy_ (u"ࠪ࠲ࡵࡧࡣࠨॲ")):
        proxies = bstack1111l1l1l_opy_(proxy, bstack1llllllll_opy_())
        if len(proxies) > 0:
          protocol, bstack1lllllllll_opy_ = proxies.popitem()
          if bstack11l1l1l_opy_ (u"ࠦ࠿࠵࠯ࠣॳ") in bstack1lllllllll_opy_:
            return bstack1lllllllll_opy_
          else:
            return bstack11l1l1l_opy_ (u"ࠧ࡮ࡴࡵࡲ࠽࠳࠴ࠨॴ") + bstack1lllllllll_opy_
      else:
        return proxy
  except Exception as e:
    logger.error(bstack11l1l1l_opy_ (u"ࠨࡅࡳࡴࡲࡶࠥ࡯࡮ࠡࡵࡨࡸࡹ࡯࡮ࡨࠢࡳࡶࡴࡾࡹࠡࡷࡵࡰࠥࡀࠠࡼࡿࠥॵ").format(str(e)))
  return bstack11llll11_opy_(self)
def bstack1ll1111ll1_opy_():
  global CONFIG
  return bstack1l11l111l_opy_(CONFIG) and bstack11l111lll_opy_() and bstack1llll1lll_opy_() >= version.parse(bstack1ll1l11ll1_opy_)
def bstack11lll1lll_opy_():
  global CONFIG
  return (bstack11l1l1l_opy_ (u"ࠧࡩࡶࡷࡴࡕࡸ࡯ࡹࡻࠪॶ") in CONFIG or bstack11l1l1l_opy_ (u"ࠨࡪࡷࡸࡵࡹࡐࡳࡱࡻࡽࠬॷ") in CONFIG) and bstack11llllll_opy_()
def bstack11l1111l_opy_(config):
  bstack1ll1lll1l_opy_ = {}
  if bstack11l1l1l_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡖࡸࡦࡩ࡫ࡍࡱࡦࡥࡱࡕࡰࡵ࡫ࡲࡲࡸ࠭ॸ") in config:
    bstack1ll1lll1l_opy_ = config[bstack11l1l1l_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡗࡹࡧࡣ࡬ࡎࡲࡧࡦࡲࡏࡱࡶ࡬ࡳࡳࡹࠧॹ")]
  if bstack11l1l1l_opy_ (u"ࠫࡱࡵࡣࡢ࡮ࡒࡴࡹ࡯࡯࡯ࡵࠪॺ") in config:
    bstack1ll1lll1l_opy_ = config[bstack11l1l1l_opy_ (u"ࠬࡲ࡯ࡤࡣ࡯ࡓࡵࡺࡩࡰࡰࡶࠫॻ")]
  proxy = bstack1ll1111l_opy_(config)
  if proxy:
    if proxy.endswith(bstack11l1l1l_opy_ (u"࠭࠮ࡱࡣࡦࠫॼ")) and os.path.isfile(proxy):
      bstack1ll1lll1l_opy_[bstack11l1l1l_opy_ (u"ࠧ࠮ࡲࡤࡧ࠲࡬ࡩ࡭ࡧࠪॽ")] = proxy
    else:
      parsed_url = None
      if proxy.endswith(bstack11l1l1l_opy_ (u"ࠨ࠰ࡳࡥࡨ࠭ॾ")):
        proxies = bstack1ll1l1l1l_opy_(config, bstack1llllllll_opy_())
        if len(proxies) > 0:
          protocol, bstack1lllllllll_opy_ = proxies.popitem()
          if bstack11l1l1l_opy_ (u"ࠤ࠽࠳࠴ࠨॿ") in bstack1lllllllll_opy_:
            parsed_url = urlparse(bstack1lllllllll_opy_)
          else:
            parsed_url = urlparse(protocol + bstack11l1l1l_opy_ (u"ࠥ࠾࠴࠵ࠢঀ") + bstack1lllllllll_opy_)
      else:
        parsed_url = urlparse(proxy)
      if parsed_url and parsed_url.hostname: bstack1ll1lll1l_opy_[bstack11l1l1l_opy_ (u"ࠫࡵࡸ࡯ࡹࡻࡋࡳࡸࡺࠧঁ")] = str(parsed_url.hostname)
      if parsed_url and parsed_url.port: bstack1ll1lll1l_opy_[bstack11l1l1l_opy_ (u"ࠬࡶࡲࡰࡺࡼࡔࡴࡸࡴࠨং")] = str(parsed_url.port)
      if parsed_url and parsed_url.username: bstack1ll1lll1l_opy_[bstack11l1l1l_opy_ (u"࠭ࡰࡳࡱࡻࡽ࡚ࡹࡥࡳࠩঃ")] = str(parsed_url.username)
      if parsed_url and parsed_url.password: bstack1ll1lll1l_opy_[bstack11l1l1l_opy_ (u"ࠧࡱࡴࡲࡼࡾࡖࡡࡴࡵࠪ঄")] = str(parsed_url.password)
  return bstack1ll1lll1l_opy_
def bstack11111l11_opy_(config):
  if bstack11l1l1l_opy_ (u"ࠨࡶࡨࡷࡹࡉ࡯࡯ࡶࡨࡼࡹࡕࡰࡵ࡫ࡲࡲࡸ࠭অ") in config:
    return config[bstack11l1l1l_opy_ (u"ࠩࡷࡩࡸࡺࡃࡰࡰࡷࡩࡽࡺࡏࡱࡶ࡬ࡳࡳࡹࠧআ")]
  return {}
def bstack11l11l11l_opy_(caps):
  global bstack11l111111_opy_
  if bstack11l1l1l_opy_ (u"ࠪࡦࡸࡺࡡࡤ࡭࠽ࡳࡵࡺࡩࡰࡰࡶࠫই") in caps:
    caps[bstack11l1l1l_opy_ (u"ࠫࡧࡹࡴࡢࡥ࡮࠾ࡴࡶࡴࡪࡱࡱࡷࠬঈ")][bstack11l1l1l_opy_ (u"ࠬࡲ࡯ࡤࡣ࡯ࠫউ")] = True
    if bstack11l111111_opy_:
      caps[bstack11l1l1l_opy_ (u"࠭ࡢࡴࡶࡤࡧࡰࡀ࡯ࡱࡶ࡬ࡳࡳࡹࠧঊ")][bstack11l1l1l_opy_ (u"ࠧ࡭ࡱࡦࡥࡱࡏࡤࡦࡰࡷ࡭࡫࡯ࡥࡳࠩঋ")] = bstack11l111111_opy_
  else:
    caps[bstack11l1l1l_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠮࡭ࡱࡦࡥࡱ࠭ঌ")] = True
    if bstack11l111111_opy_:
      caps[bstack11l1l1l_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫࠯࡮ࡲࡧࡦࡲࡉࡥࡧࡱࡸ࡮࡬ࡩࡦࡴࠪ঍")] = bstack11l111111_opy_
def bstack1l111l111_opy_():
  global CONFIG
  if bstack11l1l1l_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࡎࡲࡧࡦࡲࠧ঎") in CONFIG and bstack1111llll_opy_(CONFIG[bstack11l1l1l_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࡏࡳࡨࡧ࡬ࠨএ")]):
    bstack1ll1lll1l_opy_ = bstack11l1111l_opy_(CONFIG)
    bstack1ll11ll1ll_opy_(CONFIG[bstack11l1l1l_opy_ (u"ࠬࡧࡣࡤࡧࡶࡷࡐ࡫ࡹࠨঐ")], bstack1ll1lll1l_opy_)
def bstack1ll11ll1ll_opy_(key, bstack1ll1lll1l_opy_):
  global bstack1l1l11ll_opy_
  logger.info(bstack1111ll11l_opy_)
  try:
    bstack1l1l11ll_opy_ = Local()
    bstack1lllll1111_opy_ = {bstack11l1l1l_opy_ (u"࠭࡫ࡦࡻࠪ঑"): key}
    bstack1lllll1111_opy_.update(bstack1ll1lll1l_opy_)
    logger.debug(bstack11ll1l11_opy_.format(str(bstack1lllll1111_opy_)))
    bstack1l1l11ll_opy_.start(**bstack1lllll1111_opy_)
    if bstack1l1l11ll_opy_.isRunning():
      logger.info(bstack1lll1111l_opy_)
  except Exception as e:
    bstack111l1l111_opy_(bstack1ll111l11_opy_.format(str(e)))
def bstack11llll1l_opy_():
  global bstack1l1l11ll_opy_
  if bstack1l1l11ll_opy_.isRunning():
    logger.info(bstack1lll1lll11_opy_)
    bstack1l1l11ll_opy_.stop()
  bstack1l1l11ll_opy_ = None
def bstack1ll1lll1_opy_(bstack1l1l111ll_opy_=[]):
  global CONFIG
  bstack11ll1ll11_opy_ = []
  bstack1ll1lll1l1_opy_ = [bstack11l1l1l_opy_ (u"ࠧࡰࡵࠪ঒"), bstack11l1l1l_opy_ (u"ࠨࡱࡶ࡚ࡪࡸࡳࡪࡱࡱࠫও"), bstack11l1l1l_opy_ (u"ࠩࡧࡩࡻ࡯ࡣࡦࡐࡤࡱࡪ࠭ঔ"), bstack11l1l1l_opy_ (u"ࠪࡴࡱࡧࡴࡧࡱࡵࡱ࡛࡫ࡲࡴ࡫ࡲࡲࠬক"), bstack11l1l1l_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡓࡧ࡭ࡦࠩখ"), bstack11l1l1l_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷ࡜ࡥࡳࡵ࡬ࡳࡳ࠭গ")]
  try:
    for err in bstack1l1l111ll_opy_:
      bstack1lll1l111l_opy_ = {}
      for k in bstack1ll1lll1l1_opy_:
        val = CONFIG[bstack11l1l1l_opy_ (u"࠭ࡰ࡭ࡣࡷࡪࡴࡸ࡭ࡴࠩঘ")][int(err[bstack11l1l1l_opy_ (u"ࠧࡪࡰࡧࡩࡽ࠭ঙ")])].get(k)
        if val:
          bstack1lll1l111l_opy_[k] = val
      bstack1lll1l111l_opy_[bstack11l1l1l_opy_ (u"ࠨࡶࡨࡷࡹࡹࠧচ")] = {
        err[bstack11l1l1l_opy_ (u"ࠩࡱࡥࡲ࡫ࠧছ")]: err[bstack11l1l1l_opy_ (u"ࠪࡩࡷࡸ࡯ࡳࠩজ")]
      }
      bstack11ll1ll11_opy_.append(bstack1lll1l111l_opy_)
  except Exception as e:
    logger.debug(bstack11l1l1l_opy_ (u"ࠫࡊࡸࡲࡰࡴࠣ࡭ࡳࠦࡦࡰࡴࡰࡥࡹࡺࡩ࡯ࡩࠣࡨࡦࡺࡡࠡࡨࡲࡶࠥ࡫ࡶࡦࡰࡷ࠾ࠥ࠭ঝ") + str(e))
  finally:
    return bstack11ll1ll11_opy_
def bstack1l1ll1l1l_opy_(file_name):
  bstack1ll111ll_opy_ = []
  try:
    bstack1llll11ll_opy_ = os.path.join(tempfile.gettempdir(), file_name)
    if os.path.exists(bstack1llll11ll_opy_):
      with open(bstack1llll11ll_opy_) as f:
        bstack11111llll_opy_ = json.load(f)
        bstack1ll111ll_opy_ = bstack11111llll_opy_
      os.remove(bstack1llll11ll_opy_)
    return bstack1ll111ll_opy_
  except Exception as e:
    logger.debug(bstack11l1l1l_opy_ (u"ࠬࡋࡲࡳࡱࡵࠤ࡮ࡴࠠࡧ࡫ࡱࡨ࡮ࡴࡧࠡࡧࡵࡶࡴࡸࠠ࡭࡫ࡶࡸ࠿ࠦࠧঞ") + str(e))
def bstack111111ll1_opy_():
  global bstack1lll111l11_opy_
  global bstack11111lll1_opy_
  global bstack11ll1l1l1_opy_
  global bstack1llll1l11l_opy_
  global bstack111l11l1_opy_
  global bstack11l1l111_opy_
  percy.shutdown()
  bstack1lll1l1l_opy_ = os.environ.get(bstack11l1l1l_opy_ (u"࠭ࡆࡓࡃࡐࡉ࡜ࡕࡒࡌࡡࡘࡗࡊࡊࠧট"))
  if bstack1lll1l1l_opy_ in [bstack11l1l1l_opy_ (u"ࠧࡳࡱࡥࡳࡹ࠭ঠ"), bstack11l1l1l_opy_ (u"ࠨࡲࡤࡦࡴࡺࠧড")]:
    bstack11111l11l_opy_()
  if bstack1lll111l11_opy_:
    logger.warning(bstack111l11111_opy_.format(str(bstack1lll111l11_opy_)))
  else:
    try:
      bstack1ll1llll1l_opy_ = bstack1lll111lll_opy_(bstack11l1l1l_opy_ (u"ࠩ࠱ࡦࡸࡺࡡࡤ࡭࠰ࡧࡴࡴࡦࡪࡩ࠱࡮ࡸࡵ࡮ࠨঢ"), logger)
      if bstack1ll1llll1l_opy_.get(bstack11l1l1l_opy_ (u"ࠪࡲࡺࡪࡧࡦࡡ࡯ࡳࡨࡧ࡬ࠨণ")) and bstack1ll1llll1l_opy_.get(bstack11l1l1l_opy_ (u"ࠫࡳࡻࡤࡨࡧࡢࡰࡴࡩࡡ࡭ࠩত")).get(bstack11l1l1l_opy_ (u"ࠬ࡮࡯ࡴࡶࡱࡥࡲ࡫ࠧথ")):
        logger.warning(bstack111l11111_opy_.format(str(bstack1ll1llll1l_opy_[bstack11l1l1l_opy_ (u"࠭࡮ࡶࡦࡪࡩࡤࡲ࡯ࡤࡣ࡯ࠫদ")][bstack11l1l1l_opy_ (u"ࠧࡩࡱࡶࡸࡳࡧ࡭ࡦࠩধ")])))
    except Exception as e:
      logger.error(e)
  logger.info(bstack1l1lll111_opy_)
  global bstack1l1l11ll_opy_
  if bstack1l1l11ll_opy_:
    bstack11llll1l_opy_()
  try:
    for driver in bstack11111lll1_opy_:
      driver.quit()
  except Exception as e:
    pass
  logger.info(bstack11l111l1_opy_)
  if bstack11l1l111_opy_ == bstack11l1l1l_opy_ (u"ࠨࡴࡲࡦࡴࡺࠧন"):
    bstack111l11l1_opy_ = bstack1l1ll1l1l_opy_(bstack11l1l1l_opy_ (u"ࠩࡵࡳࡧࡵࡴࡠࡧࡵࡶࡴࡸ࡟࡭࡫ࡶࡸ࠳ࡰࡳࡰࡰࠪ঩"))
  if bstack11l1l111_opy_ == bstack11l1l1l_opy_ (u"ࠪࡴࡾࡺࡥࡴࡶࠪপ") and len(bstack1llll1l11l_opy_) == 0:
    bstack1llll1l11l_opy_ = bstack1l1ll1l1l_opy_(bstack11l1l1l_opy_ (u"ࠫࡵࡽ࡟ࡱࡻࡷࡩࡸࡺ࡟ࡦࡴࡵࡳࡷࡥ࡬ࡪࡵࡷ࠲࡯ࡹ࡯࡯ࠩফ"))
    if len(bstack1llll1l11l_opy_) == 0:
      bstack1llll1l11l_opy_ = bstack1l1ll1l1l_opy_(bstack11l1l1l_opy_ (u"ࠬࡶࡹࡵࡧࡶࡸࡤࡶࡰࡱࡡࡨࡶࡷࡵࡲࡠ࡮࡬ࡷࡹ࠴ࡪࡴࡱࡱࠫব"))
  bstack111l11lll_opy_ = bstack11l1l1l_opy_ (u"࠭ࠧভ")
  if len(bstack11ll1l1l1_opy_) > 0:
    bstack111l11lll_opy_ = bstack1ll1lll1_opy_(bstack11ll1l1l1_opy_)
  elif len(bstack1llll1l11l_opy_) > 0:
    bstack111l11lll_opy_ = bstack1ll1lll1_opy_(bstack1llll1l11l_opy_)
  elif len(bstack111l11l1_opy_) > 0:
    bstack111l11lll_opy_ = bstack1ll1lll1_opy_(bstack111l11l1_opy_)
  elif len(bstack11l11ll1_opy_) > 0:
    bstack111l11lll_opy_ = bstack1ll1lll1_opy_(bstack11l11ll1_opy_)
  if bool(bstack111l11lll_opy_):
    bstack1l1111l1l_opy_(bstack111l11lll_opy_)
  else:
    bstack1l1111l1l_opy_()
  bstack111l1llll_opy_(bstack111ll111l_opy_, logger)
def bstack1l111l1l1_opy_(self, *args):
  logger.error(bstack1l11llll_opy_)
  bstack111111ll1_opy_()
  sys.exit(1)
def bstack111l1l111_opy_(err):
  logger.critical(bstack11ll1lll1_opy_.format(str(err)))
  bstack1l1111l1l_opy_(bstack11ll1lll1_opy_.format(str(err)))
  atexit.unregister(bstack111111ll1_opy_)
  bstack11111l11l_opy_()
  sys.exit(1)
def bstack1111l111l_opy_(error, message):
  logger.critical(str(error))
  logger.critical(message)
  bstack1l1111l1l_opy_(message)
  atexit.unregister(bstack111111ll1_opy_)
  bstack11111l11l_opy_()
  sys.exit(1)
def bstack1l11111l1_opy_():
  global CONFIG
  global bstack11lllll1_opy_
  global bstack111ll1ll1_opy_
  global bstack11l1l1ll1_opy_
  CONFIG = bstack1ll1l11l_opy_()
  bstack1lll1ll1_opy_()
  bstack1ll111l1l_opy_()
  CONFIG = bstack1l1ll1l1ll_opy_(CONFIG)
  update(CONFIG, bstack111ll1ll1_opy_)
  update(CONFIG, bstack11lllll1_opy_)
  CONFIG = bstack1l1ll1lll_opy_(CONFIG)
  bstack11l1l1ll1_opy_ = bstack1ll11ll11_opy_(CONFIG)
  bstack1lllll111l_opy_.bstack1lllll1ll_opy_(bstack11l1l1l_opy_ (u"ࠧࡣࡵࡷࡥࡨࡱ࡟ࡴࡧࡶࡷ࡮ࡵ࡮ࠨম"), bstack11l1l1ll1_opy_)
  if (bstack11l1l1l_opy_ (u"ࠨࡤࡸ࡭ࡱࡪࡎࡢ࡯ࡨࠫয") in CONFIG and bstack11l1l1l_opy_ (u"ࠩࡥࡹ࡮ࡲࡤࡏࡣࡰࡩࠬর") in bstack11lllll1_opy_) or (
          bstack11l1l1l_opy_ (u"ࠪࡦࡺ࡯࡬ࡥࡐࡤࡱࡪ࠭঱") in CONFIG and bstack11l1l1l_opy_ (u"ࠫࡧࡻࡩ࡭ࡦࡑࡥࡲ࡫ࠧল") not in bstack111ll1ll1_opy_):
    if os.getenv(bstack11l1l1l_opy_ (u"ࠬࡈࡓࡕࡃࡆࡏࡤࡉࡏࡎࡄࡌࡒࡊࡊ࡟ࡃࡗࡌࡐࡉࡥࡉࡅࠩ঳")):
      CONFIG[bstack11l1l1l_opy_ (u"࠭ࡢࡶ࡫࡯ࡨࡎࡪࡥ࡯ࡶ࡬ࡪ࡮࡫ࡲࠨ঴")] = os.getenv(bstack11l1l1l_opy_ (u"ࠧࡃࡕࡗࡅࡈࡑ࡟ࡄࡑࡐࡆࡎࡔࡅࡅࡡࡅ࡙ࡎࡒࡄࡠࡋࡇࠫ঵"))
    else:
      bstack1llllll111_opy_()
  elif (bstack11l1l1l_opy_ (u"ࠨࡤࡸ࡭ࡱࡪࡎࡢ࡯ࡨࠫশ") not in CONFIG and bstack11l1l1l_opy_ (u"ࠩࡥࡹ࡮ࡲࡤࡊࡦࡨࡲࡹ࡯ࡦࡪࡧࡵࠫষ") in CONFIG) or (
          bstack11l1l1l_opy_ (u"ࠪࡦࡺ࡯࡬ࡥࡐࡤࡱࡪ࠭স") in bstack111ll1ll1_opy_ and bstack11l1l1l_opy_ (u"ࠫࡧࡻࡩ࡭ࡦࡑࡥࡲ࡫ࠧহ") not in bstack11lllll1_opy_):
    del (CONFIG[bstack11l1l1l_opy_ (u"ࠬࡨࡵࡪ࡮ࡧࡍࡩ࡫࡮ࡵ࡫ࡩ࡭ࡪࡸࠧ঺")])
  if bstack1l11l1lll_opy_(CONFIG):
    bstack111l1l111_opy_(bstack111l111ll_opy_)
  bstack1111111l1_opy_()
  bstack1lllll11ll_opy_()
  if bstack1lll1l111_opy_:
    CONFIG[bstack11l1l1l_opy_ (u"࠭ࡡࡱࡲࠪ঻")] = bstack1l1l1l1l_opy_(CONFIG)
    logger.info(bstack1ll1l1l111_opy_.format(CONFIG[bstack11l1l1l_opy_ (u"ࠧࡢࡲࡳ়ࠫ")]))
def bstack1ll1llll_opy_(config, bstack1ll111lll1_opy_):
  global CONFIG
  global bstack1lll1l111_opy_
  CONFIG = config
  bstack1lll1l111_opy_ = bstack1ll111lll1_opy_
def bstack1lllll11ll_opy_():
  global CONFIG
  global bstack1lll1l111_opy_
  if bstack11l1l1l_opy_ (u"ࠨࡣࡳࡴࠬঽ") in CONFIG:
    try:
      from appium import version
    except Exception as e:
      bstack1111l111l_opy_(e, bstack1111l1ll1_opy_)
    bstack1lll1l111_opy_ = True
    bstack1lllll111l_opy_.bstack1lllll1ll_opy_(bstack11l1l1l_opy_ (u"ࠩࡤࡴࡵࡥࡡࡶࡶࡲࡱࡦࡺࡥࠨা"), True)
def bstack1l1l1l1l_opy_(config):
  bstack1l11lll1l_opy_ = bstack11l1l1l_opy_ (u"ࠪࠫি")
  app = config[bstack11l1l1l_opy_ (u"ࠫࡦࡶࡰࠨী")]
  if isinstance(app, str):
    if os.path.splitext(app)[1] in bstack11ll1l111_opy_:
      if os.path.exists(app):
        bstack1l11lll1l_opy_ = bstack1l1lll1ll_opy_(config, app)
      elif bstack1l111llll_opy_(app):
        bstack1l11lll1l_opy_ = app
      else:
        bstack111l1l111_opy_(bstack1l11ll11_opy_.format(app))
    else:
      if bstack1l111llll_opy_(app):
        bstack1l11lll1l_opy_ = app
      elif os.path.exists(app):
        bstack1l11lll1l_opy_ = bstack1l1lll1ll_opy_(app)
      else:
        bstack111l1l111_opy_(bstack11ll11l1l_opy_)
  else:
    if len(app) > 2:
      bstack111l1l111_opy_(bstack1l1lllll11_opy_)
    elif len(app) == 2:
      if bstack11l1l1l_opy_ (u"ࠬࡶࡡࡵࡪࠪু") in app and bstack11l1l1l_opy_ (u"࠭ࡣࡶࡵࡷࡳࡲࡥࡩࡥࠩূ") in app:
        if os.path.exists(app[bstack11l1l1l_opy_ (u"ࠧࡱࡣࡷ࡬ࠬৃ")]):
          bstack1l11lll1l_opy_ = bstack1l1lll1ll_opy_(config, app[bstack11l1l1l_opy_ (u"ࠨࡲࡤࡸ࡭࠭ৄ")], app[bstack11l1l1l_opy_ (u"ࠩࡦࡹࡸࡺ࡯࡮ࡡ࡬ࡨࠬ৅")])
        else:
          bstack111l1l111_opy_(bstack1l11ll11_opy_.format(app))
      else:
        bstack111l1l111_opy_(bstack1l1lllll11_opy_)
    else:
      for key in app:
        if key in bstack1lll11ll1l_opy_:
          if key == bstack11l1l1l_opy_ (u"ࠪࡴࡦࡺࡨࠨ৆"):
            if os.path.exists(app[key]):
              bstack1l11lll1l_opy_ = bstack1l1lll1ll_opy_(config, app[key])
            else:
              bstack111l1l111_opy_(bstack1l11ll11_opy_.format(app))
          else:
            bstack1l11lll1l_opy_ = app[key]
        else:
          bstack111l1l111_opy_(bstack1ll111lll_opy_)
  return bstack1l11lll1l_opy_
def bstack1l111llll_opy_(bstack1l11lll1l_opy_):
  import re
  bstack1lllllll11_opy_ = re.compile(bstack11l1l1l_opy_ (u"ࡶࠧࡤ࡛ࡢ࠯ࡽࡅ࠲ࡠ࠰࠮࠻࡟ࡣ࠳ࡢ࠭࡞ࠬࠧࠦে"))
  bstack1l1ll11l1_opy_ = re.compile(bstack11l1l1l_opy_ (u"ࡷࠨ࡞࡜ࡣ࠰ࡾࡆ࠳࡚࠱࠯࠼ࡠࡤ࠴࡜࠮࡟࠭࠳ࡠࡧ࠭ࡻࡃ࠰࡞࠵࠳࠹࡝ࡡ࠱ࡠ࠲ࡣࠪࠥࠤৈ"))
  if bstack11l1l1l_opy_ (u"࠭ࡢࡴ࠼࠲࠳ࠬ৉") in bstack1l11lll1l_opy_ or re.fullmatch(bstack1lllllll11_opy_, bstack1l11lll1l_opy_) or re.fullmatch(bstack1l1ll11l1_opy_, bstack1l11lll1l_opy_):
    return True
  else:
    return False
def bstack1l1lll1ll_opy_(config, path, bstack11111l111_opy_=None):
  import requests
  from requests_toolbelt.multipart.encoder import MultipartEncoder
  import hashlib
  md5_hash = hashlib.md5(open(os.path.abspath(path), bstack11l1l1l_opy_ (u"ࠧࡳࡤࠪ৊")).read()).hexdigest()
  bstack1lllll111_opy_ = bstack1l1llll1_opy_(md5_hash)
  bstack1l11lll1l_opy_ = None
  if bstack1lllll111_opy_:
    logger.info(bstack111l1l11l_opy_.format(bstack1lllll111_opy_, md5_hash))
    return bstack1lllll111_opy_
  bstack1lllll11_opy_ = MultipartEncoder(
    fields={
      bstack11l1l1l_opy_ (u"ࠨࡨ࡬ࡰࡪ࠭ো"): (os.path.basename(path), open(os.path.abspath(path), bstack11l1l1l_opy_ (u"ࠩࡵࡦࠬৌ")), bstack11l1l1l_opy_ (u"ࠪࡸࡪࡾࡴ࠰ࡲ࡯ࡥ࡮ࡴ্ࠧ")),
      bstack11l1l1l_opy_ (u"ࠫࡨࡻࡳࡵࡱࡰࡣ࡮ࡪࠧৎ"): bstack11111l111_opy_
    }
  )
  response = requests.post(bstack11ll11111_opy_, data=bstack1lllll11_opy_,
                           headers={bstack11l1l1l_opy_ (u"ࠬࡉ࡯࡯ࡶࡨࡲࡹ࠳ࡔࡺࡲࡨࠫ৏"): bstack1lllll11_opy_.content_type},
                           auth=(config[bstack11l1l1l_opy_ (u"࠭ࡵࡴࡧࡵࡒࡦࡳࡥࠨ৐")], config[bstack11l1l1l_opy_ (u"ࠧࡢࡥࡦࡩࡸࡹࡋࡦࡻࠪ৑")]))
  try:
    res = json.loads(response.text)
    bstack1l11lll1l_opy_ = res[bstack11l1l1l_opy_ (u"ࠨࡣࡳࡴࡤࡻࡲ࡭ࠩ৒")]
    logger.info(bstack11l111l11_opy_.format(bstack1l11lll1l_opy_))
    bstack11l1l11l1_opy_(md5_hash, bstack1l11lll1l_opy_)
  except ValueError as err:
    bstack111l1l111_opy_(bstack11ll11l1_opy_.format(str(err)))
  return bstack1l11lll1l_opy_
def bstack1111111l1_opy_():
  global CONFIG
  global bstack1ll1111l11_opy_
  bstack1l1111ll1_opy_ = 0
  bstack1ll1l1l1l1_opy_ = 1
  if bstack11l1l1l_opy_ (u"ࠩࡳࡥࡷࡧ࡬࡭ࡧ࡯ࡷࡕ࡫ࡲࡑ࡮ࡤࡸ࡫ࡵࡲ࡮ࠩ৓") in CONFIG:
    bstack1ll1l1l1l1_opy_ = CONFIG[bstack11l1l1l_opy_ (u"ࠪࡴࡦࡸࡡ࡭࡮ࡨࡰࡸࡖࡥࡳࡒ࡯ࡥࡹ࡬࡯ࡳ࡯ࠪ৔")]
  if bstack11l1l1l_opy_ (u"ࠫࡵࡲࡡࡵࡨࡲࡶࡲࡹࠧ৕") in CONFIG:
    bstack1l1111ll1_opy_ = len(CONFIG[bstack11l1l1l_opy_ (u"ࠬࡶ࡬ࡢࡶࡩࡳࡷࡳࡳࠨ৖")])
  bstack1ll1111l11_opy_ = int(bstack1ll1l1l1l1_opy_) * int(bstack1l1111ll1_opy_)
def bstack1l1llll1_opy_(md5_hash):
  bstack1lllll1l1_opy_ = os.path.join(os.path.expanduser(bstack11l1l1l_opy_ (u"࠭ࡾࠨৗ")), bstack11l1l1l_opy_ (u"ࠧ࠯ࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱࠧ৘"), bstack11l1l1l_opy_ (u"ࠨࡣࡳࡴ࡚ࡶ࡬ࡰࡣࡧࡑࡉ࠻ࡈࡢࡵ࡫࠲࡯ࡹ࡯࡯ࠩ৙"))
  if os.path.exists(bstack1lllll1l1_opy_):
    bstack1ll1l1llll_opy_ = json.load(open(bstack1lllll1l1_opy_, bstack11l1l1l_opy_ (u"ࠩࡵࡦࠬ৚")))
    if md5_hash in bstack1ll1l1llll_opy_:
      bstack11111111_opy_ = bstack1ll1l1llll_opy_[md5_hash]
      bstack1ll11lll11_opy_ = datetime.datetime.now()
      bstack1lll1111l1_opy_ = datetime.datetime.strptime(bstack11111111_opy_[bstack11l1l1l_opy_ (u"ࠪࡸ࡮ࡳࡥࡴࡶࡤࡱࡵ࠭৛")], bstack11l1l1l_opy_ (u"ࠫࠪࡪ࠯ࠦ࡯࠲ࠩ࡞ࠦࠥࡉ࠼ࠨࡑ࠿ࠫࡓࠨড়"))
      if (bstack1ll11lll11_opy_ - bstack1lll1111l1_opy_).days > 30:
        return None
      elif version.parse(str(__version__)) > version.parse(bstack11111111_opy_[bstack11l1l1l_opy_ (u"ࠬࡹࡤ࡬ࡡࡹࡩࡷࡹࡩࡰࡰࠪঢ়")]):
        return None
      return bstack11111111_opy_[bstack11l1l1l_opy_ (u"࠭ࡩࡥࠩ৞")]
  else:
    return None
def bstack11l1l11l1_opy_(md5_hash, bstack1l11lll1l_opy_):
  bstack1ll1l1lll1_opy_ = os.path.join(os.path.expanduser(bstack11l1l1l_opy_ (u"ࠧࡿࠩয়")), bstack11l1l1l_opy_ (u"ࠨ࠰ࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࠨৠ"))
  if not os.path.exists(bstack1ll1l1lll1_opy_):
    os.makedirs(bstack1ll1l1lll1_opy_)
  bstack1lllll1l1_opy_ = os.path.join(os.path.expanduser(bstack11l1l1l_opy_ (u"ࠩࢁࠫৡ")), bstack11l1l1l_opy_ (u"ࠪ࠲ࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࠪৢ"), bstack11l1l1l_opy_ (u"ࠫࡦࡶࡰࡖࡲ࡯ࡳࡦࡪࡍࡅ࠷ࡋࡥࡸ࡮࠮࡫ࡵࡲࡲࠬৣ"))
  bstack11ll111l1_opy_ = {
    bstack11l1l1l_opy_ (u"ࠬ࡯ࡤࠨ৤"): bstack1l11lll1l_opy_,
    bstack11l1l1l_opy_ (u"࠭ࡴࡪ࡯ࡨࡷࡹࡧ࡭ࡱࠩ৥"): datetime.datetime.strftime(datetime.datetime.now(), bstack11l1l1l_opy_ (u"ࠧࠦࡦ࠲ࠩࡲ࠵࡚ࠥࠢࠨࡌ࠿ࠫࡍ࠻ࠧࡖࠫ০")),
    bstack11l1l1l_opy_ (u"ࠨࡵࡧ࡯ࡤࡼࡥࡳࡵ࡬ࡳࡳ࠭১"): str(__version__)
  }
  if os.path.exists(bstack1lllll1l1_opy_):
    bstack1ll1l1llll_opy_ = json.load(open(bstack1lllll1l1_opy_, bstack11l1l1l_opy_ (u"ࠩࡵࡦࠬ২")))
  else:
    bstack1ll1l1llll_opy_ = {}
  bstack1ll1l1llll_opy_[md5_hash] = bstack11ll111l1_opy_
  with open(bstack1lllll1l1_opy_, bstack11l1l1l_opy_ (u"ࠥࡻ࠰ࠨ৩")) as outfile:
    json.dump(bstack1ll1l1llll_opy_, outfile)
def bstack1l1l11l1_opy_(self):
  return
def bstack1l1l1ll1l_opy_(self):
  return
def bstack11lll1ll1_opy_(self):
  from selenium.webdriver.remote.webdriver import WebDriver
  WebDriver.quit(self)
def bstack1111l1l1_opy_(self):
  global bstack1lllll1ll1_opy_
  global bstack1l1ll1ll1_opy_
  global bstack1l1l1l1ll_opy_
  try:
    if bstack11l1l1l_opy_ (u"ࠫࡵࡿࡴࡦࡵࡷࠫ৪") in bstack1lllll1ll1_opy_ and self.session_id != None and bstack1111l11l_opy_(threading.current_thread(), bstack11l1l1l_opy_ (u"ࠬࡺࡥࡴࡶࡖࡸࡦࡺࡵࡴࠩ৫"), bstack11l1l1l_opy_ (u"࠭ࠧ৬")) != bstack11l1l1l_opy_ (u"ࠧࡴ࡭࡬ࡴࡵ࡫ࡤࠨ৭"):
      bstack1l1l111l_opy_ = bstack11l1l1l_opy_ (u"ࠨࡲࡤࡷࡸ࡫ࡤࠨ৮") if len(threading.current_thread().bstackTestErrorMessages) == 0 else bstack11l1l1l_opy_ (u"ࠩࡩࡥ࡮ࡲࡥࡥࠩ৯")
      bstack1l1ll111l_opy_ = bstack1l1lll1l1l_opy_(bstack11l1l1l_opy_ (u"ࠪࡷࡪࡺࡓࡦࡵࡶ࡭ࡴࡴࡓࡵࡣࡷࡹࡸ࠭ৰ"), bstack11l1l1l_opy_ (u"ࠫࠬৱ"), bstack1l1l111l_opy_, bstack11l1l1l_opy_ (u"ࠬ࠲ࠠࠨ৲").join(
        threading.current_thread().bstackTestErrorMessages), bstack11l1l1l_opy_ (u"࠭ࠧ৳"), bstack11l1l1l_opy_ (u"ࠧࠨ৴"))
      if bstack1l1l111l_opy_ == bstack11l1l1l_opy_ (u"ࠨࡨࡤ࡭ࡱ࡫ࡤࠨ৵"):
        bstack1ll111111_opy_(logger)
      if self != None:
        self.execute_script(bstack1l1ll111l_opy_)
    threading.current_thread().testStatus = bstack11l1l1l_opy_ (u"ࠩࠪ৶")
  except Exception as e:
    logger.debug(bstack11l1l1l_opy_ (u"ࠥࡉࡷࡸ࡯ࡳࠢࡺ࡬࡮ࡲࡥࠡ࡯ࡤࡶࡰ࡯࡮ࡨࠢࡶࡸࡦࡺࡵࡴ࠼ࠣࠦ৷") + str(e))
  bstack1l1l1l1ll_opy_(self)
  self.session_id = None
def bstack1lll1lll1_opy_(self, command_executor=bstack11l1l1l_opy_ (u"ࠦ࡭ࡺࡴࡱ࠼࠲࠳࠶࠸࠷࠯࠲࠱࠴࠳࠷࠺࠵࠶࠷࠸ࠧ৸"), *args, **kwargs):
  bstack11l1ll11l_opy_ = bstack1l111l1l_opy_(self, command_executor, *args, **kwargs)
  try:
    from selenium.webdriver.remote.remote_connection import RemoteConnection
    if isinstance(command_executor, RemoteConnection) and bstack11l1l1l_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮࠲ࡨࡵ࡭ࠨ৹") in command_executor._url:
      bstack1lllll111l_opy_.bstack1lllll1ll_opy_(bstack11l1l1l_opy_ (u"࠭ࡢࡴࡶࡤࡧࡰࡥࡳࡦࡵࡶ࡭ࡴࡴࠧ৺"), True)
  except:
    pass
  if (isinstance(command_executor, str) and bstack11l1l1l_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠴ࡣࡰ࡯ࠪ৻") in command_executor):
    bstack1lllll111l_opy_.bstack1lllll1ll_opy_(bstack11l1l1l_opy_ (u"ࠨࡤࡶࡸࡦࡩ࡫ࡠࡵࡨࡷࡸ࡯࡯࡯ࠩৼ"), True)
  threading.current_thread().bstackSessionDriver = self
  bstack1l11l11l_opy_.bstack1ll11llll1_opy_(self)
  return bstack11l1ll11l_opy_
def bstack1l1ll1111_opy_(self, driver_command, *args, **kwargs):
  global bstack1l111l1ll_opy_
  response = bstack1l111l1ll_opy_(self, driver_command, *args, **kwargs)
  try:
    if driver_command == bstack11l1l1l_opy_ (u"ࠩࡶࡧࡷ࡫ࡥ࡯ࡵ࡫ࡳࡹ࠭৽"):
      bstack1l11l11l_opy_.bstack111l1ll1l_opy_({
          bstack11l1l1l_opy_ (u"ࠪ࡭ࡲࡧࡧࡦࠩ৾"): response[bstack11l1l1l_opy_ (u"ࠫࡻࡧ࡬ࡶࡧࠪ৿")],
          bstack11l1l1l_opy_ (u"ࠬࡺࡥࡴࡶࡢࡶࡺࡴ࡟ࡶࡷ࡬ࡨࠬ਀"): bstack1l11l11l_opy_.current_test_uuid() if bstack1l11l11l_opy_.current_test_uuid() else bstack1l11l11l_opy_.current_hook_uuid()
      })
  except:
    pass
  return response
def bstack1ll1ll1l11_opy_(self, command_executor,
             desired_capabilities=None, browser_profile=None, proxy=None,
             keep_alive=True, file_detector=None, options=None):
  global CONFIG
  global bstack1l1ll1ll1_opy_
  global bstack1llll111l_opy_
  global bstack1ll11l1ll1_opy_
  global bstack1l1l1l1l1_opy_
  global bstack1l1lll1l11_opy_
  global bstack1lllll1ll1_opy_
  global bstack1l111l1l_opy_
  global bstack11111lll1_opy_
  global bstack1lll111l_opy_
  global bstack11l11l1l_opy_
  CONFIG[bstack11l1l1l_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࡘࡊࡋࠨਁ")] = str(bstack1lllll1ll1_opy_) + str(__version__)
  command_executor = bstack1llllllll_opy_()
  logger.debug(bstack111111l11_opy_.format(command_executor))
  proxy = bstack1ll1ll11l1_opy_(CONFIG, proxy)
  bstack1111l11l1_opy_ = 0 if bstack1llll111l_opy_ < 0 else bstack1llll111l_opy_
  try:
    if bstack1l1l1l1l1_opy_ is True:
      bstack1111l11l1_opy_ = int(multiprocessing.current_process().name)
    elif bstack1l1lll1l11_opy_ is True:
      bstack1111l11l1_opy_ = int(threading.current_thread().name)
  except:
    bstack1111l11l1_opy_ = 0
  bstack1ll1lll11_opy_ = bstack1l1ll1llll_opy_(CONFIG, bstack1111l11l1_opy_)
  logger.debug(bstack1l11l1ll1_opy_.format(str(bstack1ll1lll11_opy_)))
  if bstack11l1l1l_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰࡒ࡯ࡤࡣ࡯ࠫਂ") in CONFIG and bstack1111llll_opy_(CONFIG[bstack11l1l1l_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱࡌࡰࡥࡤࡰࠬਃ")]):
    bstack11l11l11l_opy_(bstack1ll1lll11_opy_)
  if desired_capabilities:
    bstack1l11llll1_opy_ = bstack1l1ll1l1ll_opy_(desired_capabilities)
    bstack1l11llll1_opy_[bstack11l1l1l_opy_ (u"ࠩࡸࡷࡪ࡝࠳ࡄࠩ਄")] = bstack1ll111l111_opy_(CONFIG)
    bstack1111l11ll_opy_ = bstack1l1ll1llll_opy_(bstack1l11llll1_opy_)
    if bstack1111l11ll_opy_:
      bstack1ll1lll11_opy_ = update(bstack1111l11ll_opy_, bstack1ll1lll11_opy_)
    desired_capabilities = None
  if options:
    bstack1ll1l1ll_opy_(options, bstack1ll1lll11_opy_)
  if not options:
    options = bstack1ll11lllll_opy_(bstack1ll1lll11_opy_)
  bstack11l11l1l_opy_ = CONFIG.get(bstack11l1l1l_opy_ (u"ࠪࡴࡱࡧࡴࡧࡱࡵࡱࡸ࠭ਅ"))[bstack1111l11l1_opy_]
  if bstack1111ll111_opy_.bstack1lll11l11_opy_(CONFIG, bstack1111l11l1_opy_) and bstack1111ll111_opy_.bstack1l11lll1_opy_(bstack1ll1lll11_opy_, options):
    threading.current_thread().a11yPlatform = True
    bstack1111ll111_opy_.set_capabilities(bstack1ll1lll11_opy_, CONFIG)
  if proxy and bstack1llll1lll_opy_() >= version.parse(bstack11l1l1l_opy_ (u"ࠫ࠹࠴࠱࠱࠰࠳ࠫਆ")):
    options.proxy(proxy)
  if options and bstack1llll1lll_opy_() >= version.parse(bstack11l1l1l_opy_ (u"ࠬ࠹࠮࠹࠰࠳ࠫਇ")):
    desired_capabilities = None
  if (
          not options and not desired_capabilities
  ) or (
          bstack1llll1lll_opy_() < version.parse(bstack11l1l1l_opy_ (u"࠭࠳࠯࠺࠱࠴ࠬਈ")) and not desired_capabilities
  ):
    desired_capabilities = {}
    desired_capabilities.update(bstack1ll1lll11_opy_)
  logger.info(bstack1ll11ll1_opy_)
  if bstack1llll1lll_opy_() >= version.parse(bstack11l1l1l_opy_ (u"ࠧ࠵࠰࠴࠴࠳࠶ࠧਉ")):
    bstack1l111l1l_opy_(self, command_executor=command_executor,
              options=options, keep_alive=keep_alive, file_detector=file_detector)
  elif bstack1llll1lll_opy_() >= version.parse(bstack11l1l1l_opy_ (u"ࠨ࠵࠱࠼࠳࠶ࠧਊ")):
    bstack1l111l1l_opy_(self, command_executor=command_executor,
              desired_capabilities=desired_capabilities, options=options,
              browser_profile=browser_profile, proxy=proxy,
              keep_alive=keep_alive, file_detector=file_detector)
  elif bstack1llll1lll_opy_() >= version.parse(bstack11l1l1l_opy_ (u"ࠩ࠵࠲࠺࠹࠮࠱ࠩ਋")):
    bstack1l111l1l_opy_(self, command_executor=command_executor,
              desired_capabilities=desired_capabilities,
              browser_profile=browser_profile, proxy=proxy,
              keep_alive=keep_alive, file_detector=file_detector)
  else:
    bstack1l111l1l_opy_(self, command_executor=command_executor,
              desired_capabilities=desired_capabilities,
              browser_profile=browser_profile, proxy=proxy,
              keep_alive=keep_alive)
  try:
    bstack1l1llll11l_opy_ = bstack11l1l1l_opy_ (u"ࠪࠫ਌")
    if bstack1llll1lll_opy_() >= version.parse(bstack11l1l1l_opy_ (u"ࠫ࠹࠴࠰࠯࠲ࡥ࠵ࠬ਍")):
      bstack1l1llll11l_opy_ = self.caps.get(bstack11l1l1l_opy_ (u"ࠧࡵࡰࡵ࡫ࡰࡥࡱࡎࡵࡣࡗࡵࡰࠧ਎"))
    else:
      bstack1l1llll11l_opy_ = self.capabilities.get(bstack11l1l1l_opy_ (u"ࠨ࡯ࡱࡶ࡬ࡱࡦࡲࡈࡶࡤࡘࡶࡱࠨਏ"))
    if bstack1l1llll11l_opy_:
      bstack1llll1111_opy_(bstack1l1llll11l_opy_)
      if bstack1llll1lll_opy_() <= version.parse(bstack11l1l1l_opy_ (u"ࠧ࠴࠰࠴࠷࠳࠶ࠧਐ")):
        self.command_executor._url = bstack11l1l1l_opy_ (u"ࠣࡪࡷࡸࡵࡀ࠯࠰ࠤ਑") + bstack1l1ll1ll1l_opy_ + bstack11l1l1l_opy_ (u"ࠤ࠽࠼࠵࠵ࡷࡥ࠱࡫ࡹࡧࠨ਒")
      else:
        self.command_executor._url = bstack11l1l1l_opy_ (u"ࠥ࡬ࡹࡺࡰࡴ࠼࠲࠳ࠧਓ") + bstack1l1llll11l_opy_ + bstack11l1l1l_opy_ (u"ࠦ࠴ࡽࡤ࠰ࡪࡸࡦࠧਔ")
      logger.debug(bstack11ll1lll_opy_.format(bstack1l1llll11l_opy_))
    else:
      logger.debug(bstack1l1l1ll11_opy_.format(bstack11l1l1l_opy_ (u"ࠧࡕࡰࡵ࡫ࡰࡥࡱࠦࡈࡶࡤࠣࡲࡴࡺࠠࡧࡱࡸࡲࡩࠨਕ")))
  except Exception as e:
    logger.debug(bstack1l1l1ll11_opy_.format(e))
  if bstack11l1l1l_opy_ (u"࠭ࡲࡰࡤࡲࡸࠬਖ") in bstack1lllll1ll1_opy_:
    bstack111111lll_opy_(bstack1llll111l_opy_, bstack1lll111l_opy_)
  bstack1l1ll1ll1_opy_ = self.session_id
  if bstack11l1l1l_opy_ (u"ࠧࡱࡻࡷࡩࡸࡺࠧਗ") in bstack1lllll1ll1_opy_ or bstack11l1l1l_opy_ (u"ࠨࡤࡨ࡬ࡦࡼࡥࠨਘ") in bstack1lllll1ll1_opy_ or bstack11l1l1l_opy_ (u"ࠩࡵࡳࡧࡵࡴࠨਙ") in bstack1lllll1ll1_opy_:
    threading.current_thread().bstackSessionId = self.session_id
    threading.current_thread().bstackSessionDriver = self
    threading.current_thread().bstackTestErrorMessages = []
    bstack1l11l11l_opy_.bstack1ll11llll1_opy_(self)
  bstack11111lll1_opy_.append(self)
  if bstack11l1l1l_opy_ (u"ࠪࡴࡱࡧࡴࡧࡱࡵࡱࡸ࠭ਚ") in CONFIG and bstack11l1l1l_opy_ (u"ࠫࡸ࡫ࡳࡴ࡫ࡲࡲࡓࡧ࡭ࡦࠩਛ") in CONFIG[bstack11l1l1l_opy_ (u"ࠬࡶ࡬ࡢࡶࡩࡳࡷࡳࡳࠨਜ")][bstack1111l11l1_opy_]:
    bstack1ll11l1ll1_opy_ = CONFIG[bstack11l1l1l_opy_ (u"࠭ࡰ࡭ࡣࡷࡪࡴࡸ࡭ࡴࠩਝ")][bstack1111l11l1_opy_][bstack11l1l1l_opy_ (u"ࠧࡴࡧࡶࡷ࡮ࡵ࡮ࡏࡣࡰࡩࠬਞ")]
  logger.debug(bstack1lll11ll_opy_.format(bstack1l1ll1ll1_opy_))
try:
  try:
    import Browser
    from subprocess import Popen
    def bstack1llll111_opy_(self, args, bufsize=-1, executable=None,
              stdin=None, stdout=None, stderr=None,
              preexec_fn=None, close_fds=True,
              shell=False, cwd=None, env=None, universal_newlines=None,
              startupinfo=None, creationflags=0,
              restore_signals=True, start_new_session=False,
              pass_fds=(), *, user=None, group=None, extra_groups=None,
              encoding=None, errors=None, text=None, umask=-1, pipesize=-1):
      global CONFIG
      global bstack1l1l1llll_opy_
      if(bstack11l1l1l_opy_ (u"ࠣ࡫ࡱࡨࡪࡾ࠮࡫ࡵࠥਟ") in args[1]):
        with open(os.path.join(os.path.expanduser(bstack11l1l1l_opy_ (u"ࠩࢁࠫਠ")), bstack11l1l1l_opy_ (u"ࠪ࠲ࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࠪਡ"), bstack11l1l1l_opy_ (u"ࠫ࠳ࡹࡥࡴࡵ࡬ࡳࡳ࡯ࡤࡴ࠰ࡷࡼࡹ࠭ਢ")), bstack11l1l1l_opy_ (u"ࠬࡽࠧਣ")) as fp:
          fp.write(bstack11l1l1l_opy_ (u"ࠨࠢਤ"))
        if(not os.path.exists(os.path.join(os.path.dirname(args[1]), bstack11l1l1l_opy_ (u"ࠢࡪࡰࡧࡩࡽࡥࡢࡴࡶࡤࡧࡰ࠴ࡪࡴࠤਥ")))):
          with open(args[1], bstack11l1l1l_opy_ (u"ࠨࡴࠪਦ")) as f:
            lines = f.readlines()
            index = next((i for i, line in enumerate(lines) if bstack11l1l1l_opy_ (u"ࠩࡤࡷࡾࡴࡣࠡࡨࡸࡲࡨࡺࡩࡰࡰࠣࡣࡳ࡫ࡷࡑࡣࡪࡩ࠭ࡩ࡯࡯ࡶࡨࡼࡹ࠲ࠠࡱࡣࡪࡩࠥࡃࠠࡷࡱ࡬ࡨࠥ࠶ࠩࠨਧ") in line), None)
            if index is not None:
                lines.insert(index+2, bstack1llll1l1_opy_)
            lines.insert(1, bstack1llll1ll1l_opy_)
            f.seek(0)
            with open(os.path.join(os.path.dirname(args[1]), bstack11l1l1l_opy_ (u"ࠥ࡭ࡳࡪࡥࡹࡡࡥࡷࡹࡧࡣ࡬࠰࡭ࡷࠧਨ")), bstack11l1l1l_opy_ (u"ࠫࡼ࠭਩")) as bstack1l1ll1ll_opy_:
              bstack1l1ll1ll_opy_.writelines(lines)
        CONFIG[bstack11l1l1l_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࡗࡉࡑࠧਪ")] = str(bstack1lllll1ll1_opy_) + str(__version__)
        bstack1111l11l1_opy_ = 0 if bstack1llll111l_opy_ < 0 else bstack1llll111l_opy_
        try:
          if bstack1l1l1l1l1_opy_ is True:
            bstack1111l11l1_opy_ = int(multiprocessing.current_process().name)
          elif bstack1l1lll1l11_opy_ is True:
            bstack1111l11l1_opy_ = int(threading.current_thread().name)
        except:
          bstack1111l11l1_opy_ = 0
        CONFIG[bstack11l1l1l_opy_ (u"ࠨࡵࡴࡧ࡚࠷ࡈࠨਫ")] = False
        CONFIG[bstack11l1l1l_opy_ (u"ࠢࡪࡵࡓࡰࡦࡿࡷࡳ࡫ࡪ࡬ࡹࠨਬ")] = True
        bstack1ll1lll11_opy_ = bstack1l1ll1llll_opy_(CONFIG, bstack1111l11l1_opy_)
        logger.debug(bstack1l11l1ll1_opy_.format(str(bstack1ll1lll11_opy_)))
        if CONFIG.get(bstack11l1l1l_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱࡌࡰࡥࡤࡰࠬਭ")):
          bstack11l11l11l_opy_(bstack1ll1lll11_opy_)
        if bstack11l1l1l_opy_ (u"ࠩࡳࡰࡦࡺࡦࡰࡴࡰࡷࠬਮ") in CONFIG and bstack11l1l1l_opy_ (u"ࠪࡷࡪࡹࡳࡪࡱࡱࡒࡦࡳࡥࠨਯ") in CONFIG[bstack11l1l1l_opy_ (u"ࠫࡵࡲࡡࡵࡨࡲࡶࡲࡹࠧਰ")][bstack1111l11l1_opy_]:
          bstack1ll11l1ll1_opy_ = CONFIG[bstack11l1l1l_opy_ (u"ࠬࡶ࡬ࡢࡶࡩࡳࡷࡳࡳࠨ਱")][bstack1111l11l1_opy_][bstack11l1l1l_opy_ (u"࠭ࡳࡦࡵࡶ࡭ࡴࡴࡎࡢ࡯ࡨࠫਲ")]
        args.append(os.path.join(os.path.expanduser(bstack11l1l1l_opy_ (u"ࠧࡿࠩਲ਼")), bstack11l1l1l_opy_ (u"ࠨ࠰ࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࠨ਴"), bstack11l1l1l_opy_ (u"ࠩ࠱ࡷࡪࡹࡳࡪࡱࡱ࡭ࡩࡹ࠮ࡵࡺࡷࠫਵ")))
        args.append(str(threading.get_ident()))
        args.append(json.dumps(bstack1ll1lll11_opy_))
        args[1] = os.path.join(os.path.dirname(args[1]), bstack11l1l1l_opy_ (u"ࠥ࡭ࡳࡪࡥࡹࡡࡥࡷࡹࡧࡣ࡬࠰࡭ࡷࠧਸ਼"))
      bstack1l1l1llll_opy_ = True
      return bstack1lll111l1_opy_(self, args, bufsize=bufsize, executable=executable,
                    stdin=stdin, stdout=stdout, stderr=stderr,
                    preexec_fn=preexec_fn, close_fds=close_fds,
                    shell=shell, cwd=cwd, env=env, universal_newlines=universal_newlines,
                    startupinfo=startupinfo, creationflags=creationflags,
                    restore_signals=restore_signals, start_new_session=start_new_session,
                    pass_fds=pass_fds, user=user, group=group, extra_groups=extra_groups,
                    encoding=encoding, errors=errors, text=text, umask=umask, pipesize=pipesize)
  except Exception as e:
    pass
  import playwright._impl._api_structures
  import playwright._impl._helper
  def bstack111ll1lll_opy_(self,
        executablePath = None,
        channel = None,
        args = None,
        ignoreDefaultArgs = None,
        handleSIGINT = None,
        handleSIGTERM = None,
        handleSIGHUP = None,
        timeout = None,
        env = None,
        headless = None,
        devtools = None,
        proxy = None,
        downloadsPath = None,
        slowMo = None,
        tracesDir = None,
        chromiumSandbox = None,
        firefoxUserPrefs = None
        ):
    global CONFIG
    global bstack1llll111l_opy_
    global bstack1ll11l1ll1_opy_
    global bstack1l1l1l1l1_opy_
    global bstack1l1lll1l11_opy_
    global bstack1lllll1ll1_opy_
    CONFIG[bstack11l1l1l_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࡖࡈࡐ࠭਷")] = str(bstack1lllll1ll1_opy_) + str(__version__)
    bstack1111l11l1_opy_ = 0 if bstack1llll111l_opy_ < 0 else bstack1llll111l_opy_
    try:
      if bstack1l1l1l1l1_opy_ is True:
        bstack1111l11l1_opy_ = int(multiprocessing.current_process().name)
      elif bstack1l1lll1l11_opy_ is True:
        bstack1111l11l1_opy_ = int(threading.current_thread().name)
    except:
      bstack1111l11l1_opy_ = 0
    CONFIG[bstack11l1l1l_opy_ (u"ࠧ࡯ࡳࡑ࡮ࡤࡽࡼࡸࡩࡨࡪࡷࠦਸ")] = True
    bstack1ll1lll11_opy_ = bstack1l1ll1llll_opy_(CONFIG, bstack1111l11l1_opy_)
    logger.debug(bstack1l11l1ll1_opy_.format(str(bstack1ll1lll11_opy_)))
    if CONFIG.get(bstack11l1l1l_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࡑࡵࡣࡢ࡮ࠪਹ")):
      bstack11l11l11l_opy_(bstack1ll1lll11_opy_)
    if bstack11l1l1l_opy_ (u"ࠧࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࡵࠪ਺") in CONFIG and bstack11l1l1l_opy_ (u"ࠨࡵࡨࡷࡸ࡯࡯࡯ࡐࡤࡱࡪ࠭਻") in CONFIG[bstack11l1l1l_opy_ (u"ࠩࡳࡰࡦࡺࡦࡰࡴࡰࡷ਼ࠬ")][bstack1111l11l1_opy_]:
      bstack1ll11l1ll1_opy_ = CONFIG[bstack11l1l1l_opy_ (u"ࠪࡴࡱࡧࡴࡧࡱࡵࡱࡸ࠭਽")][bstack1111l11l1_opy_][bstack11l1l1l_opy_ (u"ࠫࡸ࡫ࡳࡴ࡫ࡲࡲࡓࡧ࡭ࡦࠩਾ")]
    import urllib
    import json
    bstack1ll111l1_opy_ = bstack11l1l1l_opy_ (u"ࠬࡽࡳࡴ࠼࠲࠳ࡨࡪࡰ࠯ࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠮ࡤࡱࡰ࠳ࡵࡲࡡࡺࡹࡵ࡭࡬࡮ࡴࡀࡥࡤࡴࡸࡃࠧਿ") + urllib.parse.quote(json.dumps(bstack1ll1lll11_opy_))
    browser = self.connect(bstack1ll111l1_opy_)
    return browser
except Exception as e:
    pass
def bstack1lll111ll_opy_():
    global bstack1l1l1llll_opy_
    try:
        from playwright._impl._browser_type import BrowserType
        BrowserType.launch = bstack111ll1lll_opy_
        bstack1l1l1llll_opy_ = True
    except Exception as e:
        pass
    try:
      import Browser
      from subprocess import Popen
      Popen.__init__ = bstack1llll111_opy_
      bstack1l1l1llll_opy_ = True
    except Exception as e:
      pass
def bstack11111111l_opy_(context, bstack1lll11llll_opy_):
  try:
    context.page.evaluate(bstack11l1l1l_opy_ (u"ࠨ࡟ࠡ࠿ࡁࠤࢀࢃࠢੀ"), bstack11l1l1l_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰࡥࡥࡹࡧࡦࡹࡹࡵࡲ࠻ࠢࡾࠦࡦࡩࡴࡪࡱࡱࠦ࠿ࠦࠢࡴࡧࡷࡗࡪࡹࡳࡪࡱࡱࡒࡦࡳࡥࠣ࠮ࠣࠦࡦࡸࡧࡶ࡯ࡨࡲࡹࡹࠢ࠻ࠢࡾࠦࡳࡧ࡭ࡦࠤ࠽ࠫੁ")+ json.dumps(bstack1lll11llll_opy_) + bstack11l1l1l_opy_ (u"ࠣࡿࢀࠦੂ"))
  except Exception as e:
    logger.debug(bstack11l1l1l_opy_ (u"ࠤࡨࡼࡨ࡫ࡰࡵ࡫ࡲࡲࠥ࡯࡮ࠡࡲ࡯ࡥࡾࡽࡲࡪࡩ࡫ࡸࠥࡹࡥࡴࡵ࡬ࡳࡳࠦ࡮ࡢ࡯ࡨࠤࢀࢃࠢ੃"), e)
def bstack1111l1lll_opy_(context, message, level):
  try:
    context.page.evaluate(bstack11l1l1l_opy_ (u"ࠥࡣࠥࡃ࠾ࠡࡽࢀࠦ੄"), bstack11l1l1l_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࡢࡩࡽ࡫ࡣࡶࡶࡲࡶ࠿ࠦࡻࠣࡣࡦࡸ࡮ࡵ࡮ࠣ࠼ࠣࠦࡦࡴ࡮ࡰࡶࡤࡸࡪࠨࠬࠡࠤࡤࡶ࡬ࡻ࡭ࡦࡰࡷࡷࠧࡀࠠࡼࠤࡧࡥࡹࡧࠢ࠻ࠩ੅") + json.dumps(message) + bstack11l1l1l_opy_ (u"ࠬ࠲ࠢ࡭ࡧࡹࡩࡱࠨ࠺ࠨ੆") + json.dumps(level) + bstack11l1l1l_opy_ (u"࠭ࡽࡾࠩੇ"))
  except Exception as e:
    logger.debug(bstack11l1l1l_opy_ (u"ࠢࡦࡺࡦࡩࡵࡺࡩࡰࡰࠣ࡭ࡳࠦࡰ࡭ࡣࡼࡻࡷ࡯ࡧࡩࡶࠣࡥࡳࡴ࡯ࡵࡣࡷ࡭ࡴࡴࠠࡼࡿࠥੈ"), e)
def bstack1l11l1l1l_opy_(context, status, message = bstack11l1l1l_opy_ (u"ࠣࠤ੉")):
  try:
    if(status == bstack11l1l1l_opy_ (u"ࠤࡩࡥ࡮ࡲࡥࡥࠤ੊")):
      context.page.evaluate(bstack11l1l1l_opy_ (u"ࠥࡣࠥࡃ࠾ࠡࡽࢀࠦੋ"), bstack11l1l1l_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࡢࡩࡽ࡫ࡣࡶࡶࡲࡶ࠿ࠦࡻࠣࡣࡦࡸ࡮ࡵ࡮ࠣ࠼ࠣࠦࡸ࡫ࡴࡔࡧࡶࡷ࡮ࡵ࡮ࡔࡶࡤࡸࡺࡹࠢ࠭ࠢࠥࡥࡷ࡭ࡵ࡮ࡧࡱࡸࡸࠨ࠺ࠡࡽࠥࡶࡪࡧࡳࡰࡰࠥ࠾ࠬੌ") + json.dumps(bstack11l1l1l_opy_ (u"࡙ࠧࡣࡦࡰࡤࡶ࡮ࡵࠠࡧࡣ࡬ࡰࡪࡪࠠࡸ࡫ࡷ࡬࠿੍ࠦࠢ") + str(message)) + bstack11l1l1l_opy_ (u"࠭ࠬࠣࡵࡷࡥࡹࡻࡳࠣ࠼ࠪ੎") + json.dumps(status) + bstack11l1l1l_opy_ (u"ࠢࡾࡿࠥ੏"))
    else:
      context.page.evaluate(bstack11l1l1l_opy_ (u"ࠣࡡࠣࡁࡃࠦࡻࡾࠤ੐"), bstack11l1l1l_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࡠࡧࡻࡩࡨࡻࡴࡰࡴ࠽ࠤࢀࠨࡡࡤࡶ࡬ࡳࡳࠨ࠺ࠡࠤࡶࡩࡹ࡙ࡥࡴࡵ࡬ࡳࡳ࡙ࡴࡢࡶࡸࡷࠧ࠲ࠠࠣࡣࡵ࡫ࡺࡳࡥ࡯ࡶࡶࠦ࠿ࠦࡻࠣࡵࡷࡥࡹࡻࡳࠣ࠼ࠪੑ") + json.dumps(status) + bstack11l1l1l_opy_ (u"ࠥࢁࢂࠨ੒"))
  except Exception as e:
    logger.debug(bstack11l1l1l_opy_ (u"ࠦࡪࡾࡣࡦࡲࡷ࡭ࡴࡴࠠࡪࡰࠣࡴࡱࡧࡹࡸࡴ࡬࡫࡭ࡺࠠࡴࡧࡷࠤࡸ࡫ࡳࡴ࡫ࡲࡲࠥࡹࡴࡢࡶࡸࡷࠥࢁࡽࠣ੓"), e)
def bstack11l1ll11_opy_(self, url):
  global bstack1l11l1l11_opy_
  try:
    bstack1l1lll1lll_opy_(url)
  except Exception as err:
    logger.debug(bstack111lll11_opy_.format(str(err)))
  try:
    bstack1l11l1l11_opy_(self, url)
  except Exception as e:
    try:
      bstack1ll1111lll_opy_ = str(e)
      if any(err_msg in bstack1ll1111lll_opy_ for err_msg in bstack1ll1ll11ll_opy_):
        bstack1l1lll1lll_opy_(url, True)
    except Exception as err:
      logger.debug(bstack111lll11_opy_.format(str(err)))
    raise e
def bstack111llll1l_opy_(self):
  global bstack1llll111l1_opy_
  bstack1llll111l1_opy_ = self
  return
def bstack11l1lll1_opy_(self):
  global bstack11ll11ll1_opy_
  bstack11ll11ll1_opy_ = self
  return
def bstack11l11l11_opy_(self, test):
  global CONFIG
  global bstack11ll11ll1_opy_
  global bstack1llll111l1_opy_
  global bstack1l1ll1ll1_opy_
  global bstack11ll11ll_opy_
  global bstack1ll11l1ll1_opy_
  global bstack1l11lll11_opy_
  global bstack1l1l1l11l_opy_
  global bstack1ll1ll111_opy_
  global bstack11111lll1_opy_
  global bstack11l11l1l_opy_
  try:
    if not bstack1l1ll1ll1_opy_:
      with open(os.path.join(os.path.expanduser(bstack11l1l1l_opy_ (u"ࠬࢄࠧ੔")), bstack11l1l1l_opy_ (u"࠭࠮ࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠭੕"), bstack11l1l1l_opy_ (u"ࠧ࠯ࡵࡨࡷࡸ࡯࡯࡯࡫ࡧࡷ࠳ࡺࡸࡵࠩ੖"))) as f:
        bstack111l1ll1_opy_ = json.loads(bstack11l1l1l_opy_ (u"ࠣࡽࠥ੗") + f.read().strip() + bstack11l1l1l_opy_ (u"ࠩࠥࡼࠧࡀࠠࠣࡻࠥࠫ੘") + bstack11l1l1l_opy_ (u"ࠥࢁࠧਖ਼"))
        bstack1l1ll1ll1_opy_ = bstack111l1ll1_opy_[str(threading.get_ident())]
  except:
    pass
  if bstack11111lll1_opy_:
    for driver in bstack11111lll1_opy_:
      if bstack1l1ll1ll1_opy_ == driver.session_id:
        if test:
          bstack11ll11lll_opy_ = str(test.data)
          if bstack1111l11l_opy_(threading.current_thread(), bstack11l1l1l_opy_ (u"ࠫ࡮ࡹࡁ࠲࠳ࡼࡘࡪࡹࡴࠨਗ਼"), None) and bstack1111l11l_opy_(threading.current_thread(), bstack11l1l1l_opy_ (u"ࠬࡧ࠱࠲ࡻࡓࡰࡦࡺࡦࡰࡴࡰࠫਜ਼"), None):
            logger.info(bstack11l1l1l_opy_ (u"ࠨࡁࡶࡶࡲࡱࡦࡺࡥࠡࡶࡨࡷࡹࠦࡣࡢࡵࡨࠤࡪࡾࡥࡤࡷࡷ࡭ࡴࡴࠠࡩࡣࡶࠤࡪࡴࡤࡦࡦ࠱ࠤࡕࡸ࡯ࡤࡧࡶࡷ࡮ࡴࡧࠡࡨࡲࡶࠥࡧࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽࠥࡺࡥࡴࡶ࡬ࡲ࡬ࠦࡩࡴࠢࡸࡲࡩ࡫ࡲࡸࡣࡼ࠲ࠥࠨੜ"))
            bstack1111ll111_opy_.bstack11l11lll1_opy_(driver, class_name=test.parent.name, name=test.name, module_name=None, path=test.source, bstack1l1lll1111_opy_=bstack11l11l1l_opy_)
        if not bstack111ll11l_opy_ and bstack11ll11lll_opy_:
          bstack11l11111_opy_ = {
            bstack11l1l1l_opy_ (u"ࠧࡢࡥࡷ࡭ࡴࡴࠧ੝"): bstack11l1l1l_opy_ (u"ࠨࡵࡨࡸࡘ࡫ࡳࡴ࡫ࡲࡲࡓࡧ࡭ࡦࠩਫ਼"),
            bstack11l1l1l_opy_ (u"ࠩࡤࡶ࡬ࡻ࡭ࡦࡰࡷࡷࠬ੟"): {
              bstack11l1l1l_opy_ (u"ࠪࡲࡦࡳࡥࠨ੠"): bstack11ll11lll_opy_
            }
          }
          bstack111lll11l_opy_ = bstack11l1l1l_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࡢࡩࡽ࡫ࡣࡶࡶࡲࡶ࠿ࠦࡻࡾࠩ੡").format(json.dumps(bstack11l11111_opy_))
          driver.execute_script(bstack111lll11l_opy_)
        if bstack11ll11ll_opy_:
          bstack1ll11llll_opy_ = {
            bstack11l1l1l_opy_ (u"ࠬࡧࡣࡵ࡫ࡲࡲࠬ੢"): bstack11l1l1l_opy_ (u"࠭ࡡ࡯ࡰࡲࡸࡦࡺࡥࠨ੣"),
            bstack11l1l1l_opy_ (u"ࠧࡢࡴࡪࡹࡲ࡫࡮ࡵࡵࠪ੤"): {
              bstack11l1l1l_opy_ (u"ࠨࡦࡤࡸࡦ࠭੥"): bstack11ll11lll_opy_ + bstack11l1l1l_opy_ (u"ࠩࠣࡴࡦࡹࡳࡦࡦࠤࠫ੦"),
              bstack11l1l1l_opy_ (u"ࠪࡰࡪࡼࡥ࡭ࠩ੧"): bstack11l1l1l_opy_ (u"ࠫ࡮ࡴࡦࡰࠩ੨")
            }
          }
          bstack11l11111_opy_ = {
            bstack11l1l1l_opy_ (u"ࠬࡧࡣࡵ࡫ࡲࡲࠬ੩"): bstack11l1l1l_opy_ (u"࠭ࡳࡦࡶࡖࡩࡸࡹࡩࡰࡰࡖࡸࡦࡺࡵࡴࠩ੪"),
            bstack11l1l1l_opy_ (u"ࠧࡢࡴࡪࡹࡲ࡫࡮ࡵࡵࠪ੫"): {
              bstack11l1l1l_opy_ (u"ࠨࡵࡷࡥࡹࡻࡳࠨ੬"): bstack11l1l1l_opy_ (u"ࠩࡳࡥࡸࡹࡥࡥࠩ੭")
            }
          }
          if bstack11ll11ll_opy_.status == bstack11l1l1l_opy_ (u"ࠪࡔࡆ࡙ࡓࠨ੮"):
            bstack11l111ll1_opy_ = bstack11l1l1l_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࡢࡩࡽ࡫ࡣࡶࡶࡲࡶ࠿ࠦࡻࡾࠩ੯").format(json.dumps(bstack1ll11llll_opy_))
            driver.execute_script(bstack11l111ll1_opy_)
            bstack111lll11l_opy_ = bstack11l1l1l_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࡣࡪࡾࡥࡤࡷࡷࡳࡷࡀࠠࡼࡿࠪੰ").format(json.dumps(bstack11l11111_opy_))
            driver.execute_script(bstack111lll11l_opy_)
          elif bstack11ll11ll_opy_.status == bstack11l1l1l_opy_ (u"࠭ࡆࡂࡋࡏࠫੱ"):
            reason = bstack11l1l1l_opy_ (u"ࠢࠣੲ")
            bstack111l11ll_opy_ = bstack11ll11lll_opy_ + bstack11l1l1l_opy_ (u"ࠨࠢࡩࡥ࡮ࡲࡥࡥࠩੳ")
            if bstack11ll11ll_opy_.message:
              reason = str(bstack11ll11ll_opy_.message)
              bstack111l11ll_opy_ = bstack111l11ll_opy_ + bstack11l1l1l_opy_ (u"ࠩࠣࡻ࡮ࡺࡨࠡࡧࡵࡶࡴࡸ࠺ࠡࠩੴ") + reason
            bstack1ll11llll_opy_[bstack11l1l1l_opy_ (u"ࠪࡥࡷ࡭ࡵ࡮ࡧࡱࡸࡸ࠭ੵ")] = {
              bstack11l1l1l_opy_ (u"ࠫࡱ࡫ࡶࡦ࡮ࠪ੶"): bstack11l1l1l_opy_ (u"ࠬ࡫ࡲࡳࡱࡵࠫ੷"),
              bstack11l1l1l_opy_ (u"࠭ࡤࡢࡶࡤࠫ੸"): bstack111l11ll_opy_
            }
            bstack11l11111_opy_[bstack11l1l1l_opy_ (u"ࠧࡢࡴࡪࡹࡲ࡫࡮ࡵࡵࠪ੹")] = {
              bstack11l1l1l_opy_ (u"ࠨࡵࡷࡥࡹࡻࡳࠨ੺"): bstack11l1l1l_opy_ (u"ࠩࡩࡥ࡮ࡲࡥࡥࠩ੻"),
              bstack11l1l1l_opy_ (u"ࠪࡶࡪࡧࡳࡰࡰࠪ੼"): reason
            }
            bstack11l111ll1_opy_ = bstack11l1l1l_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࡢࡩࡽ࡫ࡣࡶࡶࡲࡶ࠿ࠦࡻࡾࠩ੽").format(json.dumps(bstack1ll11llll_opy_))
            driver.execute_script(bstack11l111ll1_opy_)
            bstack111lll11l_opy_ = bstack11l1l1l_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࡣࡪࡾࡥࡤࡷࡷࡳࡷࡀࠠࡼࡿࠪ੾").format(json.dumps(bstack11l11111_opy_))
            driver.execute_script(bstack111lll11l_opy_)
            bstack1llll1l1ll_opy_(reason, str(bstack11ll11ll_opy_), str(bstack1llll111l_opy_), logger)
  elif bstack1l1ll1ll1_opy_:
    try:
      data = {}
      bstack11ll11lll_opy_ = None
      if test:
        bstack11ll11lll_opy_ = str(test.data)
      if not bstack111ll11l_opy_ and bstack11ll11lll_opy_:
        data[bstack11l1l1l_opy_ (u"࠭࡮ࡢ࡯ࡨࠫ੿")] = bstack11ll11lll_opy_
      if bstack11ll11ll_opy_:
        if bstack11ll11ll_opy_.status == bstack11l1l1l_opy_ (u"ࠧࡑࡃࡖࡗࠬ઀"):
          data[bstack11l1l1l_opy_ (u"ࠨࡵࡷࡥࡹࡻࡳࠨઁ")] = bstack11l1l1l_opy_ (u"ࠩࡳࡥࡸࡹࡥࡥࠩં")
        elif bstack11ll11ll_opy_.status == bstack11l1l1l_opy_ (u"ࠪࡊࡆࡏࡌࠨઃ"):
          data[bstack11l1l1l_opy_ (u"ࠫࡸࡺࡡࡵࡷࡶࠫ઄")] = bstack11l1l1l_opy_ (u"ࠬ࡬ࡡࡪ࡮ࡨࡨࠬઅ")
          if bstack11ll11ll_opy_.message:
            data[bstack11l1l1l_opy_ (u"࠭ࡲࡦࡣࡶࡳࡳ࠭આ")] = str(bstack11ll11ll_opy_.message)
      user = CONFIG[bstack11l1l1l_opy_ (u"ࠧࡶࡵࡨࡶࡓࡧ࡭ࡦࠩઇ")]
      key = CONFIG[bstack11l1l1l_opy_ (u"ࠨࡣࡦࡧࡪࡹࡳࡌࡧࡼࠫઈ")]
      url = bstack11l1l1l_opy_ (u"ࠩ࡫ࡸࡹࡶࡳ࠻࠱࠲ࡿࢂࡀࡻࡾࡂࡤࡴ࡮࠴ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯࠳ࡩ࡯࡮࠱ࡤࡹࡹࡵ࡭ࡢࡶࡨ࠳ࡸ࡫ࡳࡴ࡫ࡲࡲࡸ࠵ࡻࡾ࠰࡭ࡷࡴࡴࠧઉ").format(user, key, bstack1l1ll1ll1_opy_)
      headers = {
        bstack11l1l1l_opy_ (u"ࠪࡇࡴࡴࡴࡦࡰࡷ࠱ࡹࡿࡰࡦࠩઊ"): bstack11l1l1l_opy_ (u"ࠫࡦࡶࡰ࡭࡫ࡦࡥࡹ࡯࡯࡯࠱࡭ࡷࡴࡴࠧઋ"),
      }
      if bool(data):
        requests.put(url, json=data, headers=headers)
    except Exception as e:
      logger.error(bstack111l11ll1_opy_.format(str(e)))
  if bstack11ll11ll1_opy_:
    bstack1l1l1l11l_opy_(bstack11ll11ll1_opy_)
  if bstack1llll111l1_opy_:
    bstack1ll1ll111_opy_(bstack1llll111l1_opy_)
  bstack1l11lll11_opy_(self, test)
def bstack1111l1l11_opy_(self, parent, test, skip_on_failure=None, rpa=False):
  global bstack1l11111ll_opy_
  global CONFIG
  global bstack11111lll1_opy_
  global bstack1l1ll1ll1_opy_
  bstack1l1lll1l1_opy_ = None
  try:
    if bstack1111l11l_opy_(threading.current_thread(), bstack11l1l1l_opy_ (u"ࠬࡧ࠱࠲ࡻࡓࡰࡦࡺࡦࡰࡴࡰࠫઌ"), None):
      try:
        if not bstack1l1ll1ll1_opy_:
          with open(os.path.join(os.path.expanduser(bstack11l1l1l_opy_ (u"࠭ࡾࠨઍ")), bstack11l1l1l_opy_ (u"ࠧ࠯ࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱࠧ઎"), bstack11l1l1l_opy_ (u"ࠨ࠰ࡶࡩࡸࡹࡩࡰࡰ࡬ࡨࡸ࠴ࡴࡹࡶࠪએ"))) as f:
            bstack111l1ll1_opy_ = json.loads(bstack11l1l1l_opy_ (u"ࠤࡾࠦઐ") + f.read().strip() + bstack11l1l1l_opy_ (u"ࠪࠦࡽࠨ࠺ࠡࠤࡼࠦࠬઑ") + bstack11l1l1l_opy_ (u"ࠦࢂࠨ઒"))
            bstack1l1ll1ll1_opy_ = bstack111l1ll1_opy_[str(threading.get_ident())]
      except:
        pass
      if bstack11111lll1_opy_:
        for driver in bstack11111lll1_opy_:
          if bstack1l1ll1ll1_opy_ == driver.session_id:
            bstack1l1lll1l1_opy_ = driver
    bstack1lll1l1ll1_opy_ = bstack1111ll111_opy_.bstack1l1lllll_opy_(CONFIG, test.tags)
    if bstack1l1lll1l1_opy_:
      threading.current_thread().isA11yTest = bstack1111ll111_opy_.bstack1l1llll111_opy_(bstack1l1lll1l1_opy_, bstack1lll1l1ll1_opy_)
    else:
      threading.current_thread().isA11yTest = bstack1lll1l1ll1_opy_
  except:
    pass
  bstack1l11111ll_opy_(self, parent, test, skip_on_failure=skip_on_failure, rpa=rpa)
  global bstack11ll11ll_opy_
  bstack11ll11ll_opy_ = self._test
def bstack1llll1l111_opy_():
  global bstack1lll11l1_opy_
  try:
    if os.path.exists(bstack1lll11l1_opy_):
      os.remove(bstack1lll11l1_opy_)
  except Exception as e:
    logger.debug(bstack11l1l1l_opy_ (u"ࠬࡋࡲࡳࡱࡵࠤ࡮ࡴࠠࡥࡧ࡯ࡩࡹ࡯࡮ࡨࠢࡵࡳࡧࡵࡴࠡࡴࡨࡴࡴࡸࡴࠡࡨ࡬ࡰࡪࡀࠠࠨઓ") + str(e))
def bstack1ll1ll1l1l_opy_():
  global bstack1lll11l1_opy_
  bstack1ll1llll1l_opy_ = {}
  try:
    if not os.path.isfile(bstack1lll11l1_opy_):
      with open(bstack1lll11l1_opy_, bstack11l1l1l_opy_ (u"࠭ࡷࠨઔ")):
        pass
      with open(bstack1lll11l1_opy_, bstack11l1l1l_opy_ (u"ࠢࡸ࠭ࠥક")) as outfile:
        json.dump({}, outfile)
    if os.path.exists(bstack1lll11l1_opy_):
      bstack1ll1llll1l_opy_ = json.load(open(bstack1lll11l1_opy_, bstack11l1l1l_opy_ (u"ࠨࡴࡥࠫખ")))
  except Exception as e:
    logger.debug(bstack11l1l1l_opy_ (u"ࠩࡈࡶࡷࡵࡲࠡ࡫ࡱࠤࡷ࡫ࡡࡥ࡫ࡱ࡫ࠥࡸ࡯ࡣࡱࡷࠤࡷ࡫ࡰࡰࡴࡷࠤ࡫࡯࡬ࡦ࠼ࠣࠫગ") + str(e))
  finally:
    return bstack1ll1llll1l_opy_
def bstack111111lll_opy_(platform_index, item_index):
  global bstack1lll11l1_opy_
  try:
    bstack1ll1llll1l_opy_ = bstack1ll1ll1l1l_opy_()
    bstack1ll1llll1l_opy_[item_index] = platform_index
    with open(bstack1lll11l1_opy_, bstack11l1l1l_opy_ (u"ࠥࡻ࠰ࠨઘ")) as outfile:
      json.dump(bstack1ll1llll1l_opy_, outfile)
  except Exception as e:
    logger.debug(bstack11l1l1l_opy_ (u"ࠫࡊࡸࡲࡰࡴࠣ࡭ࡳࠦࡷࡳ࡫ࡷ࡭ࡳ࡭ࠠࡵࡱࠣࡶࡴࡨ࡯ࡵࠢࡵࡩࡵࡵࡲࡵࠢࡩ࡭ࡱ࡫࠺ࠡࠩઙ") + str(e))
def bstack11l1l11ll_opy_(bstack1l11l1111_opy_):
  global CONFIG
  bstack1lll11111_opy_ = bstack11l1l1l_opy_ (u"ࠬ࠭ચ")
  if not bstack11l1l1l_opy_ (u"࠭ࡰ࡭ࡣࡷࡪࡴࡸ࡭ࡴࠩછ") in CONFIG:
    logger.info(bstack11l1l1l_opy_ (u"ࠧࡏࡱࠣࡴࡱࡧࡴࡧࡱࡵࡱࡸࠦࡰࡢࡵࡶࡩࡩࠦࡵ࡯ࡣࡥࡰࡪࠦࡴࡰࠢࡪࡩࡳ࡫ࡲࡢࡶࡨࠤࡷ࡫ࡰࡰࡴࡷࠤ࡫ࡵࡲࠡࡔࡲࡦࡴࡺࠠࡳࡷࡱࠫજ"))
  try:
    platform = CONFIG[bstack11l1l1l_opy_ (u"ࠨࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࡶࠫઝ")][bstack1l11l1111_opy_]
    if bstack11l1l1l_opy_ (u"ࠩࡲࡷࠬઞ") in platform:
      bstack1lll11111_opy_ += str(platform[bstack11l1l1l_opy_ (u"ࠪࡳࡸ࠭ટ")]) + bstack11l1l1l_opy_ (u"ࠫ࠱ࠦࠧઠ")
    if bstack11l1l1l_opy_ (u"ࠬࡵࡳࡗࡧࡵࡷ࡮ࡵ࡮ࠨડ") in platform:
      bstack1lll11111_opy_ += str(platform[bstack11l1l1l_opy_ (u"࠭࡯ࡴࡘࡨࡶࡸ࡯࡯࡯ࠩઢ")]) + bstack11l1l1l_opy_ (u"ࠧ࠭ࠢࠪણ")
    if bstack11l1l1l_opy_ (u"ࠨࡦࡨࡺ࡮ࡩࡥࡏࡣࡰࡩࠬત") in platform:
      bstack1lll11111_opy_ += str(platform[bstack11l1l1l_opy_ (u"ࠩࡧࡩࡻ࡯ࡣࡦࡐࡤࡱࡪ࠭થ")]) + bstack11l1l1l_opy_ (u"ࠪ࠰ࠥ࠭દ")
    if bstack11l1l1l_opy_ (u"ࠫࡵࡲࡡࡵࡨࡲࡶࡲ࡜ࡥࡳࡵ࡬ࡳࡳ࠭ધ") in platform:
      bstack1lll11111_opy_ += str(platform[bstack11l1l1l_opy_ (u"ࠬࡶ࡬ࡢࡶࡩࡳࡷࡳࡖࡦࡴࡶ࡭ࡴࡴࠧન")]) + bstack11l1l1l_opy_ (u"࠭ࠬࠡࠩ઩")
    if bstack11l1l1l_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡏࡣࡰࡩࠬપ") in platform:
      bstack1lll11111_opy_ += str(platform[bstack11l1l1l_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡐࡤࡱࡪ࠭ફ")]) + bstack11l1l1l_opy_ (u"ࠩ࠯ࠤࠬબ")
    if bstack11l1l1l_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵ࡚ࡪࡸࡳࡪࡱࡱࠫભ") in platform:
      bstack1lll11111_opy_ += str(platform[bstack11l1l1l_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶ࡛࡫ࡲࡴ࡫ࡲࡲࠬમ")]) + bstack11l1l1l_opy_ (u"ࠬ࠲ࠠࠨય")
  except Exception as e:
    logger.debug(bstack11l1l1l_opy_ (u"࠭ࡓࡰ࡯ࡨࠤࡪࡸࡲࡰࡴࠣ࡭ࡳࠦࡧࡦࡰࡨࡶࡦࡺࡩ࡯ࡩࠣࡴࡱࡧࡴࡧࡱࡵࡱࠥࡹࡴࡳ࡫ࡱ࡫ࠥ࡬࡯ࡳࠢࡵࡩࡵࡵࡲࡵࠢࡪࡩࡳ࡫ࡲࡢࡶ࡬ࡳࡳ࠭ર") + str(e))
  finally:
    if bstack1lll11111_opy_[len(bstack1lll11111_opy_) - 2:] == bstack11l1l1l_opy_ (u"ࠧ࠭ࠢࠪ઱"):
      bstack1lll11111_opy_ = bstack1lll11111_opy_[:-2]
    return bstack1lll11111_opy_
def bstack111lll1l_opy_(path, bstack1lll11111_opy_):
  try:
    import xml.etree.ElementTree as ET
    bstack1l111l11l_opy_ = ET.parse(path)
    bstack11lllllll_opy_ = bstack1l111l11l_opy_.getroot()
    bstack1l11111l_opy_ = None
    for suite in bstack11lllllll_opy_.iter(bstack11l1l1l_opy_ (u"ࠨࡵࡸ࡭ࡹ࡫ࠧલ")):
      if bstack11l1l1l_opy_ (u"ࠩࡶࡳࡺࡸࡣࡦࠩળ") in suite.attrib:
        suite.attrib[bstack11l1l1l_opy_ (u"ࠪࡲࡦࡳࡥࠨ઴")] += bstack11l1l1l_opy_ (u"ࠫࠥ࠭વ") + bstack1lll11111_opy_
        bstack1l11111l_opy_ = suite
    bstack1ll1l11l1_opy_ = None
    for robot in bstack11lllllll_opy_.iter(bstack11l1l1l_opy_ (u"ࠬࡸ࡯ࡣࡱࡷࠫશ")):
      bstack1ll1l11l1_opy_ = robot
    bstack1l1111lll_opy_ = len(bstack1ll1l11l1_opy_.findall(bstack11l1l1l_opy_ (u"࠭ࡳࡶ࡫ࡷࡩࠬષ")))
    if bstack1l1111lll_opy_ == 1:
      bstack1ll1l11l1_opy_.remove(bstack1ll1l11l1_opy_.findall(bstack11l1l1l_opy_ (u"ࠧࡴࡷ࡬ࡸࡪ࠭સ"))[0])
      bstack1111l111_opy_ = ET.Element(bstack11l1l1l_opy_ (u"ࠨࡵࡸ࡭ࡹ࡫ࠧહ"), attrib={bstack11l1l1l_opy_ (u"ࠩࡱࡥࡲ࡫ࠧ઺"): bstack11l1l1l_opy_ (u"ࠪࡗࡺ࡯ࡴࡦࡵࠪ઻"), bstack11l1l1l_opy_ (u"ࠫ࡮ࡪ઼ࠧ"): bstack11l1l1l_opy_ (u"ࠬࡹ࠰ࠨઽ")})
      bstack1ll1l11l1_opy_.insert(1, bstack1111l111_opy_)
      bstack111llll11_opy_ = None
      for suite in bstack1ll1l11l1_opy_.iter(bstack11l1l1l_opy_ (u"࠭ࡳࡶ࡫ࡷࡩࠬા")):
        bstack111llll11_opy_ = suite
      bstack111llll11_opy_.append(bstack1l11111l_opy_)
      bstack1ll11111_opy_ = None
      for status in bstack1l11111l_opy_.iter(bstack11l1l1l_opy_ (u"ࠧࡴࡶࡤࡸࡺࡹࠧિ")):
        bstack1ll11111_opy_ = status
      bstack111llll11_opy_.append(bstack1ll11111_opy_)
    bstack1l111l11l_opy_.write(path)
  except Exception as e:
    logger.debug(bstack11l1l1l_opy_ (u"ࠨࡇࡵࡶࡴࡸࠠࡪࡰࠣࡴࡦࡸࡳࡪࡰࡪࠤࡼ࡮ࡩ࡭ࡧࠣ࡫ࡪࡴࡥࡳࡣࡷ࡭ࡳ࡭ࠠࡳࡱࡥࡳࡹࠦࡲࡦࡲࡲࡶࡹ࠭ી") + str(e))
def bstack1ll1ll1l_opy_(outs_dir, pabot_args, options, start_time_string, tests_root_name):
  global bstack1ll111l11l_opy_
  global CONFIG
  if bstack11l1l1l_opy_ (u"ࠤࡳࡽࡹ࡮࡯࡯ࡲࡤࡸ࡭ࠨુ") in options:
    del options[bstack11l1l1l_opy_ (u"ࠥࡴࡾࡺࡨࡰࡰࡳࡥࡹ࡮ࠢૂ")]
  bstack11l1ll1l1_opy_ = bstack1ll1ll1l1l_opy_()
  for bstack11l111l1l_opy_ in bstack11l1ll1l1_opy_.keys():
    path = os.path.join(os.getcwd(), bstack11l1l1l_opy_ (u"ࠫࡵࡧࡢࡰࡶࡢࡶࡪࡹࡵ࡭ࡶࡶࠫૃ"), str(bstack11l111l1l_opy_), bstack11l1l1l_opy_ (u"ࠬࡵࡵࡵࡲࡸࡸ࠳ࡾ࡭࡭ࠩૄ"))
    bstack111lll1l_opy_(path, bstack11l1l11ll_opy_(bstack11l1ll1l1_opy_[bstack11l111l1l_opy_]))
  bstack1llll1l111_opy_()
  return bstack1ll111l11l_opy_(outs_dir, pabot_args, options, start_time_string, tests_root_name)
def bstack1111lll11_opy_(self, ff_profile_dir):
  global bstack1ll111l1ll_opy_
  if not ff_profile_dir:
    return None
  return bstack1ll111l1ll_opy_(self, ff_profile_dir)
def bstack1l1ll1l1l1_opy_(datasources, opts_for_run, outs_dir, pabot_args, suite_group):
  from pabot.pabot import QueueItem
  global CONFIG
  global bstack11l111111_opy_
  bstack11ll1ll1_opy_ = []
  if bstack11l1l1l_opy_ (u"࠭ࡰ࡭ࡣࡷࡪࡴࡸ࡭ࡴࠩૅ") in CONFIG:
    bstack11ll1ll1_opy_ = CONFIG[bstack11l1l1l_opy_ (u"ࠧࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࡵࠪ૆")]
  return [
    QueueItem(
      datasources,
      outs_dir,
      opts_for_run,
      suite,
      pabot_args[bstack11l1l1l_opy_ (u"ࠣࡥࡲࡱࡲࡧ࡮ࡥࠤે")],
      pabot_args[bstack11l1l1l_opy_ (u"ࠤࡹࡩࡷࡨ࡯ࡴࡧࠥૈ")],
      argfile,
      pabot_args.get(bstack11l1l1l_opy_ (u"ࠥ࡬࡮ࡼࡥࠣૉ")),
      pabot_args[bstack11l1l1l_opy_ (u"ࠦࡵࡸ࡯ࡤࡧࡶࡷࡪࡹࠢ૊")],
      platform[0],
      bstack11l111111_opy_
    )
    for suite in suite_group
    for argfile in pabot_args[bstack11l1l1l_opy_ (u"ࠧࡧࡲࡨࡷࡰࡩࡳࡺࡦࡪ࡮ࡨࡷࠧો")] or [(bstack11l1l1l_opy_ (u"ࠨࠢૌ"), None)]
    for platform in enumerate(bstack11ll1ll1_opy_)
  ]
def bstack1l1lllllll_opy_(self, datasources, outs_dir, options,
                        execution_item, command, verbose, argfile,
                        hive=None, processes=0, platform_index=0, bstack1ll1111ll_opy_=bstack11l1l1l_opy_ (u"ࠧࠨ્")):
  global bstack1lll11ll1_opy_
  self.platform_index = platform_index
  self.bstack1l111l11_opy_ = bstack1ll1111ll_opy_
  bstack1lll11ll1_opy_(self, datasources, outs_dir, options,
                      execution_item, command, verbose, argfile, hive, processes)
def bstack1ll11ll1l1_opy_(caller_id, datasources, is_last, item, outs_dir):
  global bstack1ll1lllll_opy_
  global bstack1l1llllll1_opy_
  if not bstack11l1l1l_opy_ (u"ࠨࡸࡤࡶ࡮ࡧࡢ࡭ࡧࠪ૎") in item.options:
    item.options[bstack11l1l1l_opy_ (u"ࠩࡹࡥࡷ࡯ࡡࡣ࡮ࡨࠫ૏")] = []
  for v in item.options[bstack11l1l1l_opy_ (u"ࠪࡺࡦࡸࡩࡢࡤ࡯ࡩࠬૐ")]:
    if bstack11l1l1l_opy_ (u"ࠫࡇ࡙ࡔࡂࡅࡎࡔࡑࡇࡔࡇࡑࡕࡑࡎࡔࡄࡆ࡚ࠪ૑") in v:
      item.options[bstack11l1l1l_opy_ (u"ࠬࡼࡡࡳ࡫ࡤࡦࡱ࡫ࠧ૒")].remove(v)
    if bstack11l1l1l_opy_ (u"࠭ࡂࡔࡖࡄࡇࡐࡉࡌࡊࡃࡕࡋࡘ࠭૓") in v:
      item.options[bstack11l1l1l_opy_ (u"ࠧࡷࡣࡵ࡭ࡦࡨ࡬ࡦࠩ૔")].remove(v)
  item.options[bstack11l1l1l_opy_ (u"ࠨࡸࡤࡶ࡮ࡧࡢ࡭ࡧࠪ૕")].insert(0, bstack11l1l1l_opy_ (u"ࠩࡅࡗ࡙ࡇࡃࡌࡒࡏࡅ࡙ࡌࡏࡓࡏࡌࡒࡉࡋࡘ࠻ࡽࢀࠫ૖").format(item.platform_index))
  item.options[bstack11l1l1l_opy_ (u"ࠪࡺࡦࡸࡩࡢࡤ࡯ࡩࠬ૗")].insert(0, bstack11l1l1l_opy_ (u"ࠫࡇ࡙ࡔࡂࡅࡎࡈࡊࡌࡌࡐࡅࡄࡐࡎࡊࡅࡏࡖࡌࡊࡎࡋࡒ࠻ࡽࢀࠫ૘").format(item.bstack1l111l11_opy_))
  if bstack1l1llllll1_opy_:
    item.options[bstack11l1l1l_opy_ (u"ࠬࡼࡡࡳ࡫ࡤࡦࡱ࡫ࠧ૙")].insert(0, bstack11l1l1l_opy_ (u"࠭ࡂࡔࡖࡄࡇࡐࡉࡌࡊࡃࡕࡋࡘࡀࡻࡾࠩ૚").format(bstack1l1llllll1_opy_))
  return bstack1ll1lllll_opy_(caller_id, datasources, is_last, item, outs_dir)
def bstack1l1ll1ll11_opy_(command, item_index):
  os.environ[bstack11l1l1l_opy_ (u"ࠧࡄࡗࡕࡖࡊࡔࡔࡠࡒࡏࡅ࡙ࡌࡏࡓࡏࡢࡈࡆ࡚ࡁࠨ૛")] = json.dumps(CONFIG[bstack11l1l1l_opy_ (u"ࠨࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࡶࠫ૜")][item_index % bstack111lll1ll_opy_])
  global bstack1l1llllll1_opy_
  if bstack1l1llllll1_opy_:
    command[0] = command[0].replace(bstack11l1l1l_opy_ (u"ࠩࡵࡳࡧࡵࡴࠨ૝"), bstack11l1l1l_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬࠯ࡶࡨࡰࠦࡲࡰࡤࡲࡸ࠲࡯࡮ࡵࡧࡵࡲࡦࡲࠠ࠮࠯ࡥࡷࡹࡧࡣ࡬ࡡ࡬ࡸࡪࡳ࡟ࡪࡰࡧࡩࡽࠦࠧ૞") + str(
      item_index) + bstack11l1l1l_opy_ (u"ࠫࠥ࠭૟") + bstack1l1llllll1_opy_, 1)
  else:
    command[0] = command[0].replace(bstack11l1l1l_opy_ (u"ࠬࡸ࡯ࡣࡱࡷࠫૠ"),
                                    bstack11l1l1l_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯࠲ࡹࡤ࡬ࠢࡵࡳࡧࡵࡴ࠮࡫ࡱࡸࡪࡸ࡮ࡢ࡮ࠣ࠱࠲ࡨࡳࡵࡣࡦ࡯ࡤ࡯ࡴࡦ࡯ࡢ࡭ࡳࡪࡥࡹࠢࠪૡ") + str(item_index), 1)
def bstack11lll1l1l_opy_(command, stderr, stdout, item_name, verbose, pool_id, item_index):
  global bstack1lll1lllll_opy_
  bstack1l1ll1ll11_opy_(command, item_index)
  return bstack1lll1lllll_opy_(command, stderr, stdout, item_name, verbose, pool_id, item_index)
def bstack11llll11l_opy_(command, stderr, stdout, item_name, verbose, pool_id, item_index, outs_dir):
  global bstack1lll1lllll_opy_
  bstack1l1ll1ll11_opy_(command, item_index)
  return bstack1lll1lllll_opy_(command, stderr, stdout, item_name, verbose, pool_id, item_index, outs_dir)
def bstack1ll1lllll1_opy_(command, stderr, stdout, item_name, verbose, pool_id, item_index, outs_dir, process_timeout):
  global bstack1lll1lllll_opy_
  bstack1l1ll1ll11_opy_(command, item_index)
  return bstack1lll1lllll_opy_(command, stderr, stdout, item_name, verbose, pool_id, item_index, outs_dir, process_timeout)
def bstack1ll1lll1ll_opy_(self, runner, quiet=False, capture=True):
  global bstack1lll1l11ll_opy_
  bstack111llllll_opy_ = bstack1lll1l11ll_opy_(self, runner, quiet=False, capture=True)
  if self.exception:
    if not hasattr(runner, bstack11l1l1l_opy_ (u"ࠧࡦࡺࡦࡩࡵࡺࡩࡰࡰࡢࡥࡷࡸࠧૢ")):
      runner.exception_arr = []
    if not hasattr(runner, bstack11l1l1l_opy_ (u"ࠨࡧࡻࡧࡤࡺࡲࡢࡥࡨࡦࡦࡩ࡫ࡠࡣࡵࡶࠬૣ")):
      runner.exc_traceback_arr = []
    runner.exception = self.exception
    runner.exc_traceback = self.exc_traceback
    runner.exception_arr.append(self.exception)
    runner.exc_traceback_arr.append(self.exc_traceback)
  return bstack111llllll_opy_
def bstack1ll11lll1l_opy_(self, name, context, *args):
  os.environ[bstack11l1l1l_opy_ (u"ࠩࡆ࡙ࡗࡘࡅࡏࡖࡢࡔࡑࡇࡔࡇࡑࡕࡑࡤࡊࡁࡕࡃࠪ૤")] = json.dumps(CONFIG[bstack11l1l1l_opy_ (u"ࠪࡴࡱࡧࡴࡧࡱࡵࡱࡸ࠭૥")][int(threading.current_thread()._name) % bstack111lll1ll_opy_])
  global bstack1ll1l1l1ll_opy_
  if name == bstack11l1l1l_opy_ (u"ࠫࡧ࡫ࡦࡰࡴࡨࡣ࡫࡫ࡡࡵࡷࡵࡩࠬ૦"):
    bstack1ll1l1l1ll_opy_(self, name, context, *args)
    try:
      if not bstack111ll11l_opy_:
        bstack1l1lll1l1_opy_ = threading.current_thread().bstackSessionDriver if bstack11lll111_opy_(bstack11l1l1l_opy_ (u"ࠬࡨࡳࡵࡣࡦ࡯ࡘ࡫ࡳࡴ࡫ࡲࡲࡉࡸࡩࡷࡧࡵࠫ૧")) else context.browser
        bstack1lll11llll_opy_ = str(self.feature.name)
        bstack11111111l_opy_(context, bstack1lll11llll_opy_)
        bstack1l1lll1l1_opy_.execute_script(bstack11l1l1l_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࡤ࡫ࡸࡦࡥࡸࡸࡴࡸ࠺ࠡࡽࠥࡥࡨࡺࡩࡰࡰࠥ࠾ࠥࠨࡳࡦࡶࡖࡩࡸࡹࡩࡰࡰࡑࡥࡲ࡫ࠢ࠭ࠢࠥࡥࡷ࡭ࡵ࡮ࡧࡱࡸࡸࠨ࠺ࠡࡽࠥࡲࡦࡳࡥࠣ࠼ࠣࠫ૨") + json.dumps(bstack1lll11llll_opy_) + bstack11l1l1l_opy_ (u"ࠧࡾࡿࠪ૩"))
      self.driver_before_scenario = False
    except Exception as e:
      logger.debug(bstack11l1l1l_opy_ (u"ࠨࡈࡤ࡭ࡱ࡫ࡤࠡࡶࡲࠤࡸ࡫ࡴࠡࡵࡨࡷࡸ࡯࡯࡯ࠢࡱࡥࡲ࡫ࠠࡪࡰࠣࡦࡪ࡬࡯ࡳࡧࠣࡪࡪࡧࡴࡶࡴࡨ࠾ࠥࢁࡽࠨ૪").format(str(e)))
  elif name == bstack11l1l1l_opy_ (u"ࠩࡥࡩ࡫ࡵࡲࡦࡡࡶࡧࡪࡴࡡࡳ࡫ࡲࠫ૫"):
    bstack1ll1l1l1ll_opy_(self, name, context, *args)
    try:
      if not hasattr(self, bstack11l1l1l_opy_ (u"ࠪࡨࡷ࡯ࡶࡦࡴࡢࡦࡪ࡬࡯ࡳࡧࡢࡷࡨ࡫࡮ࡢࡴ࡬ࡳࠬ૬")):
        self.driver_before_scenario = True
      if (not bstack111ll11l_opy_):
        scenario_name = args[0].name
        feature_name = bstack1lll11llll_opy_ = str(self.feature.name)
        bstack1lll11llll_opy_ = feature_name + bstack11l1l1l_opy_ (u"ࠫࠥ࠳ࠠࠨ૭") + scenario_name
        bstack1l1lll1l1_opy_ = threading.current_thread().bstackSessionDriver if bstack11lll111_opy_(bstack11l1l1l_opy_ (u"ࠬࡨࡳࡵࡣࡦ࡯ࡘ࡫ࡳࡴ࡫ࡲࡲࡉࡸࡩࡷࡧࡵࠫ૮")) else context.browser
        if self.driver_before_scenario:
          bstack11111111l_opy_(context, bstack1lll11llll_opy_)
          bstack1l1lll1l1_opy_.execute_script(bstack11l1l1l_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࡤ࡫ࡸࡦࡥࡸࡸࡴࡸ࠺ࠡࡽࠥࡥࡨࡺࡩࡰࡰࠥ࠾ࠥࠨࡳࡦࡶࡖࡩࡸࡹࡩࡰࡰࡑࡥࡲ࡫ࠢ࠭ࠢࠥࡥࡷ࡭ࡵ࡮ࡧࡱࡸࡸࠨ࠺ࠡࡽࠥࡲࡦࡳࡥࠣ࠼ࠣࠫ૯") + json.dumps(bstack1lll11llll_opy_) + bstack11l1l1l_opy_ (u"ࠧࡾࡿࠪ૰"))
    except Exception as e:
      logger.debug(bstack11l1l1l_opy_ (u"ࠨࡈࡤ࡭ࡱ࡫ࡤࠡࡶࡲࠤࡸ࡫ࡴࠡࡵࡨࡷࡸ࡯࡯࡯ࠢࡱࡥࡲ࡫ࠠࡪࡰࠣࡦࡪ࡬࡯ࡳࡧࠣࡷࡨ࡫࡮ࡢࡴ࡬ࡳ࠿ࠦࡻࡾࠩ૱").format(str(e)))
  elif name == bstack11l1l1l_opy_ (u"ࠩࡤࡪࡹ࡫ࡲࡠࡵࡦࡩࡳࡧࡲࡪࡱࠪ૲"):
    try:
      bstack1llll1llll_opy_ = args[0].status.name
      bstack1l1lll1l1_opy_ = threading.current_thread().bstackSessionDriver if bstack11l1l1l_opy_ (u"ࠪࡦࡸࡺࡡࡤ࡭ࡖࡩࡸࡹࡩࡰࡰࡇࡶ࡮ࡼࡥࡳࠩ૳") in threading.current_thread().__dict__.keys() else context.browser
      if str(bstack1llll1llll_opy_).lower() == bstack11l1l1l_opy_ (u"ࠫ࡫ࡧࡩ࡭ࡧࡧࠫ૴"):
        bstack1ll1111111_opy_ = bstack11l1l1l_opy_ (u"ࠬ࠭૵")
        bstack1l111lll_opy_ = bstack11l1l1l_opy_ (u"࠭ࠧ૶")
        bstack1l111ll11_opy_ = bstack11l1l1l_opy_ (u"ࠧࠨ૷")
        try:
          import traceback
          bstack1ll1111111_opy_ = self.exception.__class__.__name__
          bstack1ll1ll1l1_opy_ = traceback.format_tb(self.exc_traceback)
          bstack1l111lll_opy_ = bstack11l1l1l_opy_ (u"ࠨࠢࠪ૸").join(bstack1ll1ll1l1_opy_)
          bstack1l111ll11_opy_ = bstack1ll1ll1l1_opy_[-1]
        except Exception as e:
          logger.debug(bstack1l1l11111_opy_.format(str(e)))
        bstack1ll1111111_opy_ += bstack1l111ll11_opy_
        bstack1111l1lll_opy_(context, json.dumps(str(args[0].name) + bstack11l1l1l_opy_ (u"ࠤࠣ࠱ࠥࡌࡡࡪ࡮ࡨࡨࠦࡢ࡮ࠣૹ") + str(bstack1l111lll_opy_)),
                            bstack11l1l1l_opy_ (u"ࠥࡩࡷࡸ࡯ࡳࠤૺ"))
        if self.driver_before_scenario:
          bstack1l11l1l1l_opy_(context, bstack11l1l1l_opy_ (u"ࠦ࡫ࡧࡩ࡭ࡧࡧࠦૻ"), bstack1ll1111111_opy_)
          bstack1l1lll1l1_opy_.execute_script(bstack11l1l1l_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࡣࡪࡾࡥࡤࡷࡷࡳࡷࡀࠠࡼࠤࡤࡧࡹ࡯࡯࡯ࠤ࠽ࠤࠧࡧ࡮࡯ࡱࡷࡥࡹ࡫ࠢ࠭ࠢࠥࡥࡷ࡭ࡵ࡮ࡧࡱࡸࡸࠨ࠺ࠡࡽࠥࡨࡦࡺࡡࠣ࠼ࠪૼ") + json.dumps(str(args[0].name) + bstack11l1l1l_opy_ (u"ࠨࠠ࠮ࠢࡉࡥ࡮ࡲࡥࡥࠣ࡟ࡲࠧ૽") + str(bstack1l111lll_opy_)) + bstack11l1l1l_opy_ (u"ࠧ࠭ࠢࠥࡰࡪࡼࡥ࡭ࠤ࠽ࠤࠧ࡫ࡲࡳࡱࡵࠦࢂࢃࠧ૾"))
        if self.driver_before_scenario:
          bstack1l1lll1l1_opy_.execute_script(bstack11l1l1l_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࡟ࡦࡺࡨࡧࡺࡺ࡯ࡳ࠼ࠣࡿࠧࡧࡣࡵ࡫ࡲࡲࠧࡀࠠࠣࡵࡨࡸࡘ࡫ࡳࡴ࡫ࡲࡲࡘࡺࡡࡵࡷࡶࠦ࠱ࠦࠢࡢࡴࡪࡹࡲ࡫࡮ࡵࡵࠥ࠾ࠥࢁࠢࡴࡶࡤࡸࡺࡹࠢ࠻ࠤࡩࡥ࡮ࡲࡥࡥࠤ࠯ࠤࠧࡸࡥࡢࡵࡲࡲࠧࡀࠠࠨ૿") + json.dumps(bstack11l1l1l_opy_ (u"ࠤࡖࡧࡪࡴࡡࡳ࡫ࡲࠤ࡫ࡧࡩ࡭ࡧࡧࠤࡼ࡯ࡴࡩ࠼ࠣࡠࡳࠨ଀") + str(bstack1ll1111111_opy_)) + bstack11l1l1l_opy_ (u"ࠪࢁࢂ࠭ଁ"))
      else:
        bstack1111l1lll_opy_(context, bstack11l1l1l_opy_ (u"ࠦࡕࡧࡳࡴࡧࡧࠥࠧଂ"), bstack11l1l1l_opy_ (u"ࠧ࡯࡮ࡧࡱࠥଃ"))
        if self.driver_before_scenario:
          bstack1l11l1l1l_opy_(context, bstack11l1l1l_opy_ (u"ࠨࡰࡢࡵࡶࡩࡩࠨ଄"))
        bstack1l1lll1l1_opy_.execute_script(bstack11l1l1l_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰࡥࡥࡹࡧࡦࡹࡹࡵࡲ࠻ࠢࡾࠦࡦࡩࡴࡪࡱࡱࠦ࠿ࠦࠢࡢࡰࡱࡳࡹࡧࡴࡦࠤ࠯ࠤࠧࡧࡲࡨࡷࡰࡩࡳࡺࡳࠣ࠼ࠣࡿࠧࡪࡡࡵࡣࠥ࠾ࠬଅ") + json.dumps(str(args[0].name) + bstack11l1l1l_opy_ (u"ࠣࠢ࠰ࠤࡕࡧࡳࡴࡧࡧࠥࠧଆ")) + bstack11l1l1l_opy_ (u"ࠩ࠯ࠤࠧࡲࡥࡷࡧ࡯ࠦ࠿ࠦࠢࡪࡰࡩࡳࠧࢃࡽࠨଇ"))
        if self.driver_before_scenario:
          bstack1l1lll1l1_opy_.execute_script(bstack11l1l1l_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࡡࡨࡼࡪࡩࡵࡵࡱࡵ࠾ࠥࢁࠢࡢࡥࡷ࡭ࡴࡴࠢ࠻ࠢࠥࡷࡪࡺࡓࡦࡵࡶ࡭ࡴࡴࡓࡵࡣࡷࡹࡸࠨࠬࠡࠤࡤࡶ࡬ࡻ࡭ࡦࡰࡷࡷࠧࡀࠠࡼࠤࡶࡸࡦࡺࡵࡴࠤ࠽ࠦࡵࡧࡳࡴࡧࡧࠦࢂࢃࠧଈ"))
    except Exception as e:
      logger.debug(bstack11l1l1l_opy_ (u"ࠫࡋࡧࡩ࡭ࡧࡧࠤࡹࡵࠠ࡮ࡣࡵ࡯ࠥࡹࡥࡴࡵ࡬ࡳࡳࠦࡳࡵࡣࡷࡹࡸࠦࡩ࡯ࠢࡤࡪࡹ࡫ࡲࠡࡨࡨࡥࡹࡻࡲࡦ࠼ࠣࡿࢂ࠭ଉ").format(str(e)))
  elif name == bstack11l1l1l_opy_ (u"ࠬࡧࡦࡵࡧࡵࡣ࡫࡫ࡡࡵࡷࡵࡩࠬଊ"):
    try:
      bstack1l1lll1l1_opy_ = threading.current_thread().bstackSessionDriver if bstack11lll111_opy_(bstack11l1l1l_opy_ (u"࠭ࡢࡴࡶࡤࡧࡰ࡙ࡥࡴࡵ࡬ࡳࡳࡊࡲࡪࡸࡨࡶࠬଋ")) else context.browser
      if context.failed is True:
        bstack11l1l1111_opy_ = []
        bstack1l11l1l1_opy_ = []
        bstack1111l1ll_opy_ = []
        bstack111lllll1_opy_ = bstack11l1l1l_opy_ (u"ࠧࠨଌ")
        try:
          import traceback
          for exc in self.exception_arr:
            bstack11l1l1111_opy_.append(exc.__class__.__name__)
          for exc_tb in self.exc_traceback_arr:
            bstack1ll1ll1l1_opy_ = traceback.format_tb(exc_tb)
            bstack111ll1l1l_opy_ = bstack11l1l1l_opy_ (u"ࠨࠢࠪ଍").join(bstack1ll1ll1l1_opy_)
            bstack1l11l1l1_opy_.append(bstack111ll1l1l_opy_)
            bstack1111l1ll_opy_.append(bstack1ll1ll1l1_opy_[-1])
        except Exception as e:
          logger.debug(bstack1l1l11111_opy_.format(str(e)))
        bstack1ll1111111_opy_ = bstack11l1l1l_opy_ (u"ࠩࠪ଎")
        for i in range(len(bstack11l1l1111_opy_)):
          bstack1ll1111111_opy_ += bstack11l1l1111_opy_[i] + bstack1111l1ll_opy_[i] + bstack11l1l1l_opy_ (u"ࠪࡠࡳ࠭ଏ")
        bstack111lllll1_opy_ = bstack11l1l1l_opy_ (u"ࠫࠥ࠭ଐ").join(bstack1l11l1l1_opy_)
        if not self.driver_before_scenario:
          bstack1111l1lll_opy_(context, bstack111lllll1_opy_, bstack11l1l1l_opy_ (u"ࠧ࡫ࡲࡳࡱࡵࠦ଑"))
          bstack1l11l1l1l_opy_(context, bstack11l1l1l_opy_ (u"ࠨࡦࡢ࡫࡯ࡩࡩࠨ଒"), bstack1ll1111111_opy_)
          bstack1l1lll1l1_opy_.execute_script(bstack11l1l1l_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰࡥࡥࡹࡧࡦࡹࡹࡵࡲ࠻ࠢࡾࠦࡦࡩࡴࡪࡱࡱࠦ࠿ࠦࠢࡢࡰࡱࡳࡹࡧࡴࡦࠤ࠯ࠤࠧࡧࡲࡨࡷࡰࡩࡳࡺࡳࠣ࠼ࠣࡿࠧࡪࡡࡵࡣࠥ࠾ࠬଓ") + json.dumps(bstack111lllll1_opy_) + bstack11l1l1l_opy_ (u"ࠨ࠮ࠣࠦࡱ࡫ࡶࡦ࡮ࠥ࠾ࠥࠨࡥࡳࡴࡲࡶࠧࢃࡽࠨଔ"))
          bstack1l1lll1l1_opy_.execute_script(bstack11l1l1l_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࡠࡧࡻࡩࡨࡻࡴࡰࡴ࠽ࠤࢀࠨࡡࡤࡶ࡬ࡳࡳࠨ࠺ࠡࠤࡶࡩࡹ࡙ࡥࡴࡵ࡬ࡳࡳ࡙ࡴࡢࡶࡸࡷࠧ࠲ࠠࠣࡣࡵ࡫ࡺࡳࡥ࡯ࡶࡶࠦ࠿ࠦࡻࠣࡵࡷࡥࡹࡻࡳࠣ࠼ࠥࡪࡦ࡯࡬ࡦࡦࠥ࠰ࠥࠨࡲࡦࡣࡶࡳࡳࠨ࠺ࠡࠩକ") + json.dumps(bstack11l1l1l_opy_ (u"ࠥࡗࡴࡳࡥࠡࡵࡦࡩࡳࡧࡲࡪࡱࡶࠤ࡫ࡧࡩ࡭ࡧࡧ࠾ࠥࡢ࡮ࠣଖ") + str(bstack1ll1111111_opy_)) + bstack11l1l1l_opy_ (u"ࠫࢂࢃࠧଗ"))
          bstack1l1ll1lll1_opy_ = bstack111l111l1_opy_(bstack111lllll1_opy_, self.feature.name, logger)
          if (bstack1l1ll1lll1_opy_ != None):
            bstack11l11ll1_opy_.append(bstack1l1ll1lll1_opy_)
      else:
        if not self.driver_before_scenario:
          bstack1111l1lll_opy_(context, bstack11l1l1l_opy_ (u"ࠧࡌࡥࡢࡶࡸࡶࡪࡀࠠࠣଘ") + str(self.feature.name) + bstack11l1l1l_opy_ (u"ࠨࠠࡱࡣࡶࡷࡪࡪࠡࠣଙ"), bstack11l1l1l_opy_ (u"ࠢࡪࡰࡩࡳࠧଚ"))
          bstack1l11l1l1l_opy_(context, bstack11l1l1l_opy_ (u"ࠣࡲࡤࡷࡸ࡫ࡤࠣଛ"))
          bstack1l1lll1l1_opy_.execute_script(bstack11l1l1l_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࡠࡧࡻࡩࡨࡻࡴࡰࡴ࠽ࠤࢀࠨࡡࡤࡶ࡬ࡳࡳࠨ࠺ࠡࠤࡤࡲࡳࡵࡴࡢࡶࡨࠦ࠱ࠦࠢࡢࡴࡪࡹࡲ࡫࡮ࡵࡵࠥ࠾ࠥࢁࠢࡥࡣࡷࡥࠧࡀࠧଜ") + json.dumps(bstack11l1l1l_opy_ (u"ࠥࡊࡪࡧࡴࡶࡴࡨ࠾ࠥࠨଝ") + str(self.feature.name) + bstack11l1l1l_opy_ (u"ࠦࠥࡶࡡࡴࡵࡨࡨࠦࠨଞ")) + bstack11l1l1l_opy_ (u"ࠬ࠲ࠠࠣ࡮ࡨࡺࡪࡲࠢ࠻ࠢࠥ࡭ࡳ࡬࡯ࠣࡿࢀࠫଟ"))
          bstack1l1lll1l1_opy_.execute_script(bstack11l1l1l_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࡤ࡫ࡸࡦࡥࡸࡸࡴࡸ࠺ࠡࡽࠥࡥࡨࡺࡩࡰࡰࠥ࠾ࠥࠨࡳࡦࡶࡖࡩࡸࡹࡩࡰࡰࡖࡸࡦࡺࡵࡴࠤ࠯ࠤࠧࡧࡲࡨࡷࡰࡩࡳࡺࡳࠣ࠼ࠣࡿࠧࡹࡴࡢࡶࡸࡷࠧࡀࠢࡱࡣࡶࡷࡪࡪࠢࡾࡿࠪଠ"))
          bstack1l1ll1lll1_opy_ = bstack111l111l1_opy_(bstack111lllll1_opy_, self.feature.name, logger)
          if (bstack1l1ll1lll1_opy_ != None):
            bstack11l11ll1_opy_.append(bstack1l1ll1lll1_opy_)
    except Exception as e:
      logger.debug(bstack11l1l1l_opy_ (u"ࠧࡇࡣ࡬ࡰࡪࡪࠠࡵࡱࠣࡱࡦࡸ࡫ࠡࡵࡨࡷࡸ࡯࡯࡯ࠢࡶࡸࡦࡺࡵࡴࠢ࡬ࡲࠥࡧࡦࡵࡧࡵࠤ࡫࡫ࡡࡵࡷࡵࡩ࠿ࠦࡻࡾࠩଡ").format(str(e)))
  else:
    bstack1ll1l1l1ll_opy_(self, name, context, *args)
  if name in [bstack11l1l1l_opy_ (u"ࠨࡣࡩࡸࡪࡸ࡟ࡧࡧࡤࡸࡺࡸࡥࠨଢ"), bstack11l1l1l_opy_ (u"ࠩࡤࡪࡹ࡫ࡲࡠࡵࡦࡩࡳࡧࡲࡪࡱࠪଣ")]:
    bstack1ll1l1l1ll_opy_(self, name, context, *args)
    if (name == bstack11l1l1l_opy_ (u"ࠪࡥ࡫ࡺࡥࡳࡡࡶࡧࡪࡴࡡࡳ࡫ࡲࠫତ") and self.driver_before_scenario) or (
            name == bstack11l1l1l_opy_ (u"ࠫࡦ࡬ࡴࡦࡴࡢࡪࡪࡧࡴࡶࡴࡨࠫଥ") and not self.driver_before_scenario):
      try:
        bstack1l1lll1l1_opy_ = threading.current_thread().bstackSessionDriver if bstack11lll111_opy_(bstack11l1l1l_opy_ (u"ࠬࡨࡳࡵࡣࡦ࡯ࡘ࡫ࡳࡴ࡫ࡲࡲࡉࡸࡩࡷࡧࡵࠫଦ")) else context.browser
        bstack1l1lll1l1_opy_.quit()
      except Exception:
        pass
def bstack1llllll1l_opy_(config, startdir):
  return bstack11l1l1l_opy_ (u"ࠨࡤࡳ࡫ࡹࡩࡷࡀࠠࡼ࠲ࢀࠦଧ").format(bstack11l1l1l_opy_ (u"ࠢࡃࡴࡲࡻࡸ࡫ࡲࡔࡶࡤࡧࡰࠨନ"))
notset = Notset()
def bstack1l1ll11l_opy_(self, name: str, default=notset, skip: bool = False):
  global bstack1l1l11l1l_opy_
  if str(name).lower() == bstack11l1l1l_opy_ (u"ࠨࡦࡵ࡭ࡻ࡫ࡲࠨ଩"):
    return bstack11l1l1l_opy_ (u"ࠤࡅࡶࡴࡽࡳࡦࡴࡖࡸࡦࡩ࡫ࠣପ")
  else:
    return bstack1l1l11l1l_opy_(self, name, default, skip)
def bstack111lllll_opy_(item, when):
  global bstack11ll1l1ll_opy_
  try:
    bstack11ll1l1ll_opy_(item, when)
  except Exception as e:
    pass
def bstack1llll1l1l_opy_():
  return
def bstack1l1lll1l1l_opy_(type, name, status, reason, bstack1l1llll11_opy_, bstack11llllll1_opy_):
  bstack11l11111_opy_ = {
    bstack11l1l1l_opy_ (u"ࠪࡥࡨࡺࡩࡰࡰࠪଫ"): type,
    bstack11l1l1l_opy_ (u"ࠫࡦࡸࡧࡶ࡯ࡨࡲࡹࡹࠧବ"): {}
  }
  if type == bstack11l1l1l_opy_ (u"ࠬࡧ࡮࡯ࡱࡷࡥࡹ࡫ࠧଭ"):
    bstack11l11111_opy_[bstack11l1l1l_opy_ (u"࠭ࡡࡳࡩࡸࡱࡪࡴࡴࡴࠩମ")][bstack11l1l1l_opy_ (u"ࠧ࡭ࡧࡹࡩࡱ࠭ଯ")] = bstack1l1llll11_opy_
    bstack11l11111_opy_[bstack11l1l1l_opy_ (u"ࠨࡣࡵ࡫ࡺࡳࡥ࡯ࡶࡶࠫର")][bstack11l1l1l_opy_ (u"ࠩࡧࡥࡹࡧࠧ଱")] = json.dumps(str(bstack11llllll1_opy_))
  if type == bstack11l1l1l_opy_ (u"ࠪࡷࡪࡺࡓࡦࡵࡶ࡭ࡴࡴࡎࡢ࡯ࡨࠫଲ"):
    bstack11l11111_opy_[bstack11l1l1l_opy_ (u"ࠫࡦࡸࡧࡶ࡯ࡨࡲࡹࡹࠧଳ")][bstack11l1l1l_opy_ (u"ࠬࡴࡡ࡮ࡧࠪ଴")] = name
  if type == bstack11l1l1l_opy_ (u"࠭ࡳࡦࡶࡖࡩࡸࡹࡩࡰࡰࡖࡸࡦࡺࡵࡴࠩଵ"):
    bstack11l11111_opy_[bstack11l1l1l_opy_ (u"ࠧࡢࡴࡪࡹࡲ࡫࡮ࡵࡵࠪଶ")][bstack11l1l1l_opy_ (u"ࠨࡵࡷࡥࡹࡻࡳࠨଷ")] = status
    if status == bstack11l1l1l_opy_ (u"ࠩࡩࡥ࡮ࡲࡥࡥࠩସ"):
      bstack11l11111_opy_[bstack11l1l1l_opy_ (u"ࠪࡥࡷ࡭ࡵ࡮ࡧࡱࡸࡸ࠭ହ")][bstack11l1l1l_opy_ (u"ࠫࡷ࡫ࡡࡴࡱࡱࠫ଺")] = json.dumps(str(reason))
  bstack111lll11l_opy_ = bstack11l1l1l_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࡣࡪࡾࡥࡤࡷࡷࡳࡷࡀࠠࡼࡿࠪ଻").format(json.dumps(bstack11l11111_opy_))
  return bstack111lll11l_opy_
def bstack1ll11l111_opy_(driver_command, response):
    if driver_command == bstack11l1l1l_opy_ (u"࠭ࡳࡤࡴࡨࡩࡳࡹࡨࡰࡶ଼ࠪ"):
        bstack1l11l11l_opy_.bstack111l1ll1l_opy_({
            bstack11l1l1l_opy_ (u"ࠧࡪ࡯ࡤ࡫ࡪ࠭ଽ"): response[bstack11l1l1l_opy_ (u"ࠨࡸࡤࡰࡺ࡫ࠧା")],
            bstack11l1l1l_opy_ (u"ࠩࡷࡩࡸࡺ࡟ࡳࡷࡱࡣࡺࡻࡩࡥࠩି"): bstack1l11l11l_opy_.current_test_uuid()
        })
def bstack1ll1l111l_opy_(item, call, rep):
  global bstack1l1111l1_opy_
  global bstack11111lll1_opy_
  global bstack111ll11l_opy_
  name = bstack11l1l1l_opy_ (u"ࠪࠫୀ")
  try:
    if rep.when == bstack11l1l1l_opy_ (u"ࠫࡨࡧ࡬࡭ࠩୁ"):
      bstack1l1ll1ll1_opy_ = threading.current_thread().bstackSessionId
      try:
        if not bstack111ll11l_opy_:
          name = str(rep.nodeid)
          bstack1l1ll111l_opy_ = bstack1l1lll1l1l_opy_(bstack11l1l1l_opy_ (u"ࠬࡹࡥࡵࡕࡨࡷࡸ࡯࡯࡯ࡐࡤࡱࡪ࠭ୂ"), name, bstack11l1l1l_opy_ (u"࠭ࠧୃ"), bstack11l1l1l_opy_ (u"ࠧࠨୄ"), bstack11l1l1l_opy_ (u"ࠨࠩ୅"), bstack11l1l1l_opy_ (u"ࠩࠪ୆"))
          threading.current_thread().bstack1ll11l11_opy_ = name
          for driver in bstack11111lll1_opy_:
            if bstack1l1ll1ll1_opy_ == driver.session_id:
              driver.execute_script(bstack1l1ll111l_opy_)
      except Exception as e:
        logger.debug(bstack11l1l1l_opy_ (u"ࠪࡉࡷࡸ࡯ࡳࠢ࡬ࡲࠥࡹࡥࡵࡶ࡬ࡲ࡬ࠦࡳࡦࡵࡶ࡭ࡴࡴࡎࡢ࡯ࡨࠤ࡫ࡵࡲࠡࡲࡼࡸࡪࡹࡴ࠮ࡤࡧࡨࠥࡹࡥࡴࡵ࡬ࡳࡳࡀࠠࡼࡿࠪେ").format(str(e)))
      try:
        bstack1lll11l1ll_opy_(rep.outcome.lower())
        if rep.outcome.lower() != bstack11l1l1l_opy_ (u"ࠫࡸࡱࡩࡱࡲࡨࡨࠬୈ"):
          status = bstack11l1l1l_opy_ (u"ࠬ࡬ࡡࡪ࡮ࡨࡨࠬ୉") if rep.outcome.lower() == bstack11l1l1l_opy_ (u"࠭ࡦࡢ࡫࡯ࡩࡩ࠭୊") else bstack11l1l1l_opy_ (u"ࠧࡱࡣࡶࡷࡪࡪࠧୋ")
          reason = bstack11l1l1l_opy_ (u"ࠨࠩୌ")
          if status == bstack11l1l1l_opy_ (u"ࠩࡩࡥ࡮ࡲࡥࡥ୍ࠩ"):
            reason = rep.longrepr.reprcrash.message
            if (not threading.current_thread().bstackTestErrorMessages):
              threading.current_thread().bstackTestErrorMessages = []
            threading.current_thread().bstackTestErrorMessages.append(reason)
          level = bstack11l1l1l_opy_ (u"ࠪ࡭ࡳ࡬࡯ࠨ୎") if status == bstack11l1l1l_opy_ (u"ࠫࡵࡧࡳࡴࡧࡧࠫ୏") else bstack11l1l1l_opy_ (u"ࠬ࡫ࡲࡳࡱࡵࠫ୐")
          data = name + bstack11l1l1l_opy_ (u"࠭ࠠࡱࡣࡶࡷࡪࡪࠡࠨ୑") if status == bstack11l1l1l_opy_ (u"ࠧࡱࡣࡶࡷࡪࡪࠧ୒") else name + bstack11l1l1l_opy_ (u"ࠨࠢࡩࡥ࡮ࡲࡥࡥࠣࠣࠫ୓") + reason
          bstack111lll1l1_opy_ = bstack1l1lll1l1l_opy_(bstack11l1l1l_opy_ (u"ࠩࡤࡲࡳࡵࡴࡢࡶࡨࠫ୔"), bstack11l1l1l_opy_ (u"ࠪࠫ୕"), bstack11l1l1l_opy_ (u"ࠫࠬୖ"), bstack11l1l1l_opy_ (u"ࠬ࠭ୗ"), level, data)
          for driver in bstack11111lll1_opy_:
            if bstack1l1ll1ll1_opy_ == driver.session_id:
              driver.execute_script(bstack111lll1l1_opy_)
      except Exception as e:
        logger.debug(bstack11l1l1l_opy_ (u"࠭ࡅࡳࡴࡲࡶࠥ࡯࡮ࠡࡵࡨࡸࡹ࡯࡮ࡨࠢࡶࡩࡸࡹࡩࡰࡰࠣࡧࡴࡴࡴࡦࡺࡷࠤ࡫ࡵࡲࠡࡲࡼࡸࡪࡹࡴ࠮ࡤࡧࡨࠥࡹࡥࡴࡵ࡬ࡳࡳࡀࠠࡼࡿࠪ୘").format(str(e)))
  except Exception as e:
    logger.debug(bstack11l1l1l_opy_ (u"ࠧࡆࡴࡵࡳࡷࠦࡩ࡯ࠢࡪࡩࡹࡺࡩ࡯ࡩࠣࡷࡹࡧࡴࡦࠢ࡬ࡲࠥࡶࡹࡵࡧࡶࡸ࠲ࡨࡤࡥࠢࡷࡩࡸࡺࠠࡴࡶࡤࡸࡺࡹ࠺ࠡࡽࢀࠫ୙").format(str(e)))
  bstack1l1111l1_opy_(item, call, rep)
def bstack1l1l1l111_opy_(framework_name):
  global bstack1lllll1ll1_opy_
  global bstack1l1l1llll_opy_
  global bstack1l1l11lll_opy_
  bstack1lllll1ll1_opy_ = framework_name
  logger.info(bstack1lll1111_opy_.format(bstack1lllll1ll1_opy_.split(bstack11l1l1l_opy_ (u"ࠨ࠯ࠪ୚"))[0]))
  try:
    from selenium import webdriver
    from selenium.webdriver.common.service import Service
    from selenium.webdriver.remote.webdriver import WebDriver
    if bstack11l1l1ll1_opy_:
      Service.start = bstack1l1l11l1_opy_
      Service.stop = bstack1l1l1ll1l_opy_
      webdriver.Remote.get = bstack11l1ll11_opy_
      WebDriver.close = bstack11lll1ll1_opy_
      WebDriver.quit = bstack1111l1l1_opy_
      webdriver.Remote.__init__ = bstack1ll1ll1l11_opy_
      WebDriver.getAccessibilityResults = getAccessibilityResults
      WebDriver.bstack1lll1l1lll_opy_ = getAccessibilityResults
      WebDriver.getAccessibilityResultsSummary = getAccessibilityResultsSummary
      WebDriver.bstack1l1ll11lll_opy_ = getAccessibilityResultsSummary
    if not bstack11l1l1ll1_opy_ and bstack1l11l11l_opy_.on():
      webdriver.Remote.__init__ = bstack1lll1lll1_opy_
    if bstack1l11l11l_opy_.on():
      WebDriver.execute = bstack1l1ll1111_opy_
    bstack1l1l1llll_opy_ = True
  except Exception as e:
    pass
  bstack1lll111ll_opy_()
  if not bstack1l1l1llll_opy_:
    bstack1111l111l_opy_(bstack11l1l1l_opy_ (u"ࠤࡓࡥࡨࡱࡡࡨࡧࡶࠤࡳࡵࡴࠡ࡫ࡱࡷࡹࡧ࡬࡭ࡧࡧࠦ୛"), bstack11lll11ll_opy_)
  if bstack1ll1111ll1_opy_():
    try:
      from selenium.webdriver.remote.remote_connection import RemoteConnection
      RemoteConnection._get_proxy_url = bstack1lll11lll1_opy_
    except Exception as e:
      logger.error(bstack1ll11l11ll_opy_.format(str(e)))
  if bstack11lll1lll_opy_():
    bstack1lll1ll1l_opy_(CONFIG, logger)
  if (bstack11l1l1l_opy_ (u"ࠪࡶࡴࡨ࡯ࡵࠩଡ଼") in str(framework_name).lower()):
    try:
      from robot import run_cli
      from robot.output import Output
      from robot.running.status import TestStatus
      from pabot.pabot import QueueItem
      from pabot import pabot
      try:
        from SeleniumLibrary.keywords.webdrivertools.webdrivertools import WebDriverCreator
        WebDriverCreator._get_ff_profile = bstack1111lll11_opy_
        from SeleniumLibrary.keywords.webdrivertools.webdrivertools import WebDriverCache
        WebDriverCache.close = bstack11l1lll1_opy_
      except Exception as e:
        logger.warn(bstack1ll1l11l1l_opy_ + str(e))
      try:
        from AppiumLibrary.utils.applicationcache import ApplicationCache
        ApplicationCache.close = bstack111llll1l_opy_
      except Exception as e:
        logger.debug(bstack1ll1l1ll11_opy_ + str(e))
    except Exception as e:
      bstack1111l111l_opy_(e, bstack1ll1l11l1l_opy_)
    Output.end_test = bstack11l11l11_opy_
    TestStatus.__init__ = bstack1111l1l11_opy_
    QueueItem.__init__ = bstack1l1lllllll_opy_
    pabot._create_items = bstack1l1ll1l1l1_opy_
    try:
      from pabot import __version__ as bstack11l11111l_opy_
      if version.parse(bstack11l11111l_opy_) >= version.parse(bstack11l1l1l_opy_ (u"ࠫ࠷࠴࠱࠶࠰࠳ࠫଢ଼")):
        pabot._run = bstack1ll1lllll1_opy_
      elif version.parse(bstack11l11111l_opy_) >= version.parse(bstack11l1l1l_opy_ (u"ࠬ࠸࠮࠲࠵࠱࠴ࠬ୞")):
        pabot._run = bstack11llll11l_opy_
      else:
        pabot._run = bstack11lll1l1l_opy_
    except Exception as e:
      pabot._run = bstack11lll1l1l_opy_
    pabot._create_command_for_execution = bstack1ll11ll1l1_opy_
    pabot._report_results = bstack1ll1ll1l_opy_
  if bstack11l1l1l_opy_ (u"࠭ࡢࡦࡪࡤࡺࡪ࠭ୟ") in str(framework_name).lower():
    try:
      from behave.runner import Runner
      from behave.model import Step
    except Exception as e:
      bstack1111l111l_opy_(e, bstack1lll11ll11_opy_)
    Runner.run_hook = bstack1ll11lll1l_opy_
    Step.run = bstack1ll1lll1ll_opy_
  if bstack11l1l1l_opy_ (u"ࠧࡱࡻࡷࡩࡸࡺࠧୠ") in str(framework_name).lower():
    if not bstack11l1l1ll1_opy_:
      return
    try:
      from pytest_selenium import pytest_selenium
      from _pytest.config import Config
      pytest_selenium.pytest_report_header = bstack1llllll1l_opy_
      from pytest_selenium.drivers import browserstack
      browserstack.pytest_selenium_runtest_makereport = bstack1llll1l1l_opy_
      Config.getoption = bstack1l1ll11l_opy_
    except Exception as e:
      pass
    try:
      from pytest_bdd import reporting
      reporting.runtest_makereport = bstack1ll1l111l_opy_
    except Exception as e:
      pass
def bstack1ll1l1ll1l_opy_():
  global CONFIG
  if bstack11l1l1l_opy_ (u"ࠨࡲࡤࡶࡦࡲ࡬ࡦ࡮ࡶࡔࡪࡸࡐ࡭ࡣࡷࡪࡴࡸ࡭ࠨୡ") in CONFIG and int(CONFIG[bstack11l1l1l_opy_ (u"ࠩࡳࡥࡷࡧ࡬࡭ࡧ࡯ࡷࡕ࡫ࡲࡑ࡮ࡤࡸ࡫ࡵࡲ࡮ࠩୢ")]) > 1:
    logger.warn(bstack1ll1l1ll1_opy_)
def bstack1lll1ll1l1_opy_(arg, bstack1111llll1_opy_, bstack1ll111ll_opy_=None):
  global CONFIG
  global bstack1l1ll1ll1l_opy_
  global bstack1lll1l111_opy_
  global bstack11l1l1ll1_opy_
  global bstack1lllll111l_opy_
  bstack1lll1l1l_opy_ = bstack11l1l1l_opy_ (u"ࠪࡴࡾࡺࡥࡴࡶࠪୣ")
  if bstack1111llll1_opy_ and isinstance(bstack1111llll1_opy_, str):
    bstack1111llll1_opy_ = eval(bstack1111llll1_opy_)
  CONFIG = bstack1111llll1_opy_[bstack11l1l1l_opy_ (u"ࠫࡈࡕࡎࡇࡋࡊࠫ୤")]
  bstack1l1ll1ll1l_opy_ = bstack1111llll1_opy_[bstack11l1l1l_opy_ (u"ࠬࡎࡕࡃࡡࡘࡖࡑ࠭୥")]
  bstack1lll1l111_opy_ = bstack1111llll1_opy_[bstack11l1l1l_opy_ (u"࠭ࡉࡔࡡࡄࡔࡕࡥࡁࡖࡖࡒࡑࡆ࡚ࡅࠨ୦")]
  bstack11l1l1ll1_opy_ = bstack1111llll1_opy_[bstack11l1l1l_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡁࡖࡖࡒࡑࡆ࡚ࡉࡐࡐࠪ୧")]
  bstack1lllll111l_opy_.bstack1lllll1ll_opy_(bstack11l1l1l_opy_ (u"ࠨࡤࡶࡸࡦࡩ࡫ࡠࡵࡨࡷࡸ࡯࡯࡯ࠩ୨"), bstack11l1l1ll1_opy_)
  os.environ[bstack11l1l1l_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡈࡕࡅࡒࡋࡗࡐࡔࡎࠫ୩")] = bstack1lll1l1l_opy_
  os.environ[bstack11l1l1l_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡆࡓࡓࡌࡉࡈࠩ୪")] = json.dumps(CONFIG)
  os.environ[bstack11l1l1l_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡌ࡚ࡈ࡟ࡖࡔࡏࠫ୫")] = bstack1l1ll1ll1l_opy_
  os.environ[bstack11l1l1l_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣࡎ࡙࡟ࡂࡒࡓࡣࡆ࡛ࡔࡐࡏࡄࡘࡊ࠭୬")] = str(bstack1lll1l111_opy_)
  os.environ[bstack11l1l1l_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤࡖ࡙ࡕࡇࡖࡘࡤࡖࡌࡖࡉࡌࡒࠬ୭")] = str(True)
  if bstack1l1lll11l_opy_(arg, [bstack11l1l1l_opy_ (u"ࠧ࠮ࡰࠪ୮"), bstack11l1l1l_opy_ (u"ࠨ࠯࠰ࡲࡺࡳࡰࡳࡱࡦࡩࡸࡹࡥࡴࠩ୯")]) != -1:
    os.environ[bstack11l1l1l_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡒ࡜ࡘࡊ࡙ࡔࡠࡒࡄࡖࡆࡒࡌࡆࡎࠪ୰")] = str(True)
  if len(sys.argv) <= 1:
    logger.critical(bstack111lll111_opy_)
    return
  bstack1llllllll1_opy_()
  global bstack1ll1111l11_opy_
  global bstack1llll111l_opy_
  global bstack11l111111_opy_
  global bstack1l1llllll1_opy_
  global bstack1llll1l11l_opy_
  global bstack1l1l11lll_opy_
  global bstack1l1l1l1l1_opy_
  arg.append(bstack11l1l1l_opy_ (u"ࠥ࠱࡜ࠨୱ"))
  arg.append(bstack11l1l1l_opy_ (u"ࠦ࡮࡭࡮ࡰࡴࡨ࠾ࡒࡵࡤࡶ࡮ࡨࠤࡦࡲࡲࡦࡣࡧࡽࠥ࡯࡭ࡱࡱࡵࡸࡪࡪ࠺ࡱࡻࡷࡩࡸࡺ࠮ࡑࡻࡷࡩࡸࡺࡗࡢࡴࡱ࡭ࡳ࡭ࠢ୲"))
  arg.append(bstack11l1l1l_opy_ (u"ࠧ࠳ࡗࠣ୳"))
  arg.append(bstack11l1l1l_opy_ (u"ࠨࡩࡨࡰࡲࡶࡪࡀࡔࡩࡧࠣ࡬ࡴࡵ࡫ࡪ࡯ࡳࡰࠧ୴"))
  global bstack1l111l1l_opy_
  global bstack1l1l1l1ll_opy_
  global bstack1l11111ll_opy_
  global bstack1ll111l1ll_opy_
  global bstack1lll11ll1_opy_
  global bstack1ll1lllll_opy_
  global bstack1l111lll1_opy_
  global bstack1l11l1l11_opy_
  global bstack11llll11_opy_
  global bstack1l1l11l1l_opy_
  global bstack11ll1l1ll_opy_
  global bstack1l1111l1_opy_
  try:
    from selenium import webdriver
    from selenium.webdriver.remote.webdriver import WebDriver
    bstack1l111l1l_opy_ = webdriver.Remote.__init__
    bstack1l1l1l1ll_opy_ = WebDriver.quit
    bstack1l111lll1_opy_ = WebDriver.close
    bstack1l11l1l11_opy_ = WebDriver.get
  except Exception as e:
    pass
  if bstack1l11l111l_opy_(CONFIG) and bstack11l111lll_opy_():
    if bstack1llll1lll_opy_() < version.parse(bstack1ll1l11ll1_opy_):
      logger.error(bstack11l1111l1_opy_.format(bstack1llll1lll_opy_()))
    else:
      try:
        from selenium.webdriver.remote.remote_connection import RemoteConnection
        bstack11llll11_opy_ = RemoteConnection._get_proxy_url
      except Exception as e:
        logger.error(bstack1ll11l11ll_opy_.format(str(e)))
  try:
    from _pytest.config import Config
    bstack1l1l11l1l_opy_ = Config.getoption
    from _pytest import runner
    bstack11ll1l1ll_opy_ = runner._update_current_test_var
  except Exception as e:
    logger.warn(e, bstack1l1l1111l_opy_)
  try:
    from pytest_bdd import reporting
    bstack1l1111l1_opy_ = reporting.runtest_makereport
  except Exception as e:
    logger.debug(bstack11l1l1l_opy_ (u"ࠧࡑ࡮ࡨࡥࡸ࡫ࠠࡪࡰࡶࡸࡦࡲ࡬ࠡࡲࡼࡸࡪࡹࡴ࠮ࡤࡧࡨࠥࡺ࡯ࠡࡴࡸࡲࠥࡶࡹࡵࡧࡶࡸ࠲ࡨࡤࡥࠢࡷࡩࡸࡺࡳࠨ୵"))
  bstack11l111111_opy_ = CONFIG.get(bstack11l1l1l_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡕࡷࡥࡨࡱࡌࡰࡥࡤࡰࡔࡶࡴࡪࡱࡱࡷࠬ୶"), {}).get(bstack11l1l1l_opy_ (u"ࠩ࡯ࡳࡨࡧ࡬ࡊࡦࡨࡲࡹ࡯ࡦࡪࡧࡵࠫ୷"))
  bstack1l1l1l1l1_opy_ = True
  bstack1l1l1l111_opy_(bstack1ll111llll_opy_)
  os.environ[bstack11l1l1l_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡘࡗࡊࡘࡎࡂࡏࡈࠫ୸")] = CONFIG[bstack11l1l1l_opy_ (u"ࠫࡺࡹࡥࡳࡐࡤࡱࡪ࠭୹")]
  os.environ[bstack11l1l1l_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣࡆࡉࡃࡆࡕࡖࡣࡐࡋ࡙ࠨ୺")] = CONFIG[bstack11l1l1l_opy_ (u"࠭ࡡࡤࡥࡨࡷࡸࡑࡥࡺࠩ୻")]
  os.environ[bstack11l1l1l_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡁࡖࡖࡒࡑࡆ࡚ࡉࡐࡐࠪ୼")] = bstack11l1l1ll1_opy_.__str__()
  from _pytest.config import main as bstack1ll1llll1_opy_
  bstack1ll1llll1_opy_(arg)
  if bstack11l1l1l_opy_ (u"ࠨࡤࡶࡸࡦࡩ࡫ࡠࡧࡵࡶࡴࡸ࡟࡭࡫ࡶࡸࠬ୽") in multiprocessing.current_process().__dict__.keys():
    for bstack1lll1l11l1_opy_ in multiprocessing.current_process().bstack_error_list:
      bstack1ll111ll_opy_.append(bstack1lll1l11l1_opy_)
def bstack111ll111_opy_(arg):
  bstack1l1l1l111_opy_(bstack111l1ll11_opy_)
  os.environ[bstack11l1l1l_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡋࡖࡣࡆࡖࡐࡠࡃࡘࡘࡔࡓࡁࡕࡇࠪ୾")] = str(bstack1lll1l111_opy_)
  from behave.__main__ import main as bstack111111l1_opy_
  bstack111111l1_opy_(arg)
def bstack1l111111_opy_():
  logger.info(bstack11llll1ll_opy_)
  import argparse
  parser = argparse.ArgumentParser()
  parser.add_argument(bstack11l1l1l_opy_ (u"ࠪࡷࡪࡺࡵࡱࠩ୿"), help=bstack11l1l1l_opy_ (u"ࠫࡌ࡫࡮ࡦࡴࡤࡸࡪࠦࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࠥࡩ࡯࡯ࡨ࡬࡫ࠬ஀"))
  parser.add_argument(bstack11l1l1l_opy_ (u"ࠬ࠳ࡵࠨ஁"), bstack11l1l1l_opy_ (u"࠭࠭࠮ࡷࡶࡩࡷࡴࡡ࡮ࡧࠪஂ"), help=bstack11l1l1l_opy_ (u"࡚ࠧࡱࡸࡶࠥࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࠤࡺࡹࡥࡳࡰࡤࡱࡪ࠭ஃ"))
  parser.add_argument(bstack11l1l1l_opy_ (u"ࠨ࠯࡮ࠫ஄"), bstack11l1l1l_opy_ (u"ࠩ࠰࠱ࡰ࡫ࡹࠨஅ"), help=bstack11l1l1l_opy_ (u"ࠪ࡝ࡴࡻࡲࠡࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱࠠࡢࡥࡦࡩࡸࡹࠠ࡬ࡧࡼࠫஆ"))
  parser.add_argument(bstack11l1l1l_opy_ (u"ࠫ࠲࡬ࠧஇ"), bstack11l1l1l_opy_ (u"ࠬ࠳࠭ࡧࡴࡤࡱࡪࡽ࡯ࡳ࡭ࠪஈ"), help=bstack11l1l1l_opy_ (u"࡙࠭ࡰࡷࡵࠤࡹ࡫ࡳࡵࠢࡩࡶࡦࡳࡥࡸࡱࡵ࡯ࠬஉ"))
  bstack1ll11l1l_opy_ = parser.parse_args()
  try:
    bstack11ll111l_opy_ = bstack11l1l1l_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠴ࡧࡦࡰࡨࡶ࡮ࡩ࠮ࡺ࡯࡯࠲ࡸࡧ࡭ࡱ࡮ࡨࠫஊ")
    if bstack1ll11l1l_opy_.framework and bstack1ll11l1l_opy_.framework not in (bstack11l1l1l_opy_ (u"ࠨࡲࡼࡸ࡭ࡵ࡮ࠨ஋"), bstack11l1l1l_opy_ (u"ࠩࡳࡽࡹ࡮࡯࡯࠵ࠪ஌")):
      bstack11ll111l_opy_ = bstack11l1l1l_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬࠰ࡩࡶࡦࡳࡥࡸࡱࡵ࡯࠳ࡿ࡭࡭࠰ࡶࡥࡲࡶ࡬ࡦࠩ஍")
    bstack1ll1llllll_opy_ = os.path.join(os.path.dirname(os.path.realpath(__file__)), bstack11ll111l_opy_)
    bstack1llll11l11_opy_ = open(bstack1ll1llllll_opy_, bstack11l1l1l_opy_ (u"ࠫࡷ࠭எ"))
    bstack1l1ll1l11_opy_ = bstack1llll11l11_opy_.read()
    bstack1llll11l11_opy_.close()
    if bstack1ll11l1l_opy_.username:
      bstack1l1ll1l11_opy_ = bstack1l1ll1l11_opy_.replace(bstack11l1l1l_opy_ (u"ࠬ࡟ࡏࡖࡔࡢ࡙ࡘࡋࡒࡏࡃࡐࡉࠬஏ"), bstack1ll11l1l_opy_.username)
    if bstack1ll11l1l_opy_.key:
      bstack1l1ll1l11_opy_ = bstack1l1ll1l11_opy_.replace(bstack11l1l1l_opy_ (u"࡙࠭ࡐࡗࡕࡣࡆࡉࡃࡆࡕࡖࡣࡐࡋ࡙ࠨஐ"), bstack1ll11l1l_opy_.key)
    if bstack1ll11l1l_opy_.framework:
      bstack1l1ll1l11_opy_ = bstack1l1ll1l11_opy_.replace(bstack11l1l1l_opy_ (u"࡚ࠧࡑࡘࡖࡤࡌࡒࡂࡏࡈ࡛ࡔࡘࡋࠨ஑"), bstack1ll11l1l_opy_.framework)
    file_name = bstack11l1l1l_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠮ࡺ࡯࡯ࠫஒ")
    file_path = os.path.abspath(file_name)
    bstack1l1ll1l11l_opy_ = open(file_path, bstack11l1l1l_opy_ (u"ࠩࡺࠫஓ"))
    bstack1l1ll1l11l_opy_.write(bstack1l1ll1l11_opy_)
    bstack1l1ll1l11l_opy_.close()
    logger.info(bstack1ll11ll1l_opy_)
    try:
      os.environ[bstack11l1l1l_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡉࡖࡆࡓࡅࡘࡑࡕࡏࠬஔ")] = bstack1ll11l1l_opy_.framework if bstack1ll11l1l_opy_.framework != None else bstack11l1l1l_opy_ (u"ࠦࠧக")
      config = yaml.safe_load(bstack1l1ll1l11_opy_)
      config[bstack11l1l1l_opy_ (u"ࠬࡹ࡯ࡶࡴࡦࡩࠬ஖")] = bstack11l1l1l_opy_ (u"࠭ࡰࡺࡶ࡫ࡳࡳ࠳ࡳࡦࡶࡸࡴࠬ஗")
      bstack11l1l1ll_opy_(bstack1ll1lll111_opy_, config)
    except Exception as e:
      logger.debug(bstack1lllll1l1l_opy_.format(str(e)))
  except Exception as e:
    logger.error(bstack1l11l11l1_opy_.format(str(e)))
def bstack11l1l1ll_opy_(bstack1llll1111l_opy_, config, bstack1lll1l1l11_opy_={}):
  global bstack11l1l1ll1_opy_
  global bstack11l1l111_opy_
  if not config:
    return
  bstack111l1l1l_opy_ = bstack1lll1ll1ll_opy_ if not bstack11l1l1ll1_opy_ else (
    bstack1ll11ll11l_opy_ if bstack11l1l1l_opy_ (u"ࠧࡢࡲࡳࠫ஘") in config else bstack1llllll11_opy_)
  data = {
    bstack11l1l1l_opy_ (u"ࠨࡷࡶࡩࡷࡔࡡ࡮ࡧࠪங"): config[bstack11l1l1l_opy_ (u"ࠩࡸࡷࡪࡸࡎࡢ࡯ࡨࠫச")],
    bstack11l1l1l_opy_ (u"ࠪࡥࡨࡩࡥࡴࡵࡎࡩࡾ࠭஛"): config[bstack11l1l1l_opy_ (u"ࠫࡦࡩࡣࡦࡵࡶࡏࡪࡿࠧஜ")],
    bstack11l1l1l_opy_ (u"ࠬ࡫ࡶࡦࡰࡷࡣࡹࡿࡰࡦࠩ஝"): bstack1llll1111l_opy_,
    bstack11l1l1l_opy_ (u"࠭ࡤࡦࡶࡨࡧࡹ࡫ࡤࡇࡴࡤࡱࡪࡽ࡯ࡳ࡭ࠪஞ"): os.environ.get(bstack11l1l1l_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡆࡓࡃࡐࡉ࡜ࡕࡒࡌࠩட"), bstack11l1l111_opy_),
    bstack11l1l1l_opy_ (u"ࠨࡤࡸ࡭ࡱࡪ࡟ࡩࡣࡶ࡬ࡪࡪ࡟ࡪࡦࠪ஠"): bstack1lllllll1l_opy_,
    bstack11l1l1l_opy_ (u"ࠩࡲࡴࡹ࡯࡭ࡢ࡮ࡢ࡬ࡺࡨ࡟ࡶࡴ࡯ࠫ஡"): bstack11l11ll11_opy_(),
    bstack11l1l1l_opy_ (u"ࠪࡩࡻ࡫࡮ࡵࡡࡳࡶࡴࡶࡥࡳࡶ࡬ࡩࡸ࠭஢"): {
      bstack11l1l1l_opy_ (u"ࠫࡱࡧ࡮ࡨࡷࡤ࡫ࡪࡥࡦࡳࡣࡰࡩࡼࡵࡲ࡬ࠩண"): str(config[bstack11l1l1l_opy_ (u"ࠬࡹ࡯ࡶࡴࡦࡩࠬத")]) if bstack11l1l1l_opy_ (u"࠭ࡳࡰࡷࡵࡧࡪ࠭஥") in config else bstack11l1l1l_opy_ (u"ࠢࡶࡰ࡮ࡲࡴࡽ࡮ࠣ஦"),
      bstack11l1l1l_opy_ (u"ࠨࡴࡨࡪࡪࡸࡲࡦࡴࠪ஧"): bstack1llll11lll_opy_(os.getenv(bstack11l1l1l_opy_ (u"ࠤࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡈࡕࡅࡒࡋࡗࡐࡔࡎࠦந"), bstack11l1l1l_opy_ (u"ࠥࠦன"))),
      bstack11l1l1l_opy_ (u"ࠫࡱࡧ࡮ࡨࡷࡤ࡫ࡪ࠭ப"): bstack11l1l1l_opy_ (u"ࠬࡶࡹࡵࡪࡲࡲࠬ஫"),
      bstack11l1l1l_opy_ (u"࠭ࡰࡳࡱࡧࡹࡨࡺࠧ஬"): bstack111l1l1l_opy_,
      bstack11l1l1l_opy_ (u"ࠧࡣࡷ࡬ࡰࡩࡔࡡ࡮ࡧࠪ஭"): config[bstack11l1l1l_opy_ (u"ࠨࡤࡸ࡭ࡱࡪࡎࡢ࡯ࡨࠫம")] if config[bstack11l1l1l_opy_ (u"ࠩࡥࡹ࡮ࡲࡤࡏࡣࡰࡩࠬய")] else bstack11l1l1l_opy_ (u"ࠥࡹࡳࡱ࡮ࡰࡹࡱࠦர"),
      bstack11l1l1l_opy_ (u"ࠫࡧࡻࡩ࡭ࡦࡌࡨࡪࡴࡴࡪࡨ࡬ࡩࡷ࠭ற"): str(config[bstack11l1l1l_opy_ (u"ࠬࡨࡵࡪ࡮ࡧࡍࡩ࡫࡮ࡵ࡫ࡩ࡭ࡪࡸࠧல")]) if bstack11l1l1l_opy_ (u"࠭ࡢࡶ࡫࡯ࡨࡎࡪࡥ࡯ࡶ࡬ࡪ࡮࡫ࡲࠨள") in config else bstack11l1l1l_opy_ (u"ࠢࡶࡰ࡮ࡲࡴࡽ࡮ࠣழ"),
      bstack11l1l1l_opy_ (u"ࠨࡱࡶࠫவ"): sys.platform,
      bstack11l1l1l_opy_ (u"ࠩ࡫ࡳࡸࡺ࡮ࡢ࡯ࡨࠫஶ"): socket.gethostname()
    }
  }
  update(data[bstack11l1l1l_opy_ (u"ࠪࡩࡻ࡫࡮ࡵࡡࡳࡶࡴࡶࡥࡳࡶ࡬ࡩࡸ࠭ஷ")], bstack1lll1l1l11_opy_)
  try:
    response = bstack1ll11l1111_opy_(bstack11l1l1l_opy_ (u"ࠫࡕࡕࡓࡕࠩஸ"), bstack1llllll1l1_opy_(bstack1l111111l_opy_), data, {
      bstack11l1l1l_opy_ (u"ࠬࡧࡵࡵࡪࠪஹ"): (config[bstack11l1l1l_opy_ (u"࠭ࡵࡴࡧࡵࡒࡦࡳࡥࠨ஺")], config[bstack11l1l1l_opy_ (u"ࠧࡢࡥࡦࡩࡸࡹࡋࡦࡻࠪ஻")])
    })
    if response:
      logger.debug(bstack111ll11l1_opy_.format(bstack1llll1111l_opy_, str(response.json())))
  except Exception as e:
    logger.debug(bstack11l11ll1l_opy_.format(str(e)))
def bstack1llll11lll_opy_(framework):
  return bstack11l1l1l_opy_ (u"ࠣࡽࢀ࠱ࡵࡿࡴࡩࡱࡱࡥ࡬࡫࡮ࡵ࠱ࡾࢁࠧ஼").format(str(framework), __version__) if framework else bstack11l1l1l_opy_ (u"ࠤࡳࡽࡹ࡮࡯࡯ࡣࡪࡩࡳࡺ࠯ࡼࡿࠥ஽").format(
    __version__)
def bstack1llllllll1_opy_():
  global CONFIG
  if bool(CONFIG):
    return
  try:
    bstack1l11111l1_opy_()
    logger.debug(bstack11111l1ll_opy_.format(str(CONFIG)))
    bstack1111ll1l1_opy_()
    bstack1l11l11ll_opy_()
  except Exception as e:
    logger.error(bstack11l1l1l_opy_ (u"ࠥࡊࡦ࡯࡬ࡦࡦࠣࡸࡴࠦࡳࡦࡶࡸࡴ࠱ࠦࡥࡳࡴࡲࡶ࠿ࠦࠢா") + str(e))
    sys.exit(1)
  sys.excepthook = bstack1lllllll1_opy_
  atexit.register(bstack111111ll1_opy_)
  signal.signal(signal.SIGINT, bstack1l111l1l1_opy_)
  signal.signal(signal.SIGTERM, bstack1l111l1l1_opy_)
def bstack1lllllll1_opy_(exctype, value, traceback):
  global bstack11111lll1_opy_
  try:
    for driver in bstack11111lll1_opy_:
      driver.execute_script(
        bstack11l1l1l_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࡢࡩࡽ࡫ࡣࡶࡶࡲࡶ࠿ࠦࡻࠣࡣࡦࡸ࡮ࡵ࡮ࠣ࠼ࠣࠦࡸ࡫ࡴࡔࡧࡶࡷ࡮ࡵ࡮ࡔࡶࡤࡸࡺࡹࠢ࠭ࠢࠥࡥࡷ࡭ࡵ࡮ࡧࡱࡸࡸࠨ࠺ࠡࡽࠥࡷࡹࡧࡴࡶࡵࠥ࠾ࠧ࡬ࡡࡪ࡮ࡨࡨࠧ࠲ࠠࠣࡴࡨࡥࡸࡵ࡮ࠣ࠼ࠣࠫி") + json.dumps(
          bstack11l1l1l_opy_ (u"࡙ࠧࡥࡴࡵ࡬ࡳࡳࠦࡦࡢ࡫࡯ࡩࡩࠦࡷࡪࡶ࡫࠾ࠥࡢ࡮ࠣீ") + str(value)) + bstack11l1l1l_opy_ (u"࠭ࡽࡾࠩு"))
  except Exception:
    pass
  bstack1l1111l1l_opy_(value)
  sys.__excepthook__(exctype, value, traceback)
  sys.exit(1)
def bstack1l1111l1l_opy_(message=bstack11l1l1l_opy_ (u"ࠧࠨூ")):
  global CONFIG
  try:
    if message:
      bstack1lll1l1l11_opy_ = {
        bstack11l1l1l_opy_ (u"ࠨࡧࡵࡶࡴࡸࠧ௃"): str(message)
      }
      bstack11l1l1ll_opy_(bstack1llll1lll1_opy_, CONFIG, bstack1lll1l1l11_opy_)
    else:
      bstack11l1l1ll_opy_(bstack1llll1lll1_opy_, CONFIG)
  except Exception as e:
    logger.debug(bstack11ll11l11_opy_.format(str(e)))
def bstack1lll111111_opy_(bstack1l1llllll_opy_, size):
  bstack11l1l1l1l_opy_ = []
  while len(bstack1l1llllll_opy_) > size:
    bstack11ll1ll1l_opy_ = bstack1l1llllll_opy_[:size]
    bstack11l1l1l1l_opy_.append(bstack11ll1ll1l_opy_)
    bstack1l1llllll_opy_ = bstack1l1llllll_opy_[size:]
  bstack11l1l1l1l_opy_.append(bstack1l1llllll_opy_)
  return bstack11l1l1l1l_opy_
def bstack11l1ll1ll_opy_(args):
  if bstack11l1l1l_opy_ (u"ࠩ࠰ࡱࠬ௄") in args and bstack11l1l1l_opy_ (u"ࠪࡴࡩࡨࠧ௅") in args:
    return True
  return False
def run_on_browserstack(bstack1111111l_opy_=None, bstack1ll111ll_opy_=None, bstack11l11l1l1_opy_=False):
  global CONFIG
  global bstack1l1ll1ll1l_opy_
  global bstack1lll1l111_opy_
  global bstack11l1l111_opy_
  bstack1lll1l1l_opy_ = bstack11l1l1l_opy_ (u"ࠫࠬெ")
  bstack111l1llll_opy_(bstack111ll111l_opy_, logger)
  if bstack1111111l_opy_ and isinstance(bstack1111111l_opy_, str):
    bstack1111111l_opy_ = eval(bstack1111111l_opy_)
  if bstack1111111l_opy_:
    CONFIG = bstack1111111l_opy_[bstack11l1l1l_opy_ (u"ࠬࡉࡏࡏࡈࡌࡋࠬே")]
    bstack1l1ll1ll1l_opy_ = bstack1111111l_opy_[bstack11l1l1l_opy_ (u"࠭ࡈࡖࡄࡢ࡙ࡗࡒࠧை")]
    bstack1lll1l111_opy_ = bstack1111111l_opy_[bstack11l1l1l_opy_ (u"ࠧࡊࡕࡢࡅࡕࡖ࡟ࡂࡗࡗࡓࡒࡇࡔࡆࠩ௉")]
    bstack1lllll111l_opy_.bstack1lllll1ll_opy_(bstack11l1l1l_opy_ (u"ࠨࡋࡖࡣࡆࡖࡐࡠࡃࡘࡘࡔࡓࡁࡕࡇࠪொ"), bstack1lll1l111_opy_)
    bstack1lll1l1l_opy_ = bstack11l1l1l_opy_ (u"ࠩࡳࡽࡹ࡮࡯࡯ࠩோ")
  if not bstack11l11l1l1_opy_:
    if len(sys.argv) <= 1:
      logger.critical(bstack111lll111_opy_)
      return
    if sys.argv[1] == bstack11l1l1l_opy_ (u"ࠪ࠱࠲ࡼࡥࡳࡵ࡬ࡳࡳ࠭ௌ") or sys.argv[1] == bstack11l1l1l_opy_ (u"ࠫ࠲ࡼ்ࠧ"):
      logger.info(bstack11l1l1l_opy_ (u"ࠬࡈࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࠤࡕࡿࡴࡩࡱࡱࠤࡘࡊࡋࠡࡸࡾࢁࠬ௎").format(__version__))
      return
    if sys.argv[1] == bstack11l1l1l_opy_ (u"࠭ࡳࡦࡶࡸࡴࠬ௏"):
      bstack1l111111_opy_()
      return
  args = sys.argv
  bstack1llllllll1_opy_()
  global bstack1ll1111l11_opy_
  global bstack111lll1ll_opy_
  global bstack1l1l1l1l1_opy_
  global bstack1l1lll1l11_opy_
  global bstack1llll111l_opy_
  global bstack11l111111_opy_
  global bstack1l1llllll1_opy_
  global bstack11ll1l1l1_opy_
  global bstack1llll1l11l_opy_
  global bstack1l1l11lll_opy_
  global bstack1ll11ll111_opy_
  bstack111lll1ll_opy_ = len(CONFIG[bstack11l1l1l_opy_ (u"ࠧࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࡵࠪௐ")])
  if not bstack1lll1l1l_opy_:
    if args[1] == bstack11l1l1l_opy_ (u"ࠨࡲࡼࡸ࡭ࡵ࡮ࠨ௑") or args[1] == bstack11l1l1l_opy_ (u"ࠩࡳࡽࡹ࡮࡯࡯࠵ࠪ௒"):
      bstack1lll1l1l_opy_ = bstack11l1l1l_opy_ (u"ࠪࡴࡾࡺࡨࡰࡰࠪ௓")
      args = args[2:]
    elif args[1] == bstack11l1l1l_opy_ (u"ࠫࡷࡵࡢࡰࡶࠪ௔"):
      bstack1lll1l1l_opy_ = bstack11l1l1l_opy_ (u"ࠬࡸ࡯ࡣࡱࡷࠫ௕")
      args = args[2:]
    elif args[1] == bstack11l1l1l_opy_ (u"࠭ࡰࡢࡤࡲࡸࠬ௖"):
      bstack1lll1l1l_opy_ = bstack11l1l1l_opy_ (u"ࠧࡱࡣࡥࡳࡹ࠭ௗ")
      args = args[2:]
    elif args[1] == bstack11l1l1l_opy_ (u"ࠨࡴࡲࡦࡴࡺ࠭ࡪࡰࡷࡩࡷࡴࡡ࡭ࠩ௘"):
      bstack1lll1l1l_opy_ = bstack11l1l1l_opy_ (u"ࠩࡵࡳࡧࡵࡴ࠮࡫ࡱࡸࡪࡸ࡮ࡢ࡮ࠪ௙")
      args = args[2:]
    elif args[1] == bstack11l1l1l_opy_ (u"ࠪࡴࡾࡺࡥࡴࡶࠪ௚"):
      bstack1lll1l1l_opy_ = bstack11l1l1l_opy_ (u"ࠫࡵࡿࡴࡦࡵࡷࠫ௛")
      args = args[2:]
    elif args[1] == bstack11l1l1l_opy_ (u"ࠬࡨࡥࡩࡣࡹࡩࠬ௜"):
      bstack1lll1l1l_opy_ = bstack11l1l1l_opy_ (u"࠭ࡢࡦࡪࡤࡺࡪ࠭௝")
      args = args[2:]
    else:
      if not bstack11l1l1l_opy_ (u"ࠧࡧࡴࡤࡱࡪࡽ࡯ࡳ࡭ࠪ௞") in CONFIG or str(CONFIG[bstack11l1l1l_opy_ (u"ࠨࡨࡵࡥࡲ࡫ࡷࡰࡴ࡮ࠫ௟")]).lower() in [bstack11l1l1l_opy_ (u"ࠩࡳࡽࡹ࡮࡯࡯ࠩ௠"), bstack11l1l1l_opy_ (u"ࠪࡴࡾࡺࡨࡰࡰ࠶ࠫ௡")]:
        bstack1lll1l1l_opy_ = bstack11l1l1l_opy_ (u"ࠫࡵࡿࡴࡩࡱࡱࠫ௢")
        args = args[1:]
      elif str(CONFIG[bstack11l1l1l_opy_ (u"ࠬ࡬ࡲࡢ࡯ࡨࡻࡴࡸ࡫ࠨ௣")]).lower() == bstack11l1l1l_opy_ (u"࠭ࡲࡰࡤࡲࡸࠬ௤"):
        bstack1lll1l1l_opy_ = bstack11l1l1l_opy_ (u"ࠧࡳࡱࡥࡳࡹ࠭௥")
        args = args[1:]
      elif str(CONFIG[bstack11l1l1l_opy_ (u"ࠨࡨࡵࡥࡲ࡫ࡷࡰࡴ࡮ࠫ௦")]).lower() == bstack11l1l1l_opy_ (u"ࠩࡳࡥࡧࡵࡴࠨ௧"):
        bstack1lll1l1l_opy_ = bstack11l1l1l_opy_ (u"ࠪࡴࡦࡨ࡯ࡵࠩ௨")
        args = args[1:]
      elif str(CONFIG[bstack11l1l1l_opy_ (u"ࠫ࡫ࡸࡡ࡮ࡧࡺࡳࡷࡱࠧ௩")]).lower() == bstack11l1l1l_opy_ (u"ࠬࡶࡹࡵࡧࡶࡸࠬ௪"):
        bstack1lll1l1l_opy_ = bstack11l1l1l_opy_ (u"࠭ࡰࡺࡶࡨࡷࡹ࠭௫")
        args = args[1:]
      elif str(CONFIG[bstack11l1l1l_opy_ (u"ࠧࡧࡴࡤࡱࡪࡽ࡯ࡳ࡭ࠪ௬")]).lower() == bstack11l1l1l_opy_ (u"ࠨࡤࡨ࡬ࡦࡼࡥࠨ௭"):
        bstack1lll1l1l_opy_ = bstack11l1l1l_opy_ (u"ࠩࡥࡩ࡭ࡧࡶࡦࠩ௮")
        args = args[1:]
      else:
        os.environ[bstack11l1l1l_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡉࡖࡆࡓࡅࡘࡑࡕࡏࠬ௯")] = bstack1lll1l1l_opy_
        bstack111l1l111_opy_(bstack111l1lll1_opy_)
  os.environ[bstack11l1l1l_opy_ (u"ࠫࡋࡘࡁࡎࡇ࡚ࡓࡗࡑ࡟ࡖࡕࡈࡈࠬ௰")] = bstack1lll1l1l_opy_
  bstack11l1l111_opy_ = bstack1lll1l1l_opy_
  global bstack1lll111l1_opy_
  if bstack1111111l_opy_:
    try:
      os.environ[bstack11l1l1l_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣࡋࡘࡁࡎࡇ࡚ࡓࡗࡑࠧ௱")] = bstack1lll1l1l_opy_
      bstack11l1l1ll_opy_(bstack1ll11111l_opy_, CONFIG)
    except Exception as e:
      logger.debug(bstack11ll11l11_opy_.format(str(e)))
  global bstack1l111l1l_opy_
  global bstack1l1l1l1ll_opy_
  global bstack1l11lll11_opy_
  global bstack1ll1ll111_opy_
  global bstack1l1l1l11l_opy_
  global bstack1l11111ll_opy_
  global bstack1ll111l1ll_opy_
  global bstack1lll1lllll_opy_
  global bstack1lll11ll1_opy_
  global bstack1ll1lllll_opy_
  global bstack1l111lll1_opy_
  global bstack1ll1l1l1ll_opy_
  global bstack1lll1l11ll_opy_
  global bstack1l11l1l11_opy_
  global bstack11llll11_opy_
  global bstack1l1l11l1l_opy_
  global bstack11ll1l1ll_opy_
  global bstack1ll111l11l_opy_
  global bstack1l1111l1_opy_
  global bstack1l111l1ll_opy_
  try:
    from selenium import webdriver
    from selenium.webdriver.remote.webdriver import WebDriver
    bstack1l111l1l_opy_ = webdriver.Remote.__init__
    bstack1l1l1l1ll_opy_ = WebDriver.quit
    bstack1l111lll1_opy_ = WebDriver.close
    bstack1l11l1l11_opy_ = WebDriver.get
    bstack1l111l1ll_opy_ = WebDriver.execute
  except Exception as e:
    pass
  try:
    import Browser
    from subprocess import Popen
    bstack1lll111l1_opy_ = Popen.__init__
  except Exception as e:
    pass
  if bstack1l11l111l_opy_(CONFIG) and bstack11l111lll_opy_():
    if bstack1llll1lll_opy_() < version.parse(bstack1ll1l11ll1_opy_):
      logger.error(bstack11l1111l1_opy_.format(bstack1llll1lll_opy_()))
    else:
      try:
        from selenium.webdriver.remote.remote_connection import RemoteConnection
        bstack11llll11_opy_ = RemoteConnection._get_proxy_url
      except Exception as e:
        logger.error(bstack1ll11l11ll_opy_.format(str(e)))
  if bstack1lll1l1l_opy_ != bstack11l1l1l_opy_ (u"࠭ࡰࡺࡶ࡫ࡳࡳ࠭௲") or (bstack1lll1l1l_opy_ == bstack11l1l1l_opy_ (u"ࠧࡱࡻࡷ࡬ࡴࡴࠧ௳") and not bstack1111111l_opy_):
    bstack1ll11l1l1_opy_()
  if (bstack1lll1l1l_opy_ in [bstack11l1l1l_opy_ (u"ࠨࡲࡤࡦࡴࡺࠧ௴"), bstack11l1l1l_opy_ (u"ࠩࡵࡳࡧࡵࡴࠨ௵"), bstack11l1l1l_opy_ (u"ࠪࡶࡴࡨ࡯ࡵ࠯࡬ࡲࡹ࡫ࡲ࡯ࡣ࡯ࠫ௶")]):
    try:
      from robot import run_cli
      from robot.output import Output
      from robot.running.status import TestStatus
      from pabot.pabot import QueueItem
      from pabot import pabot
      try:
        from SeleniumLibrary.keywords.webdrivertools.webdrivertools import WebDriverCreator
        from SeleniumLibrary.keywords.webdrivertools.webdrivertools import WebDriverCache
        WebDriverCreator._get_ff_profile = bstack1111lll11_opy_
        bstack1l1l1l11l_opy_ = WebDriverCache.close
      except Exception as e:
        logger.warn(bstack1ll1l11l1l_opy_ + str(e))
      try:
        from AppiumLibrary.utils.applicationcache import ApplicationCache
        bstack1ll1ll111_opy_ = ApplicationCache.close
      except Exception as e:
        logger.debug(bstack1ll1l1ll11_opy_ + str(e))
    except Exception as e:
      bstack1111l111l_opy_(e, bstack1ll1l11l1l_opy_)
    if bstack1lll1l1l_opy_ != bstack11l1l1l_opy_ (u"ࠫࡷࡵࡢࡰࡶ࠰࡭ࡳࡺࡥࡳࡰࡤࡰࠬ௷"):
      bstack1llll1l111_opy_()
    bstack1l11lll11_opy_ = Output.end_test
    bstack1l11111ll_opy_ = TestStatus.__init__
    bstack1lll1lllll_opy_ = pabot._run
    bstack1lll11ll1_opy_ = QueueItem.__init__
    bstack1ll1lllll_opy_ = pabot._create_command_for_execution
    bstack1ll111l11l_opy_ = pabot._report_results
  if bstack1lll1l1l_opy_ == bstack11l1l1l_opy_ (u"ࠬࡨࡥࡩࡣࡹࡩࠬ௸"):
    try:
      from behave.runner import Runner
      from behave.model import Step
    except Exception as e:
      bstack1111l111l_opy_(e, bstack1lll11ll11_opy_)
    bstack1ll1l1l1ll_opy_ = Runner.run_hook
    bstack1lll1l11ll_opy_ = Step.run
  if bstack1lll1l1l_opy_ == bstack11l1l1l_opy_ (u"࠭ࡰࡺࡶࡨࡷࡹ࠭௹"):
    try:
      from _pytest.config import Config
      bstack1l1l11l1l_opy_ = Config.getoption
      from _pytest import runner
      bstack11ll1l1ll_opy_ = runner._update_current_test_var
    except Exception as e:
      logger.warn(e, bstack1l1l1111l_opy_)
    try:
      from pytest_bdd import reporting
      bstack1l1111l1_opy_ = reporting.runtest_makereport
    except Exception as e:
      logger.debug(bstack11l1l1l_opy_ (u"ࠧࡑ࡮ࡨࡥࡸ࡫ࠠࡪࡰࡶࡸࡦࡲ࡬ࠡࡲࡼࡸࡪࡹࡴ࠮ࡤࡧࡨࠥࡺ࡯ࠡࡴࡸࡲࠥࡶࡹࡵࡧࡶࡸ࠲ࡨࡤࡥࠢࡷࡩࡸࡺࡳࠨ௺"))
  if bstack1lll1l1l_opy_ in bstack1llll1ll1_opy_:
    try:
      framework_name = bstack11l1l1l_opy_ (u"ࠨࡔࡲࡦࡴࡺࠧ௻") if bstack1lll1l1l_opy_ in [bstack11l1l1l_opy_ (u"ࠩࡳࡥࡧࡵࡴࠨ௼"), bstack11l1l1l_opy_ (u"ࠪࡶࡴࡨ࡯ࡵࠩ௽"), bstack11l1l1l_opy_ (u"ࠫࡷࡵࡢࡰࡶ࠰࡭ࡳࡺࡥࡳࡰࡤࡰࠬ௾")] else bstack1llll1l1l1_opy_(bstack1lll1l1l_opy_)
      bstack1l11l11l_opy_.launch(CONFIG, {
        bstack11l1l1l_opy_ (u"ࠬ࡬ࡲࡢ࡯ࡨࡻࡴࡸ࡫ࡠࡰࡤࡱࡪ࠭௿"): bstack11l1l1l_opy_ (u"࠭ࡻ࠱ࡿ࠰ࡧࡺࡩࡵ࡮ࡤࡨࡶࠬఀ").format(framework_name) if bstack1lll1l1l_opy_ == bstack11l1l1l_opy_ (u"ࠧࡱࡻࡷࡩࡸࡺࠧఁ") and bstack11ll1111_opy_() else framework_name,
        bstack11l1l1l_opy_ (u"ࠨࡨࡵࡥࡲ࡫ࡷࡰࡴ࡮ࡣࡻ࡫ࡲࡴ࡫ࡲࡲࠬం"): bstack1lll1ll111_opy_(framework_name),
        bstack11l1l1l_opy_ (u"ࠩࡶࡨࡰࡥࡶࡦࡴࡶ࡭ࡴࡴࠧః"): __version__
      })
    except Exception as e:
      logger.debug(bstack11ll1l1l_opy_.format(bstack11l1l1l_opy_ (u"ࠪࡓࡧࡹࡥࡳࡸࡤࡦ࡮ࡲࡩࡵࡻࠪఄ"), str(e)))
  if bstack1lll1l1l_opy_ in bstack1111lllll_opy_:
    try:
      framework_name = bstack11l1l1l_opy_ (u"ࠫࡷࡵࡢࡰࡶࠪఅ") if bstack1lll1l1l_opy_ in [bstack11l1l1l_opy_ (u"ࠬࡶࡡࡣࡱࡷࠫఆ"), bstack11l1l1l_opy_ (u"࠭ࡲࡰࡤࡲࡸࠬఇ")] else bstack1lll1l1l_opy_
      if bstack11l1l1ll1_opy_ and bstack11l1l1l_opy_ (u"ࠧࡢࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿࠧఈ") in CONFIG and CONFIG[bstack11l1l1l_opy_ (u"ࠨࡣࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࠨఉ")] == True:
        if bstack11l1l1l_opy_ (u"ࠩࡤࡧࡨ࡫ࡳࡴ࡫ࡥ࡭ࡱ࡯ࡴࡺࡑࡳࡸ࡮ࡵ࡮ࡴࠩఊ") in CONFIG:
          os.environ[bstack11l1l1l_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡗࡉࡘ࡚࡟ࡂࡅࡆࡉࡘ࡙ࡉࡃࡋࡏࡍ࡙࡟࡟ࡄࡑࡑࡊࡎࡍࡕࡓࡃࡗࡍࡔࡔ࡟࡚ࡏࡏࠫఋ")] = os.getenv(bstack11l1l1l_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡘࡊ࡙ࡔࡠࡃࡆࡇࡊ࡙ࡓࡊࡄࡌࡐࡎ࡚࡙ࡠࡅࡒࡒࡋࡏࡇࡖࡔࡄࡘࡎࡕࡎࡠ࡛ࡐࡐࠬఌ"), json.dumps(CONFIG[bstack11l1l1l_opy_ (u"ࠬࡧࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽࡔࡶࡴࡪࡱࡱࡷࠬ఍")]))
          CONFIG[bstack11l1l1l_opy_ (u"࠭ࡡࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾࡕࡰࡵ࡫ࡲࡲࡸ࠭ఎ")].pop(bstack11l1l1l_opy_ (u"ࠧࡪࡰࡦࡰࡺࡪࡥࡕࡣࡪࡷࡎࡴࡔࡦࡵࡷ࡭ࡳ࡭ࡓࡤࡱࡳࡩࠬఏ"), None)
          CONFIG[bstack11l1l1l_opy_ (u"ࠨࡣࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࡐࡲࡷ࡭ࡴࡴࡳࠨఐ")].pop(bstack11l1l1l_opy_ (u"ࠩࡨࡼࡨࡲࡵࡥࡧࡗࡥ࡬ࡹࡉ࡯ࡖࡨࡷࡹ࡯࡮ࡨࡕࡦࡳࡵ࡫ࠧ఑"), None)
        bstack111ll11ll_opy_, bstack11l1ll1l_opy_ = bstack1111ll111_opy_.bstack1l1l11ll1_opy_(CONFIG, bstack1lll1l1l_opy_, bstack1lll1ll111_opy_(framework_name))
        if not bstack111ll11ll_opy_ is None:
          os.environ[bstack11l1l1l_opy_ (u"ࠪࡆࡘࡥࡁ࠲࠳࡜ࡣࡏ࡝ࡔࠨఒ")] = bstack111ll11ll_opy_
          os.environ[bstack11l1l1l_opy_ (u"ࠫࡇ࡙࡟ࡂ࠳࠴࡝ࡤ࡚ࡅࡔࡖࡢࡖ࡚ࡔ࡟ࡊࡆࠪఓ")] = str(bstack11l1ll1l_opy_)
    except Exception as e:
      logger.debug(bstack11ll1l1l_opy_.format(bstack11l1l1l_opy_ (u"ࠬࡇࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽࠬఔ"), str(e)))
  if bstack1lll1l1l_opy_ == bstack11l1l1l_opy_ (u"࠭ࡰࡺࡶ࡫ࡳࡳ࠭క"):
    bstack1l1l1l1l1_opy_ = True
    if bstack1111111l_opy_ and bstack11l11l1l1_opy_:
      bstack11l111111_opy_ = CONFIG.get(bstack11l1l1l_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡔࡶࡤࡧࡰࡒ࡯ࡤࡣ࡯ࡓࡵࡺࡩࡰࡰࡶࠫఖ"), {}).get(bstack11l1l1l_opy_ (u"ࠨ࡮ࡲࡧࡦࡲࡉࡥࡧࡱࡸ࡮࡬ࡩࡦࡴࠪగ"))
      bstack1l1l1l111_opy_(bstack1111ll1l_opy_)
    elif bstack1111111l_opy_:
      bstack11l111111_opy_ = CONFIG.get(bstack11l1l1l_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡖࡸࡦࡩ࡫ࡍࡱࡦࡥࡱࡕࡰࡵ࡫ࡲࡲࡸ࠭ఘ"), {}).get(bstack11l1l1l_opy_ (u"ࠪࡰࡴࡩࡡ࡭ࡋࡧࡩࡳࡺࡩࡧ࡫ࡨࡶࠬఙ"))
      global bstack11111lll1_opy_
      try:
        if bstack11l1ll1ll_opy_(bstack1111111l_opy_[bstack11l1l1l_opy_ (u"ࠫ࡫࡯࡬ࡦࡡࡱࡥࡲ࡫ࠧచ")]) and multiprocessing.current_process().name == bstack11l1l1l_opy_ (u"ࠬ࠶ࠧఛ"):
          bstack1111111l_opy_[bstack11l1l1l_opy_ (u"࠭ࡦࡪ࡮ࡨࡣࡳࡧ࡭ࡦࠩజ")].remove(bstack11l1l1l_opy_ (u"ࠧ࠮࡯ࠪఝ"))
          bstack1111111l_opy_[bstack11l1l1l_opy_ (u"ࠨࡨ࡬ࡰࡪࡥ࡮ࡢ࡯ࡨࠫఞ")].remove(bstack11l1l1l_opy_ (u"ࠩࡳࡨࡧ࠭ట"))
          bstack1111111l_opy_[bstack11l1l1l_opy_ (u"ࠪࡪ࡮ࡲࡥࡠࡰࡤࡱࡪ࠭ఠ")] = bstack1111111l_opy_[bstack11l1l1l_opy_ (u"ࠫ࡫࡯࡬ࡦࡡࡱࡥࡲ࡫ࠧడ")][0]
          with open(bstack1111111l_opy_[bstack11l1l1l_opy_ (u"ࠬ࡬ࡩ࡭ࡧࡢࡲࡦࡳࡥࠨఢ")], bstack11l1l1l_opy_ (u"࠭ࡲࠨణ")) as f:
            bstack1ll11l1ll_opy_ = f.read()
          bstack1ll1ll11l_opy_ = bstack11l1l1l_opy_ (u"ࠢࠣࠤࡩࡶࡴࡳࠠࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰࡥࡳࡥ࡭ࠣ࡭ࡲࡶ࡯ࡳࡶࠣࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࡡ࡬ࡲ࡮ࡺࡩࡢ࡮࡬ࡾࡪࡁࠠࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰࡥࡩ࡯࡫ࡷ࡭ࡦࡲࡩࡻࡧࠫࡿࢂ࠯࠻ࠡࡨࡵࡳࡲࠦࡰࡥࡤࠣ࡭ࡲࡶ࡯ࡳࡶࠣࡔࡩࡨ࠻ࠡࡱࡪࡣࡩࡨࠠ࠾ࠢࡓࡨࡧ࠴ࡤࡰࡡࡥࡶࡪࡧ࡫࠼ࠌࡧࡩ࡫ࠦ࡭ࡰࡦࡢࡦࡷ࡫ࡡ࡬ࠪࡶࡩࡱ࡬ࠬࠡࡣࡵ࡫࠱ࠦࡴࡦ࡯ࡳࡳࡷࡧࡲࡺࠢࡀࠤ࠵࠯࠺ࠋࠢࠣࡸࡷࡿ࠺ࠋࠢࠣࠤࠥࡧࡲࡨࠢࡀࠤࡸࡺࡲࠩ࡫ࡱࡸ࠭ࡧࡲࡨࠫ࠮࠵࠵࠯ࠊࠡࠢࡨࡼࡨ࡫ࡰࡵࠢࡈࡼࡨ࡫ࡰࡵ࡫ࡲࡲࠥࡧࡳࠡࡧ࠽ࠎࠥࠦࠠࠡࡲࡤࡷࡸࠐࠠࠡࡱࡪࡣࡩࡨࠨࡴࡧ࡯ࡪ࠱ࡧࡲࡨ࠮ࡷࡩࡲࡶ࡯ࡳࡣࡵࡽ࠮ࠐࡐࡥࡤ࠱ࡨࡴࡥࡢࠡ࠿ࠣࡱࡴࡪ࡟ࡣࡴࡨࡥࡰࠐࡐࡥࡤ࠱ࡨࡴࡥࡢࡳࡧࡤ࡯ࠥࡃࠠ࡮ࡱࡧࡣࡧࡸࡥࡢ࡭ࠍࡔࡩࡨࠨࠪ࠰ࡶࡩࡹࡥࡴࡳࡣࡦࡩ࠭࠯࡜࡯ࠤࠥࠦత").format(str(bstack1111111l_opy_))
          bstack11lll1l11_opy_ = bstack1ll1ll11l_opy_ + bstack1ll11l1ll_opy_
          bstack1ll1l1111_opy_ = bstack1111111l_opy_[bstack11l1l1l_opy_ (u"ࠨࡨ࡬ࡰࡪࡥ࡮ࡢ࡯ࡨࠫథ")] + bstack11l1l1l_opy_ (u"ࠩࡢࡦࡸࡺࡡࡤ࡭ࡢࡸࡪࡳࡰ࠯ࡲࡼࠫద")
          with open(bstack1ll1l1111_opy_, bstack11l1l1l_opy_ (u"ࠪࡻࠬధ")):
            pass
          with open(bstack1ll1l1111_opy_, bstack11l1l1l_opy_ (u"ࠦࡼ࠱ࠢన")) as f:
            f.write(bstack11lll1l11_opy_)
          import subprocess
          bstack1l1ll1l1_opy_ = subprocess.run([bstack11l1l1l_opy_ (u"ࠧࡶࡹࡵࡪࡲࡲࠧ఩"), bstack1ll1l1111_opy_])
          if os.path.exists(bstack1ll1l1111_opy_):
            os.unlink(bstack1ll1l1111_opy_)
          os._exit(bstack1l1ll1l1_opy_.returncode)
        else:
          if bstack11l1ll1ll_opy_(bstack1111111l_opy_[bstack11l1l1l_opy_ (u"࠭ࡦࡪ࡮ࡨࡣࡳࡧ࡭ࡦࠩప")]):
            bstack1111111l_opy_[bstack11l1l1l_opy_ (u"ࠧࡧ࡫࡯ࡩࡤࡴࡡ࡮ࡧࠪఫ")].remove(bstack11l1l1l_opy_ (u"ࠨ࠯ࡰࠫబ"))
            bstack1111111l_opy_[bstack11l1l1l_opy_ (u"ࠩࡩ࡭ࡱ࡫࡟࡯ࡣࡰࡩࠬభ")].remove(bstack11l1l1l_opy_ (u"ࠪࡴࡩࡨࠧమ"))
            bstack1111111l_opy_[bstack11l1l1l_opy_ (u"ࠫ࡫࡯࡬ࡦࡡࡱࡥࡲ࡫ࠧయ")] = bstack1111111l_opy_[bstack11l1l1l_opy_ (u"ࠬ࡬ࡩ࡭ࡧࡢࡲࡦࡳࡥࠨర")][0]
          bstack1l1l1l111_opy_(bstack1111ll1l_opy_)
          sys.path.append(os.path.dirname(os.path.abspath(bstack1111111l_opy_[bstack11l1l1l_opy_ (u"࠭ࡦࡪ࡮ࡨࡣࡳࡧ࡭ࡦࠩఱ")])))
          sys.argv = sys.argv[2:]
          mod_globals = globals()
          mod_globals[bstack11l1l1l_opy_ (u"ࠧࡠࡡࡱࡥࡲ࡫࡟ࡠࠩల")] = bstack11l1l1l_opy_ (u"ࠨࡡࡢࡱࡦ࡯࡮ࡠࡡࠪళ")
          mod_globals[bstack11l1l1l_opy_ (u"ࠩࡢࡣ࡫࡯࡬ࡦࡡࡢࠫఴ")] = os.path.abspath(bstack1111111l_opy_[bstack11l1l1l_opy_ (u"ࠪࡪ࡮ࡲࡥࡠࡰࡤࡱࡪ࠭వ")])
          exec(open(bstack1111111l_opy_[bstack11l1l1l_opy_ (u"ࠫ࡫࡯࡬ࡦࡡࡱࡥࡲ࡫ࠧశ")]).read(), mod_globals)
      except BaseException as e:
        try:
          traceback.print_exc()
          logger.error(bstack11l1l1l_opy_ (u"ࠬࡉࡡࡶࡩ࡫ࡸࠥࡋࡸࡤࡧࡳࡸ࡮ࡵ࡮࠻ࠢࡾࢁࠬష").format(str(e)))
          for driver in bstack11111lll1_opy_:
            bstack1ll111ll_opy_.append({
              bstack11l1l1l_opy_ (u"࠭࡮ࡢ࡯ࡨࠫస"): bstack1111111l_opy_[bstack11l1l1l_opy_ (u"ࠧࡧ࡫࡯ࡩࡤࡴࡡ࡮ࡧࠪహ")],
              bstack11l1l1l_opy_ (u"ࠨࡧࡵࡶࡴࡸࠧ఺"): str(e),
              bstack11l1l1l_opy_ (u"ࠩ࡬ࡲࡩ࡫ࡸࠨ఻"): multiprocessing.current_process().name
            })
            driver.execute_script(
              bstack11l1l1l_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࡡࡨࡼࡪࡩࡵࡵࡱࡵ࠾ࠥࢁࠢࡢࡥࡷ࡭ࡴࡴࠢ࠻ࠢࠥࡷࡪࡺࡓࡦࡵࡶ࡭ࡴࡴࡓࡵࡣࡷࡹࡸࠨࠬࠡࠤࡤࡶ࡬ࡻ࡭ࡦࡰࡷࡷࠧࡀࠠࡼࠤࡶࡸࡦࡺࡵࡴࠤ࠽ࠦ࡫ࡧࡩ࡭ࡧࡧࠦ࠱ࠦࠢࡳࡧࡤࡷࡴࡴࠢ࠻఼ࠢࠪ") + json.dumps(
                bstack11l1l1l_opy_ (u"ࠦࡘ࡫ࡳࡴ࡫ࡲࡲࠥ࡬ࡡࡪ࡮ࡨࡨࠥࡽࡩࡵࡪ࠽ࠤࡡࡴࠢఽ") + str(e)) + bstack11l1l1l_opy_ (u"ࠬࢃࡽࠨా"))
        except Exception:
          pass
      finally:
        try:
          for driver in bstack11111lll1_opy_:
            driver.quit()
        except Exception as e:
          pass
    else:
      percy.init(bstack1lll1l111_opy_, CONFIG, logger)
      bstack1l111l111_opy_()
      bstack1ll1l1ll1l_opy_()
      bstack1111llll1_opy_ = {
        bstack11l1l1l_opy_ (u"࠭ࡦࡪ࡮ࡨࡣࡳࡧ࡭ࡦࠩి"): args[0],
        bstack11l1l1l_opy_ (u"ࠧࡄࡑࡑࡊࡎࡍࠧీ"): CONFIG,
        bstack11l1l1l_opy_ (u"ࠨࡊࡘࡆࡤ࡛ࡒࡍࠩు"): bstack1l1ll1ll1l_opy_,
        bstack11l1l1l_opy_ (u"ࠩࡌࡗࡤࡇࡐࡑࡡࡄ࡙࡙ࡕࡍࡂࡖࡈࠫూ"): bstack1lll1l111_opy_
      }
      percy.bstack1l11l111_opy_()
      if bstack11l1l1l_opy_ (u"ࠪࡴࡱࡧࡴࡧࡱࡵࡱࡸ࠭ృ") in CONFIG:
        bstack11lll1ll_opy_ = []
        manager = multiprocessing.Manager()
        bstack11lllll11_opy_ = manager.list()
        if bstack11l1ll1ll_opy_(args):
          for index, platform in enumerate(CONFIG[bstack11l1l1l_opy_ (u"ࠫࡵࡲࡡࡵࡨࡲࡶࡲࡹࠧౄ")]):
            if index == 0:
              bstack1111llll1_opy_[bstack11l1l1l_opy_ (u"ࠬ࡬ࡩ࡭ࡧࡢࡲࡦࡳࡥࠨ౅")] = args
            bstack11lll1ll_opy_.append(multiprocessing.Process(name=str(index),
                                                       target=run_on_browserstack,
                                                       args=(bstack1111llll1_opy_, bstack11lllll11_opy_)))
        else:
          for index, platform in enumerate(CONFIG[bstack11l1l1l_opy_ (u"࠭ࡰ࡭ࡣࡷࡪࡴࡸ࡭ࡴࠩె")]):
            bstack11lll1ll_opy_.append(multiprocessing.Process(name=str(index),
                                                       target=run_on_browserstack,
                                                       args=(bstack1111llll1_opy_, bstack11lllll11_opy_)))
        for t in bstack11lll1ll_opy_:
          t.start()
        for t in bstack11lll1ll_opy_:
          t.join()
        bstack11ll1l1l1_opy_ = list(bstack11lllll11_opy_)
      else:
        if bstack11l1ll1ll_opy_(args):
          bstack1111llll1_opy_[bstack11l1l1l_opy_ (u"ࠧࡧ࡫࡯ࡩࡤࡴࡡ࡮ࡧࠪే")] = args
          test = multiprocessing.Process(name=str(0),
                                         target=run_on_browserstack, args=(bstack1111llll1_opy_,))
          test.start()
          test.join()
        else:
          bstack1l1l1l111_opy_(bstack1111ll1l_opy_)
          sys.path.append(os.path.dirname(os.path.abspath(args[0])))
          mod_globals = globals()
          mod_globals[bstack11l1l1l_opy_ (u"ࠨࡡࡢࡲࡦࡳࡥࡠࡡࠪై")] = bstack11l1l1l_opy_ (u"ࠩࡢࡣࡲࡧࡩ࡯ࡡࡢࠫ౉")
          mod_globals[bstack11l1l1l_opy_ (u"ࠪࡣࡤ࡬ࡩ࡭ࡧࡢࡣࠬొ")] = os.path.abspath(args[0])
          sys.argv = sys.argv[2:]
          exec(open(args[0]).read(), mod_globals)
  elif bstack1lll1l1l_opy_ == bstack11l1l1l_opy_ (u"ࠫࡵࡧࡢࡰࡶࠪో") or bstack1lll1l1l_opy_ == bstack11l1l1l_opy_ (u"ࠬࡸ࡯ࡣࡱࡷࠫౌ"):
    try:
      from pabot import pabot
    except Exception as e:
      bstack1111l111l_opy_(e, bstack1ll1l11l1l_opy_)
    bstack1l111l111_opy_()
    bstack1l1l1l111_opy_(bstack1llll1ll11_opy_)
    if bstack11l1l1l_opy_ (u"࠭࠭࠮ࡲࡵࡳࡨ࡫ࡳࡴࡧࡶ్ࠫ") in args:
      i = args.index(bstack11l1l1l_opy_ (u"ࠧ࠮࠯ࡳࡶࡴࡩࡥࡴࡵࡨࡷࠬ౎"))
      args.pop(i)
      args.pop(i)
    args.insert(0, str(bstack1ll1111l11_opy_))
    args.insert(0, str(bstack11l1l1l_opy_ (u"ࠨ࠯࠰ࡴࡷࡵࡣࡦࡵࡶࡩࡸ࠭౏")))
    if bstack1l11l11l_opy_.on():
      try:
        from robot.run import USAGE
        from robot.utils import ArgumentParser
        from pabot.arguments import _parse_pabot_args
        bstack1lll1l1l1_opy_, pabot_args = _parse_pabot_args(args)
        opts, bstack1lll1llll1_opy_ = ArgumentParser(
            USAGE,
            auto_pythonpath=False,
            auto_argumentfile=True,
            env_options=bstack11l1l1l_opy_ (u"ࠤࡕࡓࡇࡕࡔࡠࡑࡓࡘࡎࡕࡎࡔࠤ౐"),
        ).parse_args(bstack1lll1l1l1_opy_)
        args.insert(args.index(bstack1lll1llll1_opy_[0]), str(bstack11l1l1l_opy_ (u"ࠪ࠱࠲ࡲࡩࡴࡶࡨࡲࡪࡸࠧ౑")))
        args.insert(args.index(bstack1lll1llll1_opy_[0]), str(os.path.join(os.path.dirname(os.path.realpath(__file__)), bstack11l1l1l_opy_ (u"ࠫࡧࡹࡴࡢࡥ࡮ࡣࡷࡵࡢࡰࡶࡢࡰ࡮ࡹࡴࡦࡰࡨࡶ࠳ࡶࡹࠨ౒"))))
        if bstack1111llll_opy_(os.environ.get(bstack11l1l1l_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣࡗࡋࡒࡖࡐࠪ౓"))) and str(os.environ.get(bstack11l1l1l_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤࡘࡅࡓࡗࡑࡣ࡙ࡋࡓࡕࡕࠪ౔"), bstack11l1l1l_opy_ (u"ࠧ࡯ࡷ࡯ࡰౕࠬ"))) != bstack11l1l1l_opy_ (u"ࠨࡰࡸࡰࡱౖ࠭"):
          for bstack1111ll11_opy_ in bstack1lll1llll1_opy_:
            args.remove(bstack1111ll11_opy_)
          bstack1l1l111l1_opy_ = os.environ.get(bstack11l1l1l_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡔࡈࡖ࡚ࡔ࡟ࡕࡇࡖࡘࡘ࠭౗")).split(bstack11l1l1l_opy_ (u"ࠪ࠰ࠬౘ"))
          for bstack111l1l1ll_opy_ in bstack1l1l111l1_opy_:
            args.append(bstack111l1l1ll_opy_)
      except Exception as e:
        logger.error(bstack11l1l1l_opy_ (u"ࠦࡊࡸࡲࡰࡴࠣࡻ࡭࡯࡬ࡦࠢࡤࡸࡹࡧࡣࡩ࡫ࡱ࡫ࠥࡲࡩࡴࡶࡨࡲࡪࡸࠠࡧࡱࡵࠤࡔࡨࡳࡦࡴࡹࡥࡧ࡯࡬ࡪࡶࡼ࠲ࠥࡋࡲࡳࡱࡵࠤ࠲ࠦࠢౙ").format(e))
    pabot.main(args)
  elif bstack1lll1l1l_opy_ == bstack11l1l1l_opy_ (u"ࠬࡸ࡯ࡣࡱࡷ࠱࡮ࡴࡴࡦࡴࡱࡥࡱ࠭ౚ"):
    try:
      from robot import run_cli
    except Exception as e:
      bstack1111l111l_opy_(e, bstack1ll1l11l1l_opy_)
    for a in args:
      if bstack11l1l1l_opy_ (u"࠭ࡂࡔࡖࡄࡇࡐࡖࡌࡂࡖࡉࡓࡗࡓࡉࡏࡆࡈ࡜ࠬ౛") in a:
        bstack1llll111l_opy_ = int(a.split(bstack11l1l1l_opy_ (u"ࠧ࠻ࠩ౜"))[1])
      if bstack11l1l1l_opy_ (u"ࠨࡄࡖࡘࡆࡉࡋࡅࡇࡉࡐࡔࡉࡁࡍࡋࡇࡉࡓ࡚ࡉࡇࡋࡈࡖࠬౝ") in a:
        bstack11l111111_opy_ = str(a.split(bstack11l1l1l_opy_ (u"ࠩ࠽ࠫ౞"))[1])
      if bstack11l1l1l_opy_ (u"ࠪࡆࡘ࡚ࡁࡄࡍࡆࡐࡎࡇࡒࡈࡕࠪ౟") in a:
        bstack1l1llllll1_opy_ = str(a.split(bstack11l1l1l_opy_ (u"ࠫ࠿࠭ౠ"))[1])
    bstack1ll11lll_opy_ = None
    if bstack11l1l1l_opy_ (u"ࠬ࠳࠭ࡣࡵࡷࡥࡨࡱ࡟ࡪࡶࡨࡱࡤ࡯࡮ࡥࡧࡻࠫౡ") in args:
      i = args.index(bstack11l1l1l_opy_ (u"࠭࠭࠮ࡤࡶࡸࡦࡩ࡫ࡠ࡫ࡷࡩࡲࡥࡩ࡯ࡦࡨࡼࠬౢ"))
      args.pop(i)
      bstack1ll11lll_opy_ = args.pop(i)
    if bstack1ll11lll_opy_ is not None:
      global bstack1lll111l_opy_
      bstack1lll111l_opy_ = bstack1ll11lll_opy_
    bstack1l1l1l111_opy_(bstack1llll1ll11_opy_)
    run_cli(args)
    if bstack11l1l1l_opy_ (u"ࠧࡣࡵࡷࡥࡨࡱ࡟ࡦࡴࡵࡳࡷࡥ࡬ࡪࡵࡷࠫౣ") in multiprocessing.current_process().__dict__.keys():
      for bstack1lll1l11l1_opy_ in multiprocessing.current_process().bstack_error_list:
        bstack1ll111ll_opy_.append(bstack1lll1l11l1_opy_)
  elif bstack1lll1l1l_opy_ == bstack11l1l1l_opy_ (u"ࠨࡲࡼࡸࡪࡹࡴࠨ౤"):
    bstack11l1llll1_opy_ = bstack1ll111ll1_opy_(args, logger, CONFIG, bstack11l1l1ll1_opy_)
    bstack11l1llll1_opy_.bstack1lll1l1111_opy_()
    bstack1l111l111_opy_()
    bstack1l1lll1l11_opy_ = True
    bstack1l1l11lll_opy_ = bstack11l1llll1_opy_.bstack1l1lll11ll_opy_()
    bstack11l1llll1_opy_.bstack1111llll1_opy_(bstack111ll11l_opy_)
    bstack1llll1l11l_opy_ = bstack11l1llll1_opy_.bstack11llll111_opy_(bstack1lll1ll1l1_opy_, {
      bstack11l1l1l_opy_ (u"ࠩࡋ࡙ࡇࡥࡕࡓࡎࠪ౥"): bstack1l1ll1ll1l_opy_,
      bstack11l1l1l_opy_ (u"ࠪࡍࡘࡥࡁࡑࡒࡢࡅ࡚࡚ࡏࡎࡃࡗࡉࠬ౦"): bstack1lll1l111_opy_,
      bstack11l1l1l_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡅ࡚࡚ࡏࡎࡃࡗࡍࡔࡔࠧ౧"): bstack11l1l1ll1_opy_
    })
    bstack1ll11ll111_opy_ = 1 if len(bstack1llll1l11l_opy_) > 0 else 0
  elif bstack1lll1l1l_opy_ == bstack11l1l1l_opy_ (u"ࠬࡨࡥࡩࡣࡹࡩࠬ౨"):
    try:
      from behave.__main__ import main as bstack111111l1_opy_
      from behave.configuration import Configuration
    except Exception as e:
      bstack1111l111l_opy_(e, bstack1lll11ll11_opy_)
    bstack1l111l111_opy_()
    bstack1l1lll1l11_opy_ = True
    bstack1ll11l1l11_opy_ = 1
    if bstack11l1l1l_opy_ (u"࠭ࡰࡢࡴࡤࡰࡱ࡫࡬ࡴࡒࡨࡶࡕࡲࡡࡵࡨࡲࡶࡲ࠭౩") in CONFIG:
      bstack1ll11l1l11_opy_ = CONFIG[bstack11l1l1l_opy_ (u"ࠧࡱࡣࡵࡥࡱࡲࡥ࡭ࡵࡓࡩࡷࡖ࡬ࡢࡶࡩࡳࡷࡳࠧ౪")]
    bstack11l1lll11_opy_ = int(bstack1ll11l1l11_opy_) * int(len(CONFIG[bstack11l1l1l_opy_ (u"ࠨࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࡶࠫ౫")]))
    config = Configuration(args)
    bstack1l1lll111l_opy_ = config.paths
    if len(bstack1l1lll111l_opy_) == 0:
      import glob
      pattern = bstack11l1l1l_opy_ (u"ࠩ࠭࠮࠴࠰࠮ࡧࡧࡤࡸࡺࡸࡥࠨ౬")
      bstack1ll11lll1_opy_ = glob.glob(pattern, recursive=True)
      args.extend(bstack1ll11lll1_opy_)
      config = Configuration(args)
      bstack1l1lll111l_opy_ = config.paths
    bstack1ll1111l1_opy_ = [os.path.normpath(item) for item in bstack1l1lll111l_opy_]
    bstack1ll1l1l11_opy_ = [os.path.normpath(item) for item in args]
    bstack1111ll1ll_opy_ = [item for item in bstack1ll1l1l11_opy_ if item not in bstack1ll1111l1_opy_]
    import platform as pf
    if pf.system().lower() == bstack11l1l1l_opy_ (u"ࠪࡻ࡮ࡴࡤࡰࡹࡶࠫ౭"):
      from pathlib import PureWindowsPath, PurePosixPath
      bstack1ll1111l1_opy_ = [str(PurePosixPath(PureWindowsPath(bstack1lll111ll1_opy_)))
                    for bstack1lll111ll1_opy_ in bstack1ll1111l1_opy_]
    bstack111111ll_opy_ = []
    for spec in bstack1ll1111l1_opy_:
      bstack11111ll1l_opy_ = []
      bstack11111ll1l_opy_ += bstack1111ll1ll_opy_
      bstack11111ll1l_opy_.append(spec)
      bstack111111ll_opy_.append(bstack11111ll1l_opy_)
    execution_items = []
    for bstack11111ll1l_opy_ in bstack111111ll_opy_:
      for index, _ in enumerate(CONFIG[bstack11l1l1l_opy_ (u"ࠫࡵࡲࡡࡵࡨࡲࡶࡲࡹࠧ౮")]):
        item = {}
        item[bstack11l1l1l_opy_ (u"ࠬࡧࡲࡨࠩ౯")] = bstack11l1l1l_opy_ (u"࠭ࠠࠨ౰").join(bstack11111ll1l_opy_)
        item[bstack11l1l1l_opy_ (u"ࠧࡪࡰࡧࡩࡽ࠭౱")] = index
        execution_items.append(item)
    bstack1ll11l11l1_opy_ = bstack1lll111111_opy_(execution_items, bstack11l1lll11_opy_)
    for execution_item in bstack1ll11l11l1_opy_:
      bstack11lll1ll_opy_ = []
      for item in execution_item:
        bstack11lll1ll_opy_.append(bstack1ll11l1l1l_opy_(name=str(item[bstack11l1l1l_opy_ (u"ࠨ࡫ࡱࡨࡪࡾࠧ౲")]),
                                             target=bstack111ll111_opy_,
                                             args=(item[bstack11l1l1l_opy_ (u"ࠩࡤࡶ࡬࠭౳")],)))
      for t in bstack11lll1ll_opy_:
        t.start()
      for t in bstack11lll1ll_opy_:
        t.join()
  else:
    bstack111l1l111_opy_(bstack111l1lll1_opy_)
  if not bstack1111111l_opy_:
    bstack11111l11l_opy_()
def browserstack_initialize(bstack1l11l1ll_opy_=None):
  run_on_browserstack(bstack1l11l1ll_opy_, None, True)
def bstack11111l11l_opy_():
  global CONFIG
  global bstack11l1l111_opy_
  global bstack1ll11ll111_opy_
  bstack1l11l11l_opy_.stop()
  bstack1l11l11l_opy_.bstack1lll1llll_opy_()
  if bstack1111ll111_opy_.bstack1ll1ll11_opy_(CONFIG):
    bstack1111ll111_opy_.bstack1lll11l1l_opy_()
  [bstack1l11lllll_opy_, bstack11l1l111l_opy_] = bstack11ll1111l_opy_()
  if bstack1l11lllll_opy_ is not None and bstack111l1l1l1_opy_() != -1:
    sessions = bstack1lll1l11_opy_(bstack1l11lllll_opy_)
    bstack1lll1lll_opy_(sessions, bstack11l1l111l_opy_)
  if bstack11l1l111_opy_ == bstack11l1l1l_opy_ (u"ࠪࡴࡾࡺࡥࡴࡶࠪ౴") and bstack1ll11ll111_opy_ != 0:
    sys.exit(bstack1ll11ll111_opy_)
def bstack1llll1l1l1_opy_(bstack11l1111ll_opy_):
  if bstack11l1111ll_opy_:
    return bstack11l1111ll_opy_.capitalize()
  else:
    return bstack11l1l1l_opy_ (u"ࠫࠬ౵")
def bstack1l1llll1l_opy_(bstack1ll1l111l1_opy_):
  if bstack11l1l1l_opy_ (u"ࠬࡴࡡ࡮ࡧࠪ౶") in bstack1ll1l111l1_opy_ and bstack1ll1l111l1_opy_[bstack11l1l1l_opy_ (u"࠭࡮ࡢ࡯ࡨࠫ౷")] != bstack11l1l1l_opy_ (u"ࠧࠨ౸"):
    return bstack1ll1l111l1_opy_[bstack11l1l1l_opy_ (u"ࠨࡰࡤࡱࡪ࠭౹")]
  else:
    bstack11ll11lll_opy_ = bstack11l1l1l_opy_ (u"ࠤࠥ౺")
    if bstack11l1l1l_opy_ (u"ࠪࡨࡪࡼࡩࡤࡧࠪ౻") in bstack1ll1l111l1_opy_ and bstack1ll1l111l1_opy_[bstack11l1l1l_opy_ (u"ࠫࡩ࡫ࡶࡪࡥࡨࠫ౼")] != None:
      bstack11ll11lll_opy_ += bstack1ll1l111l1_opy_[bstack11l1l1l_opy_ (u"ࠬࡪࡥࡷ࡫ࡦࡩࠬ౽")] + bstack11l1l1l_opy_ (u"ࠨࠬࠡࠤ౾")
      if bstack1ll1l111l1_opy_[bstack11l1l1l_opy_ (u"ࠧࡰࡵࠪ౿")] == bstack11l1l1l_opy_ (u"ࠣ࡫ࡲࡷࠧಀ"):
        bstack11ll11lll_opy_ += bstack11l1l1l_opy_ (u"ࠤ࡬ࡓࡘࠦࠢಁ")
      bstack11ll11lll_opy_ += (bstack1ll1l111l1_opy_[bstack11l1l1l_opy_ (u"ࠪࡳࡸࡥࡶࡦࡴࡶ࡭ࡴࡴࠧಂ")] or bstack11l1l1l_opy_ (u"ࠫࠬಃ"))
      return bstack11ll11lll_opy_
    else:
      bstack11ll11lll_opy_ += bstack1llll1l1l1_opy_(bstack1ll1l111l1_opy_[bstack11l1l1l_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷ࠭಄")]) + bstack11l1l1l_opy_ (u"ࠨࠠࠣಅ") + (
              bstack1ll1l111l1_opy_[bstack11l1l1l_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡠࡸࡨࡶࡸ࡯࡯࡯ࠩಆ")] or bstack11l1l1l_opy_ (u"ࠨࠩಇ")) + bstack11l1l1l_opy_ (u"ࠤ࠯ࠤࠧಈ")
      if bstack1ll1l111l1_opy_[bstack11l1l1l_opy_ (u"ࠪࡳࡸ࠭ಉ")] == bstack11l1l1l_opy_ (u"ࠦ࡜࡯࡮ࡥࡱࡺࡷࠧಊ"):
        bstack11ll11lll_opy_ += bstack11l1l1l_opy_ (u"ࠧ࡝ࡩ࡯ࠢࠥಋ")
      bstack11ll11lll_opy_ += bstack1ll1l111l1_opy_[bstack11l1l1l_opy_ (u"࠭࡯ࡴࡡࡹࡩࡷࡹࡩࡰࡰࠪಌ")] or bstack11l1l1l_opy_ (u"ࠧࠨ಍")
      return bstack11ll11lll_opy_
def bstack11lll11l1_opy_(bstack1l1ll11ll_opy_):
  if bstack1l1ll11ll_opy_ == bstack11l1l1l_opy_ (u"ࠣࡦࡲࡲࡪࠨಎ"):
    return bstack11l1l1l_opy_ (u"ࠩ࠿ࡸࡩࠦࡣ࡭ࡣࡶࡷࡂࠨࡢࡴࡶࡤࡧࡰ࠳ࡤࡢࡶࡤࠦࠥࡹࡴࡺ࡮ࡨࡁࠧࡩ࡯࡭ࡱࡵ࠾࡬ࡸࡥࡦࡰ࠾ࠦࡃࡂࡦࡰࡰࡷࠤࡨࡵ࡬ࡰࡴࡀࠦ࡬ࡸࡥࡦࡰࠥࡂࡈࡵ࡭ࡱ࡮ࡨࡸࡪࡪ࠼࠰ࡨࡲࡲࡹࡄ࠼࠰ࡶࡧࡂࠬಏ")
  elif bstack1l1ll11ll_opy_ == bstack11l1l1l_opy_ (u"ࠥࡪࡦ࡯࡬ࡦࡦࠥಐ"):
    return bstack11l1l1l_opy_ (u"ࠫࡁࡺࡤࠡࡥ࡯ࡥࡸࡹ࠽ࠣࡤࡶࡸࡦࡩ࡫࠮ࡦࡤࡸࡦࠨࠠࡴࡶࡼࡰࡪࡃࠢࡤࡱ࡯ࡳࡷࡀࡲࡦࡦ࠾ࠦࡃࡂࡦࡰࡰࡷࠤࡨࡵ࡬ࡰࡴࡀࠦࡷ࡫ࡤࠣࡀࡉࡥ࡮ࡲࡥࡥ࠾࠲ࡪࡴࡴࡴ࠿࠾࠲ࡸࡩࡄࠧ಑")
  elif bstack1l1ll11ll_opy_ == bstack11l1l1l_opy_ (u"ࠧࡶࡡࡴࡵࡨࡨࠧಒ"):
    return bstack11l1l1l_opy_ (u"࠭࠼ࡵࡦࠣࡧࡱࡧࡳࡴ࠿ࠥࡦࡸࡺࡡࡤ࡭࠰ࡨࡦࡺࡡࠣࠢࡶࡸࡾࡲࡥ࠾ࠤࡦࡳࡱࡵࡲ࠻ࡩࡵࡩࡪࡴ࠻ࠣࡀ࠿ࡪࡴࡴࡴࠡࡥࡲࡰࡴࡸ࠽ࠣࡩࡵࡩࡪࡴࠢ࠿ࡒࡤࡷࡸ࡫ࡤ࠽࠱ࡩࡳࡳࡺ࠾࠽࠱ࡷࡨࡃ࠭ಓ")
  elif bstack1l1ll11ll_opy_ == bstack11l1l1l_opy_ (u"ࠢࡦࡴࡵࡳࡷࠨಔ"):
    return bstack11l1l1l_opy_ (u"ࠨ࠾ࡷࡨࠥࡩ࡬ࡢࡵࡶࡁࠧࡨࡳࡵࡣࡦ࡯࠲ࡪࡡࡵࡣࠥࠤࡸࡺࡹ࡭ࡧࡀࠦࡨࡵ࡬ࡰࡴ࠽ࡶࡪࡪ࠻ࠣࡀ࠿ࡪࡴࡴࡴࠡࡥࡲࡰࡴࡸ࠽ࠣࡴࡨࡨࠧࡄࡅࡳࡴࡲࡶࡁ࠵ࡦࡰࡰࡷࡂࡁ࠵ࡴࡥࡀࠪಕ")
  elif bstack1l1ll11ll_opy_ == bstack11l1l1l_opy_ (u"ࠤࡷ࡭ࡲ࡫࡯ࡶࡶࠥಖ"):
    return bstack11l1l1l_opy_ (u"ࠪࡀࡹࡪࠠࡤ࡮ࡤࡷࡸࡃࠢࡣࡵࡷࡥࡨࡱ࠭ࡥࡣࡷࡥࠧࠦࡳࡵࡻ࡯ࡩࡂࠨࡣࡰ࡮ࡲࡶ࠿ࠩࡥࡦࡣ࠶࠶࠻ࡁࠢ࠿࠾ࡩࡳࡳࡺࠠࡤࡱ࡯ࡳࡷࡃࠢࠤࡧࡨࡥ࠸࠸࠶ࠣࡀࡗ࡭ࡲ࡫࡯ࡶࡶ࠿࠳࡫ࡵ࡮ࡵࡀ࠿࠳ࡹࡪ࠾ࠨಗ")
  elif bstack1l1ll11ll_opy_ == bstack11l1l1l_opy_ (u"ࠦࡷࡻ࡮࡯࡫ࡱ࡫ࠧಘ"):
    return bstack11l1l1l_opy_ (u"ࠬࡂࡴࡥࠢࡦࡰࡦࡹࡳ࠾ࠤࡥࡷࡹࡧࡣ࡬࠯ࡧࡥࡹࡧࠢࠡࡵࡷࡽࡱ࡫࠽ࠣࡥࡲࡰࡴࡸ࠺ࡣ࡮ࡤࡧࡰࡁࠢ࠿࠾ࡩࡳࡳࡺࠠࡤࡱ࡯ࡳࡷࡃࠢࡣ࡮ࡤࡧࡰࠨ࠾ࡓࡷࡱࡲ࡮ࡴࡧ࠽࠱ࡩࡳࡳࡺ࠾࠽࠱ࡷࡨࡃ࠭ಙ")
  else:
    return bstack11l1l1l_opy_ (u"࠭࠼ࡵࡦࠣࡥࡱ࡯ࡧ࡯࠿ࠥࡧࡪࡴࡴࡦࡴࠥࠤࡨࡲࡡࡴࡵࡀࠦࡧࡹࡴࡢࡥ࡮࠱ࡩࡧࡴࡢࠤࠣࡷࡹࡿ࡬ࡦ࠿ࠥࡧࡴࡲ࡯ࡳ࠼ࡥࡰࡦࡩ࡫࠼ࠤࡁࡀ࡫ࡵ࡮ࡵࠢࡦࡳࡱࡵࡲ࠾ࠤࡥࡰࡦࡩ࡫ࠣࡀࠪಚ") + bstack1llll1l1l1_opy_(
      bstack1l1ll11ll_opy_) + bstack11l1l1l_opy_ (u"ࠧ࠽࠱ࡩࡳࡳࡺ࠾࠽࠱ࡷࡨࡃ࠭ಛ")
def bstack1l1111l11_opy_(session):
  return bstack11l1l1l_opy_ (u"ࠨ࠾ࡷࡶࠥࡩ࡬ࡢࡵࡶࡁࠧࡨࡳࡵࡣࡦ࡯࠲ࡸ࡯ࡸࠤࡁࡀࡹࡪࠠࡤ࡮ࡤࡷࡸࡃࠢࡣࡵࡷࡥࡨࡱ࠭ࡥࡣࡷࡥࠥࡹࡥࡴࡵ࡬ࡳࡳ࠳࡮ࡢ࡯ࡨࠦࡃࡂࡡࠡࡪࡵࡩ࡫ࡃࠢࡼࡿࠥࠤࡹࡧࡲࡨࡧࡷࡁࠧࡥࡢ࡭ࡣࡱ࡯ࠧࡄࡻࡾ࠾࠲ࡥࡃࡂ࠯ࡵࡦࡁࡿࢂࢁࡽ࠽ࡶࡧࠤࡦࡲࡩࡨࡰࡀࠦࡨ࡫࡮ࡵࡧࡵࠦࠥࡩ࡬ࡢࡵࡶࡁࠧࡨࡳࡵࡣࡦ࡯࠲ࡪࡡࡵࡣࠥࡂࢀࢃ࠼࠰ࡶࡧࡂࡁࡺࡤࠡࡣ࡯࡭࡬ࡴ࠽ࠣࡥࡨࡲࡹ࡫ࡲࠣࠢࡦࡰࡦࡹࡳ࠾ࠤࡥࡷࡹࡧࡣ࡬࠯ࡧࡥࡹࡧࠢ࠿ࡽࢀࡀ࠴ࡺࡤ࠿࠾ࡷࡨࠥࡧ࡬ࡪࡩࡱࡁࠧࡩࡥ࡯ࡶࡨࡶࠧࠦࡣ࡭ࡣࡶࡷࡂࠨࡢࡴࡶࡤࡧࡰ࠳ࡤࡢࡶࡤࠦࡃࢁࡽ࠽࠱ࡷࡨࡃࡂࡴࡥࠢࡤࡰ࡮࡭࡮࠾ࠤࡦࡩࡳࡺࡥࡳࠤࠣࡧࡱࡧࡳࡴ࠿ࠥࡦࡸࡺࡡࡤ࡭࠰ࡨࡦࡺࡡࠣࡀࡾࢁࡁ࠵ࡴࡥࡀ࠿࠳ࡹࡸ࠾ࠨಜ").format(
    session[bstack11l1l1l_opy_ (u"ࠩࡳࡹࡧࡲࡩࡤࡡࡸࡶࡱ࠭ಝ")], bstack1l1llll1l_opy_(session), bstack11lll11l1_opy_(session[bstack11l1l1l_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࡡࡶࡸࡦࡺࡵࡴࠩಞ")]),
    bstack11lll11l1_opy_(session[bstack11l1l1l_opy_ (u"ࠫࡸࡺࡡࡵࡷࡶࠫಟ")]),
    bstack1llll1l1l1_opy_(session[bstack11l1l1l_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷ࠭ಠ")] or session[bstack11l1l1l_opy_ (u"࠭ࡤࡦࡸ࡬ࡧࡪ࠭ಡ")] or bstack11l1l1l_opy_ (u"ࠧࠨಢ")) + bstack11l1l1l_opy_ (u"ࠣࠢࠥಣ") + (session[bstack11l1l1l_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡢࡺࡪࡸࡳࡪࡱࡱࠫತ")] or bstack11l1l1l_opy_ (u"ࠪࠫಥ")),
    session[bstack11l1l1l_opy_ (u"ࠫࡴࡹࠧದ")] + bstack11l1l1l_opy_ (u"ࠧࠦࠢಧ") + session[bstack11l1l1l_opy_ (u"࠭࡯ࡴࡡࡹࡩࡷࡹࡩࡰࡰࠪನ")], session[bstack11l1l1l_opy_ (u"ࠧࡥࡷࡵࡥࡹ࡯࡯࡯ࠩ಩")] or bstack11l1l1l_opy_ (u"ࠨࠩಪ"),
    session[bstack11l1l1l_opy_ (u"ࠩࡦࡶࡪࡧࡴࡦࡦࡢࡥࡹ࠭ಫ")] if session[bstack11l1l1l_opy_ (u"ࠪࡧࡷ࡫ࡡࡵࡧࡧࡣࡦࡺࠧಬ")] else bstack11l1l1l_opy_ (u"ࠫࠬಭ"))
def bstack1lll1lll_opy_(sessions, bstack11l1l111l_opy_):
  try:
    bstack1ll1l11l11_opy_ = bstack11l1l1l_opy_ (u"ࠧࠨಮ")
    if not os.path.exists(bstack11llll1l1_opy_):
      os.mkdir(bstack11llll1l1_opy_)
    with open(os.path.join(os.path.dirname(os.path.realpath(__file__)), bstack11l1l1l_opy_ (u"࠭ࡡࡴࡵࡨࡸࡸ࠵ࡲࡦࡲࡲࡶࡹ࠴ࡨࡵ࡯࡯ࠫಯ")), bstack11l1l1l_opy_ (u"ࠧࡳࠩರ")) as f:
      bstack1ll1l11l11_opy_ = f.read()
    bstack1ll1l11l11_opy_ = bstack1ll1l11l11_opy_.replace(bstack11l1l1l_opy_ (u"ࠨࡽࠨࡖࡊ࡙ࡕࡍࡖࡖࡣࡈࡕࡕࡏࡖࠨࢁࠬಱ"), str(len(sessions)))
    bstack1ll1l11l11_opy_ = bstack1ll1l11l11_opy_.replace(bstack11l1l1l_opy_ (u"ࠩࡾࠩࡇ࡛ࡉࡍࡆࡢ࡙ࡗࡒࠥࡾࠩಲ"), bstack11l1l111l_opy_)
    bstack1ll1l11l11_opy_ = bstack1ll1l11l11_opy_.replace(bstack11l1l1l_opy_ (u"ࠪࡿࠪࡈࡕࡊࡎࡇࡣࡓࡇࡍࡆࠧࢀࠫಳ"),
                                              sessions[0].get(bstack11l1l1l_opy_ (u"ࠫࡧࡻࡩ࡭ࡦࡢࡲࡦࡳࡥࠨ಴")) if sessions[0] else bstack11l1l1l_opy_ (u"ࠬ࠭ವ"))
    with open(os.path.join(bstack11llll1l1_opy_, bstack11l1l1l_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯࠲ࡸࡥࡱࡱࡵࡸ࠳࡮ࡴ࡮࡮ࠪಶ")), bstack11l1l1l_opy_ (u"ࠧࡸࠩಷ")) as stream:
      stream.write(bstack1ll1l11l11_opy_.split(bstack11l1l1l_opy_ (u"ࠨࡽࠨࡗࡊ࡙ࡓࡊࡑࡑࡗࡤࡊࡁࡕࡃࠨࢁࠬಸ"))[0])
      for session in sessions:
        stream.write(bstack1l1111l11_opy_(session))
      stream.write(bstack1ll1l11l11_opy_.split(bstack11l1l1l_opy_ (u"ࠩࡾࠩࡘࡋࡓࡔࡋࡒࡒࡘࡥࡄࡂࡖࡄࠩࢂ࠭ಹ"))[1])
    logger.info(bstack11l1l1l_opy_ (u"ࠪࡋࡪࡴࡥࡳࡣࡷࡩࡩࠦࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࠥࡨࡵࡪ࡮ࡧࠤࡦࡸࡴࡪࡨࡤࡧࡹࡹࠠࡢࡶࠣࡿࢂ࠭಺").format(bstack11llll1l1_opy_));
  except Exception as e:
    logger.debug(bstack1lllll11l_opy_.format(str(e)))
def bstack1lll1l11_opy_(bstack1l11lllll_opy_):
  global CONFIG
  try:
    host = bstack11l1l1l_opy_ (u"ࠫࡦࡶࡩ࠮ࡥ࡯ࡳࡺࡪࠧ಻") if bstack11l1l1l_opy_ (u"ࠬࡧࡰࡱ಼ࠩ") in CONFIG else bstack11l1l1l_opy_ (u"࠭ࡡࡱ࡫ࠪಽ")
    user = CONFIG[bstack11l1l1l_opy_ (u"ࠧࡶࡵࡨࡶࡓࡧ࡭ࡦࠩಾ")]
    key = CONFIG[bstack11l1l1l_opy_ (u"ࠨࡣࡦࡧࡪࡹࡳࡌࡧࡼࠫಿ")]
    bstack111l11l1l_opy_ = bstack11l1l1l_opy_ (u"ࠩࡤࡴࡵ࠳ࡡࡶࡶࡲࡱࡦࡺࡥࠨೀ") if bstack11l1l1l_opy_ (u"ࠪࡥࡵࡶࠧು") in CONFIG else bstack11l1l1l_opy_ (u"ࠫࡦࡻࡴࡰ࡯ࡤࡸࡪ࠭ೂ")
    url = bstack11l1l1l_opy_ (u"ࠬ࡮ࡴࡵࡲࡶ࠾࠴࠵ࡻࡾ࠼ࡾࢁࡅࢁࡽ࠯ࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠮ࡤࡱࡰ࠳ࢀࢃ࠯ࡣࡷ࡬ࡰࡩࡹ࠯ࡼࡿ࠲ࡷࡪࡹࡳࡪࡱࡱࡷ࠳ࡰࡳࡰࡰࠪೃ").format(user, key, host, bstack111l11l1l_opy_,
                                                                                bstack1l11lllll_opy_)
    headers = {
      bstack11l1l1l_opy_ (u"࠭ࡃࡰࡰࡷࡩࡳࡺ࠭ࡵࡻࡳࡩࠬೄ"): bstack11l1l1l_opy_ (u"ࠧࡢࡲࡳࡰ࡮ࡩࡡࡵ࡫ࡲࡲ࠴ࡰࡳࡰࡰࠪ೅"),
    }
    proxies = bstack1ll1l1l1l_opy_(CONFIG, url)
    response = requests.get(url, headers=headers, proxies=proxies)
    if response.json():
      return list(map(lambda session: session[bstack11l1l1l_opy_ (u"ࠨࡣࡸࡸࡴࡳࡡࡵ࡫ࡲࡲࡤࡹࡥࡴࡵ࡬ࡳࡳ࠭ೆ")], response.json()))
  except Exception as e:
    logger.debug(bstack11l11l111_opy_.format(str(e)))
def bstack11ll1111l_opy_():
  global CONFIG
  global bstack1lllllll1l_opy_
  try:
    if bstack11l1l1l_opy_ (u"ࠩࡥࡹ࡮ࡲࡤࡏࡣࡰࡩࠬೇ") in CONFIG:
      host = bstack11l1l1l_opy_ (u"ࠪࡥࡵ࡯࠭ࡤ࡮ࡲࡹࡩ࠭ೈ") if bstack11l1l1l_opy_ (u"ࠫࡦࡶࡰࠨ೉") in CONFIG else bstack11l1l1l_opy_ (u"ࠬࡧࡰࡪࠩೊ")
      user = CONFIG[bstack11l1l1l_opy_ (u"࠭ࡵࡴࡧࡵࡒࡦࡳࡥࠨೋ")]
      key = CONFIG[bstack11l1l1l_opy_ (u"ࠧࡢࡥࡦࡩࡸࡹࡋࡦࡻࠪೌ")]
      bstack111l11l1l_opy_ = bstack11l1l1l_opy_ (u"ࠨࡣࡳࡴ࠲ࡧࡵࡵࡱࡰࡥࡹ࡫್ࠧ") if bstack11l1l1l_opy_ (u"ࠩࡤࡴࡵ࠭೎") in CONFIG else bstack11l1l1l_opy_ (u"ࠪࡥࡺࡺ࡯࡮ࡣࡷࡩࠬ೏")
      url = bstack11l1l1l_opy_ (u"ࠫ࡭ࡺࡴࡱࡵ࠽࠳࠴ࢁࡽ࠻ࡽࢀࡄࢀࢃ࠮ࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠴ࡣࡰ࡯࠲ࡿࢂ࠵ࡢࡶ࡫࡯ࡨࡸ࠴ࡪࡴࡱࡱࠫ೐").format(user, key, host, bstack111l11l1l_opy_)
      headers = {
        bstack11l1l1l_opy_ (u"ࠬࡉ࡯࡯ࡶࡨࡲࡹ࠳ࡴࡺࡲࡨࠫ೑"): bstack11l1l1l_opy_ (u"࠭ࡡࡱࡲ࡯࡭ࡨࡧࡴࡪࡱࡱ࠳࡯ࡹ࡯࡯ࠩ೒"),
      }
      if bstack11l1l1l_opy_ (u"ࠧࡣࡷ࡬ࡰࡩࡏࡤࡦࡰࡷ࡭࡫࡯ࡥࡳࠩ೓") in CONFIG:
        params = {bstack11l1l1l_opy_ (u"ࠨࡰࡤࡱࡪ࠭೔"): CONFIG[bstack11l1l1l_opy_ (u"ࠩࡥࡹ࡮ࡲࡤࡏࡣࡰࡩࠬೕ")], bstack11l1l1l_opy_ (u"ࠪࡦࡺ࡯࡬ࡥࡡ࡬ࡨࡪࡴࡴࡪࡨ࡬ࡩࡷ࠭ೖ"): CONFIG[bstack11l1l1l_opy_ (u"ࠫࡧࡻࡩ࡭ࡦࡌࡨࡪࡴࡴࡪࡨ࡬ࡩࡷ࠭೗")]}
      else:
        params = {bstack11l1l1l_opy_ (u"ࠬࡴࡡ࡮ࡧࠪ೘"): CONFIG[bstack11l1l1l_opy_ (u"࠭ࡢࡶ࡫࡯ࡨࡓࡧ࡭ࡦࠩ೙")]}
      proxies = bstack1ll1l1l1l_opy_(CONFIG, url)
      response = requests.get(url, params=params, headers=headers, proxies=proxies)
      if response.json():
        bstack1lll1ll11l_opy_ = response.json()[0][bstack11l1l1l_opy_ (u"ࠧࡢࡷࡷࡳࡲࡧࡴࡪࡱࡱࡣࡧࡻࡩ࡭ࡦࠪ೚")]
        if bstack1lll1ll11l_opy_:
          bstack11l1l111l_opy_ = bstack1lll1ll11l_opy_[bstack11l1l1l_opy_ (u"ࠨࡲࡸࡦࡱ࡯ࡣࡠࡷࡵࡰࠬ೛")].split(bstack11l1l1l_opy_ (u"ࠩࡳࡹࡧࡲࡩࡤ࠯ࡥࡹ࡮ࡲࡤࠨ೜"))[0] + bstack11l1l1l_opy_ (u"ࠪࡦࡺ࡯࡬ࡥࡵ࠲ࠫೝ") + bstack1lll1ll11l_opy_[
            bstack11l1l1l_opy_ (u"ࠫ࡭ࡧࡳࡩࡧࡧࡣ࡮ࡪࠧೞ")]
          logger.info(bstack1111lll1_opy_.format(bstack11l1l111l_opy_))
          bstack1lllllll1l_opy_ = bstack1lll1ll11l_opy_[bstack11l1l1l_opy_ (u"ࠬ࡮ࡡࡴࡪࡨࡨࡤ࡯ࡤࠨ೟")]
          bstack111l11l11_opy_ = CONFIG[bstack11l1l1l_opy_ (u"࠭ࡢࡶ࡫࡯ࡨࡓࡧ࡭ࡦࠩೠ")]
          if bstack11l1l1l_opy_ (u"ࠧࡣࡷ࡬ࡰࡩࡏࡤࡦࡰࡷ࡭࡫࡯ࡥࡳࠩೡ") in CONFIG:
            bstack111l11l11_opy_ += bstack11l1l1l_opy_ (u"ࠨࠢࠪೢ") + CONFIG[bstack11l1l1l_opy_ (u"ࠩࡥࡹ࡮ࡲࡤࡊࡦࡨࡲࡹ࡯ࡦࡪࡧࡵࠫೣ")]
          if bstack111l11l11_opy_ != bstack1lll1ll11l_opy_[bstack11l1l1l_opy_ (u"ࠪࡲࡦࡳࡥࠨ೤")]:
            logger.debug(bstack1lllll1lll_opy_.format(bstack1lll1ll11l_opy_[bstack11l1l1l_opy_ (u"ࠫࡳࡧ࡭ࡦࠩ೥")], bstack111l11l11_opy_))
          return [bstack1lll1ll11l_opy_[bstack11l1l1l_opy_ (u"ࠬ࡮ࡡࡴࡪࡨࡨࡤ࡯ࡤࠨ೦")], bstack11l1l111l_opy_]
    else:
      logger.warn(bstack1ll11111l1_opy_)
  except Exception as e:
    logger.debug(bstack1l1llll1l1_opy_.format(str(e)))
  return [None, None]
def bstack1l1lll1lll_opy_(url, bstack1ll1ll1lll_opy_=False):
  global CONFIG
  global bstack1lll111l11_opy_
  if not bstack1lll111l11_opy_:
    hostname = bstack1ll1l111ll_opy_(url)
    is_private = bstack111l1l11_opy_(hostname)
    if (bstack11l1l1l_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࡑࡵࡣࡢ࡮ࠪ೧") in CONFIG and not bstack1111llll_opy_(CONFIG[bstack11l1l1l_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰࡒ࡯ࡤࡣ࡯ࠫ೨")])) and (is_private or bstack1ll1ll1lll_opy_):
      bstack1lll111l11_opy_ = hostname
def bstack1ll1l111ll_opy_(url):
  return urlparse(url).hostname
def bstack111l1l11_opy_(hostname):
  for bstack111ll1111_opy_ in bstack11111l1l_opy_:
    regex = re.compile(bstack111ll1111_opy_)
    if regex.match(hostname):
      return True
  return False
def bstack11lll111_opy_(key_name):
  return True if key_name in threading.current_thread().__dict__.keys() else False
def getAccessibilityResults(driver):
  global CONFIG
  global bstack1llll111l_opy_
  if not bstack1111ll111_opy_.bstack1lll11l11_opy_(CONFIG, bstack1llll111l_opy_):
    logger.warning(bstack11l1l1l_opy_ (u"ࠣࡐࡲࡸࠥࡧ࡮ࠡࡃࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࠡࡃࡸࡸࡴࡳࡡࡵ࡫ࡲࡲࠥࡹࡥࡴࡵ࡬ࡳࡳ࠲ࠠࡤࡣࡱࡲࡴࡺࠠࡳࡧࡷࡶ࡮࡫ࡶࡦࠢࡄࡧࡨ࡫ࡳࡴ࡫ࡥ࡭ࡱ࡯ࡴࡺࠢࡵࡩࡸࡻ࡬ࡵࡵ࠱ࠦ೩"))
    return {}
  try:
    results = driver.execute_script(bstack11l1l1l_opy_ (u"ࠤࠥࠦࠏࠦࠠࠡࠢࠣࠤࠥࠦࡲࡦࡶࡸࡶࡳࠦ࡮ࡦࡹࠣࡔࡷࡵ࡭ࡪࡵࡨࠬ࡫ࡻ࡮ࡤࡶ࡬ࡳࡳࠦࠨࡳࡧࡶࡳࡱࡼࡥ࠭ࠢࡵࡩ࡯࡫ࡣࡵࠫࠣࡿࠏࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࡸࡷࡿࠠࡼࠌࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࡨࡵ࡮ࡴࡶࠣࡩࡻ࡫࡮ࡵࠢࡀࠤࡳ࡫ࡷࠡࡅࡸࡷࡹࡵ࡭ࡆࡸࡨࡲࡹ࠮ࠧࡂ࠳࠴࡝ࡤ࡚ࡁࡑࡡࡊࡉ࡙ࡥࡒࡆࡕࡘࡐ࡙࡙ࠧࠪ࠽ࠍࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࡩ࡯࡯ࡵࡷࠤ࡫ࡴࠠ࠾ࠢࡩࡹࡳࡩࡴࡪࡱࡱࠤ࠭࡫ࡶࡦࡰࡷ࠭ࠥࢁࠊࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࡷࡪࡰࡧࡳࡼ࠴ࡲࡦ࡯ࡲࡺࡪࡋࡶࡦࡰࡷࡐ࡮ࡹࡴࡦࡰࡨࡶ࠭࠭ࡁ࠲࠳࡜ࡣࡗࡋࡓࡖࡎࡗࡗࡤࡘࡅࡔࡒࡒࡒࡘࡋࠧ࠭ࠢࡩࡲ࠮ࡁࠊࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࡲࡦࡵࡲࡰࡻ࡫ࠨࡦࡸࡨࡲࡹ࠴ࡤࡦࡶࡤ࡭ࡱ࠴ࡤࡢࡶࡤ࠭ࡀࠐࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࡿ࠾ࠎࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࡷࡪࡰࡧࡳࡼ࠴ࡡࡥࡦࡈࡺࡪࡴࡴࡍ࡫ࡶࡸࡪࡴࡥࡳࠪࠪࡅ࠶࠷࡙ࡠࡔࡈࡗ࡚ࡒࡔࡔࡡࡕࡉࡘࡖࡏࡏࡕࡈࠫ࠱ࠦࡦ࡯ࠫ࠾ࠎࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࡷࡪࡰࡧࡳࡼ࠴ࡤࡪࡵࡳࡥࡹࡩࡨࡆࡸࡨࡲࡹ࠮ࡥࡷࡧࡱࡸ࠮ࡁࠊࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࢃࠠࡤࡣࡷࡧ࡭ࠦࡻࠋࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࡶࡪࡰࡥࡤࡶࠫ࠭ࡀࠐࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࢂࠐࠠࠡࠢࠣࠤࠥࠦࠠࡾࠫ࠾ࠎࠥࠦࠠࠡࠤࠥࠦ೪"))
    return results
  except Exception:
    logger.error(bstack11l1l1l_opy_ (u"ࠥࡒࡴࠦࡡࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾࠦࡲࡦࡵࡸࡰࡹࡹࠠࡸࡧࡵࡩࠥ࡬࡯ࡶࡰࡧ࠲ࠧ೫"))
    return {}
def getAccessibilityResultsSummary(driver):
  global CONFIG
  global bstack1llll111l_opy_
  if not bstack1111ll111_opy_.bstack1lll11l11_opy_(CONFIG, bstack1llll111l_opy_):
    logger.warning(bstack11l1l1l_opy_ (u"ࠦࡓࡵࡴࠡࡣࡱࠤࡆࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࠤࡆࡻࡴࡰ࡯ࡤࡸ࡮ࡵ࡮ࠡࡵࡨࡷࡸ࡯࡯࡯࠮ࠣࡧࡦࡴ࡮ࡰࡶࠣࡶࡪࡺࡲࡪࡧࡹࡩࠥࡇࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽࠥࡸࡥࡴࡷ࡯ࡸࡸࠦࡳࡶ࡯ࡰࡥࡷࡿ࠮ࠣ೬"))
    return {}
  try:
    bstack11l11llll_opy_ = driver.execute_script(bstack11l1l1l_opy_ (u"ࠧࠨࠢࠋࠢࠣࠤࠥࠦࠠࠡࠢࡵࡩࡹࡻࡲ࡯ࠢࡱࡩࡼࠦࡐࡳࡱࡰ࡭ࡸ࡫ࠨࡧࡷࡱࡧࡹ࡯࡯࡯ࠢࠫࡶࡪࡹ࡯࡭ࡸࡨ࠰ࠥࡸࡥ࡫ࡧࡦࡸ࠮ࠦࡻࠋࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࡴࡳࡻࠣࡿࠏࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࡤࡱࡱࡷࡹࠦࡥࡷࡧࡱࡸࠥࡃࠠ࡯ࡧࡺࠤࡈࡻࡳࡵࡱࡰࡉࡻ࡫࡮ࡵࠪࠪࡅ࠶࠷࡙ࡠࡖࡄࡔࡤࡍࡅࡕࡡࡕࡉࡘ࡛ࡌࡕࡕࡢࡗ࡚ࡓࡍࡂࡔ࡜ࠫ࠮ࡁࠊࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࡦࡳࡳࡹࡴࠡࡨࡱࠤࡂࠦࡦࡶࡰࡦࡸ࡮ࡵ࡮ࠡࠪࡨࡺࡪࡴࡴࠪࠢࡾࠎࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࡻ࡮ࡴࡤࡰࡹ࠱ࡶࡪࡳ࡯ࡷࡧࡈࡺࡪࡴࡴࡍ࡫ࡶࡸࡪࡴࡥࡳࠪࠪࡅ࠶࠷࡙ࡠࡔࡈࡗ࡚ࡒࡔࡔࡡࡖ࡙ࡒࡓࡁࡓ࡛ࡢࡖࡊ࡙ࡐࡐࡐࡖࡉࠬ࠲ࠠࡧࡰࠬ࠿ࠏࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࡷ࡫ࡳࡰ࡮ࡹࡩ࠭࡫ࡶࡦࡰࡷ࠲ࡩ࡫ࡴࡢ࡫࡯࠲ࡸࡻ࡭࡮ࡣࡵࡽ࠮ࡁࠊࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࢀ࠿ࠏࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࡸ࡫ࡱࡨࡴࡽ࠮ࡢࡦࡧࡉࡻ࡫࡮ࡵࡎ࡬ࡷࡹ࡫࡮ࡦࡴࠫࠫࡆ࠷࠱࡚ࡡࡕࡉࡘ࡛ࡌࡕࡕࡢࡗ࡚ࡓࡍࡂࡔ࡜ࡣࡗࡋࡓࡑࡑࡑࡗࡊ࠭ࠬࠡࡨࡱ࠭ࡀࠐࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࡹ࡬ࡲࡩࡵࡷ࠯ࡦ࡬ࡷࡵࡧࡴࡤࡪࡈࡺࡪࡴࡴࠩࡧࡹࡩࡳࡺࠩ࠼ࠌࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࡾࠢࡦࡥࡹࡩࡨࠡࡽࠍࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࡸࡥ࡫ࡧࡦࡸ࠭࠯࠻ࠋࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࡽࠋࠢࠣࠤࠥࠦࠠࠡࠢࢀ࠭ࡀࠐࠠࠡࠢࠣࠦࠧࠨ೭"))
    return bstack11l11llll_opy_
  except Exception:
    logger.error(bstack11l1l1l_opy_ (u"ࠨࡎࡰࠢࡤࡧࡨ࡫ࡳࡴ࡫ࡥ࡭ࡱ࡯ࡴࡺࠢࡶࡹࡲࡳࡡࡳࡻࠣࡻࡦࡹࠠࡧࡱࡸࡲࡩ࠴ࠢ೮"))
    return {}