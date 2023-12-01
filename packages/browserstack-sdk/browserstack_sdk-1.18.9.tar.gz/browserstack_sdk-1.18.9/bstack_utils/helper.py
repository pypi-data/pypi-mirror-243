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
import os
import platform
import re
import subprocess
import traceback
import tempfile
import multiprocessing
import threading
from urllib.parse import urlparse
import git
import requests
from packaging import version
from bstack_utils.config import Config
from bstack_utils.constants import bstack11llll11ll_opy_, bstack1lll1ll11_opy_, bstack11lllll1l_opy_, bstack1ll111l1_opy_
from bstack_utils.messages import bstack111llll11_opy_, bstack1ll1l1111l_opy_
from bstack_utils.proxy import bstack1lll111111_opy_, bstack1l111lll1_opy_
from browserstack_sdk.bstack1llll1ll11_opy_ import *
from browserstack_sdk.bstack1l1l11lll1_opy_ import *
bstack1ll1l11l1_opy_ = Config.get_instance()
def bstack1l11111ll1_opy_(config):
    return config[bstack11l1ll_opy_ (u"ࠪࡹࡸ࡫ࡲࡏࡣࡰࡩࠬႱ")]
def bstack1l111l1111_opy_(config):
    return config[bstack11l1ll_opy_ (u"ࠫࡦࡩࡣࡦࡵࡶࡏࡪࡿࠧႲ")]
def bstack1ll11l1l1_opy_():
    try:
        import playwright
        return True
    except ImportError:
        return False
def bstack11l1llll11_opy_(obj):
    values = []
    bstack11ll1111l1_opy_ = re.compile(bstack11l1ll_opy_ (u"ࡷࠨ࡞ࡄࡗࡖࡘࡔࡓ࡟ࡕࡃࡊࡣࡡࡪࠫࠥࠤႳ"), re.I)
    for key in obj.keys():
        if bstack11ll1111l1_opy_.match(key):
            values.append(obj[key])
    return values
def bstack11ll111ll1_opy_(config):
    tags = []
    tags.extend(bstack11l1llll11_opy_(os.environ))
    tags.extend(bstack11l1llll11_opy_(config))
    return tags
def bstack11ll11llll_opy_(markers):
    tags = []
    for marker in markers:
        tags.append(marker.name)
    return tags
def bstack11ll1ll111_opy_(bstack11ll111111_opy_):
    if not bstack11ll111111_opy_:
        return bstack11l1ll_opy_ (u"࠭ࠧႴ")
    return bstack11l1ll_opy_ (u"ࠢࡼࡿࠣࠬࢀࢃࠩࠣႵ").format(bstack11ll111111_opy_.name, bstack11ll111111_opy_.email)
def bstack1l111l111l_opy_():
    try:
        repo = git.Repo(search_parent_directories=True)
        bstack11l1lll1ll_opy_ = repo.common_dir
        info = {
            bstack11l1ll_opy_ (u"ࠣࡵ࡫ࡥࠧႶ"): repo.head.commit.hexsha,
            bstack11l1ll_opy_ (u"ࠤࡶ࡬ࡴࡸࡴࡠࡵ࡫ࡥࠧႷ"): repo.git.rev_parse(repo.head.commit, short=True),
            bstack11l1ll_opy_ (u"ࠥࡦࡷࡧ࡮ࡤࡪࠥႸ"): repo.active_branch.name,
            bstack11l1ll_opy_ (u"ࠦࡹࡧࡧࠣႹ"): repo.git.describe(all=True, tags=True, exact_match=True),
            bstack11l1ll_opy_ (u"ࠧࡩ࡯࡮࡯࡬ࡸࡹ࡫ࡲࠣႺ"): bstack11ll1ll111_opy_(repo.head.commit.committer),
            bstack11l1ll_opy_ (u"ࠨࡣࡰ࡯ࡰ࡭ࡹࡺࡥࡳࡡࡧࡥࡹ࡫ࠢႻ"): repo.head.commit.committed_datetime.isoformat(),
            bstack11l1ll_opy_ (u"ࠢࡢࡷࡷ࡬ࡴࡸࠢႼ"): bstack11ll1ll111_opy_(repo.head.commit.author),
            bstack11l1ll_opy_ (u"ࠣࡣࡸࡸ࡭ࡵࡲࡠࡦࡤࡸࡪࠨႽ"): repo.head.commit.authored_datetime.isoformat(),
            bstack11l1ll_opy_ (u"ࠤࡦࡳࡲࡳࡩࡵࡡࡰࡩࡸࡹࡡࡨࡧࠥႾ"): repo.head.commit.message,
            bstack11l1ll_opy_ (u"ࠥࡶࡴࡵࡴࠣႿ"): repo.git.rev_parse(bstack11l1ll_opy_ (u"ࠦ࠲࠳ࡳࡩࡱࡺ࠱ࡹࡵࡰ࡭ࡧࡹࡩࡱࠨჀ")),
            bstack11l1ll_opy_ (u"ࠧࡩ࡯࡮࡯ࡲࡲࡤ࡭ࡩࡵࡡࡧ࡭ࡷࠨჁ"): bstack11l1lll1ll_opy_,
            bstack11l1ll_opy_ (u"ࠨࡷࡰࡴ࡮ࡸࡷ࡫ࡥࡠࡩ࡬ࡸࡤࡪࡩࡳࠤჂ"): subprocess.check_output([bstack11l1ll_opy_ (u"ࠢࡨ࡫ࡷࠦჃ"), bstack11l1ll_opy_ (u"ࠣࡴࡨࡺ࠲ࡶࡡࡳࡵࡨࠦჄ"), bstack11l1ll_opy_ (u"ࠤ࠰࠱࡬࡯ࡴ࠮ࡥࡲࡱࡲࡵ࡮࠮ࡦ࡬ࡶࠧჅ")]).strip().decode(
                bstack11l1ll_opy_ (u"ࠪࡹࡹ࡬࠭࠹ࠩ჆")),
            bstack11l1ll_opy_ (u"ࠦࡱࡧࡳࡵࡡࡷࡥ࡬ࠨჇ"): repo.git.describe(tags=True, abbrev=0, always=True),
            bstack11l1ll_opy_ (u"ࠧࡩ࡯࡮࡯࡬ࡸࡸࡥࡳࡪࡰࡦࡩࡤࡲࡡࡴࡶࡢࡸࡦ࡭ࠢ჈"): repo.git.rev_list(
                bstack11l1ll_opy_ (u"ࠨࡻࡾ࠰࠱ࡿࢂࠨ჉").format(repo.head.commit, repo.git.describe(tags=True, abbrev=0, always=True)), count=True)
        }
        remotes = repo.remotes
        bstack11ll111l11_opy_ = []
        for remote in remotes:
            bstack11ll1l111l_opy_ = {
                bstack11l1ll_opy_ (u"ࠢ࡯ࡣࡰࡩࠧ჊"): remote.name,
                bstack11l1ll_opy_ (u"ࠣࡷࡵࡰࠧ჋"): remote.url,
            }
            bstack11ll111l11_opy_.append(bstack11ll1l111l_opy_)
        return {
            bstack11l1ll_opy_ (u"ࠤࡱࡥࡲ࡫ࠢ჌"): bstack11l1ll_opy_ (u"ࠥ࡫࡮ࡺࠢჍ"),
            **info,
            bstack11l1ll_opy_ (u"ࠦࡷ࡫࡭ࡰࡶࡨࡷࠧ჎"): bstack11ll111l11_opy_
        }
    except Exception as err:
        print(bstack11l1ll_opy_ (u"ࠧࡋࡸࡤࡧࡳࡸ࡮ࡵ࡮ࠡ࡫ࡱࠤࡵࡵࡰࡶ࡮ࡤࡸ࡮ࡴࡧࠡࡉ࡬ࡸࠥࡳࡥࡵࡣࡧࡥࡹࡧࠠࡸ࡫ࡷ࡬ࠥ࡫ࡲࡳࡱࡵ࠾ࠥࢁࡽࠣ჏").format(err))
        return {}
