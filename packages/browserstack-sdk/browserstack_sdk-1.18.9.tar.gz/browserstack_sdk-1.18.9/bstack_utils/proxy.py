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
from urllib.parse import urlparse
from bstack_utils.messages import bstack11l1l1l111_opy_
def bstack111ll1l1ll_opy_(url):
    try:
        result = urlparse(url)
        return all([result.scheme, result.netloc])
    except:
        return False
def bstack111ll1lll1_opy_(bstack111ll1ll11_opy_, bstack111lll1111_opy_):
    from pypac import get_pac
    from pypac import PACSession
    from pypac.parser import PACFile
    import socket
    if os.path.isfile(bstack111ll1ll11_opy_):
        with open(bstack111ll1ll11_opy_) as f:
            pac = PACFile(f.read())
    elif bstack111ll1l1ll_opy_(bstack111ll1ll11_opy_):
        pac = get_pac(url=bstack111ll1ll11_opy_)
    else:
        raise Exception(bstack11l1ll_opy_ (u"ࠬࡖࡡࡤࠢࡩ࡭ࡱ࡫ࠠࡥࡱࡨࡷࠥࡴ࡯ࡵࠢࡨࡼ࡮ࡹࡴ࠻ࠢࡾࢁࠬጔ").format(bstack111ll1ll11_opy_))
    session = PACSession(pac)
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect((bstack11l1ll_opy_ (u"ࠨ࠸࠯࠺࠱࠼࠳࠾ࠢጕ"), 80))
        bstack111ll1ll1l_opy_ = s.getsockname()[0]
        s.close()
    except:
        bstack111ll1ll1l_opy_ = bstack11l1ll_opy_ (u"ࠧ࠱࠰࠳࠲࠵࠴࠰ࠨ጖")
    proxy_url = session.get_pac().find_proxy_for_url(bstack111lll1111_opy_, bstack111ll1ll1l_opy_)
    return proxy_url
def bstack11111llll_opy_(config):
    return bstack11l1ll_opy_ (u"ࠨࡪࡷࡸࡵࡖࡲࡰࡺࡼࠫ጗") in config or bstack11l1ll_opy_ (u"ࠩ࡫ࡸࡹࡶࡳࡑࡴࡲࡼࡾ࠭ጘ") in config
def bstack1l111lll1_opy_(config):
    if not bstack11111llll_opy_(config):
        return
    if config.get(bstack11l1ll_opy_ (u"ࠪ࡬ࡹࡺࡰࡑࡴࡲࡼࡾ࠭ጙ")):
        return config.get(bstack11l1ll_opy_ (u"ࠫ࡭ࡺࡴࡱࡒࡵࡳࡽࡿࠧጚ"))
    if config.get(bstack11l1ll_opy_ (u"ࠬ࡮ࡴࡵࡲࡶࡔࡷࡵࡸࡺࠩጛ")):
        return config.get(bstack11l1ll_opy_ (u"࠭ࡨࡵࡶࡳࡷࡕࡸ࡯ࡹࡻࠪጜ"))
def bstack1lll111111_opy_(config, bstack111lll1111_opy_):
    proxy = bstack1l111lll1_opy_(config)
    proxies = {}
    if config.get(bstack11l1ll_opy_ (u"ࠧࡩࡶࡷࡴࡕࡸ࡯ࡹࡻࠪጝ")) or config.get(bstack11l1ll_opy_ (u"ࠨࡪࡷࡸࡵࡹࡐࡳࡱࡻࡽࠬጞ")):
        if proxy.endswith(bstack11l1ll_opy_ (u"ࠩ࠱ࡴࡦࡩࠧጟ")):
            proxies = bstack111l1ll11_opy_(proxy, bstack111lll1111_opy_)
        else:
            proxies = {
                bstack11l1ll_opy_ (u"ࠪ࡬ࡹࡺࡰࡴࠩጠ"): proxy
            }
    return proxies
def bstack111l1ll11_opy_(bstack111ll1ll11_opy_, bstack111lll1111_opy_):
    proxies = {}
    global bstack111ll1llll_opy_
    if bstack11l1ll_opy_ (u"ࠫࡕࡇࡃࡠࡒࡕࡓ࡝࡟ࠧጡ") in globals():
        return bstack111ll1llll_opy_
    try:
        proxy = bstack111ll1lll1_opy_(bstack111ll1ll11_opy_, bstack111lll1111_opy_)
        if bstack11l1ll_opy_ (u"ࠧࡊࡉࡓࡇࡆࡘࠧጢ") in proxy:
            proxies = {}
        elif bstack11l1ll_opy_ (u"ࠨࡈࡕࡖࡓࠦጣ") in proxy or bstack11l1ll_opy_ (u"ࠢࡉࡖࡗࡔࡘࠨጤ") in proxy or bstack11l1ll_opy_ (u"ࠣࡕࡒࡇࡐ࡙ࠢጥ") in proxy:
            bstack111lll111l_opy_ = proxy.split(bstack11l1ll_opy_ (u"ࠤࠣࠦጦ"))
            if bstack11l1ll_opy_ (u"ࠥ࠾࠴࠵ࠢጧ") in bstack11l1ll_opy_ (u"ࠦࠧጨ").join(bstack111lll111l_opy_[1:]):
                proxies = {
                    bstack11l1ll_opy_ (u"ࠬ࡮ࡴࡵࡲࡶࠫጩ"): bstack11l1ll_opy_ (u"ࠨࠢጪ").join(bstack111lll111l_opy_[1:])
                }
            else:
                proxies = {
                    bstack11l1ll_opy_ (u"ࠧࡩࡶࡷࡴࡸ࠭ጫ"): str(bstack111lll111l_opy_[0]).lower() + bstack11l1ll_opy_ (u"ࠣ࠼࠲࠳ࠧጬ") + bstack11l1ll_opy_ (u"ࠤࠥጭ").join(bstack111lll111l_opy_[1:])
                }
        elif bstack11l1ll_opy_ (u"ࠥࡔࡗࡕࡘ࡚ࠤጮ") in proxy:
            bstack111lll111l_opy_ = proxy.split(bstack11l1ll_opy_ (u"ࠦࠥࠨጯ"))
            if bstack11l1ll_opy_ (u"ࠧࡀ࠯࠰ࠤጰ") in bstack11l1ll_opy_ (u"ࠨࠢጱ").join(bstack111lll111l_opy_[1:]):
                proxies = {
                    bstack11l1ll_opy_ (u"ࠧࡩࡶࡷࡴࡸ࠭ጲ"): bstack11l1ll_opy_ (u"ࠣࠤጳ").join(bstack111lll111l_opy_[1:])
                }
            else:
                proxies = {
                    bstack11l1ll_opy_ (u"ࠩ࡫ࡸࡹࡶࡳࠨጴ"): bstack11l1ll_opy_ (u"ࠥ࡬ࡹࡺࡰ࠻࠱࠲ࠦጵ") + bstack11l1ll_opy_ (u"ࠦࠧጶ").join(bstack111lll111l_opy_[1:])
                }
        else:
            proxies = {
                bstack11l1ll_opy_ (u"ࠬ࡮ࡴࡵࡲࡶࠫጷ"): proxy
            }
    except Exception as e:
        print(bstack11l1ll_opy_ (u"ࠨࡳࡰ࡯ࡨࠤࡪࡸࡲࡰࡴࠥጸ"), bstack11l1l1l111_opy_.format(bstack111ll1ll11_opy_, str(e)))
    bstack111ll1llll_opy_ = proxies
    return proxies