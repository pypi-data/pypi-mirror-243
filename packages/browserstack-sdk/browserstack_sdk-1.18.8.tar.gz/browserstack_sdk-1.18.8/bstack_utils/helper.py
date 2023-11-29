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
from bstack_utils.constants import bstack11llll1l11_opy_, bstack11111l1l_opy_, bstack1111111ll_opy_, bstack1111lll1l_opy_
from bstack_utils.messages import bstack1l1lll11l1_opy_, bstack1ll11l11ll_opy_
from bstack_utils.proxy import bstack1ll1l1l1l_opy_, bstack1ll1111l_opy_
from browserstack_sdk.bstack1lll11lll_opy_ import *
from browserstack_sdk.bstack1l1l1lll1l_opy_ import *
bstack1lllll111l_opy_ = Config.get_instance()
def bstack1l1111llll_opy_(config):
    return config[bstack11l1l1l_opy_ (u"ࠧࡶࡵࡨࡶࡓࡧ࡭ࡦࠩჃ")]
def bstack1l111111ll_opy_(config):
    return config[bstack11l1l1l_opy_ (u"ࠨࡣࡦࡧࡪࡹࡳࡌࡧࡼࠫჄ")]
def bstack11llllll_opy_():
    try:
        import playwright
        return True
    except ImportError:
        return False
def bstack11lll1ll1l_opy_(obj):
    values = []
    bstack11lll11l1l_opy_ = re.compile(bstack11l1l1l_opy_ (u"ࡴࠥࡢࡈ࡛ࡓࡕࡑࡐࡣ࡙ࡇࡇࡠ࡞ࡧ࠯ࠩࠨჅ"), re.I)
    for key in obj.keys():
        if bstack11lll11l1l_opy_.match(key):
            values.append(obj[key])
    return values
def bstack11ll11l11l_opy_(config):
    tags = []
    tags.extend(bstack11lll1ll1l_opy_(os.environ))
    tags.extend(bstack11lll1ll1l_opy_(config))
    return tags
def bstack11ll1lll1l_opy_(markers):
    tags = []
    for marker in markers:
        tags.append(marker.name)
    return tags
def bstack11ll111lll_opy_(bstack11lll1111l_opy_):
    if not bstack11lll1111l_opy_:
        return bstack11l1l1l_opy_ (u"ࠪࠫ჆")
    return bstack11l1l1l_opy_ (u"ࠦࢀࢃࠠࠩࡽࢀ࠭ࠧჇ").format(bstack11lll1111l_opy_.name, bstack11lll1111l_opy_.email)
def bstack1l11111l11_opy_():
    try:
        repo = git.Repo(search_parent_directories=True)
        bstack11lll1ll11_opy_ = repo.common_dir
        info = {
            bstack11l1l1l_opy_ (u"ࠧࡹࡨࡢࠤ჈"): repo.head.commit.hexsha,
            bstack11l1l1l_opy_ (u"ࠨࡳࡩࡱࡵࡸࡤࡹࡨࡢࠤ჉"): repo.git.rev_parse(repo.head.commit, short=True),
            bstack11l1l1l_opy_ (u"ࠢࡣࡴࡤࡲࡨ࡮ࠢ჊"): repo.active_branch.name,
            bstack11l1l1l_opy_ (u"ࠣࡶࡤ࡫ࠧ჋"): repo.git.describe(all=True, tags=True, exact_match=True),
            bstack11l1l1l_opy_ (u"ࠤࡦࡳࡲࡳࡩࡵࡶࡨࡶࠧ჌"): bstack11ll111lll_opy_(repo.head.commit.committer),
            bstack11l1l1l_opy_ (u"ࠥࡧࡴࡳ࡭ࡪࡶࡷࡩࡷࡥࡤࡢࡶࡨࠦჍ"): repo.head.commit.committed_datetime.isoformat(),
            bstack11l1l1l_opy_ (u"ࠦࡦࡻࡴࡩࡱࡵࠦ჎"): bstack11ll111lll_opy_(repo.head.commit.author),
            bstack11l1l1l_opy_ (u"ࠧࡧࡵࡵࡪࡲࡶࡤࡪࡡࡵࡧࠥ჏"): repo.head.commit.authored_datetime.isoformat(),
            bstack11l1l1l_opy_ (u"ࠨࡣࡰ࡯ࡰ࡭ࡹࡥ࡭ࡦࡵࡶࡥ࡬࡫ࠢა"): repo.head.commit.message,
            bstack11l1l1l_opy_ (u"ࠢࡳࡱࡲࡸࠧბ"): repo.git.rev_parse(bstack11l1l1l_opy_ (u"ࠣ࠯࠰ࡷ࡭ࡵࡷ࠮ࡶࡲࡴࡱ࡫ࡶࡦ࡮ࠥგ")),
            bstack11l1l1l_opy_ (u"ࠤࡦࡳࡲࡳ࡯࡯ࡡࡪ࡭ࡹࡥࡤࡪࡴࠥდ"): bstack11lll1ll11_opy_,
            bstack11l1l1l_opy_ (u"ࠥࡻࡴࡸ࡫ࡵࡴࡨࡩࡤ࡭ࡩࡵࡡࡧ࡭ࡷࠨე"): subprocess.check_output([bstack11l1l1l_opy_ (u"ࠦ࡬࡯ࡴࠣვ"), bstack11l1l1l_opy_ (u"ࠧࡸࡥࡷ࠯ࡳࡥࡷࡹࡥࠣზ"), bstack11l1l1l_opy_ (u"ࠨ࠭࠮ࡩ࡬ࡸ࠲ࡩ࡯࡮࡯ࡲࡲ࠲ࡪࡩࡳࠤთ")]).strip().decode(
                bstack11l1l1l_opy_ (u"ࠧࡶࡶࡩ࠱࠽࠭ი")),
            bstack11l1l1l_opy_ (u"ࠣ࡮ࡤࡷࡹࡥࡴࡢࡩࠥკ"): repo.git.describe(tags=True, abbrev=0, always=True),
            bstack11l1l1l_opy_ (u"ࠤࡦࡳࡲࡳࡩࡵࡵࡢࡷ࡮ࡴࡣࡦࡡ࡯ࡥࡸࡺ࡟ࡵࡣࡪࠦლ"): repo.git.rev_list(
                bstack11l1l1l_opy_ (u"ࠥࡿࢂ࠴࠮ࡼࡿࠥმ").format(repo.head.commit, repo.git.describe(tags=True, abbrev=0, always=True)), count=True)
        }
        remotes = repo.remotes
        bstack11ll11ll11_opy_ = []
        for remote in remotes:
            bstack11ll1l1ll1_opy_ = {
                bstack11l1l1l_opy_ (u"ࠦࡳࡧ࡭ࡦࠤნ"): remote.name,
                bstack11l1l1l_opy_ (u"ࠧࡻࡲ࡭ࠤო"): remote.url,
            }
            bstack11ll11ll11_opy_.append(bstack11ll1l1ll1_opy_)
        return {
            bstack11l1l1l_opy_ (u"ࠨ࡮ࡢ࡯ࡨࠦპ"): bstack11l1l1l_opy_ (u"ࠢࡨ࡫ࡷࠦჟ"),
            **info,
            bstack11l1l1l_opy_ (u"ࠣࡴࡨࡱࡴࡺࡥࡴࠤრ"): bstack11ll11ll11_opy_
        }
    except Exception as err:
        print(bstack11l1l1l_opy_ (u"ࠤࡈࡼࡨ࡫ࡰࡵ࡫ࡲࡲࠥ࡯࡮ࠡࡲࡲࡴࡺࡲࡡࡵ࡫ࡱ࡫ࠥࡍࡩࡵࠢࡰࡩࡹࡧࡤࡢࡶࡤࠤࡼ࡯ࡴࡩࠢࡨࡶࡷࡵࡲ࠻ࠢࡾࢁࠧს").format(err))
        return {}
