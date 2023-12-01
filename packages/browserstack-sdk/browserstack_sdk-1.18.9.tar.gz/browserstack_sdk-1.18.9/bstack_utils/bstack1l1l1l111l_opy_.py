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
from uuid import uuid4
from bstack_utils.helper import bstack1ll11111ll_opy_, bstack11ll11111l_opy_
from bstack_utils.bstack11ll1ll1_opy_ import bstack111ll1l111_opy_
class bstack1l11llllll_opy_:
    def __init__(self, name=None, code=None, uuid=None, file_path=None, bstack1l1l1l11l1_opy_=None, framework=None, tags=[], scope=[], bstack1111lll1l1_opy_=None, bstack1111llll11_opy_=True, bstack1111lllll1_opy_=None, bstack1l1lll1l1l_opy_=None, result=None, duration=None, bstack1l11l1ll11_opy_=None, meta={}):
        self.bstack1l11l1ll11_opy_ = bstack1l11l1ll11_opy_
        self.name = name
        self.code = code
        self.file_path = file_path
        self.uuid = uuid
        if not self.uuid and bstack1111llll11_opy_:
            self.uuid = uuid4().__str__()
        self.bstack1l1l1l11l1_opy_ = bstack1l1l1l11l1_opy_
        self.framework = framework
        self.tags = tags
        self.scope = scope
        self.bstack1111lll1l1_opy_ = bstack1111lll1l1_opy_
        self.bstack1111lllll1_opy_ = bstack1111lllll1_opy_
        self.bstack1l1lll1l1l_opy_ = bstack1l1lll1l1l_opy_
        self.result = result
        self.duration = duration
        self.meta = meta
    def bstack1l11lllll1_opy_(self):
        if self.uuid:
            return self.uuid
        self.uuid = uuid4().__str__()
        return self.uuid
    def bstack111l111l1l_opy_(self):
        bstack111l1111l1_opy_ = os.path.relpath(self.file_path, start=os.getcwd())
        return {
            bstack11l1ll_opy_ (u"ࠬ࡬ࡩ࡭ࡧࡢࡲࡦࡳࡥࠨᎠ"): bstack111l1111l1_opy_,
            bstack11l1ll_opy_ (u"࠭࡬ࡰࡥࡤࡸ࡮ࡵ࡮ࠨᎡ"): bstack111l1111l1_opy_,
            bstack11l1ll_opy_ (u"ࠧࡷࡥࡢࡪ࡮ࡲࡥࡱࡣࡷ࡬ࠬᎢ"): bstack111l1111l1_opy_
        }
    def set(self, **kwargs):
        for key, val in kwargs.items():
            if not hasattr(self, key):
                raise TypeError(bstack11l1ll_opy_ (u"ࠣࡗࡱࡩࡽࡶࡥࡤࡶࡨࡨࠥࡧࡲࡨࡷࡰࡩࡳࡺ࠺ࠡࠤᎣ") + key)
            setattr(self, key, val)
    def bstack111l111l11_opy_(self):
        return {
            bstack11l1ll_opy_ (u"ࠩࡱࡥࡲ࡫ࠧᎤ"): self.name,
            bstack11l1ll_opy_ (u"ࠪࡦࡴࡪࡹࠨᎥ"): {
                bstack11l1ll_opy_ (u"ࠫࡱࡧ࡮ࡨࠩᎦ"): bstack11l1ll_opy_ (u"ࠬࡶࡹࡵࡪࡲࡲࠬᎧ"),
                bstack11l1ll_opy_ (u"࠭ࡣࡰࡦࡨࠫᎨ"): self.code
            },
            bstack11l1ll_opy_ (u"ࠧࡴࡥࡲࡴࡪࡹࠧᎩ"): self.scope,
            bstack11l1ll_opy_ (u"ࠨࡶࡤ࡫ࡸ࠭Ꭺ"): self.tags,
            bstack11l1ll_opy_ (u"ࠩࡩࡶࡦࡳࡥࡸࡱࡵ࡯ࠬᎫ"): self.framework,
            bstack11l1ll_opy_ (u"ࠪࡷࡹࡧࡲࡵࡧࡧࡣࡦࡺࠧᎬ"): self.bstack1l1l1l11l1_opy_
        }
    def bstack1111lll1ll_opy_(self):
        return {
         bstack11l1ll_opy_ (u"ࠫࡲ࡫ࡴࡢࠩᎭ"): self.meta
        }
    def bstack111l11l111_opy_(self):
        return {
            bstack11l1ll_opy_ (u"ࠬࡩࡵࡴࡶࡲࡱࡗ࡫ࡲࡶࡰࡓࡥࡷࡧ࡭ࠨᎮ"): {
                bstack11l1ll_opy_ (u"࠭ࡲࡦࡴࡸࡲࡤࡴࡡ࡮ࡧࠪᎯ"): self.bstack1111lll1l1_opy_
            }
        }
    def bstack111l11111l_opy_(self, bstack111l111ll1_opy_, details):
        step = next(filter(lambda st: st[bstack11l1ll_opy_ (u"ࠧࡪࡦࠪᎰ")] == bstack111l111ll1_opy_, self.meta[bstack11l1ll_opy_ (u"ࠨࡵࡷࡩࡵࡹࠧᎱ")]), None)
        step.update(details)
    def bstack1111llllll_opy_(self, bstack111l111ll1_opy_):
        step = next(filter(lambda st: st[bstack11l1ll_opy_ (u"ࠩ࡬ࡨࠬᎲ")] == bstack111l111ll1_opy_, self.meta[bstack11l1ll_opy_ (u"ࠪࡷࡹ࡫ࡰࡴࠩᎳ")]), None)
        step.update({
            bstack11l1ll_opy_ (u"ࠫࡸࡺࡡࡳࡶࡨࡨࡤࡧࡴࠨᎴ"): bstack1ll11111ll_opy_()
        })
    def bstack1l11l11l1l_opy_(self, bstack111l111ll1_opy_, result, duration=None):
        bstack1111lllll1_opy_ = bstack1ll11111ll_opy_()
        if self.meta.get(bstack11l1ll_opy_ (u"ࠬࡹࡴࡦࡲࡶࠫᎵ")):
            step = next(filter(lambda st: st[bstack11l1ll_opy_ (u"࠭ࡩࡥࠩᎶ")] == bstack111l111ll1_opy_, self.meta[bstack11l1ll_opy_ (u"ࠧࡴࡶࡨࡴࡸ࠭Ꮇ")]), None)
            step.update({
                bstack11l1ll_opy_ (u"ࠨࡨ࡬ࡲ࡮ࡹࡨࡦࡦࡢࡥࡹ࠭Ꮈ"): bstack1111lllll1_opy_,
                bstack11l1ll_opy_ (u"ࠩࡧࡹࡷࡧࡴࡪࡱࡱࠫᎹ"): duration if duration else bstack11ll11111l_opy_(step[bstack11l1ll_opy_ (u"ࠪࡷࡹࡧࡲࡵࡧࡧࡣࡦࡺࠧᎺ")], bstack1111lllll1_opy_),
                bstack11l1ll_opy_ (u"ࠫࡷ࡫ࡳࡶ࡮ࡷࠫᎻ"): result.result,
                bstack11l1ll_opy_ (u"ࠬ࡬ࡡࡪ࡮ࡸࡶࡪ࠭Ꮌ"): str(result.exception) if result.exception else None
            })
    def add_step(self, bstack1111lll11l_opy_):
        if self.meta.get(bstack11l1ll_opy_ (u"࠭ࡳࡵࡧࡳࡷࠬᎽ")):
            self.meta[bstack11l1ll_opy_ (u"ࠧࡴࡶࡨࡴࡸ࠭Ꮎ")].append(bstack1111lll11l_opy_)
        else:
            self.meta[bstack11l1ll_opy_ (u"ࠨࡵࡷࡩࡵࡹࠧᎿ")] = [ bstack1111lll11l_opy_ ]
    def bstack111l1111ll_opy_(self):
        return {
            bstack11l1ll_opy_ (u"ࠩࡸࡹ࡮ࡪࠧᏀ"): self.bstack1l11lllll1_opy_(),
            **self.bstack111l111l11_opy_(),
            **self.bstack111l111l1l_opy_(),
            **self.bstack1111lll1ll_opy_()
        }
    def bstack1111ll1lll_opy_(self):
        if not self.result:
            return {}
        data = {
            bstack11l1ll_opy_ (u"ࠪࡪ࡮ࡴࡩࡴࡪࡨࡨࡤࡧࡴࠨᏁ"): self.bstack1111lllll1_opy_,
            bstack11l1ll_opy_ (u"ࠫࡩࡻࡲࡢࡶ࡬ࡳࡳࡥࡩ࡯ࡡࡰࡷࠬᏂ"): self.duration,
            bstack11l1ll_opy_ (u"ࠬࡸࡥࡴࡷ࡯ࡸࠬᏃ"): self.result.result
        }
        if data[bstack11l1ll_opy_ (u"࠭ࡲࡦࡵࡸࡰࡹ࠭Ꮔ")] == bstack11l1ll_opy_ (u"ࠧࡧࡣ࡬ࡰࡪࡪࠧᏅ"):
            data[bstack11l1ll_opy_ (u"ࠨࡨࡤ࡭ࡱࡻࡲࡦࡡࡷࡽࡵ࡫ࠧᏆ")] = self.result.bstack1l111l1l11_opy_()
            data[bstack11l1ll_opy_ (u"ࠩࡩࡥ࡮ࡲࡵࡳࡧࠪᏇ")] = [{bstack11l1ll_opy_ (u"ࠪࡦࡦࡩ࡫ࡵࡴࡤࡧࡪ࠭Ꮘ"): self.result.bstack11lll11lll_opy_()}]
        return data
    def bstack111l111111_opy_(self):
        return {
            bstack11l1ll_opy_ (u"ࠫࡺࡻࡩࡥࠩᏉ"): self.bstack1l11lllll1_opy_(),
            **self.bstack111l111l11_opy_(),
            **self.bstack111l111l1l_opy_(),
            **self.bstack1111ll1lll_opy_(),
            **self.bstack1111lll1ll_opy_()
        }
    def bstack1l11llll11_opy_(self, event, result=None):
        if result:
            self.result = result
        if bstack11l1ll_opy_ (u"࡙ࠬࡴࡢࡴࡷࡩࡩ࠭Ꮚ") in event:
            return self.bstack111l1111ll_opy_()
        elif bstack11l1ll_opy_ (u"࠭ࡆࡪࡰ࡬ࡷ࡭࡫ࡤࠨᏋ") in event:
            return self.bstack111l111111_opy_()
    def bstack1l11l1llll_opy_(self):
        pass
    def stop(self, time=None, duration=None, result=None):
        self.bstack1111lllll1_opy_ = time if time else bstack1ll11111ll_opy_()
        self.duration = duration if duration else bstack11ll11111l_opy_(self.bstack1l1l1l11l1_opy_, self.bstack1111lllll1_opy_)
        if result:
            self.result = result
