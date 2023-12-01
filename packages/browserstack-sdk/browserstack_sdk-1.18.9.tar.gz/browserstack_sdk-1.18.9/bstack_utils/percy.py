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
import re
import sys
import json
import time
import shutil
import tempfile
import requests
import subprocess
from threading import Thread
from os.path import expanduser
from bstack_utils.constants import *
from requests.auth import HTTPBasicAuth
from bstack_utils.helper import bstack1ll111l111_opy_, bstack1111l1lll_opy_
class bstack1ll1l1l11_opy_:
  working_dir = os.getcwd()
  bstack1ll1l11l1l_opy_ = False
  config = {}
  binary_path = bstack11l1ll_opy_ (u"ࠨࠩኵ")
  bstack11l11l11l1_opy_ = bstack11l1ll_opy_ (u"ࠩࠪ኶")
  bstack111lll1lll_opy_ = False
  bstack11l1l111ll_opy_ = None
  bstack11l1l11111_opy_ = {}
  bstack11l11l11ll_opy_ = 300
  bstack11l1111111_opy_ = False
  logger = None
  bstack11l11111l1_opy_ = False
  bstack111llll111_opy_ = bstack11l1ll_opy_ (u"ࠪࠫ኷")
  bstack111lllll1l_opy_ = {
    bstack11l1ll_opy_ (u"ࠫࡨ࡮ࡲࡰ࡯ࡨࠫኸ") : 1,
    bstack11l1ll_opy_ (u"ࠬ࡬ࡩࡳࡧࡩࡳࡽ࠭ኹ") : 2,
    bstack11l1ll_opy_ (u"࠭ࡥࡥࡩࡨࠫኺ") : 3,
    bstack11l1ll_opy_ (u"ࠧࡴࡣࡩࡥࡷ࡯ࠧኻ") : 4
  }
  def __init__(self) -> None: pass
  def bstack11l1111ll1_opy_(self):
    bstack11l11l1111_opy_ = bstack11l1ll_opy_ (u"ࠨࠩኼ")
    bstack11l111ll11_opy_ = sys.platform
    bstack11l1l111l1_opy_ = bstack11l1ll_opy_ (u"ࠩࡳࡩࡷࡩࡹࠨኽ")
    if re.match(bstack11l1ll_opy_ (u"ࠥࡨࡦࡸࡷࡪࡰࡿࡱࡦࡩࠠࡰࡵࠥኾ"), bstack11l111ll11_opy_) != None:
      bstack11l11l1111_opy_ = bstack11lll1lll1_opy_ + bstack11l1ll_opy_ (u"ࠦ࠴ࡶࡥࡳࡥࡼ࠱ࡴࡹࡸ࠯ࡼ࡬ࡴࠧ኿")
      self.bstack111llll111_opy_ = bstack11l1ll_opy_ (u"ࠬࡳࡡࡤࠩዀ")
    elif re.match(bstack11l1ll_opy_ (u"ࠨ࡭ࡴࡹ࡬ࡲࢁࡳࡳࡺࡵࡿࡱ࡮ࡴࡧࡸࡾࡦࡽ࡬ࡽࡩ࡯ࡾࡥࡧࡨࡽࡩ࡯ࡾࡺ࡭ࡳࡩࡥࡽࡧࡰࡧࢁࡽࡩ࡯࠵࠵ࠦ዁"), bstack11l111ll11_opy_) != None:
      bstack11l11l1111_opy_ = bstack11lll1lll1_opy_ + bstack11l1ll_opy_ (u"ࠢ࠰ࡲࡨࡶࡨࡿ࠭ࡸ࡫ࡱ࠲ࡿ࡯ࡰࠣዂ")
      bstack11l1l111l1_opy_ = bstack11l1ll_opy_ (u"ࠣࡲࡨࡶࡨࡿ࠮ࡦࡺࡨࠦዃ")
      self.bstack111llll111_opy_ = bstack11l1ll_opy_ (u"ࠩࡺ࡭ࡳ࠭ዄ")
    else:
      bstack11l11l1111_opy_ = bstack11lll1lll1_opy_ + bstack11l1ll_opy_ (u"ࠥ࠳ࡵ࡫ࡲࡤࡻ࠰ࡰ࡮ࡴࡵࡹ࠰ࡽ࡭ࡵࠨዅ")
      self.bstack111llll111_opy_ = bstack11l1ll_opy_ (u"ࠫࡱ࡯࡮ࡶࡺࠪ዆")
    return bstack11l11l1111_opy_, bstack11l1l111l1_opy_
  def bstack11l11ll1l1_opy_(self):
    try:
      bstack111lll1l1l_opy_ = [os.path.join(expanduser(bstack11l1ll_opy_ (u"ࠧࢄࠢ዇")), bstack11l1ll_opy_ (u"࠭࠮ࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠭ወ")), self.working_dir, tempfile.gettempdir()]
      for path in bstack111lll1l1l_opy_:
        if(self.bstack11l11ll11l_opy_(path)):
          return path
      raise bstack11l1ll_opy_ (u"ࠢࡖࡰࡤࡰࡧ࡫ࠠࡵࡱࠣࡨࡴࡽ࡮࡭ࡱࡤࡨࠥࡶࡥࡳࡥࡼࠤࡧ࡯࡮ࡢࡴࡼࠦዉ")
    except Exception as e:
      self.logger.error(bstack11l1ll_opy_ (u"ࠣࡈࡤ࡭ࡱ࡫ࡤࠡࡶࡲࠤ࡫࡯࡮ࡥࠢࡤࡺࡦ࡯࡬ࡢࡤ࡯ࡩࠥࡶࡡࡵࡪࠣࡪࡴࡸࠠࡱࡧࡵࡧࡾࠦࡤࡰࡹࡱࡰࡴࡧࡤ࠭ࠢࡈࡼࡨ࡫ࡰࡵ࡫ࡲࡲࠥ࠳ࠠࡼࡿࠥዊ").format(e))
  def bstack11l11ll11l_opy_(self, path):
    try:
      if not os.path.exists(path):
        os.makedirs(path)
      return True
    except:
      return False
  def bstack111llll1ll_opy_(self, bstack11l11l1111_opy_, bstack11l1l111l1_opy_):
    try:
      bstack111llll11l_opy_ = self.bstack11l11ll1l1_opy_()
      bstack11l11llll1_opy_ = os.path.join(bstack111llll11l_opy_, bstack11l1ll_opy_ (u"ࠩࡳࡩࡷࡩࡹ࠯ࡼ࡬ࡴࠬዋ"))
      bstack11l11ll1ll_opy_ = os.path.join(bstack111llll11l_opy_, bstack11l1l111l1_opy_)
      if os.path.exists(bstack11l11ll1ll_opy_):
        self.logger.info(bstack11l1ll_opy_ (u"ࠥࡔࡪࡸࡣࡺࠢࡥ࡭ࡳࡧࡲࡺࠢࡩࡳࡺࡴࡤࠡ࡫ࡱࠤࢀࢃࠬࠡࡵ࡮࡭ࡵࡶࡩ࡯ࡩࠣࡨࡴࡽ࡮࡭ࡱࡤࡨࠧዌ").format(bstack11l11ll1ll_opy_))
        return bstack11l11ll1ll_opy_
      if os.path.exists(bstack11l11llll1_opy_):
        self.logger.info(bstack11l1ll_opy_ (u"ࠦࡕ࡫ࡲࡤࡻࠣࡾ࡮ࡶࠠࡧࡱࡸࡲࡩࠦࡩ࡯ࠢࡾࢁ࠱ࠦࡵ࡯ࡼ࡬ࡴࡵ࡯࡮ࡨࠤው").format(bstack11l11llll1_opy_))
        return self.bstack11l111l1ll_opy_(bstack11l11llll1_opy_, bstack11l1l111l1_opy_)
      self.logger.info(bstack11l1ll_opy_ (u"ࠧࡊ࡯ࡸࡰ࡯ࡳࡦࡪࡩ࡯ࡩࠣࡴࡪࡸࡣࡺࠢࡥ࡭ࡳࡧࡲࡺࠢࡩࡶࡴࡳࠠࡼࡿࠥዎ").format(bstack11l11l1111_opy_))
      response = bstack1111l1lll_opy_(bstack11l1ll_opy_ (u"࠭ࡇࡆࡖࠪዏ"), bstack11l11l1111_opy_, {}, {})
      if response.status_code == 200:
        with open(bstack11l11llll1_opy_, bstack11l1ll_opy_ (u"ࠧࡸࡤࠪዐ")) as file:
          file.write(response.content)
        self.logger.info(bstack11l111l11l_opy_ (u"ࠣࡆࡲࡻࡳࡲ࡯ࡢࡦࡨࡨࠥࡶࡥࡳࡥࡼࠤࡧ࡯࡮ࡢࡴࡼࠤࡦࡴࡤࠡࡵࡤࡺࡪࡪࠠࡢࡶࠣࡿࡧ࡯࡮ࡢࡴࡼࡣࡿ࡯ࡰࡠࡲࡤࡸ࡭ࢃࠢዑ"))
        return self.bstack11l111l1ll_opy_(bstack11l11llll1_opy_, bstack11l1l111l1_opy_)
      else:
        raise(bstack11l111l11l_opy_ (u"ࠤࡉࡥ࡮ࡲࡥࡥࠢࡷࡳࠥࡪ࡯ࡸࡰ࡯ࡳࡦࡪࠠࡵࡪࡨࠤ࡫࡯࡬ࡦ࠰ࠣࡗࡹࡧࡴࡶࡵࠣࡧࡴࡪࡥ࠻ࠢࡾࡶࡪࡹࡰࡰࡰࡶࡩ࠳ࡹࡴࡢࡶࡸࡷࡤࡩ࡯ࡥࡧࢀࠦዒ"))
    except:
      self.logger.error(bstack11l1ll_opy_ (u"࡙ࠥࡳࡧࡢ࡭ࡧࠣࡸࡴࠦࡤࡰࡹࡱࡰࡴࡧࡤࠡࡲࡨࡶࡨࡿࠠࡣ࡫ࡱࡥࡷࡿࠢዓ"))
  def bstack11l11l1lll_opy_(self, bstack11l11l1111_opy_, bstack11l1l111l1_opy_):
    try:
      bstack11l11ll1ll_opy_ = self.bstack111llll1ll_opy_(bstack11l11l1111_opy_, bstack11l1l111l1_opy_)
      bstack11l111111l_opy_ = self.bstack11l11lll11_opy_(bstack11l11l1111_opy_, bstack11l1l111l1_opy_, bstack11l11ll1ll_opy_)
      return bstack11l11ll1ll_opy_, bstack11l111111l_opy_
    except Exception as e:
      self.logger.error(bstack11l1ll_opy_ (u"࡚ࠦࡴࡡࡣ࡮ࡨࠤࡹࡵࠠࡨࡧࡷࠤࡵ࡫ࡲࡤࡻࠣࡦ࡮ࡴࡡࡳࡻࠣࡴࡦࡺࡨࠣዔ").format(e))
    return bstack11l11ll1ll_opy_, False
  def bstack11l11lll11_opy_(self, bstack11l11l1111_opy_, bstack11l1l111l1_opy_, bstack11l11ll1ll_opy_, bstack11l1l11l11_opy_ = 0):
    if bstack11l1l11l11_opy_ > 1:
      return False
    if bstack11l11ll1ll_opy_ == None or os.path.exists(bstack11l11ll1ll_opy_) == False:
      self.logger.warn(bstack11l1ll_opy_ (u"ࠧࡖࡥࡳࡥࡼࠤࡵࡧࡴࡩࠢࡱࡳࡹࠦࡦࡰࡷࡱࡨ࠱ࠦࡲࡦࡶࡵࡽ࡮ࡴࡧࠡࡦࡲࡻࡳࡲ࡯ࡢࡦࠥዕ"))
      bstack11l11ll1ll_opy_ = self.bstack111llll1ll_opy_(bstack11l11l1111_opy_, bstack11l1l111l1_opy_)
      self.bstack11l11lll11_opy_(bstack11l11l1111_opy_, bstack11l1l111l1_opy_, bstack11l11ll1ll_opy_, bstack11l1l11l11_opy_+1)
    bstack11l1111lll_opy_ = bstack11l1ll_opy_ (u"ࠨ࡞࠯ࠬࡃࡴࡪࡸࡣࡺ࡞࠲ࡧࡱ࡯ࠠ࡝ࡦ࠱ࡠࡩ࠱࠮࡝ࡦ࠮ࠦዖ")
    command = bstack11l1ll_opy_ (u"ࠧࡼࡿࠣ࠱࠲ࡼࡥࡳࡵ࡬ࡳࡳ࠭዗").format(bstack11l11ll1ll_opy_)
    bstack111lll11l1_opy_ = subprocess.check_output(command, shell=True, text=True)
    if re.match(bstack11l1111lll_opy_, bstack111lll11l1_opy_) != None:
      return True
    else:
      self.logger.error(bstack11l1ll_opy_ (u"ࠣࡒࡨࡶࡨࡿࠠࡷࡧࡵࡷ࡮ࡵ࡮ࠡࡥ࡫ࡩࡨࡱࠠࡧࡣ࡬ࡰࡪࡪࠢዘ"))
      bstack11l11ll1ll_opy_ = self.bstack111llll1ll_opy_(bstack11l11l1111_opy_, bstack11l1l111l1_opy_)
      self.bstack11l11lll11_opy_(bstack11l11l1111_opy_, bstack11l1l111l1_opy_, bstack11l11ll1ll_opy_, bstack11l1l11l11_opy_+1)
  def bstack11l111l1ll_opy_(self, bstack11l11llll1_opy_, bstack11l1l111l1_opy_):
    try:
      working_dir = os.path.dirname(bstack11l11llll1_opy_)
      shutil.unpack_archive(bstack11l11llll1_opy_, working_dir)
      bstack11l11ll1ll_opy_ = os.path.join(working_dir, bstack11l1l111l1_opy_)
      os.chmod(bstack11l11ll1ll_opy_, 0o755)
      return bstack11l11ll1ll_opy_
    except Exception as e:
      self.logger.error(bstack11l1ll_opy_ (u"ࠤࡘࡲࡦࡨ࡬ࡦࠢࡷࡳࠥࡻ࡮ࡻ࡫ࡳࠤࡵ࡫ࡲࡤࡻࠣࡦ࡮ࡴࡡࡳࡻࠥዙ"))
  def bstack11l1111l1l_opy_(self):
    try:
      percy = str(self.config.get(bstack11l1ll_opy_ (u"ࠪࡴࡪࡸࡣࡺࠩዚ"), bstack11l1ll_opy_ (u"ࠦ࡫ࡧ࡬ࡴࡧࠥዛ"))).lower()
      if percy != bstack11l1ll_opy_ (u"ࠧࡺࡲࡶࡧࠥዜ"):
        return False
      self.bstack111lll1lll_opy_ = True
      return True
    except Exception as e:
      self.logger.error(bstack11l1ll_opy_ (u"ࠨࡕ࡯ࡣࡥࡰࡪࠦࡴࡰࠢࡧࡩࡹ࡫ࡣࡵࠢࡳࡩࡷࡩࡹ࠭ࠢࡈࡼࡨ࡫ࡰࡵ࡫ࡲࡲࠥࢁࡽࠣዝ").format(e))
  def init(self, bstack1ll1l11l1l_opy_, config, logger):
    self.bstack1ll1l11l1l_opy_ = bstack1ll1l11l1l_opy_
    self.config = config
    self.logger = logger
    if not self.bstack11l1111l1l_opy_():
      return
    self.bstack11l1l11111_opy_ = config.get(bstack11l1ll_opy_ (u"ࠧࡱࡧࡵࡧࡾࡕࡰࡵ࡫ࡲࡲࡸ࠭ዞ"), {})
    try:
      bstack11l11l1111_opy_, bstack11l1l111l1_opy_ = self.bstack11l1111ll1_opy_()
      bstack11l11ll1ll_opy_, bstack11l111111l_opy_ = self.bstack11l11l1lll_opy_(bstack11l11l1111_opy_, bstack11l1l111l1_opy_)
      if bstack11l111111l_opy_:
        self.binary_path = bstack11l11ll1ll_opy_
        thread = Thread(target=self.bstack11l111ll1l_opy_)
        thread.start()
      else:
        self.bstack11l11111l1_opy_ = True
        self.logger.error(bstack11l1ll_opy_ (u"ࠣࡋࡱࡺࡦࡲࡩࡥࠢࡳࡩࡷࡩࡹࠡࡲࡤࡸ࡭ࠦࡦࡰࡷࡱࡨࠥ࠳ࠠࡼࡿ࠯ࠤ࡚ࡴࡡࡣ࡮ࡨࠤࡹࡵࠠࡴࡶࡤࡶࡹࠦࡐࡦࡴࡦࡽࠧዟ").format(bstack11l11ll1ll_opy_))
    except Exception as e:
      self.logger.error(bstack11l1ll_opy_ (u"ࠤࡘࡲࡦࡨ࡬ࡦࠢࡷࡳࠥࡹࡴࡢࡴࡷࠤࡵ࡫ࡲࡤࡻ࠯ࠤࡊࡾࡣࡦࡲࡷ࡭ࡴࡴࠠࡼࡿࠥዠ").format(e))
  def bstack11l1l1111l_opy_(self):
    try:
      logfile = os.path.join(self.working_dir, bstack11l1ll_opy_ (u"ࠪࡰࡴ࡭ࠧዡ"), bstack11l1ll_opy_ (u"ࠫࡵ࡫ࡲࡤࡻ࠱ࡰࡴ࡭ࠧዢ"))
      os.makedirs(os.path.dirname(logfile)) if not os.path.exists(os.path.dirname(logfile)) else None
      self.logger.debug(bstack11l1ll_opy_ (u"ࠧࡖࡵࡴࡪ࡬ࡲ࡬ࠦࡰࡦࡴࡦࡽࠥࡲ࡯ࡨࡵࠣࡥࡹࠦࡻࡾࠤዣ").format(logfile))
      self.bstack11l11l11l1_opy_ = logfile
    except Exception as e:
      self.logger.error(bstack11l1ll_opy_ (u"ࠨࡕ࡯ࡣࡥࡰࡪࠦࡴࡰࠢࡶࡩࡹࠦࡰࡦࡴࡦࡽࠥࡲ࡯ࡨࠢࡳࡥࡹ࡮ࠬࠡࡇࡻࡧࡪࡶࡴࡪࡱࡱࠤࢀࢃࠢዤ").format(e))
  def bstack11l111ll1l_opy_(self):
    bstack11l11lllll_opy_ = self.bstack11l11ll111_opy_()
    if bstack11l11lllll_opy_ == None:
      self.bstack11l11111l1_opy_ = True
      self.logger.error(bstack11l1ll_opy_ (u"ࠢࡑࡧࡵࡧࡾࠦࡴࡰ࡭ࡨࡲࠥࡴ࡯ࡵࠢࡩࡳࡺࡴࡤ࠭ࠢࡉࡥ࡮ࡲࡥࡥࠢࡷࡳࠥࡹࡴࡢࡴࡷࠤࡵ࡫ࡲࡤࡻࠥዥ"))
      return False
    command_args = [bstack11l1ll_opy_ (u"ࠣࡣࡳࡴ࠿࡫ࡸࡦࡥ࠽ࡷࡹࡧࡲࡵࠤዦ") if self.bstack1ll1l11l1l_opy_ else bstack11l1ll_opy_ (u"ࠩࡨࡼࡪࡩ࠺ࡴࡶࡤࡶࡹ࠭ዧ")]
    bstack111lll1ll1_opy_ = self.bstack11l111llll_opy_()
    if bstack111lll1ll1_opy_ != None:
      command_args.append(bstack11l1ll_opy_ (u"ࠥ࠱ࡨࠦࡻࡾࠤየ").format(bstack111lll1ll1_opy_))
    env = os.environ.copy()
    env[bstack11l1ll_opy_ (u"ࠦࡕࡋࡒࡄ࡛ࡢࡘࡔࡑࡅࡏࠤዩ")] = bstack11l11lllll_opy_
    bstack11l1l11l1l_opy_ = [self.binary_path]
    self.bstack11l1l1111l_opy_()
    self.bstack11l1l111ll_opy_ = self.bstack111llll1l1_opy_(bstack11l1l11l1l_opy_ + command_args, env)
    self.logger.debug(bstack11l1ll_opy_ (u"࡙ࠧࡴࡢࡴࡷ࡭ࡳ࡭ࠠࡉࡧࡤࡰࡹ࡮ࠠࡄࡪࡨࡧࡰࠨዪ"))
    bstack11l1l11l11_opy_ = 0
    while self.bstack11l1l111ll_opy_.poll() == None:
      bstack11l11l1l1l_opy_ = self.bstack111lllll11_opy_()
      if bstack11l11l1l1l_opy_:
        self.logger.debug(bstack11l1ll_opy_ (u"ࠨࡈࡦࡣ࡯ࡸ࡭ࠦࡃࡩࡧࡦ࡯ࠥࡹࡵࡤࡥࡨࡷࡸ࡬ࡵ࡭ࠤያ"))
        self.bstack11l1111111_opy_ = True
        return True
      bstack11l1l11l11_opy_ += 1
      self.logger.debug(bstack11l1ll_opy_ (u"ࠢࡉࡧࡤࡰࡹ࡮ࠠࡄࡪࡨࡧࡰࠦࡒࡦࡶࡵࡽࠥ࠳ࠠࡼࡿࠥዬ").format(bstack11l1l11l11_opy_))
      time.sleep(2)
    self.logger.error(bstack11l1ll_opy_ (u"ࠣࡈࡤ࡭ࡱ࡫ࡤࠡࡶࡲࠤࡸࡺࡡࡳࡶࠣࡴࡪࡸࡣࡺ࠮ࠣࡌࡪࡧ࡬ࡵࡪࠣࡇ࡭࡫ࡣ࡬ࠢࡉࡥ࡮ࡲࡥࡥࠢࡤࡪࡹ࡫ࡲࠡࡽࢀࠤࡦࡺࡴࡦ࡯ࡳࡸࡸࠨይ").format(bstack11l1l11l11_opy_))
    self.bstack11l11111l1_opy_ = True
    return False
  def bstack111lllll11_opy_(self, bstack11l1l11l11_opy_ = 0):
    try:
      if bstack11l1l11l11_opy_ > 10:
        return False
      bstack111llllll1_opy_ = os.environ.get(bstack11l1ll_opy_ (u"ࠩࡓࡉࡗࡉ࡙ࡠࡕࡈࡖ࡛ࡋࡒࡠࡃࡇࡈࡗࡋࡓࡔࠩዮ"), bstack11l1ll_opy_ (u"ࠪ࡬ࡹࡺࡰ࠻࠱࠲ࡰࡴࡩࡡ࡭ࡪࡲࡷࡹࡀ࠵࠴࠵࠻ࠫዯ"))
      bstack111lll1l11_opy_ = bstack111llllll1_opy_ + bstack11llll111l_opy_
      response = requests.get(bstack111lll1l11_opy_)
      return True if response.json() else False
    except:
      return False
  def bstack11l11ll111_opy_(self):
    bstack11l11lll1l_opy_ = bstack11l1ll_opy_ (u"ࠫࡦࡶࡰࠨደ") if self.bstack1ll1l11l1l_opy_ else bstack11l1ll_opy_ (u"ࠬࡧࡵࡵࡱࡰࡥࡹ࡫ࠧዱ")
    bstack11l1llll1l_opy_ = bstack11l1ll_opy_ (u"ࠨࡡࡱ࡫࠲ࡥࡵࡶ࡟ࡱࡧࡵࡧࡾ࠵ࡧࡦࡶࡢࡴࡷࡵࡪࡦࡥࡷࡣࡹࡵ࡫ࡦࡰࡂࡲࡦࡳࡥ࠾ࡽࢀࠪࡹࡿࡰࡦ࠿ࡾࢁࠧዲ").format(self.config[bstack11l1ll_opy_ (u"ࠧࡱࡴࡲ࡮ࡪࡩࡴࡏࡣࡰࡩࠬዳ")], bstack11l11lll1l_opy_)
    uri = bstack1ll111l111_opy_(bstack11l1llll1l_opy_)
    try:
      response = bstack1111l1lll_opy_(bstack11l1ll_opy_ (u"ࠨࡉࡈࡘࠬዴ"), uri, {}, {bstack11l1ll_opy_ (u"ࠩࡤࡹࡹ࡮ࠧድ"): (self.config[bstack11l1ll_opy_ (u"ࠪࡹࡸ࡫ࡲࡏࡣࡰࡩࠬዶ")], self.config[bstack11l1ll_opy_ (u"ࠫࡦࡩࡣࡦࡵࡶࡏࡪࡿࠧዷ")])})
      if response.status_code == 200:
        bstack111lllllll_opy_ = response.json()
        if bstack11l1ll_opy_ (u"ࠧࡺ࡯࡬ࡧࡱࠦዸ") in bstack111lllllll_opy_:
          return bstack111lllllll_opy_[bstack11l1ll_opy_ (u"ࠨࡴࡰ࡭ࡨࡲࠧዹ")]
        else:
          raise bstack11l1ll_opy_ (u"ࠧࡕࡱ࡮ࡩࡳࠦࡎࡰࡶࠣࡊࡴࡻ࡮ࡥࠢ࠰ࠤࢀࢃࠧዺ").format(bstack111lllllll_opy_)
      else:
        raise bstack11l1ll_opy_ (u"ࠣࡈࡤ࡭ࡱ࡫ࡤࠡࡶࡲࠤ࡫࡫ࡴࡤࡪࠣࡴࡪࡸࡣࡺࠢࡷࡳࡰ࡫࡮࠭ࠢࡕࡩࡸࡶ࡯࡯ࡵࡨࠤࡸࡺࡡࡵࡷࡶࠤ࠲ࠦࡻࡾ࠮ࠣࡖࡪࡹࡰࡰࡰࡶࡩࠥࡈ࡯ࡥࡻࠣ࠱ࠥࢁࡽࠣዻ").format(response.status_code, response.json())
    except Exception as e:
      self.logger.error(bstack11l1ll_opy_ (u"ࠤࡈࡼࡨ࡫ࡰࡵ࡫ࡲࡲࠥ࡯࡮ࠡࡥࡵࡩࡦࡺࡩ࡯ࡩࠣࡴࡪࡸࡣࡺࠢࡳࡶࡴࡰࡥࡤࡶࠥዼ").format(e))
  def bstack11l111llll_opy_(self):
    bstack11l111l111_opy_ = os.path.join(tempfile.gettempdir(), bstack11l1ll_opy_ (u"ࠥࡴࡪࡸࡣࡺࡅࡲࡲ࡫࡯ࡧ࠯࡬ࡶࡳࡳࠨዽ"))
    try:
      if bstack11l1ll_opy_ (u"ࠫࡻ࡫ࡲࡴ࡫ࡲࡲࠬዾ") not in self.bstack11l1l11111_opy_:
        self.bstack11l1l11111_opy_[bstack11l1ll_opy_ (u"ࠬࡼࡥࡳࡵ࡬ࡳࡳ࠭ዿ")] = 2
      with open(bstack11l111l111_opy_, bstack11l1ll_opy_ (u"࠭ࡷࠨጀ")) as fp:
        json.dump(self.bstack11l1l11111_opy_, fp)
      return bstack11l111l111_opy_
    except Exception as e:
      self.logger.error(bstack11l1ll_opy_ (u"ࠢࡖࡰࡤࡦࡱ࡫ࠠࡵࡱࠣࡧࡷ࡫ࡡࡵࡧࠣࡴࡪࡸࡣࡺࠢࡦࡳࡳ࡬ࠬࠡࡇࡻࡧࡪࡶࡴࡪࡱࡱࠤࢀࢃࠢጁ").format(e))
  def bstack111llll1l1_opy_(self, cmd, env = os.environ.copy()):
    try:
      if self.bstack111llll111_opy_ == bstack11l1ll_opy_ (u"ࠨࡹ࡬ࡲࠬጂ"):
        bstack11l111lll1_opy_ = [bstack11l1ll_opy_ (u"ࠩࡦࡱࡩ࠴ࡥࡹࡧࠪጃ"), bstack11l1ll_opy_ (u"ࠪ࠳ࡨ࠭ጄ")]
        cmd = bstack11l111lll1_opy_ + cmd
      cmd = bstack11l1ll_opy_ (u"ࠫࠥ࠭ጅ").join(cmd)
      self.logger.debug(bstack11l1ll_opy_ (u"ࠧࡘࡵ࡯ࡰ࡬ࡲ࡬ࠦࡻࡾࠤጆ").format(cmd))
      with open(self.bstack11l11l11l1_opy_, bstack11l1ll_opy_ (u"ࠨࡡࠣጇ")) as bstack11l111l1l1_opy_:
        process = subprocess.Popen(cmd, shell=True, stdout=bstack11l111l1l1_opy_, text=True, stderr=bstack11l111l1l1_opy_, env=env, universal_newlines=True)
      return process
    except Exception as e:
      self.bstack11l11111l1_opy_ = True
      self.logger.error(bstack11l1ll_opy_ (u"ࠢࡇࡣ࡬ࡰࡪࡪࠠࡵࡱࠣࡷࡹࡧࡲࡵࠢࡳࡩࡷࡩࡹࠡࡹ࡬ࡸ࡭ࠦࡣ࡮ࡦࠣ࠱ࠥࢁࡽ࠭ࠢࡈࡼࡨ࡫ࡰࡵ࡫ࡲࡲ࠿ࠦࡻࡾࠤገ").format(cmd, e))
  def shutdown(self):
    try:
      if self.bstack11l1111111_opy_:
        self.logger.info(bstack11l1ll_opy_ (u"ࠣࡕࡷࡳࡵࡶࡩ࡯ࡩࠣࡔࡪࡸࡣࡺࠤጉ"))
        cmd = [self.binary_path, bstack11l1ll_opy_ (u"ࠤࡨࡼࡪࡩ࠺ࡴࡶࡲࡴࠧጊ")]
        self.bstack111llll1l1_opy_(cmd)
        self.bstack11l1111111_opy_ = False
    except Exception as e:
      self.logger.error(bstack11l1ll_opy_ (u"ࠥࡊࡦ࡯࡬ࡦࡦࠣࡸࡴࠦࡳࡵࡱࡳࠤࡸ࡫ࡳࡴ࡫ࡲࡲࠥࡽࡩࡵࡪࠣࡧࡴࡳ࡭ࡢࡰࡧࠤ࠲ࠦࡻࡾ࠮ࠣࡉࡽࡩࡥࡱࡶ࡬ࡳࡳࡀࠠࡼࡿࠥጋ").format(cmd, e))
  def bstack1l1llll111_opy_(self):
    if not self.bstack111lll1lll_opy_:
      return
    try:
      bstack11l11111ll_opy_ = 0
      while not self.bstack11l1111111_opy_ and bstack11l11111ll_opy_ < self.bstack11l11l11ll_opy_:
        if self.bstack11l11111l1_opy_:
          self.logger.info(bstack11l1ll_opy_ (u"ࠦࡕ࡫ࡲࡤࡻࠣࡷࡪࡺࡵࡱࠢࡩࡥ࡮ࡲࡥࡥࠤጌ"))
          return
        time.sleep(1)
        bstack11l11111ll_opy_ += 1
      os.environ[bstack11l1ll_opy_ (u"ࠬࡖࡅࡓࡅ࡜ࡣࡇࡋࡓࡕࡡࡓࡐࡆ࡚ࡆࡐࡔࡐࠫግ")] = str(self.bstack11l1111l11_opy_())
      self.logger.info(bstack11l1ll_opy_ (u"ࠨࡐࡦࡴࡦࡽࠥࡹࡥࡵࡷࡳࠤࡨࡵ࡭ࡱ࡮ࡨࡸࡪࡪࠢጎ"))
    except Exception as e:
      self.logger.error(bstack11l1ll_opy_ (u"ࠢࡖࡰࡤࡦࡱ࡫ࠠࡵࡱࠣࡷࡪࡺࡵࡱࠢࡳࡩࡷࡩࡹ࠭ࠢࡈࡼࡨ࡫ࡰࡵ࡫ࡲࡲࠥࢁࡽࠣጏ").format(e))
  def bstack11l1111l11_opy_(self):
    if self.bstack1ll1l11l1l_opy_:
      return
    try:
      bstack11l11l1l11_opy_ = [platform[bstack11l1ll_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡐࡤࡱࡪ࠭ጐ")].lower() for platform in self.config.get(bstack11l1ll_opy_ (u"ࠩࡳࡰࡦࡺࡦࡰࡴࡰࡷࠬ጑"), [])]
      bstack11l11l1ll1_opy_ = sys.maxsize
      bstack11l11l111l_opy_ = bstack11l1ll_opy_ (u"ࠪࠫጒ")
      for browser in bstack11l11l1l11_opy_:
        if browser in self.bstack111lllll1l_opy_:
          bstack111lll11ll_opy_ = self.bstack111lllll1l_opy_[browser]
        if bstack111lll11ll_opy_ < bstack11l11l1ll1_opy_:
          bstack11l11l1ll1_opy_ = bstack111lll11ll_opy_
          bstack11l11l111l_opy_ = browser
      return bstack11l11l111l_opy_
    except Exception as e:
      self.logger.error(bstack11l1ll_opy_ (u"࡚ࠦࡴࡡࡣ࡮ࡨࠤࡹࡵࠠࡧ࡫ࡱࡨࠥࡨࡥࡴࡶࠣࡴࡱࡧࡴࡧࡱࡵࡱ࠱ࠦࡅࡹࡥࡨࡴࡹ࡯࡯࡯ࠢࡾࢁࠧጓ").format(e))