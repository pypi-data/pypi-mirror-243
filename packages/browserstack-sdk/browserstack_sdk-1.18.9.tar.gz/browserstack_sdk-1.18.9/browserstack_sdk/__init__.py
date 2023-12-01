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
def bstack1ll11lll1_opy_():
  global CONFIG
  headers = {
        bstack11l1ll_opy_ (u"ࠪࡇࡴࡴࡴࡦࡰࡷ࠱ࡹࡿࡰࡦࠩࡶ"): bstack11l1ll_opy_ (u"ࠫࡦࡶࡰ࡭࡫ࡦࡥࡹ࡯࡯࡯࠱࡭ࡷࡴࡴࠧࡷ"),
      }
  proxies = bstack1lll111111_opy_(CONFIG, bstack11llll1l1_opy_)
  try:
    response = requests.get(bstack11llll1l1_opy_, headers=headers, proxies=proxies, timeout=5)
    if response.json():
      bstack11l1ll11l_opy_ = response.json()[bstack11l1ll_opy_ (u"ࠬ࡮ࡵࡣࡵࠪࡸ")]
      logger.debug(bstack11lll11l1_opy_.format(response.json()))
      return bstack11l1ll11l_opy_
    else:
      logger.debug(bstack1ll1l1ll1_opy_.format(bstack11l1ll_opy_ (u"ࠨࡒࡦࡵࡳࡳࡳࡹࡥࠡࡌࡖࡓࡓࠦࡰࡢࡴࡶࡩࠥ࡫ࡲࡳࡱࡵࠤࠧࡹ")))
  except Exception as e:
    logger.debug(bstack1ll1l1ll1_opy_.format(e))
def bstack1llll1l1l_opy_(hub_url):
  global CONFIG
  url = bstack11l1ll_opy_ (u"ࠢࡩࡶࡷࡴࡸࡀ࠯࠰ࠤࡺ")+  hub_url + bstack11l1ll_opy_ (u"ࠣ࠱ࡦ࡬ࡪࡩ࡫ࠣࡻ")
  headers = {
        bstack11l1ll_opy_ (u"ࠩࡆࡳࡳࡺࡥ࡯ࡶ࠰ࡸࡾࡶࡥࠨࡼ"): bstack11l1ll_opy_ (u"ࠪࡥࡵࡶ࡬ࡪࡥࡤࡸ࡮ࡵ࡮࠰࡬ࡶࡳࡳ࠭ࡽ"),
      }
  proxies = bstack1lll111111_opy_(CONFIG, url)
  try:
    start_time = time.perf_counter()
    requests.get(url, headers=headers, proxies=proxies, timeout=5)
    latency = time.perf_counter() - start_time
    logger.debug(bstack1ll111l11l_opy_.format(hub_url, latency))
    return dict(hub_url=hub_url, latency=latency)
  except Exception as e:
    logger.debug(bstack1ll1ll11l_opy_.format(hub_url, e))
def bstack111111l1_opy_():
  try:
    global bstack1lll1l1l1_opy_
    bstack11l1ll11l_opy_ = bstack1ll11lll1_opy_()
    bstack1l1llll1l1_opy_ = []
    results = []
    for bstack1ll111lll_opy_ in bstack11l1ll11l_opy_:
      bstack1l1llll1l1_opy_.append(bstack1llll1llll_opy_(target=bstack1llll1l1l_opy_,args=(bstack1ll111lll_opy_,)))
    for t in bstack1l1llll1l1_opy_:
      t.start()
    for t in bstack1l1llll1l1_opy_:
      results.append(t.join())
    bstack1l111l111_opy_ = {}
    for item in results:
      hub_url = item[bstack11l1ll_opy_ (u"ࠫ࡭ࡻࡢࡠࡷࡵࡰࠬࡾ")]
      latency = item[bstack11l1ll_opy_ (u"ࠬࡲࡡࡵࡧࡱࡧࡾ࠭ࡿ")]
      bstack1l111l111_opy_[hub_url] = latency
    bstack1l11lll11_opy_ = min(bstack1l111l111_opy_, key= lambda x: bstack1l111l111_opy_[x])
    bstack1lll1l1l1_opy_ = bstack1l11lll11_opy_
    logger.debug(bstack111l1l11l_opy_.format(bstack1l11lll11_opy_))
  except Exception as e:
    logger.debug(bstack11ll1111l_opy_.format(e))
from bstack_utils.messages import *
from bstack_utils.config import Config
from bstack_utils.helper import bstack1111l1lll_opy_, bstack1ll111l111_opy_, bstack11111l11_opy_, bstack1ll111ll1_opy_, Notset, bstack1ll1l111_opy_, \
  bstack1lll1l1l1l_opy_, bstack1l1llll11_opy_, bstack1lllll1lll_opy_, bstack1ll11ll1ll_opy_, bstack1l11ll11_opy_, bstack1l1l11lll_opy_, bstack1ll11l1l1_opy_, \
  bstack111l1llll_opy_, bstack1llll1l1l1_opy_, bstack1ll11lll11_opy_, bstack1111l1l1_opy_, bstack1l1lll1l1_opy_, bstack11l11l1ll_opy_, \
  bstack1111lll11_opy_, bstack111l1l1l1_opy_
from bstack_utils.bstack11l1ll111_opy_ import bstack1l1l111l_opy_
from bstack_utils.bstack1l11l11l1_opy_ import bstack1111ll1l1_opy_, bstack1l1ll111l_opy_
from bstack_utils.bstack1ll11ll1l1_opy_ import bstack11l1ll11_opy_
from bstack_utils.proxy import bstack111l1ll11_opy_, bstack1lll111111_opy_, bstack1l111lll1_opy_, bstack11111llll_opy_
import bstack_utils.bstack1111lll1_opy_ as bstack1ll111l11_opy_
from browserstack_sdk.bstack1llll1ll11_opy_ import *
from browserstack_sdk.bstack1ll1ll11ll_opy_ import *
from bstack_utils.bstack11ll1ll1_opy_ import bstack111l1111_opy_
bstack111lll1ll_opy_ = bstack11l1ll_opy_ (u"࠭ࠠࠡ࠱࠭ࠤࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽ࠡࠬ࠲ࡠࡳࠦࠠࡪࡨࠫࡴࡦ࡭ࡥࠡ࠿ࡀࡁࠥࡼ࡯ࡪࡦࠣ࠴࠮ࠦࡻ࡝ࡰࠣࠤࠥࡺࡲࡺࡽ࡟ࡲࠥࡩ࡯࡯ࡵࡷࠤ࡫ࡹࠠ࠾ࠢࡵࡩࡶࡻࡩࡳࡧࠫࡠࠬ࡬ࡳ࡝ࠩࠬ࠿ࡡࡴࠠࠡࠢࠣࠤ࡫ࡹ࠮ࡢࡲࡳࡩࡳࡪࡆࡪ࡮ࡨࡗࡾࡴࡣࠩࡤࡶࡸࡦࡩ࡫ࡠࡲࡤࡸ࡭࠲ࠠࡋࡕࡒࡒ࠳ࡹࡴࡳ࡫ࡱ࡫࡮࡬ࡹࠩࡲࡢ࡭ࡳࡪࡥࡹࠫࠣ࠯ࠥࠨ࠺ࠣࠢ࠮ࠤࡏ࡙ࡏࡏ࠰ࡶࡸࡷ࡯࡮ࡨ࡫ࡩࡽ࠭ࡐࡓࡐࡐ࠱ࡴࡦࡸࡳࡦࠪࠫࡥࡼࡧࡩࡵࠢࡱࡩࡼࡖࡡࡨࡧ࠵࠲ࡪࡼࡡ࡭ࡷࡤࡸࡪ࠮ࠢࠩࠫࠣࡁࡃࠦࡻࡾࠤ࠯ࠤࡡ࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࡤ࡫ࡸࡦࡥࡸࡸࡴࡸ࠺ࠡࡽࠥࡥࡨࡺࡩࡰࡰࠥ࠾ࠥࠨࡧࡦࡶࡖࡩࡸࡹࡩࡰࡰࡇࡩࡹࡧࡩ࡭ࡵࠥࢁࡡ࠭ࠩࠪࠫ࡞ࠦ࡭ࡧࡳࡩࡧࡧࡣ࡮ࡪࠢ࡞ࠫࠣ࠯ࠥࠨࠬ࡝࡞ࡱࠦ࠮ࡢ࡮ࠡࠢࠣࠤࢂࡩࡡࡵࡥ࡫ࠬࡪࡾࠩࡼ࡞ࡱࠤࠥࠦࠠࡾ࡞ࡱࠤࠥࢃ࡜࡯ࠢࠣ࠳࠯ࠦ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࠣ࠮࠴࠭ࢀ")
bstack1lll1111l_opy_ = bstack11l1ll_opy_ (u"ࠧ࡝ࡰ࠲࠮ࠥࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾ࠢ࠭࠳ࡡࡴࡣࡰࡰࡶࡸࠥࡨࡳࡵࡣࡦ࡯ࡤࡶࡡࡵࡪࠣࡁࠥࡶࡲࡰࡥࡨࡷࡸ࠴ࡡࡳࡩࡹ࡟ࡵࡸ࡯ࡤࡧࡶࡷ࠳ࡧࡲࡨࡸ࠱ࡰࡪࡴࡧࡵࡪࠣ࠱ࠥ࠹࡝࡝ࡰࡦࡳࡳࡹࡴࠡࡤࡶࡸࡦࡩ࡫ࡠࡥࡤࡴࡸࠦ࠽ࠡࡲࡵࡳࡨ࡫ࡳࡴ࠰ࡤࡶ࡬ࡼ࡛ࡱࡴࡲࡧࡪࡹࡳ࠯ࡣࡵ࡫ࡻ࠴࡬ࡦࡰࡪࡸ࡭ࠦ࠭ࠡ࠳ࡠࡠࡳࡩ࡯࡯ࡵࡷࠤࡵࡥࡩ࡯ࡦࡨࡼࠥࡃࠠࡱࡴࡲࡧࡪࡹࡳ࠯ࡣࡵ࡫ࡻࡡࡰࡳࡱࡦࡩࡸࡹ࠮ࡢࡴࡪࡺ࠳ࡲࡥ࡯ࡩࡷ࡬ࠥ࠳ࠠ࠳࡟࡟ࡲࡵࡸ࡯ࡤࡧࡶࡷ࠳ࡧࡲࡨࡸࠣࡁࠥࡶࡲࡰࡥࡨࡷࡸ࠴ࡡࡳࡩࡹ࠲ࡸࡲࡩࡤࡧࠫ࠴࠱ࠦࡰࡳࡱࡦࡩࡸࡹ࠮ࡢࡴࡪࡺ࠳ࡲࡥ࡯ࡩࡷ࡬ࠥ࠳ࠠ࠴ࠫ࡟ࡲࡨࡵ࡮ࡴࡶࠣ࡭ࡲࡶ࡯ࡳࡶࡢࡴࡱࡧࡹࡸࡴ࡬࡫࡭ࡺ࠴ࡠࡤࡶࡸࡦࡩ࡫ࠡ࠿ࠣࡶࡪࡷࡵࡪࡴࡨࠬࠧࡶ࡬ࡢࡻࡺࡶ࡮࡭ࡨࡵࠤࠬ࠿ࡡࡴࡩ࡮ࡲࡲࡶࡹࡥࡰ࡭ࡣࡼࡻࡷ࡯ࡧࡩࡶ࠷ࡣࡧࡹࡴࡢࡥ࡮࠲ࡨ࡮ࡲࡰ࡯࡬ࡹࡲ࠴࡬ࡢࡷࡱࡧ࡭ࠦ࠽ࠡࡣࡶࡽࡳࡩࠠࠩ࡮ࡤࡹࡳࡩࡨࡐࡲࡷ࡭ࡴࡴࡳࠪࠢࡀࡂࠥࢁ࡜࡯࡮ࡨࡸࠥࡩࡡࡱࡵ࠾ࡠࡳࡺࡲࡺࠢࡾࡠࡳࡩࡡࡱࡵࠣࡁࠥࡐࡓࡐࡐ࠱ࡴࡦࡸࡳࡦࠪࡥࡷࡹࡧࡣ࡬ࡡࡦࡥࡵࡹࠩ࡝ࡰࠣࠤࢂࠦࡣࡢࡶࡦ࡬࠭࡫ࡸࠪࠢࡾࡠࡳࠦࠠࠡࠢࢀࡠࡳࠦࠠࡳࡧࡷࡹࡷࡴࠠࡢࡹࡤ࡭ࡹࠦࡩ࡮ࡲࡲࡶࡹࡥࡰ࡭ࡣࡼࡻࡷ࡯ࡧࡩࡶ࠷ࡣࡧࡹࡴࡢࡥ࡮࠲ࡨ࡮ࡲࡰ࡯࡬ࡹࡲ࠴ࡣࡰࡰࡱࡩࡨࡺࠨࡼ࡞ࡱࠤࠥࠦࠠࡸࡵࡈࡲࡩࡶ࡯ࡪࡰࡷ࠾ࠥࡦࡷࡴࡵ࠽࠳࠴ࡩࡤࡱ࠰ࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫࠯ࡥࡲࡱ࠴ࡶ࡬ࡢࡻࡺࡶ࡮࡭ࡨࡵࡁࡦࡥࡵࡹ࠽ࠥࡽࡨࡲࡨࡵࡤࡦࡗࡕࡍࡈࡵ࡭ࡱࡱࡱࡩࡳࡺࠨࡋࡕࡒࡒ࠳ࡹࡴࡳ࡫ࡱ࡫࡮࡬ࡹࠩࡥࡤࡴࡸ࠯ࠩࡾࡢ࠯ࡠࡳࠦࠠࠡࠢ࠱࠲࠳ࡲࡡࡶࡰࡦ࡬ࡔࡶࡴࡪࡱࡱࡷࡡࡴࠠࠡࡿࠬࡠࡳࢃ࡜࡯࠱࠭ࠤࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽ࠡࠬ࠲ࡠࡳ࠭ࢁ")
from ._version import __version__
bstack1lll1ll1_opy_ = None
CONFIG = {}
bstack11l11ll1l_opy_ = {}
bstack11l1l11l1_opy_ = {}
bstack111l1l11_opy_ = None
bstack1l1lll11_opy_ = None
bstack1ll1ll1l1l_opy_ = None
bstack111lll111_opy_ = -1
bstack1lll11l1_opy_ = 0
bstack1l11llll1_opy_ = bstack111111l1l_opy_
bstack1ll1llllll_opy_ = 1
bstack1ll11l1ll1_opy_ = False
bstack11l1l1l11_opy_ = False
bstack11ll11ll1_opy_ = bstack11l1ll_opy_ (u"ࠨࠩࢂ")
bstack1l1111ll_opy_ = bstack11l1ll_opy_ (u"ࠩࠪࢃ")
bstack1ll11ll111_opy_ = False
bstack1l1lll1lll_opy_ = True
bstack1llll1ll_opy_ = bstack11l1ll_opy_ (u"ࠪࠫࢄ")
bstack11l1l1111_opy_ = []
bstack1lll1l1l1_opy_ = bstack11l1ll_opy_ (u"ࠫࠬࢅ")
bstack1111llll1_opy_ = False
bstack1ll1111ll_opy_ = None
bstack1lll11lll1_opy_ = None
bstack1lll1111_opy_ = -1
bstack1lll11111l_opy_ = os.path.join(os.path.expanduser(bstack11l1ll_opy_ (u"ࠬࢄࠧࢆ")), bstack11l1ll_opy_ (u"࠭࠮ࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠭ࢇ"), bstack11l1ll_opy_ (u"ࠧ࠯ࡴࡲࡦࡴࡺ࠭ࡳࡧࡳࡳࡷࡺ࠭ࡩࡧ࡯ࡴࡪࡸ࠮࡫ࡵࡲࡲࠬ࢈"))
bstack1ll1lll1ll_opy_ = 0
bstack1lllll11l1_opy_ = []
bstack11l111l11_opy_ = []
bstack11ll1lll_opy_ = []
bstack1l1ll1lll_opy_ = []
bstack111l1ll1_opy_ = bstack11l1ll_opy_ (u"ࠨࠩࢉ")
bstack11ll111ll_opy_ = bstack11l1ll_opy_ (u"ࠩࠪࢊ")
bstack1lll1111l1_opy_ = False
bstack1lll11l11_opy_ = False
bstack11l1llll_opy_ = {}
bstack1l11l11ll_opy_ = None
bstack1l11ll1ll_opy_ = None
bstack11lll1ll_opy_ = None
bstack1ll1ll111l_opy_ = None
bstack1ll11l1111_opy_ = None
bstack111l111l1_opy_ = None
bstack111l111ll_opy_ = None
bstack1l1lllll1l_opy_ = None
bstack111l11111_opy_ = None
bstack1l11lllll_opy_ = None
bstack1llll1111l_opy_ = None
bstack1ll111ll11_opy_ = None
bstack11l111111_opy_ = None
bstack1l1lll11ll_opy_ = None
bstack111llllll_opy_ = None
bstack1l1l1l1ll_opy_ = None
bstack1ll11ll11l_opy_ = None
bstack1lll11l111_opy_ = None
bstack1ll111llll_opy_ = None
bstack1ll11l11l_opy_ = bstack11l1ll_opy_ (u"ࠥࠦࢋ")
logger = logging.getLogger(__name__)
logging.basicConfig(level=bstack1l11llll1_opy_,
                    format=bstack11l1ll_opy_ (u"ࠫࡡࡴࠥࠩࡣࡶࡧࡹ࡯࡭ࡦࠫࡶࠤࡠࠫࠨ࡯ࡣࡰࡩ࠮ࡹ࡝࡜ࠧࠫࡰࡪࡼࡥ࡭ࡰࡤࡱࡪ࠯ࡳ࡞ࠢ࠰ࠤࠪ࠮࡭ࡦࡵࡶࡥ࡬࡫ࠩࡴࠩࢌ"),
                    datefmt=bstack11l1ll_opy_ (u"ࠬࠫࡈ࠻ࠧࡐ࠾࡙ࠪࠧࢍ"),
                    stream=sys.stdout)
bstack1ll1l11l1_opy_ = Config.get_instance()
percy = bstack1ll1l1l11_opy_()
def bstack1lll111l1_opy_():
  global CONFIG
  global bstack1l11llll1_opy_
  if bstack11l1ll_opy_ (u"࠭࡬ࡰࡩࡏࡩࡻ࡫࡬ࠨࢎ") in CONFIG:
    bstack1l11llll1_opy_ = bstack1ll11ll11_opy_[CONFIG[bstack11l1ll_opy_ (u"ࠧ࡭ࡱࡪࡐࡪࡼࡥ࡭ࠩ࢏")]]
    logging.getLogger().setLevel(bstack1l11llll1_opy_)
def bstack11111ll1l_opy_():
  global CONFIG
  global bstack1lll1111l1_opy_
  global bstack1ll1l11l1_opy_
  bstack11ll1ll11_opy_ = bstack1l11l1ll1_opy_(CONFIG)
  if (bstack11l1ll_opy_ (u"ࠨࡵ࡮࡭ࡵ࡙ࡥࡴࡵ࡬ࡳࡳࡔࡡ࡮ࡧࠪ࢐") in bstack11ll1ll11_opy_ and str(bstack11ll1ll11_opy_[bstack11l1ll_opy_ (u"ࠩࡶ࡯࡮ࡶࡓࡦࡵࡶ࡭ࡴࡴࡎࡢ࡯ࡨࠫ࢑")]).lower() == bstack11l1ll_opy_ (u"ࠪࡸࡷࡻࡥࠨ࢒")):
    bstack1lll1111l1_opy_ = True
  bstack1ll1l11l1_opy_.bstack1l11111l1_opy_(bstack11ll1ll11_opy_.get(bstack11l1ll_opy_ (u"ࠫࡸࡱࡩࡱࡕࡨࡷࡸ࡯࡯࡯ࡕࡷࡥࡹࡻࡳࠨ࢓"), False))
def bstack1111ll11l_opy_():
  from appium.version import version as appium_version
  return version.parse(appium_version)
def bstack1lll1ll1l_opy_():
  from selenium import webdriver
  return version.parse(webdriver.__version__)
def bstack1ll11l11l1_opy_():
  args = sys.argv
  for i in range(len(args)):
    if bstack11l1ll_opy_ (u"ࠧ࠳࠭ࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰࡩ࡯࡯ࡨ࡬࡫࡫࡯࡬ࡦࠤ࢔") == args[i].lower() or bstack11l1ll_opy_ (u"ࠨ࠭࠮ࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠮ࡤࡱࡱࡪ࡮࡭ࠢ࢕") == args[i].lower():
      path = args[i + 1]
      sys.argv.remove(args[i])
      sys.argv.remove(path)
      global bstack1llll1ll_opy_
      bstack1llll1ll_opy_ += bstack11l1ll_opy_ (u"ࠧ࠮࠯ࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࡄࡱࡱࡪ࡮࡭ࡆࡪ࡮ࡨࠤࠬ࢖") + path
      return path
  return None
bstack111l11ll_opy_ = re.compile(bstack11l1ll_opy_ (u"ࡳࠤ࠱࠮ࡄࡢࠤࡼࠪ࠱࠮ࡄ࠯ࡽ࠯ࠬࡂࠦࢗ"))
def bstack1ll1l1l1l_opy_(loader, node):
  value = loader.construct_scalar(node)
  for group in bstack111l11ll_opy_.findall(value):
    if group is not None and os.environ.get(group) is not None:
      value = value.replace(bstack11l1ll_opy_ (u"ࠤࠧࡿࠧ࢘") + group + bstack11l1ll_opy_ (u"ࠥࢁ࢙ࠧ"), os.environ.get(group))
  return value
