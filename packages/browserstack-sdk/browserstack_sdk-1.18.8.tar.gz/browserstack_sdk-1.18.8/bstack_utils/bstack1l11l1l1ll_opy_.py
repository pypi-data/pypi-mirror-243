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
from uuid import uuid4
from bstack_utils.helper import bstack1llllll11l_opy_, bstack11ll1ll1l1_opy_
from bstack_utils.bstack11l111ll_opy_ import bstack111ll1ll1l_opy_
class bstack1l1l111111_opy_:
    def __init__(self, name=None, code=None, uuid=None, file_path=None, bstack1l1l1l1ll1_opy_=None, framework=None, tags=[], scope=[], bstack111l111l11_opy_=None, bstack111l1111l1_opy_=True, bstack111l11l1l1_opy_=None, bstack1llll1111l_opy_=None, result=None, duration=None, bstack1l1l1ll11l_opy_=None, meta={}):
        self.bstack1l1l1ll11l_opy_ = bstack1l1l1ll11l_opy_
        self.name = name
        self.code = code
        self.file_path = file_path
        self.uuid = uuid
        if not self.uuid and bstack111l1111l1_opy_:
            self.uuid = uuid4().__str__()
        self.bstack1l1l1l1ll1_opy_ = bstack1l1l1l1ll1_opy_
        self.framework = framework
        self.tags = tags
        self.scope = scope
        self.bstack111l111l11_opy_ = bstack111l111l11_opy_
        self.bstack111l11l1l1_opy_ = bstack111l11l1l1_opy_
        self.bstack1llll1111l_opy_ = bstack1llll1111l_opy_
        self.result = result
        self.duration = duration
        self.meta = meta
    def bstack1l1l11l11l_opy_(self):
        if self.uuid:
            return self.uuid
        self.uuid = uuid4().__str__()
        return self.uuid
    def bstack1111llll1l_opy_(self):
        bstack1111lllll1_opy_ = os.path.relpath(self.file_path, start=os.getcwd())
        return {
            bstack11l1l1l_opy_ (u"ࠫ࡫࡯࡬ࡦࡡࡱࡥࡲ࡫ࠧᎦ"): bstack1111lllll1_opy_,
            bstack11l1l1l_opy_ (u"ࠬࡲ࡯ࡤࡣࡷ࡭ࡴࡴࠧᎧ"): bstack1111lllll1_opy_,
            bstack11l1l1l_opy_ (u"࠭ࡶࡤࡡࡩ࡭ࡱ࡫ࡰࡢࡶ࡫ࠫᎨ"): bstack1111lllll1_opy_
        }
    def set(self, **kwargs):
        for key, val in kwargs.items():
            if not hasattr(self, key):
                raise TypeError(bstack11l1l1l_opy_ (u"ࠢࡖࡰࡨࡼࡵ࡫ࡣࡵࡧࡧࠤࡦࡸࡧࡶ࡯ࡨࡲࡹࡀࠠࠣᎩ") + key)
            setattr(self, key, val)
    def bstack111l11l111_opy_(self):
        return {
            bstack11l1l1l_opy_ (u"ࠨࡰࡤࡱࡪ࠭Ꭺ"): self.name,
            bstack11l1l1l_opy_ (u"ࠩࡥࡳࡩࡿࠧᎫ"): {
                bstack11l1l1l_opy_ (u"ࠪࡰࡦࡴࡧࠨᎬ"): bstack11l1l1l_opy_ (u"ࠫࡵࡿࡴࡩࡱࡱࠫᎭ"),
                bstack11l1l1l_opy_ (u"ࠬࡩ࡯ࡥࡧࠪᎮ"): self.code
            },
            bstack11l1l1l_opy_ (u"࠭ࡳࡤࡱࡳࡩࡸ࠭Ꭿ"): self.scope,
            bstack11l1l1l_opy_ (u"ࠧࡵࡣࡪࡷࠬᎰ"): self.tags,
            bstack11l1l1l_opy_ (u"ࠨࡨࡵࡥࡲ࡫ࡷࡰࡴ࡮ࠫᎱ"): self.framework,
            bstack11l1l1l_opy_ (u"ࠩࡶࡸࡦࡸࡴࡦࡦࡢࡥࡹ࠭Ꮂ"): self.bstack1l1l1l1ll1_opy_
        }
    def bstack1111llll11_opy_(self):
        return {
         bstack11l1l1l_opy_ (u"ࠪࡱࡪࡺࡡࠨᎳ"): self.meta
        }
    def bstack111l11l11l_opy_(self):
        return {
            bstack11l1l1l_opy_ (u"ࠫࡨࡻࡳࡵࡱࡰࡖࡪࡸࡵ࡯ࡒࡤࡶࡦࡳࠧᎴ"): {
                bstack11l1l1l_opy_ (u"ࠬࡸࡥࡳࡷࡱࡣࡳࡧ࡭ࡦࠩᎵ"): self.bstack111l111l11_opy_
            }
        }
    def bstack111l111111_opy_(self, bstack111l11111l_opy_, details):
        step = next(filter(lambda st: st[bstack11l1l1l_opy_ (u"࠭ࡩࡥࠩᎶ")] == bstack111l11111l_opy_, self.meta[bstack11l1l1l_opy_ (u"ࠧࡴࡶࡨࡴࡸ࠭Ꮇ")]), None)
        step.update(details)
    def bstack111l111lll_opy_(self, bstack111l11111l_opy_):
        step = next(filter(lambda st: st[bstack11l1l1l_opy_ (u"ࠨ࡫ࡧࠫᎸ")] == bstack111l11111l_opy_, self.meta[bstack11l1l1l_opy_ (u"ࠩࡶࡸࡪࡶࡳࠨᎹ")]), None)
        step.update({
            bstack11l1l1l_opy_ (u"ࠪࡷࡹࡧࡲࡵࡧࡧࡣࡦࡺࠧᎺ"): bstack1llllll11l_opy_()
        })
    def bstack1l1l111l11_opy_(self, bstack111l11111l_opy_, result, duration=None):
        bstack111l11l1l1_opy_ = bstack1llllll11l_opy_()
        if self.meta.get(bstack11l1l1l_opy_ (u"ࠫࡸࡺࡥࡱࡵࠪᎻ")):
            step = next(filter(lambda st: st[bstack11l1l1l_opy_ (u"ࠬ࡯ࡤࠨᎼ")] == bstack111l11111l_opy_, self.meta[bstack11l1l1l_opy_ (u"࠭ࡳࡵࡧࡳࡷࠬᎽ")]), None)
            step.update({
                bstack11l1l1l_opy_ (u"ࠧࡧ࡫ࡱ࡭ࡸ࡮ࡥࡥࡡࡤࡸࠬᎾ"): bstack111l11l1l1_opy_,
                bstack11l1l1l_opy_ (u"ࠨࡦࡸࡶࡦࡺࡩࡰࡰࠪᎿ"): duration if duration else bstack11ll1ll1l1_opy_(step[bstack11l1l1l_opy_ (u"ࠩࡶࡸࡦࡸࡴࡦࡦࡢࡥࡹ࠭Ꮐ")], bstack111l11l1l1_opy_),
                bstack11l1l1l_opy_ (u"ࠪࡶࡪࡹࡵ࡭ࡶࠪᏁ"): result.result,
                bstack11l1l1l_opy_ (u"ࠫ࡫ࡧࡩ࡭ࡷࡵࡩࠬᏂ"): str(result.exception) if result.exception else None
            })
    def add_step(self, bstack1111llllll_opy_):
        if self.meta.get(bstack11l1l1l_opy_ (u"ࠬࡹࡴࡦࡲࡶࠫᏃ")):
            self.meta[bstack11l1l1l_opy_ (u"࠭ࡳࡵࡧࡳࡷࠬᏄ")].append(bstack1111llllll_opy_)
        else:
            self.meta[bstack11l1l1l_opy_ (u"ࠧࡴࡶࡨࡴࡸ࠭Ꮕ")] = [ bstack1111llllll_opy_ ]
    def bstack111l1111ll_opy_(self):
        return {
            bstack11l1l1l_opy_ (u"ࠨࡷࡸ࡭ࡩ࠭Ꮖ"): self.bstack1l1l11l11l_opy_(),
            **self.bstack111l11l111_opy_(),
            **self.bstack1111llll1l_opy_(),
            **self.bstack1111llll11_opy_()
        }
    def bstack1111lll11l_opy_(self):
        if not self.result:
            return {}
        data = {
            bstack11l1l1l_opy_ (u"ࠩࡩ࡭ࡳ࡯ࡳࡩࡧࡧࡣࡦࡺࠧᏇ"): self.bstack111l11l1l1_opy_,
            bstack11l1l1l_opy_ (u"ࠪࡨࡺࡸࡡࡵ࡫ࡲࡲࡤ࡯࡮ࡠ࡯ࡶࠫᏈ"): self.duration,
            bstack11l1l1l_opy_ (u"ࠫࡷ࡫ࡳࡶ࡮ࡷࠫᏉ"): self.result.result
        }
        if data[bstack11l1l1l_opy_ (u"ࠬࡸࡥࡴࡷ࡯ࡸࠬᏊ")] == bstack11l1l1l_opy_ (u"࠭ࡦࡢ࡫࡯ࡩࡩ࠭Ꮛ"):
            data[bstack11l1l1l_opy_ (u"ࠧࡧࡣ࡬ࡰࡺࡸࡥࡠࡶࡼࡴࡪ࠭Ꮜ")] = self.result.bstack1l111ll11l_opy_()
            data[bstack11l1l1l_opy_ (u"ࠨࡨࡤ࡭ࡱࡻࡲࡦࠩᏍ")] = [{bstack11l1l1l_opy_ (u"ࠩࡥࡥࡨࡱࡴࡳࡣࡦࡩࠬᏎ"): self.result.bstack11ll11llll_opy_()}]
        return data
    def bstack111l11l1ll_opy_(self):
        return {
            bstack11l1l1l_opy_ (u"ࠪࡹࡺ࡯ࡤࠨᏏ"): self.bstack1l1l11l11l_opy_(),
            **self.bstack111l11l111_opy_(),
            **self.bstack1111llll1l_opy_(),
            **self.bstack1111lll11l_opy_(),
            **self.bstack1111llll11_opy_()
        }
    def bstack1l1l11llll_opy_(self, event, result=None):
        if result:
            self.result = result
        if bstack11l1l1l_opy_ (u"ࠫࡘࡺࡡࡳࡶࡨࡨࠬᏐ") in event:
            return self.bstack111l1111ll_opy_()
        elif bstack11l1l1l_opy_ (u"ࠬࡌࡩ࡯࡫ࡶ࡬ࡪࡪࠧᏑ") in event:
            return self.bstack111l11l1ll_opy_()
    def bstack1l11l1l11l_opy_(self):
        pass
    def stop(self, time=None, duration=None, result=None):
        self.bstack111l11l1l1_opy_ = time if time else bstack1llllll11l_opy_()
        self.duration = duration if duration else bstack11ll1ll1l1_opy_(self.bstack1l1l1l1ll1_opy_, self.bstack111l11l1l1_opy_)
        if result:
            self.result = result