def bstack1lll1l1ll_opy_():
    env = os.environ
    if (bstack11l1l1l_opy_ (u"ࠥࡎࡊࡔࡋࡊࡐࡖࡣ࡚ࡘࡌࠣტ") in env and len(env[bstack11l1l1l_opy_ (u"ࠦࡏࡋࡎࡌࡋࡑࡗࡤ࡛ࡒࡍࠤუ")]) > 0) or (
            bstack11l1l1l_opy_ (u"ࠧࡐࡅࡏࡍࡌࡒࡘࡥࡈࡐࡏࡈࠦფ") in env and len(env[bstack11l1l1l_opy_ (u"ࠨࡊࡆࡐࡎࡍࡓ࡙࡟ࡉࡑࡐࡉࠧქ")]) > 0):
        return {
            bstack11l1l1l_opy_ (u"ࠢ࡯ࡣࡰࡩࠧღ"): bstack11l1l1l_opy_ (u"ࠣࡌࡨࡲࡰ࡯࡮ࡴࠤყ"),
            bstack11l1l1l_opy_ (u"ࠤࡥࡹ࡮ࡲࡤࡠࡷࡵࡰࠧშ"): env.get(bstack11l1l1l_opy_ (u"ࠥࡆ࡚ࡏࡌࡅࡡࡘࡖࡑࠨჩ")),
            bstack11l1l1l_opy_ (u"ࠦ࡯ࡵࡢࡠࡰࡤࡱࡪࠨც"): env.get(bstack11l1l1l_opy_ (u"ࠧࡐࡏࡃࡡࡑࡅࡒࡋࠢძ")),
            bstack11l1l1l_opy_ (u"ࠨࡢࡶ࡫࡯ࡨࡤࡴࡵ࡮ࡤࡨࡶࠧწ"): env.get(bstack11l1l1l_opy_ (u"ࠢࡃࡗࡌࡐࡉࡥࡎࡖࡏࡅࡉࡗࠨჭ"))
        }
    if env.get(bstack11l1l1l_opy_ (u"ࠣࡅࡌࠦხ")) == bstack11l1l1l_opy_ (u"ࠤࡷࡶࡺ࡫ࠢჯ") and bstack1111llll_opy_(env.get(bstack11l1l1l_opy_ (u"ࠥࡇࡎࡘࡃࡍࡇࡆࡍࠧჰ"))):
        return {
            bstack11l1l1l_opy_ (u"ࠦࡳࡧ࡭ࡦࠤჱ"): bstack11l1l1l_opy_ (u"ࠧࡉࡩࡳࡥ࡯ࡩࡈࡏࠢჲ"),
            bstack11l1l1l_opy_ (u"ࠨࡢࡶ࡫࡯ࡨࡤࡻࡲ࡭ࠤჳ"): env.get(bstack11l1l1l_opy_ (u"ࠢࡄࡋࡕࡇࡑࡋ࡟ࡃࡗࡌࡐࡉࡥࡕࡓࡎࠥჴ")),
            bstack11l1l1l_opy_ (u"ࠣ࡬ࡲࡦࡤࡴࡡ࡮ࡧࠥჵ"): env.get(bstack11l1l1l_opy_ (u"ࠤࡆࡍࡗࡉࡌࡆࡡࡍࡓࡇࠨჶ")),
            bstack11l1l1l_opy_ (u"ࠥࡦࡺ࡯࡬ࡥࡡࡱࡹࡲࡨࡥࡳࠤჷ"): env.get(bstack11l1l1l_opy_ (u"ࠦࡈࡏࡒࡄࡎࡈࡣࡇ࡛ࡉࡍࡆࡢࡒ࡚ࡓࠢჸ"))
        }
    if env.get(bstack11l1l1l_opy_ (u"ࠧࡉࡉࠣჹ")) == bstack11l1l1l_opy_ (u"ࠨࡴࡳࡷࡨࠦჺ") and bstack1111llll_opy_(env.get(bstack11l1l1l_opy_ (u"ࠢࡕࡔࡄ࡚ࡎ࡙ࠢ჻"))):
        return {
            bstack11l1l1l_opy_ (u"ࠣࡰࡤࡱࡪࠨჼ"): bstack11l1l1l_opy_ (u"ࠤࡗࡶࡦࡼࡩࡴࠢࡆࡍࠧჽ"),
            bstack11l1l1l_opy_ (u"ࠥࡦࡺ࡯࡬ࡥࡡࡸࡶࡱࠨჾ"): env.get(bstack11l1l1l_opy_ (u"࡙ࠦࡘࡁࡗࡋࡖࡣࡇ࡛ࡉࡍࡆࡢ࡛ࡊࡈ࡟ࡖࡔࡏࠦჿ")),
            bstack11l1l1l_opy_ (u"ࠧࡰ࡯ࡣࡡࡱࡥࡲ࡫ࠢᄀ"): env.get(bstack11l1l1l_opy_ (u"ࠨࡔࡓࡃ࡙ࡍࡘࡥࡊࡐࡄࡢࡒࡆࡓࡅࠣᄁ")),
            bstack11l1l1l_opy_ (u"ࠢࡣࡷ࡬ࡰࡩࡥ࡮ࡶ࡯ࡥࡩࡷࠨᄂ"): env.get(bstack11l1l1l_opy_ (u"ࠣࡖࡕࡅ࡛ࡏࡓࡠࡄࡘࡍࡑࡊ࡟ࡏࡗࡐࡆࡊࡘࠢᄃ"))
        }
    if env.get(bstack11l1l1l_opy_ (u"ࠤࡆࡍࠧᄄ")) == bstack11l1l1l_opy_ (u"ࠥࡸࡷࡻࡥࠣᄅ") and env.get(bstack11l1l1l_opy_ (u"ࠦࡈࡏ࡟ࡏࡃࡐࡉࠧᄆ")) == bstack11l1l1l_opy_ (u"ࠧࡩ࡯ࡥࡧࡶ࡬࡮ࡶࠢᄇ"):
        return {
            bstack11l1l1l_opy_ (u"ࠨ࡮ࡢ࡯ࡨࠦᄈ"): bstack11l1l1l_opy_ (u"ࠢࡄࡱࡧࡩࡸ࡮ࡩࡱࠤᄉ"),
            bstack11l1l1l_opy_ (u"ࠣࡤࡸ࡭ࡱࡪ࡟ࡶࡴ࡯ࠦᄊ"): None,
            bstack11l1l1l_opy_ (u"ࠤ࡭ࡳࡧࡥ࡮ࡢ࡯ࡨࠦᄋ"): None,
            bstack11l1l1l_opy_ (u"ࠥࡦࡺ࡯࡬ࡥࡡࡱࡹࡲࡨࡥࡳࠤᄌ"): None
        }
    if env.get(bstack11l1l1l_opy_ (u"ࠦࡇࡏࡔࡃࡗࡆࡏࡊ࡚࡟ࡃࡔࡄࡒࡈࡎࠢᄍ")) and env.get(bstack11l1l1l_opy_ (u"ࠧࡈࡉࡕࡄࡘࡇࡐࡋࡔࡠࡅࡒࡑࡒࡏࡔࠣᄎ")):
        return {
            bstack11l1l1l_opy_ (u"ࠨ࡮ࡢ࡯ࡨࠦᄏ"): bstack11l1l1l_opy_ (u"ࠢࡃ࡫ࡷࡦࡺࡩ࡫ࡦࡶࠥᄐ"),
            bstack11l1l1l_opy_ (u"ࠣࡤࡸ࡭ࡱࡪ࡟ࡶࡴ࡯ࠦᄑ"): env.get(bstack11l1l1l_opy_ (u"ࠤࡅࡍ࡙ࡈࡕࡄࡍࡈࡘࡤࡍࡉࡕࡡࡋࡘ࡙ࡖ࡟ࡐࡔࡌࡋࡎࡔࠢᄒ")),
            bstack11l1l1l_opy_ (u"ࠥ࡮ࡴࡨ࡟࡯ࡣࡰࡩࠧᄓ"): None,
            bstack11l1l1l_opy_ (u"ࠦࡧࡻࡩ࡭ࡦࡢࡲࡺࡳࡢࡦࡴࠥᄔ"): env.get(bstack11l1l1l_opy_ (u"ࠧࡈࡉࡕࡄࡘࡇࡐࡋࡔࡠࡄࡘࡍࡑࡊ࡟ࡏࡗࡐࡆࡊࡘࠢᄕ"))
        }
    if env.get(bstack11l1l1l_opy_ (u"ࠨࡃࡊࠤᄖ")) == bstack11l1l1l_opy_ (u"ࠢࡵࡴࡸࡩࠧᄗ") and bstack1111llll_opy_(env.get(bstack11l1l1l_opy_ (u"ࠣࡆࡕࡓࡓࡋࠢᄘ"))):
        return {
            bstack11l1l1l_opy_ (u"ࠤࡱࡥࡲ࡫ࠢᄙ"): bstack11l1l1l_opy_ (u"ࠥࡈࡷࡵ࡮ࡦࠤᄚ"),
            bstack11l1l1l_opy_ (u"ࠦࡧࡻࡩ࡭ࡦࡢࡹࡷࡲࠢᄛ"): env.get(bstack11l1l1l_opy_ (u"ࠧࡊࡒࡐࡐࡈࡣࡇ࡛ࡉࡍࡆࡢࡐࡎࡔࡋࠣᄜ")),
            bstack11l1l1l_opy_ (u"ࠨࡪࡰࡤࡢࡲࡦࡳࡥࠣᄝ"): None,
            bstack11l1l1l_opy_ (u"ࠢࡣࡷ࡬ࡰࡩࡥ࡮ࡶ࡯ࡥࡩࡷࠨᄞ"): env.get(bstack11l1l1l_opy_ (u"ࠣࡆࡕࡓࡓࡋ࡟ࡃࡗࡌࡐࡉࡥࡎࡖࡏࡅࡉࡗࠨᄟ"))
        }
    if env.get(bstack11l1l1l_opy_ (u"ࠤࡆࡍࠧᄠ")) == bstack11l1l1l_opy_ (u"ࠥࡸࡷࡻࡥࠣᄡ") and bstack1111llll_opy_(env.get(bstack11l1l1l_opy_ (u"ࠦࡘࡋࡍࡂࡒࡋࡓࡗࡋࠢᄢ"))):
        return {
            bstack11l1l1l_opy_ (u"ࠧࡴࡡ࡮ࡧࠥᄣ"): bstack11l1l1l_opy_ (u"ࠨࡓࡦ࡯ࡤࡴ࡭ࡵࡲࡦࠤᄤ"),
            bstack11l1l1l_opy_ (u"ࠢࡣࡷ࡬ࡰࡩࡥࡵࡳ࡮ࠥᄥ"): env.get(bstack11l1l1l_opy_ (u"ࠣࡕࡈࡑࡆࡖࡈࡐࡔࡈࡣࡔࡘࡇࡂࡐࡌ࡞ࡆ࡚ࡉࡐࡐࡢ࡙ࡗࡒࠢᄦ")),
            bstack11l1l1l_opy_ (u"ࠤ࡭ࡳࡧࡥ࡮ࡢ࡯ࡨࠦᄧ"): env.get(bstack11l1l1l_opy_ (u"ࠥࡗࡊࡓࡁࡑࡊࡒࡖࡊࡥࡊࡐࡄࡢࡒࡆࡓࡅࠣᄨ")),
            bstack11l1l1l_opy_ (u"ࠦࡧࡻࡩ࡭ࡦࡢࡲࡺࡳࡢࡦࡴࠥᄩ"): env.get(bstack11l1l1l_opy_ (u"࡙ࠧࡅࡎࡃࡓࡌࡔࡘࡅࡠࡌࡒࡆࡤࡏࡄࠣᄪ"))
        }
    if env.get(bstack11l1l1l_opy_ (u"ࠨࡃࡊࠤᄫ")) == bstack11l1l1l_opy_ (u"ࠢࡵࡴࡸࡩࠧᄬ") and bstack1111llll_opy_(env.get(bstack11l1l1l_opy_ (u"ࠣࡉࡌࡘࡑࡇࡂࡠࡅࡌࠦᄭ"))):
        return {
            bstack11l1l1l_opy_ (u"ࠤࡱࡥࡲ࡫ࠢᄮ"): bstack11l1l1l_opy_ (u"ࠥࡋ࡮ࡺࡌࡢࡤࠥᄯ"),
            bstack11l1l1l_opy_ (u"ࠦࡧࡻࡩ࡭ࡦࡢࡹࡷࡲࠢᄰ"): env.get(bstack11l1l1l_opy_ (u"ࠧࡉࡉࡠࡌࡒࡆࡤ࡛ࡒࡍࠤᄱ")),
            bstack11l1l1l_opy_ (u"ࠨࡪࡰࡤࡢࡲࡦࡳࡥࠣᄲ"): env.get(bstack11l1l1l_opy_ (u"ࠢࡄࡋࡢࡎࡔࡈ࡟ࡏࡃࡐࡉࠧᄳ")),
            bstack11l1l1l_opy_ (u"ࠣࡤࡸ࡭ࡱࡪ࡟࡯ࡷࡰࡦࡪࡸࠢᄴ"): env.get(bstack11l1l1l_opy_ (u"ࠤࡆࡍࡤࡐࡏࡃࡡࡌࡈࠧᄵ"))
        }
    if env.get(bstack11l1l1l_opy_ (u"ࠥࡇࡎࠨᄶ")) == bstack11l1l1l_opy_ (u"ࠦࡹࡸࡵࡦࠤᄷ") and bstack1111llll_opy_(env.get(bstack11l1l1l_opy_ (u"ࠧࡈࡕࡊࡎࡇࡏࡎ࡚ࡅࠣᄸ"))):
        return {
            bstack11l1l1l_opy_ (u"ࠨ࡮ࡢ࡯ࡨࠦᄹ"): bstack11l1l1l_opy_ (u"ࠢࡃࡷ࡬ࡰࡩࡱࡩࡵࡧࠥᄺ"),
            bstack11l1l1l_opy_ (u"ࠣࡤࡸ࡭ࡱࡪ࡟ࡶࡴ࡯ࠦᄻ"): env.get(bstack11l1l1l_opy_ (u"ࠤࡅ࡙ࡎࡒࡄࡌࡋࡗࡉࡤࡈࡕࡊࡎࡇࡣ࡚ࡘࡌࠣᄼ")),
            bstack11l1l1l_opy_ (u"ࠥ࡮ࡴࡨ࡟࡯ࡣࡰࡩࠧᄽ"): env.get(bstack11l1l1l_opy_ (u"ࠦࡇ࡛ࡉࡍࡆࡎࡍ࡙ࡋ࡟ࡍࡃࡅࡉࡑࠨᄾ")) or env.get(bstack11l1l1l_opy_ (u"ࠧࡈࡕࡊࡎࡇࡏࡎ࡚ࡅࡠࡒࡌࡔࡊࡒࡉࡏࡇࡢࡒࡆࡓࡅࠣᄿ")),
            bstack11l1l1l_opy_ (u"ࠨࡢࡶ࡫࡯ࡨࡤࡴࡵ࡮ࡤࡨࡶࠧᅀ"): env.get(bstack11l1l1l_opy_ (u"ࠢࡃࡗࡌࡐࡉࡑࡉࡕࡇࡢࡆ࡚ࡏࡌࡅࡡࡑ࡙ࡒࡈࡅࡓࠤᅁ"))
        }
    if bstack1111llll_opy_(env.get(bstack11l1l1l_opy_ (u"ࠣࡖࡉࡣࡇ࡛ࡉࡍࡆࠥᅂ"))):
        return {
            bstack11l1l1l_opy_ (u"ࠤࡱࡥࡲ࡫ࠢᅃ"): bstack11l1l1l_opy_ (u"࡚ࠥ࡮ࡹࡵࡢ࡮ࠣࡗࡹࡻࡤࡪࡱࠣࡘࡪࡧ࡭ࠡࡕࡨࡶࡻ࡯ࡣࡦࡵࠥᅄ"),
            bstack11l1l1l_opy_ (u"ࠦࡧࡻࡩ࡭ࡦࡢࡹࡷࡲࠢᅅ"): bstack11l1l1l_opy_ (u"ࠧࢁࡽࡼࡿࠥᅆ").format(env.get(bstack11l1l1l_opy_ (u"࠭ࡓ࡚ࡕࡗࡉࡒࡥࡔࡆࡃࡐࡊࡔ࡛ࡎࡅࡃࡗࡍࡔࡔࡓࡆࡔ࡙ࡉࡗ࡛ࡒࡊࠩᅇ")), env.get(bstack11l1l1l_opy_ (u"ࠧࡔ࡛ࡖࡘࡊࡓ࡟ࡕࡇࡄࡑࡕࡘࡏࡋࡇࡆࡘࡎࡊࠧᅈ"))),
            bstack11l1l1l_opy_ (u"ࠣ࡬ࡲࡦࡤࡴࡡ࡮ࡧࠥᅉ"): env.get(bstack11l1l1l_opy_ (u"ࠤࡖ࡝ࡘ࡚ࡅࡎࡡࡇࡉࡋࡏࡎࡊࡖࡌࡓࡓࡏࡄࠣᅊ")),
            bstack11l1l1l_opy_ (u"ࠥࡦࡺ࡯࡬ࡥࡡࡱࡹࡲࡨࡥࡳࠤᅋ"): env.get(bstack11l1l1l_opy_ (u"ࠦࡇ࡛ࡉࡍࡆࡢࡆ࡚ࡏࡌࡅࡋࡇࠦᅌ"))
        }
    if bstack1111llll_opy_(env.get(bstack11l1l1l_opy_ (u"ࠧࡇࡐࡑࡘࡈ࡝ࡔࡘࠢᅍ"))):
        return {
            bstack11l1l1l_opy_ (u"ࠨ࡮ࡢ࡯ࡨࠦᅎ"): bstack11l1l1l_opy_ (u"ࠢࡂࡲࡳࡺࡪࡿ࡯ࡳࠤᅏ"),
            bstack11l1l1l_opy_ (u"ࠣࡤࡸ࡭ࡱࡪ࡟ࡶࡴ࡯ࠦᅐ"): bstack11l1l1l_opy_ (u"ࠤࡾࢁ࠴ࡶࡲࡰ࡬ࡨࡧࡹ࠵ࡻࡾ࠱ࡾࢁ࠴ࡨࡵࡪ࡮ࡧࡷ࠴ࢁࡽࠣᅑ").format(env.get(bstack11l1l1l_opy_ (u"ࠪࡅࡕࡖࡖࡆ࡛ࡒࡖࡤ࡛ࡒࡍࠩᅒ")), env.get(bstack11l1l1l_opy_ (u"ࠫࡆࡖࡐࡗࡇ࡜ࡓࡗࡥࡁࡄࡅࡒ࡙ࡓ࡚࡟ࡏࡃࡐࡉࠬᅓ")), env.get(bstack11l1l1l_opy_ (u"ࠬࡇࡐࡑࡘࡈ࡝ࡔࡘ࡟ࡑࡔࡒࡎࡊࡉࡔࡠࡕࡏ࡙ࡌ࠭ᅔ")), env.get(bstack11l1l1l_opy_ (u"࠭ࡁࡑࡒ࡙ࡉ࡞ࡕࡒࡠࡄࡘࡍࡑࡊ࡟ࡊࡆࠪᅕ"))),
            bstack11l1l1l_opy_ (u"ࠢ࡫ࡱࡥࡣࡳࡧ࡭ࡦࠤᅖ"): env.get(bstack11l1l1l_opy_ (u"ࠣࡃࡓࡔ࡛ࡋ࡙ࡐࡔࡢࡎࡔࡈ࡟ࡏࡃࡐࡉࠧᅗ")),
            bstack11l1l1l_opy_ (u"ࠤࡥࡹ࡮ࡲࡤࡠࡰࡸࡱࡧ࡫ࡲࠣᅘ"): env.get(bstack11l1l1l_opy_ (u"ࠥࡅࡕࡖࡖࡆ࡛ࡒࡖࡤࡈࡕࡊࡎࡇࡣࡓ࡛ࡍࡃࡇࡕࠦᅙ"))
        }
    if env.get(bstack11l1l1l_opy_ (u"ࠦࡆࡠࡕࡓࡇࡢࡌ࡙࡚ࡐࡠࡗࡖࡉࡗࡥࡁࡈࡇࡑࡘࠧᅚ")) and env.get(bstack11l1l1l_opy_ (u"࡚ࠧࡆࡠࡄࡘࡍࡑࡊࠢᅛ")):
        return {
            bstack11l1l1l_opy_ (u"ࠨ࡮ࡢ࡯ࡨࠦᅜ"): bstack11l1l1l_opy_ (u"ࠢࡂࡼࡸࡶࡪࠦࡃࡊࠤᅝ"),
            bstack11l1l1l_opy_ (u"ࠣࡤࡸ࡭ࡱࡪ࡟ࡶࡴ࡯ࠦᅞ"): bstack11l1l1l_opy_ (u"ࠤࡾࢁࢀࢃ࠯ࡠࡤࡸ࡭ࡱࡪ࠯ࡳࡧࡶࡹࡱࡺࡳࡀࡤࡸ࡭ࡱࡪࡉࡥ࠿ࡾࢁࠧᅟ").format(env.get(bstack11l1l1l_opy_ (u"ࠪࡗ࡞࡙ࡔࡆࡏࡢࡘࡊࡇࡍࡇࡑࡘࡒࡉࡇࡔࡊࡑࡑࡗࡊࡘࡖࡆࡔࡘࡖࡎ࠭ᅠ")), env.get(bstack11l1l1l_opy_ (u"ࠫࡘ࡟ࡓࡕࡇࡐࡣ࡙ࡋࡁࡎࡒࡕࡓࡏࡋࡃࡕࠩᅡ")), env.get(bstack11l1l1l_opy_ (u"ࠬࡈࡕࡊࡎࡇࡣࡇ࡛ࡉࡍࡆࡌࡈࠬᅢ"))),
            bstack11l1l1l_opy_ (u"ࠨࡪࡰࡤࡢࡲࡦࡳࡥࠣᅣ"): env.get(bstack11l1l1l_opy_ (u"ࠢࡃࡗࡌࡐࡉࡥࡂࡖࡋࡏࡈࡎࡊࠢᅤ")),
            bstack11l1l1l_opy_ (u"ࠣࡤࡸ࡭ࡱࡪ࡟࡯ࡷࡰࡦࡪࡸࠢᅥ"): env.get(bstack11l1l1l_opy_ (u"ࠤࡅ࡙ࡎࡒࡄࡠࡄࡘࡍࡑࡊࡉࡅࠤᅦ"))
        }
    if any([env.get(bstack11l1l1l_opy_ (u"ࠥࡇࡔࡊࡅࡃࡗࡌࡐࡉࡥࡂࡖࡋࡏࡈࡤࡏࡄࠣᅧ")), env.get(bstack11l1l1l_opy_ (u"ࠦࡈࡕࡄࡆࡄࡘࡍࡑࡊ࡟ࡓࡇࡖࡓࡑ࡜ࡅࡅࡡࡖࡓ࡚ࡘࡃࡆࡡ࡙ࡉࡗ࡙ࡉࡐࡐࠥᅨ")), env.get(bstack11l1l1l_opy_ (u"ࠧࡉࡏࡅࡇࡅ࡙ࡎࡒࡄࡠࡕࡒ࡙ࡗࡉࡅࡠࡘࡈࡖࡘࡏࡏࡏࠤᅩ"))]):
        return {
            bstack11l1l1l_opy_ (u"ࠨ࡮ࡢ࡯ࡨࠦᅪ"): bstack11l1l1l_opy_ (u"ࠢࡂ࡙ࡖࠤࡈࡵࡤࡦࡄࡸ࡭ࡱࡪࠢᅫ"),
            bstack11l1l1l_opy_ (u"ࠣࡤࡸ࡭ࡱࡪ࡟ࡶࡴ࡯ࠦᅬ"): env.get(bstack11l1l1l_opy_ (u"ࠤࡆࡓࡉࡋࡂࡖࡋࡏࡈࡤࡖࡕࡃࡎࡌࡇࡤࡈࡕࡊࡎࡇࡣ࡚ࡘࡌࠣᅭ")),
            bstack11l1l1l_opy_ (u"ࠥ࡮ࡴࡨ࡟࡯ࡣࡰࡩࠧᅮ"): env.get(bstack11l1l1l_opy_ (u"ࠦࡈࡕࡄࡆࡄࡘࡍࡑࡊ࡟ࡃࡗࡌࡐࡉࡥࡉࡅࠤᅯ")),
            bstack11l1l1l_opy_ (u"ࠧࡨࡵࡪ࡮ࡧࡣࡳࡻ࡭ࡣࡧࡵࠦᅰ"): env.get(bstack11l1l1l_opy_ (u"ࠨࡃࡐࡆࡈࡆ࡚ࡏࡌࡅࡡࡅ࡙ࡎࡒࡄࡠࡋࡇࠦᅱ"))
        }
    if env.get(bstack11l1l1l_opy_ (u"ࠢࡣࡣࡰࡦࡴࡵ࡟ࡣࡷ࡬ࡰࡩࡔࡵ࡮ࡤࡨࡶࠧᅲ")):
        return {
            bstack11l1l1l_opy_ (u"ࠣࡰࡤࡱࡪࠨᅳ"): bstack11l1l1l_opy_ (u"ࠤࡅࡥࡲࡨ࡯ࡰࠤᅴ"),
            bstack11l1l1l_opy_ (u"ࠥࡦࡺ࡯࡬ࡥࡡࡸࡶࡱࠨᅵ"): env.get(bstack11l1l1l_opy_ (u"ࠦࡧࡧ࡭ࡣࡱࡲࡣࡧࡻࡩ࡭ࡦࡕࡩࡸࡻ࡬ࡵࡵࡘࡶࡱࠨᅶ")),
            bstack11l1l1l_opy_ (u"ࠧࡰ࡯ࡣࡡࡱࡥࡲ࡫ࠢᅷ"): env.get(bstack11l1l1l_opy_ (u"ࠨࡢࡢ࡯ࡥࡳࡴࡥࡳࡩࡱࡵࡸࡏࡵࡢࡏࡣࡰࡩࠧᅸ")),
            bstack11l1l1l_opy_ (u"ࠢࡣࡷ࡬ࡰࡩࡥ࡮ࡶ࡯ࡥࡩࡷࠨᅹ"): env.get(bstack11l1l1l_opy_ (u"ࠣࡤࡤࡱࡧࡵ࡯ࡠࡤࡸ࡭ࡱࡪࡎࡶ࡯ࡥࡩࡷࠨᅺ"))
        }
    if env.get(bstack11l1l1l_opy_ (u"ࠤ࡚ࡉࡗࡉࡋࡆࡔࠥᅻ")) or env.get(bstack11l1l1l_opy_ (u"࡛ࠥࡊࡘࡃࡌࡇࡕࡣࡒࡇࡉࡏࡡࡓࡍࡕࡋࡌࡊࡐࡈࡣࡘ࡚ࡁࡓࡖࡈࡈࠧᅼ")):
        return {
            bstack11l1l1l_opy_ (u"ࠦࡳࡧ࡭ࡦࠤᅽ"): bstack11l1l1l_opy_ (u"ࠧ࡝ࡥࡳࡥ࡮ࡩࡷࠨᅾ"),
            bstack11l1l1l_opy_ (u"ࠨࡢࡶ࡫࡯ࡨࡤࡻࡲ࡭ࠤᅿ"): env.get(bstack11l1l1l_opy_ (u"ࠢࡘࡇࡕࡇࡐࡋࡒࡠࡄࡘࡍࡑࡊ࡟ࡖࡔࡏࠦᆀ")),
            bstack11l1l1l_opy_ (u"ࠣ࡬ࡲࡦࡤࡴࡡ࡮ࡧࠥᆁ"): bstack11l1l1l_opy_ (u"ࠤࡐࡥ࡮ࡴࠠࡑ࡫ࡳࡩࡱ࡯࡮ࡦࠤᆂ") if env.get(bstack11l1l1l_opy_ (u"࡛ࠥࡊࡘࡃࡌࡇࡕࡣࡒࡇࡉࡏࡡࡓࡍࡕࡋࡌࡊࡐࡈࡣࡘ࡚ࡁࡓࡖࡈࡈࠧᆃ")) else None,
            bstack11l1l1l_opy_ (u"ࠦࡧࡻࡩ࡭ࡦࡢࡲࡺࡳࡢࡦࡴࠥᆄ"): env.get(bstack11l1l1l_opy_ (u"ࠧ࡝ࡅࡓࡅࡎࡉࡗࡥࡇࡊࡖࡢࡇࡔࡓࡍࡊࡖࠥᆅ"))
        }
    if any([env.get(bstack11l1l1l_opy_ (u"ࠨࡇࡄࡒࡢࡔࡗࡕࡊࡆࡅࡗࠦᆆ")), env.get(bstack11l1l1l_opy_ (u"ࠢࡈࡅࡏࡓ࡚ࡊ࡟ࡑࡔࡒࡎࡊࡉࡔࠣᆇ")), env.get(bstack11l1l1l_opy_ (u"ࠣࡉࡒࡓࡌࡒࡅࡠࡅࡏࡓ࡚ࡊ࡟ࡑࡔࡒࡎࡊࡉࡔࠣᆈ"))]):
        return {
            bstack11l1l1l_opy_ (u"ࠤࡱࡥࡲ࡫ࠢᆉ"): bstack11l1l1l_opy_ (u"ࠥࡋࡴࡵࡧ࡭ࡧࠣࡇࡱࡵࡵࡥࠤᆊ"),
            bstack11l1l1l_opy_ (u"ࠦࡧࡻࡩ࡭ࡦࡢࡹࡷࡲࠢᆋ"): None,
            bstack11l1l1l_opy_ (u"ࠧࡰ࡯ࡣࡡࡱࡥࡲ࡫ࠢᆌ"): env.get(bstack11l1l1l_opy_ (u"ࠨࡐࡓࡑࡍࡉࡈ࡚࡟ࡊࡆࠥᆍ")),
            bstack11l1l1l_opy_ (u"ࠢࡣࡷ࡬ࡰࡩࡥ࡮ࡶ࡯ࡥࡩࡷࠨᆎ"): env.get(bstack11l1l1l_opy_ (u"ࠣࡄࡘࡍࡑࡊ࡟ࡊࡆࠥᆏ"))
        }
    if env.get(bstack11l1l1l_opy_ (u"ࠤࡖࡌࡎࡖࡐࡂࡄࡏࡉࠧᆐ")):
        return {
            bstack11l1l1l_opy_ (u"ࠥࡲࡦࡳࡥࠣᆑ"): bstack11l1l1l_opy_ (u"ࠦࡘ࡮ࡩࡱࡲࡤࡦࡱ࡫ࠢᆒ"),
            bstack11l1l1l_opy_ (u"ࠧࡨࡵࡪ࡮ࡧࡣࡺࡸ࡬ࠣᆓ"): env.get(bstack11l1l1l_opy_ (u"ࠨࡓࡉࡋࡓࡔࡆࡈࡌࡆࡡࡅ࡙ࡎࡒࡄࡠࡗࡕࡐࠧᆔ")),
            bstack11l1l1l_opy_ (u"ࠢ࡫ࡱࡥࡣࡳࡧ࡭ࡦࠤᆕ"): bstack11l1l1l_opy_ (u"ࠣࡌࡲࡦࠥࠩࡻࡾࠤᆖ").format(env.get(bstack11l1l1l_opy_ (u"ࠩࡖࡌࡎࡖࡐࡂࡄࡏࡉࡤࡐࡏࡃࡡࡌࡈࠬᆗ"))) if env.get(bstack11l1l1l_opy_ (u"ࠥࡗࡍࡏࡐࡑࡃࡅࡐࡊࡥࡊࡐࡄࡢࡍࡉࠨᆘ")) else None,
            bstack11l1l1l_opy_ (u"ࠦࡧࡻࡩ࡭ࡦࡢࡲࡺࡳࡢࡦࡴࠥᆙ"): env.get(bstack11l1l1l_opy_ (u"࡙ࠧࡈࡊࡒࡓࡅࡇࡒࡅࡠࡄࡘࡍࡑࡊ࡟ࡏࡗࡐࡆࡊࡘࠢᆚ"))
        }
    if bstack1111llll_opy_(env.get(bstack11l1l1l_opy_ (u"ࠨࡎࡆࡖࡏࡍࡋ࡟ࠢᆛ"))):
        return {
            bstack11l1l1l_opy_ (u"ࠢ࡯ࡣࡰࡩࠧᆜ"): bstack11l1l1l_opy_ (u"ࠣࡐࡨࡸࡱ࡯ࡦࡺࠤᆝ"),
            bstack11l1l1l_opy_ (u"ࠤࡥࡹ࡮ࡲࡤࡠࡷࡵࡰࠧᆞ"): env.get(bstack11l1l1l_opy_ (u"ࠥࡈࡊࡖࡌࡐ࡛ࡢ࡙ࡗࡒࠢᆟ")),
            bstack11l1l1l_opy_ (u"ࠦ࡯ࡵࡢࡠࡰࡤࡱࡪࠨᆠ"): env.get(bstack11l1l1l_opy_ (u"࡙ࠧࡉࡕࡇࡢࡒࡆࡓࡅࠣᆡ")),
            bstack11l1l1l_opy_ (u"ࠨࡢࡶ࡫࡯ࡨࡤࡴࡵ࡮ࡤࡨࡶࠧᆢ"): env.get(bstack11l1l1l_opy_ (u"ࠢࡃࡗࡌࡐࡉࡥࡉࡅࠤᆣ"))
        }
    if bstack1111llll_opy_(env.get(bstack11l1l1l_opy_ (u"ࠣࡉࡌࡘࡍ࡛ࡂࡠࡃࡆࡘࡎࡕࡎࡔࠤᆤ"))):
        return {
            bstack11l1l1l_opy_ (u"ࠤࡱࡥࡲ࡫ࠢᆥ"): bstack11l1l1l_opy_ (u"ࠥࡋ࡮ࡺࡈࡶࡤࠣࡅࡨࡺࡩࡰࡰࡶࠦᆦ"),
            bstack11l1l1l_opy_ (u"ࠦࡧࡻࡩ࡭ࡦࡢࡹࡷࡲࠢᆧ"): bstack11l1l1l_opy_ (u"ࠧࢁࡽ࠰ࡽࢀ࠳ࡦࡩࡴࡪࡱࡱࡷ࠴ࡸࡵ࡯ࡵ࠲ࡿࢂࠨᆨ").format(env.get(bstack11l1l1l_opy_ (u"࠭ࡇࡊࡖࡋ࡙ࡇࡥࡓࡆࡔ࡙ࡉࡗࡥࡕࡓࡎࠪᆩ")), env.get(bstack11l1l1l_opy_ (u"ࠧࡈࡋࡗࡌ࡚ࡈ࡟ࡓࡇࡓࡓࡘࡏࡔࡐࡔ࡜ࠫᆪ")), env.get(bstack11l1l1l_opy_ (u"ࠨࡉࡌࡘࡍ࡛ࡂࡠࡔࡘࡒࡤࡏࡄࠨᆫ"))),
            bstack11l1l1l_opy_ (u"ࠤ࡭ࡳࡧࡥ࡮ࡢ࡯ࡨࠦᆬ"): env.get(bstack11l1l1l_opy_ (u"ࠥࡋࡎ࡚ࡈࡖࡄࡢ࡛ࡔࡘࡋࡇࡎࡒ࡛ࠧᆭ")),
            bstack11l1l1l_opy_ (u"ࠦࡧࡻࡩ࡭ࡦࡢࡲࡺࡳࡢࡦࡴࠥᆮ"): env.get(bstack11l1l1l_opy_ (u"ࠧࡍࡉࡕࡊࡘࡆࡤࡘࡕࡏࡡࡌࡈࠧᆯ"))
        }
    if env.get(bstack11l1l1l_opy_ (u"ࠨࡃࡊࠤᆰ")) == bstack11l1l1l_opy_ (u"ࠢࡵࡴࡸࡩࠧᆱ") and env.get(bstack11l1l1l_opy_ (u"ࠣࡘࡈࡖࡈࡋࡌࠣᆲ")) == bstack11l1l1l_opy_ (u"ࠤ࠴ࠦᆳ"):
        return {
            bstack11l1l1l_opy_ (u"ࠥࡲࡦࡳࡥࠣᆴ"): bstack11l1l1l_opy_ (u"࡛ࠦ࡫ࡲࡤࡧ࡯ࠦᆵ"),
            bstack11l1l1l_opy_ (u"ࠧࡨࡵࡪ࡮ࡧࡣࡺࡸ࡬ࠣᆶ"): bstack11l1l1l_opy_ (u"ࠨࡨࡵࡶࡳ࠾࠴࠵ࡻࡾࠤᆷ").format(env.get(bstack11l1l1l_opy_ (u"ࠧࡗࡇࡕࡇࡊࡒ࡟ࡖࡔࡏࠫᆸ"))),
            bstack11l1l1l_opy_ (u"ࠣ࡬ࡲࡦࡤࡴࡡ࡮ࡧࠥᆹ"): None,
            bstack11l1l1l_opy_ (u"ࠤࡥࡹ࡮ࡲࡤࡠࡰࡸࡱࡧ࡫ࡲࠣᆺ"): None,
        }
    if env.get(bstack11l1l1l_opy_ (u"ࠥࡘࡊࡇࡍࡄࡋࡗ࡝ࡤ࡜ࡅࡓࡕࡌࡓࡓࠨᆻ")):
        return {
            bstack11l1l1l_opy_ (u"ࠦࡳࡧ࡭ࡦࠤᆼ"): bstack11l1l1l_opy_ (u"࡚ࠧࡥࡢ࡯ࡦ࡭ࡹࡿࠢᆽ"),
            bstack11l1l1l_opy_ (u"ࠨࡢࡶ࡫࡯ࡨࡤࡻࡲ࡭ࠤᆾ"): None,
            bstack11l1l1l_opy_ (u"ࠢ࡫ࡱࡥࡣࡳࡧ࡭ࡦࠤᆿ"): env.get(bstack11l1l1l_opy_ (u"ࠣࡖࡈࡅࡒࡉࡉࡕ࡛ࡢࡔࡗࡕࡊࡆࡅࡗࡣࡓࡇࡍࡆࠤᇀ")),
            bstack11l1l1l_opy_ (u"ࠤࡥࡹ࡮ࡲࡤࡠࡰࡸࡱࡧ࡫ࡲࠣᇁ"): env.get(bstack11l1l1l_opy_ (u"ࠥࡆ࡚ࡏࡌࡅࡡࡑ࡙ࡒࡈࡅࡓࠤᇂ"))
        }
    if any([env.get(bstack11l1l1l_opy_ (u"ࠦࡈࡕࡎࡄࡑࡘࡖࡘࡋࠢᇃ")), env.get(bstack11l1l1l_opy_ (u"ࠧࡉࡏࡏࡅࡒ࡙ࡗ࡙ࡅࡠࡗࡕࡐࠧᇄ")), env.get(bstack11l1l1l_opy_ (u"ࠨࡃࡐࡐࡆࡓ࡚ࡘࡓࡆࡡࡘࡗࡊࡘࡎࡂࡏࡈࠦᇅ")), env.get(bstack11l1l1l_opy_ (u"ࠢࡄࡑࡑࡇࡔ࡛ࡒࡔࡇࡢࡘࡊࡇࡍࠣᇆ"))]):
        return {
            bstack11l1l1l_opy_ (u"ࠣࡰࡤࡱࡪࠨᇇ"): bstack11l1l1l_opy_ (u"ࠤࡆࡳࡳࡩ࡯ࡶࡴࡶࡩࠧᇈ"),
            bstack11l1l1l_opy_ (u"ࠥࡦࡺ࡯࡬ࡥࡡࡸࡶࡱࠨᇉ"): None,
            bstack11l1l1l_opy_ (u"ࠦ࡯ࡵࡢࡠࡰࡤࡱࡪࠨᇊ"): env.get(bstack11l1l1l_opy_ (u"ࠧࡈࡕࡊࡎࡇࡣࡏࡕࡂࡠࡐࡄࡑࡊࠨᇋ")) or None,
            bstack11l1l1l_opy_ (u"ࠨࡢࡶ࡫࡯ࡨࡤࡴࡵ࡮ࡤࡨࡶࠧᇌ"): env.get(bstack11l1l1l_opy_ (u"ࠢࡃࡗࡌࡐࡉࡥࡉࡅࠤᇍ"), 0)
        }
    if env.get(bstack11l1l1l_opy_ (u"ࠣࡉࡒࡣࡏࡕࡂࡠࡐࡄࡑࡊࠨᇎ")):
        return {
            bstack11l1l1l_opy_ (u"ࠤࡱࡥࡲ࡫ࠢᇏ"): bstack11l1l1l_opy_ (u"ࠥࡋࡴࡉࡄࠣᇐ"),
            bstack11l1l1l_opy_ (u"ࠦࡧࡻࡩ࡭ࡦࡢࡹࡷࡲࠢᇑ"): None,
            bstack11l1l1l_opy_ (u"ࠧࡰ࡯ࡣࡡࡱࡥࡲ࡫ࠢᇒ"): env.get(bstack11l1l1l_opy_ (u"ࠨࡇࡐࡡࡍࡓࡇࡥࡎࡂࡏࡈࠦᇓ")),
            bstack11l1l1l_opy_ (u"ࠢࡣࡷ࡬ࡰࡩࡥ࡮ࡶ࡯ࡥࡩࡷࠨᇔ"): env.get(bstack11l1l1l_opy_ (u"ࠣࡉࡒࡣࡕࡏࡐࡆࡎࡌࡒࡊࡥࡃࡐࡗࡑࡘࡊࡘࠢᇕ"))
        }
    if env.get(bstack11l1l1l_opy_ (u"ࠤࡆࡊࡤࡈࡕࡊࡎࡇࡣࡎࡊࠢᇖ")):
        return {
            bstack11l1l1l_opy_ (u"ࠥࡲࡦࡳࡥࠣᇗ"): bstack11l1l1l_opy_ (u"ࠦࡈࡵࡤࡦࡈࡵࡩࡸ࡮ࠢᇘ"),
            bstack11l1l1l_opy_ (u"ࠧࡨࡵࡪ࡮ࡧࡣࡺࡸ࡬ࠣᇙ"): env.get(bstack11l1l1l_opy_ (u"ࠨࡃࡇࡡࡅ࡙ࡎࡒࡄࡠࡗࡕࡐࠧᇚ")),
            bstack11l1l1l_opy_ (u"ࠢ࡫ࡱࡥࡣࡳࡧ࡭ࡦࠤᇛ"): env.get(bstack11l1l1l_opy_ (u"ࠣࡅࡉࡣࡕࡏࡐࡆࡎࡌࡒࡊࡥࡎࡂࡏࡈࠦᇜ")),
            bstack11l1l1l_opy_ (u"ࠤࡥࡹ࡮ࡲࡤࡠࡰࡸࡱࡧ࡫ࡲࠣᇝ"): env.get(bstack11l1l1l_opy_ (u"ࠥࡇࡋࡥࡂࡖࡋࡏࡈࡤࡏࡄࠣᇞ"))
        }
    return {bstack11l1l1l_opy_ (u"ࠦࡧࡻࡩ࡭ࡦࡢࡲࡺࡳࡢࡦࡴࠥᇟ"): None}
