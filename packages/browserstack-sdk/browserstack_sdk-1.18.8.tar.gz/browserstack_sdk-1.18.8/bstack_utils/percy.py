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
from bstack_utils.helper import bstack1llllll1l1_opy_, bstack1ll11l1111_opy_
class bstack1ll111l1l1_opy_:
  working_dir = os.getcwd()
  bstack1ll111lll1_opy_ = False
  config = {}
  binary_path = bstack11l1l1l_opy_ (u"ࠬ࠭዇")
  bstack11l111l111_opy_ = bstack11l1l1l_opy_ (u"࠭ࠧወ")
  bstack11l11l11ll_opy_ = False
  bstack111lllll1l_opy_ = None
  bstack111lllll11_opy_ = {}
  bstack11l11ll1l1_opy_ = 300
  bstack11l111llll_opy_ = False
  logger = None
  bstack111llll1ll_opy_ = False
  bstack11l1111lll_opy_ = bstack11l1l1l_opy_ (u"ࠧࠨዉ")
  bstack11l111l11l_opy_ = {
    bstack11l1l1l_opy_ (u"ࠨࡥ࡫ࡶࡴࡳࡥࠨዊ") : 1,
    bstack11l1l1l_opy_ (u"ࠩࡩ࡭ࡷ࡫ࡦࡰࡺࠪዋ") : 2,
    bstack11l1l1l_opy_ (u"ࠪࡩࡩ࡭ࡥࠨዌ") : 3,
    bstack11l1l1l_opy_ (u"ࠫࡸࡧࡦࡢࡴ࡬ࠫው") : 4
  }
  def __init__(self) -> None: pass
  def bstack11l11111ll_opy_(self):
    bstack11l11ll111_opy_ = bstack11l1l1l_opy_ (u"ࠬ࠭ዎ")
    bstack11l1l111l1_opy_ = sys.platform
    bstack11l1111l11_opy_ = bstack11l1l1l_opy_ (u"࠭ࡰࡦࡴࡦࡽࠬዏ")
    if re.match(bstack11l1l1l_opy_ (u"ࠢࡥࡣࡵࡻ࡮ࡴࡼ࡮ࡣࡦࠤࡴࡹࠢዐ"), bstack11l1l111l1_opy_) != None:
      bstack11l11ll111_opy_ = bstack11llll11l1_opy_ + bstack11l1l1l_opy_ (u"ࠣ࠱ࡳࡩࡷࡩࡹ࠮ࡱࡶࡼ࠳ࢀࡩࡱࠤዑ")
      self.bstack11l1111lll_opy_ = bstack11l1l1l_opy_ (u"ࠩࡰࡥࡨ࠭ዒ")
    elif re.match(bstack11l1l1l_opy_ (u"ࠥࡱࡸࡽࡩ࡯ࡾࡰࡷࡾࡹࡼ࡮࡫ࡱ࡫ࡼࢂࡣࡺࡩࡺ࡭ࡳࢂࡢࡤࡥࡺ࡭ࡳࢂࡷࡪࡰࡦࡩࢁ࡫࡭ࡤࡾࡺ࡭ࡳ࠹࠲ࠣዓ"), bstack11l1l111l1_opy_) != None:
      bstack11l11ll111_opy_ = bstack11llll11l1_opy_ + bstack11l1l1l_opy_ (u"ࠦ࠴ࡶࡥࡳࡥࡼ࠱ࡼ࡯࡮࠯ࡼ࡬ࡴࠧዔ")
      bstack11l1111l11_opy_ = bstack11l1l1l_opy_ (u"ࠧࡶࡥࡳࡥࡼ࠲ࡪࡾࡥࠣዕ")
      self.bstack11l1111lll_opy_ = bstack11l1l1l_opy_ (u"࠭ࡷࡪࡰࠪዖ")
    else:
      bstack11l11ll111_opy_ = bstack11llll11l1_opy_ + bstack11l1l1l_opy_ (u"ࠢ࠰ࡲࡨࡶࡨࡿ࠭࡭࡫ࡱࡹࡽ࠴ࡺࡪࡲࠥ዗")
      self.bstack11l1111lll_opy_ = bstack11l1l1l_opy_ (u"ࠨ࡮࡬ࡲࡺࡾࠧዘ")
    return bstack11l11ll111_opy_, bstack11l1111l11_opy_
  def bstack111llll11l_opy_(self):
    try:
      bstack11l1l11111_opy_ = [os.path.join(expanduser(bstack11l1l1l_opy_ (u"ࠤࢁࠦዙ")), bstack11l1l1l_opy_ (u"ࠪ࠲ࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࠪዚ")), self.working_dir, tempfile.gettempdir()]
      for path in bstack11l1l11111_opy_:
        if(self.bstack11l1l11l1l_opy_(path)):
          return path
      raise bstack11l1l1l_opy_ (u"࡚ࠦࡴࡡ࡭ࡤࡨࠤࡹࡵࠠࡥࡱࡺࡲࡱࡵࡡࡥࠢࡳࡩࡷࡩࡹࠡࡤ࡬ࡲࡦࡸࡹࠣዛ")
    except Exception as e:
      self.logger.error(bstack11l1l1l_opy_ (u"ࠧࡌࡡࡪ࡮ࡨࡨࠥࡺ࡯ࠡࡨ࡬ࡲࡩࠦࡡࡷࡣ࡬ࡰࡦࡨ࡬ࡦࠢࡳࡥࡹ࡮ࠠࡧࡱࡵࠤࡵ࡫ࡲࡤࡻࠣࡨࡴࡽ࡮࡭ࡱࡤࡨ࠱ࠦࡅࡹࡥࡨࡴࡹ࡯࡯࡯ࠢ࠰ࠤࢀࢃࠢዜ").format(e))
  def bstack11l1l11l1l_opy_(self, path):
    try:
      if not os.path.exists(path):
        os.makedirs(path)
      return True
    except:
      return False
  def bstack11l11l11l1_opy_(self, bstack11l11ll111_opy_, bstack11l1111l11_opy_):
    try:
      bstack11l11111l1_opy_ = self.bstack111llll11l_opy_()
      bstack11l11lll1l_opy_ = os.path.join(bstack11l11111l1_opy_, bstack11l1l1l_opy_ (u"࠭ࡰࡦࡴࡦࡽ࠳ࢀࡩࡱࠩዝ"))
      bstack11l11ll11l_opy_ = os.path.join(bstack11l11111l1_opy_, bstack11l1111l11_opy_)
      if os.path.exists(bstack11l11ll11l_opy_):
        self.logger.info(bstack11l1l1l_opy_ (u"ࠢࡑࡧࡵࡧࡾࠦࡢࡪࡰࡤࡶࡾࠦࡦࡰࡷࡱࡨࠥ࡯࡮ࠡࡽࢀ࠰ࠥࡹ࡫ࡪࡲࡳ࡭ࡳ࡭ࠠࡥࡱࡺࡲࡱࡵࡡࡥࠤዞ").format(bstack11l11ll11l_opy_))
        return bstack11l11ll11l_opy_
      if os.path.exists(bstack11l11lll1l_opy_):
        self.logger.info(bstack11l1l1l_opy_ (u"ࠣࡒࡨࡶࡨࡿࠠࡻ࡫ࡳࠤ࡫ࡵࡵ࡯ࡦࠣ࡭ࡳࠦࡻࡾ࠮ࠣࡹࡳࢀࡩࡱࡲ࡬ࡲ࡬ࠨዟ").format(bstack11l11lll1l_opy_))
        return self.bstack11l1l111ll_opy_(bstack11l11lll1l_opy_, bstack11l1111l11_opy_)
      self.logger.info(bstack11l1l1l_opy_ (u"ࠤࡇࡳࡼࡴ࡬ࡰࡣࡧ࡭ࡳ࡭ࠠࡱࡧࡵࡧࡾࠦࡢࡪࡰࡤࡶࡾࠦࡦࡳࡱࡰࠤࢀࢃࠢዠ").format(bstack11l11ll111_opy_))
      response = bstack1ll11l1111_opy_(bstack11l1l1l_opy_ (u"ࠪࡋࡊ࡚ࠧዡ"), bstack11l11ll111_opy_, {}, {})
      if response.status_code == 200:
        with open(bstack11l11lll1l_opy_, bstack11l1l1l_opy_ (u"ࠫࡼࡨࠧዢ")) as file:
          file.write(response.content)
        self.logger.info(bstack11l1l1l11l_opy_ (u"ࠧࡊ࡯ࡸࡰ࡯ࡳࡦࡪࡥࡥࠢࡳࡩࡷࡩࡹࠡࡤ࡬ࡲࡦࡸࡹࠡࡣࡱࡨࠥࡹࡡࡷࡧࡧࠤࡦࡺࠠࡼࡤ࡬ࡲࡦࡸࡹࡠࡼ࡬ࡴࡤࡶࡡࡵࡪࢀࠦዣ"))
        return self.bstack11l1l111ll_opy_(bstack11l11lll1l_opy_, bstack11l1111l11_opy_)
      else:
        raise(bstack11l1l1l11l_opy_ (u"ࠨࡆࡢ࡫࡯ࡩࡩࠦࡴࡰࠢࡧࡳࡼࡴ࡬ࡰࡣࡧࠤࡹ࡮ࡥࠡࡨ࡬ࡰࡪ࠴ࠠࡔࡶࡤࡸࡺࡹࠠࡤࡱࡧࡩ࠿ࠦࡻࡳࡧࡶࡴࡴࡴࡳࡦ࠰ࡶࡸࡦࡺࡵࡴࡡࡦࡳࡩ࡫ࡽࠣዤ"))
    except:
      self.logger.error(bstack11l1l1l_opy_ (u"ࠢࡖࡰࡤࡦࡱ࡫ࠠࡵࡱࠣࡨࡴࡽ࡮࡭ࡱࡤࡨࠥࡶࡥࡳࡥࡼࠤࡧ࡯࡮ࡢࡴࡼࠦዥ"))
  def bstack111lll1lll_opy_(self, bstack11l11ll111_opy_, bstack11l1111l11_opy_):
    try:
      bstack11l11ll11l_opy_ = self.bstack11l11l11l1_opy_(bstack11l11ll111_opy_, bstack11l1111l11_opy_)
      bstack11l11llll1_opy_ = self.bstack11l1l11l11_opy_(bstack11l11ll111_opy_, bstack11l1111l11_opy_, bstack11l11ll11l_opy_)
      return bstack11l11ll11l_opy_, bstack11l11llll1_opy_
    except Exception as e:
      self.logger.error(bstack11l1l1l_opy_ (u"ࠣࡗࡱࡥࡧࡲࡥࠡࡶࡲࠤ࡬࡫ࡴࠡࡲࡨࡶࡨࡿࠠࡣ࡫ࡱࡥࡷࡿࠠࡱࡣࡷ࡬ࠧዦ").format(e))
    return bstack11l11ll11l_opy_, False
  def bstack11l1l11l11_opy_(self, bstack11l11ll111_opy_, bstack11l1111l11_opy_, bstack11l11ll11l_opy_, bstack111llll1l1_opy_ = 0):
    if bstack111llll1l1_opy_ > 1:
      return False
    if bstack11l11ll11l_opy_ == None or os.path.exists(bstack11l11ll11l_opy_) == False:
      self.logger.warn(bstack11l1l1l_opy_ (u"ࠤࡓࡩࡷࡩࡹࠡࡲࡤࡸ࡭ࠦ࡮ࡰࡶࠣࡪࡴࡻ࡮ࡥ࠮ࠣࡶࡪࡺࡲࡺ࡫ࡱ࡫ࠥࡪ࡯ࡸࡰ࡯ࡳࡦࡪࠢዧ"))
      bstack11l11ll11l_opy_ = self.bstack11l11l11l1_opy_(bstack11l11ll111_opy_, bstack11l1111l11_opy_)
      self.bstack11l1l11l11_opy_(bstack11l11ll111_opy_, bstack11l1111l11_opy_, bstack11l11ll11l_opy_, bstack111llll1l1_opy_+1)
    bstack11l1111ll1_opy_ = bstack11l1l1l_opy_ (u"ࠥࡢ࠳࠰ࡀࡱࡧࡵࡧࡾࡢ࠯ࡤ࡮࡬ࠤࡡࡪ࠮࡝ࡦ࠮࠲ࡡࡪࠫࠣየ")
    command = bstack11l1l1l_opy_ (u"ࠫࢀࢃࠠ࠮࠯ࡹࡩࡷࡹࡩࡰࡰࠪዩ").format(bstack11l11ll11l_opy_)
    bstack11l11l1l1l_opy_ = subprocess.check_output(command, shell=True, text=True)
    if re.match(bstack11l1111ll1_opy_, bstack11l11l1l1l_opy_) != None:
      return True
    else:
      self.logger.error(bstack11l1l1l_opy_ (u"ࠧࡖࡥࡳࡥࡼࠤࡻ࡫ࡲࡴ࡫ࡲࡲࠥࡩࡨࡦࡥ࡮ࠤ࡫ࡧࡩ࡭ࡧࡧࠦዪ"))
      bstack11l11ll11l_opy_ = self.bstack11l11l11l1_opy_(bstack11l11ll111_opy_, bstack11l1111l11_opy_)
      self.bstack11l1l11l11_opy_(bstack11l11ll111_opy_, bstack11l1111l11_opy_, bstack11l11ll11l_opy_, bstack111llll1l1_opy_+1)
  def bstack11l1l111ll_opy_(self, bstack11l11lll1l_opy_, bstack11l1111l11_opy_):
    try:
      working_dir = os.path.dirname(bstack11l11lll1l_opy_)
      shutil.unpack_archive(bstack11l11lll1l_opy_, working_dir)
      bstack11l11ll11l_opy_ = os.path.join(working_dir, bstack11l1111l11_opy_)
      os.chmod(bstack11l11ll11l_opy_, 0o755)
      return bstack11l11ll11l_opy_
    except Exception as e:
      self.logger.error(bstack11l1l1l_opy_ (u"ࠨࡕ࡯ࡣࡥࡰࡪࠦࡴࡰࠢࡸࡲࡿ࡯ࡰࠡࡲࡨࡶࡨࡿࠠࡣ࡫ࡱࡥࡷࡿࠢያ"))
  def bstack11l1l11lll_opy_(self):
    try:
      percy = str(self.config.get(bstack11l1l1l_opy_ (u"ࠧࡱࡧࡵࡧࡾ࠭ዬ"), bstack11l1l1l_opy_ (u"ࠣࡨࡤࡰࡸ࡫ࠢይ"))).lower()
      if percy != bstack11l1l1l_opy_ (u"ࠤࡷࡶࡺ࡫ࠢዮ"):
        return False
      self.bstack11l11l11ll_opy_ = True
      return True
    except Exception as e:
      self.logger.error(bstack11l1l1l_opy_ (u"࡙ࠥࡳࡧࡢ࡭ࡧࠣࡸࡴࠦࡤࡦࡶࡨࡧࡹࠦࡰࡦࡴࡦࡽ࠱ࠦࡅࡹࡥࡨࡴࡹ࡯࡯࡯ࠢࡾࢁࠧዯ").format(e))
  def init(self, bstack1ll111lll1_opy_, config, logger):
    self.bstack1ll111lll1_opy_ = bstack1ll111lll1_opy_
    self.config = config
    self.logger = logger
    if not self.bstack11l1l11lll_opy_():
      return
    self.bstack111lllll11_opy_ = config.get(bstack11l1l1l_opy_ (u"ࠫࡵ࡫ࡲࡤࡻࡒࡴࡹ࡯࡯࡯ࡵࠪደ"), {})
    try:
      bstack11l11ll111_opy_, bstack11l1111l11_opy_ = self.bstack11l11111ll_opy_()
      bstack11l11ll11l_opy_, bstack11l11llll1_opy_ = self.bstack111lll1lll_opy_(bstack11l11ll111_opy_, bstack11l1111l11_opy_)
      if bstack11l11llll1_opy_:
        self.binary_path = bstack11l11ll11l_opy_
        thread = Thread(target=self.bstack11l11lll11_opy_)
        thread.start()
      else:
        self.bstack111llll1ll_opy_ = True
        self.logger.error(bstack11l1l1l_opy_ (u"ࠧࡏ࡮ࡷࡣ࡯࡭ࡩࠦࡰࡦࡴࡦࡽࠥࡶࡡࡵࡪࠣࡪࡴࡻ࡮ࡥࠢ࠰ࠤࢀࢃࠬࠡࡗࡱࡥࡧࡲࡥࠡࡶࡲࠤࡸࡺࡡࡳࡶࠣࡔࡪࡸࡣࡺࠤዱ").format(bstack11l11ll11l_opy_))
    except Exception as e:
      self.logger.error(bstack11l1l1l_opy_ (u"ࠨࡕ࡯ࡣࡥࡰࡪࠦࡴࡰࠢࡶࡸࡦࡸࡴࠡࡲࡨࡶࡨࡿࠬࠡࡇࡻࡧࡪࡶࡴࡪࡱࡱࠤࢀࢃࠢዲ").format(e))
  def bstack11l1111111_opy_(self):
    try:
      logfile = os.path.join(self.working_dir, bstack11l1l1l_opy_ (u"ࠧ࡭ࡱࡪࠫዳ"), bstack11l1l1l_opy_ (u"ࠨࡲࡨࡶࡨࡿ࠮࡭ࡱࡪࠫዴ"))
      os.makedirs(os.path.dirname(logfile)) if not os.path.exists(os.path.dirname(logfile)) else None
      self.logger.debug(bstack11l1l1l_opy_ (u"ࠤࡓࡹࡸ࡮ࡩ࡯ࡩࠣࡴࡪࡸࡣࡺࠢ࡯ࡳ࡬ࡹࠠࡢࡶࠣࡿࢂࠨድ").format(logfile))
      self.bstack11l111l111_opy_ = logfile
    except Exception as e:
      self.logger.error(bstack11l1l1l_opy_ (u"࡙ࠥࡳࡧࡢ࡭ࡧࠣࡸࡴࠦࡳࡦࡶࠣࡴࡪࡸࡣࡺࠢ࡯ࡳ࡬ࠦࡰࡢࡶ࡫࠰ࠥࡋࡸࡤࡧࡳࡸ࡮ࡵ࡮ࠡࡽࢀࠦዶ").format(e))
  def bstack11l11lll11_opy_(self):
    bstack11l11l1111_opy_ = self.bstack11l11l1lll_opy_()
    if bstack11l11l1111_opy_ == None:
      self.bstack111llll1ll_opy_ = True
      self.logger.error(bstack11l1l1l_opy_ (u"ࠦࡕ࡫ࡲࡤࡻࠣࡸࡴࡱࡥ࡯ࠢࡱࡳࡹࠦࡦࡰࡷࡱࡨ࠱ࠦࡆࡢ࡫࡯ࡩࡩࠦࡴࡰࠢࡶࡸࡦࡸࡴࠡࡲࡨࡶࡨࡿࠢዷ"))
      return False
    command_args = [bstack11l1l1l_opy_ (u"ࠧࡧࡰࡱ࠼ࡨࡼࡪࡩ࠺ࡴࡶࡤࡶࡹࠨዸ") if self.bstack1ll111lll1_opy_ else bstack11l1l1l_opy_ (u"࠭ࡥࡹࡧࡦ࠾ࡸࡺࡡࡳࡶࠪዹ")]
    bstack11l11l1l11_opy_ = self.bstack111lllllll_opy_()
    if bstack11l11l1l11_opy_ != None:
      command_args.append(bstack11l1l1l_opy_ (u"ࠢ࠮ࡥࠣࡿࢂࠨዺ").format(bstack11l11l1l11_opy_))
    env = os.environ.copy()
    env[bstack11l1l1l_opy_ (u"ࠣࡒࡈࡖࡈ࡟࡟ࡕࡑࡎࡉࡓࠨዻ")] = bstack11l11l1111_opy_
    bstack111lll1ll1_opy_ = [self.binary_path]
    self.bstack11l1111111_opy_()
    self.bstack111lllll1l_opy_ = self.bstack11l111lll1_opy_(bstack111lll1ll1_opy_ + command_args, env)
    self.logger.debug(bstack11l1l1l_opy_ (u"ࠤࡖࡸࡦࡸࡴࡪࡰࡪࠤࡍ࡫ࡡ࡭ࡶ࡫ࠤࡈ࡮ࡥࡤ࡭ࠥዼ"))
    bstack111llll1l1_opy_ = 0
    while self.bstack111lllll1l_opy_.poll() == None:
      bstack11l111l1ll_opy_ = self.bstack11l1l1l111_opy_()
      if bstack11l111l1ll_opy_:
        self.logger.debug(bstack11l1l1l_opy_ (u"ࠥࡌࡪࡧ࡬ࡵࡪࠣࡇ࡭࡫ࡣ࡬ࠢࡶࡹࡨࡩࡥࡴࡵࡩࡹࡱࠨዽ"))
        self.bstack11l111llll_opy_ = True
        return True
      bstack111llll1l1_opy_ += 1
      self.logger.debug(bstack11l1l1l_opy_ (u"ࠦࡍ࡫ࡡ࡭ࡶ࡫ࠤࡈ࡮ࡥࡤ࡭ࠣࡖࡪࡺࡲࡺࠢ࠰ࠤࢀࢃࠢዾ").format(bstack111llll1l1_opy_))
      time.sleep(2)
    self.logger.error(bstack11l1l1l_opy_ (u"ࠧࡌࡡࡪ࡮ࡨࡨࠥࡺ࡯ࠡࡵࡷࡥࡷࡺࠠࡱࡧࡵࡧࡾ࠲ࠠࡉࡧࡤࡰࡹ࡮ࠠࡄࡪࡨࡧࡰࠦࡆࡢ࡫࡯ࡩࡩࠦࡡࡧࡶࡨࡶࠥࢁࡽࠡࡣࡷࡸࡪࡳࡰࡵࡵࠥዿ").format(bstack111llll1l1_opy_))
    self.bstack111llll1ll_opy_ = True
    return False
  def bstack11l1l1l111_opy_(self, bstack111llll1l1_opy_ = 0):
    try:
      if bstack111llll1l1_opy_ > 10:
        return False
      bstack11l11lllll_opy_ = os.environ.get(bstack11l1l1l_opy_ (u"࠭ࡐࡆࡔࡆ࡝ࡤ࡙ࡅࡓࡘࡈࡖࡤࡇࡄࡅࡔࡈࡗࡘ࠭ጀ"), bstack11l1l1l_opy_ (u"ࠧࡩࡶࡷࡴ࠿࠵࠯࡭ࡱࡦࡥࡱ࡮࡯ࡴࡶ࠽࠹࠸࠹࠸ࠨጁ"))
      bstack11l11l1ll1_opy_ = bstack11l11lllll_opy_ + bstack11llll1l1l_opy_
      response = requests.get(bstack11l11l1ll1_opy_)
      return True if response.json() else False
    except:
      return False
  def bstack11l11l1lll_opy_(self):
    bstack11l1l1111l_opy_ = bstack11l1l1l_opy_ (u"ࠨࡣࡳࡴࠬጂ") if self.bstack1ll111lll1_opy_ else bstack11l1l1l_opy_ (u"ࠩࡤࡹࡹࡵ࡭ࡢࡶࡨࠫጃ")
    bstack11ll1l11l1_opy_ = bstack11l1l1l_opy_ (u"ࠥࡥࡵ࡯࠯ࡢࡲࡳࡣࡵ࡫ࡲࡤࡻ࠲࡫ࡪࡺ࡟ࡱࡴࡲ࡮ࡪࡩࡴࡠࡶࡲ࡯ࡪࡴ࠿࡯ࡣࡰࡩࡂࢁࡽࠧࡶࡼࡴࡪࡃࡻࡾࠤጄ").format(self.config[bstack11l1l1l_opy_ (u"ࠫࡵࡸ࡯࡫ࡧࡦࡸࡓࡧ࡭ࡦࠩጅ")], bstack11l1l1111l_opy_)
    uri = bstack1llllll1l1_opy_(bstack11ll1l11l1_opy_)
    try:
      response = bstack1ll11l1111_opy_(bstack11l1l1l_opy_ (u"ࠬࡍࡅࡕࠩጆ"), uri, {}, {bstack11l1l1l_opy_ (u"࠭ࡡࡶࡶ࡫ࠫጇ"): (self.config[bstack11l1l1l_opy_ (u"ࠧࡶࡵࡨࡶࡓࡧ࡭ࡦࠩገ")], self.config[bstack11l1l1l_opy_ (u"ࠨࡣࡦࡧࡪࡹࡳࡌࡧࡼࠫጉ")])})
      if response.status_code == 200:
        bstack111llll111_opy_ = response.json()
        if bstack11l1l1l_opy_ (u"ࠤࡷࡳࡰ࡫࡮ࠣጊ") in bstack111llll111_opy_:
          return bstack111llll111_opy_[bstack11l1l1l_opy_ (u"ࠥࡸࡴࡱࡥ࡯ࠤጋ")]
        else:
          raise bstack11l1l1l_opy_ (u"࡙ࠫࡵ࡫ࡦࡰࠣࡒࡴࡺࠠࡇࡱࡸࡲࡩࠦ࠭ࠡࡽࢀࠫጌ").format(bstack111llll111_opy_)
      else:
        raise bstack11l1l1l_opy_ (u"ࠧࡌࡡࡪ࡮ࡨࡨࠥࡺ࡯ࠡࡨࡨࡸࡨ࡮ࠠࡱࡧࡵࡧࡾࠦࡴࡰ࡭ࡨࡲ࠱ࠦࡒࡦࡵࡳࡳࡳࡹࡥࠡࡵࡷࡥࡹࡻࡳࠡ࠯ࠣࡿࢂ࠲ࠠࡓࡧࡶࡴࡴࡴࡳࡦࠢࡅࡳࡩࡿࠠ࠮ࠢࡾࢁࠧግ").format(response.status_code, response.json())
    except Exception as e:
      self.logger.error(bstack11l1l1l_opy_ (u"ࠨࡅࡹࡥࡨࡴࡹ࡯࡯࡯ࠢ࡬ࡲࠥࡩࡲࡦࡣࡷ࡭ࡳ࡭ࠠࡱࡧࡵࡧࡾࠦࡰࡳࡱ࡭ࡩࡨࡺࠢጎ").format(e))
  def bstack111lllllll_opy_(self):
    bstack11l111111l_opy_ = os.path.join(tempfile.gettempdir(), bstack11l1l1l_opy_ (u"ࠢࡱࡧࡵࡧࡾࡉ࡯࡯ࡨ࡬࡫࠳ࡰࡳࡰࡰࠥጏ"))
    try:
      if bstack11l1l1l_opy_ (u"ࠨࡸࡨࡶࡸ࡯࡯࡯ࠩጐ") not in self.bstack111lllll11_opy_:
        self.bstack111lllll11_opy_[bstack11l1l1l_opy_ (u"ࠩࡹࡩࡷࡹࡩࡰࡰࠪ጑")] = 2
      with open(bstack11l111111l_opy_, bstack11l1l1l_opy_ (u"ࠪࡻࠬጒ")) as fp:
        json.dump(self.bstack111lllll11_opy_, fp)
      return bstack11l111111l_opy_
    except Exception as e:
      self.logger.error(bstack11l1l1l_opy_ (u"࡚ࠦࡴࡡࡣ࡮ࡨࠤࡹࡵࠠࡤࡴࡨࡥࡹ࡫ࠠࡱࡧࡵࡧࡾࠦࡣࡰࡰࡩ࠰ࠥࡋࡸࡤࡧࡳࡸ࡮ࡵ࡮ࠡࡽࢀࠦጓ").format(e))
  def bstack11l111lll1_opy_(self, cmd, env = os.environ.copy()):
    try:
      if self.bstack11l1111lll_opy_ == bstack11l1l1l_opy_ (u"ࠬࡽࡩ࡯ࠩጔ"):
        bstack11l1111l1l_opy_ = [bstack11l1l1l_opy_ (u"࠭ࡣ࡮ࡦ࠱ࡩࡽ࡫ࠧጕ"), bstack11l1l1l_opy_ (u"ࠧ࠰ࡥࠪ጖")]
        cmd = bstack11l1111l1l_opy_ + cmd
      cmd = bstack11l1l1l_opy_ (u"ࠨࠢࠪ጗").join(cmd)
      self.logger.debug(bstack11l1l1l_opy_ (u"ࠤࡕࡹࡳࡴࡩ࡯ࡩࠣࡿࢂࠨጘ").format(cmd))
      with open(self.bstack11l111l111_opy_, bstack11l1l1l_opy_ (u"ࠥࡥࠧጙ")) as bstack11l111ll1l_opy_:
        process = subprocess.Popen(cmd, shell=True, stdout=bstack11l111ll1l_opy_, text=True, stderr=bstack11l111ll1l_opy_, env=env, universal_newlines=True)
      return process
    except Exception as e:
      self.bstack111llll1ll_opy_ = True
      self.logger.error(bstack11l1l1l_opy_ (u"ࠦࡋࡧࡩ࡭ࡧࡧࠤࡹࡵࠠࡴࡶࡤࡶࡹࠦࡰࡦࡴࡦࡽࠥࡽࡩࡵࡪࠣࡧࡲࡪࠠ࠮ࠢࡾࢁ࠱ࠦࡅࡹࡥࡨࡴࡹ࡯࡯࡯࠼ࠣࡿࢂࠨጚ").format(cmd, e))
  def shutdown(self):
    try:
      if self.bstack11l111llll_opy_:
        self.logger.info(bstack11l1l1l_opy_ (u"࡙ࠧࡴࡰࡲࡳ࡭ࡳ࡭ࠠࡑࡧࡵࡧࡾࠨጛ"))
        cmd = [self.binary_path, bstack11l1l1l_opy_ (u"ࠨࡥࡹࡧࡦ࠾ࡸࡺ࡯ࡱࠤጜ")]
        self.bstack11l111lll1_opy_(cmd)
        self.bstack11l111llll_opy_ = False
    except Exception as e:
      self.logger.error(bstack11l1l1l_opy_ (u"ࠢࡇࡣ࡬ࡰࡪࡪࠠࡵࡱࠣࡷࡹࡵࡰࠡࡵࡨࡷࡸ࡯࡯࡯ࠢࡺ࡭ࡹ࡮ࠠࡤࡱࡰࡱࡦࡴࡤࠡ࠯ࠣࡿࢂ࠲ࠠࡆࡺࡦࡩࡵࡺࡩࡰࡰ࠽ࠤࢀࢃࠢጝ").format(cmd, e))
  def bstack1l11l111_opy_(self):
    if not self.bstack11l11l11ll_opy_:
      return
    try:
      bstack111llllll1_opy_ = 0
      while not self.bstack11l111llll_opy_ and bstack111llllll1_opy_ < self.bstack11l11ll1l1_opy_:
        if self.bstack111llll1ll_opy_:
          self.logger.info(bstack11l1l1l_opy_ (u"ࠣࡒࡨࡶࡨࡿࠠࡴࡧࡷࡹࡵࠦࡦࡢ࡫࡯ࡩࡩࠨጞ"))
          return
        time.sleep(1)
        bstack111llllll1_opy_ += 1
      os.environ[bstack11l1l1l_opy_ (u"ࠩࡓࡉࡗࡉ࡙ࡠࡄࡈࡗ࡙ࡥࡐࡍࡃࡗࡊࡔࡘࡍࠨጟ")] = str(self.bstack11l111l1l1_opy_())
      self.logger.info(bstack11l1l1l_opy_ (u"ࠥࡔࡪࡸࡣࡺࠢࡶࡩࡹࡻࡰࠡࡥࡲࡱࡵࡲࡥࡵࡧࡧࠦጠ"))
    except Exception as e:
      self.logger.error(bstack11l1l1l_opy_ (u"࡚ࠦࡴࡡࡣ࡮ࡨࠤࡹࡵࠠࡴࡧࡷࡹࡵࠦࡰࡦࡴࡦࡽ࠱ࠦࡅࡹࡥࡨࡴࡹ࡯࡯࡯ࠢࡾࢁࠧጡ").format(e))
  def bstack11l111l1l1_opy_(self):
    if self.bstack1ll111lll1_opy_:
      return
    try:
      bstack11l11l111l_opy_ = [platform[bstack11l1l1l_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡔࡡ࡮ࡧࠪጢ")].lower() for platform in self.config.get(bstack11l1l1l_opy_ (u"࠭ࡰ࡭ࡣࡷࡪࡴࡸ࡭ࡴࠩጣ"), [])]
      bstack11l111ll11_opy_ = sys.maxsize
      bstack11l1l11ll1_opy_ = bstack11l1l1l_opy_ (u"ࠧࠨጤ")
      for browser in bstack11l11l111l_opy_:
        if browser in self.bstack11l111l11l_opy_:
          bstack11l11ll1ll_opy_ = self.bstack11l111l11l_opy_[browser]
        if bstack11l11ll1ll_opy_ < bstack11l111ll11_opy_:
          bstack11l111ll11_opy_ = bstack11l11ll1ll_opy_
          bstack11l1l11ll1_opy_ = browser
      return bstack11l1l11ll1_opy_
    except Exception as e:
      self.logger.error(bstack11l1l1l_opy_ (u"ࠣࡗࡱࡥࡧࡲࡥࠡࡶࡲࠤ࡫࡯࡮ࡥࠢࡥࡩࡸࡺࠠࡱ࡮ࡤࡸ࡫ࡵࡲ࡮࠮ࠣࡉࡽࡩࡥࡱࡶ࡬ࡳࡳࠦࡻࡾࠤጥ").format(e))