def bstack1ll11ll1ll_opy_():
    env = os.environ
    if (bstack11l1ll_opy_ (u"ࠨࡊࡆࡐࡎࡍࡓ࡙࡟ࡖࡔࡏࠦა") in env and len(env[bstack11l1ll_opy_ (u"ࠢࡋࡇࡑࡏࡎࡔࡓࡠࡗࡕࡐࠧბ")]) > 0) or (
            bstack11l1ll_opy_ (u"ࠣࡌࡈࡒࡐࡏࡎࡔࡡࡋࡓࡒࡋࠢგ") in env and len(env[bstack11l1ll_opy_ (u"ࠤࡍࡉࡓࡑࡉࡏࡕࡢࡌࡔࡓࡅࠣდ")]) > 0):
        return {
            bstack11l1ll_opy_ (u"ࠥࡲࡦࡳࡥࠣე"): bstack11l1ll_opy_ (u"ࠦࡏ࡫࡮࡬࡫ࡱࡷࠧვ"),
            bstack11l1ll_opy_ (u"ࠧࡨࡵࡪ࡮ࡧࡣࡺࡸ࡬ࠣზ"): env.get(bstack11l1ll_opy_ (u"ࠨࡂࡖࡋࡏࡈࡤ࡛ࡒࡍࠤთ")),
            bstack11l1ll_opy_ (u"ࠢ࡫ࡱࡥࡣࡳࡧ࡭ࡦࠤი"): env.get(bstack11l1ll_opy_ (u"ࠣࡌࡒࡆࡤࡔࡁࡎࡇࠥკ")),
            bstack11l1ll_opy_ (u"ࠤࡥࡹ࡮ࡲࡤࡠࡰࡸࡱࡧ࡫ࡲࠣლ"): env.get(bstack11l1ll_opy_ (u"ࠥࡆ࡚ࡏࡌࡅࡡࡑ࡙ࡒࡈࡅࡓࠤმ"))
        }
    if env.get(bstack11l1ll_opy_ (u"ࠦࡈࡏࠢნ")) == bstack11l1ll_opy_ (u"ࠧࡺࡲࡶࡧࠥო") and bstack111l1l1l1_opy_(env.get(bstack11l1ll_opy_ (u"ࠨࡃࡊࡔࡆࡐࡊࡉࡉࠣპ"))):
        return {
            bstack11l1ll_opy_ (u"ࠢ࡯ࡣࡰࡩࠧჟ"): bstack11l1ll_opy_ (u"ࠣࡅ࡬ࡶࡨࡲࡥࡄࡋࠥრ"),
            bstack11l1ll_opy_ (u"ࠤࡥࡹ࡮ࡲࡤࡠࡷࡵࡰࠧს"): env.get(bstack11l1ll_opy_ (u"ࠥࡇࡎࡘࡃࡍࡇࡢࡆ࡚ࡏࡌࡅࡡࡘࡖࡑࠨტ")),
            bstack11l1ll_opy_ (u"ࠦ࡯ࡵࡢࡠࡰࡤࡱࡪࠨუ"): env.get(bstack11l1ll_opy_ (u"ࠧࡉࡉࡓࡅࡏࡉࡤࡐࡏࡃࠤფ")),
            bstack11l1ll_opy_ (u"ࠨࡢࡶ࡫࡯ࡨࡤࡴࡵ࡮ࡤࡨࡶࠧქ"): env.get(bstack11l1ll_opy_ (u"ࠢࡄࡋࡕࡇࡑࡋ࡟ࡃࡗࡌࡐࡉࡥࡎࡖࡏࠥღ"))
        }
    if env.get(bstack11l1ll_opy_ (u"ࠣࡅࡌࠦყ")) == bstack11l1ll_opy_ (u"ࠤࡷࡶࡺ࡫ࠢშ") and bstack111l1l1l1_opy_(env.get(bstack11l1ll_opy_ (u"ࠥࡘࡗࡇࡖࡊࡕࠥჩ"))):
        return {
            bstack11l1ll_opy_ (u"ࠦࡳࡧ࡭ࡦࠤც"): bstack11l1ll_opy_ (u"࡚ࠧࡲࡢࡸ࡬ࡷࠥࡉࡉࠣძ"),
            bstack11l1ll_opy_ (u"ࠨࡢࡶ࡫࡯ࡨࡤࡻࡲ࡭ࠤწ"): env.get(bstack11l1ll_opy_ (u"ࠢࡕࡔࡄ࡚ࡎ࡙࡟ࡃࡗࡌࡐࡉࡥࡗࡆࡄࡢ࡙ࡗࡒࠢჭ")),
            bstack11l1ll_opy_ (u"ࠣ࡬ࡲࡦࡤࡴࡡ࡮ࡧࠥხ"): env.get(bstack11l1ll_opy_ (u"ࠤࡗࡖࡆ࡜ࡉࡔࡡࡍࡓࡇࡥࡎࡂࡏࡈࠦჯ")),
            bstack11l1ll_opy_ (u"ࠥࡦࡺ࡯࡬ࡥࡡࡱࡹࡲࡨࡥࡳࠤჰ"): env.get(bstack11l1ll_opy_ (u"࡙ࠦࡘࡁࡗࡋࡖࡣࡇ࡛ࡉࡍࡆࡢࡒ࡚ࡓࡂࡆࡔࠥჱ"))
        }
    if env.get(bstack11l1ll_opy_ (u"ࠧࡉࡉࠣჲ")) == bstack11l1ll_opy_ (u"ࠨࡴࡳࡷࡨࠦჳ") and env.get(bstack11l1ll_opy_ (u"ࠢࡄࡋࡢࡒࡆࡓࡅࠣჴ")) == bstack11l1ll_opy_ (u"ࠣࡥࡲࡨࡪࡹࡨࡪࡲࠥჵ"):
        return {
            bstack11l1ll_opy_ (u"ࠤࡱࡥࡲ࡫ࠢჶ"): bstack11l1ll_opy_ (u"ࠥࡇࡴࡪࡥࡴࡪ࡬ࡴࠧჷ"),
            bstack11l1ll_opy_ (u"ࠦࡧࡻࡩ࡭ࡦࡢࡹࡷࡲࠢჸ"): None,
            bstack11l1ll_opy_ (u"ࠧࡰ࡯ࡣࡡࡱࡥࡲ࡫ࠢჹ"): None,
            bstack11l1ll_opy_ (u"ࠨࡢࡶ࡫࡯ࡨࡤࡴࡵ࡮ࡤࡨࡶࠧჺ"): None
        }
    if env.get(bstack11l1ll_opy_ (u"ࠢࡃࡋࡗࡆ࡚ࡉࡋࡆࡖࡢࡆࡗࡇࡎࡄࡊࠥ჻")) and env.get(bstack11l1ll_opy_ (u"ࠣࡄࡌࡘࡇ࡛ࡃࡌࡇࡗࡣࡈࡕࡍࡎࡋࡗࠦჼ")):
        return {
            bstack11l1ll_opy_ (u"ࠤࡱࡥࡲ࡫ࠢჽ"): bstack11l1ll_opy_ (u"ࠥࡆ࡮ࡺࡢࡶࡥ࡮ࡩࡹࠨჾ"),
            bstack11l1ll_opy_ (u"ࠦࡧࡻࡩ࡭ࡦࡢࡹࡷࡲࠢჿ"): env.get(bstack11l1ll_opy_ (u"ࠧࡈࡉࡕࡄࡘࡇࡐࡋࡔࡠࡉࡌࡘࡤࡎࡔࡕࡒࡢࡓࡗࡏࡇࡊࡐࠥᄀ")),
            bstack11l1ll_opy_ (u"ࠨࡪࡰࡤࡢࡲࡦࡳࡥࠣᄁ"): None,
            bstack11l1ll_opy_ (u"ࠢࡣࡷ࡬ࡰࡩࡥ࡮ࡶ࡯ࡥࡩࡷࠨᄂ"): env.get(bstack11l1ll_opy_ (u"ࠣࡄࡌࡘࡇ࡛ࡃࡌࡇࡗࡣࡇ࡛ࡉࡍࡆࡢࡒ࡚ࡓࡂࡆࡔࠥᄃ"))
        }
    if env.get(bstack11l1ll_opy_ (u"ࠤࡆࡍࠧᄄ")) == bstack11l1ll_opy_ (u"ࠥࡸࡷࡻࡥࠣᄅ") and bstack111l1l1l1_opy_(env.get(bstack11l1ll_opy_ (u"ࠦࡉࡘࡏࡏࡇࠥᄆ"))):
        return {
            bstack11l1ll_opy_ (u"ࠧࡴࡡ࡮ࡧࠥᄇ"): bstack11l1ll_opy_ (u"ࠨࡄࡳࡱࡱࡩࠧᄈ"),
            bstack11l1ll_opy_ (u"ࠢࡣࡷ࡬ࡰࡩࡥࡵࡳ࡮ࠥᄉ"): env.get(bstack11l1ll_opy_ (u"ࠣࡆࡕࡓࡓࡋ࡟ࡃࡗࡌࡐࡉࡥࡌࡊࡐࡎࠦᄊ")),
            bstack11l1ll_opy_ (u"ࠤ࡭ࡳࡧࡥ࡮ࡢ࡯ࡨࠦᄋ"): None,
            bstack11l1ll_opy_ (u"ࠥࡦࡺ࡯࡬ࡥࡡࡱࡹࡲࡨࡥࡳࠤᄌ"): env.get(bstack11l1ll_opy_ (u"ࠦࡉࡘࡏࡏࡇࡢࡆ࡚ࡏࡌࡅࡡࡑ࡙ࡒࡈࡅࡓࠤᄍ"))
        }
    if env.get(bstack11l1ll_opy_ (u"ࠧࡉࡉࠣᄎ")) == bstack11l1ll_opy_ (u"ࠨࡴࡳࡷࡨࠦᄏ") and bstack111l1l1l1_opy_(env.get(bstack11l1ll_opy_ (u"ࠢࡔࡇࡐࡅࡕࡎࡏࡓࡇࠥᄐ"))):
        return {
            bstack11l1ll_opy_ (u"ࠣࡰࡤࡱࡪࠨᄑ"): bstack11l1ll_opy_ (u"ࠤࡖࡩࡲࡧࡰࡩࡱࡵࡩࠧᄒ"),
            bstack11l1ll_opy_ (u"ࠥࡦࡺ࡯࡬ࡥࡡࡸࡶࡱࠨᄓ"): env.get(bstack11l1ll_opy_ (u"ࠦࡘࡋࡍࡂࡒࡋࡓࡗࡋ࡟ࡐࡔࡊࡅࡓࡏ࡚ࡂࡖࡌࡓࡓࡥࡕࡓࡎࠥᄔ")),
            bstack11l1ll_opy_ (u"ࠧࡰ࡯ࡣࡡࡱࡥࡲ࡫ࠢᄕ"): env.get(bstack11l1ll_opy_ (u"ࠨࡓࡆࡏࡄࡔࡍࡕࡒࡆࡡࡍࡓࡇࡥࡎࡂࡏࡈࠦᄖ")),
            bstack11l1ll_opy_ (u"ࠢࡣࡷ࡬ࡰࡩࡥ࡮ࡶ࡯ࡥࡩࡷࠨᄗ"): env.get(bstack11l1ll_opy_ (u"ࠣࡕࡈࡑࡆࡖࡈࡐࡔࡈࡣࡏࡕࡂࡠࡋࡇࠦᄘ"))
        }
    if env.get(bstack11l1ll_opy_ (u"ࠤࡆࡍࠧᄙ")) == bstack11l1ll_opy_ (u"ࠥࡸࡷࡻࡥࠣᄚ") and bstack111l1l1l1_opy_(env.get(bstack11l1ll_opy_ (u"ࠦࡌࡏࡔࡍࡃࡅࡣࡈࡏࠢᄛ"))):
        return {
            bstack11l1ll_opy_ (u"ࠧࡴࡡ࡮ࡧࠥᄜ"): bstack11l1ll_opy_ (u"ࠨࡇࡪࡶࡏࡥࡧࠨᄝ"),
            bstack11l1ll_opy_ (u"ࠢࡣࡷ࡬ࡰࡩࡥࡵࡳ࡮ࠥᄞ"): env.get(bstack11l1ll_opy_ (u"ࠣࡅࡌࡣࡏࡕࡂࡠࡗࡕࡐࠧᄟ")),
            bstack11l1ll_opy_ (u"ࠤ࡭ࡳࡧࡥ࡮ࡢ࡯ࡨࠦᄠ"): env.get(bstack11l1ll_opy_ (u"ࠥࡇࡎࡥࡊࡐࡄࡢࡒࡆࡓࡅࠣᄡ")),
            bstack11l1ll_opy_ (u"ࠦࡧࡻࡩ࡭ࡦࡢࡲࡺࡳࡢࡦࡴࠥᄢ"): env.get(bstack11l1ll_opy_ (u"ࠧࡉࡉࡠࡌࡒࡆࡤࡏࡄࠣᄣ"))
        }
    if env.get(bstack11l1ll_opy_ (u"ࠨࡃࡊࠤᄤ")) == bstack11l1ll_opy_ (u"ࠢࡵࡴࡸࡩࠧᄥ") and bstack111l1l1l1_opy_(env.get(bstack11l1ll_opy_ (u"ࠣࡄࡘࡍࡑࡊࡋࡊࡖࡈࠦᄦ"))):
        return {
            bstack11l1ll_opy_ (u"ࠤࡱࡥࡲ࡫ࠢᄧ"): bstack11l1ll_opy_ (u"ࠥࡆࡺ࡯࡬ࡥ࡭࡬ࡸࡪࠨᄨ"),
            bstack11l1ll_opy_ (u"ࠦࡧࡻࡩ࡭ࡦࡢࡹࡷࡲࠢᄩ"): env.get(bstack11l1ll_opy_ (u"ࠧࡈࡕࡊࡎࡇࡏࡎ࡚ࡅࡠࡄࡘࡍࡑࡊ࡟ࡖࡔࡏࠦᄪ")),
            bstack11l1ll_opy_ (u"ࠨࡪࡰࡤࡢࡲࡦࡳࡥࠣᄫ"): env.get(bstack11l1ll_opy_ (u"ࠢࡃࡗࡌࡐࡉࡑࡉࡕࡇࡢࡐࡆࡈࡅࡍࠤᄬ")) or env.get(bstack11l1ll_opy_ (u"ࠣࡄࡘࡍࡑࡊࡋࡊࡖࡈࡣࡕࡏࡐࡆࡎࡌࡒࡊࡥࡎࡂࡏࡈࠦᄭ")),
            bstack11l1ll_opy_ (u"ࠤࡥࡹ࡮ࡲࡤࡠࡰࡸࡱࡧ࡫ࡲࠣᄮ"): env.get(bstack11l1ll_opy_ (u"ࠥࡆ࡚ࡏࡌࡅࡍࡌࡘࡊࡥࡂࡖࡋࡏࡈࡤࡔࡕࡎࡄࡈࡖࠧᄯ"))
        }
    if bstack111l1l1l1_opy_(env.get(bstack11l1ll_opy_ (u"࡙ࠦࡌ࡟ࡃࡗࡌࡐࡉࠨᄰ"))):
        return {
            bstack11l1ll_opy_ (u"ࠧࡴࡡ࡮ࡧࠥᄱ"): bstack11l1ll_opy_ (u"ࠨࡖࡪࡵࡸࡥࡱࠦࡓࡵࡷࡧ࡭ࡴࠦࡔࡦࡣࡰࠤࡘ࡫ࡲࡷ࡫ࡦࡩࡸࠨᄲ"),
            bstack11l1ll_opy_ (u"ࠢࡣࡷ࡬ࡰࡩࡥࡵࡳ࡮ࠥᄳ"): bstack11l1ll_opy_ (u"ࠣࡽࢀࡿࢂࠨᄴ").format(env.get(bstack11l1ll_opy_ (u"ࠩࡖ࡝ࡘ࡚ࡅࡎࡡࡗࡉࡆࡓࡆࡐࡗࡑࡈࡆ࡚ࡉࡐࡐࡖࡉࡗ࡜ࡅࡓࡗࡕࡍࠬᄵ")), env.get(bstack11l1ll_opy_ (u"ࠪࡗ࡞࡙ࡔࡆࡏࡢࡘࡊࡇࡍࡑࡔࡒࡎࡊࡉࡔࡊࡆࠪᄶ"))),
            bstack11l1ll_opy_ (u"ࠦ࡯ࡵࡢࡠࡰࡤࡱࡪࠨᄷ"): env.get(bstack11l1ll_opy_ (u"࡙࡙ࠧࡔࡖࡈࡑࡤࡊࡅࡇࡋࡑࡍ࡙ࡏࡏࡏࡋࡇࠦᄸ")),
            bstack11l1ll_opy_ (u"ࠨࡢࡶ࡫࡯ࡨࡤࡴࡵ࡮ࡤࡨࡶࠧᄹ"): env.get(bstack11l1ll_opy_ (u"ࠢࡃࡗࡌࡐࡉࡥࡂࡖࡋࡏࡈࡎࡊࠢᄺ"))
        }
    if bstack111l1l1l1_opy_(env.get(bstack11l1ll_opy_ (u"ࠣࡃࡓࡔ࡛ࡋ࡙ࡐࡔࠥᄻ"))):
        return {
            bstack11l1ll_opy_ (u"ࠤࡱࡥࡲ࡫ࠢᄼ"): bstack11l1ll_opy_ (u"ࠥࡅࡵࡶࡶࡦࡻࡲࡶࠧᄽ"),
            bstack11l1ll_opy_ (u"ࠦࡧࡻࡩ࡭ࡦࡢࡹࡷࡲࠢᄾ"): bstack11l1ll_opy_ (u"ࠧࢁࡽ࠰ࡲࡵࡳ࡯࡫ࡣࡵ࠱ࡾࢁ࠴ࢁࡽ࠰ࡤࡸ࡭ࡱࡪࡳ࠰ࡽࢀࠦᄿ").format(env.get(bstack11l1ll_opy_ (u"࠭ࡁࡑࡒ࡙ࡉ࡞ࡕࡒࡠࡗࡕࡐࠬᅀ")), env.get(bstack11l1ll_opy_ (u"ࠧࡂࡒࡓ࡚ࡊ࡟ࡏࡓࡡࡄࡇࡈࡕࡕࡏࡖࡢࡒࡆࡓࡅࠨᅁ")), env.get(bstack11l1ll_opy_ (u"ࠨࡃࡓࡔ࡛ࡋ࡙ࡐࡔࡢࡔࡗࡕࡊࡆࡅࡗࡣࡘࡒࡕࡈࠩᅂ")), env.get(bstack11l1ll_opy_ (u"ࠩࡄࡔࡕ࡜ࡅ࡚ࡑࡕࡣࡇ࡛ࡉࡍࡆࡢࡍࡉ࠭ᅃ"))),
            bstack11l1ll_opy_ (u"ࠥ࡮ࡴࡨ࡟࡯ࡣࡰࡩࠧᅄ"): env.get(bstack11l1ll_opy_ (u"ࠦࡆࡖࡐࡗࡇ࡜ࡓࡗࡥࡊࡐࡄࡢࡒࡆࡓࡅࠣᅅ")),
            bstack11l1ll_opy_ (u"ࠧࡨࡵࡪ࡮ࡧࡣࡳࡻ࡭ࡣࡧࡵࠦᅆ"): env.get(bstack11l1ll_opy_ (u"ࠨࡁࡑࡒ࡙ࡉ࡞ࡕࡒࡠࡄࡘࡍࡑࡊ࡟ࡏࡗࡐࡆࡊࡘࠢᅇ"))
        }
    if env.get(bstack11l1ll_opy_ (u"ࠢࡂ࡜ࡘࡖࡊࡥࡈࡕࡖࡓࡣ࡚࡙ࡅࡓࡡࡄࡋࡊࡔࡔࠣᅈ")) and env.get(bstack11l1ll_opy_ (u"ࠣࡖࡉࡣࡇ࡛ࡉࡍࡆࠥᅉ")):
        return {
            bstack11l1ll_opy_ (u"ࠤࡱࡥࡲ࡫ࠢᅊ"): bstack11l1ll_opy_ (u"ࠥࡅࡿࡻࡲࡦࠢࡆࡍࠧᅋ"),
            bstack11l1ll_opy_ (u"ࠦࡧࡻࡩ࡭ࡦࡢࡹࡷࡲࠢᅌ"): bstack11l1ll_opy_ (u"ࠧࢁࡽࡼࡿ࠲ࡣࡧࡻࡩ࡭ࡦ࠲ࡶࡪࡹࡵ࡭ࡶࡶࡃࡧࡻࡩ࡭ࡦࡌࡨࡂࢁࡽࠣᅍ").format(env.get(bstack11l1ll_opy_ (u"࠭ࡓ࡚ࡕࡗࡉࡒࡥࡔࡆࡃࡐࡊࡔ࡛ࡎࡅࡃࡗࡍࡔࡔࡓࡆࡔ࡙ࡉࡗ࡛ࡒࡊࠩᅎ")), env.get(bstack11l1ll_opy_ (u"ࠧࡔ࡛ࡖࡘࡊࡓ࡟ࡕࡇࡄࡑࡕࡘࡏࡋࡇࡆࡘࠬᅏ")), env.get(bstack11l1ll_opy_ (u"ࠨࡄࡘࡍࡑࡊ࡟ࡃࡗࡌࡐࡉࡏࡄࠨᅐ"))),
            bstack11l1ll_opy_ (u"ࠤ࡭ࡳࡧࡥ࡮ࡢ࡯ࡨࠦᅑ"): env.get(bstack11l1ll_opy_ (u"ࠥࡆ࡚ࡏࡌࡅࡡࡅ࡙ࡎࡒࡄࡊࡆࠥᅒ")),
            bstack11l1ll_opy_ (u"ࠦࡧࡻࡩ࡭ࡦࡢࡲࡺࡳࡢࡦࡴࠥᅓ"): env.get(bstack11l1ll_opy_ (u"ࠧࡈࡕࡊࡎࡇࡣࡇ࡛ࡉࡍࡆࡌࡈࠧᅔ"))
        }
    if any([env.get(bstack11l1ll_opy_ (u"ࠨࡃࡐࡆࡈࡆ࡚ࡏࡌࡅࡡࡅ࡙ࡎࡒࡄࡠࡋࡇࠦᅕ")), env.get(bstack11l1ll_opy_ (u"ࠢࡄࡑࡇࡉࡇ࡛ࡉࡍࡆࡢࡖࡊ࡙ࡏࡍࡘࡈࡈࡤ࡙ࡏࡖࡔࡆࡉࡤ࡜ࡅࡓࡕࡌࡓࡓࠨᅖ")), env.get(bstack11l1ll_opy_ (u"ࠣࡅࡒࡈࡊࡈࡕࡊࡎࡇࡣࡘࡕࡕࡓࡅࡈࡣ࡛ࡋࡒࡔࡋࡒࡒࠧᅗ"))]):
        return {
            bstack11l1ll_opy_ (u"ࠤࡱࡥࡲ࡫ࠢᅘ"): bstack11l1ll_opy_ (u"ࠥࡅ࡜࡙ࠠࡄࡱࡧࡩࡇࡻࡩ࡭ࡦࠥᅙ"),
            bstack11l1ll_opy_ (u"ࠦࡧࡻࡩ࡭ࡦࡢࡹࡷࡲࠢᅚ"): env.get(bstack11l1ll_opy_ (u"ࠧࡉࡏࡅࡇࡅ࡙ࡎࡒࡄࡠࡒࡘࡆࡑࡏࡃࡠࡄࡘࡍࡑࡊ࡟ࡖࡔࡏࠦᅛ")),
            bstack11l1ll_opy_ (u"ࠨࡪࡰࡤࡢࡲࡦࡳࡥࠣᅜ"): env.get(bstack11l1ll_opy_ (u"ࠢࡄࡑࡇࡉࡇ࡛ࡉࡍࡆࡢࡆ࡚ࡏࡌࡅࡡࡌࡈࠧᅝ")),
            bstack11l1ll_opy_ (u"ࠣࡤࡸ࡭ࡱࡪ࡟࡯ࡷࡰࡦࡪࡸࠢᅞ"): env.get(bstack11l1ll_opy_ (u"ࠤࡆࡓࡉࡋࡂࡖࡋࡏࡈࡤࡈࡕࡊࡎࡇࡣࡎࡊࠢᅟ"))
        }
    if env.get(bstack11l1ll_opy_ (u"ࠥࡦࡦࡳࡢࡰࡱࡢࡦࡺ࡯࡬ࡥࡐࡸࡱࡧ࡫ࡲࠣᅠ")):
        return {
            bstack11l1ll_opy_ (u"ࠦࡳࡧ࡭ࡦࠤᅡ"): bstack11l1ll_opy_ (u"ࠧࡈࡡ࡮ࡤࡲࡳࠧᅢ"),
            bstack11l1ll_opy_ (u"ࠨࡢࡶ࡫࡯ࡨࡤࡻࡲ࡭ࠤᅣ"): env.get(bstack11l1ll_opy_ (u"ࠢࡣࡣࡰࡦࡴࡵ࡟ࡣࡷ࡬ࡰࡩࡘࡥࡴࡷ࡯ࡸࡸ࡛ࡲ࡭ࠤᅤ")),
            bstack11l1ll_opy_ (u"ࠣ࡬ࡲࡦࡤࡴࡡ࡮ࡧࠥᅥ"): env.get(bstack11l1ll_opy_ (u"ࠤࡥࡥࡲࡨ࡯ࡰࡡࡶ࡬ࡴࡸࡴࡋࡱࡥࡒࡦࡳࡥࠣᅦ")),
            bstack11l1ll_opy_ (u"ࠥࡦࡺ࡯࡬ࡥࡡࡱࡹࡲࡨࡥࡳࠤᅧ"): env.get(bstack11l1ll_opy_ (u"ࠦࡧࡧ࡭ࡣࡱࡲࡣࡧࡻࡩ࡭ࡦࡑࡹࡲࡨࡥࡳࠤᅨ"))
        }
    if env.get(bstack11l1ll_opy_ (u"ࠧ࡝ࡅࡓࡅࡎࡉࡗࠨᅩ")) or env.get(bstack11l1ll_opy_ (u"ࠨࡗࡆࡔࡆࡏࡊࡘ࡟ࡎࡃࡌࡒࡤࡖࡉࡑࡇࡏࡍࡓࡋ࡟ࡔࡖࡄࡖ࡙ࡋࡄࠣᅪ")):
        return {
            bstack11l1ll_opy_ (u"ࠢ࡯ࡣࡰࡩࠧᅫ"): bstack11l1ll_opy_ (u"࡙ࠣࡨࡶࡨࡱࡥࡳࠤᅬ"),
            bstack11l1ll_opy_ (u"ࠤࡥࡹ࡮ࡲࡤࡠࡷࡵࡰࠧᅭ"): env.get(bstack11l1ll_opy_ (u"࡛ࠥࡊࡘࡃࡌࡇࡕࡣࡇ࡛ࡉࡍࡆࡢ࡙ࡗࡒࠢᅮ")),
            bstack11l1ll_opy_ (u"ࠦ࡯ࡵࡢࡠࡰࡤࡱࡪࠨᅯ"): bstack11l1ll_opy_ (u"ࠧࡓࡡࡪࡰࠣࡔ࡮ࡶࡥ࡭࡫ࡱࡩࠧᅰ") if env.get(bstack11l1ll_opy_ (u"ࠨࡗࡆࡔࡆࡏࡊࡘ࡟ࡎࡃࡌࡒࡤࡖࡉࡑࡇࡏࡍࡓࡋ࡟ࡔࡖࡄࡖ࡙ࡋࡄࠣᅱ")) else None,
            bstack11l1ll_opy_ (u"ࠢࡣࡷ࡬ࡰࡩࡥ࡮ࡶ࡯ࡥࡩࡷࠨᅲ"): env.get(bstack11l1ll_opy_ (u"࡙ࠣࡈࡖࡈࡑࡅࡓࡡࡊࡍ࡙ࡥࡃࡐࡏࡐࡍ࡙ࠨᅳ"))
        }
    if any([env.get(bstack11l1ll_opy_ (u"ࠤࡊࡇࡕࡥࡐࡓࡑࡍࡉࡈ࡚ࠢᅴ")), env.get(bstack11l1ll_opy_ (u"ࠥࡋࡈࡒࡏࡖࡆࡢࡔࡗࡕࡊࡆࡅࡗࠦᅵ")), env.get(bstack11l1ll_opy_ (u"ࠦࡌࡕࡏࡈࡎࡈࡣࡈࡒࡏࡖࡆࡢࡔࡗࡕࡊࡆࡅࡗࠦᅶ"))]):
        return {
            bstack11l1ll_opy_ (u"ࠧࡴࡡ࡮ࡧࠥᅷ"): bstack11l1ll_opy_ (u"ࠨࡇࡰࡱࡪࡰࡪࠦࡃ࡭ࡱࡸࡨࠧᅸ"),
            bstack11l1ll_opy_ (u"ࠢࡣࡷ࡬ࡰࡩࡥࡵࡳ࡮ࠥᅹ"): None,
            bstack11l1ll_opy_ (u"ࠣ࡬ࡲࡦࡤࡴࡡ࡮ࡧࠥᅺ"): env.get(bstack11l1ll_opy_ (u"ࠤࡓࡖࡔࡐࡅࡄࡖࡢࡍࡉࠨᅻ")),
            bstack11l1ll_opy_ (u"ࠥࡦࡺ࡯࡬ࡥࡡࡱࡹࡲࡨࡥࡳࠤᅼ"): env.get(bstack11l1ll_opy_ (u"ࠦࡇ࡛ࡉࡍࡆࡢࡍࡉࠨᅽ"))
        }
    if env.get(bstack11l1ll_opy_ (u"࡙ࠧࡈࡊࡒࡓࡅࡇࡒࡅࠣᅾ")):
        return {
            bstack11l1ll_opy_ (u"ࠨ࡮ࡢ࡯ࡨࠦᅿ"): bstack11l1ll_opy_ (u"ࠢࡔࡪ࡬ࡴࡵࡧࡢ࡭ࡧࠥᆀ"),
            bstack11l1ll_opy_ (u"ࠣࡤࡸ࡭ࡱࡪ࡟ࡶࡴ࡯ࠦᆁ"): env.get(bstack11l1ll_opy_ (u"ࠤࡖࡌࡎࡖࡐࡂࡄࡏࡉࡤࡈࡕࡊࡎࡇࡣ࡚ࡘࡌࠣᆂ")),
            bstack11l1ll_opy_ (u"ࠥ࡮ࡴࡨ࡟࡯ࡣࡰࡩࠧᆃ"): bstack11l1ll_opy_ (u"ࠦࡏࡵࡢࠡࠥࡾࢁࠧᆄ").format(env.get(bstack11l1ll_opy_ (u"࡙ࠬࡈࡊࡒࡓࡅࡇࡒࡅࡠࡌࡒࡆࡤࡏࡄࠨᆅ"))) if env.get(bstack11l1ll_opy_ (u"ࠨࡓࡉࡋࡓࡔࡆࡈࡌࡆࡡࡍࡓࡇࡥࡉࡅࠤᆆ")) else None,
            bstack11l1ll_opy_ (u"ࠢࡣࡷ࡬ࡰࡩࡥ࡮ࡶ࡯ࡥࡩࡷࠨᆇ"): env.get(bstack11l1ll_opy_ (u"ࠣࡕࡋࡍࡕࡖࡁࡃࡎࡈࡣࡇ࡛ࡉࡍࡆࡢࡒ࡚ࡓࡂࡆࡔࠥᆈ"))
        }
    if bstack111l1l1l1_opy_(env.get(bstack11l1ll_opy_ (u"ࠤࡑࡉ࡙ࡒࡉࡇ࡛ࠥᆉ"))):
        return {
            bstack11l1ll_opy_ (u"ࠥࡲࡦࡳࡥࠣᆊ"): bstack11l1ll_opy_ (u"ࠦࡓ࡫ࡴ࡭࡫ࡩࡽࠧᆋ"),
            bstack11l1ll_opy_ (u"ࠧࡨࡵࡪ࡮ࡧࡣࡺࡸ࡬ࠣᆌ"): env.get(bstack11l1ll_opy_ (u"ࠨࡄࡆࡒࡏࡓ࡞ࡥࡕࡓࡎࠥᆍ")),
            bstack11l1ll_opy_ (u"ࠢ࡫ࡱࡥࡣࡳࡧ࡭ࡦࠤᆎ"): env.get(bstack11l1ll_opy_ (u"ࠣࡕࡌࡘࡊࡥࡎࡂࡏࡈࠦᆏ")),
            bstack11l1ll_opy_ (u"ࠤࡥࡹ࡮ࡲࡤࡠࡰࡸࡱࡧ࡫ࡲࠣᆐ"): env.get(bstack11l1ll_opy_ (u"ࠥࡆ࡚ࡏࡌࡅࡡࡌࡈࠧᆑ"))
        }
    if bstack111l1l1l1_opy_(env.get(bstack11l1ll_opy_ (u"ࠦࡌࡏࡔࡉࡗࡅࡣࡆࡉࡔࡊࡑࡑࡗࠧᆒ"))):
        return {
            bstack11l1ll_opy_ (u"ࠧࡴࡡ࡮ࡧࠥᆓ"): bstack11l1ll_opy_ (u"ࠨࡇࡪࡶࡋࡹࡧࠦࡁࡤࡶ࡬ࡳࡳࡹࠢᆔ"),
            bstack11l1ll_opy_ (u"ࠢࡣࡷ࡬ࡰࡩࡥࡵࡳ࡮ࠥᆕ"): bstack11l1ll_opy_ (u"ࠣࡽࢀ࠳ࢀࢃ࠯ࡢࡥࡷ࡭ࡴࡴࡳ࠰ࡴࡸࡲࡸ࠵ࡻࡾࠤᆖ").format(env.get(bstack11l1ll_opy_ (u"ࠩࡊࡍ࡙ࡎࡕࡃࡡࡖࡉࡗ࡜ࡅࡓࡡࡘࡖࡑ࠭ᆗ")), env.get(bstack11l1ll_opy_ (u"ࠪࡋࡎ࡚ࡈࡖࡄࡢࡖࡊࡖࡏࡔࡋࡗࡓࡗ࡟ࠧᆘ")), env.get(bstack11l1ll_opy_ (u"ࠫࡌࡏࡔࡉࡗࡅࡣࡗ࡛ࡎࡠࡋࡇࠫᆙ"))),
            bstack11l1ll_opy_ (u"ࠧࡰ࡯ࡣࡡࡱࡥࡲ࡫ࠢᆚ"): env.get(bstack11l1ll_opy_ (u"ࠨࡇࡊࡖࡋ࡙ࡇࡥࡗࡐࡔࡎࡊࡑࡕࡗࠣᆛ")),
            bstack11l1ll_opy_ (u"ࠢࡣࡷ࡬ࡰࡩࡥ࡮ࡶ࡯ࡥࡩࡷࠨᆜ"): env.get(bstack11l1ll_opy_ (u"ࠣࡉࡌࡘࡍ࡛ࡂࡠࡔࡘࡒࡤࡏࡄࠣᆝ"))
        }
    if env.get(bstack11l1ll_opy_ (u"ࠤࡆࡍࠧᆞ")) == bstack11l1ll_opy_ (u"ࠥࡸࡷࡻࡥࠣᆟ") and env.get(bstack11l1ll_opy_ (u"࡛ࠦࡋࡒࡄࡇࡏࠦᆠ")) == bstack11l1ll_opy_ (u"ࠧ࠷ࠢᆡ"):
        return {
            bstack11l1ll_opy_ (u"ࠨ࡮ࡢ࡯ࡨࠦᆢ"): bstack11l1ll_opy_ (u"ࠢࡗࡧࡵࡧࡪࡲࠢᆣ"),
            bstack11l1ll_opy_ (u"ࠣࡤࡸ࡭ࡱࡪ࡟ࡶࡴ࡯ࠦᆤ"): bstack11l1ll_opy_ (u"ࠤ࡫ࡸࡹࡶ࠺࠰࠱ࡾࢁࠧᆥ").format(env.get(bstack11l1ll_opy_ (u"࡚ࠪࡊࡘࡃࡆࡎࡢ࡙ࡗࡒࠧᆦ"))),
            bstack11l1ll_opy_ (u"ࠦ࡯ࡵࡢࡠࡰࡤࡱࡪࠨᆧ"): None,
            bstack11l1ll_opy_ (u"ࠧࡨࡵࡪ࡮ࡧࡣࡳࡻ࡭ࡣࡧࡵࠦᆨ"): None,
        }
    if env.get(bstack11l1ll_opy_ (u"ࠨࡔࡆࡃࡐࡇࡎ࡚࡙ࡠࡘࡈࡖࡘࡏࡏࡏࠤᆩ")):
        return {
            bstack11l1ll_opy_ (u"ࠢ࡯ࡣࡰࡩࠧᆪ"): bstack11l1ll_opy_ (u"ࠣࡖࡨࡥࡲࡩࡩࡵࡻࠥᆫ"),
            bstack11l1ll_opy_ (u"ࠤࡥࡹ࡮ࡲࡤࡠࡷࡵࡰࠧᆬ"): None,
            bstack11l1ll_opy_ (u"ࠥ࡮ࡴࡨ࡟࡯ࡣࡰࡩࠧᆭ"): env.get(bstack11l1ll_opy_ (u"࡙ࠦࡋࡁࡎࡅࡌࡘ࡞ࡥࡐࡓࡑࡍࡉࡈ࡚࡟ࡏࡃࡐࡉࠧᆮ")),
            bstack11l1ll_opy_ (u"ࠧࡨࡵࡪ࡮ࡧࡣࡳࡻ࡭ࡣࡧࡵࠦᆯ"): env.get(bstack11l1ll_opy_ (u"ࠨࡂࡖࡋࡏࡈࡤࡔࡕࡎࡄࡈࡖࠧᆰ"))
        }
    if any([env.get(bstack11l1ll_opy_ (u"ࠢࡄࡑࡑࡇࡔ࡛ࡒࡔࡇࠥᆱ")), env.get(bstack11l1ll_opy_ (u"ࠣࡅࡒࡒࡈࡕࡕࡓࡕࡈࡣ࡚ࡘࡌࠣᆲ")), env.get(bstack11l1ll_opy_ (u"ࠤࡆࡓࡓࡉࡏࡖࡔࡖࡉࡤ࡛ࡓࡆࡔࡑࡅࡒࡋࠢᆳ")), env.get(bstack11l1ll_opy_ (u"ࠥࡇࡔࡔࡃࡐࡗࡕࡗࡊࡥࡔࡆࡃࡐࠦᆴ"))]):
        return {
            bstack11l1ll_opy_ (u"ࠦࡳࡧ࡭ࡦࠤᆵ"): bstack11l1ll_opy_ (u"ࠧࡉ࡯࡯ࡥࡲࡹࡷࡹࡥࠣᆶ"),
            bstack11l1ll_opy_ (u"ࠨࡢࡶ࡫࡯ࡨࡤࡻࡲ࡭ࠤᆷ"): None,
            bstack11l1ll_opy_ (u"ࠢ࡫ࡱࡥࡣࡳࡧ࡭ࡦࠤᆸ"): env.get(bstack11l1ll_opy_ (u"ࠣࡄࡘࡍࡑࡊ࡟ࡋࡑࡅࡣࡓࡇࡍࡆࠤᆹ")) or None,
            bstack11l1ll_opy_ (u"ࠤࡥࡹ࡮ࡲࡤࡠࡰࡸࡱࡧ࡫ࡲࠣᆺ"): env.get(bstack11l1ll_opy_ (u"ࠥࡆ࡚ࡏࡌࡅࡡࡌࡈࠧᆻ"), 0)
        }
    if env.get(bstack11l1ll_opy_ (u"ࠦࡌࡕ࡟ࡋࡑࡅࡣࡓࡇࡍࡆࠤᆼ")):
        return {
            bstack11l1ll_opy_ (u"ࠧࡴࡡ࡮ࡧࠥᆽ"): bstack11l1ll_opy_ (u"ࠨࡇࡰࡅࡇࠦᆾ"),
            bstack11l1ll_opy_ (u"ࠢࡣࡷ࡬ࡰࡩࡥࡵࡳ࡮ࠥᆿ"): None,
            bstack11l1ll_opy_ (u"ࠣ࡬ࡲࡦࡤࡴࡡ࡮ࡧࠥᇀ"): env.get(bstack11l1ll_opy_ (u"ࠤࡊࡓࡤࡐࡏࡃࡡࡑࡅࡒࡋࠢᇁ")),
            bstack11l1ll_opy_ (u"ࠥࡦࡺ࡯࡬ࡥࡡࡱࡹࡲࡨࡥࡳࠤᇂ"): env.get(bstack11l1ll_opy_ (u"ࠦࡌࡕ࡟ࡑࡋࡓࡉࡑࡏࡎࡆࡡࡆࡓ࡚ࡔࡔࡆࡔࠥᇃ"))
        }
    if env.get(bstack11l1ll_opy_ (u"ࠧࡉࡆࡠࡄࡘࡍࡑࡊ࡟ࡊࡆࠥᇄ")):
        return {
            bstack11l1ll_opy_ (u"ࠨ࡮ࡢ࡯ࡨࠦᇅ"): bstack11l1ll_opy_ (u"ࠢࡄࡱࡧࡩࡋࡸࡥࡴࡪࠥᇆ"),
            bstack11l1ll_opy_ (u"ࠣࡤࡸ࡭ࡱࡪ࡟ࡶࡴ࡯ࠦᇇ"): env.get(bstack11l1ll_opy_ (u"ࠤࡆࡊࡤࡈࡕࡊࡎࡇࡣ࡚ࡘࡌࠣᇈ")),
            bstack11l1ll_opy_ (u"ࠥ࡮ࡴࡨ࡟࡯ࡣࡰࡩࠧᇉ"): env.get(bstack11l1ll_opy_ (u"ࠦࡈࡌ࡟ࡑࡋࡓࡉࡑࡏࡎࡆࡡࡑࡅࡒࡋࠢᇊ")),
            bstack11l1ll_opy_ (u"ࠧࡨࡵࡪ࡮ࡧࡣࡳࡻ࡭ࡣࡧࡵࠦᇋ"): env.get(bstack11l1ll_opy_ (u"ࠨࡃࡇࡡࡅ࡙ࡎࡒࡄࡠࡋࡇࠦᇌ"))
        }
    return {bstack11l1ll_opy_ (u"ࠢࡣࡷ࡬ࡰࡩࡥ࡮ࡶ࡯ࡥࡩࡷࠨᇍ"): None}