def get_host_info():
    return {
        bstack11l1l1l_opy_ (u"ࠧ࡮࡯ࡴࡶࡱࡥࡲ࡫ࠢᇠ"): platform.node(),
        bstack11l1l1l_opy_ (u"ࠨࡰ࡭ࡣࡷࡪࡴࡸ࡭ࠣᇡ"): platform.system(),
        bstack11l1l1l_opy_ (u"ࠢࡵࡻࡳࡩࠧᇢ"): platform.machine(),
        bstack11l1l1l_opy_ (u"ࠣࡸࡨࡶࡸ࡯࡯࡯ࠤᇣ"): platform.version(),
        bstack11l1l1l_opy_ (u"ࠤࡤࡶࡨ࡮ࠢᇤ"): platform.architecture()[0]
    }
def bstack11l111lll_opy_():
    try:
        import selenium
        return True
    except ImportError:
        return False
def bstack11ll1ll11l_opy_():
    if bstack1lllll111l_opy_.get_property(bstack11l1l1l_opy_ (u"ࠪࡦࡸࡺࡡࡤ࡭ࡢࡷࡪࡹࡳࡪࡱࡱࠫᇥ")):
        return bstack11l1l1l_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࠪᇦ")
    return bstack11l1l1l_opy_ (u"ࠬࡻ࡮࡬ࡰࡲࡻࡳࡥࡧࡳ࡫ࡧࠫᇧ")