class bstack1l1l111ll1_opy_(bstack1l11llllll_opy_):
    def __init__(self, hooks=[], bstack1l11l1l1l1_opy_={}, *args, **kwargs):
        self.hooks = hooks
        self.bstack1l11l1l1l1_opy_ = bstack1l11l1l1l1_opy_
        super().__init__(*args, **kwargs, bstack1l1lll1l1l_opy_=bstack11l1ll_opy_ (u"ࠧࡵࡧࡶࡸࠬᏌ"))
    @classmethod
    def bstack1111lll111_opy_(cls, scenario, feature, test, **kwargs):
        steps = []
        for step in scenario.steps:
            steps.append({
                bstack11l1ll_opy_ (u"ࠨ࡫ࡧࠫᏍ"): id(step),
                bstack11l1ll_opy_ (u"ࠩࡷࡩࡽࡺࠧᏎ"): step.name,
                bstack11l1ll_opy_ (u"ࠪ࡯ࡪࡿࡷࡰࡴࡧࠫᏏ"): step.keyword,
            })
        return bstack1l1l111ll1_opy_(
            **kwargs,
            meta={
                bstack11l1ll_opy_ (u"ࠫ࡫࡫ࡡࡵࡷࡵࡩࠬᏐ"): {
                    bstack11l1ll_opy_ (u"ࠬࡴࡡ࡮ࡧࠪᏑ"): feature.name,
                    bstack11l1ll_opy_ (u"࠭ࡰࡢࡶ࡫ࠫᏒ"): feature.filename,
                    bstack11l1ll_opy_ (u"ࠧࡥࡧࡶࡧࡷ࡯ࡰࡵ࡫ࡲࡲࠬᏓ"): feature.description
                },
                bstack11l1ll_opy_ (u"ࠨࡵࡦࡩࡳࡧࡲࡪࡱࠪᏔ"): {
                    bstack11l1ll_opy_ (u"ࠩࡱࡥࡲ࡫ࠧᏕ"): scenario.name
                },
                bstack11l1ll_opy_ (u"ࠪࡷࡹ࡫ࡰࡴࠩᏖ"): steps,
                bstack11l1ll_opy_ (u"ࠫࡪࡾࡡ࡮ࡲ࡯ࡩࡸ࠭Ꮧ"): bstack111ll1l111_opy_(test)
            }
        )
    def bstack1111llll1l_opy_(self):
        return {
            bstack11l1ll_opy_ (u"ࠬ࡮࡯ࡰ࡭ࡶࠫᏘ"): self.hooks
        }
    def bstack111l111lll_opy_(self):
        if self.bstack1l11l1l1l1_opy_:
            return {
                bstack11l1ll_opy_ (u"࠭ࡩ࡯ࡶࡨ࡫ࡷࡧࡴࡪࡱࡱࡷࠬᏙ"): self.bstack1l11l1l1l1_opy_
            }
        return {}
    def bstack111l111111_opy_(self):
        return {
            **super().bstack111l111111_opy_(),
            **self.bstack1111llll1l_opy_()
        }
    def bstack111l1111ll_opy_(self):
        return {
            **super().bstack111l1111ll_opy_(),
            **self.bstack111l111lll_opy_()
        }
    def bstack1l11l1llll_opy_(self):
        return bstack11l1ll_opy_ (u"ࠧࡵࡧࡶࡸࡤࡸࡵ࡯ࠩᏚ")
class bstack1l11ll1ll1_opy_(bstack1l11llllll_opy_):
    def __init__(self, hook_type, *args, **kwargs):
        self.hook_type = hook_type
        super().__init__(*args, **kwargs, bstack1l1lll1l1l_opy_=bstack11l1ll_opy_ (u"ࠨࡪࡲࡳࡰ࠭Ꮫ"))
    def bstack1l1l1111ll_opy_(self):
        return self.hook_type
    def bstack1111ll1ll1_opy_(self):
        return {
            bstack11l1ll_opy_ (u"ࠩ࡫ࡳࡴࡱ࡟ࡵࡻࡳࡩࠬᏜ"): self.hook_type
        }
    def bstack111l111111_opy_(self):
        return {
            **super().bstack111l111111_opy_(),
            **self.bstack1111ll1ll1_opy_()
        }
    def bstack111l1111ll_opy_(self):
        return {
            **super().bstack111l1111ll_opy_(),
            **self.bstack1111ll1ll1_opy_()
        }
    def bstack1l11l1llll_opy_(self):
        return bstack11l1ll_opy_ (u"ࠪ࡬ࡴࡵ࡫ࡠࡴࡸࡲࠬᏝ")