def get_host_info():
    return {
        bstack11l1ll_opy_ (u"ࠣࡪࡲࡷࡹࡴࡡ࡮ࡧࠥᇎ"): platform.node(),
        bstack11l1ll_opy_ (u"ࠤࡳࡰࡦࡺࡦࡰࡴࡰࠦᇏ"): platform.system(),
        bstack11l1ll_opy_ (u"ࠥࡸࡾࡶࡥࠣᇐ"): platform.machine(),
        bstack11l1ll_opy_ (u"ࠦࡻ࡫ࡲࡴ࡫ࡲࡲࠧᇑ"): platform.version(),
        bstack11l1ll_opy_ (u"ࠧࡧࡲࡤࡪࠥᇒ"): platform.architecture()[0]
    }
def bstack1l1l11lll_opy_():
    try:
        import selenium
        return True
    except ImportError:
        return False
def bstack11lll11111_opy_():
    if bstack1ll1l11l1_opy_.get_property(bstack11l1ll_opy_ (u"࠭ࡢࡴࡶࡤࡧࡰࡥࡳࡦࡵࡶ࡭ࡴࡴࠧᇓ")):
        return bstack11l1ll_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠭ᇔ")
    return bstack11l1ll_opy_ (u"ࠨࡷࡱ࡯ࡳࡵࡷ࡯ࡡࡪࡶ࡮ࡪࠧᇕ")