def bstack1ll1l1l11l_opy_():
  bstack1ll1111l1l_opy_ = bstack1ll11l11l1_opy_()
  if bstack1ll1111l1l_opy_ and os.path.exists(os.path.abspath(bstack1ll1111l1l_opy_)):
    fileName = bstack1ll1111l1l_opy_
  if bstack11l1ll_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡇࡔࡔࡆࡊࡉࡢࡊࡎࡒࡅࠨ࢚") in os.environ and os.path.exists(
          os.path.abspath(os.environ[bstack11l1ll_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣࡈࡕࡎࡇࡋࡊࡣࡋࡏࡌࡆ࢛ࠩ")])) and not bstack11l1ll_opy_ (u"࠭ࡦࡪ࡮ࡨࡒࡦࡳࡥࠨ࢜") in locals():
    fileName = os.environ[bstack11l1ll_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡃࡐࡐࡉࡍࡌࡥࡆࡊࡎࡈࠫ࢝")]
  if bstack11l1ll_opy_ (u"ࠨࡨ࡬ࡰࡪࡔࡡ࡮ࡧࠪ࢞") in locals():
    bstack11l1_opy_ = os.path.abspath(fileName)
  else:
    bstack11l1_opy_ = bstack11l1ll_opy_ (u"ࠩࠪ࢟")
  bstack11l1l1lll_opy_ = os.getcwd()
  bstack1l1lllllll_opy_ = bstack11l1ll_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬࠰ࡼࡱࡱ࠭ࢠ")
  bstack1l111llll_opy_ = bstack11l1ll_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭࠱ࡽࡦࡳ࡬ࠨࢡ")
  while (not os.path.exists(bstack11l1_opy_)) and bstack11l1l1lll_opy_ != bstack11l1ll_opy_ (u"ࠧࠨࢢ"):
    bstack11l1_opy_ = os.path.join(bstack11l1l1lll_opy_, bstack1l1lllllll_opy_)
    if not os.path.exists(bstack11l1_opy_):
      bstack11l1_opy_ = os.path.join(bstack11l1l1lll_opy_, bstack1l111llll_opy_)
    if bstack11l1l1lll_opy_ != os.path.dirname(bstack11l1l1lll_opy_):
      bstack11l1l1lll_opy_ = os.path.dirname(bstack11l1l1lll_opy_)
    else:
      bstack11l1l1lll_opy_ = bstack11l1ll_opy_ (u"ࠨࠢࢣ")
  if not os.path.exists(bstack11l1_opy_):
    bstack1ll1111l1_opy_(
      bstack1llllllll1_opy_.format(os.getcwd()))
  try:
    with open(bstack11l1_opy_, bstack11l1ll_opy_ (u"ࠧࡳࠩࢤ")) as stream:
      yaml.add_implicit_resolver(bstack11l1ll_opy_ (u"ࠣࠣࡳࡥࡹ࡮ࡥࡹࠤࢥ"), bstack111l11ll_opy_)
      yaml.add_constructor(bstack11l1ll_opy_ (u"ࠤࠤࡴࡦࡺࡨࡦࡺࠥࢦ"), bstack1ll1l1l1l_opy_)
      config = yaml.load(stream, yaml.FullLoader)
      return config
  except:
    with open(bstack11l1_opy_, bstack11l1ll_opy_ (u"ࠪࡶࠬࢧ")) as stream:
      try:
        config = yaml.safe_load(stream)
        return config
      except yaml.YAMLError as exc:
        bstack1ll1111l1_opy_(bstack1l11l111_opy_.format(str(exc)))
def bstack1lllllllll_opy_(config):
  bstack1ll1111lll_opy_ = bstack1lllll1111_opy_(config)
  for option in list(bstack1ll1111lll_opy_):
    if option.lower() in bstack1lll111ll_opy_ and option != bstack1lll111ll_opy_[option.lower()]:
      bstack1ll1111lll_opy_[bstack1lll111ll_opy_[option.lower()]] = bstack1ll1111lll_opy_[option]
      del bstack1ll1111lll_opy_[option]
  return config
def bstack1llll1ll1_opy_():
  global bstack11l1l11l1_opy_
  for key, bstack1ll1l11ll_opy_ in bstack111l1l1l_opy_.items():
    if isinstance(bstack1ll1l11ll_opy_, list):
      for var in bstack1ll1l11ll_opy_:
        if var in os.environ and os.environ[var] and str(os.environ[var]).strip():
          bstack11l1l11l1_opy_[key] = os.environ[var]
          break
    elif bstack1ll1l11ll_opy_ in os.environ and os.environ[bstack1ll1l11ll_opy_] and str(os.environ[bstack1ll1l11ll_opy_]).strip():
      bstack11l1l11l1_opy_[key] = os.environ[bstack1ll1l11ll_opy_]
  if bstack11l1ll_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡐࡔࡉࡁࡍࡡࡌࡈࡊࡔࡔࡊࡈࡌࡉࡗ࠭ࢨ") in os.environ:
    bstack11l1l11l1_opy_[bstack11l1ll_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷ࡙ࡴࡢࡥ࡮ࡐࡴࡩࡡ࡭ࡑࡳࡸ࡮ࡵ࡮ࡴࠩࢩ")] = {}
    bstack11l1l11l1_opy_[bstack11l1ll_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡓࡵࡣࡦ࡯ࡑࡵࡣࡢ࡮ࡒࡴࡹ࡯࡯࡯ࡵࠪࢪ")][bstack11l1ll_opy_ (u"ࠧ࡭ࡱࡦࡥࡱࡏࡤࡦࡰࡷ࡭࡫࡯ࡥࡳࠩࢫ")] = os.environ[bstack11l1ll_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡍࡑࡆࡅࡑࡥࡉࡅࡇࡑࡘࡎࡌࡉࡆࡔࠪࢬ")]
def bstack1l111111_opy_():
  global bstack11l11ll1l_opy_
  global bstack1llll1ll_opy_
  for idx, val in enumerate(sys.argv):
    if idx < len(sys.argv) and bstack11l1ll_opy_ (u"ࠩ࠰࠱ࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭࠱ࡰࡴࡩࡡ࡭ࡋࡧࡩࡳࡺࡩࡧ࡫ࡨࡶࠬࢭ").lower() == val.lower():
      bstack11l11ll1l_opy_[bstack11l1ll_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡗࡹࡧࡣ࡬ࡎࡲࡧࡦࡲࡏࡱࡶ࡬ࡳࡳࡹࠧࢮ")] = {}
      bstack11l11ll1l_opy_[bstack11l1ll_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡘࡺࡡࡤ࡭ࡏࡳࡨࡧ࡬ࡐࡲࡷ࡭ࡴࡴࡳࠨࢯ")][bstack11l1ll_opy_ (u"ࠬࡲ࡯ࡤࡣ࡯ࡍࡩ࡫࡮ࡵ࡫ࡩ࡭ࡪࡸࠧࢰ")] = sys.argv[idx + 1]
      del sys.argv[idx:idx + 2]
      break
  for key, bstack11111lll_opy_ in bstack1llll11ll1_opy_.items():
    if isinstance(bstack11111lll_opy_, list):
      for idx, val in enumerate(sys.argv):
        for var in bstack11111lll_opy_:
          if idx < len(sys.argv) and bstack11l1ll_opy_ (u"࠭࠭࠮ࠩࢱ") + var.lower() == val.lower() and not key in bstack11l11ll1l_opy_:
            bstack11l11ll1l_opy_[key] = sys.argv[idx + 1]
            bstack1llll1ll_opy_ += bstack11l1ll_opy_ (u"ࠧࠡ࠯࠰ࠫࢲ") + var + bstack11l1ll_opy_ (u"ࠨࠢࠪࢳ") + sys.argv[idx + 1]
            del sys.argv[idx:idx + 2]
            break
    else:
      for idx, val in enumerate(sys.argv):
        if idx < len(sys.argv) and bstack11l1ll_opy_ (u"ࠩ࠰࠱ࠬࢴ") + bstack11111lll_opy_.lower() == val.lower() and not key in bstack11l11ll1l_opy_:
          bstack11l11ll1l_opy_[key] = sys.argv[idx + 1]
          bstack1llll1ll_opy_ += bstack11l1ll_opy_ (u"ࠪࠤ࠲࠳ࠧࢵ") + bstack11111lll_opy_ + bstack11l1ll_opy_ (u"ࠫࠥ࠭ࢶ") + sys.argv[idx + 1]
          del sys.argv[idx:idx + 2]
def bstack1l1lll1111_opy_(config):
  bstack1llll111l1_opy_ = config.keys()
  for bstack1111l11l_opy_, bstack1ll1l1l1l1_opy_ in bstack1lll1l111l_opy_.items():
    if bstack1ll1l1l1l1_opy_ in bstack1llll111l1_opy_:
      config[bstack1111l11l_opy_] = config[bstack1ll1l1l1l1_opy_]
      del config[bstack1ll1l1l1l1_opy_]
  for bstack1111l11l_opy_, bstack1ll1l1l1l1_opy_ in bstack1l11l11l_opy_.items():
    if isinstance(bstack1ll1l1l1l1_opy_, list):
      for bstack111llll1_opy_ in bstack1ll1l1l1l1_opy_:
        if bstack111llll1_opy_ in bstack1llll111l1_opy_:
          config[bstack1111l11l_opy_] = config[bstack111llll1_opy_]
          del config[bstack111llll1_opy_]
          break
    elif bstack1ll1l1l1l1_opy_ in bstack1llll111l1_opy_:
      config[bstack1111l11l_opy_] = config[bstack1ll1l1l1l1_opy_]
      del config[bstack1ll1l1l1l1_opy_]
  for bstack111llll1_opy_ in list(config):
    for bstack111lll11_opy_ in bstack1l1ll1l1_opy_:
      if bstack111llll1_opy_.lower() == bstack111lll11_opy_.lower() and bstack111llll1_opy_ != bstack111lll11_opy_:
        config[bstack111lll11_opy_] = config[bstack111llll1_opy_]
        del config[bstack111llll1_opy_]
  bstack11l1111ll_opy_ = []
  if bstack11l1ll_opy_ (u"ࠬࡶ࡬ࡢࡶࡩࡳࡷࡳࡳࠨࢷ") in config:
    bstack11l1111ll_opy_ = config[bstack11l1ll_opy_ (u"࠭ࡰ࡭ࡣࡷࡪࡴࡸ࡭ࡴࠩࢸ")]
  for platform in bstack11l1111ll_opy_:
    for bstack111llll1_opy_ in list(platform):
      for bstack111lll11_opy_ in bstack1l1ll1l1_opy_:
        if bstack111llll1_opy_.lower() == bstack111lll11_opy_.lower() and bstack111llll1_opy_ != bstack111lll11_opy_:
          platform[bstack111lll11_opy_] = platform[bstack111llll1_opy_]
          del platform[bstack111llll1_opy_]
  for bstack1111l11l_opy_, bstack1ll1l1l1l1_opy_ in bstack1l11l11l_opy_.items():
    for platform in bstack11l1111ll_opy_:
      if isinstance(bstack1ll1l1l1l1_opy_, list):
        for bstack111llll1_opy_ in bstack1ll1l1l1l1_opy_:
          if bstack111llll1_opy_ in platform:
            platform[bstack1111l11l_opy_] = platform[bstack111llll1_opy_]
            del platform[bstack111llll1_opy_]
            break
      elif bstack1ll1l1l1l1_opy_ in platform:
        platform[bstack1111l11l_opy_] = platform[bstack1ll1l1l1l1_opy_]
        del platform[bstack1ll1l1l1l1_opy_]
  for bstack1l1llllll_opy_ in bstack1111l111_opy_:
    if bstack1l1llllll_opy_ in config:
      if not bstack1111l111_opy_[bstack1l1llllll_opy_] in config:
        config[bstack1111l111_opy_[bstack1l1llllll_opy_]] = {}
      config[bstack1111l111_opy_[bstack1l1llllll_opy_]].update(config[bstack1l1llllll_opy_])
      del config[bstack1l1llllll_opy_]
  for platform in bstack11l1111ll_opy_:
    for bstack1l1llllll_opy_ in bstack1111l111_opy_:
      if bstack1l1llllll_opy_ in list(platform):
        if not bstack1111l111_opy_[bstack1l1llllll_opy_] in platform:
          platform[bstack1111l111_opy_[bstack1l1llllll_opy_]] = {}
        platform[bstack1111l111_opy_[bstack1l1llllll_opy_]].update(platform[bstack1l1llllll_opy_])
        del platform[bstack1l1llllll_opy_]
  config = bstack1lllllllll_opy_(config)
  return config
def bstack1l1llllll1_opy_(config):
  global bstack1l1111ll_opy_
  if bstack11l1ll_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰࡒ࡯ࡤࡣ࡯ࠫࢹ") in config and str(config[bstack11l1ll_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱࡌࡰࡥࡤࡰࠬࢺ")]).lower() != bstack11l1ll_opy_ (u"ࠩࡩࡥࡱࡹࡥࠨࢻ"):
    if not bstack11l1ll_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡗࡹࡧࡣ࡬ࡎࡲࡧࡦࡲࡏࡱࡶ࡬ࡳࡳࡹࠧࢼ") in config:
      config[bstack11l1ll_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡘࡺࡡࡤ࡭ࡏࡳࡨࡧ࡬ࡐࡲࡷ࡭ࡴࡴࡳࠨࢽ")] = {}
    if not bstack11l1ll_opy_ (u"ࠬࡲ࡯ࡤࡣ࡯ࡍࡩ࡫࡮ࡵ࡫ࡩ࡭ࡪࡸࠧࢾ") in config[bstack11l1ll_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡓࡵࡣࡦ࡯ࡑࡵࡣࡢ࡮ࡒࡴࡹ࡯࡯࡯ࡵࠪࢿ")]:
      bstack1ll11111ll_opy_ = datetime.datetime.now()
      bstack1ll1l1ll1l_opy_ = bstack1ll11111ll_opy_.strftime(bstack11l1ll_opy_ (u"ࠧࠦࡦࡢࠩࡧࡥࠥࡉࠧࡐࠫࣀ"))
      hostname = socket.gethostname()
      bstack111l11l1l_opy_ = bstack11l1ll_opy_ (u"ࠨࠩࣁ").join(random.choices(string.ascii_lowercase + string.digits, k=4))
      identifier = bstack11l1ll_opy_ (u"ࠩࡾࢁࡤࢁࡽࡠࡽࢀࠫࣂ").format(bstack1ll1l1ll1l_opy_, hostname, bstack111l11l1l_opy_)
      config[bstack11l1ll_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡗࡹࡧࡣ࡬ࡎࡲࡧࡦࡲࡏࡱࡶ࡬ࡳࡳࡹࠧࣃ")][bstack11l1ll_opy_ (u"ࠫࡱࡵࡣࡢ࡮ࡌࡨࡪࡴࡴࡪࡨ࡬ࡩࡷ࠭ࣄ")] = identifier
    bstack1l1111ll_opy_ = config[bstack11l1ll_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷ࡙ࡴࡢࡥ࡮ࡐࡴࡩࡡ࡭ࡑࡳࡸ࡮ࡵ࡮ࡴࠩࣅ")][bstack11l1ll_opy_ (u"࠭࡬ࡰࡥࡤࡰࡎࡪࡥ࡯ࡶ࡬ࡪ࡮࡫ࡲࠨࣆ")]
  return config
def bstack1l11lll1l_opy_():
  bstack1ll111l1l_opy_ =  bstack1ll11ll1ll_opy_()[bstack11l1ll_opy_ (u"ࠧࡣࡷ࡬ࡰࡩࡥ࡮ࡶ࡯ࡥࡩࡷ࠭ࣇ")]
  return bstack1ll111l1l_opy_ if bstack1ll111l1l_opy_ else -1
def bstack111ll1ll_opy_(bstack1ll111l1l_opy_):
  global CONFIG
  if not bstack11l1ll_opy_ (u"ࠨࠦࡾࡆ࡚ࡏࡌࡅࡡࡑ࡙ࡒࡈࡅࡓࡿࠪࣈ") in CONFIG[bstack11l1ll_opy_ (u"ࠩࡥࡹ࡮ࡲࡤࡊࡦࡨࡲࡹ࡯ࡦࡪࡧࡵࠫࣉ")]:
    return
  CONFIG[bstack11l1ll_opy_ (u"ࠪࡦࡺ࡯࡬ࡥࡋࡧࡩࡳࡺࡩࡧ࡫ࡨࡶࠬ࣊")] = CONFIG[bstack11l1ll_opy_ (u"ࠫࡧࡻࡩ࡭ࡦࡌࡨࡪࡴࡴࡪࡨ࡬ࡩࡷ࠭࣋")].replace(
    bstack11l1ll_opy_ (u"ࠬࠪࡻࡃࡗࡌࡐࡉࡥࡎࡖࡏࡅࡉࡗࢃࠧ࣌"),
    str(bstack1ll111l1l_opy_)
  )
def bstack1l11111l_opy_():
  global CONFIG
  if not bstack11l1ll_opy_ (u"࠭ࠤࡼࡆࡄࡘࡊࡥࡔࡊࡏࡈࢁࠬ࣍") in CONFIG[bstack11l1ll_opy_ (u"ࠧࡣࡷ࡬ࡰࡩࡏࡤࡦࡰࡷ࡭࡫࡯ࡥࡳࠩ࣎")]:
    return
  bstack1ll11111ll_opy_ = datetime.datetime.now()
  bstack1ll1l1ll1l_opy_ = bstack1ll11111ll_opy_.strftime(bstack11l1ll_opy_ (u"ࠨࠧࡧ࠱ࠪࡨ࠭ࠦࡊ࠽ࠩࡒ࣏࠭"))
  CONFIG[bstack11l1ll_opy_ (u"ࠩࡥࡹ࡮ࡲࡤࡊࡦࡨࡲࡹ࡯ࡦࡪࡧࡵ࣐ࠫ")] = CONFIG[bstack11l1ll_opy_ (u"ࠪࡦࡺ࡯࡬ࡥࡋࡧࡩࡳࡺࡩࡧ࡫ࡨࡶ࣑ࠬ")].replace(
    bstack11l1ll_opy_ (u"ࠫࠩࢁࡄࡂࡖࡈࡣ࡙ࡏࡍࡆࡿ࣒ࠪ"),
    bstack1ll1l1ll1l_opy_
  )
def bstack1ll111lll1_opy_():
  global CONFIG
  if bstack11l1ll_opy_ (u"ࠬࡨࡵࡪ࡮ࡧࡍࡩ࡫࡮ࡵ࡫ࡩ࡭ࡪࡸ࣓ࠧ") in CONFIG and not bool(CONFIG[bstack11l1ll_opy_ (u"࠭ࡢࡶ࡫࡯ࡨࡎࡪࡥ࡯ࡶ࡬ࡪ࡮࡫ࡲࠨࣔ")]):
    del CONFIG[bstack11l1ll_opy_ (u"ࠧࡣࡷ࡬ࡰࡩࡏࡤࡦࡰࡷ࡭࡫࡯ࡥࡳࠩࣕ")]
    return
  if not bstack11l1ll_opy_ (u"ࠨࡤࡸ࡭ࡱࡪࡉࡥࡧࡱࡸ࡮࡬ࡩࡦࡴࠪࣖ") in CONFIG:
    CONFIG[bstack11l1ll_opy_ (u"ࠩࡥࡹ࡮ࡲࡤࡊࡦࡨࡲࡹ࡯ࡦࡪࡧࡵࠫࣗ")] = bstack11l1ll_opy_ (u"ࠪࠧࠩࢁࡂࡖࡋࡏࡈࡤࡔࡕࡎࡄࡈࡖࢂ࠭ࣘ")
  if bstack11l1ll_opy_ (u"ࠫࠩࢁࡄࡂࡖࡈࡣ࡙ࡏࡍࡆࡿࠪࣙ") in CONFIG[bstack11l1ll_opy_ (u"ࠬࡨࡵࡪ࡮ࡧࡍࡩ࡫࡮ࡵ࡫ࡩ࡭ࡪࡸࠧࣚ")]:
    bstack1l11111l_opy_()
    os.environ[bstack11l1ll_opy_ (u"࠭ࡂࡔࡖࡄࡇࡐࡥࡃࡐࡏࡅࡍࡓࡋࡄࡠࡄࡘࡍࡑࡊ࡟ࡊࡆࠪࣛ")] = CONFIG[bstack11l1ll_opy_ (u"ࠧࡣࡷ࡬ࡰࡩࡏࡤࡦࡰࡷ࡭࡫࡯ࡥࡳࠩࣜ")]
  if not bstack11l1ll_opy_ (u"ࠨࠦࡾࡆ࡚ࡏࡌࡅࡡࡑ࡙ࡒࡈࡅࡓࡿࠪࣝ") in CONFIG[bstack11l1ll_opy_ (u"ࠩࡥࡹ࡮ࡲࡤࡊࡦࡨࡲࡹ࡯ࡦࡪࡧࡵࠫࣞ")]:
    return
  bstack1ll111l1l_opy_ = bstack11l1ll_opy_ (u"ࠪࠫࣟ")
  bstack1ll111ll_opy_ = bstack1l11lll1l_opy_()
  if bstack1ll111ll_opy_ != -1:
    bstack1ll111l1l_opy_ = bstack11l1ll_opy_ (u"ࠫࡈࡏࠠࠨ࣠") + str(bstack1ll111ll_opy_)
  if bstack1ll111l1l_opy_ == bstack11l1ll_opy_ (u"ࠬ࠭࣡"):
    bstack111lll11l_opy_ = bstack11l1l111l_opy_(CONFIG[bstack11l1ll_opy_ (u"࠭ࡢࡶ࡫࡯ࡨࡓࡧ࡭ࡦࠩ࣢")])
    if bstack111lll11l_opy_ != -1:
      bstack1ll111l1l_opy_ = str(bstack111lll11l_opy_)
  if bstack1ll111l1l_opy_:
    bstack111ll1ll_opy_(bstack1ll111l1l_opy_)
    os.environ[bstack11l1ll_opy_ (u"ࠧࡃࡕࡗࡅࡈࡑ࡟ࡄࡑࡐࡆࡎࡔࡅࡅࡡࡅ࡙ࡎࡒࡄࡠࡋࡇࣣࠫ")] = CONFIG[bstack11l1ll_opy_ (u"ࠨࡤࡸ࡭ࡱࡪࡉࡥࡧࡱࡸ࡮࡬ࡩࡦࡴࠪࣤ")]
def bstack1l1ll1lll1_opy_(bstack11l1111l_opy_, bstack1l11111ll_opy_, path):
  bstack11lll111l_opy_ = {
    bstack11l1ll_opy_ (u"ࠩ࡬ࡨࡪࡴࡴࡪࡨ࡬ࡩࡷ࠭ࣥ"): bstack1l11111ll_opy_
  }
  if os.path.exists(path):
    bstack1ll1111ll1_opy_ = json.load(open(path, bstack11l1ll_opy_ (u"ࠪࡶࡧࣦ࠭")))
  else:
    bstack1ll1111ll1_opy_ = {}
  bstack1ll1111ll1_opy_[bstack11l1111l_opy_] = bstack11lll111l_opy_
  with open(path, bstack11l1ll_opy_ (u"ࠦࡼ࠱ࠢࣧ")) as outfile:
    json.dump(bstack1ll1111ll1_opy_, outfile)
def bstack11l1l111l_opy_(bstack11l1111l_opy_):
  bstack11l1111l_opy_ = str(bstack11l1111l_opy_)
  bstack1llll1l111_opy_ = os.path.join(os.path.expanduser(bstack11l1ll_opy_ (u"ࠬࢄࠧࣨ")), bstack11l1ll_opy_ (u"࠭࠮ࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰࣩ࠭"))
  try:
    if not os.path.exists(bstack1llll1l111_opy_):
      os.makedirs(bstack1llll1l111_opy_)
    file_path = os.path.join(os.path.expanduser(bstack11l1ll_opy_ (u"ࠧࡿࠩ࣪")), bstack11l1ll_opy_ (u"ࠨ࠰ࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࠨ࣫"), bstack11l1ll_opy_ (u"ࠩ࠱ࡦࡺ࡯࡬ࡥ࠯ࡱࡥࡲ࡫࠭ࡤࡣࡦ࡬ࡪ࠴ࡪࡴࡱࡱࠫ࣬"))
    if not os.path.isfile(file_path):
      with open(file_path, bstack11l1ll_opy_ (u"ࠪࡻ࣭ࠬ")):
        pass
      with open(file_path, bstack11l1ll_opy_ (u"ࠦࡼ࠱࣮ࠢ")) as outfile:
        json.dump({}, outfile)
    with open(file_path, bstack11l1ll_opy_ (u"ࠬࡸ࣯ࠧ")) as bstack11l11l1l_opy_:
      bstack111l11lll_opy_ = json.load(bstack11l11l1l_opy_)
    if bstack11l1111l_opy_ in bstack111l11lll_opy_:
      bstack1ll1ll11l1_opy_ = bstack111l11lll_opy_[bstack11l1111l_opy_][bstack11l1ll_opy_ (u"࠭ࡩࡥࡧࡱࡸ࡮࡬ࡩࡦࡴࣰࠪ")]
      bstack1111ll11_opy_ = int(bstack1ll1ll11l1_opy_) + 1
      bstack1l1ll1lll1_opy_(bstack11l1111l_opy_, bstack1111ll11_opy_, file_path)
      return bstack1111ll11_opy_
    else:
      bstack1l1ll1lll1_opy_(bstack11l1111l_opy_, 1, file_path)
      return 1
  except Exception as e:
    logger.warn(bstack111llll11_opy_.format(str(e)))
    return -1
def bstack1l111ll1_opy_(config):
  if not config[bstack11l1ll_opy_ (u"ࠧࡶࡵࡨࡶࡓࡧ࡭ࡦࣱࠩ")] or not config[bstack11l1ll_opy_ (u"ࠨࡣࡦࡧࡪࡹࡳࡌࡧࡼࣲࠫ")]:
    return True
  else:
    return False
def bstack1l11l1lll_opy_(config, index=0):
  global bstack1ll11ll111_opy_
  bstack11ll1l111_opy_ = {}
  caps = bstack111l1l111_opy_ + bstack1l1111l1_opy_
  if bstack1ll11ll111_opy_:
    caps += bstack1lll1111ll_opy_
  for key in config:
    if key in caps + [bstack11l1ll_opy_ (u"ࠩࡳࡰࡦࡺࡦࡰࡴࡰࡷࠬࣳ")]:
      continue
    bstack11ll1l111_opy_[key] = config[key]
  if bstack11l1ll_opy_ (u"ࠪࡴࡱࡧࡴࡧࡱࡵࡱࡸ࠭ࣴ") in config:
    for bstack1ll1l1ll11_opy_ in config[bstack11l1ll_opy_ (u"ࠫࡵࡲࡡࡵࡨࡲࡶࡲࡹࠧࣵ")][index]:
      if bstack1ll1l1ll11_opy_ in caps + [bstack11l1ll_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡔࡡ࡮ࡧࣶࠪ"), bstack11l1ll_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡖࡦࡴࡶ࡭ࡴࡴࠧࣷ")]:
        continue
      bstack11ll1l111_opy_[bstack1ll1l1ll11_opy_] = config[bstack11l1ll_opy_ (u"ࠧࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࡵࠪࣸ")][index][bstack1ll1l1ll11_opy_]
  bstack11ll1l111_opy_[bstack11l1ll_opy_ (u"ࠨࡪࡲࡷࡹࡔࡡ࡮ࡧࣹࠪ")] = socket.gethostname()
  if bstack11l1ll_opy_ (u"ࠩࡹࡩࡷࡹࡩࡰࡰࣺࠪ") in bstack11ll1l111_opy_:
    del (bstack11ll1l111_opy_[bstack11l1ll_opy_ (u"ࠪࡺࡪࡸࡳࡪࡱࡱࠫࣻ")])
  return bstack11ll1l111_opy_
def bstack111l1ll1l_opy_(config):
  global bstack1ll11ll111_opy_
  bstack11llll11l_opy_ = {}
  caps = bstack1l1111l1_opy_
  if bstack1ll11ll111_opy_:
    caps += bstack1lll1111ll_opy_
  for key in caps:
    if key in config:
      bstack11llll11l_opy_[key] = config[key]
  return bstack11llll11l_opy_
def bstack1lll11l11l_opy_(bstack11ll1l111_opy_, bstack11llll11l_opy_):
  bstack11l1l11l_opy_ = {}
  for key in bstack11ll1l111_opy_.keys():
    if key in bstack1lll1l111l_opy_:
      bstack11l1l11l_opy_[bstack1lll1l111l_opy_[key]] = bstack11ll1l111_opy_[key]
    else:
      bstack11l1l11l_opy_[key] = bstack11ll1l111_opy_[key]
  for key in bstack11llll11l_opy_:
    if key in bstack1lll1l111l_opy_:
      bstack11l1l11l_opy_[bstack1lll1l111l_opy_[key]] = bstack11llll11l_opy_[key]
    else:
      bstack11l1l11l_opy_[key] = bstack11llll11l_opy_[key]
  return bstack11l1l11l_opy_
def bstack1llll1l1ll_opy_(config, index=0):
  global bstack1ll11ll111_opy_
  config = copy.deepcopy(config)
  caps = {}
  bstack11llll11l_opy_ = bstack111l1ll1l_opy_(config)
  bstack1l11l1l1_opy_ = bstack1l1111l1_opy_
  bstack1l11l1l1_opy_ += bstack1ll11l111_opy_
  if bstack1ll11ll111_opy_:
    bstack1l11l1l1_opy_ += bstack1lll1111ll_opy_
  if bstack11l1ll_opy_ (u"ࠫࡵࡲࡡࡵࡨࡲࡶࡲࡹࠧࣼ") in config:
    if bstack11l1ll_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡔࡡ࡮ࡧࠪࣽ") in config[bstack11l1ll_opy_ (u"࠭ࡰ࡭ࡣࡷࡪࡴࡸ࡭ࡴࠩࣾ")][index]:
      caps[bstack11l1ll_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡏࡣࡰࡩࠬࣿ")] = config[bstack11l1ll_opy_ (u"ࠨࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࡶࠫऀ")][index][bstack11l1ll_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡑࡥࡲ࡫ࠧँ")]
    if bstack11l1ll_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵ࡚ࡪࡸࡳࡪࡱࡱࠫं") in config[bstack11l1ll_opy_ (u"ࠫࡵࡲࡡࡵࡨࡲࡶࡲࡹࠧः")][index]:
      caps[bstack11l1ll_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷ࡜ࡥࡳࡵ࡬ࡳࡳ࠭ऄ")] = str(config[bstack11l1ll_opy_ (u"࠭ࡰ࡭ࡣࡷࡪࡴࡸ࡭ࡴࠩअ")][index][bstack11l1ll_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡗࡧࡵࡷ࡮ࡵ࡮ࠨआ")])
    bstack11ll111l1_opy_ = {}
    for bstack1l11ll1l_opy_ in bstack1l11l1l1_opy_:
      if bstack1l11ll1l_opy_ in config[bstack11l1ll_opy_ (u"ࠨࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࡶࠫइ")][index]:
        if bstack1l11ll1l_opy_ == bstack11l1ll_opy_ (u"ࠩࡳࡰࡦࡺࡦࡰࡴࡰ࡚ࡪࡸࡳࡪࡱࡱࠫई"):
          try:
            bstack11ll111l1_opy_[bstack1l11ll1l_opy_] = str(config[bstack11l1ll_opy_ (u"ࠪࡴࡱࡧࡴࡧࡱࡵࡱࡸ࠭उ")][index][bstack1l11ll1l_opy_] * 1.0)
          except:
            bstack11ll111l1_opy_[bstack1l11ll1l_opy_] = str(config[bstack11l1ll_opy_ (u"ࠫࡵࡲࡡࡵࡨࡲࡶࡲࡹࠧऊ")][index][bstack1l11ll1l_opy_])
        else:
          bstack11ll111l1_opy_[bstack1l11ll1l_opy_] = config[bstack11l1ll_opy_ (u"ࠬࡶ࡬ࡢࡶࡩࡳࡷࡳࡳࠨऋ")][index][bstack1l11ll1l_opy_]
        del (config[bstack11l1ll_opy_ (u"࠭ࡰ࡭ࡣࡷࡪࡴࡸ࡭ࡴࠩऌ")][index][bstack1l11ll1l_opy_])
    bstack11llll11l_opy_ = update(bstack11llll11l_opy_, bstack11ll111l1_opy_)
  bstack11ll1l111_opy_ = bstack1l11l1lll_opy_(config, index)
  for bstack111llll1_opy_ in bstack1l1111l1_opy_ + [bstack11l1ll_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡏࡣࡰࡩࠬऍ"), bstack11l1ll_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡘࡨࡶࡸ࡯࡯࡯ࠩऎ")]:
    if bstack111llll1_opy_ in bstack11ll1l111_opy_:
      bstack11llll11l_opy_[bstack111llll1_opy_] = bstack11ll1l111_opy_[bstack111llll1_opy_]
      del (bstack11ll1l111_opy_[bstack111llll1_opy_])
  if bstack1ll1l111_opy_(config):
    bstack11ll1l111_opy_[bstack11l1ll_opy_ (u"ࠩࡸࡷࡪ࡝࠳ࡄࠩए")] = True
    caps.update(bstack11llll11l_opy_)
    caps[bstack11l1ll_opy_ (u"ࠪࡦࡸࡺࡡࡤ࡭࠽ࡳࡵࡺࡩࡰࡰࡶࠫऐ")] = bstack11ll1l111_opy_
  else:
    bstack11ll1l111_opy_[bstack11l1ll_opy_ (u"ࠫࡺࡹࡥࡘ࠵ࡆࠫऑ")] = False
    caps.update(bstack1lll11l11l_opy_(bstack11ll1l111_opy_, bstack11llll11l_opy_))
    if bstack11l1ll_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡔࡡ࡮ࡧࠪऒ") in caps:
      caps[bstack11l1ll_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࠧओ")] = caps[bstack11l1ll_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡏࡣࡰࡩࠬऔ")]
      del (caps[bstack11l1ll_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡐࡤࡱࡪ࠭क")])
    if bstack11l1ll_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴ࡙ࡩࡷࡹࡩࡰࡰࠪख") in caps:
      caps[bstack11l1ll_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡣࡻ࡫ࡲࡴ࡫ࡲࡲࠬग")] = caps[bstack11l1ll_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶ࡛࡫ࡲࡴ࡫ࡲࡲࠬघ")]
      del (caps[bstack11l1ll_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷ࡜ࡥࡳࡵ࡬ࡳࡳ࠭ङ")])
  return caps
def bstack1ll1lll1_opy_():
  global bstack1lll1l1l1_opy_
  if bstack1lll1ll1l_opy_() <= version.parse(bstack11l1ll_opy_ (u"࠭࠳࠯࠳࠶࠲࠵࠭च")):
    if bstack1lll1l1l1_opy_ != bstack11l1ll_opy_ (u"ࠧࠨछ"):
      return bstack11l1ll_opy_ (u"ࠣࡪࡷࡸࡵࡀ࠯࠰ࠤज") + bstack1lll1l1l1_opy_ + bstack11l1ll_opy_ (u"ࠤ࠽࠼࠵࠵ࡷࡥ࠱࡫ࡹࡧࠨझ")
    return bstack11lllll1l_opy_
  if bstack1lll1l1l1_opy_ != bstack11l1ll_opy_ (u"ࠪࠫञ"):
    return bstack11l1ll_opy_ (u"ࠦ࡭ࡺࡴࡱࡵ࠽࠳࠴ࠨट") + bstack1lll1l1l1_opy_ + bstack11l1ll_opy_ (u"ࠧ࠵ࡷࡥ࠱࡫ࡹࡧࠨठ")
  return bstack1ll111l1_opy_
def bstack1ll1l1llll_opy_(options):
  return hasattr(options, bstack11l1ll_opy_ (u"࠭ࡳࡦࡶࡢࡧࡦࡶࡡࡣ࡫࡯࡭ࡹࡿࠧड"))
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
def bstack1l1llll1_opy_(options, bstack1llll11l1l_opy_):
  for bstack1l11l1l1l_opy_ in bstack1llll11l1l_opy_:
    if bstack1l11l1l1l_opy_ in [bstack11l1ll_opy_ (u"ࠧࡢࡴࡪࡷࠬढ"), bstack11l1ll_opy_ (u"ࠨࡧࡻࡸࡪࡴࡳࡪࡱࡱࡷࠬण")]:
      continue
    if bstack1l11l1l1l_opy_ in options._experimental_options:
      options._experimental_options[bstack1l11l1l1l_opy_] = update(options._experimental_options[bstack1l11l1l1l_opy_],
                                                         bstack1llll11l1l_opy_[bstack1l11l1l1l_opy_])
    else:
      options.add_experimental_option(bstack1l11l1l1l_opy_, bstack1llll11l1l_opy_[bstack1l11l1l1l_opy_])
  if bstack11l1ll_opy_ (u"ࠩࡤࡶ࡬ࡹࠧत") in bstack1llll11l1l_opy_:
    for arg in bstack1llll11l1l_opy_[bstack11l1ll_opy_ (u"ࠪࡥࡷ࡭ࡳࠨथ")]:
      options.add_argument(arg)
    del (bstack1llll11l1l_opy_[bstack11l1ll_opy_ (u"ࠫࡦࡸࡧࡴࠩद")])
  if bstack11l1ll_opy_ (u"ࠬ࡫ࡸࡵࡧࡱࡷ࡮ࡵ࡮ࡴࠩध") in bstack1llll11l1l_opy_:
    for ext in bstack1llll11l1l_opy_[bstack11l1ll_opy_ (u"࠭ࡥࡹࡶࡨࡲࡸ࡯࡯࡯ࡵࠪन")]:
      options.add_extension(ext)
    del (bstack1llll11l1l_opy_[bstack11l1ll_opy_ (u"ࠧࡦࡺࡷࡩࡳࡹࡩࡰࡰࡶࠫऩ")])
def bstack1ll1l1l1_opy_(options, bstack1l1ll1ll1l_opy_):
  if bstack11l1ll_opy_ (u"ࠨࡲࡵࡩ࡫ࡹࠧप") in bstack1l1ll1ll1l_opy_:
    for bstack1l1lllll_opy_ in bstack1l1ll1ll1l_opy_[bstack11l1ll_opy_ (u"ࠩࡳࡶࡪ࡬ࡳࠨफ")]:
      if bstack1l1lllll_opy_ in options._preferences:
        options._preferences[bstack1l1lllll_opy_] = update(options._preferences[bstack1l1lllll_opy_], bstack1l1ll1ll1l_opy_[bstack11l1ll_opy_ (u"ࠪࡴࡷ࡫ࡦࡴࠩब")][bstack1l1lllll_opy_])
      else:
        options.set_preference(bstack1l1lllll_opy_, bstack1l1ll1ll1l_opy_[bstack11l1ll_opy_ (u"ࠫࡵࡸࡥࡧࡵࠪभ")][bstack1l1lllll_opy_])
  if bstack11l1ll_opy_ (u"ࠬࡧࡲࡨࡵࠪम") in bstack1l1ll1ll1l_opy_:
    for arg in bstack1l1ll1ll1l_opy_[bstack11l1ll_opy_ (u"࠭ࡡࡳࡩࡶࠫय")]:
      options.add_argument(arg)
def bstack11l1ll1ll_opy_(options, bstack11lll11l_opy_):
  if bstack11l1ll_opy_ (u"ࠧࡸࡧࡥࡺ࡮࡫ࡷࠨर") in bstack11lll11l_opy_:
    options.use_webview(bool(bstack11lll11l_opy_[bstack11l1ll_opy_ (u"ࠨࡹࡨࡦࡻ࡯ࡥࡸࠩऱ")]))
  bstack1l1llll1_opy_(options, bstack11lll11l_opy_)
def bstack1l1lll1ll1_opy_(options, bstack1lll1ll111_opy_):
  for bstack11111l1ll_opy_ in bstack1lll1ll111_opy_:
    if bstack11111l1ll_opy_ in [bstack11l1ll_opy_ (u"ࠩࡷࡩࡨ࡮࡮ࡰ࡮ࡲ࡫ࡾࡖࡲࡦࡸ࡬ࡩࡼ࠭ल"), bstack11l1ll_opy_ (u"ࠪࡥࡷ࡭ࡳࠨळ")]:
      continue
    options.set_capability(bstack11111l1ll_opy_, bstack1lll1ll111_opy_[bstack11111l1ll_opy_])
  if bstack11l1ll_opy_ (u"ࠫࡦࡸࡧࡴࠩऴ") in bstack1lll1ll111_opy_:
    for arg in bstack1lll1ll111_opy_[bstack11l1ll_opy_ (u"ࠬࡧࡲࡨࡵࠪव")]:
      options.add_argument(arg)
  if bstack11l1ll_opy_ (u"࠭ࡴࡦࡥ࡫ࡲࡴࡲ࡯ࡨࡻࡓࡶࡪࡼࡩࡦࡹࠪश") in bstack1lll1ll111_opy_:
    options.bstack1l11l1111_opy_(bool(bstack1lll1ll111_opy_[bstack11l1ll_opy_ (u"ࠧࡵࡧࡦ࡬ࡳࡵ࡬ࡰࡩࡼࡔࡷ࡫ࡶࡪࡧࡺࠫष")]))
def bstack1l1ll11l1_opy_(options, bstack1ll111111_opy_):
  for bstack1llll1l11_opy_ in bstack1ll111111_opy_:
    if bstack1llll1l11_opy_ in [bstack11l1ll_opy_ (u"ࠨࡣࡧࡨ࡮ࡺࡩࡰࡰࡤࡰࡔࡶࡴࡪࡱࡱࡷࠬस"), bstack11l1ll_opy_ (u"ࠩࡤࡶ࡬ࡹࠧह")]:
      continue
    options._options[bstack1llll1l11_opy_] = bstack1ll111111_opy_[bstack1llll1l11_opy_]
  if bstack11l1ll_opy_ (u"ࠪࡥࡩࡪࡩࡵ࡫ࡲࡲࡦࡲࡏࡱࡶ࡬ࡳࡳࡹࠧऺ") in bstack1ll111111_opy_:
    for bstack1111l1ll1_opy_ in bstack1ll111111_opy_[bstack11l1ll_opy_ (u"ࠫࡦࡪࡤࡪࡶ࡬ࡳࡳࡧ࡬ࡐࡲࡷ࡭ࡴࡴࡳࠨऻ")]:
      options.bstack1l1ll11l1l_opy_(
        bstack1111l1ll1_opy_, bstack1ll111111_opy_[bstack11l1ll_opy_ (u"ࠬࡧࡤࡥ࡫ࡷ࡭ࡴࡴࡡ࡭ࡑࡳࡸ࡮ࡵ࡮ࡴ़ࠩ")][bstack1111l1ll1_opy_])
  if bstack11l1ll_opy_ (u"࠭ࡡࡳࡩࡶࠫऽ") in bstack1ll111111_opy_:
    for arg in bstack1ll111111_opy_[bstack11l1ll_opy_ (u"ࠧࡢࡴࡪࡷࠬा")]:
      options.add_argument(arg)
def bstack11ll1l11l_opy_(options, caps):
  if not hasattr(options, bstack11l1ll_opy_ (u"ࠨࡍࡈ࡝ࠬि")):
    return
  if options.KEY == bstack11l1ll_opy_ (u"ࠩࡪࡳࡴ࡭࠺ࡤࡪࡵࡳࡲ࡫ࡏࡱࡶ࡬ࡳࡳࡹࠧी") and options.KEY in caps:
    bstack1l1llll1_opy_(options, caps[bstack11l1ll_opy_ (u"ࠪ࡫ࡴࡵࡧ࠻ࡥ࡫ࡶࡴࡳࡥࡐࡲࡷ࡭ࡴࡴࡳࠨु")])
  elif options.KEY == bstack11l1ll_opy_ (u"ࠫࡲࡵࡺ࠻ࡨ࡬ࡶࡪ࡬࡯ࡹࡑࡳࡸ࡮ࡵ࡮ࡴࠩू") and options.KEY in caps:
    bstack1ll1l1l1_opy_(options, caps[bstack11l1ll_opy_ (u"ࠬࡳ࡯ࡻ࠼ࡩ࡭ࡷ࡫ࡦࡰࡺࡒࡴࡹ࡯࡯࡯ࡵࠪृ")])
  elif options.KEY == bstack11l1ll_opy_ (u"࠭ࡳࡢࡨࡤࡶ࡮࠴࡯ࡱࡶ࡬ࡳࡳࡹࠧॄ") and options.KEY in caps:
    bstack1l1lll1ll1_opy_(options, caps[bstack11l1ll_opy_ (u"ࠧࡴࡣࡩࡥࡷ࡯࠮ࡰࡲࡷ࡭ࡴࡴࡳࠨॅ")])
  elif options.KEY == bstack11l1ll_opy_ (u"ࠨ࡯ࡶ࠾ࡪࡪࡧࡦࡑࡳࡸ࡮ࡵ࡮ࡴࠩॆ") and options.KEY in caps:
    bstack11l1ll1ll_opy_(options, caps[bstack11l1ll_opy_ (u"ࠩࡰࡷ࠿࡫ࡤࡨࡧࡒࡴࡹ࡯࡯࡯ࡵࠪे")])
  elif options.KEY == bstack11l1ll_opy_ (u"ࠪࡷࡪࡀࡩࡦࡑࡳࡸ࡮ࡵ࡮ࡴࠩै") and options.KEY in caps:
    bstack1l1ll11l1_opy_(options, caps[bstack11l1ll_opy_ (u"ࠫࡸ࡫࠺ࡪࡧࡒࡴࡹ࡯࡯࡯ࡵࠪॉ")])
def bstack1lll11lll_opy_(caps):
  global bstack1ll11ll111_opy_
  if isinstance(os.environ.get(bstack11l1ll_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣࡎ࡙࡟ࡂࡒࡓࡣࡆ࡛ࡔࡐࡏࡄࡘࡊ࠭ॊ")), str):
    bstack1ll11ll111_opy_ = eval(os.getenv(bstack11l1ll_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤࡏࡓࡠࡃࡓࡔࡤࡇࡕࡕࡑࡐࡅ࡙ࡋࠧो")))
  if bstack1ll11ll111_opy_:
    if bstack1111ll11l_opy_() < version.parse(bstack11l1ll_opy_ (u"ࠧ࠳࠰࠶࠲࠵࠭ौ")):
      return None
    else:
      from appium.options.common.base import AppiumOptions
      options = AppiumOptions().load_capabilities(caps)
      return options
  else:
    browser = bstack11l1ll_opy_ (u"ࠨࡥ࡫ࡶࡴࡳࡥࠨ्")
    if bstack11l1ll_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡑࡥࡲ࡫ࠧॎ") in caps:
      browser = caps[bstack11l1ll_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡒࡦࡳࡥࠨॏ")]
    elif bstack11l1ll_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࠬॐ") in caps:
      browser = caps[bstack11l1ll_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷ࠭॑")]
    browser = str(browser).lower()
    if browser == bstack11l1ll_opy_ (u"࠭ࡩࡱࡪࡲࡲࡪ॒࠭") or browser == bstack11l1ll_opy_ (u"ࠧࡪࡲࡤࡨࠬ॓"):
      browser = bstack11l1ll_opy_ (u"ࠨࡵࡤࡪࡦࡸࡩࠨ॔")
    if browser == bstack11l1ll_opy_ (u"ࠩࡶࡥࡲࡹࡵ࡯ࡩࠪॕ"):
      browser = bstack11l1ll_opy_ (u"ࠪࡧ࡭ࡸ࡯࡮ࡧࠪॖ")
    if browser not in [bstack11l1ll_opy_ (u"ࠫࡨ࡮ࡲࡰ࡯ࡨࠫॗ"), bstack11l1ll_opy_ (u"ࠬ࡫ࡤࡨࡧࠪक़"), bstack11l1ll_opy_ (u"࠭ࡩࡦࠩख़"), bstack11l1ll_opy_ (u"ࠧࡴࡣࡩࡥࡷ࡯ࠧग़"), bstack11l1ll_opy_ (u"ࠨࡨ࡬ࡶࡪ࡬࡯ࡹࠩज़")]:
      return None
    try:
      package = bstack11l1ll_opy_ (u"ࠩࡶࡩࡱ࡫࡮ࡪࡷࡰ࠲ࡼ࡫ࡢࡥࡴ࡬ࡺࡪࡸ࠮ࡼࡿ࠱ࡳࡵࡺࡩࡰࡰࡶࠫड़").format(browser)
      name = bstack11l1ll_opy_ (u"ࠪࡓࡵࡺࡩࡰࡰࡶࠫढ़")
      browser_options = getattr(__import__(package, fromlist=[name]), name)
      options = browser_options()
      if not bstack1ll1l1llll_opy_(options):
        return None
      for bstack111llll1_opy_ in caps.keys():
        options.set_capability(bstack111llll1_opy_, caps[bstack111llll1_opy_])
      bstack11ll1l11l_opy_(options, caps)
      return options
    except Exception as e:
      logger.debug(str(e))
      return None
def bstack1l1ll1l11l_opy_(options, bstack111lllll1_opy_):
  if not bstack1ll1l1llll_opy_(options):
    return
  for bstack111llll1_opy_ in bstack111lllll1_opy_.keys():
    if bstack111llll1_opy_ in bstack1ll11l111_opy_:
      continue
    if bstack111llll1_opy_ in options._caps and type(options._caps[bstack111llll1_opy_]) in [dict, list]:
      options._caps[bstack111llll1_opy_] = update(options._caps[bstack111llll1_opy_], bstack111lllll1_opy_[bstack111llll1_opy_])
    else:
      options.set_capability(bstack111llll1_opy_, bstack111lllll1_opy_[bstack111llll1_opy_])
  bstack11ll1l11l_opy_(options, bstack111lllll1_opy_)
  if bstack11l1ll_opy_ (u"ࠫࡲࡵࡺ࠻ࡦࡨࡦࡺ࡭ࡧࡦࡴࡄࡨࡩࡸࡥࡴࡵࠪफ़") in options._caps:
    if options._caps[bstack11l1ll_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡔࡡ࡮ࡧࠪय़")] and options._caps[bstack11l1ll_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡎࡢ࡯ࡨࠫॠ")].lower() != bstack11l1ll_opy_ (u"ࠧࡧ࡫ࡵࡩ࡫ࡵࡸࠨॡ"):
      del options._caps[bstack11l1ll_opy_ (u"ࠨ࡯ࡲࡾ࠿ࡪࡥࡣࡷࡪ࡫ࡪࡸࡁࡥࡦࡵࡩࡸࡹࠧॢ")]
def bstack1l1ll1l1ll_opy_(proxy_config):
  if bstack11l1ll_opy_ (u"ࠩ࡫ࡸࡹࡶࡳࡑࡴࡲࡼࡾ࠭ॣ") in proxy_config:
    proxy_config[bstack11l1ll_opy_ (u"ࠪࡷࡸࡲࡐࡳࡱࡻࡽࠬ।")] = proxy_config[bstack11l1ll_opy_ (u"ࠫ࡭ࡺࡴࡱࡵࡓࡶࡴࡾࡹࠨ॥")]
    del (proxy_config[bstack11l1ll_opy_ (u"ࠬ࡮ࡴࡵࡲࡶࡔࡷࡵࡸࡺࠩ०")])
  if bstack11l1ll_opy_ (u"࠭ࡰࡳࡱࡻࡽ࡙ࡿࡰࡦࠩ१") in proxy_config and proxy_config[bstack11l1ll_opy_ (u"ࠧࡱࡴࡲࡼࡾ࡚ࡹࡱࡧࠪ२")].lower() != bstack11l1ll_opy_ (u"ࠨࡦ࡬ࡶࡪࡩࡴࠨ३"):
    proxy_config[bstack11l1ll_opy_ (u"ࠩࡳࡶࡴࡾࡹࡕࡻࡳࡩࠬ४")] = bstack11l1ll_opy_ (u"ࠪࡱࡦࡴࡵࡢ࡮ࠪ५")
  if bstack11l1ll_opy_ (u"ࠫࡵࡸ࡯ࡹࡻࡄࡹࡹࡵࡣࡰࡰࡩ࡭࡬࡛ࡲ࡭ࠩ६") in proxy_config:
    proxy_config[bstack11l1ll_opy_ (u"ࠬࡶࡲࡰࡺࡼࡘࡾࡶࡥࠨ७")] = bstack11l1ll_opy_ (u"࠭ࡰࡢࡥࠪ८")
  return proxy_config
def bstack1l1ll11lll_opy_(config, proxy):
  from selenium.webdriver.common.proxy import Proxy
  if not bstack11l1ll_opy_ (u"ࠧࡱࡴࡲࡼࡾ࠭९") in config:
    return proxy
  config[bstack11l1ll_opy_ (u"ࠨࡲࡵࡳࡽࡿࠧ॰")] = bstack1l1ll1l1ll_opy_(config[bstack11l1ll_opy_ (u"ࠩࡳࡶࡴࡾࡹࠨॱ")])
  if proxy == None:
    proxy = Proxy(config[bstack11l1ll_opy_ (u"ࠪࡴࡷࡵࡸࡺࠩॲ")])
  return proxy
def bstack1ll1llll11_opy_(self):
  global CONFIG
  global bstack1llll1111l_opy_
  try:
    proxy = bstack1l111lll1_opy_(CONFIG)
    if proxy:
      if proxy.endswith(bstack11l1ll_opy_ (u"ࠫ࠳ࡶࡡࡤࠩॳ")):
        proxies = bstack111l1ll11_opy_(proxy, bstack1ll1lll1_opy_())
        if len(proxies) > 0:
          protocol, bstack1ll11ll1_opy_ = proxies.popitem()
          if bstack11l1ll_opy_ (u"ࠧࡀ࠯࠰ࠤॴ") in bstack1ll11ll1_opy_:
            return bstack1ll11ll1_opy_
          else:
            return bstack11l1ll_opy_ (u"ࠨࡨࡵࡶࡳ࠾࠴࠵ࠢॵ") + bstack1ll11ll1_opy_
      else:
        return proxy
  except Exception as e:
    logger.error(bstack11l1ll_opy_ (u"ࠢࡆࡴࡵࡳࡷࠦࡩ࡯ࠢࡶࡩࡹࡺࡩ࡯ࡩࠣࡴࡷࡵࡸࡺࠢࡸࡶࡱࠦ࠺ࠡࡽࢀࠦॶ").format(str(e)))
  return bstack1llll1111l_opy_(self)
def bstack111111lll_opy_():
  global CONFIG
  return bstack11111llll_opy_(CONFIG) and bstack1l1l11lll_opy_() and bstack1lll1ll1l_opy_() >= version.parse(bstack11l1lll11_opy_)
def bstack1lllll11_opy_():
  global CONFIG
  return (bstack11l1ll_opy_ (u"ࠨࡪࡷࡸࡵࡖࡲࡰࡺࡼࠫॷ") in CONFIG or bstack11l1ll_opy_ (u"ࠩ࡫ࡸࡹࡶࡳࡑࡴࡲࡼࡾ࠭ॸ") in CONFIG) and bstack1ll11l1l1_opy_()
def bstack1lllll1111_opy_(config):
  bstack1ll1111lll_opy_ = {}
  if bstack11l1ll_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡗࡹࡧࡣ࡬ࡎࡲࡧࡦࡲࡏࡱࡶ࡬ࡳࡳࡹࠧॹ") in config:
    bstack1ll1111lll_opy_ = config[bstack11l1ll_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡘࡺࡡࡤ࡭ࡏࡳࡨࡧ࡬ࡐࡲࡷ࡭ࡴࡴࡳࠨॺ")]
  if bstack11l1ll_opy_ (u"ࠬࡲ࡯ࡤࡣ࡯ࡓࡵࡺࡩࡰࡰࡶࠫॻ") in config:
    bstack1ll1111lll_opy_ = config[bstack11l1ll_opy_ (u"࠭࡬ࡰࡥࡤࡰࡔࡶࡴࡪࡱࡱࡷࠬॼ")]
  proxy = bstack1l111lll1_opy_(config)
  if proxy:
    if proxy.endswith(bstack11l1ll_opy_ (u"ࠧ࠯ࡲࡤࡧࠬॽ")) and os.path.isfile(proxy):
      bstack1ll1111lll_opy_[bstack11l1ll_opy_ (u"ࠨ࠯ࡳࡥࡨ࠳ࡦࡪ࡮ࡨࠫॾ")] = proxy
    else:
      parsed_url = None
      if proxy.endswith(bstack11l1ll_opy_ (u"ࠩ࠱ࡴࡦࡩࠧॿ")):
        proxies = bstack1lll111111_opy_(config, bstack1ll1lll1_opy_())
        if len(proxies) > 0:
          protocol, bstack1ll11ll1_opy_ = proxies.popitem()
          if bstack11l1ll_opy_ (u"ࠥ࠾࠴࠵ࠢঀ") in bstack1ll11ll1_opy_:
            parsed_url = urlparse(bstack1ll11ll1_opy_)
          else:
            parsed_url = urlparse(protocol + bstack11l1ll_opy_ (u"ࠦ࠿࠵࠯ࠣঁ") + bstack1ll11ll1_opy_)
      else:
        parsed_url = urlparse(proxy)
      if parsed_url and parsed_url.hostname: bstack1ll1111lll_opy_[bstack11l1ll_opy_ (u"ࠬࡶࡲࡰࡺࡼࡌࡴࡹࡴࠨং")] = str(parsed_url.hostname)
      if parsed_url and parsed_url.port: bstack1ll1111lll_opy_[bstack11l1ll_opy_ (u"࠭ࡰࡳࡱࡻࡽࡕࡵࡲࡵࠩঃ")] = str(parsed_url.port)
      if parsed_url and parsed_url.username: bstack1ll1111lll_opy_[bstack11l1ll_opy_ (u"ࠧࡱࡴࡲࡼࡾ࡛ࡳࡦࡴࠪ঄")] = str(parsed_url.username)
      if parsed_url and parsed_url.password: bstack1ll1111lll_opy_[bstack11l1ll_opy_ (u"ࠨࡲࡵࡳࡽࡿࡐࡢࡵࡶࠫঅ")] = str(parsed_url.password)
  return bstack1ll1111lll_opy_
def bstack1l11l1ll1_opy_(config):
  if bstack11l1ll_opy_ (u"ࠩࡷࡩࡸࡺࡃࡰࡰࡷࡩࡽࡺࡏࡱࡶ࡬ࡳࡳࡹࠧআ") in config:
    return config[bstack11l1ll_opy_ (u"ࠪࡸࡪࡹࡴࡄࡱࡱࡸࡪࡾࡴࡐࡲࡷ࡭ࡴࡴࡳࠨই")]
  return {}
def bstack1ll1111111_opy_(caps):
  global bstack1l1111ll_opy_
  if bstack11l1ll_opy_ (u"ࠫࡧࡹࡴࡢࡥ࡮࠾ࡴࡶࡴࡪࡱࡱࡷࠬঈ") in caps:
    caps[bstack11l1ll_opy_ (u"ࠬࡨࡳࡵࡣࡦ࡯࠿ࡵࡰࡵ࡫ࡲࡲࡸ࠭উ")][bstack11l1ll_opy_ (u"࠭࡬ࡰࡥࡤࡰࠬঊ")] = True
    if bstack1l1111ll_opy_:
      caps[bstack11l1ll_opy_ (u"ࠧࡣࡵࡷࡥࡨࡱ࠺ࡰࡲࡷ࡭ࡴࡴࡳࠨঋ")][bstack11l1ll_opy_ (u"ࠨ࡮ࡲࡧࡦࡲࡉࡥࡧࡱࡸ࡮࡬ࡩࡦࡴࠪঌ")] = bstack1l1111ll_opy_
  else:
    caps[bstack11l1ll_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫࠯࡮ࡲࡧࡦࡲࠧ঍")] = True
    if bstack1l1111ll_opy_:
      caps[bstack11l1ll_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬࠰࡯ࡳࡨࡧ࡬ࡊࡦࡨࡲࡹ࡯ࡦࡪࡧࡵࠫ঎")] = bstack1l1111ll_opy_
def bstack1lllll11ll_opy_():
  global CONFIG
  if bstack11l1ll_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࡏࡳࡨࡧ࡬ࠨএ") in CONFIG and bstack111l1l1l1_opy_(CONFIG[bstack11l1ll_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࡐࡴࡩࡡ࡭ࠩঐ")]):
    bstack1ll1111lll_opy_ = bstack1lllll1111_opy_(CONFIG)
    bstack11l111ll_opy_(CONFIG[bstack11l1ll_opy_ (u"࠭ࡡࡤࡥࡨࡷࡸࡑࡥࡺࠩ঑")], bstack1ll1111lll_opy_)
def bstack11l111ll_opy_(key, bstack1ll1111lll_opy_):
  global bstack1lll1ll1_opy_
  logger.info(bstack1l1l1111l_opy_)
  try:
    bstack1lll1ll1_opy_ = Local()
    bstack1lll1l11l_opy_ = {bstack11l1ll_opy_ (u"ࠧ࡬ࡧࡼࠫ঒"): key}
    bstack1lll1l11l_opy_.update(bstack1ll1111lll_opy_)
    logger.debug(bstack1l1ll1llll_opy_.format(str(bstack1lll1l11l_opy_)))
    bstack1lll1ll1_opy_.start(**bstack1lll1l11l_opy_)
    if bstack1lll1ll1_opy_.isRunning():
      logger.info(bstack1lll1lll1l_opy_)
  except Exception as e:
    bstack1ll1111l1_opy_(bstack111ll1lll_opy_.format(str(e)))
def bstack11111ll11_opy_():
  global bstack1lll1ll1_opy_
  if bstack1lll1ll1_opy_.isRunning():
    logger.info(bstack1ll111l1l1_opy_)
    bstack1lll1ll1_opy_.stop()
  bstack1lll1ll1_opy_ = None
def bstack1ll1lllll1_opy_(bstack1lllll1l11_opy_=[]):
  global CONFIG
  bstack1l1l1llll_opy_ = []
  bstack1111l1ll_opy_ = [bstack11l1ll_opy_ (u"ࠨࡱࡶࠫও"), bstack11l1ll_opy_ (u"ࠩࡲࡷ࡛࡫ࡲࡴ࡫ࡲࡲࠬঔ"), bstack11l1ll_opy_ (u"ࠪࡨࡪࡼࡩࡤࡧࡑࡥࡲ࡫ࠧক"), bstack11l1ll_opy_ (u"ࠫࡵࡲࡡࡵࡨࡲࡶࡲ࡜ࡥࡳࡵ࡬ࡳࡳ࠭খ"), bstack11l1ll_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡔࡡ࡮ࡧࠪগ"), bstack11l1ll_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡖࡦࡴࡶ࡭ࡴࡴࠧঘ")]
  try:
    for err in bstack1lllll1l11_opy_:
      bstack1lll1l11_opy_ = {}
      for k in bstack1111l1ll_opy_:
        val = CONFIG[bstack11l1ll_opy_ (u"ࠧࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࡵࠪঙ")][int(err[bstack11l1ll_opy_ (u"ࠨ࡫ࡱࡨࡪࡾࠧচ")])].get(k)
        if val:
          bstack1lll1l11_opy_[k] = val
      bstack1lll1l11_opy_[bstack11l1ll_opy_ (u"ࠩࡷࡩࡸࡺࡳࠨছ")] = {
        err[bstack11l1ll_opy_ (u"ࠪࡲࡦࡳࡥࠨজ")]: err[bstack11l1ll_opy_ (u"ࠫࡪࡸࡲࡰࡴࠪঝ")]
      }
      bstack1l1l1llll_opy_.append(bstack1lll1l11_opy_)
  except Exception as e:
    logger.debug(bstack11l1ll_opy_ (u"ࠬࡋࡲࡳࡱࡵࠤ࡮ࡴࠠࡧࡱࡵࡱࡦࡺࡴࡪࡰࡪࠤࡩࡧࡴࡢࠢࡩࡳࡷࠦࡥࡷࡧࡱࡸ࠿ࠦࠧঞ") + str(e))
  finally:
    return bstack1l1l1llll_opy_
def bstack1ll1l11111_opy_(file_name):
  bstack1llll111l_opy_ = []
  try:
    bstack11ll1111_opy_ = os.path.join(tempfile.gettempdir(), file_name)
    if os.path.exists(bstack11ll1111_opy_):
      with open(bstack11ll1111_opy_) as f:
        bstack11l11l11l_opy_ = json.load(f)
        bstack1llll111l_opy_ = bstack11l11l11l_opy_
      os.remove(bstack11ll1111_opy_)
    return bstack1llll111l_opy_
  except Exception as e:
    logger.debug(bstack11l1ll_opy_ (u"࠭ࡅࡳࡴࡲࡶࠥ࡯࡮ࠡࡨ࡬ࡲࡩ࡯࡮ࡨࠢࡨࡶࡷࡵࡲࠡ࡮࡬ࡷࡹࡀࠠࠨট") + str(e))
def bstack1lllll111l_opy_():
  global bstack1ll11l11l_opy_
  global bstack11l1l1111_opy_
  global bstack1lllll11l1_opy_
  global bstack11l111l11_opy_
  global bstack11ll1lll_opy_
  global bstack11ll111ll_opy_
  percy.shutdown()
  bstack1ll1llll_opy_ = os.environ.get(bstack11l1ll_opy_ (u"ࠧࡇࡔࡄࡑࡊ࡝ࡏࡓࡍࡢ࡙ࡘࡋࡄࠨঠ"))
  if bstack1ll1llll_opy_ in [bstack11l1ll_opy_ (u"ࠨࡴࡲࡦࡴࡺࠧড"), bstack11l1ll_opy_ (u"ࠩࡳࡥࡧࡵࡴࠨঢ")]:
    bstack11111ll1_opy_()
  if bstack1ll11l11l_opy_:
    logger.warning(bstack1lllll111_opy_.format(str(bstack1ll11l11l_opy_)))
  else:
    try:
      bstack1ll1111ll1_opy_ = bstack1lll1l1l1l_opy_(bstack11l1ll_opy_ (u"ࠪ࠲ࡧࡹࡴࡢࡥ࡮࠱ࡨࡵ࡮ࡧ࡫ࡪ࠲࡯ࡹ࡯࡯ࠩণ"), logger)
      if bstack1ll1111ll1_opy_.get(bstack11l1ll_opy_ (u"ࠫࡳࡻࡤࡨࡧࡢࡰࡴࡩࡡ࡭ࠩত")) and bstack1ll1111ll1_opy_.get(bstack11l1ll_opy_ (u"ࠬࡴࡵࡥࡩࡨࡣࡱࡵࡣࡢ࡮ࠪথ")).get(bstack11l1ll_opy_ (u"࠭ࡨࡰࡵࡷࡲࡦࡳࡥࠨদ")):
        logger.warning(bstack1lllll111_opy_.format(str(bstack1ll1111ll1_opy_[bstack11l1ll_opy_ (u"ࠧ࡯ࡷࡧ࡫ࡪࡥ࡬ࡰࡥࡤࡰࠬধ")][bstack11l1ll_opy_ (u"ࠨࡪࡲࡷࡹࡴࡡ࡮ࡧࠪন")])))
    except Exception as e:
      logger.error(e)
  logger.info(bstack111ll1l1l_opy_)
  global bstack1lll1ll1_opy_
  if bstack1lll1ll1_opy_:
    bstack11111ll11_opy_()
  try:
    for driver in bstack11l1l1111_opy_:
      driver.quit()
  except Exception as e:
    pass
  logger.info(bstack1ll1l111l_opy_)
  if bstack11ll111ll_opy_ == bstack11l1ll_opy_ (u"ࠩࡵࡳࡧࡵࡴࠨ঩"):
    bstack11ll1lll_opy_ = bstack1ll1l11111_opy_(bstack11l1ll_opy_ (u"ࠪࡶࡴࡨ࡯ࡵࡡࡨࡶࡷࡵࡲࡠ࡮࡬ࡷࡹ࠴ࡪࡴࡱࡱࠫপ"))
  if bstack11ll111ll_opy_ == bstack11l1ll_opy_ (u"ࠫࡵࡿࡴࡦࡵࡷࠫফ") and len(bstack11l111l11_opy_) == 0:
    bstack11l111l11_opy_ = bstack1ll1l11111_opy_(bstack11l1ll_opy_ (u"ࠬࡶࡷࡠࡲࡼࡸࡪࡹࡴࡠࡧࡵࡶࡴࡸ࡟࡭࡫ࡶࡸ࠳ࡰࡳࡰࡰࠪব"))
    if len(bstack11l111l11_opy_) == 0:
      bstack11l111l11_opy_ = bstack1ll1l11111_opy_(bstack11l1ll_opy_ (u"࠭ࡰࡺࡶࡨࡷࡹࡥࡰࡱࡲࡢࡩࡷࡸ࡯ࡳࡡ࡯࡭ࡸࡺ࠮࡫ࡵࡲࡲࠬভ"))
  bstack111ll1l11_opy_ = bstack11l1ll_opy_ (u"ࠧࠨম")
  if len(bstack1lllll11l1_opy_) > 0:
    bstack111ll1l11_opy_ = bstack1ll1lllll1_opy_(bstack1lllll11l1_opy_)
  elif len(bstack11l111l11_opy_) > 0:
    bstack111ll1l11_opy_ = bstack1ll1lllll1_opy_(bstack11l111l11_opy_)
  elif len(bstack11ll1lll_opy_) > 0:
    bstack111ll1l11_opy_ = bstack1ll1lllll1_opy_(bstack11ll1lll_opy_)
  elif len(bstack1l1ll1lll_opy_) > 0:
    bstack111ll1l11_opy_ = bstack1ll1lllll1_opy_(bstack1l1ll1lll_opy_)
  if bool(bstack111ll1l11_opy_):
    bstack1lll11l1l_opy_(bstack111ll1l11_opy_)
  else:
    bstack1lll11l1l_opy_()
  bstack1l1llll11_opy_(bstack111ll1111_opy_, logger)
def bstack1l1ll1ll11_opy_(self, *args):
  logger.error(bstack111111l11_opy_)
  bstack1lllll111l_opy_()
  sys.exit(1)
def bstack1ll1111l1_opy_(err):
  logger.critical(bstack1l1l1l1l_opy_.format(str(err)))
  bstack1lll11l1l_opy_(bstack1l1l1l1l_opy_.format(str(err)))
  atexit.unregister(bstack1lllll111l_opy_)
  bstack11111ll1_opy_()
  sys.exit(1)
def bstack1l11lll1_opy_(error, message):
  logger.critical(str(error))
  logger.critical(message)
  bstack1lll11l1l_opy_(message)
  atexit.unregister(bstack1lllll111l_opy_)
  bstack11111ll1_opy_()
  sys.exit(1)
def bstack1llll1ll1l_opy_():
  global CONFIG
  global bstack11l11ll1l_opy_
  global bstack11l1l11l1_opy_
  global bstack1l1lll1lll_opy_
  CONFIG = bstack1ll1l1l11l_opy_()
  bstack1llll1ll1_opy_()
  bstack1l111111_opy_()
  CONFIG = bstack1l1lll1111_opy_(CONFIG)
  update(CONFIG, bstack11l1l11l1_opy_)
  update(CONFIG, bstack11l11ll1l_opy_)
  CONFIG = bstack1l1llllll1_opy_(CONFIG)
  bstack1l1lll1lll_opy_ = bstack1ll111ll1_opy_(CONFIG)
  bstack1ll1l11l1_opy_.bstack1l1ll1ll1_opy_(bstack11l1ll_opy_ (u"ࠨࡤࡶࡸࡦࡩ࡫ࡠࡵࡨࡷࡸ࡯࡯࡯ࠩয"), bstack1l1lll1lll_opy_)
  if (bstack11l1ll_opy_ (u"ࠩࡥࡹ࡮ࡲࡤࡏࡣࡰࡩࠬর") in CONFIG and bstack11l1ll_opy_ (u"ࠪࡦࡺ࡯࡬ࡥࡐࡤࡱࡪ࠭঱") in bstack11l11ll1l_opy_) or (
          bstack11l1ll_opy_ (u"ࠫࡧࡻࡩ࡭ࡦࡑࡥࡲ࡫ࠧল") in CONFIG and bstack11l1ll_opy_ (u"ࠬࡨࡵࡪ࡮ࡧࡒࡦࡳࡥࠨ঳") not in bstack11l1l11l1_opy_):
    if os.getenv(bstack11l1ll_opy_ (u"࠭ࡂࡔࡖࡄࡇࡐࡥࡃࡐࡏࡅࡍࡓࡋࡄࡠࡄࡘࡍࡑࡊ࡟ࡊࡆࠪ঴")):
      CONFIG[bstack11l1ll_opy_ (u"ࠧࡣࡷ࡬ࡰࡩࡏࡤࡦࡰࡷ࡭࡫࡯ࡥࡳࠩ঵")] = os.getenv(bstack11l1ll_opy_ (u"ࠨࡄࡖࡘࡆࡉࡋࡠࡅࡒࡑࡇࡏࡎࡆࡆࡢࡆ࡚ࡏࡌࡅࡡࡌࡈࠬশ"))
    else:
      bstack1ll111lll1_opy_()
  elif (bstack11l1ll_opy_ (u"ࠩࡥࡹ࡮ࡲࡤࡏࡣࡰࡩࠬষ") not in CONFIG and bstack11l1ll_opy_ (u"ࠪࡦࡺ࡯࡬ࡥࡋࡧࡩࡳࡺࡩࡧ࡫ࡨࡶࠬস") in CONFIG) or (
          bstack11l1ll_opy_ (u"ࠫࡧࡻࡩ࡭ࡦࡑࡥࡲ࡫ࠧহ") in bstack11l1l11l1_opy_ and bstack11l1ll_opy_ (u"ࠬࡨࡵࡪ࡮ࡧࡒࡦࡳࡥࠨ঺") not in bstack11l11ll1l_opy_):
    del (CONFIG[bstack11l1ll_opy_ (u"࠭ࡢࡶ࡫࡯ࡨࡎࡪࡥ࡯ࡶ࡬ࡪ࡮࡫ࡲࠨ঻")])
  if bstack1l111ll1_opy_(CONFIG):
    bstack1ll1111l1_opy_(bstack1llllll11l_opy_)
  bstack1l111ll11_opy_()
  bstack111lll1l1_opy_()
  if bstack1ll11ll111_opy_:
    CONFIG[bstack11l1ll_opy_ (u"ࠧࡢࡲࡳ়ࠫ")] = bstack1l1l11l11_opy_(CONFIG)
    logger.info(bstack1lll1l1ll_opy_.format(CONFIG[bstack11l1ll_opy_ (u"ࠨࡣࡳࡴࠬঽ")]))
def bstack1lllll1l1_opy_(config, bstack1ll1l11l1l_opy_):
  global CONFIG
  global bstack1ll11ll111_opy_
  CONFIG = config
  bstack1ll11ll111_opy_ = bstack1ll1l11l1l_opy_
def bstack111lll1l1_opy_():
  global CONFIG
  global bstack1ll11ll111_opy_
  if bstack11l1ll_opy_ (u"ࠩࡤࡴࡵ࠭া") in CONFIG:
    try:
      from appium import version
    except Exception as e:
      bstack1l11lll1_opy_(e, bstack11l1ll1l_opy_)
    bstack1ll11ll111_opy_ = True
    bstack1ll1l11l1_opy_.bstack1l1ll1ll1_opy_(bstack11l1ll_opy_ (u"ࠪࡥࡵࡶ࡟ࡢࡷࡷࡳࡲࡧࡴࡦࠩি"), True)
def bstack1l1l11l11_opy_(config):
  bstack1ll1l1111_opy_ = bstack11l1ll_opy_ (u"ࠫࠬী")
  app = config[bstack11l1ll_opy_ (u"ࠬࡧࡰࡱࠩু")]
  if isinstance(app, str):
    if os.path.splitext(app)[1] in bstack1111111ll_opy_:
      if os.path.exists(app):
        bstack1ll1l1111_opy_ = bstack1lll111l1l_opy_(config, app)
      elif bstack11lll1l1l_opy_(app):
        bstack1ll1l1111_opy_ = app
      else:
        bstack1ll1111l1_opy_(bstack1llllllll_opy_.format(app))
    else:
      if bstack11lll1l1l_opy_(app):
        bstack1ll1l1111_opy_ = app
      elif os.path.exists(app):
        bstack1ll1l1111_opy_ = bstack1lll111l1l_opy_(app)
      else:
        bstack1ll1111l1_opy_(bstack1l1llll11l_opy_)
  else:
    if len(app) > 2:
      bstack1ll1111l1_opy_(bstack1ll1ll1111_opy_)
    elif len(app) == 2:
      if bstack11l1ll_opy_ (u"࠭ࡰࡢࡶ࡫ࠫূ") in app and bstack11l1ll_opy_ (u"ࠧࡤࡷࡶࡸࡴࡳ࡟ࡪࡦࠪৃ") in app:
        if os.path.exists(app[bstack11l1ll_opy_ (u"ࠨࡲࡤࡸ࡭࠭ৄ")]):
          bstack1ll1l1111_opy_ = bstack1lll111l1l_opy_(config, app[bstack11l1ll_opy_ (u"ࠩࡳࡥࡹ࡮ࠧ৅")], app[bstack11l1ll_opy_ (u"ࠪࡧࡺࡹࡴࡰ࡯ࡢ࡭ࡩ࠭৆")])
        else:
          bstack1ll1111l1_opy_(bstack1llllllll_opy_.format(app))
      else:
        bstack1ll1111l1_opy_(bstack1ll1ll1111_opy_)
    else:
      for key in app:
        if key in bstack11111l1l_opy_:
          if key == bstack11l1ll_opy_ (u"ࠫࡵࡧࡴࡩࠩে"):
            if os.path.exists(app[key]):
              bstack1ll1l1111_opy_ = bstack1lll111l1l_opy_(config, app[key])
            else:
              bstack1ll1111l1_opy_(bstack1llllllll_opy_.format(app))
          else:
            bstack1ll1l1111_opy_ = app[key]
        else:
          bstack1ll1111l1_opy_(bstack1ll11l1l_opy_)
  return bstack1ll1l1111_opy_
def bstack11lll1l1l_opy_(bstack1ll1l1111_opy_):
  import re
  bstack111ll11l1_opy_ = re.compile(bstack11l1ll_opy_ (u"ࡷࠨ࡞࡜ࡣ࠰ࡾࡆ࠳࡚࠱࠯࠼ࡠࡤ࠴࡜࠮࡟࠭ࠨࠧৈ"))
  bstack1lll111ll1_opy_ = re.compile(bstack11l1ll_opy_ (u"ࡸࠢ࡟࡝ࡤ࠱ࡿࡇ࡛࠭࠲࠰࠽ࡡࡥ࠮࡝࠯ࡠ࠮࠴ࡡࡡ࠮ࡼࡄ࠱࡟࠶࠭࠺࡞ࡢ࠲ࡡ࠳࡝ࠫࠦࠥ৉"))
  if bstack11l1ll_opy_ (u"ࠧࡣࡵ࠽࠳࠴࠭৊") in bstack1ll1l1111_opy_ or re.fullmatch(bstack111ll11l1_opy_, bstack1ll1l1111_opy_) or re.fullmatch(bstack1lll111ll1_opy_, bstack1ll1l1111_opy_):
    return True
  else:
    return False
def bstack1lll111l1l_opy_(config, path, bstack1llll111ll_opy_=None):
  import requests
  from requests_toolbelt.multipart.encoder import MultipartEncoder
  import hashlib
  md5_hash = hashlib.md5(open(os.path.abspath(path), bstack11l1ll_opy_ (u"ࠨࡴࡥࠫো")).read()).hexdigest()
  bstack1l1ll1l1l_opy_ = bstack11ll11l1l_opy_(md5_hash)
  bstack1ll1l1111_opy_ = None
  if bstack1l1ll1l1l_opy_:
    logger.info(bstack111ll1ll1_opy_.format(bstack1l1ll1l1l_opy_, md5_hash))
    return bstack1l1ll1l1l_opy_
  bstack1ll1lll11l_opy_ = MultipartEncoder(
    fields={
      bstack11l1ll_opy_ (u"ࠩࡩ࡭ࡱ࡫ࠧৌ"): (os.path.basename(path), open(os.path.abspath(path), bstack11l1ll_opy_ (u"ࠪࡶࡧ্࠭")), bstack11l1ll_opy_ (u"ࠫࡹ࡫ࡸࡵ࠱ࡳࡰࡦ࡯࡮ࠨৎ")),
      bstack11l1ll_opy_ (u"ࠬࡩࡵࡴࡶࡲࡱࡤ࡯ࡤࠨ৏"): bstack1llll111ll_opy_
    }
  )
  response = requests.post(bstack1lll1llll1_opy_, data=bstack1ll1lll11l_opy_,
                           headers={bstack11l1ll_opy_ (u"࠭ࡃࡰࡰࡷࡩࡳࡺ࠭ࡕࡻࡳࡩࠬ৐"): bstack1ll1lll11l_opy_.content_type},
                           auth=(config[bstack11l1ll_opy_ (u"ࠧࡶࡵࡨࡶࡓࡧ࡭ࡦࠩ৑")], config[bstack11l1ll_opy_ (u"ࠨࡣࡦࡧࡪࡹࡳࡌࡧࡼࠫ৒")]))
  try:
    res = json.loads(response.text)
    bstack1ll1l1111_opy_ = res[bstack11l1ll_opy_ (u"ࠩࡤࡴࡵࡥࡵࡳ࡮ࠪ৓")]
    logger.info(bstack1lll1lllll_opy_.format(bstack1ll1l1111_opy_))
    bstack11lll1lll_opy_(md5_hash, bstack1ll1l1111_opy_)
  except ValueError as err:
    bstack1ll1111l1_opy_(bstack1ll1ll111_opy_.format(str(err)))
  return bstack1ll1l1111_opy_
def bstack1l111ll11_opy_():
  global CONFIG
  global bstack1ll1llllll_opy_
  bstack11l11llll_opy_ = 0
  bstack1llll11l_opy_ = 1
  if bstack11l1ll_opy_ (u"ࠪࡴࡦࡸࡡ࡭࡮ࡨࡰࡸࡖࡥࡳࡒ࡯ࡥࡹ࡬࡯ࡳ࡯ࠪ৔") in CONFIG:
    bstack1llll11l_opy_ = CONFIG[bstack11l1ll_opy_ (u"ࠫࡵࡧࡲࡢ࡮࡯ࡩࡱࡹࡐࡦࡴࡓࡰࡦࡺࡦࡰࡴࡰࠫ৕")]
  if bstack11l1ll_opy_ (u"ࠬࡶ࡬ࡢࡶࡩࡳࡷࡳࡳࠨ৖") in CONFIG:
    bstack11l11llll_opy_ = len(CONFIG[bstack11l1ll_opy_ (u"࠭ࡰ࡭ࡣࡷࡪࡴࡸ࡭ࡴࠩৗ")])
  bstack1ll1llllll_opy_ = int(bstack1llll11l_opy_) * int(bstack11l11llll_opy_)
def bstack11ll11l1l_opy_(md5_hash):
  bstack1ll11lll1l_opy_ = os.path.join(os.path.expanduser(bstack11l1ll_opy_ (u"ࠧࡿࠩ৘")), bstack11l1ll_opy_ (u"ࠨ࠰ࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࠨ৙"), bstack11l1ll_opy_ (u"ࠩࡤࡴࡵ࡛ࡰ࡭ࡱࡤࡨࡒࡊ࠵ࡉࡣࡶ࡬࠳ࡰࡳࡰࡰࠪ৚"))
  if os.path.exists(bstack1ll11lll1l_opy_):
    bstack11lllllll_opy_ = json.load(open(bstack1ll11lll1l_opy_, bstack11l1ll_opy_ (u"ࠪࡶࡧ࠭৛")))
    if md5_hash in bstack11lllllll_opy_:
      bstack111lll1l_opy_ = bstack11lllllll_opy_[md5_hash]
      bstack11lll111_opy_ = datetime.datetime.now()
      bstack1111lll1l_opy_ = datetime.datetime.strptime(bstack111lll1l_opy_[bstack11l1ll_opy_ (u"ࠫࡹ࡯࡭ࡦࡵࡷࡥࡲࡶࠧড়")], bstack11l1ll_opy_ (u"ࠬࠫࡤ࠰ࠧࡰ࠳ࠪ࡟ࠠࠦࡊ࠽ࠩࡒࡀࠥࡔࠩঢ়"))
      if (bstack11lll111_opy_ - bstack1111lll1l_opy_).days > 30:
        return None
      elif version.parse(str(__version__)) > version.parse(bstack111lll1l_opy_[bstack11l1ll_opy_ (u"࠭ࡳࡥ࡭ࡢࡺࡪࡸࡳࡪࡱࡱࠫ৞")]):
        return None
      return bstack111lll1l_opy_[bstack11l1ll_opy_ (u"ࠧࡪࡦࠪয়")]
  else:
    return None
def bstack11lll1lll_opy_(md5_hash, bstack1ll1l1111_opy_):
  bstack1llll1l111_opy_ = os.path.join(os.path.expanduser(bstack11l1ll_opy_ (u"ࠨࢀࠪৠ")), bstack11l1ll_opy_ (u"ࠩ࠱ࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࠩৡ"))
  if not os.path.exists(bstack1llll1l111_opy_):
    os.makedirs(bstack1llll1l111_opy_)
  bstack1ll11lll1l_opy_ = os.path.join(os.path.expanduser(bstack11l1ll_opy_ (u"ࠪࢂࠬৢ")), bstack11l1ll_opy_ (u"ࠫ࠳ࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࠫৣ"), bstack11l1ll_opy_ (u"ࠬࡧࡰࡱࡗࡳࡰࡴࡧࡤࡎࡆ࠸ࡌࡦࡹࡨ࠯࡬ࡶࡳࡳ࠭৤"))
  bstack1111l111l_opy_ = {
    bstack11l1ll_opy_ (u"࠭ࡩࡥࠩ৥"): bstack1ll1l1111_opy_,
    bstack11l1ll_opy_ (u"ࠧࡵ࡫ࡰࡩࡸࡺࡡ࡮ࡲࠪ০"): datetime.datetime.strftime(datetime.datetime.now(), bstack11l1ll_opy_ (u"ࠨࠧࡧ࠳ࠪࡳ࠯࡛ࠦࠣࠩࡍࡀࠥࡎ࠼ࠨࡗࠬ১")),
    bstack11l1ll_opy_ (u"ࠩࡶࡨࡰࡥࡶࡦࡴࡶ࡭ࡴࡴࠧ২"): str(__version__)
  }
  if os.path.exists(bstack1ll11lll1l_opy_):
    bstack11lllllll_opy_ = json.load(open(bstack1ll11lll1l_opy_, bstack11l1ll_opy_ (u"ࠪࡶࡧ࠭৩")))
  else:
    bstack11lllllll_opy_ = {}
  bstack11lllllll_opy_[md5_hash] = bstack1111l111l_opy_
  with open(bstack1ll11lll1l_opy_, bstack11l1ll_opy_ (u"ࠦࡼ࠱ࠢ৪")) as outfile:
    json.dump(bstack11lllllll_opy_, outfile)
def bstack11lll1ll1_opy_(self):
  return
def bstack1111llll_opy_(self):
  return
def bstack1ll1ll1l11_opy_(self):
  from selenium.webdriver.remote.webdriver import WebDriver
  WebDriver.quit(self)
def bstack1ll1l11lll_opy_(self):
  global bstack11ll11ll1_opy_
  global bstack111l1l11_opy_
  global bstack1l11ll1ll_opy_
  try:
    if bstack11l1ll_opy_ (u"ࠬࡶࡹࡵࡧࡶࡸࠬ৫") in bstack11ll11ll1_opy_ and self.session_id != None and bstack11111l11_opy_(threading.current_thread(), bstack11l1ll_opy_ (u"࠭ࡴࡦࡵࡷࡗࡹࡧࡴࡶࡵࠪ৬"), bstack11l1ll_opy_ (u"ࠧࠨ৭")) != bstack11l1ll_opy_ (u"ࠨࡵ࡮࡭ࡵࡶࡥࡥࠩ৮"):
      bstack11l1l1l1l_opy_ = bstack11l1ll_opy_ (u"ࠩࡳࡥࡸࡹࡥࡥࠩ৯") if len(threading.current_thread().bstackTestErrorMessages) == 0 else bstack11l1ll_opy_ (u"ࠪࡪࡦ࡯࡬ࡦࡦࠪৰ")
      if bstack11l1l1l1l_opy_ == bstack11l1ll_opy_ (u"ࠫ࡫ࡧࡩ࡭ࡧࡧࠫৱ"):
        bstack1l1lll1l1_opy_(logger)
      if self != None:
        bstack1111ll1l1_opy_(self, bstack11l1l1l1l_opy_, bstack11l1ll_opy_ (u"ࠬ࠲ࠠࠨ৲").join(threading.current_thread().bstackTestErrorMessages))
    threading.current_thread().testStatus = bstack11l1ll_opy_ (u"࠭ࠧ৳")
  except Exception as e:
    logger.debug(bstack11l1ll_opy_ (u"ࠢࡆࡴࡵࡳࡷࠦࡷࡩ࡫࡯ࡩࠥࡳࡡࡳ࡭࡬ࡲ࡬ࠦࡳࡵࡣࡷࡹࡸࡀࠠࠣ৴") + str(e))
  bstack1l11ll1ll_opy_(self)
  self.session_id = None
def bstack1ll1l11l_opy_(self, command_executor=bstack11l1ll_opy_ (u"ࠣࡪࡷࡸࡵࡀ࠯࠰࠳࠵࠻࠳࠶࠮࠱࠰࠴࠾࠹࠺࠴࠵ࠤ৵"), *args, **kwargs):
  bstack1l111l11l_opy_ = bstack1l11l11ll_opy_(self, command_executor, *args, **kwargs)
  try:
    from selenium.webdriver.remote.remote_connection import RemoteConnection
    if isinstance(command_executor, RemoteConnection) and bstack11l1ll_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫࠯ࡥࡲࡱࠬ৶") in command_executor._url:
      bstack1ll1l11l1_opy_.bstack1l1ll1ll1_opy_(bstack11l1ll_opy_ (u"ࠪࡦࡸࡺࡡࡤ࡭ࡢࡷࡪࡹࡳࡪࡱࡱࠫ৷"), True)
  except:
    pass
  if (isinstance(command_executor, str) and bstack11l1ll_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭࠱ࡧࡴࡳࠧ৸") in command_executor):
    bstack1ll1l11l1_opy_.bstack1l1ll1ll1_opy_(bstack11l1ll_opy_ (u"ࠬࡨࡳࡵࡣࡦ࡯ࡤࡹࡥࡴࡵ࡬ࡳࡳ࠭৹"), True)
  threading.current_thread().bstackSessionDriver = self
  bstack11l1ll11_opy_.bstack111111111_opy_(self)
  return bstack1l111l11l_opy_
def bstack1l1lll11l1_opy_(self, driver_command, *args, **kwargs):
  global bstack1ll111llll_opy_
  response = bstack1ll111llll_opy_(self, driver_command, *args, **kwargs)
  try:
    if driver_command == bstack11l1ll_opy_ (u"࠭ࡳࡤࡴࡨࡩࡳࡹࡨࡰࡶࠪ৺"):
      bstack11l1ll11_opy_.bstack1lll11ll_opy_({
          bstack11l1ll_opy_ (u"ࠧࡪ࡯ࡤ࡫ࡪ࠭৻"): response[bstack11l1ll_opy_ (u"ࠨࡸࡤࡰࡺ࡫ࠧৼ")],
          bstack11l1ll_opy_ (u"ࠩࡷࡩࡸࡺ࡟ࡳࡷࡱࡣࡺࡻࡩࡥࠩ৽"): bstack11l1ll11_opy_.current_test_uuid() if bstack11l1ll11_opy_.current_test_uuid() else bstack11l1ll11_opy_.current_hook_uuid()
      })
  except:
    pass
  return response
def bstack11lllll11_opy_(self, command_executor,
             desired_capabilities=None, browser_profile=None, proxy=None,
             keep_alive=True, file_detector=None, options=None):
  global CONFIG
  global bstack111l1l11_opy_
  global bstack111lll111_opy_
  global bstack1ll1ll1l1l_opy_
  global bstack1ll11l1ll1_opy_
  global bstack11l1l1l11_opy_
  global bstack11ll11ll1_opy_
  global bstack1l11l11ll_opy_
  global bstack11l1l1111_opy_
  global bstack1lll1111_opy_
  global bstack11l1llll_opy_
  CONFIG[bstack11l1ll_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࡕࡇࡏࠬ৾")] = str(bstack11ll11ll1_opy_) + str(__version__)
  command_executor = bstack1ll1lll1_opy_()
  logger.debug(bstack11ll1l1l1_opy_.format(command_executor))
  proxy = bstack1l1ll11lll_opy_(CONFIG, proxy)
  bstack11111111_opy_ = 0 if bstack111lll111_opy_ < 0 else bstack111lll111_opy_
  try:
    if bstack1ll11l1ll1_opy_ is True:
      bstack11111111_opy_ = int(multiprocessing.current_process().name)
    elif bstack11l1l1l11_opy_ is True:
      bstack11111111_opy_ = int(threading.current_thread().name)
  except:
    bstack11111111_opy_ = 0
  bstack111lllll1_opy_ = bstack1llll1l1ll_opy_(CONFIG, bstack11111111_opy_)
  logger.debug(bstack111l1l1ll_opy_.format(str(bstack111lllll1_opy_)))
  if bstack11l1ll_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࡏࡳࡨࡧ࡬ࠨ৿") in CONFIG and bstack111l1l1l1_opy_(CONFIG[bstack11l1ll_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࡐࡴࡩࡡ࡭ࠩ਀")]):
    bstack1ll1111111_opy_(bstack111lllll1_opy_)
  if desired_capabilities:
    bstack1111111l1_opy_ = bstack1l1lll1111_opy_(desired_capabilities)
    bstack1111111l1_opy_[bstack11l1ll_opy_ (u"࠭ࡵࡴࡧ࡚࠷ࡈ࠭ਁ")] = bstack1ll1l111_opy_(CONFIG)
    bstack1llll11l1_opy_ = bstack1llll1l1ll_opy_(bstack1111111l1_opy_)
    if bstack1llll11l1_opy_:
      bstack111lllll1_opy_ = update(bstack1llll11l1_opy_, bstack111lllll1_opy_)
    desired_capabilities = None
  if options:
    bstack1l1ll1l11l_opy_(options, bstack111lllll1_opy_)
  if not options:
    options = bstack1lll11lll_opy_(bstack111lllll1_opy_)
  bstack11l1llll_opy_ = CONFIG.get(bstack11l1ll_opy_ (u"ࠧࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࡵࠪਂ"))[bstack11111111_opy_]
  if bstack1ll111l11_opy_.bstack1lll111lll_opy_(CONFIG, bstack11111111_opy_) and bstack1ll111l11_opy_.bstack111l11l1_opy_(bstack111lllll1_opy_, options):
    threading.current_thread().a11yPlatform = True
    bstack1ll111l11_opy_.set_capabilities(bstack111lllll1_opy_, CONFIG)
  if proxy and bstack1lll1ll1l_opy_() >= version.parse(bstack11l1ll_opy_ (u"ࠨ࠶࠱࠵࠵࠴࠰ࠨਃ")):
    options.proxy(proxy)
  if options and bstack1lll1ll1l_opy_() >= version.parse(bstack11l1ll_opy_ (u"ࠩ࠶࠲࠽࠴࠰ࠨ਄")):
    desired_capabilities = None
  if (
          not options and not desired_capabilities
  ) or (
          bstack1lll1ll1l_opy_() < version.parse(bstack11l1ll_opy_ (u"ࠪ࠷࠳࠾࠮࠱ࠩਅ")) and not desired_capabilities
  ):
    desired_capabilities = {}
    desired_capabilities.update(bstack111lllll1_opy_)
  logger.info(bstack1llllll11_opy_)
  if bstack1lll1ll1l_opy_() >= version.parse(bstack11l1ll_opy_ (u"ࠫ࠹࠴࠱࠱࠰࠳ࠫਆ")):
    bstack1l11l11ll_opy_(self, command_executor=command_executor,
              options=options, keep_alive=keep_alive, file_detector=file_detector)
  elif bstack1lll1ll1l_opy_() >= version.parse(bstack11l1ll_opy_ (u"ࠬ࠹࠮࠹࠰࠳ࠫਇ")):
    bstack1l11l11ll_opy_(self, command_executor=command_executor,
              desired_capabilities=desired_capabilities, options=options,
              browser_profile=browser_profile, proxy=proxy,
              keep_alive=keep_alive, file_detector=file_detector)
  elif bstack1lll1ll1l_opy_() >= version.parse(bstack11l1ll_opy_ (u"࠭࠲࠯࠷࠶࠲࠵࠭ਈ")):
    bstack1l11l11ll_opy_(self, command_executor=command_executor,
              desired_capabilities=desired_capabilities,
              browser_profile=browser_profile, proxy=proxy,
              keep_alive=keep_alive, file_detector=file_detector)
  else:
    bstack1l11l11ll_opy_(self, command_executor=command_executor,
              desired_capabilities=desired_capabilities,
              browser_profile=browser_profile, proxy=proxy,
              keep_alive=keep_alive)
  try:
    bstack11ll11111_opy_ = bstack11l1ll_opy_ (u"ࠧࠨਉ")
    if bstack1lll1ll1l_opy_() >= version.parse(bstack11l1ll_opy_ (u"ࠨ࠶࠱࠴࠳࠶ࡢ࠲ࠩਊ")):
      bstack11ll11111_opy_ = self.caps.get(bstack11l1ll_opy_ (u"ࠤࡲࡴࡹ࡯࡭ࡢ࡮ࡋࡹࡧ࡛ࡲ࡭ࠤ਋"))
    else:
      bstack11ll11111_opy_ = self.capabilities.get(bstack11l1ll_opy_ (u"ࠥࡳࡵࡺࡩ࡮ࡣ࡯ࡌࡺࡨࡕࡳ࡮ࠥ਌"))
    if bstack11ll11111_opy_:
      bstack1ll11lll11_opy_(bstack11ll11111_opy_)
      if bstack1lll1ll1l_opy_() <= version.parse(bstack11l1ll_opy_ (u"ࠫ࠸࠴࠱࠴࠰࠳ࠫ਍")):
        self.command_executor._url = bstack11l1ll_opy_ (u"ࠧ࡮ࡴࡵࡲ࠽࠳࠴ࠨ਎") + bstack1lll1l1l1_opy_ + bstack11l1ll_opy_ (u"ࠨ࠺࠹࠲࠲ࡻࡩ࠵ࡨࡶࡤࠥਏ")
      else:
        self.command_executor._url = bstack11l1ll_opy_ (u"ࠢࡩࡶࡷࡴࡸࡀ࠯࠰ࠤਐ") + bstack11ll11111_opy_ + bstack11l1ll_opy_ (u"ࠣ࠱ࡺࡨ࠴࡮ࡵࡣࠤ਑")
      logger.debug(bstack1ll1l1l111_opy_.format(bstack11ll11111_opy_))
    else:
      logger.debug(bstack1l1l1l11l_opy_.format(bstack11l1ll_opy_ (u"ࠤࡒࡴࡹ࡯࡭ࡢ࡮ࠣࡌࡺࡨࠠ࡯ࡱࡷࠤ࡫ࡵࡵ࡯ࡦࠥ਒")))
  except Exception as e:
    logger.debug(bstack1l1l1l11l_opy_.format(e))
  if bstack11l1ll_opy_ (u"ࠪࡶࡴࡨ࡯ࡵࠩਓ") in bstack11ll11ll1_opy_:
    bstack11lll1111_opy_(bstack111lll111_opy_, bstack1lll1111_opy_)
  bstack111l1l11_opy_ = self.session_id
  if bstack11l1ll_opy_ (u"ࠫࡵࡿࡴࡦࡵࡷࠫਔ") in bstack11ll11ll1_opy_ or bstack11l1ll_opy_ (u"ࠬࡨࡥࡩࡣࡹࡩࠬਕ") in bstack11ll11ll1_opy_ or bstack11l1ll_opy_ (u"࠭ࡲࡰࡤࡲࡸࠬਖ") in bstack11ll11ll1_opy_:
    threading.current_thread().bstackSessionId = self.session_id
    threading.current_thread().bstackSessionDriver = self
    threading.current_thread().bstackTestErrorMessages = []
    bstack11l1ll11_opy_.bstack111111111_opy_(self)
  bstack11l1l1111_opy_.append(self)
  if bstack11l1ll_opy_ (u"ࠧࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࡵࠪਗ") in CONFIG and bstack11l1ll_opy_ (u"ࠨࡵࡨࡷࡸ࡯࡯࡯ࡐࡤࡱࡪ࠭ਘ") in CONFIG[bstack11l1ll_opy_ (u"ࠩࡳࡰࡦࡺࡦࡰࡴࡰࡷࠬਙ")][bstack11111111_opy_]:
    bstack1ll1ll1l1l_opy_ = CONFIG[bstack11l1ll_opy_ (u"ࠪࡴࡱࡧࡴࡧࡱࡵࡱࡸ࠭ਚ")][bstack11111111_opy_][bstack11l1ll_opy_ (u"ࠫࡸ࡫ࡳࡴ࡫ࡲࡲࡓࡧ࡭ࡦࠩਛ")]
  logger.debug(bstack1ll1ll1l1_opy_.format(bstack111l1l11_opy_))
try:
  try:
    import Browser
    from subprocess import Popen
    def bstack1ll1lllll_opy_(self, args, bufsize=-1, executable=None,
              stdin=None, stdout=None, stderr=None,
              preexec_fn=None, close_fds=True,
              shell=False, cwd=None, env=None, universal_newlines=None,
              startupinfo=None, creationflags=0,
              restore_signals=True, start_new_session=False,
              pass_fds=(), *, user=None, group=None, extra_groups=None,
              encoding=None, errors=None, text=None, umask=-1, pipesize=-1):
      global CONFIG
      global bstack1111llll1_opy_
      if(bstack11l1ll_opy_ (u"ࠧ࡯࡮ࡥࡧࡻ࠲࡯ࡹࠢਜ") in args[1]):
        with open(os.path.join(os.path.expanduser(bstack11l1ll_opy_ (u"࠭ࡾࠨਝ")), bstack11l1ll_opy_ (u"ࠧ࠯ࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱࠧਞ"), bstack11l1ll_opy_ (u"ࠨ࠰ࡶࡩࡸࡹࡩࡰࡰ࡬ࡨࡸ࠴ࡴࡹࡶࠪਟ")), bstack11l1ll_opy_ (u"ࠩࡺࠫਠ")) as fp:
          fp.write(bstack11l1ll_opy_ (u"ࠥࠦਡ"))
        if(not os.path.exists(os.path.join(os.path.dirname(args[1]), bstack11l1ll_opy_ (u"ࠦ࡮ࡴࡤࡦࡺࡢࡦࡸࡺࡡࡤ࡭࠱࡮ࡸࠨਢ")))):
          with open(args[1], bstack11l1ll_opy_ (u"ࠬࡸࠧਣ")) as f:
            lines = f.readlines()
            index = next((i for i, line in enumerate(lines) if bstack11l1ll_opy_ (u"࠭ࡡࡴࡻࡱࡧࠥ࡬ࡵ࡯ࡥࡷ࡭ࡴࡴࠠࡠࡰࡨࡻࡕࡧࡧࡦࠪࡦࡳࡳࡺࡥࡹࡶ࠯ࠤࡵࡧࡧࡦࠢࡀࠤࡻࡵࡩࡥࠢ࠳࠭ࠬਤ") in line), None)
            if index is not None:
                lines.insert(index+2, bstack111lll1ll_opy_)
            lines.insert(1, bstack1lll1111l_opy_)
            f.seek(0)
            with open(os.path.join(os.path.dirname(args[1]), bstack11l1ll_opy_ (u"ࠢࡪࡰࡧࡩࡽࡥࡢࡴࡶࡤࡧࡰ࠴ࡪࡴࠤਥ")), bstack11l1ll_opy_ (u"ࠨࡹࠪਦ")) as bstack111l11l11_opy_:
              bstack111l11l11_opy_.writelines(lines)
        CONFIG[bstack11l1ll_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࡔࡆࡎࠫਧ")] = str(bstack11ll11ll1_opy_) + str(__version__)
        bstack11111111_opy_ = 0 if bstack111lll111_opy_ < 0 else bstack111lll111_opy_
        try:
          if bstack1ll11l1ll1_opy_ is True:
            bstack11111111_opy_ = int(multiprocessing.current_process().name)
          elif bstack11l1l1l11_opy_ is True:
            bstack11111111_opy_ = int(threading.current_thread().name)
        except:
          bstack11111111_opy_ = 0
        CONFIG[bstack11l1ll_opy_ (u"ࠥࡹࡸ࡫ࡗ࠴ࡅࠥਨ")] = False
        CONFIG[bstack11l1ll_opy_ (u"ࠦ࡮ࡹࡐ࡭ࡣࡼࡻࡷ࡯ࡧࡩࡶࠥ਩")] = True
        bstack111lllll1_opy_ = bstack1llll1l1ll_opy_(CONFIG, bstack11111111_opy_)
        logger.debug(bstack111l1l1ll_opy_.format(str(bstack111lllll1_opy_)))
        if CONFIG.get(bstack11l1ll_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࡐࡴࡩࡡ࡭ࠩਪ")):
          bstack1ll1111111_opy_(bstack111lllll1_opy_)
        if bstack11l1ll_opy_ (u"࠭ࡰ࡭ࡣࡷࡪࡴࡸ࡭ࡴࠩਫ") in CONFIG and bstack11l1ll_opy_ (u"ࠧࡴࡧࡶࡷ࡮ࡵ࡮ࡏࡣࡰࡩࠬਬ") in CONFIG[bstack11l1ll_opy_ (u"ࠨࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࡶࠫਭ")][bstack11111111_opy_]:
          bstack1ll1ll1l1l_opy_ = CONFIG[bstack11l1ll_opy_ (u"ࠩࡳࡰࡦࡺࡦࡰࡴࡰࡷࠬਮ")][bstack11111111_opy_][bstack11l1ll_opy_ (u"ࠪࡷࡪࡹࡳࡪࡱࡱࡒࡦࡳࡥࠨਯ")]
        args.append(os.path.join(os.path.expanduser(bstack11l1ll_opy_ (u"ࠫࢃ࠭ਰ")), bstack11l1ll_opy_ (u"ࠬ࠴ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࠬ਱"), bstack11l1ll_opy_ (u"࠭࠮ࡴࡧࡶࡷ࡮ࡵ࡮ࡪࡦࡶ࠲ࡹࡾࡴࠨਲ")))
        args.append(str(threading.get_ident()))
        args.append(json.dumps(bstack111lllll1_opy_))
        args[1] = os.path.join(os.path.dirname(args[1]), bstack11l1ll_opy_ (u"ࠢࡪࡰࡧࡩࡽࡥࡢࡴࡶࡤࡧࡰ࠴ࡪࡴࠤਲ਼"))
      bstack1111llll1_opy_ = True
      return bstack1l1lll11ll_opy_(self, args, bufsize=bufsize, executable=executable,
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
  def bstack1lll111l11_opy_(self,
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
    global bstack111lll111_opy_
    global bstack1ll1ll1l1l_opy_
    global bstack1ll11l1ll1_opy_
    global bstack11l1l1l11_opy_
    global bstack11ll11ll1_opy_
    CONFIG[bstack11l1ll_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱࡓࡅࡍࠪ਴")] = str(bstack11ll11ll1_opy_) + str(__version__)
    bstack11111111_opy_ = 0 if bstack111lll111_opy_ < 0 else bstack111lll111_opy_
    try:
      if bstack1ll11l1ll1_opy_ is True:
        bstack11111111_opy_ = int(multiprocessing.current_process().name)
      elif bstack11l1l1l11_opy_ is True:
        bstack11111111_opy_ = int(threading.current_thread().name)
    except:
      bstack11111111_opy_ = 0
    CONFIG[bstack11l1ll_opy_ (u"ࠤ࡬ࡷࡕࡲࡡࡺࡹࡵ࡭࡬࡮ࡴࠣਵ")] = True
    bstack111lllll1_opy_ = bstack1llll1l1ll_opy_(CONFIG, bstack11111111_opy_)
    logger.debug(bstack111l1l1ll_opy_.format(str(bstack111lllll1_opy_)))
    if CONFIG.get(bstack11l1ll_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࡎࡲࡧࡦࡲࠧਸ਼")):
      bstack1ll1111111_opy_(bstack111lllll1_opy_)
    if bstack11l1ll_opy_ (u"ࠫࡵࡲࡡࡵࡨࡲࡶࡲࡹࠧ਷") in CONFIG and bstack11l1ll_opy_ (u"ࠬࡹࡥࡴࡵ࡬ࡳࡳࡔࡡ࡮ࡧࠪਸ") in CONFIG[bstack11l1ll_opy_ (u"࠭ࡰ࡭ࡣࡷࡪࡴࡸ࡭ࡴࠩਹ")][bstack11111111_opy_]:
      bstack1ll1ll1l1l_opy_ = CONFIG[bstack11l1ll_opy_ (u"ࠧࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࡵࠪ਺")][bstack11111111_opy_][bstack11l1ll_opy_ (u"ࠨࡵࡨࡷࡸ࡯࡯࡯ࡐࡤࡱࡪ࠭਻")]
    import urllib
    import json
    bstack1lllll1ll1_opy_ = bstack11l1ll_opy_ (u"ࠩࡺࡷࡸࡀ࠯࠰ࡥࡧࡴ࠳ࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮࠲ࡨࡵ࡭࠰ࡲ࡯ࡥࡾࡽࡲࡪࡩ࡫ࡸࡄࡩࡡࡱࡵࡀ਼ࠫ") + urllib.parse.quote(json.dumps(bstack111lllll1_opy_))
    browser = self.connect(bstack1lllll1ll1_opy_)
    return browser
except Exception as e:
    pass
def bstack1lll1l11l1_opy_():
    global bstack1111llll1_opy_
    try:
        from playwright._impl._browser_type import BrowserType
        BrowserType.launch = bstack1lll111l11_opy_
        bstack1111llll1_opy_ = True
    except Exception as e:
        pass
    try:
      import Browser
      from subprocess import Popen
      Popen.__init__ = bstack1ll1lllll_opy_
      bstack1111llll1_opy_ = True
    except Exception as e:
      pass
def bstack1l1ll1l11_opy_(context, bstack1l1l1ll1l_opy_):
  try:
    context.page.evaluate(bstack11l1ll_opy_ (u"ࠥࡣࠥࡃ࠾ࠡࡽࢀࠦ਽"), bstack11l1ll_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࡢࡩࡽ࡫ࡣࡶࡶࡲࡶ࠿ࠦࡻࠣࡣࡦࡸ࡮ࡵ࡮ࠣ࠼ࠣࠦࡸ࡫ࡴࡔࡧࡶࡷ࡮ࡵ࡮ࡏࡣࡰࡩࠧ࠲ࠠࠣࡣࡵ࡫ࡺࡳࡥ࡯ࡶࡶࠦ࠿ࠦࡻࠣࡰࡤࡱࡪࠨ࠺ࠨਾ")+ json.dumps(bstack1l1l1ll1l_opy_) + bstack11l1ll_opy_ (u"ࠧࢃࡽࠣਿ"))
  except Exception as e:
    logger.debug(bstack11l1ll_opy_ (u"ࠨࡥࡹࡥࡨࡴࡹ࡯࡯࡯ࠢ࡬ࡲࠥࡶ࡬ࡢࡻࡺࡶ࡮࡭ࡨࡵࠢࡶࡩࡸࡹࡩࡰࡰࠣࡲࡦࡳࡥࠡࡽࢀࠦੀ"), e)
def bstack11lllll1_opy_(context, message, level):
  try:
    context.page.evaluate(bstack11l1ll_opy_ (u"ࠢࡠࠢࡀࡂࠥࢁࡽࠣੁ"), bstack11l1ll_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࡟ࡦࡺࡨࡧࡺࡺ࡯ࡳ࠼ࠣࡿࠧࡧࡣࡵ࡫ࡲࡲࠧࡀࠠࠣࡣࡱࡲࡴࡺࡡࡵࡧࠥ࠰ࠥࠨࡡࡳࡩࡸࡱࡪࡴࡴࡴࠤ࠽ࠤࢀࠨࡤࡢࡶࡤࠦ࠿࠭ੂ") + json.dumps(message) + bstack11l1ll_opy_ (u"ࠩ࠯ࠦࡱ࡫ࡶࡦ࡮ࠥ࠾ࠬ੃") + json.dumps(level) + bstack11l1ll_opy_ (u"ࠪࢁࢂ࠭੄"))
  except Exception as e:
    logger.debug(bstack11l1ll_opy_ (u"ࠦࡪࡾࡣࡦࡲࡷ࡭ࡴࡴࠠࡪࡰࠣࡴࡱࡧࡹࡸࡴ࡬࡫࡭ࡺࠠࡢࡰࡱࡳࡹࡧࡴࡪࡱࡱࠤࢀࢃࠢ੅"), e)
def bstack1l1l111l1_opy_(self, url):
  global bstack11l111111_opy_
  try:
    bstack1lllllll1_opy_(url)
  except Exception as err:
    logger.debug(bstack1ll1l1lll_opy_.format(str(err)))
  try:
    bstack11l111111_opy_(self, url)
  except Exception as e:
    try:
      bstack1llll111_opy_ = str(e)
      if any(err_msg in bstack1llll111_opy_ for err_msg in bstack11llllll1_opy_):
        bstack1lllllll1_opy_(url, True)
    except Exception as err:
      logger.debug(bstack1ll1l1lll_opy_.format(str(err)))
    raise e
def bstack1l1lll11l_opy_(self):
  global bstack1lll11lll1_opy_
  bstack1lll11lll1_opy_ = self
  return
def bstack1l11l111l_opy_(self):
  global bstack1ll1111ll_opy_
  bstack1ll1111ll_opy_ = self
  return
def bstack1lllll1ll_opy_(self, test):
  global CONFIG
  global bstack1ll1111ll_opy_
  global bstack1lll11lll1_opy_
  global bstack111l1l11_opy_
  global bstack1l1lll11_opy_
  global bstack1ll1ll1l1l_opy_
  global bstack11lll1ll_opy_
  global bstack1ll1ll111l_opy_
  global bstack1ll11l1111_opy_
  global bstack11l1l1111_opy_
  global bstack11l1llll_opy_
  try:
    if not bstack111l1l11_opy_:
      with open(os.path.join(os.path.expanduser(bstack11l1ll_opy_ (u"ࠬࢄࠧ੆")), bstack11l1ll_opy_ (u"࠭࠮ࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠭ੇ"), bstack11l1ll_opy_ (u"ࠧ࠯ࡵࡨࡷࡸ࡯࡯࡯࡫ࡧࡷ࠳ࡺࡸࡵࠩੈ"))) as f:
        bstack11l11l111_opy_ = json.loads(bstack11l1ll_opy_ (u"ࠣࡽࠥ੉") + f.read().strip() + bstack11l1ll_opy_ (u"ࠩࠥࡼࠧࡀࠠࠣࡻࠥࠫ੊") + bstack11l1ll_opy_ (u"ࠥࢁࠧੋ"))
        bstack111l1l11_opy_ = bstack11l11l111_opy_[str(threading.get_ident())]
  except:
    pass
  if bstack11l1l1111_opy_:
    for driver in bstack11l1l1111_opy_:
      if bstack111l1l11_opy_ == driver.session_id:
        if test:
          bstack111l1lll1_opy_ = str(test.data)
          if bstack11111l11_opy_(threading.current_thread(), bstack11l1ll_opy_ (u"ࠫ࡮ࡹࡁ࠲࠳ࡼࡘࡪࡹࡴࠨੌ"), None) and bstack11111l11_opy_(threading.current_thread(), bstack11l1ll_opy_ (u"ࠬࡧ࠱࠲ࡻࡓࡰࡦࡺࡦࡰࡴࡰ੍ࠫ"), None):
            logger.info(bstack11l1ll_opy_ (u"ࠨࡁࡶࡶࡲࡱࡦࡺࡥࠡࡶࡨࡷࡹࠦࡣࡢࡵࡨࠤࡪࡾࡥࡤࡷࡷ࡭ࡴࡴࠠࡩࡣࡶࠤࡪࡴࡤࡦࡦ࠱ࠤࡕࡸ࡯ࡤࡧࡶࡷ࡮ࡴࡧࠡࡨࡲࡶࠥࡧࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽࠥࡺࡥࡴࡶ࡬ࡲ࡬ࠦࡩࡴࠢࡸࡲࡩ࡫ࡲࡸࡣࡼ࠲ࠥࠨ੎"))
            bstack1ll111l11_opy_.bstack1l1llll1l_opy_(driver, class_name=test.parent.name, name=test.name, module_name=None, path=test.source, bstack1l1ll11ll1_opy_=bstack11l1llll_opy_)
        if not bstack1lll1111l1_opy_ and bstack111l1lll1_opy_:
          bstack11l1l1ll_opy_ = {
            bstack11l1ll_opy_ (u"ࠧࡢࡥࡷ࡭ࡴࡴࠧ੏"): bstack11l1ll_opy_ (u"ࠨࡵࡨࡸࡘ࡫ࡳࡴ࡫ࡲࡲࡓࡧ࡭ࡦࠩ੐"),
            bstack11l1ll_opy_ (u"ࠩࡤࡶ࡬ࡻ࡭ࡦࡰࡷࡷࠬੑ"): {
              bstack11l1ll_opy_ (u"ࠪࡲࡦࡳࡥࠨ੒"): bstack111l1lll1_opy_
            }
          }
          bstack1ll11l111l_opy_ = bstack11l1ll_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࡢࡩࡽ࡫ࡣࡶࡶࡲࡶ࠿ࠦࡻࡾࠩ੓").format(json.dumps(bstack11l1l1ll_opy_))
          driver.execute_script(bstack1ll11l111l_opy_)
        if bstack1l1lll11_opy_:
          bstack1111111l_opy_ = {
            bstack11l1ll_opy_ (u"ࠬࡧࡣࡵ࡫ࡲࡲࠬ੔"): bstack11l1ll_opy_ (u"࠭ࡡ࡯ࡰࡲࡸࡦࡺࡥࠨ੕"),
            bstack11l1ll_opy_ (u"ࠧࡢࡴࡪࡹࡲ࡫࡮ࡵࡵࠪ੖"): {
              bstack11l1ll_opy_ (u"ࠨࡦࡤࡸࡦ࠭੗"): bstack111l1lll1_opy_ + bstack11l1ll_opy_ (u"ࠩࠣࡴࡦࡹࡳࡦࡦࠤࠫ੘"),
              bstack11l1ll_opy_ (u"ࠪࡰࡪࡼࡥ࡭ࠩਖ਼"): bstack11l1ll_opy_ (u"ࠫ࡮ࡴࡦࡰࠩਗ਼")
            }
          }
          if bstack1l1lll11_opy_.status == bstack11l1ll_opy_ (u"ࠬࡖࡁࡔࡕࠪਜ਼"):
            bstack1ll11ll1l_opy_ = bstack11l1ll_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࡤ࡫ࡸࡦࡥࡸࡸࡴࡸ࠺ࠡࡽࢀࠫੜ").format(json.dumps(bstack1111111l_opy_))
            driver.execute_script(bstack1ll11ll1l_opy_)
            bstack1111ll1l1_opy_(driver, bstack11l1ll_opy_ (u"ࠧࡱࡣࡶࡷࡪࡪࠧ੝"))
          elif bstack1l1lll11_opy_.status == bstack11l1ll_opy_ (u"ࠨࡈࡄࡍࡑ࠭ਫ਼"):
            reason = bstack11l1ll_opy_ (u"ࠤࠥ੟")
            bstack1l1ll11l_opy_ = bstack111l1lll1_opy_ + bstack11l1ll_opy_ (u"ࠪࠤ࡫ࡧࡩ࡭ࡧࡧࠫ੠")
            if bstack1l1lll11_opy_.message:
              reason = str(bstack1l1lll11_opy_.message)
              bstack1l1ll11l_opy_ = bstack1l1ll11l_opy_ + bstack11l1ll_opy_ (u"ࠫࠥࡽࡩࡵࡪࠣࡩࡷࡸ࡯ࡳ࠼ࠣࠫ੡") + reason
            bstack1111111l_opy_[bstack11l1ll_opy_ (u"ࠬࡧࡲࡨࡷࡰࡩࡳࡺࡳࠨ੢")] = {
              bstack11l1ll_opy_ (u"࠭࡬ࡦࡸࡨࡰࠬ੣"): bstack11l1ll_opy_ (u"ࠧࡦࡴࡵࡳࡷ࠭੤"),
              bstack11l1ll_opy_ (u"ࠨࡦࡤࡸࡦ࠭੥"): bstack1l1ll11l_opy_
            }
            bstack1ll11ll1l_opy_ = bstack11l1ll_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࡠࡧࡻࡩࡨࡻࡴࡰࡴ࠽ࠤࢀࢃࠧ੦").format(json.dumps(bstack1111111l_opy_))
            driver.execute_script(bstack1ll11ll1l_opy_)
            bstack1111ll1l1_opy_(driver, bstack11l1ll_opy_ (u"ࠪࡪࡦ࡯࡬ࡦࡦࠪ੧"), reason)
            bstack11l11l1ll_opy_(reason, str(bstack1l1lll11_opy_), str(bstack111lll111_opy_), logger)
  elif bstack111l1l11_opy_:
    try:
      data = {}
      bstack111l1lll1_opy_ = None
      if test:
        bstack111l1lll1_opy_ = str(test.data)
      if not bstack1lll1111l1_opy_ and bstack111l1lll1_opy_:
        data[bstack11l1ll_opy_ (u"ࠫࡳࡧ࡭ࡦࠩ੨")] = bstack111l1lll1_opy_
      if bstack1l1lll11_opy_:
        if bstack1l1lll11_opy_.status == bstack11l1ll_opy_ (u"ࠬࡖࡁࡔࡕࠪ੩"):
          data[bstack11l1ll_opy_ (u"࠭ࡳࡵࡣࡷࡹࡸ࠭੪")] = bstack11l1ll_opy_ (u"ࠧࡱࡣࡶࡷࡪࡪࠧ੫")
        elif bstack1l1lll11_opy_.status == bstack11l1ll_opy_ (u"ࠨࡈࡄࡍࡑ࠭੬"):
          data[bstack11l1ll_opy_ (u"ࠩࡶࡸࡦࡺࡵࡴࠩ੭")] = bstack11l1ll_opy_ (u"ࠪࡪࡦ࡯࡬ࡦࡦࠪ੮")
          if bstack1l1lll11_opy_.message:
            data[bstack11l1ll_opy_ (u"ࠫࡷ࡫ࡡࡴࡱࡱࠫ੯")] = str(bstack1l1lll11_opy_.message)
      user = CONFIG[bstack11l1ll_opy_ (u"ࠬࡻࡳࡦࡴࡑࡥࡲ࡫ࠧੰ")]
      key = CONFIG[bstack11l1ll_opy_ (u"࠭ࡡࡤࡥࡨࡷࡸࡑࡥࡺࠩੱ")]
      url = bstack11l1ll_opy_ (u"ࠧࡩࡶࡷࡴࡸࡀ࠯࠰ࡽࢀ࠾ࢀࢃࡀࡢࡲ࡬࠲ࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭࠱ࡧࡴࡳ࠯ࡢࡷࡷࡳࡲࡧࡴࡦ࠱ࡶࡩࡸࡹࡩࡰࡰࡶ࠳ࢀࢃ࠮࡫ࡵࡲࡲࠬੲ").format(user, key, bstack111l1l11_opy_)
      headers = {
        bstack11l1ll_opy_ (u"ࠨࡅࡲࡲࡹ࡫࡮ࡵ࠯ࡷࡽࡵ࡫ࠧੳ"): bstack11l1ll_opy_ (u"ࠩࡤࡴࡵࡲࡩࡤࡣࡷ࡭ࡴࡴ࠯࡫ࡵࡲࡲࠬੴ"),
      }
      if bool(data):
        requests.put(url, json=data, headers=headers)
    except Exception as e:
      logger.error(bstack1lll1l1l_opy_.format(str(e)))
  if bstack1ll1111ll_opy_:
    bstack1ll1ll111l_opy_(bstack1ll1111ll_opy_)
  if bstack1lll11lll1_opy_:
    bstack1ll11l1111_opy_(bstack1lll11lll1_opy_)
  bstack11lll1ll_opy_(self, test)
def bstack1llllll1l1_opy_(self, parent, test, skip_on_failure=None, rpa=False):
  global bstack111l111l1_opy_
  global CONFIG
  global bstack11l1l1111_opy_
  global bstack111l1l11_opy_
  bstack1l1l11ll_opy_ = None
  try:
    if bstack11111l11_opy_(threading.current_thread(), bstack11l1ll_opy_ (u"ࠪࡥ࠶࠷ࡹࡑ࡮ࡤࡸ࡫ࡵࡲ࡮ࠩੵ"), None):
      try:
        if not bstack111l1l11_opy_:
          with open(os.path.join(os.path.expanduser(bstack11l1ll_opy_ (u"ࠫࢃ࠭੶")), bstack11l1ll_opy_ (u"ࠬ࠴ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࠬ੷"), bstack11l1ll_opy_ (u"࠭࠮ࡴࡧࡶࡷ࡮ࡵ࡮ࡪࡦࡶ࠲ࡹࡾࡴࠨ੸"))) as f:
            bstack11l11l111_opy_ = json.loads(bstack11l1ll_opy_ (u"ࠢࡼࠤ੹") + f.read().strip() + bstack11l1ll_opy_ (u"ࠨࠤࡻࠦ࠿ࠦࠢࡺࠤࠪ੺") + bstack11l1ll_opy_ (u"ࠤࢀࠦ੻"))
            bstack111l1l11_opy_ = bstack11l11l111_opy_[str(threading.get_ident())]
      except:
        pass
      if bstack11l1l1111_opy_:
        for driver in bstack11l1l1111_opy_:
          if bstack111l1l11_opy_ == driver.session_id:
            bstack1l1l11ll_opy_ = driver
    bstack111111ll_opy_ = bstack1ll111l11_opy_.bstack1llllll111_opy_(CONFIG, test.tags)
    if bstack1l1l11ll_opy_:
      threading.current_thread().isA11yTest = bstack1ll111l11_opy_.bstack1l1l1lll1_opy_(bstack1l1l11ll_opy_, bstack111111ll_opy_)
    else:
      threading.current_thread().isA11yTest = bstack111111ll_opy_
  except:
    pass
  bstack111l111l1_opy_(self, parent, test, skip_on_failure=skip_on_failure, rpa=rpa)
  global bstack1l1lll11_opy_
  bstack1l1lll11_opy_ = self._test
def bstack1l11ll11l_opy_():
  global bstack1lll11111l_opy_
  try:
    if os.path.exists(bstack1lll11111l_opy_):
      os.remove(bstack1lll11111l_opy_)
  except Exception as e:
    logger.debug(bstack11l1ll_opy_ (u"ࠪࡉࡷࡸ࡯ࡳࠢ࡬ࡲࠥࡪࡥ࡭ࡧࡷ࡭ࡳ࡭ࠠࡳࡱࡥࡳࡹࠦࡲࡦࡲࡲࡶࡹࠦࡦࡪ࡮ࡨ࠾ࠥ࠭੼") + str(e))
def bstack11l1l1l1_opy_():
  global bstack1lll11111l_opy_
  bstack1ll1111ll1_opy_ = {}
  try:
    if not os.path.isfile(bstack1lll11111l_opy_):
      with open(bstack1lll11111l_opy_, bstack11l1ll_opy_ (u"ࠫࡼ࠭੽")):
        pass
      with open(bstack1lll11111l_opy_, bstack11l1ll_opy_ (u"ࠧࡽࠫࠣ੾")) as outfile:
        json.dump({}, outfile)
    if os.path.exists(bstack1lll11111l_opy_):
      bstack1ll1111ll1_opy_ = json.load(open(bstack1lll11111l_opy_, bstack11l1ll_opy_ (u"࠭ࡲࡣࠩ੿")))
  except Exception as e:
    logger.debug(bstack11l1ll_opy_ (u"ࠧࡆࡴࡵࡳࡷࠦࡩ࡯ࠢࡵࡩࡦࡪࡩ࡯ࡩࠣࡶࡴࡨ࡯ࡵࠢࡵࡩࡵࡵࡲࡵࠢࡩ࡭ࡱ࡫࠺ࠡࠩ઀") + str(e))
  finally:
    return bstack1ll1111ll1_opy_
def bstack11lll1111_opy_(platform_index, item_index):
  global bstack1lll11111l_opy_
  try:
    bstack1ll1111ll1_opy_ = bstack11l1l1l1_opy_()
    bstack1ll1111ll1_opy_[item_index] = platform_index
    with open(bstack1lll11111l_opy_, bstack11l1ll_opy_ (u"ࠣࡹ࠮ࠦઁ")) as outfile:
      json.dump(bstack1ll1111ll1_opy_, outfile)
  except Exception as e:
    logger.debug(bstack11l1ll_opy_ (u"ࠩࡈࡶࡷࡵࡲࠡ࡫ࡱࠤࡼࡸࡩࡵ࡫ࡱ࡫ࠥࡺ࡯ࠡࡴࡲࡦࡴࡺࠠࡳࡧࡳࡳࡷࡺࠠࡧ࡫࡯ࡩ࠿ࠦࠧં") + str(e))
def bstack11111l1l1_opy_(bstack1ll11l1l1l_opy_):
  global CONFIG
  bstack111ll11l_opy_ = bstack11l1ll_opy_ (u"ࠪࠫઃ")
  if not bstack11l1ll_opy_ (u"ࠫࡵࡲࡡࡵࡨࡲࡶࡲࡹࠧ઄") in CONFIG:
    logger.info(bstack11l1ll_opy_ (u"ࠬࡔ࡯ࠡࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࡶࠤࡵࡧࡳࡴࡧࡧࠤࡺࡴࡡࡣ࡮ࡨࠤࡹࡵࠠࡨࡧࡱࡩࡷࡧࡴࡦࠢࡵࡩࡵࡵࡲࡵࠢࡩࡳࡷࠦࡒࡰࡤࡲࡸࠥࡸࡵ࡯ࠩઅ"))
  try:
    platform = CONFIG[bstack11l1ll_opy_ (u"࠭ࡰ࡭ࡣࡷࡪࡴࡸ࡭ࡴࠩઆ")][bstack1ll11l1l1l_opy_]
    if bstack11l1ll_opy_ (u"ࠧࡰࡵࠪઇ") in platform:
      bstack111ll11l_opy_ += str(platform[bstack11l1ll_opy_ (u"ࠨࡱࡶࠫઈ")]) + bstack11l1ll_opy_ (u"ࠩ࠯ࠤࠬઉ")
    if bstack11l1ll_opy_ (u"ࠪࡳࡸ࡜ࡥࡳࡵ࡬ࡳࡳ࠭ઊ") in platform:
      bstack111ll11l_opy_ += str(platform[bstack11l1ll_opy_ (u"ࠫࡴࡹࡖࡦࡴࡶ࡭ࡴࡴࠧઋ")]) + bstack11l1ll_opy_ (u"ࠬ࠲ࠠࠨઌ")
    if bstack11l1ll_opy_ (u"࠭ࡤࡦࡸ࡬ࡧࡪࡔࡡ࡮ࡧࠪઍ") in platform:
      bstack111ll11l_opy_ += str(platform[bstack11l1ll_opy_ (u"ࠧࡥࡧࡹ࡭ࡨ࡫ࡎࡢ࡯ࡨࠫ઎")]) + bstack11l1ll_opy_ (u"ࠨ࠮ࠣࠫએ")
    if bstack11l1ll_opy_ (u"ࠩࡳࡰࡦࡺࡦࡰࡴࡰ࡚ࡪࡸࡳࡪࡱࡱࠫઐ") in platform:
      bstack111ll11l_opy_ += str(platform[bstack11l1ll_opy_ (u"ࠪࡴࡱࡧࡴࡧࡱࡵࡱ࡛࡫ࡲࡴ࡫ࡲࡲࠬઑ")]) + bstack11l1ll_opy_ (u"ࠫ࠱ࠦࠧ઒")
    if bstack11l1ll_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡔࡡ࡮ࡧࠪઓ") in platform:
      bstack111ll11l_opy_ += str(platform[bstack11l1ll_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡎࡢ࡯ࡨࠫઔ")]) + bstack11l1ll_opy_ (u"ࠧ࠭ࠢࠪક")
    if bstack11l1ll_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡘࡨࡶࡸ࡯࡯࡯ࠩખ") in platform:
      bstack111ll11l_opy_ += str(platform[bstack11l1ll_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴ࡙ࡩࡷࡹࡩࡰࡰࠪગ")]) + bstack11l1ll_opy_ (u"ࠪ࠰ࠥ࠭ઘ")
  except Exception as e:
    logger.debug(bstack11l1ll_opy_ (u"ࠫࡘࡵ࡭ࡦࠢࡨࡶࡷࡵࡲࠡ࡫ࡱࠤ࡬࡫࡮ࡦࡴࡤࡸ࡮ࡴࡧࠡࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࠣࡷࡹࡸࡩ࡯ࡩࠣࡪࡴࡸࠠࡳࡧࡳࡳࡷࡺࠠࡨࡧࡱࡩࡷࡧࡴࡪࡱࡱࠫઙ") + str(e))
  finally:
    if bstack111ll11l_opy_[len(bstack111ll11l_opy_) - 2:] == bstack11l1ll_opy_ (u"ࠬ࠲ࠠࠨચ"):
      bstack111ll11l_opy_ = bstack111ll11l_opy_[:-2]
    return bstack111ll11l_opy_
def bstack1l1ll1111_opy_(path, bstack111ll11l_opy_):
  try:
    import xml.etree.ElementTree as ET
    bstack11l111ll1_opy_ = ET.parse(path)
    bstack1l1lllll11_opy_ = bstack11l111ll1_opy_.getroot()
    bstack111ll1l1_opy_ = None
    for suite in bstack1l1lllll11_opy_.iter(bstack11l1ll_opy_ (u"࠭ࡳࡶ࡫ࡷࡩࠬછ")):
      if bstack11l1ll_opy_ (u"ࠧࡴࡱࡸࡶࡨ࡫ࠧજ") in suite.attrib:
        suite.attrib[bstack11l1ll_opy_ (u"ࠨࡰࡤࡱࡪ࠭ઝ")] += bstack11l1ll_opy_ (u"ࠩࠣࠫઞ") + bstack111ll11l_opy_
        bstack111ll1l1_opy_ = suite
    bstack1l1l11l1_opy_ = None
    for robot in bstack1l1lllll11_opy_.iter(bstack11l1ll_opy_ (u"ࠪࡶࡴࡨ࡯ࡵࠩટ")):
      bstack1l1l11l1_opy_ = robot
    bstack1111lllll_opy_ = len(bstack1l1l11l1_opy_.findall(bstack11l1ll_opy_ (u"ࠫࡸࡻࡩࡵࡧࠪઠ")))
    if bstack1111lllll_opy_ == 1:
      bstack1l1l11l1_opy_.remove(bstack1l1l11l1_opy_.findall(bstack11l1ll_opy_ (u"ࠬࡹࡵࡪࡶࡨࠫડ"))[0])
      bstack11111l11l_opy_ = ET.Element(bstack11l1ll_opy_ (u"࠭ࡳࡶ࡫ࡷࡩࠬઢ"), attrib={bstack11l1ll_opy_ (u"ࠧ࡯ࡣࡰࡩࠬણ"): bstack11l1ll_opy_ (u"ࠨࡕࡸ࡭ࡹ࡫ࡳࠨત"), bstack11l1ll_opy_ (u"ࠩ࡬ࡨࠬથ"): bstack11l1ll_opy_ (u"ࠪࡷ࠵࠭દ")})
      bstack1l1l11l1_opy_.insert(1, bstack11111l11l_opy_)
      bstack111l1lll_opy_ = None
      for suite in bstack1l1l11l1_opy_.iter(bstack11l1ll_opy_ (u"ࠫࡸࡻࡩࡵࡧࠪધ")):
        bstack111l1lll_opy_ = suite
      bstack111l1lll_opy_.append(bstack111ll1l1_opy_)
      bstack1l1111ll1_opy_ = None
      for status in bstack111ll1l1_opy_.iter(bstack11l1ll_opy_ (u"ࠬࡹࡴࡢࡶࡸࡷࠬન")):
        bstack1l1111ll1_opy_ = status
      bstack111l1lll_opy_.append(bstack1l1111ll1_opy_)
    bstack11l111ll1_opy_.write(path)
  except Exception as e:
    logger.debug(bstack11l1ll_opy_ (u"࠭ࡅࡳࡴࡲࡶࠥ࡯࡮ࠡࡲࡤࡶࡸ࡯࡮ࡨࠢࡺ࡬࡮ࡲࡥࠡࡩࡨࡲࡪࡸࡡࡵ࡫ࡱ࡫ࠥࡸ࡯ࡣࡱࡷࠤࡷ࡫ࡰࡰࡴࡷࠫ઩") + str(e))
def bstack1ll1l1ll_opy_(outs_dir, pabot_args, options, start_time_string, tests_root_name):
  global bstack1ll11ll11l_opy_
  global CONFIG
  if bstack11l1ll_opy_ (u"ࠢࡱࡻࡷ࡬ࡴࡴࡰࡢࡶ࡫ࠦપ") in options:
    del options[bstack11l1ll_opy_ (u"ࠣࡲࡼࡸ࡭ࡵ࡮ࡱࡣࡷ࡬ࠧફ")]
  bstack11lll111l_opy_ = bstack11l1l1l1_opy_()
  for bstack1ll1l1l1ll_opy_ in bstack11lll111l_opy_.keys():
    path = os.path.join(os.getcwd(), bstack11l1ll_opy_ (u"ࠩࡳࡥࡧࡵࡴࡠࡴࡨࡷࡺࡲࡴࡴࠩબ"), str(bstack1ll1l1l1ll_opy_), bstack11l1ll_opy_ (u"ࠪࡳࡺࡺࡰࡶࡶ࠱ࡼࡲࡲࠧભ"))
    bstack1l1ll1111_opy_(path, bstack11111l1l1_opy_(bstack11lll111l_opy_[bstack1ll1l1l1ll_opy_]))
  bstack1l11ll11l_opy_()
  return bstack1ll11ll11l_opy_(outs_dir, pabot_args, options, start_time_string, tests_root_name)
def bstack1lll1ll1l1_opy_(self, ff_profile_dir):
  global bstack111l111ll_opy_
  if not ff_profile_dir:
    return None
  return bstack111l111ll_opy_(self, ff_profile_dir)
def bstack1ll1lll1l1_opy_(datasources, opts_for_run, outs_dir, pabot_args, suite_group):
  from pabot.pabot import QueueItem
  global CONFIG
  global bstack1l1111ll_opy_
  bstack11ll1lll1_opy_ = []
  if bstack11l1ll_opy_ (u"ࠫࡵࡲࡡࡵࡨࡲࡶࡲࡹࠧમ") in CONFIG:
    bstack11ll1lll1_opy_ = CONFIG[bstack11l1ll_opy_ (u"ࠬࡶ࡬ࡢࡶࡩࡳࡷࡳࡳࠨય")]
  return [
    QueueItem(
      datasources,
      outs_dir,
      opts_for_run,
      suite,
      pabot_args[bstack11l1ll_opy_ (u"ࠨࡣࡰ࡯ࡰࡥࡳࡪࠢર")],
      pabot_args[bstack11l1ll_opy_ (u"ࠢࡷࡧࡵࡦࡴࡹࡥࠣ઱")],
      argfile,
      pabot_args.get(bstack11l1ll_opy_ (u"ࠣࡪ࡬ࡺࡪࠨલ")),
      pabot_args[bstack11l1ll_opy_ (u"ࠤࡳࡶࡴࡩࡥࡴࡵࡨࡷࠧળ")],
      platform[0],
      bstack1l1111ll_opy_
    )
    for suite in suite_group
    for argfile in pabot_args[bstack11l1ll_opy_ (u"ࠥࡥࡷ࡭ࡵ࡮ࡧࡱࡸ࡫࡯࡬ࡦࡵࠥ઴")] or [(bstack11l1ll_opy_ (u"ࠦࠧવ"), None)]
    for platform in enumerate(bstack11ll1lll1_opy_)
  ]
def bstack111l11ll1_opy_(self, datasources, outs_dir, options,
                        execution_item, command, verbose, argfile,
                        hive=None, processes=0, platform_index=0, bstack1lll1lll1_opy_=bstack11l1ll_opy_ (u"ࠬ࠭શ")):
  global bstack111l11111_opy_
  self.platform_index = platform_index
  self.bstack1llllll1l_opy_ = bstack1lll1lll1_opy_
  bstack111l11111_opy_(self, datasources, outs_dir, options,
                      execution_item, command, verbose, argfile, hive, processes)
def bstack11l11ll11_opy_(caller_id, datasources, is_last, item, outs_dir):
  global bstack1l11lllll_opy_
  global bstack1llll1ll_opy_
  if not bstack11l1ll_opy_ (u"࠭ࡶࡢࡴ࡬ࡥࡧࡲࡥࠨષ") in item.options:
    item.options[bstack11l1ll_opy_ (u"ࠧࡷࡣࡵ࡭ࡦࡨ࡬ࡦࠩસ")] = []
  for v in item.options[bstack11l1ll_opy_ (u"ࠨࡸࡤࡶ࡮ࡧࡢ࡭ࡧࠪહ")]:
    if bstack11l1ll_opy_ (u"ࠩࡅࡗ࡙ࡇࡃࡌࡒࡏࡅ࡙ࡌࡏࡓࡏࡌࡒࡉࡋࡘࠨ઺") in v:
      item.options[bstack11l1ll_opy_ (u"ࠪࡺࡦࡸࡩࡢࡤ࡯ࡩࠬ઻")].remove(v)
    if bstack11l1ll_opy_ (u"ࠫࡇ࡙ࡔࡂࡅࡎࡇࡑࡏࡁࡓࡉࡖ઼ࠫ") in v:
      item.options[bstack11l1ll_opy_ (u"ࠬࡼࡡࡳ࡫ࡤࡦࡱ࡫ࠧઽ")].remove(v)
  item.options[bstack11l1ll_opy_ (u"࠭ࡶࡢࡴ࡬ࡥࡧࡲࡥࠨા")].insert(0, bstack11l1ll_opy_ (u"ࠧࡃࡕࡗࡅࡈࡑࡐࡍࡃࡗࡊࡔࡘࡍࡊࡐࡇࡉ࡝ࡀࡻࡾࠩિ").format(item.platform_index))
  item.options[bstack11l1ll_opy_ (u"ࠨࡸࡤࡶ࡮ࡧࡢ࡭ࡧࠪી")].insert(0, bstack11l1ll_opy_ (u"ࠩࡅࡗ࡙ࡇࡃࡌࡆࡈࡊࡑࡕࡃࡂࡎࡌࡈࡊࡔࡔࡊࡈࡌࡉࡗࡀࡻࡾࠩુ").format(item.bstack1llllll1l_opy_))
  if bstack1llll1ll_opy_:
    item.options[bstack11l1ll_opy_ (u"ࠪࡺࡦࡸࡩࡢࡤ࡯ࡩࠬૂ")].insert(0, bstack11l1ll_opy_ (u"ࠫࡇ࡙ࡔࡂࡅࡎࡇࡑࡏࡁࡓࡉࡖ࠾ࢀࢃࠧૃ").format(bstack1llll1ll_opy_))
  return bstack1l11lllll_opy_(caller_id, datasources, is_last, item, outs_dir)
def bstack1ll1l11l11_opy_(command, item_index):
  os.environ[bstack11l1ll_opy_ (u"ࠬࡉࡕࡓࡔࡈࡒ࡙ࡥࡐࡍࡃࡗࡊࡔࡘࡍࡠࡆࡄࡘࡆ࠭ૄ")] = json.dumps(CONFIG[bstack11l1ll_opy_ (u"࠭ࡰ࡭ࡣࡷࡪࡴࡸ࡭ࡴࠩૅ")][item_index % bstack1lll11l1_opy_])
  global bstack1llll1ll_opy_
  if bstack1llll1ll_opy_:
    command[0] = command[0].replace(bstack11l1ll_opy_ (u"ࠧࡳࡱࡥࡳࡹ࠭૆"), bstack11l1ll_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠭ࡴࡦ࡮ࠤࡷࡵࡢࡰࡶ࠰࡭ࡳࡺࡥࡳࡰࡤࡰࠥ࠳࠭ࡣࡵࡷࡥࡨࡱ࡟ࡪࡶࡨࡱࡤ࡯࡮ࡥࡧࡻࠤࠬે") + str(
      item_index) + bstack11l1ll_opy_ (u"ࠩࠣࠫૈ") + bstack1llll1ll_opy_, 1)
  else:
    command[0] = command[0].replace(bstack11l1ll_opy_ (u"ࠪࡶࡴࡨ࡯ࡵࠩૉ"),
                                    bstack11l1ll_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭࠰ࡷࡩࡱࠠࡳࡱࡥࡳࡹ࠳ࡩ࡯ࡶࡨࡶࡳࡧ࡬ࠡ࠯࠰ࡦࡸࡺࡡࡤ࡭ࡢ࡭ࡹ࡫࡭ࡠ࡫ࡱࡨࡪࡾࠠࠨ૊") + str(item_index), 1)
def bstack1l1l1lll_opy_(command, stderr, stdout, item_name, verbose, pool_id, item_index):
  global bstack1l1lllll1l_opy_
  bstack1ll1l11l11_opy_(command, item_index)
  return bstack1l1lllll1l_opy_(command, stderr, stdout, item_name, verbose, pool_id, item_index)
def bstack1l1l1ll11_opy_(command, stderr, stdout, item_name, verbose, pool_id, item_index, outs_dir):
  global bstack1l1lllll1l_opy_
  bstack1ll1l11l11_opy_(command, item_index)
  return bstack1l1lllll1l_opy_(command, stderr, stdout, item_name, verbose, pool_id, item_index, outs_dir)
def bstack1ll1l11ll1_opy_(command, stderr, stdout, item_name, verbose, pool_id, item_index, outs_dir, process_timeout):
  global bstack1l1lllll1l_opy_
  bstack1ll1l11l11_opy_(command, item_index)
  return bstack1l1lllll1l_opy_(command, stderr, stdout, item_name, verbose, pool_id, item_index, outs_dir, process_timeout)
def bstack11ll1ll1l_opy_(self, runner, quiet=False, capture=True):
  global bstack1ll11llll1_opy_
  bstack1l111l1l1_opy_ = bstack1ll11llll1_opy_(self, runner, quiet=False, capture=True)
  if self.exception:
    if not hasattr(runner, bstack11l1ll_opy_ (u"ࠬ࡫ࡸࡤࡧࡳࡸ࡮ࡵ࡮ࡠࡣࡵࡶࠬો")):
      runner.exception_arr = []
    if not hasattr(runner, bstack11l1ll_opy_ (u"࠭ࡥࡹࡥࡢࡸࡷࡧࡣࡦࡤࡤࡧࡰࡥࡡࡳࡴࠪૌ")):
      runner.exc_traceback_arr = []
    runner.exception = self.exception
    runner.exc_traceback = self.exc_traceback
    runner.exception_arr.append(self.exception)
    runner.exc_traceback_arr.append(self.exc_traceback)
  return bstack1l111l1l1_opy_
def bstack1l1lll111_opy_(self, name, context, *args):
  os.environ[bstack11l1ll_opy_ (u"ࠧࡄࡗࡕࡖࡊࡔࡔࡠࡒࡏࡅ࡙ࡌࡏࡓࡏࡢࡈࡆ࡚ࡁࠨ્")] = json.dumps(CONFIG[bstack11l1ll_opy_ (u"ࠨࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࡶࠫ૎")][int(threading.current_thread()._name) % bstack1lll11l1_opy_])
  global bstack1l1ll11l11_opy_
  if name == bstack11l1ll_opy_ (u"ࠩࡥࡩ࡫ࡵࡲࡦࡡࡩࡩࡦࡺࡵࡳࡧࠪ૏"):
    bstack1l1ll11l11_opy_(self, name, context, *args)
    try:
      if not bstack1lll1111l1_opy_:
        bstack1l1l11ll_opy_ = threading.current_thread().bstackSessionDriver if bstack1llll11111_opy_(bstack11l1ll_opy_ (u"ࠪࡦࡸࡺࡡࡤ࡭ࡖࡩࡸࡹࡩࡰࡰࡇࡶ࡮ࡼࡥࡳࠩૐ")) else context.browser
        bstack1l1l1ll1l_opy_ = str(self.feature.name)
        bstack1l1ll1l11_opy_(context, bstack1l1l1ll1l_opy_)
        bstack1l1l11ll_opy_.execute_script(bstack11l1ll_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࡢࡩࡽ࡫ࡣࡶࡶࡲࡶ࠿ࠦࡻࠣࡣࡦࡸ࡮ࡵ࡮ࠣ࠼ࠣࠦࡸ࡫ࡴࡔࡧࡶࡷ࡮ࡵ࡮ࡏࡣࡰࡩࠧ࠲ࠠࠣࡣࡵ࡫ࡺࡳࡥ࡯ࡶࡶࠦ࠿ࠦࡻࠣࡰࡤࡱࡪࠨ࠺ࠡࠩ૑") + json.dumps(bstack1l1l1ll1l_opy_) + bstack11l1ll_opy_ (u"ࠬࢃࡽࠨ૒"))
      self.driver_before_scenario = False
    except Exception as e:
      logger.debug(bstack11l1ll_opy_ (u"࠭ࡆࡢ࡫࡯ࡩࡩࠦࡴࡰࠢࡶࡩࡹࠦࡳࡦࡵࡶ࡭ࡴࡴࠠ࡯ࡣࡰࡩࠥ࡯࡮ࠡࡤࡨࡪࡴࡸࡥࠡࡨࡨࡥࡹࡻࡲࡦ࠼ࠣࡿࢂ࠭૓").format(str(e)))
  elif name == bstack11l1ll_opy_ (u"ࠧࡣࡧࡩࡳࡷ࡫࡟ࡴࡥࡨࡲࡦࡸࡩࡰࠩ૔"):
    bstack1l1ll11l11_opy_(self, name, context, *args)
    try:
      if not hasattr(self, bstack11l1ll_opy_ (u"ࠨࡦࡵ࡭ࡻ࡫ࡲࡠࡤࡨࡪࡴࡸࡥࡠࡵࡦࡩࡳࡧࡲࡪࡱࠪ૕")):
        self.driver_before_scenario = True
      if (not bstack1lll1111l1_opy_):
        scenario_name = args[0].name
        feature_name = bstack1l1l1ll1l_opy_ = str(self.feature.name)
        bstack1l1l1ll1l_opy_ = feature_name + bstack11l1ll_opy_ (u"ࠩࠣ࠱ࠥ࠭૖") + scenario_name
        bstack1l1l11ll_opy_ = threading.current_thread().bstackSessionDriver if bstack1llll11111_opy_(bstack11l1ll_opy_ (u"ࠪࡦࡸࡺࡡࡤ࡭ࡖࡩࡸࡹࡩࡰࡰࡇࡶ࡮ࡼࡥࡳࠩ૗")) else context.browser
        if self.driver_before_scenario:
          bstack1l1ll1l11_opy_(context, bstack1l1l1ll1l_opy_)
          bstack1l1l11ll_opy_.execute_script(bstack11l1ll_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࡢࡩࡽ࡫ࡣࡶࡶࡲࡶ࠿ࠦࡻࠣࡣࡦࡸ࡮ࡵ࡮ࠣ࠼ࠣࠦࡸ࡫ࡴࡔࡧࡶࡷ࡮ࡵ࡮ࡏࡣࡰࡩࠧ࠲ࠠࠣࡣࡵ࡫ࡺࡳࡥ࡯ࡶࡶࠦ࠿ࠦࡻࠣࡰࡤࡱࡪࠨ࠺ࠡࠩ૘") + json.dumps(bstack1l1l1ll1l_opy_) + bstack11l1ll_opy_ (u"ࠬࢃࡽࠨ૙"))
    except Exception as e:
      logger.debug(bstack11l1ll_opy_ (u"࠭ࡆࡢ࡫࡯ࡩࡩࠦࡴࡰࠢࡶࡩࡹࠦࡳࡦࡵࡶ࡭ࡴࡴࠠ࡯ࡣࡰࡩࠥ࡯࡮ࠡࡤࡨࡪࡴࡸࡥࠡࡵࡦࡩࡳࡧࡲࡪࡱ࠽ࠤࢀࢃࠧ૚").format(str(e)))
  elif name == bstack11l1ll_opy_ (u"ࠧࡢࡨࡷࡩࡷࡥࡳࡤࡧࡱࡥࡷ࡯࡯ࠨ૛"):
    try:
      bstack1l1111l11_opy_ = args[0].status.name
      bstack1l1l11ll_opy_ = threading.current_thread().bstackSessionDriver if bstack11l1ll_opy_ (u"ࠨࡤࡶࡸࡦࡩ࡫ࡔࡧࡶࡷ࡮ࡵ࡮ࡅࡴ࡬ࡺࡪࡸࠧ૜") in threading.current_thread().__dict__.keys() else context.browser
      if str(bstack1l1111l11_opy_).lower() == bstack11l1ll_opy_ (u"ࠩࡩࡥ࡮ࡲࡥࡥࠩ૝"):
        bstack111l1111l_opy_ = bstack11l1ll_opy_ (u"ࠪࠫ૞")
        bstack1llll1lll1_opy_ = bstack11l1ll_opy_ (u"ࠫࠬ૟")
        bstack1ll1llll1l_opy_ = bstack11l1ll_opy_ (u"ࠬ࠭ૠ")
        try:
          import traceback
          bstack111l1111l_opy_ = self.exception.__class__.__name__
          bstack1lllllll1l_opy_ = traceback.format_tb(self.exc_traceback)
          bstack1llll1lll1_opy_ = bstack11l1ll_opy_ (u"࠭ࠠࠨૡ").join(bstack1lllllll1l_opy_)
          bstack1ll1llll1l_opy_ = bstack1lllllll1l_opy_[-1]
        except Exception as e:
          logger.debug(bstack1ll11llll_opy_.format(str(e)))
        bstack111l1111l_opy_ += bstack1ll1llll1l_opy_
        bstack11lllll1_opy_(context, json.dumps(str(args[0].name) + bstack11l1ll_opy_ (u"ࠢࠡ࠯ࠣࡊࡦ࡯࡬ࡦࡦࠤࡠࡳࠨૢ") + str(bstack1llll1lll1_opy_)),
                            bstack11l1ll_opy_ (u"ࠣࡧࡵࡶࡴࡸࠢૣ"))
        if self.driver_before_scenario:
          bstack1l1ll111l_opy_(getattr(context, bstack11l1ll_opy_ (u"ࠩࡳࡥ࡬࡫ࠧ૤"), None), bstack11l1ll_opy_ (u"ࠥࡪࡦ࡯࡬ࡦࡦࠥ૥"), bstack111l1111l_opy_)
          bstack1l1l11ll_opy_.execute_script(bstack11l1ll_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࡢࡩࡽ࡫ࡣࡶࡶࡲࡶ࠿ࠦࡻࠣࡣࡦࡸ࡮ࡵ࡮ࠣ࠼ࠣࠦࡦࡴ࡮ࡰࡶࡤࡸࡪࠨࠬࠡࠤࡤࡶ࡬ࡻ࡭ࡦࡰࡷࡷࠧࡀࠠࡼࠤࡧࡥࡹࡧࠢ࠻ࠩ૦") + json.dumps(str(args[0].name) + bstack11l1ll_opy_ (u"ࠧࠦ࠭ࠡࡈࡤ࡭ࡱ࡫ࡤࠢ࡞ࡱࠦ૧") + str(bstack1llll1lll1_opy_)) + bstack11l1ll_opy_ (u"࠭ࠬࠡࠤ࡯ࡩࡻ࡫࡬ࠣ࠼ࠣࠦࡪࡸࡲࡰࡴࠥࢁࢂ࠭૨"))
        if self.driver_before_scenario:
          bstack1111ll1l1_opy_(bstack1l1l11ll_opy_, bstack11l1ll_opy_ (u"ࠧࡧࡣ࡬ࡰࡪࡪࠧ૩"), bstack11l1ll_opy_ (u"ࠣࡕࡦࡩࡳࡧࡲࡪࡱࠣࡪࡦ࡯࡬ࡦࡦࠣࡻ࡮ࡺࡨ࠻ࠢ࡟ࡲࠧ૪") + str(bstack111l1111l_opy_))
      else:
        bstack11lllll1_opy_(context, bstack11l1ll_opy_ (u"ࠤࡓࡥࡸࡹࡥࡥࠣࠥ૫"), bstack11l1ll_opy_ (u"ࠥ࡭ࡳ࡬࡯ࠣ૬"))
        if self.driver_before_scenario:
          bstack1l1ll111l_opy_(getattr(context, bstack11l1ll_opy_ (u"ࠫࡵࡧࡧࡦࠩ૭"), None), bstack11l1ll_opy_ (u"ࠧࡶࡡࡴࡵࡨࡨࠧ૮"))
        bstack1l1l11ll_opy_.execute_script(bstack11l1ll_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࡤ࡫ࡸࡦࡥࡸࡸࡴࡸ࠺ࠡࡽࠥࡥࡨࡺࡩࡰࡰࠥ࠾ࠥࠨࡡ࡯ࡰࡲࡸࡦࡺࡥࠣ࠮ࠣࠦࡦࡸࡧࡶ࡯ࡨࡲࡹࡹࠢ࠻ࠢࡾࠦࡩࡧࡴࡢࠤ࠽ࠫ૯") + json.dumps(str(args[0].name) + bstack11l1ll_opy_ (u"ࠢࠡ࠯ࠣࡔࡦࡹࡳࡦࡦࠤࠦ૰")) + bstack11l1ll_opy_ (u"ࠨ࠮ࠣࠦࡱ࡫ࡶࡦ࡮ࠥ࠾ࠥࠨࡩ࡯ࡨࡲࠦࢂࢃࠧ૱"))
        if self.driver_before_scenario:
          bstack1111ll1l1_opy_(bstack1l1l11ll_opy_, bstack11l1ll_opy_ (u"ࠤࡳࡥࡸࡹࡥࡥࠤ૲"))
    except Exception as e:
      logger.debug(bstack11l1ll_opy_ (u"ࠪࡊࡦ࡯࡬ࡦࡦࠣࡸࡴࠦ࡭ࡢࡴ࡮ࠤࡸ࡫ࡳࡴ࡫ࡲࡲࠥࡹࡴࡢࡶࡸࡷࠥ࡯࡮ࠡࡣࡩࡸࡪࡸࠠࡧࡧࡤࡸࡺࡸࡥ࠻ࠢࡾࢁࠬ૳").format(str(e)))
  elif name == bstack11l1ll_opy_ (u"ࠫࡦ࡬ࡴࡦࡴࡢࡪࡪࡧࡴࡶࡴࡨࠫ૴"):
    try:
      bstack1l1l11ll_opy_ = threading.current_thread().bstackSessionDriver if bstack1llll11111_opy_(bstack11l1ll_opy_ (u"ࠬࡨࡳࡵࡣࡦ࡯ࡘ࡫ࡳࡴ࡫ࡲࡲࡉࡸࡩࡷࡧࡵࠫ૵")) else context.browser
      if context.failed is True:
        bstack1l1l1l1l1_opy_ = []
        bstack1l1ll111_opy_ = []
        bstack1lll11llll_opy_ = []
        bstack1ll111l1ll_opy_ = bstack11l1ll_opy_ (u"࠭ࠧ૶")
        try:
          import traceback
          for exc in self.exception_arr:
            bstack1l1l1l1l1_opy_.append(exc.__class__.__name__)
          for exc_tb in self.exc_traceback_arr:
            bstack1lllllll1l_opy_ = traceback.format_tb(exc_tb)
            bstack11l11ll1_opy_ = bstack11l1ll_opy_ (u"ࠧࠡࠩ૷").join(bstack1lllllll1l_opy_)
            bstack1l1ll111_opy_.append(bstack11l11ll1_opy_)
            bstack1lll11llll_opy_.append(bstack1lllllll1l_opy_[-1])
        except Exception as e:
          logger.debug(bstack1ll11llll_opy_.format(str(e)))
        bstack111l1111l_opy_ = bstack11l1ll_opy_ (u"ࠨࠩ૸")
        for i in range(len(bstack1l1l1l1l1_opy_)):
          bstack111l1111l_opy_ += bstack1l1l1l1l1_opy_[i] + bstack1lll11llll_opy_[i] + bstack11l1ll_opy_ (u"ࠩ࡟ࡲࠬૹ")
        bstack1ll111l1ll_opy_ = bstack11l1ll_opy_ (u"ࠪࠤࠬૺ").join(bstack1l1ll111_opy_)
        if not self.driver_before_scenario:
          bstack11lllll1_opy_(context, bstack1ll111l1ll_opy_, bstack11l1ll_opy_ (u"ࠦࡪࡸࡲࡰࡴࠥૻ"))
          bstack1l1ll111l_opy_(getattr(context, bstack11l1ll_opy_ (u"ࠬࡶࡡࡨࡧࠪૼ"), None), bstack11l1ll_opy_ (u"ࠨࡦࡢ࡫࡯ࡩࡩࠨ૽"), bstack111l1111l_opy_)
          bstack1l1l11ll_opy_.execute_script(bstack11l1ll_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰࡥࡥࡹࡧࡦࡹࡹࡵࡲ࠻ࠢࡾࠦࡦࡩࡴࡪࡱࡱࠦ࠿ࠦࠢࡢࡰࡱࡳࡹࡧࡴࡦࠤ࠯ࠤࠧࡧࡲࡨࡷࡰࡩࡳࡺࡳࠣ࠼ࠣࡿࠧࡪࡡࡵࡣࠥ࠾ࠬ૾") + json.dumps(bstack1ll111l1ll_opy_) + bstack11l1ll_opy_ (u"ࠨ࠮ࠣࠦࡱ࡫ࡶࡦ࡮ࠥ࠾ࠥࠨࡥࡳࡴࡲࡶࠧࢃࡽࠨ૿"))
          bstack1111ll1l1_opy_(bstack1l1l11ll_opy_, bstack11l1ll_opy_ (u"ࠤࡩࡥ࡮ࡲࡥࡥࠤ଀"), bstack11l1ll_opy_ (u"ࠥࡗࡴࡳࡥࠡࡵࡦࡩࡳࡧࡲࡪࡱࡶࠤ࡫ࡧࡩ࡭ࡧࡧ࠾ࠥࡢ࡮ࠣଁ") + str(bstack111l1111l_opy_))
          bstack1l1111l1l_opy_ = bstack1111l1l1_opy_(bstack1ll111l1ll_opy_, self.feature.name, logger)
          if (bstack1l1111l1l_opy_ != None):
            bstack1l1ll1lll_opy_.append(bstack1l1111l1l_opy_)
      else:
        if not self.driver_before_scenario:
          bstack11lllll1_opy_(context, bstack11l1ll_opy_ (u"ࠦࡋ࡫ࡡࡵࡷࡵࡩ࠿ࠦࠢଂ") + str(self.feature.name) + bstack11l1ll_opy_ (u"ࠧࠦࡰࡢࡵࡶࡩࡩࠧࠢଃ"), bstack11l1ll_opy_ (u"ࠨࡩ࡯ࡨࡲࠦ଄"))
          bstack1l1ll111l_opy_(getattr(context, bstack11l1ll_opy_ (u"ࠧࡱࡣࡪࡩࠬଅ"), None), bstack11l1ll_opy_ (u"ࠣࡲࡤࡷࡸ࡫ࡤࠣଆ"))
          bstack1l1l11ll_opy_.execute_script(bstack11l1ll_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࡠࡧࡻࡩࡨࡻࡴࡰࡴ࠽ࠤࢀࠨࡡࡤࡶ࡬ࡳࡳࠨ࠺ࠡࠤࡤࡲࡳࡵࡴࡢࡶࡨࠦ࠱ࠦࠢࡢࡴࡪࡹࡲ࡫࡮ࡵࡵࠥ࠾ࠥࢁࠢࡥࡣࡷࡥࠧࡀࠧଇ") + json.dumps(bstack11l1ll_opy_ (u"ࠥࡊࡪࡧࡴࡶࡴࡨ࠾ࠥࠨଈ") + str(self.feature.name) + bstack11l1ll_opy_ (u"ࠦࠥࡶࡡࡴࡵࡨࡨࠦࠨଉ")) + bstack11l1ll_opy_ (u"ࠬ࠲ࠠࠣ࡮ࡨࡺࡪࡲࠢ࠻ࠢࠥ࡭ࡳ࡬࡯ࠣࡿࢀࠫଊ"))
          bstack1111ll1l1_opy_(bstack1l1l11ll_opy_, bstack11l1ll_opy_ (u"࠭ࡰࡢࡵࡶࡩࡩ࠭ଋ"))
          bstack1l1111l1l_opy_ = bstack1111l1l1_opy_(bstack1ll111l1ll_opy_, self.feature.name, logger)
          if (bstack1l1111l1l_opy_ != None):
            bstack1l1ll1lll_opy_.append(bstack1l1111l1l_opy_)
    except Exception as e:
      logger.debug(bstack11l1ll_opy_ (u"ࠧࡇࡣ࡬ࡰࡪࡪࠠࡵࡱࠣࡱࡦࡸ࡫ࠡࡵࡨࡷࡸ࡯࡯࡯ࠢࡶࡸࡦࡺࡵࡴࠢ࡬ࡲࠥࡧࡦࡵࡧࡵࠤ࡫࡫ࡡࡵࡷࡵࡩ࠿ࠦࡻࡾࠩଌ").format(str(e)))
  else:
    bstack1l1ll11l11_opy_(self, name, context, *args)
  if name in [bstack11l1ll_opy_ (u"ࠨࡣࡩࡸࡪࡸ࡟ࡧࡧࡤࡸࡺࡸࡥࠨ଍"), bstack11l1ll_opy_ (u"ࠩࡤࡪࡹ࡫ࡲࡠࡵࡦࡩࡳࡧࡲࡪࡱࠪ଎")]:
    bstack1l1ll11l11_opy_(self, name, context, *args)
    if (name == bstack11l1ll_opy_ (u"ࠪࡥ࡫ࡺࡥࡳࡡࡶࡧࡪࡴࡡࡳ࡫ࡲࠫଏ") and self.driver_before_scenario) or (
            name == bstack11l1ll_opy_ (u"ࠫࡦ࡬ࡴࡦࡴࡢࡪࡪࡧࡴࡶࡴࡨࠫଐ") and not self.driver_before_scenario):
      try:
        bstack1l1l11ll_opy_ = threading.current_thread().bstackSessionDriver if bstack1llll11111_opy_(bstack11l1ll_opy_ (u"ࠬࡨࡳࡵࡣࡦ࡯ࡘ࡫ࡳࡴ࡫ࡲࡲࡉࡸࡩࡷࡧࡵࠫ଑")) else context.browser
        bstack1l1l11ll_opy_.quit()
      except Exception:
        pass
def bstack1l1ll1l111_opy_(config, startdir):
  return bstack11l1ll_opy_ (u"ࠨࡤࡳ࡫ࡹࡩࡷࡀࠠࡼ࠲ࢀࠦ଒").format(bstack11l1ll_opy_ (u"ࠢࡃࡴࡲࡻࡸ࡫ࡲࡔࡶࡤࡧࡰࠨଓ"))
notset = Notset()
def bstack1ll11111l_opy_(self, name: str, default=notset, skip: bool = False):
  global bstack111llllll_opy_
  if str(name).lower() == bstack11l1ll_opy_ (u"ࠨࡦࡵ࡭ࡻ࡫ࡲࠨଔ"):
    return bstack11l1ll_opy_ (u"ࠤࡅࡶࡴࡽࡳࡦࡴࡖࡸࡦࡩ࡫ࠣକ")
  else:
    return bstack111llllll_opy_(self, name, default, skip)
def bstack11llll1l_opy_(item, when):
  global bstack1l1l1l1ll_opy_
  try:
    bstack1l1l1l1ll_opy_(item, when)
  except Exception as e:
    pass
def bstack1ll11111_opy_():
  return
def bstack1ll1lll1l_opy_(type, name, status, reason, bstack11llll11_opy_, bstack1111ll111_opy_):
  bstack11l1l1ll_opy_ = {
    bstack11l1ll_opy_ (u"ࠪࡥࡨࡺࡩࡰࡰࠪଖ"): type,
    bstack11l1ll_opy_ (u"ࠫࡦࡸࡧࡶ࡯ࡨࡲࡹࡹࠧଗ"): {}
  }
  if type == bstack11l1ll_opy_ (u"ࠬࡧ࡮࡯ࡱࡷࡥࡹ࡫ࠧଘ"):
    bstack11l1l1ll_opy_[bstack11l1ll_opy_ (u"࠭ࡡࡳࡩࡸࡱࡪࡴࡴࡴࠩଙ")][bstack11l1ll_opy_ (u"ࠧ࡭ࡧࡹࡩࡱ࠭ଚ")] = bstack11llll11_opy_
    bstack11l1l1ll_opy_[bstack11l1ll_opy_ (u"ࠨࡣࡵ࡫ࡺࡳࡥ࡯ࡶࡶࠫଛ")][bstack11l1ll_opy_ (u"ࠩࡧࡥࡹࡧࠧଜ")] = json.dumps(str(bstack1111ll111_opy_))
  if type == bstack11l1ll_opy_ (u"ࠪࡷࡪࡺࡓࡦࡵࡶ࡭ࡴࡴࡎࡢ࡯ࡨࠫଝ"):
    bstack11l1l1ll_opy_[bstack11l1ll_opy_ (u"ࠫࡦࡸࡧࡶ࡯ࡨࡲࡹࡹࠧଞ")][bstack11l1ll_opy_ (u"ࠬࡴࡡ࡮ࡧࠪଟ")] = name
  if type == bstack11l1ll_opy_ (u"࠭ࡳࡦࡶࡖࡩࡸࡹࡩࡰࡰࡖࡸࡦࡺࡵࡴࠩଠ"):
    bstack11l1l1ll_opy_[bstack11l1ll_opy_ (u"ࠧࡢࡴࡪࡹࡲ࡫࡮ࡵࡵࠪଡ")][bstack11l1ll_opy_ (u"ࠨࡵࡷࡥࡹࡻࡳࠨଢ")] = status
    if status == bstack11l1ll_opy_ (u"ࠩࡩࡥ࡮ࡲࡥࡥࠩଣ"):
      bstack11l1l1ll_opy_[bstack11l1ll_opy_ (u"ࠪࡥࡷ࡭ࡵ࡮ࡧࡱࡸࡸ࠭ତ")][bstack11l1ll_opy_ (u"ࠫࡷ࡫ࡡࡴࡱࡱࠫଥ")] = json.dumps(str(reason))
  bstack1ll11l111l_opy_ = bstack11l1ll_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࡣࡪࡾࡥࡤࡷࡷࡳࡷࡀࠠࡼࡿࠪଦ").format(json.dumps(bstack11l1l1ll_opy_))
  return bstack1ll11l111l_opy_
def bstack11ll1l11_opy_(driver_command, response):
    if driver_command == bstack11l1ll_opy_ (u"࠭ࡳࡤࡴࡨࡩࡳࡹࡨࡰࡶࠪଧ"):
        bstack11l1ll11_opy_.bstack1lll11ll_opy_({
            bstack11l1ll_opy_ (u"ࠧࡪ࡯ࡤ࡫ࡪ࠭ନ"): response[bstack11l1ll_opy_ (u"ࠨࡸࡤࡰࡺ࡫ࠧ଩")],
            bstack11l1ll_opy_ (u"ࠩࡷࡩࡸࡺ࡟ࡳࡷࡱࡣࡺࡻࡩࡥࠩପ"): bstack11l1ll11_opy_.current_test_uuid()
        })
def bstack1lllll11l_opy_(item, call, rep):
  global bstack1lll11l111_opy_
  global bstack11l1l1111_opy_
  global bstack1lll1111l1_opy_
  name = bstack11l1ll_opy_ (u"ࠪࠫଫ")
  try:
    if rep.when == bstack11l1ll_opy_ (u"ࠫࡨࡧ࡬࡭ࠩବ"):
      bstack111l1l11_opy_ = threading.current_thread().bstackSessionId
      try:
        if not bstack1lll1111l1_opy_:
          name = str(rep.nodeid)
          bstack1l111lll_opy_ = bstack1ll1lll1l_opy_(bstack11l1ll_opy_ (u"ࠬࡹࡥࡵࡕࡨࡷࡸ࡯࡯࡯ࡐࡤࡱࡪ࠭ଭ"), name, bstack11l1ll_opy_ (u"࠭ࠧମ"), bstack11l1ll_opy_ (u"ࠧࠨଯ"), bstack11l1ll_opy_ (u"ࠨࠩର"), bstack11l1ll_opy_ (u"ࠩࠪ଱"))
          threading.current_thread().bstack1lllll1l1l_opy_ = name
          for driver in bstack11l1l1111_opy_:
            if bstack111l1l11_opy_ == driver.session_id:
              driver.execute_script(bstack1l111lll_opy_)
      except Exception as e:
        logger.debug(bstack11l1ll_opy_ (u"ࠪࡉࡷࡸ࡯ࡳࠢ࡬ࡲࠥࡹࡥࡵࡶ࡬ࡲ࡬ࠦࡳࡦࡵࡶ࡭ࡴࡴࡎࡢ࡯ࡨࠤ࡫ࡵࡲࠡࡲࡼࡸࡪࡹࡴ࠮ࡤࡧࡨࠥࡹࡥࡴࡵ࡬ࡳࡳࡀࠠࡼࡿࠪଲ").format(str(e)))
      try:
        bstack111l1111_opy_(rep.outcome.lower())
        if rep.outcome.lower() != bstack11l1ll_opy_ (u"ࠫࡸࡱࡩࡱࡲࡨࡨࠬଳ"):
          status = bstack11l1ll_opy_ (u"ࠬ࡬ࡡࡪ࡮ࡨࡨࠬ଴") if rep.outcome.lower() == bstack11l1ll_opy_ (u"࠭ࡦࡢ࡫࡯ࡩࡩ࠭ଵ") else bstack11l1ll_opy_ (u"ࠧࡱࡣࡶࡷࡪࡪࠧଶ")
          reason = bstack11l1ll_opy_ (u"ࠨࠩଷ")
          if status == bstack11l1ll_opy_ (u"ࠩࡩࡥ࡮ࡲࡥࡥࠩସ"):
            reason = rep.longrepr.reprcrash.message
            if (not threading.current_thread().bstackTestErrorMessages):
              threading.current_thread().bstackTestErrorMessages = []
            threading.current_thread().bstackTestErrorMessages.append(reason)
          level = bstack11l1ll_opy_ (u"ࠪ࡭ࡳ࡬࡯ࠨହ") if status == bstack11l1ll_opy_ (u"ࠫࡵࡧࡳࡴࡧࡧࠫ଺") else bstack11l1ll_opy_ (u"ࠬ࡫ࡲࡳࡱࡵࠫ଻")
          data = name + bstack11l1ll_opy_ (u"࠭ࠠࡱࡣࡶࡷࡪࡪࠡࠨ଼") if status == bstack11l1ll_opy_ (u"ࠧࡱࡣࡶࡷࡪࡪࠧଽ") else name + bstack11l1ll_opy_ (u"ࠨࠢࡩࡥ࡮ࡲࡥࡥࠣࠣࠫା") + reason
          bstack11l1l11ll_opy_ = bstack1ll1lll1l_opy_(bstack11l1ll_opy_ (u"ࠩࡤࡲࡳࡵࡴࡢࡶࡨࠫି"), bstack11l1ll_opy_ (u"ࠪࠫୀ"), bstack11l1ll_opy_ (u"ࠫࠬୁ"), bstack11l1ll_opy_ (u"ࠬ࠭ୂ"), level, data)
          for driver in bstack11l1l1111_opy_:
            if bstack111l1l11_opy_ == driver.session_id:
              driver.execute_script(bstack11l1l11ll_opy_)
      except Exception as e:
        logger.debug(bstack11l1ll_opy_ (u"࠭ࡅࡳࡴࡲࡶࠥ࡯࡮ࠡࡵࡨࡸࡹ࡯࡮ࡨࠢࡶࡩࡸࡹࡩࡰࡰࠣࡧࡴࡴࡴࡦࡺࡷࠤ࡫ࡵࡲࠡࡲࡼࡸࡪࡹࡴ࠮ࡤࡧࡨࠥࡹࡥࡴࡵ࡬ࡳࡳࡀࠠࡼࡿࠪୃ").format(str(e)))
  except Exception as e:
    logger.debug(bstack11l1ll_opy_ (u"ࠧࡆࡴࡵࡳࡷࠦࡩ࡯ࠢࡪࡩࡹࡺࡩ࡯ࡩࠣࡷࡹࡧࡴࡦࠢ࡬ࡲࠥࡶࡹࡵࡧࡶࡸ࠲ࡨࡤࡥࠢࡷࡩࡸࡺࠠࡴࡶࡤࡸࡺࡹ࠺ࠡࡽࢀࠫୄ").format(str(e)))
  bstack1lll11l111_opy_(item, call, rep)
def bstack1l1lllll1_opy_(framework_name):
  global bstack11ll11ll1_opy_
  global bstack1111llll1_opy_
  global bstack1lll11l11_opy_
  bstack11ll11ll1_opy_ = framework_name
  logger.info(bstack1111l11l1_opy_.format(bstack11ll11ll1_opy_.split(bstack11l1ll_opy_ (u"ࠨ࠯ࠪ୅"))[0]))
  try:
    from selenium import webdriver
    from selenium.webdriver.common.service import Service
    from selenium.webdriver.remote.webdriver import WebDriver
    if bstack1l1lll1lll_opy_:
      Service.start = bstack11lll1ll1_opy_
      Service.stop = bstack1111llll_opy_
      webdriver.Remote.get = bstack1l1l111l1_opy_
      WebDriver.close = bstack1ll1ll1l11_opy_
      WebDriver.quit = bstack1ll1l11lll_opy_
      webdriver.Remote.__init__ = bstack11lllll11_opy_
      WebDriver.getAccessibilityResults = getAccessibilityResults
      WebDriver.bstack1111l1111_opy_ = getAccessibilityResults
      WebDriver.getAccessibilityResultsSummary = getAccessibilityResultsSummary
      WebDriver.bstack1ll1lll11_opy_ = getAccessibilityResultsSummary
    if not bstack1l1lll1lll_opy_ and bstack11l1ll11_opy_.on():
      webdriver.Remote.__init__ = bstack1ll1l11l_opy_
    if bstack11l1ll11_opy_.on():
      WebDriver.execute = bstack1l1lll11l1_opy_
    bstack1111llll1_opy_ = True
  except Exception as e:
    pass
  bstack1lll1l11l1_opy_()
  if not bstack1111llll1_opy_:
    bstack1l11lll1_opy_(bstack11l1ll_opy_ (u"ࠤࡓࡥࡨࡱࡡࡨࡧࡶࠤࡳࡵࡴࠡ࡫ࡱࡷࡹࡧ࡬࡭ࡧࡧࠦ୆"), bstack1ll1l1lll1_opy_)
  if bstack111111lll_opy_():
    try:
      from selenium.webdriver.remote.remote_connection import RemoteConnection
      RemoteConnection._get_proxy_url = bstack1ll1llll11_opy_
    except Exception as e:
      logger.error(bstack1ll1l1111l_opy_.format(str(e)))
  if bstack1lllll11_opy_():
    bstack111l1llll_opy_(CONFIG, logger)
  if (bstack11l1ll_opy_ (u"ࠪࡶࡴࡨ࡯ࡵࠩେ") in str(framework_name).lower()):
    try:
      from robot import run_cli
      from robot.output import Output
      from robot.running.status import TestStatus
      from pabot.pabot import QueueItem
      from pabot import pabot
      try:
        from SeleniumLibrary.keywords.webdrivertools.webdrivertools import WebDriverCreator
        WebDriverCreator._get_ff_profile = bstack1lll1ll1l1_opy_
        from SeleniumLibrary.keywords.webdrivertools.webdrivertools import WebDriverCache
        WebDriverCache.close = bstack1l11l111l_opy_
      except Exception as e:
        logger.warn(bstack11l1l1ll1_opy_ + str(e))
      try:
        from AppiumLibrary.utils.applicationcache import ApplicationCache
        ApplicationCache.close = bstack1l1lll11l_opy_
      except Exception as e:
        logger.debug(bstack11lll1l1_opy_ + str(e))
    except Exception as e:
      bstack1l11lll1_opy_(e, bstack11l1l1ll1_opy_)
    Output.end_test = bstack1lllll1ll_opy_
    TestStatus.__init__ = bstack1llllll1l1_opy_
    QueueItem.__init__ = bstack111l11ll1_opy_
    pabot._create_items = bstack1ll1lll1l1_opy_
    try:
      from pabot import __version__ as bstack1lll1l111_opy_
      if version.parse(bstack1lll1l111_opy_) >= version.parse(bstack11l1ll_opy_ (u"ࠫ࠷࠴࠱࠶࠰࠳ࠫୈ")):
        pabot._run = bstack1ll1l11ll1_opy_
      elif version.parse(bstack1lll1l111_opy_) >= version.parse(bstack11l1ll_opy_ (u"ࠬ࠸࠮࠲࠵࠱࠴ࠬ୉")):
        pabot._run = bstack1l1l1ll11_opy_
      else:
        pabot._run = bstack1l1l1lll_opy_
    except Exception as e:
      pabot._run = bstack1l1l1lll_opy_
    pabot._create_command_for_execution = bstack11l11ll11_opy_
    pabot._report_results = bstack1ll1l1ll_opy_
  if bstack11l1ll_opy_ (u"࠭ࡢࡦࡪࡤࡺࡪ࠭୊") in str(framework_name).lower():
    try:
      from behave.runner import Runner
      from behave.model import Step
    except Exception as e:
      bstack1l11lll1_opy_(e, bstack1ll1ll1ll_opy_)
    Runner.run_hook = bstack1l1lll111_opy_
    Step.run = bstack11ll1ll1l_opy_
  if bstack11l1ll_opy_ (u"ࠧࡱࡻࡷࡩࡸࡺࠧୋ") in str(framework_name).lower():
    if not bstack1l1lll1lll_opy_:
      return
    try:
      from pytest_selenium import pytest_selenium
      from _pytest.config import Config
      pytest_selenium.pytest_report_header = bstack1l1ll1l111_opy_
      from pytest_selenium.drivers import browserstack
      browserstack.pytest_selenium_runtest_makereport = bstack1ll11111_opy_
      Config.getoption = bstack1ll11111l_opy_
    except Exception as e:
      pass
    try:
      from pytest_bdd import reporting
      reporting.runtest_makereport = bstack1lllll11l_opy_
    except Exception as e:
      pass
def bstack1l1lll111l_opy_():
  global CONFIG
  if bstack11l1ll_opy_ (u"ࠨࡲࡤࡶࡦࡲ࡬ࡦ࡮ࡶࡔࡪࡸࡐ࡭ࡣࡷࡪࡴࡸ࡭ࠨୌ") in CONFIG and int(CONFIG[bstack11l1ll_opy_ (u"ࠩࡳࡥࡷࡧ࡬࡭ࡧ࡯ࡷࡕ࡫ࡲࡑ࡮ࡤࡸ࡫ࡵࡲ࡮୍ࠩ")]) > 1:
    logger.warn(bstack1l1111111_opy_)
def bstack1l11ll111_opy_(arg, bstack1ll1ll1lll_opy_, bstack1llll111l_opy_=None):
  global CONFIG
  global bstack1lll1l1l1_opy_
  global bstack1ll11ll111_opy_
  global bstack1l1lll1lll_opy_
  global bstack1ll1l11l1_opy_
  bstack1ll1llll_opy_ = bstack11l1ll_opy_ (u"ࠪࡴࡾࡺࡥࡴࡶࠪ୎")
  if bstack1ll1ll1lll_opy_ and isinstance(bstack1ll1ll1lll_opy_, str):
    bstack1ll1ll1lll_opy_ = eval(bstack1ll1ll1lll_opy_)
  CONFIG = bstack1ll1ll1lll_opy_[bstack11l1ll_opy_ (u"ࠫࡈࡕࡎࡇࡋࡊࠫ୏")]
  bstack1lll1l1l1_opy_ = bstack1ll1ll1lll_opy_[bstack11l1ll_opy_ (u"ࠬࡎࡕࡃࡡࡘࡖࡑ࠭୐")]
  bstack1ll11ll111_opy_ = bstack1ll1ll1lll_opy_[bstack11l1ll_opy_ (u"࠭ࡉࡔࡡࡄࡔࡕࡥࡁࡖࡖࡒࡑࡆ࡚ࡅࠨ୑")]
  bstack1l1lll1lll_opy_ = bstack1ll1ll1lll_opy_[bstack11l1ll_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡁࡖࡖࡒࡑࡆ࡚ࡉࡐࡐࠪ୒")]
  bstack1ll1l11l1_opy_.bstack1l1ll1ll1_opy_(bstack11l1ll_opy_ (u"ࠨࡤࡶࡸࡦࡩ࡫ࡠࡵࡨࡷࡸ࡯࡯࡯ࠩ୓"), bstack1l1lll1lll_opy_)
  os.environ[bstack11l1ll_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡈࡕࡅࡒࡋࡗࡐࡔࡎࠫ୔")] = bstack1ll1llll_opy_
  os.environ[bstack11l1ll_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡆࡓࡓࡌࡉࡈࠩ୕")] = json.dumps(CONFIG)
  os.environ[bstack11l1ll_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡌ࡚ࡈ࡟ࡖࡔࡏࠫୖ")] = bstack1lll1l1l1_opy_
  os.environ[bstack11l1ll_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣࡎ࡙࡟ࡂࡒࡓࡣࡆ࡛ࡔࡐࡏࡄࡘࡊ࠭ୗ")] = str(bstack1ll11ll111_opy_)
  os.environ[bstack11l1ll_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤࡖ࡙ࡕࡇࡖࡘࡤࡖࡌࡖࡉࡌࡒࠬ୘")] = str(True)
  if bstack1lllll1lll_opy_(arg, [bstack11l1ll_opy_ (u"ࠧ࠮ࡰࠪ୙"), bstack11l1ll_opy_ (u"ࠨ࠯࠰ࡲࡺࡳࡰࡳࡱࡦࡩࡸࡹࡥࡴࠩ୚")]) != -1:
    os.environ[bstack11l1ll_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡒ࡜ࡘࡊ࡙ࡔࡠࡒࡄࡖࡆࡒࡌࡆࡎࠪ୛")] = str(True)
  if len(sys.argv) <= 1:
    logger.critical(bstack1ll1ll11_opy_)
    return
  bstack1ll11lll_opy_()
  global bstack1ll1llllll_opy_
  global bstack111lll111_opy_
  global bstack1l1111ll_opy_
  global bstack1llll1ll_opy_
  global bstack11l111l11_opy_
  global bstack1lll11l11_opy_
  global bstack1ll11l1ll1_opy_
  arg.append(bstack11l1ll_opy_ (u"ࠥ࠱࡜ࠨଡ଼"))
  arg.append(bstack11l1ll_opy_ (u"ࠦ࡮࡭࡮ࡰࡴࡨ࠾ࡒࡵࡤࡶ࡮ࡨࠤࡦࡲࡲࡦࡣࡧࡽࠥ࡯࡭ࡱࡱࡵࡸࡪࡪ࠺ࡱࡻࡷࡩࡸࡺ࠮ࡑࡻࡷࡩࡸࡺࡗࡢࡴࡱ࡭ࡳ࡭ࠢଢ଼"))
  arg.append(bstack11l1ll_opy_ (u"ࠧ࠳ࡗࠣ୞"))
  arg.append(bstack11l1ll_opy_ (u"ࠨࡩࡨࡰࡲࡶࡪࡀࡔࡩࡧࠣ࡬ࡴࡵ࡫ࡪ࡯ࡳࡰࠧୟ"))
  global bstack1l11l11ll_opy_
  global bstack1l11ll1ll_opy_
  global bstack111l111l1_opy_
  global bstack111l111ll_opy_
  global bstack111l11111_opy_
  global bstack1l11lllll_opy_
  global bstack1ll111ll11_opy_
  global bstack11l111111_opy_
  global bstack1llll1111l_opy_
  global bstack111llllll_opy_
  global bstack1l1l1l1ll_opy_
  global bstack1lll11l111_opy_
  try:
    from selenium import webdriver
    from selenium.webdriver.remote.webdriver import WebDriver
    bstack1l11l11ll_opy_ = webdriver.Remote.__init__
    bstack1l11ll1ll_opy_ = WebDriver.quit
    bstack1ll111ll11_opy_ = WebDriver.close
    bstack11l111111_opy_ = WebDriver.get
  except Exception as e:
    pass
  if bstack11111llll_opy_(CONFIG) and bstack1l1l11lll_opy_():
    if bstack1lll1ll1l_opy_() < version.parse(bstack11l1lll11_opy_):
      logger.error(bstack11l111lll_opy_.format(bstack1lll1ll1l_opy_()))
    else:
      try:
        from selenium.webdriver.remote.remote_connection import RemoteConnection
        bstack1llll1111l_opy_ = RemoteConnection._get_proxy_url
      except Exception as e:
        logger.error(bstack1ll1l1111l_opy_.format(str(e)))
  try:
    from _pytest.config import Config
    bstack111llllll_opy_ = Config.getoption
    from _pytest import runner
    bstack1l1l1l1ll_opy_ = runner._update_current_test_var
  except Exception as e:
    logger.warn(e, bstack1lll11ll1l_opy_)
  try:
    from pytest_bdd import reporting
    bstack1lll11l111_opy_ = reporting.runtest_makereport
  except Exception as e:
    logger.debug(bstack11l1ll_opy_ (u"ࠧࡑ࡮ࡨࡥࡸ࡫ࠠࡪࡰࡶࡸࡦࡲ࡬ࠡࡲࡼࡸࡪࡹࡴ࠮ࡤࡧࡨࠥࡺ࡯ࠡࡴࡸࡲࠥࡶࡹࡵࡧࡶࡸ࠲ࡨࡤࡥࠢࡷࡩࡸࡺࡳࠨୠ"))
  bstack1l1111ll_opy_ = CONFIG.get(bstack11l1ll_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡕࡷࡥࡨࡱࡌࡰࡥࡤࡰࡔࡶࡴࡪࡱࡱࡷࠬୡ"), {}).get(bstack11l1ll_opy_ (u"ࠩ࡯ࡳࡨࡧ࡬ࡊࡦࡨࡲࡹ࡯ࡦࡪࡧࡵࠫୢ"))
  bstack1ll11l1ll1_opy_ = True
  bstack1l1lllll1_opy_(bstack1ll1ll1ll1_opy_)
  os.environ[bstack11l1ll_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡘࡗࡊࡘࡎࡂࡏࡈࠫୣ")] = CONFIG[bstack11l1ll_opy_ (u"ࠫࡺࡹࡥࡳࡐࡤࡱࡪ࠭୤")]
  os.environ[bstack11l1ll_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣࡆࡉࡃࡆࡕࡖࡣࡐࡋ࡙ࠨ୥")] = CONFIG[bstack11l1ll_opy_ (u"࠭ࡡࡤࡥࡨࡷࡸࡑࡥࡺࠩ୦")]
  os.environ[bstack11l1ll_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡁࡖࡖࡒࡑࡆ࡚ࡉࡐࡐࠪ୧")] = bstack1l1lll1lll_opy_.__str__()
  from _pytest.config import main as bstack1l1lll1l_opy_
  bstack1l1lll1l_opy_(arg)
  if bstack11l1ll_opy_ (u"ࠨࡤࡶࡸࡦࡩ࡫ࡠࡧࡵࡶࡴࡸ࡟࡭࡫ࡶࡸࠬ୨") in multiprocessing.current_process().__dict__.keys():
    for bstack1l111l1ll_opy_ in multiprocessing.current_process().bstack_error_list:
      bstack1llll111l_opy_.append(bstack1l111l1ll_opy_)
def bstack1ll11lllll_opy_(arg):
  bstack1l1lllll1_opy_(bstack111111ll1_opy_)
  os.environ[bstack11l1ll_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡋࡖࡣࡆࡖࡐࡠࡃࡘࡘࡔࡓࡁࡕࡇࠪ୩")] = str(bstack1ll11ll111_opy_)
  from behave.__main__ import main as bstack1l11llll_opy_
  bstack1l11llll_opy_(arg)
def bstack1l1llll1ll_opy_():
  logger.info(bstack11l1111l1_opy_)
  import argparse
  parser = argparse.ArgumentParser()
  parser.add_argument(bstack11l1ll_opy_ (u"ࠪࡷࡪࡺࡵࡱࠩ୪"), help=bstack11l1ll_opy_ (u"ࠫࡌ࡫࡮ࡦࡴࡤࡸࡪࠦࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࠥࡩ࡯࡯ࡨ࡬࡫ࠬ୫"))
  parser.add_argument(bstack11l1ll_opy_ (u"ࠬ࠳ࡵࠨ୬"), bstack11l1ll_opy_ (u"࠭࠭࠮ࡷࡶࡩࡷࡴࡡ࡮ࡧࠪ୭"), help=bstack11l1ll_opy_ (u"࡚ࠧࡱࡸࡶࠥࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࠤࡺࡹࡥࡳࡰࡤࡱࡪ࠭୮"))
  parser.add_argument(bstack11l1ll_opy_ (u"ࠨ࠯࡮ࠫ୯"), bstack11l1ll_opy_ (u"ࠩ࠰࠱ࡰ࡫ࡹࠨ୰"), help=bstack11l1ll_opy_ (u"ࠪ࡝ࡴࡻࡲࠡࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱࠠࡢࡥࡦࡩࡸࡹࠠ࡬ࡧࡼࠫୱ"))
  parser.add_argument(bstack11l1ll_opy_ (u"ࠫ࠲࡬ࠧ୲"), bstack11l1ll_opy_ (u"ࠬ࠳࠭ࡧࡴࡤࡱࡪࡽ࡯ࡳ࡭ࠪ୳"), help=bstack11l1ll_opy_ (u"࡙࠭ࡰࡷࡵࠤࡹ࡫ࡳࡵࠢࡩࡶࡦࡳࡥࡸࡱࡵ࡯ࠬ୴"))
  bstack111llll1l_opy_ = parser.parse_args()
  try:
    bstack1lll1l1lll_opy_ = bstack11l1ll_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠴ࡧࡦࡰࡨࡶ࡮ࡩ࠮ࡺ࡯࡯࠲ࡸࡧ࡭ࡱ࡮ࡨࠫ୵")
    if bstack111llll1l_opy_.framework and bstack111llll1l_opy_.framework not in (bstack11l1ll_opy_ (u"ࠨࡲࡼࡸ࡭ࡵ࡮ࠨ୶"), bstack11l1ll_opy_ (u"ࠩࡳࡽࡹ࡮࡯࡯࠵ࠪ୷")):
      bstack1lll1l1lll_opy_ = bstack11l1ll_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬࠰ࡩࡶࡦࡳࡥࡸࡱࡵ࡯࠳ࡿ࡭࡭࠰ࡶࡥࡲࡶ࡬ࡦࠩ୸")
    bstack1l1l1l11_opy_ = os.path.join(os.path.dirname(os.path.realpath(__file__)), bstack1lll1l1lll_opy_)
    bstack11111111l_opy_ = open(bstack1l1l1l11_opy_, bstack11l1ll_opy_ (u"ࠫࡷ࠭୹"))
    bstack11lll1l11_opy_ = bstack11111111l_opy_.read()
    bstack11111111l_opy_.close()
    if bstack111llll1l_opy_.username:
      bstack11lll1l11_opy_ = bstack11lll1l11_opy_.replace(bstack11l1ll_opy_ (u"ࠬ࡟ࡏࡖࡔࡢ࡙ࡘࡋࡒࡏࡃࡐࡉࠬ୺"), bstack111llll1l_opy_.username)
    if bstack111llll1l_opy_.key:
      bstack11lll1l11_opy_ = bstack11lll1l11_opy_.replace(bstack11l1ll_opy_ (u"࡙࠭ࡐࡗࡕࡣࡆࡉࡃࡆࡕࡖࡣࡐࡋ࡙ࠨ୻"), bstack111llll1l_opy_.key)
    if bstack111llll1l_opy_.framework:
      bstack11lll1l11_opy_ = bstack11lll1l11_opy_.replace(bstack11l1ll_opy_ (u"࡚ࠧࡑࡘࡖࡤࡌࡒࡂࡏࡈ࡛ࡔࡘࡋࠨ୼"), bstack111llll1l_opy_.framework)
    file_name = bstack11l1ll_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠮ࡺ࡯࡯ࠫ୽")
    file_path = os.path.abspath(file_name)
    bstack11llll111_opy_ = open(file_path, bstack11l1ll_opy_ (u"ࠩࡺࠫ୾"))
    bstack11llll111_opy_.write(bstack11lll1l11_opy_)
    bstack11llll111_opy_.close()
    logger.info(bstack1lll1lll_opy_)
    try:
      os.environ[bstack11l1ll_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡉࡖࡆࡓࡅࡘࡑࡕࡏࠬ୿")] = bstack111llll1l_opy_.framework if bstack111llll1l_opy_.framework != None else bstack11l1ll_opy_ (u"ࠦࠧ஀")
      config = yaml.safe_load(bstack11lll1l11_opy_)
      config[bstack11l1ll_opy_ (u"ࠬࡹ࡯ࡶࡴࡦࡩࠬ஁")] = bstack11l1ll_opy_ (u"࠭ࡰࡺࡶ࡫ࡳࡳ࠳ࡳࡦࡶࡸࡴࠬஂ")
      bstack111ll11ll_opy_(bstack1111l1l1l_opy_, config)
    except Exception as e:
      logger.debug(bstack1111ll1l_opy_.format(str(e)))
  except Exception as e:
    logger.error(bstack11l111l1_opy_.format(str(e)))
def bstack111ll11ll_opy_(bstack1l1lll1l1l_opy_, config, bstack1lllllll11_opy_={}):
  global bstack1l1lll1lll_opy_
  global bstack11ll111ll_opy_
  if not config:
    return
  bstack11ll1l1ll_opy_ = bstack11l1ll1l1_opy_ if not bstack1l1lll1lll_opy_ else (
    bstack1llll1lll_opy_ if bstack11l1ll_opy_ (u"ࠧࡢࡲࡳࠫஃ") in config else bstack1lll111l_opy_)
  data = {
    bstack11l1ll_opy_ (u"ࠨࡷࡶࡩࡷࡔࡡ࡮ࡧࠪ஄"): config[bstack11l1ll_opy_ (u"ࠩࡸࡷࡪࡸࡎࡢ࡯ࡨࠫஅ")],
    bstack11l1ll_opy_ (u"ࠪࡥࡨࡩࡥࡴࡵࡎࡩࡾ࠭ஆ"): config[bstack11l1ll_opy_ (u"ࠫࡦࡩࡣࡦࡵࡶࡏࡪࡿࠧஇ")],
    bstack11l1ll_opy_ (u"ࠬ࡫ࡶࡦࡰࡷࡣࡹࡿࡰࡦࠩஈ"): bstack1l1lll1l1l_opy_,
    bstack11l1ll_opy_ (u"࠭ࡤࡦࡶࡨࡧࡹ࡫ࡤࡇࡴࡤࡱࡪࡽ࡯ࡳ࡭ࠪஉ"): os.environ.get(bstack11l1ll_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡆࡓࡃࡐࡉ࡜ࡕࡒࡌࠩஊ"), bstack11ll111ll_opy_),
    bstack11l1ll_opy_ (u"ࠨࡤࡸ࡭ࡱࡪ࡟ࡩࡣࡶ࡬ࡪࡪ࡟ࡪࡦࠪ஋"): bstack111l1ll1_opy_,
    bstack11l1ll_opy_ (u"ࠩࡲࡴࡹ࡯࡭ࡢ࡮ࡢ࡬ࡺࡨ࡟ࡶࡴ࡯ࠫ஌"): bstack1llll1l1l1_opy_(),
    bstack11l1ll_opy_ (u"ࠪࡩࡻ࡫࡮ࡵࡡࡳࡶࡴࡶࡥࡳࡶ࡬ࡩࡸ࠭஍"): {
      bstack11l1ll_opy_ (u"ࠫࡱࡧ࡮ࡨࡷࡤ࡫ࡪࡥࡦࡳࡣࡰࡩࡼࡵࡲ࡬ࠩஎ"): str(config[bstack11l1ll_opy_ (u"ࠬࡹ࡯ࡶࡴࡦࡩࠬஏ")]) if bstack11l1ll_opy_ (u"࠭ࡳࡰࡷࡵࡧࡪ࠭ஐ") in config else bstack11l1ll_opy_ (u"ࠢࡶࡰ࡮ࡲࡴࡽ࡮ࠣ஑"),
      bstack11l1ll_opy_ (u"ࠨࡴࡨࡪࡪࡸࡲࡦࡴࠪஒ"): bstack11ll11ll_opy_(os.getenv(bstack11l1ll_opy_ (u"ࠤࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡈࡕࡅࡒࡋࡗࡐࡔࡎࠦஓ"), bstack11l1ll_opy_ (u"ࠥࠦஔ"))),
      bstack11l1ll_opy_ (u"ࠫࡱࡧ࡮ࡨࡷࡤ࡫ࡪ࠭க"): bstack11l1ll_opy_ (u"ࠬࡶࡹࡵࡪࡲࡲࠬ஖"),
      bstack11l1ll_opy_ (u"࠭ࡰࡳࡱࡧࡹࡨࡺࠧ஗"): bstack11ll1l1ll_opy_,
      bstack11l1ll_opy_ (u"ࠧࡣࡷ࡬ࡰࡩࡔࡡ࡮ࡧࠪ஘"): config[bstack11l1ll_opy_ (u"ࠨࡤࡸ࡭ࡱࡪࡎࡢ࡯ࡨࠫங")] if config[bstack11l1ll_opy_ (u"ࠩࡥࡹ࡮ࡲࡤࡏࡣࡰࡩࠬச")] else bstack11l1ll_opy_ (u"ࠥࡹࡳࡱ࡮ࡰࡹࡱࠦ஛"),
      bstack11l1ll_opy_ (u"ࠫࡧࡻࡩ࡭ࡦࡌࡨࡪࡴࡴࡪࡨ࡬ࡩࡷ࠭ஜ"): str(config[bstack11l1ll_opy_ (u"ࠬࡨࡵࡪ࡮ࡧࡍࡩ࡫࡮ࡵ࡫ࡩ࡭ࡪࡸࠧ஝")]) if bstack11l1ll_opy_ (u"࠭ࡢࡶ࡫࡯ࡨࡎࡪࡥ࡯ࡶ࡬ࡪ࡮࡫ࡲࠨஞ") in config else bstack11l1ll_opy_ (u"ࠢࡶࡰ࡮ࡲࡴࡽ࡮ࠣட"),
      bstack11l1ll_opy_ (u"ࠨࡱࡶࠫ஠"): sys.platform,
      bstack11l1ll_opy_ (u"ࠩ࡫ࡳࡸࡺ࡮ࡢ࡯ࡨࠫ஡"): socket.gethostname()
    }
  }
  update(data[bstack11l1ll_opy_ (u"ࠪࡩࡻ࡫࡮ࡵࡡࡳࡶࡴࡶࡥࡳࡶ࡬ࡩࡸ࠭஢")], bstack1lllllll11_opy_)
  try:
    response = bstack1111l1lll_opy_(bstack11l1ll_opy_ (u"ࠫࡕࡕࡓࡕࠩண"), bstack1ll111l111_opy_(bstack1ll11l11ll_opy_), data, {
      bstack11l1ll_opy_ (u"ࠬࡧࡵࡵࡪࠪத"): (config[bstack11l1ll_opy_ (u"࠭ࡵࡴࡧࡵࡒࡦࡳࡥࠨ஥")], config[bstack11l1ll_opy_ (u"ࠧࡢࡥࡦࡩࡸࡹࡋࡦࡻࠪ஦")])
    })
    if response:
      logger.debug(bstack1ll11l11_opy_.format(bstack1l1lll1l1l_opy_, str(response.json())))
  except Exception as e:
    logger.debug(bstack1ll111ll1l_opy_.format(str(e)))
def bstack11ll11ll_opy_(framework):
  return bstack11l1ll_opy_ (u"ࠣࡽࢀ࠱ࡵࡿࡴࡩࡱࡱࡥ࡬࡫࡮ࡵ࠱ࡾࢁࠧ஧").format(str(framework), __version__) if framework else bstack11l1ll_opy_ (u"ࠤࡳࡽࡹ࡮࡯࡯ࡣࡪࡩࡳࡺ࠯ࡼࡿࠥந").format(
    __version__)
def bstack1ll11lll_opy_():
  global CONFIG
  if bool(CONFIG):
    return
  try:
    bstack1llll1ll1l_opy_()
    logger.debug(bstack11llll1ll_opy_.format(str(CONFIG)))
    bstack1lll111l1_opy_()
    bstack11111ll1l_opy_()
  except Exception as e:
    logger.error(bstack11l1ll_opy_ (u"ࠥࡊࡦ࡯࡬ࡦࡦࠣࡸࡴࠦࡳࡦࡶࡸࡴ࠱ࠦࡥࡳࡴࡲࡶ࠿ࠦࠢன") + str(e))
    sys.exit(1)
  sys.excepthook = bstack11ll111l_opy_
  atexit.register(bstack1lllll111l_opy_)
  signal.signal(signal.SIGINT, bstack1l1ll1ll11_opy_)
  signal.signal(signal.SIGTERM, bstack1l1ll1ll11_opy_)
def bstack11ll111l_opy_(exctype, value, traceback):
  global bstack11l1l1111_opy_
  try:
    for driver in bstack11l1l1111_opy_:
      bstack1111ll1l1_opy_(driver, bstack11l1ll_opy_ (u"ࠫ࡫ࡧࡩ࡭ࡧࡧࠫப"), bstack11l1ll_opy_ (u"࡙ࠧࡥࡴࡵ࡬ࡳࡳࠦࡦࡢ࡫࡯ࡩࡩࠦࡷࡪࡶ࡫࠾ࠥࡢ࡮ࠣ஫") + str(value))
  except Exception:
    pass
  bstack1lll11l1l_opy_(value)
  sys.__excepthook__(exctype, value, traceback)
  sys.exit(1)
def bstack1lll11l1l_opy_(message=bstack11l1ll_opy_ (u"࠭ࠧ஬")):
  global CONFIG
  try:
    if message:
      bstack1lllllll11_opy_ = {
        bstack11l1ll_opy_ (u"ࠧࡦࡴࡵࡳࡷ࠭஭"): str(message)
      }
      bstack111ll11ll_opy_(bstack1llll1l11l_opy_, CONFIG, bstack1lllllll11_opy_)
    else:
      bstack111ll11ll_opy_(bstack1llll1l11l_opy_, CONFIG)
  except Exception as e:
    logger.debug(bstack1111l1l11_opy_.format(str(e)))
def bstack1llll11lll_opy_(bstack1l11ll1l1_opy_, size):
  bstack1lll11l1ll_opy_ = []
  while len(bstack1l11ll1l1_opy_) > size:
    bstack1l1l1l111_opy_ = bstack1l11ll1l1_opy_[:size]
    bstack1lll11l1ll_opy_.append(bstack1l1l1l111_opy_)
    bstack1l11ll1l1_opy_ = bstack1l11ll1l1_opy_[size:]
  bstack1lll11l1ll_opy_.append(bstack1l11ll1l1_opy_)
  return bstack1lll11l1ll_opy_
def bstack1l1l11l1l_opy_(args):
  if bstack11l1ll_opy_ (u"ࠨ࠯ࡰࠫம") in args and bstack11l1ll_opy_ (u"ࠩࡳࡨࡧ࠭ய") in args:
    return True
  return False
def run_on_browserstack(bstack1111l11ll_opy_=None, bstack1llll111l_opy_=None, bstack1ll1l111l1_opy_=False):
  global CONFIG
  global bstack1lll1l1l1_opy_
  global bstack1ll11ll111_opy_
  global bstack11ll111ll_opy_
  bstack1ll1llll_opy_ = bstack11l1ll_opy_ (u"ࠪࠫர")
  bstack1l1llll11_opy_(bstack111ll1111_opy_, logger)
  if bstack1111l11ll_opy_ and isinstance(bstack1111l11ll_opy_, str):
    bstack1111l11ll_opy_ = eval(bstack1111l11ll_opy_)
  if bstack1111l11ll_opy_:
    CONFIG = bstack1111l11ll_opy_[bstack11l1ll_opy_ (u"ࠫࡈࡕࡎࡇࡋࡊࠫற")]
    bstack1lll1l1l1_opy_ = bstack1111l11ll_opy_[bstack11l1ll_opy_ (u"ࠬࡎࡕࡃࡡࡘࡖࡑ࠭ல")]
    bstack1ll11ll111_opy_ = bstack1111l11ll_opy_[bstack11l1ll_opy_ (u"࠭ࡉࡔࡡࡄࡔࡕࡥࡁࡖࡖࡒࡑࡆ࡚ࡅࠨள")]
    bstack1ll1l11l1_opy_.bstack1l1ll1ll1_opy_(bstack11l1ll_opy_ (u"ࠧࡊࡕࡢࡅࡕࡖ࡟ࡂࡗࡗࡓࡒࡇࡔࡆࠩழ"), bstack1ll11ll111_opy_)
    bstack1ll1llll_opy_ = bstack11l1ll_opy_ (u"ࠨࡲࡼࡸ࡭ࡵ࡮ࠨவ")
  if not bstack1ll1l111l1_opy_:
    if len(sys.argv) <= 1:
      logger.critical(bstack1ll1ll11_opy_)
      return
    if sys.argv[1] == bstack11l1ll_opy_ (u"ࠩ࠰࠱ࡻ࡫ࡲࡴ࡫ࡲࡲࠬஶ") or sys.argv[1] == bstack11l1ll_opy_ (u"ࠪ࠱ࡻ࠭ஷ"):
      logger.info(bstack11l1ll_opy_ (u"ࠫࡇࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࠣࡔࡾࡺࡨࡰࡰࠣࡗࡉࡑࠠࡷࡽࢀࠫஸ").format(__version__))
      return
    if sys.argv[1] == bstack11l1ll_opy_ (u"ࠬࡹࡥࡵࡷࡳࠫஹ"):
      bstack1l1llll1ll_opy_()
      return
  args = sys.argv
  bstack1ll11lll_opy_()
  global bstack1ll1llllll_opy_
  global bstack1lll11l1_opy_
  global bstack1ll11l1ll1_opy_
  global bstack11l1l1l11_opy_
  global bstack111lll111_opy_
  global bstack1l1111ll_opy_
  global bstack1llll1ll_opy_
  global bstack1lllll11l1_opy_
  global bstack11l111l11_opy_
  global bstack1lll11l11_opy_
  global bstack1ll1lll1ll_opy_
  bstack1lll11l1_opy_ = len(CONFIG[bstack11l1ll_opy_ (u"࠭ࡰ࡭ࡣࡷࡪࡴࡸ࡭ࡴࠩ஺")])
  if not bstack1ll1llll_opy_:
    if args[1] == bstack11l1ll_opy_ (u"ࠧࡱࡻࡷ࡬ࡴࡴࠧ஻") or args[1] == bstack11l1ll_opy_ (u"ࠨࡲࡼࡸ࡭ࡵ࡮࠴ࠩ஼"):
      bstack1ll1llll_opy_ = bstack11l1ll_opy_ (u"ࠩࡳࡽࡹ࡮࡯࡯ࠩ஽")
      args = args[2:]
    elif args[1] == bstack11l1ll_opy_ (u"ࠪࡶࡴࡨ࡯ࡵࠩா"):
      bstack1ll1llll_opy_ = bstack11l1ll_opy_ (u"ࠫࡷࡵࡢࡰࡶࠪி")
      args = args[2:]
    elif args[1] == bstack11l1ll_opy_ (u"ࠬࡶࡡࡣࡱࡷࠫீ"):
      bstack1ll1llll_opy_ = bstack11l1ll_opy_ (u"࠭ࡰࡢࡤࡲࡸࠬு")
      args = args[2:]
    elif args[1] == bstack11l1ll_opy_ (u"ࠧࡳࡱࡥࡳࡹ࠳ࡩ࡯ࡶࡨࡶࡳࡧ࡬ࠨூ"):
      bstack1ll1llll_opy_ = bstack11l1ll_opy_ (u"ࠨࡴࡲࡦࡴࡺ࠭ࡪࡰࡷࡩࡷࡴࡡ࡭ࠩ௃")
      args = args[2:]
    elif args[1] == bstack11l1ll_opy_ (u"ࠩࡳࡽࡹ࡫ࡳࡵࠩ௄"):
      bstack1ll1llll_opy_ = bstack11l1ll_opy_ (u"ࠪࡴࡾࡺࡥࡴࡶࠪ௅")
      args = args[2:]
    elif args[1] == bstack11l1ll_opy_ (u"ࠫࡧ࡫ࡨࡢࡸࡨࠫெ"):
      bstack1ll1llll_opy_ = bstack11l1ll_opy_ (u"ࠬࡨࡥࡩࡣࡹࡩࠬே")
      args = args[2:]
    else:
      if not bstack11l1ll_opy_ (u"࠭ࡦࡳࡣࡰࡩࡼࡵࡲ࡬ࠩை") in CONFIG or str(CONFIG[bstack11l1ll_opy_ (u"ࠧࡧࡴࡤࡱࡪࡽ࡯ࡳ࡭ࠪ௉")]).lower() in [bstack11l1ll_opy_ (u"ࠨࡲࡼࡸ࡭ࡵ࡮ࠨொ"), bstack11l1ll_opy_ (u"ࠩࡳࡽࡹ࡮࡯࡯࠵ࠪோ")]:
        bstack1ll1llll_opy_ = bstack11l1ll_opy_ (u"ࠪࡴࡾࡺࡨࡰࡰࠪௌ")
        args = args[1:]
      elif str(CONFIG[bstack11l1ll_opy_ (u"ࠫ࡫ࡸࡡ࡮ࡧࡺࡳࡷࡱ்ࠧ")]).lower() == bstack11l1ll_opy_ (u"ࠬࡸ࡯ࡣࡱࡷࠫ௎"):
        bstack1ll1llll_opy_ = bstack11l1ll_opy_ (u"࠭ࡲࡰࡤࡲࡸࠬ௏")
        args = args[1:]
      elif str(CONFIG[bstack11l1ll_opy_ (u"ࠧࡧࡴࡤࡱࡪࡽ࡯ࡳ࡭ࠪௐ")]).lower() == bstack11l1ll_opy_ (u"ࠨࡲࡤࡦࡴࡺࠧ௑"):
        bstack1ll1llll_opy_ = bstack11l1ll_opy_ (u"ࠩࡳࡥࡧࡵࡴࠨ௒")
        args = args[1:]
      elif str(CONFIG[bstack11l1ll_opy_ (u"ࠪࡪࡷࡧ࡭ࡦࡹࡲࡶࡰ࠭௓")]).lower() == bstack11l1ll_opy_ (u"ࠫࡵࡿࡴࡦࡵࡷࠫ௔"):
        bstack1ll1llll_opy_ = bstack11l1ll_opy_ (u"ࠬࡶࡹࡵࡧࡶࡸࠬ௕")
        args = args[1:]
      elif str(CONFIG[bstack11l1ll_opy_ (u"࠭ࡦࡳࡣࡰࡩࡼࡵࡲ࡬ࠩ௖")]).lower() == bstack11l1ll_opy_ (u"ࠧࡣࡧ࡫ࡥࡻ࡫ࠧௗ"):
        bstack1ll1llll_opy_ = bstack11l1ll_opy_ (u"ࠨࡤࡨ࡬ࡦࡼࡥࠨ௘")
        args = args[1:]
      else:
        os.environ[bstack11l1ll_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡈࡕࡅࡒࡋࡗࡐࡔࡎࠫ௙")] = bstack1ll1llll_opy_
        bstack1ll1111l1_opy_(bstack11l1l111_opy_)
  os.environ[bstack11l1ll_opy_ (u"ࠪࡊࡗࡇࡍࡆ࡙ࡒࡖࡐࡥࡕࡔࡇࡇࠫ௚")] = bstack1ll1llll_opy_
  bstack11ll111ll_opy_ = bstack1ll1llll_opy_
  global bstack1l1lll11ll_opy_
  if bstack1111l11ll_opy_:
    try:
      os.environ[bstack11l1ll_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡊࡗࡇࡍࡆ࡙ࡒࡖࡐ࠭௛")] = bstack1ll1llll_opy_
      bstack111ll11ll_opy_(bstack11ll1llll_opy_, CONFIG)
    except Exception as e:
      logger.debug(bstack1111l1l11_opy_.format(str(e)))
  global bstack1l11l11ll_opy_
  global bstack1l11ll1ll_opy_
  global bstack11lll1ll_opy_
  global bstack1ll11l1111_opy_
  global bstack1ll1ll111l_opy_
  global bstack111l111l1_opy_
  global bstack111l111ll_opy_
  global bstack1l1lllll1l_opy_
  global bstack111l11111_opy_
  global bstack1l11lllll_opy_
  global bstack1ll111ll11_opy_
  global bstack1l1ll11l11_opy_
  global bstack1ll11llll1_opy_
  global bstack11l111111_opy_
  global bstack1llll1111l_opy_
  global bstack111llllll_opy_
  global bstack1l1l1l1ll_opy_
  global bstack1ll11ll11l_opy_
  global bstack1lll11l111_opy_
  global bstack1ll111llll_opy_
  try:
    from selenium import webdriver
    from selenium.webdriver.remote.webdriver import WebDriver
    bstack1l11l11ll_opy_ = webdriver.Remote.__init__
    bstack1l11ll1ll_opy_ = WebDriver.quit
    bstack1ll111ll11_opy_ = WebDriver.close
    bstack11l111111_opy_ = WebDriver.get
    bstack1ll111llll_opy_ = WebDriver.execute
  except Exception as e:
    pass
  try:
    import Browser
    from subprocess import Popen
    bstack1l1lll11ll_opy_ = Popen.__init__
  except Exception as e:
    pass
  if bstack11111llll_opy_(CONFIG) and bstack1l1l11lll_opy_():
    if bstack1lll1ll1l_opy_() < version.parse(bstack11l1lll11_opy_):
      logger.error(bstack11l111lll_opy_.format(bstack1lll1ll1l_opy_()))
    else:
      try:
        from selenium.webdriver.remote.remote_connection import RemoteConnection
        bstack1llll1111l_opy_ = RemoteConnection._get_proxy_url
      except Exception as e:
        logger.error(bstack1ll1l1111l_opy_.format(str(e)))
  if bstack1ll1llll_opy_ != bstack11l1ll_opy_ (u"ࠬࡶࡹࡵࡪࡲࡲࠬ௜") or (bstack1ll1llll_opy_ == bstack11l1ll_opy_ (u"࠭ࡰࡺࡶ࡫ࡳࡳ࠭௝") and not bstack1111l11ll_opy_):
    bstack111111l1_opy_()
  if (bstack1ll1llll_opy_ in [bstack11l1ll_opy_ (u"ࠧࡱࡣࡥࡳࡹ࠭௞"), bstack11l1ll_opy_ (u"ࠨࡴࡲࡦࡴࡺࠧ௟"), bstack11l1ll_opy_ (u"ࠩࡵࡳࡧࡵࡴ࠮࡫ࡱࡸࡪࡸ࡮ࡢ࡮ࠪ௠")]):
    try:
      from robot import run_cli
      from robot.output import Output
      from robot.running.status import TestStatus
      from pabot.pabot import QueueItem
      from pabot import pabot
      try:
        from SeleniumLibrary.keywords.webdrivertools.webdrivertools import WebDriverCreator
        from SeleniumLibrary.keywords.webdrivertools.webdrivertools import WebDriverCache
        WebDriverCreator._get_ff_profile = bstack1lll1ll1l1_opy_
        bstack1ll1ll111l_opy_ = WebDriverCache.close
      except Exception as e:
        logger.warn(bstack11l1l1ll1_opy_ + str(e))
      try:
        from AppiumLibrary.utils.applicationcache import ApplicationCache
        bstack1ll11l1111_opy_ = ApplicationCache.close
      except Exception as e:
        logger.debug(bstack11lll1l1_opy_ + str(e))
    except Exception as e:
      bstack1l11lll1_opy_(e, bstack11l1l1ll1_opy_)
    if bstack1ll1llll_opy_ != bstack11l1ll_opy_ (u"ࠪࡶࡴࡨ࡯ࡵ࠯࡬ࡲࡹ࡫ࡲ࡯ࡣ࡯ࠫ௡"):
      bstack1l11ll11l_opy_()
    bstack11lll1ll_opy_ = Output.end_test
    bstack111l111l1_opy_ = TestStatus.__init__
    bstack1l1lllll1l_opy_ = pabot._run
    bstack111l11111_opy_ = QueueItem.__init__
    bstack1l11lllll_opy_ = pabot._create_command_for_execution
    bstack1ll11ll11l_opy_ = pabot._report_results
  if bstack1ll1llll_opy_ == bstack11l1ll_opy_ (u"ࠫࡧ࡫ࡨࡢࡸࡨࠫ௢"):
    try:
      from behave.runner import Runner
      from behave.model import Step
    except Exception as e:
      bstack1l11lll1_opy_(e, bstack1ll1ll1ll_opy_)
    bstack1l1ll11l11_opy_ = Runner.run_hook
    bstack1ll11llll1_opy_ = Step.run
  if bstack1ll1llll_opy_ == bstack11l1ll_opy_ (u"ࠬࡶࡹࡵࡧࡶࡸࠬ௣"):
    try:
      from _pytest.config import Config
      bstack111llllll_opy_ = Config.getoption
      from _pytest import runner
      bstack1l1l1l1ll_opy_ = runner._update_current_test_var
    except Exception as e:
      logger.warn(e, bstack1lll11ll1l_opy_)
    try:
      from pytest_bdd import reporting
      bstack1lll11l111_opy_ = reporting.runtest_makereport
    except Exception as e:
      logger.debug(bstack11l1ll_opy_ (u"࠭ࡐ࡭ࡧࡤࡷࡪࠦࡩ࡯ࡵࡷࡥࡱࡲࠠࡱࡻࡷࡩࡸࡺ࠭ࡣࡦࡧࠤࡹࡵࠠࡳࡷࡱࠤࡵࡿࡴࡦࡵࡷ࠱ࡧࡪࡤࠡࡶࡨࡷࡹࡹࠧ௤"))
  if bstack1ll1llll_opy_ in bstack11l11111_opy_:
    try:
      framework_name = bstack11l1ll_opy_ (u"ࠧࡓࡱࡥࡳࡹ࠭௥") if bstack1ll1llll_opy_ in [bstack11l1ll_opy_ (u"ࠨࡲࡤࡦࡴࡺࠧ௦"), bstack11l1ll_opy_ (u"ࠩࡵࡳࡧࡵࡴࠨ௧"), bstack11l1ll_opy_ (u"ࠪࡶࡴࡨ࡯ࡵ࠯࡬ࡲࡹ࡫ࡲ࡯ࡣ࡯ࠫ௨")] else bstack11l11l11_opy_(bstack1ll1llll_opy_)
      bstack11l1ll11_opy_.launch(CONFIG, {
        bstack11l1ll_opy_ (u"ࠫ࡫ࡸࡡ࡮ࡧࡺࡳࡷࡱ࡟࡯ࡣࡰࡩࠬ௩"): bstack11l1ll_opy_ (u"ࠬࢁ࠰ࡾ࠯ࡦࡹࡨࡻ࡭ࡣࡧࡵࠫ௪").format(framework_name) if bstack1ll1llll_opy_ == bstack11l1ll_opy_ (u"࠭ࡰࡺࡶࡨࡷࡹ࠭௫") and bstack1l11ll11_opy_() else framework_name,
        bstack11l1ll_opy_ (u"ࠧࡧࡴࡤࡱࡪࡽ࡯ࡳ࡭ࡢࡺࡪࡸࡳࡪࡱࡱࠫ௬"): bstack1111lll11_opy_(framework_name),
        bstack11l1ll_opy_ (u"ࠨࡵࡧ࡯ࡤࡼࡥࡳࡵ࡬ࡳࡳ࠭௭"): __version__
      })
    except Exception as e:
      logger.debug(bstack11ll11lll_opy_.format(bstack11l1ll_opy_ (u"ࠩࡒࡦࡸ࡫ࡲࡷࡣࡥ࡭ࡱ࡯ࡴࡺࠩ௮"), str(e)))
  if bstack1ll1llll_opy_ in bstack1l1ll1ll_opy_:
    try:
      framework_name = bstack11l1ll_opy_ (u"ࠪࡶࡴࡨ࡯ࡵࠩ௯") if bstack1ll1llll_opy_ in [bstack11l1ll_opy_ (u"ࠫࡵࡧࡢࡰࡶࠪ௰"), bstack11l1ll_opy_ (u"ࠬࡸ࡯ࡣࡱࡷࠫ௱")] else bstack1ll1llll_opy_
      if bstack1l1lll1lll_opy_ and bstack11l1ll_opy_ (u"࠭ࡡࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾ࠭௲") in CONFIG and CONFIG[bstack11l1ll_opy_ (u"ࠧࡢࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿࠧ௳")] == True:
        if bstack11l1ll_opy_ (u"ࠨࡣࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࡐࡲࡷ࡭ࡴࡴࡳࠨ௴") in CONFIG:
          os.environ[bstack11l1ll_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡖࡈࡗ࡙ࡥࡁࡄࡅࡈࡗࡘࡏࡂࡊࡎࡌࡘ࡞ࡥࡃࡐࡐࡉࡍࡌ࡛ࡒࡂࡖࡌࡓࡓࡥ࡙ࡎࡎࠪ௵")] = os.getenv(bstack11l1ll_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡗࡉࡘ࡚࡟ࡂࡅࡆࡉࡘ࡙ࡉࡃࡋࡏࡍ࡙࡟࡟ࡄࡑࡑࡊࡎࡍࡕࡓࡃࡗࡍࡔࡔ࡟࡚ࡏࡏࠫ௶"), json.dumps(CONFIG[bstack11l1ll_opy_ (u"ࠫࡦࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࡓࡵࡺࡩࡰࡰࡶࠫ௷")]))
          CONFIG[bstack11l1ll_opy_ (u"ࠬࡧࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽࡔࡶࡴࡪࡱࡱࡷࠬ௸")].pop(bstack11l1ll_opy_ (u"࠭ࡩ࡯ࡥ࡯ࡹࡩ࡫ࡔࡢࡩࡶࡍࡳ࡚ࡥࡴࡶ࡬ࡲ࡬࡙ࡣࡰࡲࡨࠫ௹"), None)
          CONFIG[bstack11l1ll_opy_ (u"ࠧࡢࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿࡏࡱࡶ࡬ࡳࡳࡹࠧ௺")].pop(bstack11l1ll_opy_ (u"ࠨࡧࡻࡧࡱࡻࡤࡦࡖࡤ࡫ࡸࡏ࡮ࡕࡧࡶࡸ࡮ࡴࡧࡔࡥࡲࡴࡪ࠭௻"), None)
        bstack1l111l1l_opy_, bstack111lllll_opy_ = bstack1ll111l11_opy_.bstack1ll11l1l11_opy_(CONFIG, bstack1ll1llll_opy_, bstack1111lll11_opy_(framework_name))
        if not bstack1l111l1l_opy_ is None:
          os.environ[bstack11l1ll_opy_ (u"ࠩࡅࡗࡤࡇ࠱࠲࡛ࡢࡎ࡜࡚ࠧ௼")] = bstack1l111l1l_opy_
          os.environ[bstack11l1ll_opy_ (u"ࠪࡆࡘࡥࡁ࠲࠳࡜ࡣ࡙ࡋࡓࡕࡡࡕ࡙ࡓࡥࡉࡅࠩ௽")] = str(bstack111lllll_opy_)
    except Exception as e:
      logger.debug(bstack11ll11lll_opy_.format(bstack11l1ll_opy_ (u"ࠫࡆࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࠫ௾"), str(e)))
  if bstack1ll1llll_opy_ == bstack11l1ll_opy_ (u"ࠬࡶࡹࡵࡪࡲࡲࠬ௿"):
    bstack1ll11l1ll1_opy_ = True
    if bstack1111l11ll_opy_ and bstack1ll1l111l1_opy_:
      bstack1l1111ll_opy_ = CONFIG.get(bstack11l1ll_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡓࡵࡣࡦ࡯ࡑࡵࡣࡢ࡮ࡒࡴࡹ࡯࡯࡯ࡵࠪఀ"), {}).get(bstack11l1ll_opy_ (u"ࠧ࡭ࡱࡦࡥࡱࡏࡤࡦࡰࡷ࡭࡫࡯ࡥࡳࠩఁ"))
      bstack1l1lllll1_opy_(bstack11111lll1_opy_)
    elif bstack1111l11ll_opy_:
      bstack1l1111ll_opy_ = CONFIG.get(bstack11l1ll_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡕࡷࡥࡨࡱࡌࡰࡥࡤࡰࡔࡶࡴࡪࡱࡱࡷࠬం"), {}).get(bstack11l1ll_opy_ (u"ࠩ࡯ࡳࡨࡧ࡬ࡊࡦࡨࡲࡹ࡯ࡦࡪࡧࡵࠫః"))
      global bstack11l1l1111_opy_
      try:
        if bstack1l1l11l1l_opy_(bstack1111l11ll_opy_[bstack11l1ll_opy_ (u"ࠪࡪ࡮ࡲࡥࡠࡰࡤࡱࡪ࠭ఄ")]) and multiprocessing.current_process().name == bstack11l1ll_opy_ (u"ࠫ࠵࠭అ"):
          bstack1111l11ll_opy_[bstack11l1ll_opy_ (u"ࠬ࡬ࡩ࡭ࡧࡢࡲࡦࡳࡥࠨఆ")].remove(bstack11l1ll_opy_ (u"࠭࠭࡮ࠩఇ"))
          bstack1111l11ll_opy_[bstack11l1ll_opy_ (u"ࠧࡧ࡫࡯ࡩࡤࡴࡡ࡮ࡧࠪఈ")].remove(bstack11l1ll_opy_ (u"ࠨࡲࡧࡦࠬఉ"))
          bstack1111l11ll_opy_[bstack11l1ll_opy_ (u"ࠩࡩ࡭ࡱ࡫࡟࡯ࡣࡰࡩࠬఊ")] = bstack1111l11ll_opy_[bstack11l1ll_opy_ (u"ࠪࡪ࡮ࡲࡥࡠࡰࡤࡱࡪ࠭ఋ")][0]
          with open(bstack1111l11ll_opy_[bstack11l1ll_opy_ (u"ࠫ࡫࡯࡬ࡦࡡࡱࡥࡲ࡫ࠧఌ")], bstack11l1ll_opy_ (u"ࠬࡸࠧ఍")) as f:
            bstack1ll1llll1_opy_ = f.read()
          bstack1l1111lll_opy_ = bstack11l1ll_opy_ (u"ࠨࠢࠣࡨࡵࡳࡲࠦࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࡤࡹࡤ࡬ࠢ࡬ࡱࡵࡵࡲࡵࠢࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࡠ࡫ࡱ࡭ࡹ࡯ࡡ࡭࡫ࡽࡩࡀࠦࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࡤ࡯࡮ࡪࡶ࡬ࡥࡱ࡯ࡺࡦࠪࡾࢁ࠮ࡁࠠࡧࡴࡲࡱࠥࡶࡤࡣࠢ࡬ࡱࡵࡵࡲࡵࠢࡓࡨࡧࡁࠠࡰࡩࡢࡨࡧࠦ࠽ࠡࡒࡧࡦ࠳ࡪ࡯ࡠࡤࡵࡩࡦࡱ࠻ࠋࡦࡨࡪࠥࡳ࡯ࡥࡡࡥࡶࡪࡧ࡫ࠩࡵࡨࡰ࡫࠲ࠠࡢࡴࡪ࠰ࠥࡺࡥ࡮ࡲࡲࡶࡦࡸࡹࠡ࠿ࠣ࠴࠮ࡀࠊࠡࠢࡷࡶࡾࡀࠊࠡࠢࠣࠤࡦࡸࡧࠡ࠿ࠣࡷࡹࡸࠨࡪࡰࡷࠬࡦࡸࡧࠪ࠭࠴࠴࠮ࠐࠠࠡࡧࡻࡧࡪࡶࡴࠡࡇࡻࡧࡪࡶࡴࡪࡱࡱࠤࡦࡹࠠࡦ࠼ࠍࠤࠥࠦࠠࡱࡣࡶࡷࠏࠦࠠࡰࡩࡢࡨࡧ࠮ࡳࡦ࡮ࡩ࠰ࡦࡸࡧ࠭ࡶࡨࡱࡵࡵࡲࡢࡴࡼ࠭ࠏࡖࡤࡣ࠰ࡧࡳࡤࡨࠠ࠾ࠢࡰࡳࡩࡥࡢࡳࡧࡤ࡯ࠏࡖࡤࡣ࠰ࡧࡳࡤࡨࡲࡦࡣ࡮ࠤࡂࠦ࡭ࡰࡦࡢࡦࡷ࡫ࡡ࡬ࠌࡓࡨࡧ࠮ࠩ࠯ࡵࡨࡸࡤࡺࡲࡢࡥࡨࠬ࠮ࡢ࡮ࠣࠤࠥఎ").format(str(bstack1111l11ll_opy_))
          bstack11l1lll1_opy_ = bstack1l1111lll_opy_ + bstack1ll1llll1_opy_
          bstack1ll1l111ll_opy_ = bstack1111l11ll_opy_[bstack11l1ll_opy_ (u"ࠧࡧ࡫࡯ࡩࡤࡴࡡ࡮ࡧࠪఏ")] + bstack11l1ll_opy_ (u"ࠨࡡࡥࡷࡹࡧࡣ࡬ࡡࡷࡩࡲࡶ࠮ࡱࡻࠪఐ")
          with open(bstack1ll1l111ll_opy_, bstack11l1ll_opy_ (u"ࠩࡺࠫ఑")):
            pass
          with open(bstack1ll1l111ll_opy_, bstack11l1ll_opy_ (u"ࠥࡻ࠰ࠨఒ")) as f:
            f.write(bstack11l1lll1_opy_)
          import subprocess
          bstack111ll111_opy_ = subprocess.run([bstack11l1ll_opy_ (u"ࠦࡵࡿࡴࡩࡱࡱࠦఓ"), bstack1ll1l111ll_opy_])
          if os.path.exists(bstack1ll1l111ll_opy_):
            os.unlink(bstack1ll1l111ll_opy_)
          os._exit(bstack111ll111_opy_.returncode)
        else:
          if bstack1l1l11l1l_opy_(bstack1111l11ll_opy_[bstack11l1ll_opy_ (u"ࠬ࡬ࡩ࡭ࡧࡢࡲࡦࡳࡥࠨఔ")]):
            bstack1111l11ll_opy_[bstack11l1ll_opy_ (u"࠭ࡦࡪ࡮ࡨࡣࡳࡧ࡭ࡦࠩక")].remove(bstack11l1ll_opy_ (u"ࠧ࠮࡯ࠪఖ"))
            bstack1111l11ll_opy_[bstack11l1ll_opy_ (u"ࠨࡨ࡬ࡰࡪࡥ࡮ࡢ࡯ࡨࠫగ")].remove(bstack11l1ll_opy_ (u"ࠩࡳࡨࡧ࠭ఘ"))
            bstack1111l11ll_opy_[bstack11l1ll_opy_ (u"ࠪࡪ࡮ࡲࡥࡠࡰࡤࡱࡪ࠭ఙ")] = bstack1111l11ll_opy_[bstack11l1ll_opy_ (u"ࠫ࡫࡯࡬ࡦࡡࡱࡥࡲ࡫ࠧచ")][0]
          bstack1l1lllll1_opy_(bstack11111lll1_opy_)
          sys.path.append(os.path.dirname(os.path.abspath(bstack1111l11ll_opy_[bstack11l1ll_opy_ (u"ࠬ࡬ࡩ࡭ࡧࡢࡲࡦࡳࡥࠨఛ")])))
          sys.argv = sys.argv[2:]
          mod_globals = globals()
          mod_globals[bstack11l1ll_opy_ (u"࠭࡟ࡠࡰࡤࡱࡪࡥ࡟ࠨజ")] = bstack11l1ll_opy_ (u"ࠧࡠࡡࡰࡥ࡮ࡴ࡟ࡠࠩఝ")
          mod_globals[bstack11l1ll_opy_ (u"ࠨࡡࡢࡪ࡮ࡲࡥࡠࡡࠪఞ")] = os.path.abspath(bstack1111l11ll_opy_[bstack11l1ll_opy_ (u"ࠩࡩ࡭ࡱ࡫࡟࡯ࡣࡰࡩࠬట")])
          exec(open(bstack1111l11ll_opy_[bstack11l1ll_opy_ (u"ࠪࡪ࡮ࡲࡥࡠࡰࡤࡱࡪ࠭ఠ")]).read(), mod_globals)
      except BaseException as e:
        try:
          traceback.print_exc()
          logger.error(bstack11l1ll_opy_ (u"ࠫࡈࡧࡵࡨࡪࡷࠤࡊࡾࡣࡦࡲࡷ࡭ࡴࡴ࠺ࠡࡽࢀࠫడ").format(str(e)))
          for driver in bstack11l1l1111_opy_:
            bstack1llll111l_opy_.append({
              bstack11l1ll_opy_ (u"ࠬࡴࡡ࡮ࡧࠪఢ"): bstack1111l11ll_opy_[bstack11l1ll_opy_ (u"࠭ࡦࡪ࡮ࡨࡣࡳࡧ࡭ࡦࠩణ")],
              bstack11l1ll_opy_ (u"ࠧࡦࡴࡵࡳࡷ࠭త"): str(e),
              bstack11l1ll_opy_ (u"ࠨ࡫ࡱࡨࡪࡾࠧథ"): multiprocessing.current_process().name
            })
            bstack1111ll1l1_opy_(driver, bstack11l1ll_opy_ (u"ࠩࡩࡥ࡮ࡲࡥࡥࠩద"), bstack11l1ll_opy_ (u"ࠥࡗࡪࡹࡳࡪࡱࡱࠤ࡫ࡧࡩ࡭ࡧࡧࠤࡼ࡯ࡴࡩ࠼ࠣࡠࡳࠨధ") + str(e))
        except Exception:
          pass
      finally:
        try:
          for driver in bstack11l1l1111_opy_:
            driver.quit()
        except Exception as e:
          pass
    else:
      percy.init(bstack1ll11ll111_opy_, CONFIG, logger)
      bstack1lllll11ll_opy_()
      bstack1l1lll111l_opy_()
      bstack1ll1ll1lll_opy_ = {
        bstack11l1ll_opy_ (u"ࠫ࡫࡯࡬ࡦࡡࡱࡥࡲ࡫ࠧన"): args[0],
        bstack11l1ll_opy_ (u"ࠬࡉࡏࡏࡈࡌࡋࠬ఩"): CONFIG,
        bstack11l1ll_opy_ (u"࠭ࡈࡖࡄࡢ࡙ࡗࡒࠧప"): bstack1lll1l1l1_opy_,
        bstack11l1ll_opy_ (u"ࠧࡊࡕࡢࡅࡕࡖ࡟ࡂࡗࡗࡓࡒࡇࡔࡆࠩఫ"): bstack1ll11ll111_opy_
      }
      percy.bstack1l1llll111_opy_()
      if bstack11l1ll_opy_ (u"ࠨࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࡶࠫబ") in CONFIG:
        bstack1ll111111l_opy_ = []
        manager = multiprocessing.Manager()
        bstack1lll1ll1ll_opy_ = manager.list()
        if bstack1l1l11l1l_opy_(args):
          for index, platform in enumerate(CONFIG[bstack11l1ll_opy_ (u"ࠩࡳࡰࡦࡺࡦࡰࡴࡰࡷࠬభ")]):
            if index == 0:
              bstack1ll1ll1lll_opy_[bstack11l1ll_opy_ (u"ࠪࡪ࡮ࡲࡥࡠࡰࡤࡱࡪ࠭మ")] = args
            bstack1ll111111l_opy_.append(multiprocessing.Process(name=str(index),
                                                       target=run_on_browserstack,
                                                       args=(bstack1ll1ll1lll_opy_, bstack1lll1ll1ll_opy_)))
        else:
          for index, platform in enumerate(CONFIG[bstack11l1ll_opy_ (u"ࠫࡵࡲࡡࡵࡨࡲࡶࡲࡹࠧయ")]):
            bstack1ll111111l_opy_.append(multiprocessing.Process(name=str(index),
                                                       target=run_on_browserstack,
                                                       args=(bstack1ll1ll1lll_opy_, bstack1lll1ll1ll_opy_)))
        for t in bstack1ll111111l_opy_:
          t.start()
        for t in bstack1ll111111l_opy_:
          t.join()
        bstack1lllll11l1_opy_ = list(bstack1lll1ll1ll_opy_)
      else:
        if bstack1l1l11l1l_opy_(args):
          bstack1ll1ll1lll_opy_[bstack11l1ll_opy_ (u"ࠬ࡬ࡩ࡭ࡧࡢࡲࡦࡳࡥࠨర")] = args
          test = multiprocessing.Process(name=str(0),
                                         target=run_on_browserstack, args=(bstack1ll1ll1lll_opy_,))
          test.start()
          test.join()
        else:
          bstack1l1lllll1_opy_(bstack11111lll1_opy_)
          sys.path.append(os.path.dirname(os.path.abspath(args[0])))
          mod_globals = globals()
          mod_globals[bstack11l1ll_opy_ (u"࠭࡟ࡠࡰࡤࡱࡪࡥ࡟ࠨఱ")] = bstack11l1ll_opy_ (u"ࠧࡠࡡࡰࡥ࡮ࡴ࡟ࡠࠩల")
          mod_globals[bstack11l1ll_opy_ (u"ࠨࡡࡢࡪ࡮ࡲࡥࡠࡡࠪళ")] = os.path.abspath(args[0])
          sys.argv = sys.argv[2:]
          exec(open(args[0]).read(), mod_globals)
  elif bstack1ll1llll_opy_ == bstack11l1ll_opy_ (u"ࠩࡳࡥࡧࡵࡴࠨఴ") or bstack1ll1llll_opy_ == bstack11l1ll_opy_ (u"ࠪࡶࡴࡨ࡯ࡵࠩవ"):
    try:
      from pabot import pabot
    except Exception as e:
      bstack1l11lll1_opy_(e, bstack11l1l1ll1_opy_)
    bstack1lllll11ll_opy_()
    bstack1l1lllll1_opy_(bstack1l1lll1ll_opy_)
    if bstack11l1ll_opy_ (u"ࠫ࠲࠳ࡰࡳࡱࡦࡩࡸࡹࡥࡴࠩశ") in args:
      i = args.index(bstack11l1ll_opy_ (u"ࠬ࠳࠭ࡱࡴࡲࡧࡪࡹࡳࡦࡵࠪష"))
      args.pop(i)
      args.pop(i)
    args.insert(0, str(bstack1ll1llllll_opy_))
    args.insert(0, str(bstack11l1ll_opy_ (u"࠭࠭࠮ࡲࡵࡳࡨ࡫ࡳࡴࡧࡶࠫస")))
    if bstack11l1ll11_opy_.on():
      try:
        from robot.run import USAGE
        from robot.utils import ArgumentParser
        from pabot.arguments import _parse_pabot_args
        bstack1l1l11111_opy_, pabot_args = _parse_pabot_args(args)
        opts, bstack1111ll1ll_opy_ = ArgumentParser(
            USAGE,
            auto_pythonpath=False,
            auto_argumentfile=True,
            env_options=bstack11l1ll_opy_ (u"ࠢࡓࡑࡅࡓ࡙ࡥࡏࡑࡖࡌࡓࡓ࡙ࠢహ"),
        ).parse_args(bstack1l1l11111_opy_)
        args.insert(args.index(bstack1111ll1ll_opy_[0]), str(bstack11l1ll_opy_ (u"ࠨ࠯࠰ࡰ࡮ࡹࡴࡦࡰࡨࡶࠬ఺")))
        args.insert(args.index(bstack1111ll1ll_opy_[0]), str(os.path.join(os.path.dirname(os.path.realpath(__file__)), bstack11l1ll_opy_ (u"ࠩࡥࡷࡹࡧࡣ࡬ࡡࡵࡳࡧࡵࡴࡠ࡮࡬ࡷࡹ࡫࡮ࡦࡴ࠱ࡴࡾ࠭఻"))))
        if bstack111l1l1l1_opy_(os.environ.get(bstack11l1ll_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡕࡉࡗ࡛ࡎࠨ఼"))) and str(os.environ.get(bstack11l1ll_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡖࡊࡘࡕࡏࡡࡗࡉࡘ࡚ࡓࠨఽ"), bstack11l1ll_opy_ (u"ࠬࡴࡵ࡭࡮ࠪా"))) != bstack11l1ll_opy_ (u"࠭࡮ࡶ࡮࡯ࠫి"):
          for bstack11l11l1l1_opy_ in bstack1111ll1ll_opy_:
            args.remove(bstack11l11l1l1_opy_)
          bstack1l111l11_opy_ = os.environ.get(bstack11l1ll_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡒࡆࡔࡘࡒࡤ࡚ࡅࡔࡖࡖࠫీ")).split(bstack11l1ll_opy_ (u"ࠨ࠮ࠪు"))
          for bstack1l111ll1l_opy_ in bstack1l111l11_opy_:
            args.append(bstack1l111ll1l_opy_)
      except Exception as e:
        logger.error(bstack11l1ll_opy_ (u"ࠤࡈࡶࡷࡵࡲࠡࡹ࡫࡭ࡱ࡫ࠠࡢࡶࡷࡥࡨ࡮ࡩ࡯ࡩࠣࡰ࡮ࡹࡴࡦࡰࡨࡶࠥ࡬࡯ࡳࠢࡒࡦࡸ࡫ࡲࡷࡣࡥ࡭ࡱ࡯ࡴࡺ࠰ࠣࡉࡷࡸ࡯ࡳࠢ࠰ࠤࠧూ").format(e))
    pabot.main(args)
  elif bstack1ll1llll_opy_ == bstack11l1ll_opy_ (u"ࠪࡶࡴࡨ࡯ࡵ࠯࡬ࡲࡹ࡫ࡲ࡯ࡣ࡯ࠫృ"):
    try:
      from robot import run_cli
    except Exception as e:
      bstack1l11lll1_opy_(e, bstack11l1l1ll1_opy_)
    for a in args:
      if bstack11l1ll_opy_ (u"ࠫࡇ࡙ࡔࡂࡅࡎࡔࡑࡇࡔࡇࡑࡕࡑࡎࡔࡄࡆ࡚ࠪౄ") in a:
        bstack111lll111_opy_ = int(a.split(bstack11l1ll_opy_ (u"ࠬࡀࠧ౅"))[1])
      if bstack11l1ll_opy_ (u"࠭ࡂࡔࡖࡄࡇࡐࡊࡅࡇࡎࡒࡇࡆࡒࡉࡅࡇࡑࡘࡎࡌࡉࡆࡔࠪె") in a:
        bstack1l1111ll_opy_ = str(a.split(bstack11l1ll_opy_ (u"ࠧ࠻ࠩే"))[1])
      if bstack11l1ll_opy_ (u"ࠨࡄࡖࡘࡆࡉࡋࡄࡎࡌࡅࡗࡍࡓࠨై") in a:
        bstack1llll1ll_opy_ = str(a.split(bstack11l1ll_opy_ (u"ࠩ࠽ࠫ౉"))[1])
    bstack1ll1ll1l_opy_ = None
    if bstack11l1ll_opy_ (u"ࠪ࠱࠲ࡨࡳࡵࡣࡦ࡯ࡤ࡯ࡴࡦ࡯ࡢ࡭ࡳࡪࡥࡹࠩొ") in args:
      i = args.index(bstack11l1ll_opy_ (u"ࠫ࠲࠳ࡢࡴࡶࡤࡧࡰࡥࡩࡵࡧࡰࡣ࡮ࡴࡤࡦࡺࠪో"))
      args.pop(i)
      bstack1ll1ll1l_opy_ = args.pop(i)
    if bstack1ll1ll1l_opy_ is not None:
      global bstack1lll1111_opy_
      bstack1lll1111_opy_ = bstack1ll1ll1l_opy_
    bstack1l1lllll1_opy_(bstack1l1lll1ll_opy_)
    run_cli(args)
    if bstack11l1ll_opy_ (u"ࠬࡨࡳࡵࡣࡦ࡯ࡤ࡫ࡲࡳࡱࡵࡣࡱ࡯ࡳࡵࠩౌ") in multiprocessing.current_process().__dict__.keys():
      for bstack1l111l1ll_opy_ in multiprocessing.current_process().bstack_error_list:
        bstack1llll111l_opy_.append(bstack1l111l1ll_opy_)
  elif bstack1ll1llll_opy_ == bstack11l1ll_opy_ (u"࠭ࡰࡺࡶࡨࡷࡹ్࠭"):
    bstack1lll11ll1_opy_ = bstack1lll11ll11_opy_(args, logger, CONFIG, bstack1l1lll1lll_opy_)
    bstack1lll11ll1_opy_.bstack111ll111l_opy_()
    bstack1lllll11ll_opy_()
    bstack11l1l1l11_opy_ = True
    bstack1lll11l11_opy_ = bstack1lll11ll1_opy_.bstack1ll11111l1_opy_()
    bstack1lll11ll1_opy_.bstack1ll1ll1lll_opy_(bstack1lll1111l1_opy_)
    bstack11l111l11_opy_ = bstack1lll11ll1_opy_.bstack11llllll_opy_(bstack1l11ll111_opy_, {
      bstack11l1ll_opy_ (u"ࠧࡉࡗࡅࡣ࡚ࡘࡌࠨ౎"): bstack1lll1l1l1_opy_,
      bstack11l1ll_opy_ (u"ࠨࡋࡖࡣࡆࡖࡐࡠࡃࡘࡘࡔࡓࡁࡕࡇࠪ౏"): bstack1ll11ll111_opy_,
      bstack11l1ll_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡃࡘࡘࡔࡓࡁࡕࡋࡒࡒࠬ౐"): bstack1l1lll1lll_opy_
    })
    bstack1ll1lll1ll_opy_ = 1 if len(bstack11l111l11_opy_) > 0 else 0
  elif bstack1ll1llll_opy_ == bstack11l1ll_opy_ (u"ࠪࡦࡪ࡮ࡡࡷࡧࠪ౑"):
    try:
      from behave.__main__ import main as bstack1l11llll_opy_
      from behave.configuration import Configuration
    except Exception as e:
      bstack1l11lll1_opy_(e, bstack1ll1ll1ll_opy_)
    bstack1lllll11ll_opy_()
    bstack11l1l1l11_opy_ = True
    bstack1l1l1ll1_opy_ = 1
    if bstack11l1ll_opy_ (u"ࠫࡵࡧࡲࡢ࡮࡯ࡩࡱࡹࡐࡦࡴࡓࡰࡦࡺࡦࡰࡴࡰࠫ౒") in CONFIG:
      bstack1l1l1ll1_opy_ = CONFIG[bstack11l1ll_opy_ (u"ࠬࡶࡡࡳࡣ࡯ࡰࡪࡲࡳࡑࡧࡵࡔࡱࡧࡴࡧࡱࡵࡱࠬ౓")]
    bstack1lll1l11ll_opy_ = int(bstack1l1l1ll1_opy_) * int(len(CONFIG[bstack11l1ll_opy_ (u"࠭ࡰ࡭ࡣࡷࡪࡴࡸ࡭ࡴࠩ౔")]))
    config = Configuration(args)
    bstack1l1l111ll_opy_ = config.paths
    if len(bstack1l1l111ll_opy_) == 0:
      import glob
      pattern = bstack11l1ll_opy_ (u"ࠧࠫࠬ࠲࠮࠳࡬ࡥࡢࡶࡸࡶࡪౕ࠭")
      bstack1lll1ll11l_opy_ = glob.glob(pattern, recursive=True)
      args.extend(bstack1lll1ll11l_opy_)
      config = Configuration(args)
      bstack1l1l111ll_opy_ = config.paths
    bstack1ll1111l_opy_ = [os.path.normpath(item) for item in bstack1l1l111ll_opy_]
    bstack1l11l1l11_opy_ = [os.path.normpath(item) for item in args]
    bstack1llll1111_opy_ = [item for item in bstack1l11l1l11_opy_ if item not in bstack1ll1111l_opy_]
    import platform as pf
    if pf.system().lower() == bstack11l1ll_opy_ (u"ࠨࡹ࡬ࡲࡩࡵࡷࡴౖࠩ"):
      from pathlib import PureWindowsPath, PurePosixPath
      bstack1ll1111l_opy_ = [str(PurePosixPath(PureWindowsPath(bstack11l1llll1_opy_)))
                    for bstack11l1llll1_opy_ in bstack1ll1111l_opy_]
    bstack1l1ll1l1l1_opy_ = []
    for spec in bstack1ll1111l_opy_:
      bstack11lll11ll_opy_ = []
      bstack11lll11ll_opy_ += bstack1llll1111_opy_
      bstack11lll11ll_opy_.append(spec)
      bstack1l1ll1l1l1_opy_.append(bstack11lll11ll_opy_)
    execution_items = []
    for bstack11lll11ll_opy_ in bstack1l1ll1l1l1_opy_:
      for index, _ in enumerate(CONFIG[bstack11l1ll_opy_ (u"ࠩࡳࡰࡦࡺࡦࡰࡴࡰࡷࠬ౗")]):
        item = {}
        item[bstack11l1ll_opy_ (u"ࠪࡥࡷ࡭ࠧౘ")] = bstack11l1ll_opy_ (u"ࠫࠥ࠭ౙ").join(bstack11lll11ll_opy_)
        item[bstack11l1ll_opy_ (u"ࠬ࡯࡮ࡥࡧࡻࠫౚ")] = index
        execution_items.append(item)
    bstack1lll1lll11_opy_ = bstack1llll11lll_opy_(execution_items, bstack1lll1l11ll_opy_)
    for execution_item in bstack1lll1lll11_opy_:
      bstack1ll111111l_opy_ = []
      for item in execution_item:
        bstack1ll111111l_opy_.append(bstack1llll1llll_opy_(name=str(item[bstack11l1ll_opy_ (u"࠭ࡩ࡯ࡦࡨࡼࠬ౛")]),
                                             target=bstack1ll11lllll_opy_,
                                             args=(item[bstack11l1ll_opy_ (u"ࠧࡢࡴࡪࠫ౜")],)))
      for t in bstack1ll111111l_opy_:
        t.start()
      for t in bstack1ll111111l_opy_:
        t.join()
  else:
    bstack1ll1111l1_opy_(bstack11l1l111_opy_)
  if not bstack1111l11ll_opy_:
    bstack11111ll1_opy_()
def browserstack_initialize(bstack1llll11l11_opy_=None):
  run_on_browserstack(bstack1llll11l11_opy_, None, True)
def bstack11111ll1_opy_():
  global CONFIG
  global bstack11ll111ll_opy_
  global bstack1ll1lll1ll_opy_
  bstack11l1ll11_opy_.stop()
  bstack11l1ll11_opy_.bstack1l1lll1l11_opy_()
  if bstack1ll111l11_opy_.bstack1ll1lll111_opy_(CONFIG):
    bstack1ll111l11_opy_.bstack1ll1111l11_opy_()
  [bstack11l11lll1_opy_, bstack11l11111l_opy_] = bstack1l111111l_opy_()
  if bstack11l11lll1_opy_ is not None and bstack1l11lll1l_opy_() != -1:
    sessions = bstack1ll11l1ll_opy_(bstack11l11lll1_opy_)
    bstack1llll1l1_opy_(sessions, bstack11l11111l_opy_)
  if bstack11ll111ll_opy_ == bstack11l1ll_opy_ (u"ࠨࡲࡼࡸࡪࡹࡴࠨౝ") and bstack1ll1lll1ll_opy_ != 0:
    sys.exit(bstack1ll1lll1ll_opy_)
def bstack11l11l11_opy_(bstack1l1l11ll1_opy_):
  if bstack1l1l11ll1_opy_:
    return bstack1l1l11ll1_opy_.capitalize()
  else:
    return bstack11l1ll_opy_ (u"ࠩࠪ౞")
def bstack11ll11l1_opy_(bstack11l111l1l_opy_):
  if bstack11l1ll_opy_ (u"ࠪࡲࡦࡳࡥࠨ౟") in bstack11l111l1l_opy_ and bstack11l111l1l_opy_[bstack11l1ll_opy_ (u"ࠫࡳࡧ࡭ࡦࠩౠ")] != bstack11l1ll_opy_ (u"ࠬ࠭ౡ"):
    return bstack11l111l1l_opy_[bstack11l1ll_opy_ (u"࠭࡮ࡢ࡯ࡨࠫౢ")]
  else:
    bstack111l1lll1_opy_ = bstack11l1ll_opy_ (u"ࠢࠣౣ")
    if bstack11l1ll_opy_ (u"ࠨࡦࡨࡺ࡮ࡩࡥࠨ౤") in bstack11l111l1l_opy_ and bstack11l111l1l_opy_[bstack11l1ll_opy_ (u"ࠩࡧࡩࡻ࡯ࡣࡦࠩ౥")] != None:
      bstack111l1lll1_opy_ += bstack11l111l1l_opy_[bstack11l1ll_opy_ (u"ࠪࡨࡪࡼࡩࡤࡧࠪ౦")] + bstack11l1ll_opy_ (u"ࠦ࠱ࠦࠢ౧")
      if bstack11l111l1l_opy_[bstack11l1ll_opy_ (u"ࠬࡵࡳࠨ౨")] == bstack11l1ll_opy_ (u"ࠨࡩࡰࡵࠥ౩"):
        bstack111l1lll1_opy_ += bstack11l1ll_opy_ (u"ࠢࡪࡑࡖࠤࠧ౪")
      bstack111l1lll1_opy_ += (bstack11l111l1l_opy_[bstack11l1ll_opy_ (u"ࠨࡱࡶࡣࡻ࡫ࡲࡴ࡫ࡲࡲࠬ౫")] or bstack11l1ll_opy_ (u"ࠩࠪ౬"))
      return bstack111l1lll1_opy_
    else:
      bstack111l1lll1_opy_ += bstack11l11l11_opy_(bstack11l111l1l_opy_[bstack11l1ll_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࠫ౭")]) + bstack11l1ll_opy_ (u"ࠦࠥࠨ౮") + (
              bstack11l111l1l_opy_[bstack11l1ll_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡥࡶࡦࡴࡶ࡭ࡴࡴࠧ౯")] or bstack11l1ll_opy_ (u"࠭ࠧ౰")) + bstack11l1ll_opy_ (u"ࠢ࠭ࠢࠥ౱")
      if bstack11l111l1l_opy_[bstack11l1ll_opy_ (u"ࠨࡱࡶࠫ౲")] == bstack11l1ll_opy_ (u"ࠤ࡚࡭ࡳࡪ࡯ࡸࡵࠥ౳"):
        bstack111l1lll1_opy_ += bstack11l1ll_opy_ (u"࡛ࠥ࡮ࡴࠠࠣ౴")
      bstack111l1lll1_opy_ += bstack11l111l1l_opy_[bstack11l1ll_opy_ (u"ࠫࡴࡹ࡟ࡷࡧࡵࡷ࡮ࡵ࡮ࠨ౵")] or bstack11l1ll_opy_ (u"ࠬ࠭౶")
      return bstack111l1lll1_opy_
def bstack1llllll1ll_opy_(bstack11l1lllll_opy_):
  if bstack11l1lllll_opy_ == bstack11l1ll_opy_ (u"ࠨࡤࡰࡰࡨࠦ౷"):
    return bstack11l1ll_opy_ (u"ࠧ࠽ࡶࡧࠤࡨࡲࡡࡴࡵࡀࠦࡧࡹࡴࡢࡥ࡮࠱ࡩࡧࡴࡢࠤࠣࡷࡹࡿ࡬ࡦ࠿ࠥࡧࡴࡲ࡯ࡳ࠼ࡪࡶࡪ࡫࡮࠼ࠤࡁࡀ࡫ࡵ࡮ࡵࠢࡦࡳࡱࡵࡲ࠾ࠤࡪࡶࡪ࡫࡮ࠣࡀࡆࡳࡲࡶ࡬ࡦࡶࡨࡨࡁ࠵ࡦࡰࡰࡷࡂࡁ࠵ࡴࡥࡀࠪ౸")
  elif bstack11l1lllll_opy_ == bstack11l1ll_opy_ (u"ࠣࡨࡤ࡭ࡱ࡫ࡤࠣ౹"):
    return bstack11l1ll_opy_ (u"ࠩ࠿ࡸࡩࠦࡣ࡭ࡣࡶࡷࡂࠨࡢࡴࡶࡤࡧࡰ࠳ࡤࡢࡶࡤࠦࠥࡹࡴࡺ࡮ࡨࡁࠧࡩ࡯࡭ࡱࡵ࠾ࡷ࡫ࡤ࠼ࠤࡁࡀ࡫ࡵ࡮ࡵࠢࡦࡳࡱࡵࡲ࠾ࠤࡵࡩࡩࠨ࠾ࡇࡣ࡬ࡰࡪࡪ࠼࠰ࡨࡲࡲࡹࡄ࠼࠰ࡶࡧࡂࠬ౺")
  elif bstack11l1lllll_opy_ == bstack11l1ll_opy_ (u"ࠥࡴࡦࡹࡳࡦࡦࠥ౻"):
    return bstack11l1ll_opy_ (u"ࠫࡁࡺࡤࠡࡥ࡯ࡥࡸࡹ࠽ࠣࡤࡶࡸࡦࡩ࡫࠮ࡦࡤࡸࡦࠨࠠࡴࡶࡼࡰࡪࡃࠢࡤࡱ࡯ࡳࡷࡀࡧࡳࡧࡨࡲࡀࠨ࠾࠽ࡨࡲࡲࡹࠦࡣࡰ࡮ࡲࡶࡂࠨࡧࡳࡧࡨࡲࠧࡄࡐࡢࡵࡶࡩࡩࡂ࠯ࡧࡱࡱࡸࡃࡂ࠯ࡵࡦࡁࠫ౼")
  elif bstack11l1lllll_opy_ == bstack11l1ll_opy_ (u"ࠧ࡫ࡲࡳࡱࡵࠦ౽"):
    return bstack11l1ll_opy_ (u"࠭࠼ࡵࡦࠣࡧࡱࡧࡳࡴ࠿ࠥࡦࡸࡺࡡࡤ࡭࠰ࡨࡦࡺࡡࠣࠢࡶࡸࡾࡲࡥ࠾ࠤࡦࡳࡱࡵࡲ࠻ࡴࡨࡨࡀࠨ࠾࠽ࡨࡲࡲࡹࠦࡣࡰ࡮ࡲࡶࡂࠨࡲࡦࡦࠥࡂࡊࡸࡲࡰࡴ࠿࠳࡫ࡵ࡮ࡵࡀ࠿࠳ࡹࡪ࠾ࠨ౾")
  elif bstack11l1lllll_opy_ == bstack11l1ll_opy_ (u"ࠢࡵ࡫ࡰࡩࡴࡻࡴࠣ౿"):
    return bstack11l1ll_opy_ (u"ࠨ࠾ࡷࡨࠥࡩ࡬ࡢࡵࡶࡁࠧࡨࡳࡵࡣࡦ࡯࠲ࡪࡡࡵࡣࠥࠤࡸࡺࡹ࡭ࡧࡀࠦࡨࡵ࡬ࡰࡴ࠽ࠧࡪ࡫ࡡ࠴࠴࠹࠿ࠧࡄ࠼ࡧࡱࡱࡸࠥࡩ࡯࡭ࡱࡵࡁࠧࠩࡥࡦࡣ࠶࠶࠻ࠨ࠾ࡕ࡫ࡰࡩࡴࡻࡴ࠽࠱ࡩࡳࡳࡺ࠾࠽࠱ࡷࡨࡃ࠭ಀ")
  elif bstack11l1lllll_opy_ == bstack11l1ll_opy_ (u"ࠤࡵࡹࡳࡴࡩ࡯ࡩࠥಁ"):
    return bstack11l1ll_opy_ (u"ࠪࡀࡹࡪࠠࡤ࡮ࡤࡷࡸࡃࠢࡣࡵࡷࡥࡨࡱ࠭ࡥࡣࡷࡥࠧࠦࡳࡵࡻ࡯ࡩࡂࠨࡣࡰ࡮ࡲࡶ࠿ࡨ࡬ࡢࡥ࡮࠿ࠧࡄ࠼ࡧࡱࡱࡸࠥࡩ࡯࡭ࡱࡵࡁࠧࡨ࡬ࡢࡥ࡮ࠦࡃࡘࡵ࡯ࡰ࡬ࡲ࡬ࡂ࠯ࡧࡱࡱࡸࡃࡂ࠯ࡵࡦࡁࠫಂ")
  else:
    return bstack11l1ll_opy_ (u"ࠫࡁࡺࡤࠡࡣ࡯࡭࡬ࡴ࠽ࠣࡥࡨࡲࡹ࡫ࡲࠣࠢࡦࡰࡦࡹࡳ࠾ࠤࡥࡷࡹࡧࡣ࡬࠯ࡧࡥࡹࡧࠢࠡࡵࡷࡽࡱ࡫࠽ࠣࡥࡲࡰࡴࡸ࠺ࡣ࡮ࡤࡧࡰࡁࠢ࠿࠾ࡩࡳࡳࡺࠠࡤࡱ࡯ࡳࡷࡃࠢࡣ࡮ࡤࡧࡰࠨ࠾ࠨಃ") + bstack11l11l11_opy_(
      bstack11l1lllll_opy_) + bstack11l1ll_opy_ (u"ࠬࡂ࠯ࡧࡱࡱࡸࡃࡂ࠯ࡵࡦࡁࠫ಄")
def bstack1lll11l1l1_opy_(session):
  return bstack11l1ll_opy_ (u"࠭࠼ࡵࡴࠣࡧࡱࡧࡳࡴ࠿ࠥࡦࡸࡺࡡࡤ࡭࠰ࡶࡴࡽࠢ࠿࠾ࡷࡨࠥࡩ࡬ࡢࡵࡶࡁࠧࡨࡳࡵࡣࡦ࡯࠲ࡪࡡࡵࡣࠣࡷࡪࡹࡳࡪࡱࡱ࠱ࡳࡧ࡭ࡦࠤࡁࡀࡦࠦࡨࡳࡧࡩࡁࠧࢁࡽࠣࠢࡷࡥࡷ࡭ࡥࡵ࠿ࠥࡣࡧࡲࡡ࡯࡭ࠥࡂࢀࢃ࠼࠰ࡣࡁࡀ࠴ࡺࡤ࠿ࡽࢀࡿࢂࡂࡴࡥࠢࡤࡰ࡮࡭࡮࠾ࠤࡦࡩࡳࡺࡥࡳࠤࠣࡧࡱࡧࡳࡴ࠿ࠥࡦࡸࡺࡡࡤ࡭࠰ࡨࡦࡺࡡࠣࡀࡾࢁࡁ࠵ࡴࡥࡀ࠿ࡸࡩࠦࡡ࡭࡫ࡪࡲࡂࠨࡣࡦࡰࡷࡩࡷࠨࠠࡤ࡮ࡤࡷࡸࡃࠢࡣࡵࡷࡥࡨࡱ࠭ࡥࡣࡷࡥࠧࡄࡻࡾ࠾࠲ࡸࡩࡄ࠼ࡵࡦࠣࡥࡱ࡯ࡧ࡯࠿ࠥࡧࡪࡴࡴࡦࡴࠥࠤࡨࡲࡡࡴࡵࡀࠦࡧࡹࡴࡢࡥ࡮࠱ࡩࡧࡴࡢࠤࡁࡿࢂࡂ࠯ࡵࡦࡁࡀࡹࡪࠠࡢ࡮࡬࡫ࡳࡃࠢࡤࡧࡱࡸࡪࡸࠢࠡࡥ࡯ࡥࡸࡹ࠽ࠣࡤࡶࡸࡦࡩ࡫࠮ࡦࡤࡸࡦࠨ࠾ࡼࡿ࠿࠳ࡹࡪ࠾࠽࠱ࡷࡶࡃ࠭ಅ").format(
    session[bstack11l1ll_opy_ (u"ࠧࡱࡷࡥࡰ࡮ࡩ࡟ࡶࡴ࡯ࠫಆ")], bstack11ll11l1_opy_(session), bstack1llllll1ll_opy_(session[bstack11l1ll_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࡟ࡴࡶࡤࡸࡺࡹࠧಇ")]),
    bstack1llllll1ll_opy_(session[bstack11l1ll_opy_ (u"ࠩࡶࡸࡦࡺࡵࡴࠩಈ")]),
    bstack11l11l11_opy_(session[bstack11l1ll_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࠫಉ")] or session[bstack11l1ll_opy_ (u"ࠫࡩ࡫ࡶࡪࡥࡨࠫಊ")] or bstack11l1ll_opy_ (u"ࠬ࠭ಋ")) + bstack11l1ll_opy_ (u"ࠨࠠࠣಌ") + (session[bstack11l1ll_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡠࡸࡨࡶࡸ࡯࡯࡯ࠩ಍")] or bstack11l1ll_opy_ (u"ࠨࠩಎ")),
    session[bstack11l1ll_opy_ (u"ࠩࡲࡷࠬಏ")] + bstack11l1ll_opy_ (u"ࠥࠤࠧಐ") + session[bstack11l1ll_opy_ (u"ࠫࡴࡹ࡟ࡷࡧࡵࡷ࡮ࡵ࡮ࠨ಑")], session[bstack11l1ll_opy_ (u"ࠬࡪࡵࡳࡣࡷ࡭ࡴࡴࠧಒ")] or bstack11l1ll_opy_ (u"࠭ࠧಓ"),
    session[bstack11l1ll_opy_ (u"ࠧࡤࡴࡨࡥࡹ࡫ࡤࡠࡣࡷࠫಔ")] if session[bstack11l1ll_opy_ (u"ࠨࡥࡵࡩࡦࡺࡥࡥࡡࡤࡸࠬಕ")] else bstack11l1ll_opy_ (u"ࠩࠪಖ"))
def bstack1llll1l1_opy_(sessions, bstack11l11111l_opy_):
  try:
    bstack1lll1l1l11_opy_ = bstack11l1ll_opy_ (u"ࠥࠦಗ")
    if not os.path.exists(bstack1lll1l1ll1_opy_):
      os.mkdir(bstack1lll1l1ll1_opy_)
    with open(os.path.join(os.path.dirname(os.path.realpath(__file__)), bstack11l1ll_opy_ (u"ࠫࡦࡹࡳࡦࡶࡶ࠳ࡷ࡫ࡰࡰࡴࡷ࠲࡭ࡺ࡭࡭ࠩಘ")), bstack11l1ll_opy_ (u"ࠬࡸࠧಙ")) as f:
      bstack1lll1l1l11_opy_ = f.read()
    bstack1lll1l1l11_opy_ = bstack1lll1l1l11_opy_.replace(bstack11l1ll_opy_ (u"࠭ࡻࠦࡔࡈࡗ࡚ࡒࡔࡔࡡࡆࡓ࡚ࡔࡔࠦࡿࠪಚ"), str(len(sessions)))
    bstack1lll1l1l11_opy_ = bstack1lll1l1l11_opy_.replace(bstack11l1ll_opy_ (u"ࠧࡼࠧࡅ࡙ࡎࡒࡄࡠࡗࡕࡐࠪࢃࠧಛ"), bstack11l11111l_opy_)
    bstack1lll1l1l11_opy_ = bstack1lll1l1l11_opy_.replace(bstack11l1ll_opy_ (u"ࠨࡽࠨࡆ࡚ࡏࡌࡅࡡࡑࡅࡒࡋࠥࡾࠩಜ"),
                                              sessions[0].get(bstack11l1ll_opy_ (u"ࠩࡥࡹ࡮ࡲࡤࡠࡰࡤࡱࡪ࠭ಝ")) if sessions[0] else bstack11l1ll_opy_ (u"ࠪࠫಞ"))
    with open(os.path.join(bstack1lll1l1ll1_opy_, bstack11l1ll_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭࠰ࡶࡪࡶ࡯ࡳࡶ࠱࡬ࡹࡳ࡬ࠨಟ")), bstack11l1ll_opy_ (u"ࠬࡽࠧಠ")) as stream:
      stream.write(bstack1lll1l1l11_opy_.split(bstack11l1ll_opy_ (u"࠭ࡻࠦࡕࡈࡗࡘࡏࡏࡏࡕࡢࡈࡆ࡚ࡁࠦࡿࠪಡ"))[0])
      for session in sessions:
        stream.write(bstack1lll11l1l1_opy_(session))
      stream.write(bstack1lll1l1l11_opy_.split(bstack11l1ll_opy_ (u"ࠧࡼࠧࡖࡉࡘ࡙ࡉࡐࡐࡖࡣࡉࡇࡔࡂࠧࢀࠫಢ"))[1])
    logger.info(bstack11l1ll_opy_ (u"ࠨࡉࡨࡲࡪࡸࡡࡵࡧࡧࠤࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࠣࡦࡺ࡯࡬ࡥࠢࡤࡶࡹ࡯ࡦࡢࡥࡷࡷࠥࡧࡴࠡࡽࢀࠫಣ").format(bstack1lll1l1ll1_opy_));
  except Exception as e:
    logger.debug(bstack1lll11111_opy_.format(str(e)))
def bstack1ll11l1ll_opy_(bstack11l11lll1_opy_):
  global CONFIG
  try:
    host = bstack11l1ll_opy_ (u"ࠩࡤࡴ࡮࠳ࡣ࡭ࡱࡸࡨࠬತ") if bstack11l1ll_opy_ (u"ࠪࡥࡵࡶࠧಥ") in CONFIG else bstack11l1ll_opy_ (u"ࠫࡦࡶࡩࠨದ")
    user = CONFIG[bstack11l1ll_opy_ (u"ࠬࡻࡳࡦࡴࡑࡥࡲ࡫ࠧಧ")]
    key = CONFIG[bstack11l1ll_opy_ (u"࠭ࡡࡤࡥࡨࡷࡸࡑࡥࡺࠩನ")]
    bstack1l11l1ll_opy_ = bstack11l1ll_opy_ (u"ࠧࡢࡲࡳ࠱ࡦࡻࡴࡰ࡯ࡤࡸࡪ࠭಩") if bstack11l1ll_opy_ (u"ࠨࡣࡳࡴࠬಪ") in CONFIG else bstack11l1ll_opy_ (u"ࠩࡤࡹࡹࡵ࡭ࡢࡶࡨࠫಫ")
    url = bstack11l1ll_opy_ (u"ࠪ࡬ࡹࡺࡰࡴ࠼࠲࠳ࢀࢃ࠺ࡼࡿࡃࡿࢂ࠴ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯࠳ࡩ࡯࡮࠱ࡾࢁ࠴ࡨࡵࡪ࡮ࡧࡷ࠴ࢁࡽ࠰ࡵࡨࡷࡸ࡯࡯࡯ࡵ࠱࡮ࡸࡵ࡮ࠨಬ").format(user, key, host, bstack1l11l1ll_opy_,
                                                                                bstack11l11lll1_opy_)
    headers = {
      bstack11l1ll_opy_ (u"ࠫࡈࡵ࡮ࡵࡧࡱࡸ࠲ࡺࡹࡱࡧࠪಭ"): bstack11l1ll_opy_ (u"ࠬࡧࡰࡱ࡮࡬ࡧࡦࡺࡩࡰࡰ࠲࡮ࡸࡵ࡮ࠨಮ"),
    }
    proxies = bstack1lll111111_opy_(CONFIG, url)
    response = requests.get(url, headers=headers, proxies=proxies)
    if response.json():
      return list(map(lambda session: session[bstack11l1ll_opy_ (u"࠭ࡡࡶࡶࡲࡱࡦࡺࡩࡰࡰࡢࡷࡪࡹࡳࡪࡱࡱࠫಯ")], response.json()))
  except Exception as e:
    logger.debug(bstack11l11lll_opy_.format(str(e)))
def bstack1l111111l_opy_():
  global CONFIG
  global bstack111l1ll1_opy_
  try:
    if bstack11l1ll_opy_ (u"ࠧࡣࡷ࡬ࡰࡩࡔࡡ࡮ࡧࠪರ") in CONFIG:
      host = bstack11l1ll_opy_ (u"ࠨࡣࡳ࡭࠲ࡩ࡬ࡰࡷࡧࠫಱ") if bstack11l1ll_opy_ (u"ࠩࡤࡴࡵ࠭ಲ") in CONFIG else bstack11l1ll_opy_ (u"ࠪࡥࡵ࡯ࠧಳ")
      user = CONFIG[bstack11l1ll_opy_ (u"ࠫࡺࡹࡥࡳࡐࡤࡱࡪ࠭಴")]
      key = CONFIG[bstack11l1ll_opy_ (u"ࠬࡧࡣࡤࡧࡶࡷࡐ࡫ࡹࠨವ")]
      bstack1l11l1ll_opy_ = bstack11l1ll_opy_ (u"࠭ࡡࡱࡲ࠰ࡥࡺࡺ࡯࡮ࡣࡷࡩࠬಶ") if bstack11l1ll_opy_ (u"ࠧࡢࡲࡳࠫಷ") in CONFIG else bstack11l1ll_opy_ (u"ࠨࡣࡸࡸࡴࡳࡡࡵࡧࠪಸ")
      url = bstack11l1ll_opy_ (u"ࠩ࡫ࡸࡹࡶࡳ࠻࠱࠲ࡿࢂࡀࡻࡾࡂࡾࢁ࠳ࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮࠲ࡨࡵ࡭࠰ࡽࢀ࠳ࡧࡻࡩ࡭ࡦࡶ࠲࡯ࡹ࡯࡯ࠩಹ").format(user, key, host, bstack1l11l1ll_opy_)
      headers = {
        bstack11l1ll_opy_ (u"ࠪࡇࡴࡴࡴࡦࡰࡷ࠱ࡹࡿࡰࡦࠩ಺"): bstack11l1ll_opy_ (u"ࠫࡦࡶࡰ࡭࡫ࡦࡥࡹ࡯࡯࡯࠱࡭ࡷࡴࡴࠧ಻"),
      }
      if bstack11l1ll_opy_ (u"ࠬࡨࡵࡪ࡮ࡧࡍࡩ࡫࡮ࡵ࡫ࡩ࡭ࡪࡸ಼ࠧ") in CONFIG:
        params = {bstack11l1ll_opy_ (u"࠭࡮ࡢ࡯ࡨࠫಽ"): CONFIG[bstack11l1ll_opy_ (u"ࠧࡣࡷ࡬ࡰࡩࡔࡡ࡮ࡧࠪಾ")], bstack11l1ll_opy_ (u"ࠨࡤࡸ࡭ࡱࡪ࡟ࡪࡦࡨࡲࡹ࡯ࡦࡪࡧࡵࠫಿ"): CONFIG[bstack11l1ll_opy_ (u"ࠩࡥࡹ࡮ࡲࡤࡊࡦࡨࡲࡹ࡯ࡦࡪࡧࡵࠫೀ")]}
      else:
        params = {bstack11l1ll_opy_ (u"ࠪࡲࡦࡳࡥࠨು"): CONFIG[bstack11l1ll_opy_ (u"ࠫࡧࡻࡩ࡭ࡦࡑࡥࡲ࡫ࠧೂ")]}
      proxies = bstack1lll111111_opy_(CONFIG, url)
      response = requests.get(url, params=params, headers=headers, proxies=proxies)
      if response.json():
        bstack11ll11l11_opy_ = response.json()[0][bstack11l1ll_opy_ (u"ࠬࡧࡵࡵࡱࡰࡥࡹ࡯࡯࡯ࡡࡥࡹ࡮ࡲࡤࠨೃ")]
        if bstack11ll11l11_opy_:
          bstack11l11111l_opy_ = bstack11ll11l11_opy_[bstack11l1ll_opy_ (u"࠭ࡰࡶࡤ࡯࡭ࡨࡥࡵࡳ࡮ࠪೄ")].split(bstack11l1ll_opy_ (u"ࠧࡱࡷࡥࡰ࡮ࡩ࠭ࡣࡷ࡬ࡰࡩ࠭೅"))[0] + bstack11l1ll_opy_ (u"ࠨࡤࡸ࡭ࡱࡪࡳ࠰ࠩೆ") + bstack11ll11l11_opy_[
            bstack11l1ll_opy_ (u"ࠩ࡫ࡥࡸ࡮ࡥࡥࡡ࡬ࡨࠬೇ")]
          logger.info(bstack111l111l_opy_.format(bstack11l11111l_opy_))
          bstack111l1ll1_opy_ = bstack11ll11l11_opy_[bstack11l1ll_opy_ (u"ࠪ࡬ࡦࡹࡨࡦࡦࡢ࡭ࡩ࠭ೈ")]
          bstack1lll1l1111_opy_ = CONFIG[bstack11l1ll_opy_ (u"ࠫࡧࡻࡩ࡭ࡦࡑࡥࡲ࡫ࠧ೉")]
          if bstack11l1ll_opy_ (u"ࠬࡨࡵࡪ࡮ࡧࡍࡩ࡫࡮ࡵ࡫ࡩ࡭ࡪࡸࠧೊ") in CONFIG:
            bstack1lll1l1111_opy_ += bstack11l1ll_opy_ (u"࠭ࠠࠨೋ") + CONFIG[bstack11l1ll_opy_ (u"ࠧࡣࡷ࡬ࡰࡩࡏࡤࡦࡰࡷ࡭࡫࡯ࡥࡳࠩೌ")]
          if bstack1lll1l1111_opy_ != bstack11ll11l11_opy_[bstack11l1ll_opy_ (u"ࠨࡰࡤࡱࡪ್࠭")]:
            logger.debug(bstack11111l111_opy_.format(bstack11ll11l11_opy_[bstack11l1ll_opy_ (u"ࠩࡱࡥࡲ࡫ࠧ೎")], bstack1lll1l1111_opy_))
          return [bstack11ll11l11_opy_[bstack11l1ll_opy_ (u"ࠪ࡬ࡦࡹࡨࡦࡦࡢ࡭ࡩ࠭೏")], bstack11l11111l_opy_]
    else:
      logger.warn(bstack1llll11ll_opy_)
  except Exception as e:
    logger.debug(bstack1ll11l1lll_opy_.format(str(e)))
  return [None, None]
def bstack1lllllll1_opy_(url, bstack1lll1llll_opy_=False):
  global CONFIG
  global bstack1ll11l11l_opy_
  if not bstack1ll11l11l_opy_:
    hostname = bstack1l1ll11ll_opy_(url)
    is_private = bstack11ll1l1l_opy_(hostname)
    if (bstack11l1ll_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࡏࡳࡨࡧ࡬ࠨ೐") in CONFIG and not bstack111l1l1l1_opy_(CONFIG[bstack11l1ll_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࡐࡴࡩࡡ࡭ࠩ೑")])) and (is_private or bstack1lll1llll_opy_):
      bstack1ll11l11l_opy_ = hostname
def bstack1l1ll11ll_opy_(url):
  return urlparse(url).hostname
def bstack11ll1l1l_opy_(hostname):
  for bstack11l1lll1l_opy_ in bstack1lll1ll11_opy_:
    regex = re.compile(bstack11l1lll1l_opy_)
    if regex.match(hostname):
      return True
  return False
def bstack1llll11111_opy_(key_name):
  return True if key_name in threading.current_thread().__dict__.keys() else False
def getAccessibilityResults(driver):
  global CONFIG
  global bstack111lll111_opy_
  if not bstack1ll111l11_opy_.bstack1lll111lll_opy_(CONFIG, bstack111lll111_opy_):
    logger.warning(bstack11l1ll_opy_ (u"ࠨࡎࡰࡶࠣࡥࡳࠦࡁࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾࠦࡁࡶࡶࡲࡱࡦࡺࡩࡰࡰࠣࡷࡪࡹࡳࡪࡱࡱ࠰ࠥࡩࡡ࡯ࡰࡲࡸࠥࡸࡥࡵࡴ࡬ࡩࡻ࡫ࠠࡂࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿࠠࡳࡧࡶࡹࡱࡺࡳ࠯ࠤ೒"))
    return {}
  try:
    results = driver.execute_script(bstack11l1ll_opy_ (u"ࠢࠣࠤࠍࠤࠥࠦࠠࠡࠢࠣࠤࡷ࡫ࡴࡶࡴࡱࠤࡳ࡫ࡷࠡࡒࡵࡳࡲ࡯ࡳࡦࠪࡩࡹࡳࡩࡴࡪࡱࡱࠤ࠭ࡸࡥࡴࡱ࡯ࡺࡪ࠲ࠠࡳࡧ࡭ࡩࡨࡺࠩࠡࡽࠍࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࡶࡵࡽࠥࢁࠊࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࡦࡳࡳࡹࡴࠡࡧࡹࡩࡳࡺࠠ࠾ࠢࡱࡩࡼࠦࡃࡶࡵࡷࡳࡲࡋࡶࡦࡰࡷࠬࠬࡇ࠱࠲࡛ࡢࡘࡆࡖ࡟ࡈࡇࡗࡣࡗࡋࡓࡖࡎࡗࡗࠬ࠯࠻ࠋࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࡧࡴࡴࡳࡵࠢࡩࡲࠥࡃࠠࡧࡷࡱࡧࡹ࡯࡯࡯ࠢࠫࡩࡻ࡫࡮ࡵࠫࠣࡿࠏࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࡼ࡯࡮ࡥࡱࡺ࠲ࡷ࡫࡭ࡰࡸࡨࡉࡻ࡫࡮ࡵࡎ࡬ࡷࡹ࡫࡮ࡦࡴࠫࠫࡆ࠷࠱࡚ࡡࡕࡉࡘ࡛ࡌࡕࡕࡢࡖࡊ࡙ࡐࡐࡐࡖࡉࠬ࠲ࠠࡧࡰࠬ࠿ࠏࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࡷ࡫ࡳࡰ࡮ࡹࡩ࠭࡫ࡶࡦࡰࡷ࠲ࡩ࡫ࡴࡢ࡫࡯࠲ࡩࡧࡴࡢࠫ࠾ࠎࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࡽ࠼ࠌࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࡼ࡯࡮ࡥࡱࡺ࠲ࡦࡪࡤࡆࡸࡨࡲࡹࡒࡩࡴࡶࡨࡲࡪࡸࠨࠨࡃ࠴࠵࡞ࡥࡒࡆࡕࡘࡐ࡙࡙࡟ࡓࡇࡖࡔࡔࡔࡓࡆࠩ࠯ࠤ࡫ࡴࠩ࠼ࠌࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࡼ࡯࡮ࡥࡱࡺ࠲ࡩ࡯ࡳࡱࡣࡷࡧ࡭ࡋࡶࡦࡰࡷࠬࡪࡼࡥ࡯ࡶࠬ࠿ࠏࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࢁࠥࡩࡡࡵࡥ࡫ࠤࢀࠐࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࡴࡨ࡮ࡪࡩࡴࠩࠫ࠾ࠎࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࢀࠎࠥࠦࠠࠡࠢࠣࠤࠥࢃࠩ࠼ࠌࠣࠤࠥࠦࠢࠣࠤ೓"))
    return results
  except Exception:
    logger.error(bstack11l1ll_opy_ (u"ࠣࡐࡲࠤࡦࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࠤࡷ࡫ࡳࡶ࡮ࡷࡷࠥࡽࡥࡳࡧࠣࡪࡴࡻ࡮ࡥ࠰ࠥ೔"))
    return {}
def getAccessibilityResultsSummary(driver):
  global CONFIG
  global bstack111lll111_opy_
  if not bstack1ll111l11_opy_.bstack1lll111lll_opy_(CONFIG, bstack111lll111_opy_):
    logger.warning(bstack11l1ll_opy_ (u"ࠤࡑࡳࡹࠦࡡ࡯ࠢࡄࡧࡨ࡫ࡳࡴ࡫ࡥ࡭ࡱ࡯ࡴࡺࠢࡄࡹࡹࡵ࡭ࡢࡶ࡬ࡳࡳࠦࡳࡦࡵࡶ࡭ࡴࡴࠬࠡࡥࡤࡲࡳࡵࡴࠡࡴࡨࡸࡷ࡯ࡥࡷࡧࠣࡅࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࠣࡶࡪࡹࡵ࡭ࡶࡶࠤࡸࡻ࡭࡮ࡣࡵࡽ࠳ࠨೕ"))
    return {}
  try:
    bstack1l1l1111_opy_ = driver.execute_script(bstack11l1ll_opy_ (u"ࠥࠦࠧࠐࠠࠡࠢࠣࠤࠥࠦࠠࡳࡧࡷࡹࡷࡴࠠ࡯ࡧࡺࠤࡕࡸ࡯࡮࡫ࡶࡩ࠭࡬ࡵ࡯ࡥࡷ࡭ࡴࡴࠠࠩࡴࡨࡷࡴࡲࡶࡦ࠮ࠣࡶࡪࡰࡥࡤࡶࠬࠤࢀࠐࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࡹࡸࡹࠡࡽࠍࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࡩ࡯࡯ࡵࡷࠤࡪࡼࡥ࡯ࡶࠣࡁࠥࡴࡥࡸࠢࡆࡹࡸࡺ࡯࡮ࡇࡹࡩࡳࡺࠨࠨࡃ࠴࠵࡞ࡥࡔࡂࡒࡢࡋࡊ࡚࡟ࡓࡇࡖ࡙ࡑ࡚ࡓࡠࡕࡘࡑࡒࡇࡒ࡚ࠩࠬ࠿ࠏࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࡤࡱࡱࡷࡹࠦࡦ࡯ࠢࡀࠤ࡫ࡻ࡮ࡤࡶ࡬ࡳࡳࠦࠨࡦࡸࡨࡲࡹ࠯ࠠࡼࠌࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࡹ࡬ࡲࡩࡵࡷ࠯ࡴࡨࡱࡴࡼࡥࡆࡸࡨࡲࡹࡒࡩࡴࡶࡨࡲࡪࡸࠨࠨࡃ࠴࠵࡞ࡥࡒࡆࡕࡘࡐ࡙࡙࡟ࡔࡗࡐࡑࡆࡘ࡙ࡠࡔࡈࡗࡕࡕࡎࡔࡇࠪ࠰ࠥ࡬࡮ࠪ࠽ࠍࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࡵࡩࡸࡵ࡬ࡷࡧࠫࡩࡻ࡫࡮ࡵ࠰ࡧࡩࡹࡧࡩ࡭࠰ࡶࡹࡲࡳࡡࡳࡻࠬ࠿ࠏࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࡾ࠽ࠍࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࡽࡩ࡯ࡦࡲࡻ࠳ࡧࡤࡥࡇࡹࡩࡳࡺࡌࡪࡵࡷࡩࡳ࡫ࡲࠩࠩࡄ࠵࠶࡟࡟ࡓࡇࡖ࡙ࡑ࡚ࡓࡠࡕࡘࡑࡒࡇࡒ࡚ࡡࡕࡉࡘࡖࡏࡏࡕࡈࠫ࠱ࠦࡦ࡯ࠫ࠾ࠎࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࡷࡪࡰࡧࡳࡼ࠴ࡤࡪࡵࡳࡥࡹࡩࡨࡆࡸࡨࡲࡹ࠮ࡥࡷࡧࡱࡸ࠮ࡁࠊࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࢃࠠࡤࡣࡷࡧ࡭ࠦࡻࠋࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࡶࡪࡰࡥࡤࡶࠫ࠭ࡀࠐࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࢂࠐࠠࠡࠢࠣࠤࠥࠦࠠࡾࠫ࠾ࠎࠥࠦࠠࠡࠤࠥࠦೖ"))
    return bstack1l1l1111_opy_
  except Exception:
    logger.error(bstack11l1ll_opy_ (u"ࠦࡓࡵࠠࡢࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿࠠࡴࡷࡰࡱࡦࡸࡹࠡࡹࡤࡷࠥ࡬࡯ࡶࡰࡧ࠲ࠧ೗"))
    return {}