def bstack11ll1l11ll_opy_(driver):
    info = {
        bstack11l1l1l_opy_ (u"࠭ࡣࡢࡲࡤࡦ࡮ࡲࡩࡵ࡫ࡨࡷࠬᇨ"): driver.capabilities,
        bstack11l1l1l_opy_ (u"ࠧࡴࡧࡶࡷ࡮ࡵ࡮ࡠ࡫ࡧࠫᇩ"): driver.session_id,
        bstack11l1l1l_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࠩᇪ"): driver.capabilities.get(bstack11l1l1l_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡑࡥࡲ࡫ࠧᇫ"), None),
        bstack11l1l1l_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡣࡻ࡫ࡲࡴ࡫ࡲࡲࠬᇬ"): driver.capabilities.get(bstack11l1l1l_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶ࡛࡫ࡲࡴ࡫ࡲࡲࠬᇭ"), None),
        bstack11l1l1l_opy_ (u"ࠬࡶ࡬ࡢࡶࡩࡳࡷࡳࠧᇮ"): driver.capabilities.get(bstack11l1l1l_opy_ (u"࠭ࡰ࡭ࡣࡷࡪࡴࡸ࡭ࡏࡣࡰࡩࠬᇯ"), None),
    }
    if bstack11ll1ll11l_opy_() == bstack11l1l1l_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠭ᇰ"):
        info[bstack11l1l1l_opy_ (u"ࠨࡲࡵࡳࡩࡻࡣࡵࠩᇱ")] = bstack11l1l1l_opy_ (u"ࠩࡤࡴࡵ࠳ࡡࡶࡶࡲࡱࡦࡺࡥࠨᇲ") if bstack1ll111lll1_opy_() else bstack11l1l1l_opy_ (u"ࠪࡥࡺࡺ࡯࡮ࡣࡷࡩࠬᇳ")
    return info