def bstack11ll1ll1l1_opy_(driver):
    info = {
        bstack11l1ll_opy_ (u"ࠩࡦࡥࡵࡧࡢࡪ࡮࡬ࡸ࡮࡫ࡳࠨᇖ"): driver.capabilities,
        bstack11l1ll_opy_ (u"ࠪࡷࡪࡹࡳࡪࡱࡱࡣ࡮ࡪࠧᇗ"): driver.session_id,
        bstack11l1ll_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࠬᇘ"): driver.capabilities.get(bstack11l1ll_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡔࡡ࡮ࡧࠪᇙ"), None),
        bstack11l1ll_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸ࡟ࡷࡧࡵࡷ࡮ࡵ࡮ࠨᇚ"): driver.capabilities.get(bstack11l1ll_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡗࡧࡵࡷ࡮ࡵ࡮ࠨᇛ"), None),
        bstack11l1ll_opy_ (u"ࠨࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࠪᇜ"): driver.capabilities.get(bstack11l1ll_opy_ (u"ࠩࡳࡰࡦࡺࡦࡰࡴࡰࡒࡦࡳࡥࠨᇝ"), None),
    }
    if bstack11lll11111_opy_() == bstack11l1ll_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࠩᇞ"):
        info[bstack11l1ll_opy_ (u"ࠫࡵࡸ࡯ࡥࡷࡦࡸࠬᇟ")] = bstack11l1ll_opy_ (u"ࠬࡧࡰࡱ࠯ࡤࡹࡹࡵ࡭ࡢࡶࡨࠫᇠ") if bstack1ll1l11l1l_opy_() else bstack11l1ll_opy_ (u"࠭ࡡࡶࡶࡲࡱࡦࡺࡥࠨᇡ")
    return info