class bstack1l1l1llll1_opy_(bstack1l1l111111_opy_):
    def __init__(self, hooks=[], bstack1l11lllll1_opy_={}, *args, **kwargs):
        self.hooks = hooks
        self.bstack1l11lllll1_opy_ = bstack1l11lllll1_opy_
        super().__init__(*args, **kwargs, bstack1llll1111l_opy_=bstack11l1l1l_opy_ (u"࠭ࡴࡦࡵࡷࠫᏒ"))
    @classmethod
    def bstack111l111ll1_opy_(cls, scenario, feature, test, **kwargs):
        steps = []
        for step in scenario.steps:
            steps.append({
                bstack11l1l1l_opy_ (u"ࠧࡪࡦࠪᏓ"): id(step),
                bstack11l1l1l_opy_ (u"ࠨࡶࡨࡼࡹ࠭Ꮤ"): step.name,
                bstack11l1l1l_opy_ (u"ࠩ࡮ࡩࡾࡽ࡯ࡳࡦࠪᏕ"): step.keyword,
            })
        return bstack1l1l1llll1_opy_(
            **kwargs,
            meta={
                bstack11l1l1l_opy_ (u"ࠪࡪࡪࡧࡴࡶࡴࡨࠫᏖ"): {
                    bstack11l1l1l_opy_ (u"ࠫࡳࡧ࡭ࡦࠩᏗ"): feature.name,
                    bstack11l1l1l_opy_ (u"ࠬࡶࡡࡵࡪࠪᏘ"): feature.filename,
                    bstack11l1l1l_opy_ (u"࠭ࡤࡦࡵࡦࡶ࡮ࡶࡴࡪࡱࡱࠫᏙ"): feature.description
                },
                bstack11l1l1l_opy_ (u"ࠧࡴࡥࡨࡲࡦࡸࡩࡰࠩᏚ"): {
                    bstack11l1l1l_opy_ (u"ࠨࡰࡤࡱࡪ࠭Ꮫ"): scenario.name
                },
                bstack11l1l1l_opy_ (u"ࠩࡶࡸࡪࡶࡳࠨᏜ"): steps,
                bstack11l1l1l_opy_ (u"ࠪࡩࡽࡧ࡭ࡱ࡮ࡨࡷࠬᏝ"): bstack111ll1ll1l_opy_(test)
            }
        )
    def bstack1111lll1l1_opy_(self):
        return {
            bstack11l1l1l_opy_ (u"ࠫ࡭ࡵ࡯࡬ࡵࠪᏞ"): self.hooks
        }
    def bstack111l111l1l_opy_(self):
        if self.bstack1l11lllll1_opy_:
            return {
                bstack11l1l1l_opy_ (u"ࠬ࡯࡮ࡵࡧࡪࡶࡦࡺࡩࡰࡰࡶࠫᏟ"): self.bstack1l11lllll1_opy_
            }
        return {}
    def bstack111l11l1ll_opy_(self):
        return {
            **super().bstack111l11l1ll_opy_(),
            **self.bstack1111lll1l1_opy_()
        }
    def bstack111l1111ll_opy_(self):
        return {
            **super().bstack111l1111ll_opy_(),
            **self.bstack111l111l1l_opy_()
        }
    def bstack1l11l1l11l_opy_(self):
        return bstack11l1l1l_opy_ (u"࠭ࡴࡦࡵࡷࡣࡷࡻ࡮ࠨᏠ")
class bstack1l11ll1l11_opy_(bstack1l1l111111_opy_):
    def __init__(self, hook_type, *args, **kwargs):
        self.hook_type = hook_type
        super().__init__(*args, **kwargs, bstack1llll1111l_opy_=bstack11l1l1l_opy_ (u"ࠧࡩࡱࡲ࡯ࠬᏡ"))
    def bstack1l1l11ll1l_opy_(self):
        return self.hook_type
    def bstack1111lll1ll_opy_(self):
        return {
            bstack11l1l1l_opy_ (u"ࠨࡪࡲࡳࡰࡥࡴࡺࡲࡨࠫᏢ"): self.hook_type
        }
    def bstack111l11l1ll_opy_(self):
        return {
            **super().bstack111l11l1ll_opy_(),
            **self.bstack1111lll1ll_opy_()
        }
    def bstack111l1111ll_opy_(self):
        return {
            **super().bstack111l1111ll_opy_(),
            **self.bstack1111lll1ll_opy_()
        }
    def bstack1l11l1l11l_opy_(self):
        return bstack11l1l1l_opy_ (u"ࠩ࡫ࡳࡴࡱ࡟ࡳࡷࡱࠫᏣ")