def bstack1ll111lll1_opy_():
    if bstack1lllll111l_opy_.get_property(bstack11l1l1l_opy_ (u"ࠫࡦࡶࡰࡠࡣࡸࡸࡴࡳࡡࡵࡧࠪᇴ")):
        return True
    if bstack1111llll_opy_(os.environ.get(bstack11l1l1l_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣࡎ࡙࡟ࡂࡒࡓࡣࡆ࡛ࡔࡐࡏࡄࡘࡊ࠭ᇵ"), None)):
        return True
    return False
def bstack1ll11l1111_opy_(bstack11ll111l11_opy_, url, data, config):
    headers = config.get(bstack11l1l1l_opy_ (u"࠭ࡨࡦࡣࡧࡩࡷࡹࠧᇶ"), None)
    proxies = bstack1ll1l1l1l_opy_(config, url)
    auth = config.get(bstack11l1l1l_opy_ (u"ࠧࡢࡷࡷ࡬ࠬᇷ"), None)
    response = requests.request(
            bstack11ll111l11_opy_,
            url=url,
            headers=headers,
            auth=auth,
            json=data,
            proxies=proxies
        )
    return response
def bstack1lll111111_opy_(bstack1l1llllll_opy_, size):
    bstack11l1l1l1l_opy_ = []
    while len(bstack1l1llllll_opy_) > size:
        bstack11ll1ll1l_opy_ = bstack1l1llllll_opy_[:size]
        bstack11l1l1l1l_opy_.append(bstack11ll1ll1l_opy_)
        bstack1l1llllll_opy_ = bstack1l1llllll_opy_[size:]
    bstack11l1l1l1l_opy_.append(bstack1l1llllll_opy_)
    return bstack11l1l1l1l_opy_
def bstack11ll1l111l_opy_(message, bstack11lll11ll1_opy_=False):
    os.write(1, bytes(message, bstack11l1l1l_opy_ (u"ࠨࡷࡷࡪ࠲࠾ࠧᇸ")))
    os.write(1, bytes(bstack11l1l1l_opy_ (u"ࠩ࡟ࡲࠬᇹ"), bstack11l1l1l_opy_ (u"ࠪࡹࡹ࡬࠭࠹ࠩᇺ")))
    if bstack11lll11ll1_opy_:
        with open(bstack11l1l1l_opy_ (u"ࠫࡧࡹࡴࡢࡥ࡮࠱ࡴ࠷࠱ࡺ࠯ࠪᇻ") + os.environ[bstack11l1l1l_opy_ (u"ࠬࡈࡓࡠࡖࡈࡗ࡙ࡕࡐࡔࡡࡅ࡙ࡎࡒࡄࡠࡊࡄࡗࡍࡋࡄࡠࡋࡇࠫᇼ")] + bstack11l1l1l_opy_ (u"࠭࠮࡭ࡱࡪࠫᇽ"), bstack11l1l1l_opy_ (u"ࠧࡢࠩᇾ")) as f:
            f.write(message + bstack11l1l1l_opy_ (u"ࠨ࡞ࡱࠫᇿ"))
def bstack11lll1l1ll_opy_():
    return os.environ[bstack11l1l1l_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡃࡘࡘࡔࡓࡁࡕࡋࡒࡒࠬሀ")].lower() == bstack11l1l1l_opy_ (u"ࠪࡸࡷࡻࡥࠨሁ")
def bstack1llllll1l1_opy_(bstack11ll1l11l1_opy_):
    return bstack11l1l1l_opy_ (u"ࠫࢀࢃ࠯ࡼࡿࠪሂ").format(bstack11llll1l11_opy_, bstack11ll1l11l1_opy_)
def bstack1llllll11l_opy_():
    return datetime.datetime.utcnow().isoformat() + bstack11l1l1l_opy_ (u"ࠬࡠࠧሃ")
def bstack11ll1ll1l1_opy_(start, finish):
    return (datetime.datetime.fromisoformat(finish.rstrip(bstack11l1l1l_opy_ (u"࡚࠭ࠨሄ"))) - datetime.datetime.fromisoformat(start.rstrip(bstack11l1l1l_opy_ (u"࡛ࠧࠩህ")))).total_seconds() * 1000
def bstack11ll1lll11_opy_(timestamp):
    return datetime.datetime.utcfromtimestamp(timestamp).isoformat() + bstack11l1l1l_opy_ (u"ࠨ࡜ࠪሆ")
def bstack11lll111l1_opy_(bstack11ll1l1lll_opy_):
    date_format = bstack11l1l1l_opy_ (u"ࠩࠨ࡝ࠪࡳࠥࡥࠢࠨࡌ࠿ࠫࡍ࠻ࠧࡖ࠲ࠪ࡬ࠧሇ")
    bstack11lll111ll_opy_ = datetime.datetime.strptime(bstack11ll1l1lll_opy_, date_format)
    return bstack11lll111ll_opy_.isoformat() + bstack11l1l1l_opy_ (u"ࠪ࡞ࠬለ")
def bstack11ll1111ll_opy_(outcome):
    _, exception, _ = outcome.excinfo or (None, None, None)
    if exception:
        return bstack11l1l1l_opy_ (u"ࠫ࡫ࡧࡩ࡭ࡧࡧࠫሉ")
    else:
        return bstack11l1l1l_opy_ (u"ࠬࡶࡡࡴࡵࡨࡨࠬሊ")
def bstack1111llll_opy_(val):
    if val is None:
        return False
    return val.__str__().lower() == bstack11l1l1l_opy_ (u"࠭ࡴࡳࡷࡨࠫላ")
def bstack11lll11111_opy_(val):
    return val.__str__().lower() == bstack11l1l1l_opy_ (u"ࠧࡧࡣ࡯ࡷࡪ࠭ሌ")
def bstack1l11ll1ll1_opy_(bstack11ll11l111_opy_=Exception, class_method=False, default_value=None):
    def decorator(func):
        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except bstack11ll11l111_opy_ as e:
                print(bstack11l1l1l_opy_ (u"ࠣࡇࡻࡧࡪࡶࡴࡪࡱࡱࠤ࡮ࡴࠠࡧࡷࡱࡧࡹ࡯࡯࡯ࠢࡾࢁࠥ࠳࠾ࠡࡽࢀ࠾ࠥࢁࡽࠣል").format(func.__name__, bstack11ll11l111_opy_.__name__, str(e)))
                return default_value
        return wrapper
    def bstack11ll1ll1ll_opy_(bstack11llll1111_opy_):
        def wrapped(cls, *args, **kwargs):
            try:
                return bstack11llll1111_opy_(cls, *args, **kwargs)
            except bstack11ll11l111_opy_ as e:
                print(bstack11l1l1l_opy_ (u"ࠤࡈࡼࡨ࡫ࡰࡵ࡫ࡲࡲࠥ࡯࡮ࠡࡨࡸࡲࡨࡺࡩࡰࡰࠣࡿࢂࠦ࠭࠿ࠢࡾࢁ࠿ࠦࡻࡾࠤሎ").format(bstack11llll1111_opy_.__name__, bstack11ll11l111_opy_.__name__, str(e)))
                return default_value
        return wrapped
    if class_method:
        return bstack11ll1ll1ll_opy_
    else:
        return decorator
def bstack1ll11ll11_opy_(bstack1l111ll1ll_opy_):
    if bstack11l1l1l_opy_ (u"ࠪࡥࡺࡺ࡯࡮ࡣࡷ࡭ࡴࡴࠧሏ") in bstack1l111ll1ll_opy_ and bstack11lll11111_opy_(bstack1l111ll1ll_opy_[bstack11l1l1l_opy_ (u"ࠫࡦࡻࡴࡰ࡯ࡤࡸ࡮ࡵ࡮ࠨሐ")]):
        return False
    if bstack11l1l1l_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࡅࡺࡺ࡯࡮ࡣࡷ࡭ࡴࡴࠧሑ") in bstack1l111ll1ll_opy_ and bstack11lll11111_opy_(bstack1l111ll1ll_opy_[bstack11l1l1l_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࡆࡻࡴࡰ࡯ࡤࡸ࡮ࡵ࡮ࠨሒ")]):
        return False
    return True