def bstack1ll1l11l1l_opy_():
    if bstack1ll1l11l1_opy_.get_property(bstack11l1ll_opy_ (u"ࠧࡢࡲࡳࡣࡦࡻࡴࡰ࡯ࡤࡸࡪ࠭ᇢ")):
        return True
    if bstack111l1l1l1_opy_(os.environ.get(bstack11l1ll_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡊࡕࡢࡅࡕࡖ࡟ࡂࡗࡗࡓࡒࡇࡔࡆࠩᇣ"), None)):
        return True
    return False
def bstack1111l1lll_opy_(bstack11ll11ll1l_opy_, url, data, config):
    headers = config.get(bstack11l1ll_opy_ (u"ࠩ࡫ࡩࡦࡪࡥࡳࡵࠪᇤ"), None)
    proxies = bstack1lll111111_opy_(config, url)
    auth = config.get(bstack11l1ll_opy_ (u"ࠪࡥࡺࡺࡨࠨᇥ"), None)
    response = requests.request(
            bstack11ll11ll1l_opy_,
            url=url,
            headers=headers,
            auth=auth,
            json=data,
            proxies=proxies
        )
    return response
def bstack1llll11lll_opy_(bstack1l11ll1l1_opy_, size):
    bstack1lll11l1ll_opy_ = []
    while len(bstack1l11ll1l1_opy_) > size:
        bstack1l1l1l111_opy_ = bstack1l11ll1l1_opy_[:size]
        bstack1lll11l1ll_opy_.append(bstack1l1l1l111_opy_)
        bstack1l11ll1l1_opy_ = bstack1l11ll1l1_opy_[size:]
    bstack1lll11l1ll_opy_.append(bstack1l11ll1l1_opy_)
    return bstack1lll11l1ll_opy_
def bstack11lll1111l_opy_(message, bstack11ll111l1l_opy_=False):
    os.write(1, bytes(message, bstack11l1ll_opy_ (u"ࠫࡺࡺࡦ࠮࠺ࠪᇦ")))
    os.write(1, bytes(bstack11l1ll_opy_ (u"ࠬࡢ࡮ࠨᇧ"), bstack11l1ll_opy_ (u"࠭ࡵࡵࡨ࠰࠼ࠬᇨ")))
    if bstack11ll111l1l_opy_:
        with open(bstack11l1ll_opy_ (u"ࠧࡣࡵࡷࡥࡨࡱ࠭ࡰ࠳࠴ࡽ࠲࠭ᇩ") + os.environ[bstack11l1ll_opy_ (u"ࠨࡄࡖࡣ࡙ࡋࡓࡕࡑࡓࡗࡤࡈࡕࡊࡎࡇࡣࡍࡇࡓࡉࡇࡇࡣࡎࡊࠧᇪ")] + bstack11l1ll_opy_ (u"ࠩ࠱ࡰࡴ࡭ࠧᇫ"), bstack11l1ll_opy_ (u"ࠪࡥࠬᇬ")) as f:
            f.write(message + bstack11l1ll_opy_ (u"ࠫࡡࡴࠧᇭ"))
def bstack11l1llllll_opy_():
    return os.environ[bstack11l1ll_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣࡆ࡛ࡔࡐࡏࡄࡘࡎࡕࡎࠨᇮ")].lower() == bstack11l1ll_opy_ (u"࠭ࡴࡳࡷࡨࠫᇯ")
def bstack1ll111l111_opy_(bstack11l1llll1l_opy_):
    return bstack11l1ll_opy_ (u"ࠧࡼࡿ࠲ࡿࢂ࠭ᇰ").format(bstack11llll11ll_opy_, bstack11l1llll1l_opy_)
def bstack1ll11111ll_opy_():
    return datetime.datetime.utcnow().isoformat() + bstack11l1ll_opy_ (u"ࠨ࡜ࠪᇱ")
def bstack11ll11111l_opy_(start, finish):
    return (datetime.datetime.fromisoformat(finish.rstrip(bstack11l1ll_opy_ (u"ࠩ࡝ࠫᇲ"))) - datetime.datetime.fromisoformat(start.rstrip(bstack11l1ll_opy_ (u"ࠪ࡞ࠬᇳ")))).total_seconds() * 1000
def bstack11lll11l11_opy_(timestamp):
    return datetime.datetime.utcfromtimestamp(timestamp).isoformat() + bstack11l1ll_opy_ (u"ࠫ࡟࠭ᇴ")
def bstack11ll11ll11_opy_(bstack11lll111l1_opy_):
    date_format = bstack11l1ll_opy_ (u"࡙ࠬࠫࠦ࡯ࠨࡨࠥࠫࡈ࠻ࠧࡐ࠾࡙ࠪ࠮ࠦࡨࠪᇵ")
    bstack11ll1111ll_opy_ = datetime.datetime.strptime(bstack11lll111l1_opy_, date_format)
    return bstack11ll1111ll_opy_.isoformat() + bstack11l1ll_opy_ (u"࡚࠭ࠨᇶ")
def bstack11lll1l111_opy_(outcome):
    _, exception, _ = outcome.excinfo or (None, None, None)
    if exception:
        return bstack11l1ll_opy_ (u"ࠧࡧࡣ࡬ࡰࡪࡪࠧᇷ")
    else:
        return bstack11l1ll_opy_ (u"ࠨࡲࡤࡷࡸ࡫ࡤࠨᇸ")
def bstack111l1l1l1_opy_(val):
    if val is None:
        return False
    return val.__str__().lower() == bstack11l1ll_opy_ (u"ࠩࡷࡶࡺ࡫ࠧᇹ")
def bstack11ll1ll11l_opy_(val):
    return val.__str__().lower() == bstack11l1ll_opy_ (u"ࠪࡪࡦࡲࡳࡦࠩᇺ")
def bstack1l1l1ll111_opy_(bstack11ll11lll1_opy_=Exception, class_method=False, default_value=None):
    def decorator(func):
        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except bstack11ll11lll1_opy_ as e:
                print(bstack11l1ll_opy_ (u"ࠦࡊࡾࡣࡦࡲࡷ࡭ࡴࡴࠠࡪࡰࠣࡪࡺࡴࡣࡵ࡫ࡲࡲࠥࢁࡽࠡ࠯ࡁࠤࢀࢃ࠺ࠡࡽࢀࠦᇻ").format(func.__name__, bstack11ll11lll1_opy_.__name__, str(e)))
                return default_value
        return wrapper
    def bstack11ll111lll_opy_(bstack11ll1l1l11_opy_):
        def wrapped(cls, *args, **kwargs):
            try:
                return bstack11ll1l1l11_opy_(cls, *args, **kwargs)
            except bstack11ll11lll1_opy_ as e:
                print(bstack11l1ll_opy_ (u"ࠧࡋࡸࡤࡧࡳࡸ࡮ࡵ࡮ࠡ࡫ࡱࠤ࡫ࡻ࡮ࡤࡶ࡬ࡳࡳࠦࡻࡾࠢ࠰ࡂࠥࢁࡽ࠻ࠢࡾࢁࠧᇼ").format(bstack11ll1l1l11_opy_.__name__, bstack11ll11lll1_opy_.__name__, str(e)))
                return default_value
        return wrapped
    if class_method:
        return bstack11ll111lll_opy_
    else:
        return decorator
def bstack1ll111ll1_opy_(bstack1l111ll1ll_opy_):
    if bstack11l1ll_opy_ (u"࠭ࡡࡶࡶࡲࡱࡦࡺࡩࡰࡰࠪᇽ") in bstack1l111ll1ll_opy_ and bstack11ll1ll11l_opy_(bstack1l111ll1ll_opy_[bstack11l1ll_opy_ (u"ࠧࡢࡷࡷࡳࡲࡧࡴࡪࡱࡱࠫᇾ")]):
        return False
    if bstack11l1ll_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱࡁࡶࡶࡲࡱࡦࡺࡩࡰࡰࠪᇿ") in bstack1l111ll1ll_opy_ and bstack11ll1ll11l_opy_(bstack1l111ll1ll_opy_[bstack11l1ll_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࡂࡷࡷࡳࡲࡧࡴࡪࡱࡱࠫሀ")]):
        return False
    return True
