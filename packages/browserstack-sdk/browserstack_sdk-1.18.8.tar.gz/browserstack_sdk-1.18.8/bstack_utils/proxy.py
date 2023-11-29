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
from urllib.parse import urlparse
from bstack_utils.messages import bstack11l1l1l1ll_opy_
def bstack111lll11l1_opy_(url):
    try:
        result = urlparse(url)
        return all([result.scheme, result.netloc])
    except:
        return False
def bstack111lll1111_opy_(bstack111ll1llll_opy_, bstack111lll111l_opy_):
    from pypac import get_pac
    from pypac import PACSession
    from pypac.parser import PACFile
    import socket
    if os.path.isfile(bstack111ll1llll_opy_):
        with open(bstack111ll1llll_opy_) as f:
            pac = PACFile(f.read())
    elif bstack111lll11l1_opy_(bstack111ll1llll_opy_):
        pac = get_pac(url=bstack111ll1llll_opy_)
    else:
        raise Exception(bstack11l1l1l_opy_ (u"ࠩࡓࡥࡨࠦࡦࡪ࡮ࡨࠤࡩࡵࡥࡴࠢࡱࡳࡹࠦࡥࡹ࡫ࡶࡸ࠿ࠦࡻࡾࠩጦ").format(bstack111ll1llll_opy_))
    session = PACSession(pac)
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect((bstack11l1l1l_opy_ (u"ࠥ࠼࠳࠾࠮࠹࠰࠻ࠦጧ"), 80))
        bstack111lll1l1l_opy_ = s.getsockname()[0]
        s.close()
    except:
        bstack111lll1l1l_opy_ = bstack11l1l1l_opy_ (u"ࠫ࠵࠴࠰࠯࠲࠱࠴ࠬጨ")
    proxy_url = session.get_pac().find_proxy_for_url(bstack111lll111l_opy_, bstack111lll1l1l_opy_)
    return proxy_url
def bstack1l11l111l_opy_(config):
    return bstack11l1l1l_opy_ (u"ࠬ࡮ࡴࡵࡲࡓࡶࡴࡾࡹࠨጩ") in config or bstack11l1l1l_opy_ (u"࠭ࡨࡵࡶࡳࡷࡕࡸ࡯ࡹࡻࠪጪ") in config
def bstack1ll1111l_opy_(config):
    if not bstack1l11l111l_opy_(config):
        return
    if config.get(bstack11l1l1l_opy_ (u"ࠧࡩࡶࡷࡴࡕࡸ࡯ࡹࡻࠪጫ")):
        return config.get(bstack11l1l1l_opy_ (u"ࠨࡪࡷࡸࡵࡖࡲࡰࡺࡼࠫጬ"))
    if config.get(bstack11l1l1l_opy_ (u"ࠩ࡫ࡸࡹࡶࡳࡑࡴࡲࡼࡾ࠭ጭ")):
        return config.get(bstack11l1l1l_opy_ (u"ࠪ࡬ࡹࡺࡰࡴࡒࡵࡳࡽࡿࠧጮ"))
def bstack1ll1l1l1l_opy_(config, bstack111lll111l_opy_):
    proxy = bstack1ll1111l_opy_(config)
    proxies = {}
    if config.get(bstack11l1l1l_opy_ (u"ࠫ࡭ࡺࡴࡱࡒࡵࡳࡽࡿࠧጯ")) or config.get(bstack11l1l1l_opy_ (u"ࠬ࡮ࡴࡵࡲࡶࡔࡷࡵࡸࡺࠩጰ")):
        if proxy.endswith(bstack11l1l1l_opy_ (u"࠭࠮ࡱࡣࡦࠫጱ")):
            proxies = bstack1111l1l1l_opy_(proxy, bstack111lll111l_opy_)
        else:
            proxies = {
                bstack11l1l1l_opy_ (u"ࠧࡩࡶࡷࡴࡸ࠭ጲ"): proxy
            }
    return proxies
def bstack1111l1l1l_opy_(bstack111ll1llll_opy_, bstack111lll111l_opy_):
    proxies = {}
    global bstack111lll1l11_opy_
    if bstack11l1l1l_opy_ (u"ࠨࡒࡄࡇࡤࡖࡒࡐ࡚࡜ࠫጳ") in globals():
        return bstack111lll1l11_opy_
    try:
        proxy = bstack111lll1111_opy_(bstack111ll1llll_opy_, bstack111lll111l_opy_)
        if bstack11l1l1l_opy_ (u"ࠤࡇࡍࡗࡋࡃࡕࠤጴ") in proxy:
            proxies = {}
        elif bstack11l1l1l_opy_ (u"ࠥࡌ࡙࡚ࡐࠣጵ") in proxy or bstack11l1l1l_opy_ (u"ࠦࡍ࡚ࡔࡑࡕࠥጶ") in proxy or bstack11l1l1l_opy_ (u"࡙ࠧࡏࡄࡍࡖࠦጷ") in proxy:
            bstack111lll11ll_opy_ = proxy.split(bstack11l1l1l_opy_ (u"ࠨࠠࠣጸ"))
            if bstack11l1l1l_opy_ (u"ࠢ࠻࠱࠲ࠦጹ") in bstack11l1l1l_opy_ (u"ࠣࠤጺ").join(bstack111lll11ll_opy_[1:]):
                proxies = {
                    bstack11l1l1l_opy_ (u"ࠩ࡫ࡸࡹࡶࡳࠨጻ"): bstack11l1l1l_opy_ (u"ࠥࠦጼ").join(bstack111lll11ll_opy_[1:])
                }
            else:
                proxies = {
                    bstack11l1l1l_opy_ (u"ࠫ࡭ࡺࡴࡱࡵࠪጽ"): str(bstack111lll11ll_opy_[0]).lower() + bstack11l1l1l_opy_ (u"ࠧࡀ࠯࠰ࠤጾ") + bstack11l1l1l_opy_ (u"ࠨࠢጿ").join(bstack111lll11ll_opy_[1:])
                }
        elif bstack11l1l1l_opy_ (u"ࠢࡑࡔࡒ࡜࡞ࠨፀ") in proxy:
            bstack111lll11ll_opy_ = proxy.split(bstack11l1l1l_opy_ (u"ࠣࠢࠥፁ"))
            if bstack11l1l1l_opy_ (u"ࠤ࠽࠳࠴ࠨፂ") in bstack11l1l1l_opy_ (u"ࠥࠦፃ").join(bstack111lll11ll_opy_[1:]):
                proxies = {
                    bstack11l1l1l_opy_ (u"ࠫ࡭ࡺࡴࡱࡵࠪፄ"): bstack11l1l1l_opy_ (u"ࠧࠨፅ").join(bstack111lll11ll_opy_[1:])
                }
            else:
                proxies = {
                    bstack11l1l1l_opy_ (u"࠭ࡨࡵࡶࡳࡷࠬፆ"): bstack11l1l1l_opy_ (u"ࠢࡩࡶࡷࡴ࠿࠵࠯ࠣፇ") + bstack11l1l1l_opy_ (u"ࠣࠤፈ").join(bstack111lll11ll_opy_[1:])
                }
        else:
            proxies = {
                bstack11l1l1l_opy_ (u"ࠩ࡫ࡸࡹࡶࡳࠨፉ"): proxy
            }
    except Exception as e:
        print(bstack11l1l1l_opy_ (u"ࠥࡷࡴࡳࡥࠡࡧࡵࡶࡴࡸࠢፊ"), bstack11l1l1l1ll_opy_.format(bstack111ll1llll_opy_, str(e)))
    bstack111lll1l11_opy_ = proxies
    return proxies