def bstack11ll1111_opy_():
    try:
        from pytest_bdd import reporting
        return True
    except Exception as e:
        return False
def bstack1llllllll_opy_(hub_url):
    if bstack1llll1lll_opy_() <= version.parse(bstack11l1l1l_opy_ (u"ࠧ࠴࠰࠴࠷࠳࠶ࠧሓ")):
        if hub_url != bstack11l1l1l_opy_ (u"ࠨࠩሔ"):
            return bstack11l1l1l_opy_ (u"ࠤ࡫ࡸࡹࡶ࠺࠰࠱ࠥሕ") + hub_url + bstack11l1l1l_opy_ (u"ࠥ࠾࠽࠶࠯ࡸࡦ࠲࡬ࡺࡨࠢሖ")
        return bstack1111111ll_opy_
    if hub_url != bstack11l1l1l_opy_ (u"ࠫࠬሗ"):
        return bstack11l1l1l_opy_ (u"ࠧ࡮ࡴࡵࡲࡶ࠾࠴࠵ࠢመ") + hub_url + bstack11l1l1l_opy_ (u"ࠨ࠯ࡸࡦ࠲࡬ࡺࡨࠢሙ")
    return bstack1111lll1l_opy_
def bstack11ll11lll1_opy_():
    return isinstance(os.getenv(bstack11l1l1l_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡐ࡚ࡖࡈࡗ࡙ࡥࡐࡍࡗࡊࡍࡓ࠭ሚ")), str)
def bstack1ll1l111ll_opy_(url):
    return urlparse(url).hostname
def bstack111l1l11_opy_(hostname):
    for bstack111ll1111_opy_ in bstack11111l1l_opy_:
        regex = re.compile(bstack111ll1111_opy_)
        if regex.match(hostname):
            return True
    return False
def bstack11lll1l1l1_opy_(bstack11ll11ll1l_opy_, file_name, logger):
    bstack1ll1l1lll1_opy_ = os.path.join(os.path.expanduser(bstack11l1l1l_opy_ (u"ࠨࢀࠪማ")), bstack11ll11ll1l_opy_)
    try:
        if not os.path.exists(bstack1ll1l1lll1_opy_):
            os.makedirs(bstack1ll1l1lll1_opy_)
        file_path = os.path.join(os.path.expanduser(bstack11l1l1l_opy_ (u"ࠩࢁࠫሜ")), bstack11ll11ll1l_opy_, file_name)
        if not os.path.isfile(file_path):
            with open(file_path, bstack11l1l1l_opy_ (u"ࠪࡻࠬም")):
                pass
            with open(file_path, bstack11l1l1l_opy_ (u"ࠦࡼ࠱ࠢሞ")) as outfile:
                json.dump({}, outfile)
        return file_path
    except Exception as e:
        logger.debug(bstack1l1lll11l1_opy_.format(str(e)))
def bstack11lll1l111_opy_(file_name, key, value, logger):
    file_path = bstack11lll1l1l1_opy_(bstack11l1l1l_opy_ (u"ࠬ࠴ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࠬሟ"), file_name, logger)
    if file_path != None:
        if os.path.exists(file_path):
            bstack1ll1llll1l_opy_ = json.load(open(file_path, bstack11l1l1l_opy_ (u"࠭ࡲࡣࠩሠ")))
        else:
            bstack1ll1llll1l_opy_ = {}
        bstack1ll1llll1l_opy_[key] = value
        with open(file_path, bstack11l1l1l_opy_ (u"ࠢࡸ࠭ࠥሡ")) as outfile:
            json.dump(bstack1ll1llll1l_opy_, outfile)
def bstack1lll111lll_opy_(file_name, logger):
    file_path = bstack11lll1l1l1_opy_(bstack11l1l1l_opy_ (u"ࠨ࠰ࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࠨሢ"), file_name, logger)
    bstack1ll1llll1l_opy_ = {}
    if file_path != None and os.path.exists(file_path):
        with open(file_path, bstack11l1l1l_opy_ (u"ࠩࡵࠫሣ")) as bstack1ll1l1lll_opy_:
            bstack1ll1llll1l_opy_ = json.load(bstack1ll1l1lll_opy_)
    return bstack1ll1llll1l_opy_
def bstack111l1llll_opy_(file_path, logger):
    try:
        if os.path.exists(file_path):
            os.remove(file_path)
    except Exception as e:
        logger.debug(bstack11l1l1l_opy_ (u"ࠪࡉࡷࡸ࡯ࡳࠢ࡬ࡲࠥࡪࡥ࡭ࡧࡷ࡭ࡳ࡭ࠠࡧ࡫࡯ࡩ࠿ࠦࠧሤ") + file_path + bstack11l1l1l_opy_ (u"ࠫࠥ࠭ሥ") + str(e))
def bstack1llll1lll_opy_():
    from selenium import webdriver
    return version.parse(webdriver.__version__)
class Notset:
    def __repr__(self):
        return bstack11l1l1l_opy_ (u"ࠧࡂࡎࡐࡖࡖࡉ࡙ࡄࠢሦ")
def bstack1ll111l111_opy_(config):
    if bstack11l1l1l_opy_ (u"࠭ࡩࡴࡒ࡯ࡥࡾࡽࡲࡪࡩ࡫ࡸࠬሧ") in config:
        del (config[bstack11l1l1l_opy_ (u"ࠧࡪࡵࡓࡰࡦࡿࡷࡳ࡫ࡪ࡬ࡹ࠭ረ")])
        return False
    if bstack1llll1lll_opy_() < version.parse(bstack11l1l1l_opy_ (u"ࠨ࠵࠱࠸࠳࠶ࠧሩ")):
        return False
    if bstack1llll1lll_opy_() >= version.parse(bstack11l1l1l_opy_ (u"ࠩ࠷࠲࠶࠴࠵ࠨሪ")):
        return True
    if bstack11l1l1l_opy_ (u"ࠪࡹࡸ࡫ࡗ࠴ࡅࠪራ") in config and config[bstack11l1l1l_opy_ (u"ࠫࡺࡹࡥࡘ࠵ࡆࠫሬ")] is False:
        return False
    else:
        return True
def bstack1l1lll11l_opy_(args_list, bstack11lll11lll_opy_):
    index = -1
    for value in bstack11lll11lll_opy_:
        try:
            index = args_list.index(value)
            return index
        except Exception as e:
            return index
    return index
class Result:
    def __init__(self, result=None, duration=None, exception=None, bstack1l1l1l1l11_opy_=None):
        self.result = result
        self.duration = duration
        self.exception = exception
        self.exception_type = type(self.exception).__name__ if exception else None
        self.bstack1l1l1l1l11_opy_ = bstack1l1l1l1l11_opy_
    @classmethod
    def passed(cls):
        return Result(result=bstack11l1l1l_opy_ (u"ࠬࡶࡡࡴࡵࡨࡨࠬር"))
    @classmethod
    def failed(cls, exception=None):
        return Result(result=bstack11l1l1l_opy_ (u"࠭ࡦࡢ࡫࡯ࡩࡩ࠭ሮ"), exception=exception)
    def bstack1l111ll11l_opy_(self):
        if self.result != bstack11l1l1l_opy_ (u"ࠧࡧࡣ࡬ࡰࡪࡪࠧሯ"):
            return None
        if bstack11l1l1l_opy_ (u"ࠣࡃࡶࡷࡪࡸࡴࡪࡱࡱࠦሰ") in self.exception_type:
            return bstack11l1l1l_opy_ (u"ࠤࡄࡷࡸ࡫ࡲࡵ࡫ࡲࡲࡊࡸࡲࡰࡴࠥሱ")
        return bstack11l1l1l_opy_ (u"࡙ࠥࡳ࡮ࡡ࡯ࡦ࡯ࡩࡩࡋࡲࡳࡱࡵࠦሲ")
    def bstack11ll11llll_opy_(self):
        if self.result != bstack11l1l1l_opy_ (u"ࠫ࡫ࡧࡩ࡭ࡧࡧࠫሳ"):
            return None
        if self.bstack1l1l1l1l11_opy_:
            return self.bstack1l1l1l1l11_opy_
        return bstack11ll1l1l11_opy_(self.exception)
def bstack11ll1l1l11_opy_(exc):
    return [traceback.format_exception(exc)]
def bstack11lll1l11l_opy_(message):
    if isinstance(message, str):
        return not bool(message and message.strip())
    return True
def bstack1111l11l_opy_(object, key, default_value):
    if not object or not object.__dict__:
        return default_value
    if key in object.__dict__.keys():
        return object.__dict__.get(key)
    return default_value
def bstack1lll1ll1l_opy_(config, logger):
    try:
        import playwright
        bstack11ll11111l_opy_ = playwright.__file__
        bstack11ll1lllll_opy_ = os.path.split(bstack11ll11111l_opy_)
        bstack11ll1l1111_opy_ = bstack11ll1lllll_opy_[0] + bstack11l1l1l_opy_ (u"ࠬ࠵ࡤࡳ࡫ࡹࡩࡷ࠵ࡰࡢࡥ࡮ࡥ࡬࡫࠯࡭࡫ࡥ࠳ࡨࡲࡩ࠰ࡥ࡯࡭࠳ࡰࡳࠨሴ")
        os.environ[bstack11l1l1l_opy_ (u"࠭ࡇࡍࡑࡅࡅࡑࡥࡁࡈࡇࡑࡘࡤࡎࡔࡕࡒࡢࡔࡗࡕࡘ࡚ࠩስ")] = bstack1ll1111l_opy_(config)
        with open(bstack11ll1l1111_opy_, bstack11l1l1l_opy_ (u"ࠧࡳࠩሶ")) as f:
            bstack1ll11l1ll_opy_ = f.read()
            bstack11l1llllll_opy_ = bstack11l1l1l_opy_ (u"ࠨࡩ࡯ࡳࡧࡧ࡬࠮ࡣࡪࡩࡳࡺࠧሷ")
            bstack11ll1llll1_opy_ = bstack1ll11l1ll_opy_.find(bstack11l1llllll_opy_)
            if bstack11ll1llll1_opy_ == -1:
              process = subprocess.Popen(bstack11l1l1l_opy_ (u"ࠤࡱࡴࡲࠦࡩ࡯ࡵࡷࡥࡱࡲࠠࡨ࡮ࡲࡦࡦࡲ࠭ࡢࡩࡨࡲࡹࠨሸ"), shell=True, cwd=bstack11ll1lllll_opy_[0])
              process.wait()
              bstack11ll111l1l_opy_ = bstack11l1l1l_opy_ (u"ࠪࠦࡺࡹࡥࠡࡵࡷࡶ࡮ࡩࡴࠣ࠽ࠪሹ")
              bstack11lll11l11_opy_ = bstack11l1l1l_opy_ (u"ࠦࠧࠨࠠ࡝ࠤࡸࡷࡪࠦࡳࡵࡴ࡬ࡧࡹࡢࠢ࠼ࠢࡦࡳࡳࡹࡴࠡࡽࠣࡦࡴࡵࡴࡴࡶࡵࡥࡵࠦࡽࠡ࠿ࠣࡶࡪࡷࡵࡪࡴࡨࠬࠬ࡭࡬ࡰࡤࡤࡰ࠲ࡧࡧࡦࡰࡷࠫ࠮ࡁࠠࡪࡨࠣࠬࡵࡸ࡯ࡤࡧࡶࡷ࠳࡫࡮ࡷ࠰ࡊࡐࡔࡈࡁࡍࡡࡄࡋࡊࡔࡔࡠࡊࡗࡘࡕࡥࡐࡓࡑ࡛࡝࠮ࠦࡢࡰࡱࡷࡷࡹࡸࡡࡱࠪࠬ࠿ࠥࠨࠢࠣሺ")
              bstack11ll1111l1_opy_ = bstack1ll11l1ll_opy_.replace(bstack11ll111l1l_opy_, bstack11lll11l11_opy_)
              with open(bstack11ll1l1111_opy_, bstack11l1l1l_opy_ (u"ࠬࡽࠧሻ")) as f:
                f.write(bstack11ll1111l1_opy_)
    except Exception as e:
        logger.error(bstack1ll11l11ll_opy_.format(str(e)))
def bstack11l11ll11_opy_():
  try:
    bstack11ll111111_opy_ = os.path.join(tempfile.gettempdir(), bstack11l1l1l_opy_ (u"࠭࡯ࡱࡶ࡬ࡱࡦࡲ࡟ࡩࡷࡥࡣࡺࡸ࡬࠯࡬ࡶࡳࡳ࠭ሼ"))
    bstack11lll1lll1_opy_ = []
    if os.path.exists(bstack11ll111111_opy_):
      with open(bstack11ll111111_opy_) as f:
        bstack11lll1lll1_opy_ = json.load(f)
      os.remove(bstack11ll111111_opy_)
    return bstack11lll1lll1_opy_
  except:
    pass
  return []
def bstack1llll1111_opy_(bstack1l1llll11l_opy_):
  try:
    bstack11lll1lll1_opy_ = []
    bstack11ll111111_opy_ = os.path.join(tempfile.gettempdir(), bstack11l1l1l_opy_ (u"ࠧࡰࡲࡷ࡭ࡲࡧ࡬ࡠࡪࡸࡦࡤࡻࡲ࡭࠰࡭ࡷࡴࡴࠧሽ"))
    if os.path.exists(bstack11ll111111_opy_):
      with open(bstack11ll111111_opy_) as f:
        bstack11lll1lll1_opy_ = json.load(f)
    bstack11lll1lll1_opy_.append(bstack1l1llll11l_opy_)
    with open(bstack11ll111111_opy_, bstack11l1l1l_opy_ (u"ࠨࡹࠪሾ")) as f:
        json.dump(bstack11lll1lll1_opy_, f)
  except:
    pass
def bstack1ll111111_opy_(logger, bstack11ll111ll1_opy_ = False):
  try:
    test_name = os.environ.get(bstack11l1l1l_opy_ (u"ࠩࡓ࡝࡙ࡋࡓࡕࡡࡗࡉࡘ࡚࡟ࡏࡃࡐࡉࠬሿ"), bstack11l1l1l_opy_ (u"ࠪࠫቀ"))
    if test_name == bstack11l1l1l_opy_ (u"ࠫࠬቁ"):
        test_name = threading.current_thread().__dict__.get(bstack11l1l1l_opy_ (u"ࠬࡶࡹࡵࡧࡶࡸࡇࡪࡤࡠࡶࡨࡷࡹࡥ࡮ࡢ࡯ࡨࠫቂ"), bstack11l1l1l_opy_ (u"࠭ࠧቃ"))
    bstack11ll1l1l1l_opy_ = bstack11l1l1l_opy_ (u"ࠧ࠭ࠢࠪቄ").join(threading.current_thread().bstackTestErrorMessages)
    if bstack11ll111ll1_opy_:
        bstack1111l11l1_opy_ = os.environ.get(bstack11l1l1l_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡑࡎࡄࡘࡋࡕࡒࡎࡡࡌࡒࡉࡋࡘࠨቅ"), bstack11l1l1l_opy_ (u"ࠩ࠳ࠫቆ"))
        bstack1l1ll1lll1_opy_ = {bstack11l1l1l_opy_ (u"ࠪࡲࡦࡳࡥࠨቇ"): test_name, bstack11l1l1l_opy_ (u"ࠫࡪࡸࡲࡰࡴࠪቈ"): bstack11ll1l1l1l_opy_, bstack11l1l1l_opy_ (u"ࠬ࡯࡮ࡥࡧࡻࠫ቉"): bstack1111l11l1_opy_}
        bstack11ll11l1l1_opy_ = []
        bstack11ll11l1ll_opy_ = os.path.join(tempfile.gettempdir(), bstack11l1l1l_opy_ (u"࠭ࡰࡺࡶࡨࡷࡹࡥࡰࡱࡲࡢࡩࡷࡸ࡯ࡳࡡ࡯࡭ࡸࡺ࠮࡫ࡵࡲࡲࠬቊ"))
        if os.path.exists(bstack11ll11l1ll_opy_):
            with open(bstack11ll11l1ll_opy_) as f:
                bstack11ll11l1l1_opy_ = json.load(f)
        bstack11ll11l1l1_opy_.append(bstack1l1ll1lll1_opy_)
        with open(bstack11ll11l1ll_opy_, bstack11l1l1l_opy_ (u"ࠧࡸࠩቋ")) as f:
            json.dump(bstack11ll11l1l1_opy_, f)
    else:
        bstack1l1ll1lll1_opy_ = {bstack11l1l1l_opy_ (u"ࠨࡰࡤࡱࡪ࠭ቌ"): test_name, bstack11l1l1l_opy_ (u"ࠩࡨࡶࡷࡵࡲࠨቍ"): bstack11ll1l1l1l_opy_, bstack11l1l1l_opy_ (u"ࠪ࡭ࡳࡪࡥࡹࠩ቎"): str(multiprocessing.current_process().name)}
        if bstack11l1l1l_opy_ (u"ࠫࡧࡹࡴࡢࡥ࡮ࡣࡪࡸࡲࡰࡴࡢࡰ࡮ࡹࡴࠨ቏") not in multiprocessing.current_process().__dict__.keys():
            multiprocessing.current_process().bstack_error_list = []
        multiprocessing.current_process().bstack_error_list.append(bstack1l1ll1lll1_opy_)
  except Exception as e:
      logger.warn(bstack11l1l1l_opy_ (u"࡛ࠧ࡮ࡢࡤ࡯ࡩࠥࡺ࡯ࠡࡵࡷࡳࡷ࡫ࠠࡱࡻࡷࡩࡸࡺࠠࡧࡷࡱࡲࡪࡲࠠࡥࡣࡷࡥ࠿ࠦࡻࡾࠤቐ").format(e))
def bstack1llll1l1ll_opy_(error_message, test_name, index, logger):
  try:
    bstack11ll1ll111_opy_ = []
    bstack1l1ll1lll1_opy_ = {bstack11l1l1l_opy_ (u"࠭࡮ࡢ࡯ࡨࠫቑ"): test_name, bstack11l1l1l_opy_ (u"ࠧࡦࡴࡵࡳࡷ࠭ቒ"): error_message, bstack11l1l1l_opy_ (u"ࠨ࡫ࡱࡨࡪࡾࠧቓ"): index}
    bstack11lll1llll_opy_ = os.path.join(tempfile.gettempdir(), bstack11l1l1l_opy_ (u"ࠩࡵࡳࡧࡵࡴࡠࡧࡵࡶࡴࡸ࡟࡭࡫ࡶࡸ࠳ࡰࡳࡰࡰࠪቔ"))
    if os.path.exists(bstack11lll1llll_opy_):
        with open(bstack11lll1llll_opy_) as f:
            bstack11ll1ll111_opy_ = json.load(f)
    bstack11ll1ll111_opy_.append(bstack1l1ll1lll1_opy_)
    with open(bstack11lll1llll_opy_, bstack11l1l1l_opy_ (u"ࠪࡻࠬቕ")) as f:
        json.dump(bstack11ll1ll111_opy_, f)
  except Exception as e:
    logger.warn(bstack11l1l1l_opy_ (u"࡚ࠦࡴࡡࡣ࡮ࡨࠤࡹࡵࠠࡴࡶࡲࡶࡪࠦࡲࡰࡤࡲࡸࠥ࡬ࡵ࡯ࡰࡨࡰࠥࡪࡡࡵࡣ࠽ࠤࢀࢃࠢቖ").format(e))
def bstack111l111l1_opy_(bstack111lllll1_opy_, name, logger):
  try:
    bstack1l1ll1lll1_opy_ = {bstack11l1l1l_opy_ (u"ࠬࡴࡡ࡮ࡧࠪ቗"): name, bstack11l1l1l_opy_ (u"࠭ࡥࡳࡴࡲࡶࠬቘ"): bstack111lllll1_opy_, bstack11l1l1l_opy_ (u"ࠧࡪࡰࡧࡩࡽ࠭቙"): str(threading.current_thread()._name)}
    return bstack1l1ll1lll1_opy_
  except Exception as e:
    logger.warn(bstack11l1l1l_opy_ (u"ࠣࡗࡱࡥࡧࡲࡥࠡࡶࡲࠤࡸࡺ࡯ࡳࡧࠣࡦࡪ࡮ࡡࡷࡧࠣࡪࡺࡴ࡮ࡦ࡮ࠣࡨࡦࡺࡡ࠻ࠢࡾࢁࠧቚ").format(e))
  return
def bstack1lll1ll111_opy_(framework):
    if framework.lower() == bstack11l1l1l_opy_ (u"ࠩࡳࡽࡹ࡫ࡳࡵࠩቛ"):
        return bstack1ll111ll1_opy_.version()
    elif framework.lower() == bstack11l1l1l_opy_ (u"ࠪࡶࡴࡨ࡯ࡵࠩቜ"):
        return RobotHandler.version()
    elif framework.lower() == bstack11l1l1l_opy_ (u"ࠫࡧ࡫ࡨࡢࡸࡨࠫቝ"):
        import behave
        return behave.__version__
    else:
        return bstack11l1l1l_opy_ (u"ࠬࡻ࡮࡬ࡰࡲࡻࡳ࠭቞")