def bstack1l11ll11_opy_():
    try:
        from pytest_bdd import reporting
        return True
    except Exception as e:
        return False
def bstack1ll1lll1_opy_(hub_url):
    if bstack1lll1ll1l_opy_() <= version.parse(bstack11l1ll_opy_ (u"ࠪ࠷࠳࠷࠳࠯࠲ࠪሁ")):
        if hub_url != bstack11l1ll_opy_ (u"ࠫࠬሂ"):
            return bstack11l1ll_opy_ (u"ࠧ࡮ࡴࡵࡲ࠽࠳࠴ࠨሃ") + hub_url + bstack11l1ll_opy_ (u"ࠨ࠺࠹࠲࠲ࡻࡩ࠵ࡨࡶࡤࠥሄ")
        return bstack11lllll1l_opy_
    if hub_url != bstack11l1ll_opy_ (u"ࠧࠨህ"):
        return bstack11l1ll_opy_ (u"ࠣࡪࡷࡸࡵࡹ࠺࠰࠱ࠥሆ") + hub_url + bstack11l1ll_opy_ (u"ࠤ࠲ࡻࡩ࠵ࡨࡶࡤࠥሇ")
    return bstack1ll111l1_opy_
def bstack11ll11l1l1_opy_():
    return isinstance(os.getenv(bstack11l1ll_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡓ࡝࡙ࡋࡓࡕࡡࡓࡐ࡚ࡍࡉࡏࠩለ")), str)
def bstack1l1ll11ll_opy_(url):
    return urlparse(url).hostname
def bstack11ll1l1l_opy_(hostname):
    for bstack11l1lll1l_opy_ in bstack1lll1ll11_opy_:
        regex = re.compile(bstack11l1lll1l_opy_)
        if regex.match(hostname):
            return True
    return False
def bstack11ll1l1lll_opy_(bstack11lll11ll1_opy_, file_name, logger):
    bstack1llll1l111_opy_ = os.path.join(os.path.expanduser(bstack11l1ll_opy_ (u"ࠫࢃ࠭ሉ")), bstack11lll11ll1_opy_)
    try:
        if not os.path.exists(bstack1llll1l111_opy_):
            os.makedirs(bstack1llll1l111_opy_)
        file_path = os.path.join(os.path.expanduser(bstack11l1ll_opy_ (u"ࠬࢄࠧሊ")), bstack11lll11ll1_opy_, file_name)
        if not os.path.isfile(file_path):
            with open(file_path, bstack11l1ll_opy_ (u"࠭ࡷࠨላ")):
                pass
            with open(file_path, bstack11l1ll_opy_ (u"ࠢࡸ࠭ࠥሌ")) as outfile:
                json.dump({}, outfile)
        return file_path
    except Exception as e:
        logger.debug(bstack111llll11_opy_.format(str(e)))
def bstack11lll1l11l_opy_(file_name, key, value, logger):
    file_path = bstack11ll1l1lll_opy_(bstack11l1ll_opy_ (u"ࠨ࠰ࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࠨል"), file_name, logger)
    if file_path != None:
        if os.path.exists(file_path):
            bstack1ll1111ll1_opy_ = json.load(open(file_path, bstack11l1ll_opy_ (u"ࠩࡵࡦࠬሎ")))
        else:
            bstack1ll1111ll1_opy_ = {}
        bstack1ll1111ll1_opy_[key] = value
        with open(file_path, bstack11l1ll_opy_ (u"ࠥࡻ࠰ࠨሏ")) as outfile:
            json.dump(bstack1ll1111ll1_opy_, outfile)
def bstack1lll1l1l1l_opy_(file_name, logger):
    file_path = bstack11ll1l1lll_opy_(bstack11l1ll_opy_ (u"ࠫ࠳ࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࠫሐ"), file_name, logger)
    bstack1ll1111ll1_opy_ = {}
    if file_path != None and os.path.exists(file_path):
        with open(file_path, bstack11l1ll_opy_ (u"ࠬࡸࠧሑ")) as bstack11l11l1l_opy_:
            bstack1ll1111ll1_opy_ = json.load(bstack11l11l1l_opy_)
    return bstack1ll1111ll1_opy_
def bstack1l1llll11_opy_(file_path, logger):
    try:
        if os.path.exists(file_path):
            os.remove(file_path)
    except Exception as e:
        logger.debug(bstack11l1ll_opy_ (u"࠭ࡅࡳࡴࡲࡶࠥ࡯࡮ࠡࡦࡨࡰࡪࡺࡩ࡯ࡩࠣࡪ࡮ࡲࡥ࠻ࠢࠪሒ") + file_path + bstack11l1ll_opy_ (u"ࠧࠡࠩሓ") + str(e))
def bstack1lll1ll1l_opy_():
    from selenium import webdriver
    return version.parse(webdriver.__version__)
class Notset:
    def __repr__(self):
        return bstack11l1ll_opy_ (u"ࠣ࠾ࡑࡓ࡙࡙ࡅࡕࡀࠥሔ")
def bstack1ll1l111_opy_(config):
    if bstack11l1ll_opy_ (u"ࠩ࡬ࡷࡕࡲࡡࡺࡹࡵ࡭࡬࡮ࡴࠨሕ") in config:
        del (config[bstack11l1ll_opy_ (u"ࠪ࡭ࡸࡖ࡬ࡢࡻࡺࡶ࡮࡭ࡨࡵࠩሖ")])
        return False
    if bstack1lll1ll1l_opy_() < version.parse(bstack11l1ll_opy_ (u"ࠫ࠸࠴࠴࠯࠲ࠪሗ")):
        return False
    if bstack1lll1ll1l_opy_() >= version.parse(bstack11l1ll_opy_ (u"ࠬ࠺࠮࠲࠰࠸ࠫመ")):
        return True
    if bstack11l1ll_opy_ (u"࠭ࡵࡴࡧ࡚࠷ࡈ࠭ሙ") in config and config[bstack11l1ll_opy_ (u"ࠧࡶࡵࡨ࡛࠸ࡉࠧሚ")] is False:
        return False
    else:
        return True
def bstack1lllll1lll_opy_(args_list, bstack11ll1llll1_opy_):
    index = -1
    for value in bstack11ll1llll1_opy_:
        try:
            index = args_list.index(value)
            return index
        except Exception as e:
            return index
    return index
class Result:
    def __init__(self, result=None, duration=None, exception=None, bstack1l11llll1l_opy_=None):
        self.result = result
        self.duration = duration
        self.exception = exception
        self.exception_type = type(self.exception).__name__ if exception else None
        self.bstack1l11llll1l_opy_ = bstack1l11llll1l_opy_
    @classmethod
    def passed(cls):
        return Result(result=bstack11l1ll_opy_ (u"ࠨࡲࡤࡷࡸ࡫ࡤࠨማ"))
    @classmethod
    def failed(cls, exception=None):
        return Result(result=bstack11l1ll_opy_ (u"ࠩࡩࡥ࡮ࡲࡥࡥࠩሜ"), exception=exception)
    def bstack1l111l1l11_opy_(self):
        if self.result != bstack11l1ll_opy_ (u"ࠪࡪࡦ࡯࡬ࡦࡦࠪም"):
            return None
        if bstack11l1ll_opy_ (u"ࠦࡆࡹࡳࡦࡴࡷ࡭ࡴࡴࠢሞ") in self.exception_type:
            return bstack11l1ll_opy_ (u"ࠧࡇࡳࡴࡧࡵࡸ࡮ࡵ࡮ࡆࡴࡵࡳࡷࠨሟ")
        return bstack11l1ll_opy_ (u"ࠨࡕ࡯ࡪࡤࡲࡩࡲࡥࡥࡇࡵࡶࡴࡸࠢሠ")
    def bstack11lll11lll_opy_(self):
        if self.result != bstack11l1ll_opy_ (u"ࠧࡧࡣ࡬ࡰࡪࡪࠧሡ"):
            return None
        if self.bstack1l11llll1l_opy_:
            return self.bstack1l11llll1l_opy_
        return bstack11lll1l1ll_opy_(self.exception)
def bstack11lll1l1ll_opy_(exc):
    return [traceback.format_exception(exc)]
def bstack11lll1l1l1_opy_(message):
    if isinstance(message, str):
        return not bool(message and message.strip())
    return True
def bstack11111l11_opy_(object, key, default_value):
    if not object or not object.__dict__:
        return default_value
    if key in object.__dict__.keys():
        return object.__dict__.get(key)
    return default_value
def bstack111l1llll_opy_(config, logger):
    try:
        import playwright
        bstack11lll11l1l_opy_ = playwright.__file__
        bstack11ll1l1ll1_opy_ = os.path.split(bstack11lll11l1l_opy_)
        bstack11ll1lll1l_opy_ = bstack11ll1l1ll1_opy_[0] + bstack11l1ll_opy_ (u"ࠨ࠱ࡧࡶ࡮ࡼࡥࡳ࠱ࡳࡥࡨࡱࡡࡨࡧ࠲ࡰ࡮ࡨ࠯ࡤ࡮࡬࠳ࡨࡲࡩ࠯࡬ࡶࠫሢ")
        os.environ[bstack11l1ll_opy_ (u"ࠩࡊࡐࡔࡈࡁࡍࡡࡄࡋࡊࡔࡔࡠࡊࡗࡘࡕࡥࡐࡓࡑ࡛࡝ࠬሣ")] = bstack1l111lll1_opy_(config)
        with open(bstack11ll1lll1l_opy_, bstack11l1ll_opy_ (u"ࠪࡶࠬሤ")) as f:
            bstack1ll1llll1_opy_ = f.read()
            bstack11ll1l11l1_opy_ = bstack11l1ll_opy_ (u"ࠫ࡬ࡲ࡯ࡣࡣ࡯࠱ࡦ࡭ࡥ࡯ࡶࠪሥ")
            bstack11ll11l111_opy_ = bstack1ll1llll1_opy_.find(bstack11ll1l11l1_opy_)
            if bstack11ll11l111_opy_ == -1:
              process = subprocess.Popen(bstack11l1ll_opy_ (u"ࠧࡴࡰ࡮ࠢ࡬ࡲࡸࡺࡡ࡭࡮ࠣ࡫ࡱࡵࡢࡢ࡮࠰ࡥ࡬࡫࡮ࡵࠤሦ"), shell=True, cwd=bstack11ll1l1ll1_opy_[0])
              process.wait()
              bstack11lll111ll_opy_ = bstack11l1ll_opy_ (u"࠭ࠢࡶࡵࡨࠤࡸࡺࡲࡪࡥࡷࠦࡀ࠭ሧ")
              bstack11ll1l1l1l_opy_ = bstack11l1ll_opy_ (u"ࠢࠣࠤࠣࡠࠧࡻࡳࡦࠢࡶࡸࡷ࡯ࡣࡵ࡞ࠥ࠿ࠥࡩ࡯࡯ࡵࡷࠤࢀࠦࡢࡰࡱࡷࡷࡹࡸࡡࡱࠢࢀࠤࡂࠦࡲࡦࡳࡸ࡭ࡷ࡫ࠨࠨࡩ࡯ࡳࡧࡧ࡬࠮ࡣࡪࡩࡳࡺࠧࠪ࠽ࠣ࡭࡫ࠦࠨࡱࡴࡲࡧࡪࡹࡳ࠯ࡧࡱࡺ࠳ࡍࡌࡐࡄࡄࡐࡤࡇࡇࡆࡐࡗࡣࡍ࡚ࡔࡑࡡࡓࡖࡔ࡞࡙ࠪࠢࡥࡳࡴࡺࡳࡵࡴࡤࡴ࠭࠯࠻ࠡࠤࠥࠦረ")
              bstack11ll11l1ll_opy_ = bstack1ll1llll1_opy_.replace(bstack11lll111ll_opy_, bstack11ll1l1l1l_opy_)
              with open(bstack11ll1lll1l_opy_, bstack11l1ll_opy_ (u"ࠨࡹࠪሩ")) as f:
                f.write(bstack11ll11l1ll_opy_)
    except Exception as e:
        logger.error(bstack1ll1l1111l_opy_.format(str(e)))
def bstack1llll1l1l1_opy_():
  try:
    bstack11ll1l1111_opy_ = os.path.join(tempfile.gettempdir(), bstack11l1ll_opy_ (u"ࠩࡲࡴࡹ࡯࡭ࡢ࡮ࡢ࡬ࡺࡨ࡟ࡶࡴ࡯࠲࡯ࡹ࡯࡯ࠩሪ"))
    bstack11lll1ll11_opy_ = []
    if os.path.exists(bstack11ll1l1111_opy_):
      with open(bstack11ll1l1111_opy_) as f:
        bstack11lll1ll11_opy_ = json.load(f)
      os.remove(bstack11ll1l1111_opy_)
    return bstack11lll1ll11_opy_
  except:
    pass
  return []
def bstack1ll11lll11_opy_(bstack11ll11111_opy_):
  try:
    bstack11lll1ll11_opy_ = []
    bstack11ll1l1111_opy_ = os.path.join(tempfile.gettempdir(), bstack11l1ll_opy_ (u"ࠪࡳࡵࡺࡩ࡮ࡣ࡯ࡣ࡭ࡻࡢࡠࡷࡵࡰ࠳ࡰࡳࡰࡰࠪራ"))
    if os.path.exists(bstack11ll1l1111_opy_):
      with open(bstack11ll1l1111_opy_) as f:
        bstack11lll1ll11_opy_ = json.load(f)
    bstack11lll1ll11_opy_.append(bstack11ll11111_opy_)
    with open(bstack11ll1l1111_opy_, bstack11l1ll_opy_ (u"ࠫࡼ࠭ሬ")) as f:
        json.dump(bstack11lll1ll11_opy_, f)
  except:
    pass
def bstack1l1lll1l1_opy_(logger, bstack11ll1ll1ll_opy_ = False):
  try:
    test_name = os.environ.get(bstack11l1ll_opy_ (u"ࠬࡖ࡙ࡕࡇࡖࡘࡤ࡚ࡅࡔࡖࡢࡒࡆࡓࡅࠨር"), bstack11l1ll_opy_ (u"࠭ࠧሮ"))
    if test_name == bstack11l1ll_opy_ (u"ࠧࠨሯ"):
        test_name = threading.current_thread().__dict__.get(bstack11l1ll_opy_ (u"ࠨࡲࡼࡸࡪࡹࡴࡃࡦࡧࡣࡹ࡫ࡳࡵࡡࡱࡥࡲ࡫ࠧሰ"), bstack11l1ll_opy_ (u"ࠩࠪሱ"))
    bstack11ll11l11l_opy_ = bstack11l1ll_opy_ (u"ࠪ࠰ࠥ࠭ሲ").join(threading.current_thread().bstackTestErrorMessages)
    if bstack11ll1ll1ll_opy_:
        bstack11111111_opy_ = os.environ.get(bstack11l1ll_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡔࡑࡇࡔࡇࡑࡕࡑࡤࡏࡎࡅࡇ࡛ࠫሳ"), bstack11l1ll_opy_ (u"ࠬ࠶ࠧሴ"))
        bstack1l1111l1l_opy_ = {bstack11l1ll_opy_ (u"࠭࡮ࡢ࡯ࡨࠫስ"): test_name, bstack11l1ll_opy_ (u"ࠧࡦࡴࡵࡳࡷ࠭ሶ"): bstack11ll11l11l_opy_, bstack11l1ll_opy_ (u"ࠨ࡫ࡱࡨࡪࡾࠧሷ"): bstack11111111_opy_}
        bstack11ll1lll11_opy_ = []
        bstack11l1lllll1_opy_ = os.path.join(tempfile.gettempdir(), bstack11l1ll_opy_ (u"ࠩࡳࡽࡹ࡫ࡳࡵࡡࡳࡴࡵࡥࡥࡳࡴࡲࡶࡤࡲࡩࡴࡶ࠱࡮ࡸࡵ࡮ࠨሸ"))
        if os.path.exists(bstack11l1lllll1_opy_):
            with open(bstack11l1lllll1_opy_) as f:
                bstack11ll1lll11_opy_ = json.load(f)
        bstack11ll1lll11_opy_.append(bstack1l1111l1l_opy_)
        with open(bstack11l1lllll1_opy_, bstack11l1ll_opy_ (u"ࠪࡻࠬሹ")) as f:
            json.dump(bstack11ll1lll11_opy_, f)
    else:
        bstack1l1111l1l_opy_ = {bstack11l1ll_opy_ (u"ࠫࡳࡧ࡭ࡦࠩሺ"): test_name, bstack11l1ll_opy_ (u"ࠬ࡫ࡲࡳࡱࡵࠫሻ"): bstack11ll11l11l_opy_, bstack11l1ll_opy_ (u"࠭ࡩ࡯ࡦࡨࡼࠬሼ"): str(multiprocessing.current_process().name)}
        if bstack11l1ll_opy_ (u"ࠧࡣࡵࡷࡥࡨࡱ࡟ࡦࡴࡵࡳࡷࡥ࡬ࡪࡵࡷࠫሽ") not in multiprocessing.current_process().__dict__.keys():
            multiprocessing.current_process().bstack_error_list = []
        multiprocessing.current_process().bstack_error_list.append(bstack1l1111l1l_opy_)
  except Exception as e:
      logger.warn(bstack11l1ll_opy_ (u"ࠣࡗࡱࡥࡧࡲࡥࠡࡶࡲࠤࡸࡺ࡯ࡳࡧࠣࡴࡾࡺࡥࡴࡶࠣࡪࡺࡴ࡮ࡦ࡮ࠣࡨࡦࡺࡡ࠻ࠢࡾࢁࠧሾ").format(e))
def bstack11l11l1ll_opy_(error_message, test_name, index, logger):
  try:
    bstack11ll1l11ll_opy_ = []
    bstack1l1111l1l_opy_ = {bstack11l1ll_opy_ (u"ࠩࡱࡥࡲ࡫ࠧሿ"): test_name, bstack11l1ll_opy_ (u"ࠪࡩࡷࡸ࡯ࡳࠩቀ"): error_message, bstack11l1ll_opy_ (u"ࠫ࡮ࡴࡤࡦࡺࠪቁ"): index}
    bstack11ll1lllll_opy_ = os.path.join(tempfile.gettempdir(), bstack11l1ll_opy_ (u"ࠬࡸ࡯ࡣࡱࡷࡣࡪࡸࡲࡰࡴࡢࡰ࡮ࡹࡴ࠯࡬ࡶࡳࡳ࠭ቂ"))
    if os.path.exists(bstack11ll1lllll_opy_):
        with open(bstack11ll1lllll_opy_) as f:
            bstack11ll1l11ll_opy_ = json.load(f)
    bstack11ll1l11ll_opy_.append(bstack1l1111l1l_opy_)
    with open(bstack11ll1lllll_opy_, bstack11l1ll_opy_ (u"࠭ࡷࠨቃ")) as f:
        json.dump(bstack11ll1l11ll_opy_, f)
  except Exception as e:
    logger.warn(bstack11l1ll_opy_ (u"ࠢࡖࡰࡤࡦࡱ࡫ࠠࡵࡱࠣࡷࡹࡵࡲࡦࠢࡵࡳࡧࡵࡴࠡࡨࡸࡲࡳ࡫࡬ࠡࡦࡤࡸࡦࡀࠠࡼࡿࠥቄ").format(e))
def bstack1111l1l1_opy_(bstack1ll111l1ll_opy_, name, logger):
  try:
    bstack1l1111l1l_opy_ = {bstack11l1ll_opy_ (u"ࠨࡰࡤࡱࡪ࠭ቅ"): name, bstack11l1ll_opy_ (u"ࠩࡨࡶࡷࡵࡲࠨቆ"): bstack1ll111l1ll_opy_, bstack11l1ll_opy_ (u"ࠪ࡭ࡳࡪࡥࡹࠩቇ"): str(threading.current_thread()._name)}
    return bstack1l1111l1l_opy_
  except Exception as e:
    logger.warn(bstack11l1ll_opy_ (u"࡚ࠦࡴࡡࡣ࡮ࡨࠤࡹࡵࠠࡴࡶࡲࡶࡪࠦࡢࡦࡪࡤࡺࡪࠦࡦࡶࡰࡱࡩࡱࠦࡤࡢࡶࡤ࠾ࠥࢁࡽࠣቈ").format(e))
  return
def bstack1111lll11_opy_(framework):
    if framework.lower() == bstack11l1ll_opy_ (u"ࠬࡶࡹࡵࡧࡶࡸࠬ቉"):
        return bstack1lll11ll11_opy_.version()
    elif framework.lower() == bstack11l1ll_opy_ (u"࠭ࡲࡰࡤࡲࡸࠬቊ"):
        return RobotHandler.version()
    elif framework.lower() == bstack11l1ll_opy_ (u"ࠧࡣࡧ࡫ࡥࡻ࡫ࠧቋ"):
        import behave
        return behave.__version__
    else:
        return bstack11l1ll_opy_ (u"ࠨࡷࡱ࡯ࡳࡵࡷ࡯ࠩቌ")