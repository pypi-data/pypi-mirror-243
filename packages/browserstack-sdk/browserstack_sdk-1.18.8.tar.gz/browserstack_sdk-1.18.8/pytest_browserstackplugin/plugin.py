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
import datetime
import inspect
import logging
import os
import sys
import threading
from uuid import uuid4
import tempfile
import pytest
from packaging import version
from browserstack_sdk.__init__ import (bstack1l1ll1llll_opy_, bstack1l1ll1l1ll_opy_, update, bstack1ll11lllll_opy_,
                                       bstack1llllll1l_opy_, bstack1llll1l1l_opy_, bstack1l1l11l1_opy_, bstack1l1l1ll1l_opy_,
                                       bstack11lll1ll1_opy_, bstack1ll1l1ll_opy_, bstack1111l111l_opy_, bstack1ll1llll_opy_,
                                       bstack1ll1ll11l1_opy_, getAccessibilityResults, getAccessibilityResultsSummary)
from browserstack_sdk._version import __version__
from bstack_utils.capture import bstack1l1ll1111l_opy_
from bstack_utils.constants import bstack1l1lll1l_opy_, bstack1llll1l11_opy_, bstack1ll1l11ll1_opy_, bstack1ll1ll11ll_opy_, \
    bstack1ll111llll_opy_
from bstack_utils.helper import bstack1111l11l_opy_, bstack11l111lll_opy_, bstack11lll1l1ll_opy_, bstack1llllll11l_opy_, bstack11ll1111ll_opy_, \
    bstack11ll1lll1l_opy_, bstack1llll1lll_opy_, bstack1llllllll_opy_, bstack11ll11lll1_opy_, bstack11ll1111_opy_, Notset, \
    bstack1ll111l111_opy_, bstack11ll1ll1l1_opy_, bstack11ll1l1l11_opy_, Result, bstack11ll1lll11_opy_, bstack11lll1l11l_opy_, bstack1l11ll1ll1_opy_, bstack1llll1111_opy_, bstack1ll111111_opy_
from bstack_utils.bstack11l1lll1ll_opy_ import bstack11l1ll11ll_opy_
from bstack_utils.messages import bstack1l1l1ll11_opy_, bstack11ll1lll_opy_, bstack1ll11ll1_opy_, bstack111111l11_opy_, bstack1l1l1111l_opy_, \
    bstack1ll11l11ll_opy_, bstack11l1111l1_opy_, bstack1l11l1ll1_opy_, bstack111lll11_opy_, bstack1lll11ll_opy_, \
    bstack11lll11ll_opy_, bstack1lll1111_opy_
from bstack_utils.proxy import bstack1ll1111l_opy_, bstack1111l1l1l_opy_
from bstack_utils.bstack11l111ll_opy_ import bstack111ll1lll1_opy_, bstack111ll11lll_opy_, bstack111ll1ll11_opy_, bstack111ll11ll1_opy_, \
    bstack111ll1l1ll_opy_, bstack111ll111ll_opy_, bstack111ll1l11l_opy_, bstack1lll11l1ll_opy_, bstack111ll11l1l_opy_
from bstack_utils.bstack1lll11111l_opy_ import bstack11lll111l_opy_
from bstack_utils.bstack111ll1l111_opy_ import bstack1l1lll1l1l_opy_, bstack1l1lll1lll_opy_, bstack11l11l11l_opy_
from bstack_utils.bstack1l11l1l1ll_opy_ import bstack1l1l1llll1_opy_
from bstack_utils.bstack1l1ll111_opy_ import bstack1l11l11l_opy_
import bstack_utils.bstack11l1ll111_opy_ as bstack1111ll111_opy_
bstack1l111l1l_opy_ = None
bstack1l1l1l1ll_opy_ = None
bstack1l11111ll_opy_ = None
bstack1ll111l1ll_opy_ = None
bstack1lll11ll1_opy_ = None
bstack1ll1lllll_opy_ = None
bstack11llll11_opy_ = None
bstack1l111lll1_opy_ = None
bstack1l11l1l11_opy_ = None
bstack1lll111l1_opy_ = None
bstack1l1l11l1l_opy_ = None
bstack11ll1l1ll_opy_ = None
bstack1l1111l1_opy_ = None
bstack1lllll1ll1_opy_ = bstack11l1l1l_opy_ (u"ࠬ࠭ᒸ")
CONFIG = {}
bstack1lll1l111_opy_ = False
bstack1l1ll1ll1l_opy_ = bstack11l1l1l_opy_ (u"࠭ࠧᒹ")
bstack11l111111_opy_ = bstack11l1l1l_opy_ (u"ࠧࠨᒺ")
bstack1l1l1l1l1_opy_ = False
bstack11111lll1_opy_ = []
bstack1ll1l11111_opy_ = bstack1llll1l11_opy_
bstack11111l1ll1_opy_ = bstack11l1l1l_opy_ (u"ࠨࡲࡼࡸࡪࡹࡴࠨᒻ")
bstack11111l11l1_opy_ = False
bstack11l11l1l_opy_ = {}
logger = logging.getLogger(__name__)
logging.basicConfig(level=bstack1ll1l11111_opy_,
                    format=bstack11l1l1l_opy_ (u"ࠩ࡟ࡲࠪ࠮ࡡࡴࡥࡷ࡭ࡲ࡫ࠩࡴࠢ࡞ࠩ࠭ࡴࡡ࡮ࡧࠬࡷࡢࡡࠥࠩ࡮ࡨࡺࡪࡲ࡮ࡢ࡯ࡨ࠭ࡸࡣࠠ࠮ࠢࠨࠬࡲ࡫ࡳࡴࡣࡪࡩ࠮ࡹࠧᒼ"),
                    datefmt=bstack11l1l1l_opy_ (u"ࠪࠩࡍࡀࠥࡎ࠼ࠨࡗࠬᒽ"),
                    stream=sys.stdout)
store = {
    bstack11l1l1l_opy_ (u"ࠫࡨࡻࡲࡳࡧࡱࡸࡤ࡮࡯ࡰ࡭ࡢࡹࡺ࡯ࡤࠨᒾ"): []
}
def bstack1111ll1l1_opy_():
    global CONFIG
    global bstack1ll1l11111_opy_
    if bstack11l1l1l_opy_ (u"ࠬࡲ࡯ࡨࡎࡨࡺࡪࡲࠧᒿ") in CONFIG:
        bstack1ll1l11111_opy_ = bstack1l1lll1l_opy_[CONFIG[bstack11l1l1l_opy_ (u"࠭࡬ࡰࡩࡏࡩࡻ࡫࡬ࠨᓀ")]]
        logging.getLogger().setLevel(bstack1ll1l11111_opy_)
try:
    from playwright.sync_api import (
        BrowserContext,
        Page
    )
except:
    pass
import json
_1l1ll11111_opy_ = {}
current_test_uuid = None
def bstack11111111l_opy_(page, bstack1lll11llll_opy_):
    try:
        page.evaluate(bstack11l1l1l_opy_ (u"ࠢࡠࠢࡀࡂࠥࢁࡽࠣᓁ"),
                      bstack11l1l1l_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࡟ࡦࡺࡨࡧࡺࡺ࡯ࡳ࠼ࠣࡿࠧࡧࡣࡵ࡫ࡲࡲࠧࡀࠠࠣࡵࡨࡸࡘ࡫ࡳࡴ࡫ࡲࡲࡓࡧ࡭ࡦࠤ࠯ࠤࠧࡧࡲࡨࡷࡰࡩࡳࡺࡳࠣ࠼ࠣࡿࠧࡴࡡ࡮ࡧࠥ࠾ࠬᓂ") + json.dumps(
                          bstack1lll11llll_opy_) + bstack11l1l1l_opy_ (u"ࠤࢀࢁࠧᓃ"))
    except Exception as e:
        print(bstack11l1l1l_opy_ (u"ࠥࡩࡽࡩࡥࡱࡶ࡬ࡳࡳࠦࡩ࡯ࠢࡳࡰࡦࡿࡷࡳ࡫ࡪ࡬ࡹࠦࡳࡦࡵࡶ࡭ࡴࡴࠠ࡯ࡣࡰࡩࠥࢁࡽࠣᓄ"), e)
def bstack1111l1lll_opy_(page, message, level):
    try:
        page.evaluate(bstack11l1l1l_opy_ (u"ࠦࡤࠦ࠽࠿ࠢࡾࢁࠧᓅ"), bstack11l1l1l_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࡣࡪࡾࡥࡤࡷࡷࡳࡷࡀࠠࡼࠤࡤࡧࡹ࡯࡯࡯ࠤ࠽ࠤࠧࡧ࡮࡯ࡱࡷࡥࡹ࡫ࠢ࠭ࠢࠥࡥࡷ࡭ࡵ࡮ࡧࡱࡸࡸࠨ࠺ࠡࡽࠥࡨࡦࡺࡡࠣ࠼ࠪᓆ") + json.dumps(
            message) + bstack11l1l1l_opy_ (u"࠭ࠬࠣ࡮ࡨࡺࡪࡲࠢ࠻ࠩᓇ") + json.dumps(level) + bstack11l1l1l_opy_ (u"ࠧࡾࡿࠪᓈ"))
    except Exception as e:
        print(bstack11l1l1l_opy_ (u"ࠣࡧࡻࡧࡪࡶࡴࡪࡱࡱࠤ࡮ࡴࠠࡱ࡮ࡤࡽࡼࡸࡩࡨࡪࡷࠤࡦࡴ࡮ࡰࡶࡤࡸ࡮ࡵ࡮ࠡࡽࢀࠦᓉ"), e)
def bstack1l11l1l1l_opy_(page, status, message=bstack11l1l1l_opy_ (u"ࠤࠥᓊ")):
    try:
        if (status == bstack11l1l1l_opy_ (u"ࠥࡪࡦ࡯࡬ࡦࡦࠥᓋ")):
            page.evaluate(bstack11l1l1l_opy_ (u"ࠦࡤࠦ࠽࠿ࠢࡾࢁࠧᓌ"),
                          bstack11l1l1l_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࡣࡪࡾࡥࡤࡷࡷࡳࡷࡀࠠࡼࠤࡤࡧࡹ࡯࡯࡯ࠤ࠽ࠤࠧࡹࡥࡵࡕࡨࡷࡸ࡯࡯࡯ࡕࡷࡥࡹࡻࡳࠣ࠮ࠣࠦࡦࡸࡧࡶ࡯ࡨࡲࡹࡹࠢ࠻ࠢࡾࠦࡷ࡫ࡡࡴࡱࡱࠦ࠿࠭ᓍ") + json.dumps(
                              bstack11l1l1l_opy_ (u"ࠨࡓࡤࡧࡱࡥࡷ࡯࡯ࠡࡨࡤ࡭ࡱ࡫ࡤࠡࡹ࡬ࡸ࡭ࡀࠠࠣᓎ") + str(message)) + bstack11l1l1l_opy_ (u"ࠧ࠭ࠤࡶࡸࡦࡺࡵࡴࠤ࠽ࠫᓏ") + json.dumps(status) + bstack11l1l1l_opy_ (u"ࠣࡿࢀࠦᓐ"))
        else:
            page.evaluate(bstack11l1l1l_opy_ (u"ࠤࡢࠤࡂࡄࠠࡼࡿࠥᓑ"),
                          bstack11l1l1l_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࡡࡨࡼࡪࡩࡵࡵࡱࡵ࠾ࠥࢁࠢࡢࡥࡷ࡭ࡴࡴࠢ࠻ࠢࠥࡷࡪࡺࡓࡦࡵࡶ࡭ࡴࡴࡓࡵࡣࡷࡹࡸࠨࠬࠡࠤࡤࡶ࡬ࡻ࡭ࡦࡰࡷࡷࠧࡀࠠࡼࠤࡶࡸࡦࡺࡵࡴࠤ࠽ࠫᓒ") + json.dumps(
                              status) + bstack11l1l1l_opy_ (u"ࠦࢂࢃࠢᓓ"))
    except Exception as e:
        print(bstack11l1l1l_opy_ (u"ࠧ࡫ࡸࡤࡧࡳࡸ࡮ࡵ࡮ࠡ࡫ࡱࠤࡵࡲࡡࡺࡹࡵ࡭࡬࡮ࡴࠡࡵࡨࡸࠥࡹࡥࡴࡵ࡬ࡳࡳࠦࡳࡵࡣࡷࡹࡸࠦࡻࡾࠤᓔ"), e)
def pytest_configure(config):
    config.args = bstack1l11l11l_opy_.bstack1111lll111_opy_(config.args)
@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    bstack11111l1l11_opy_ = item.config.getoption(bstack11l1l1l_opy_ (u"࠭ࡳ࡬࡫ࡳࡗࡪࡹࡳࡪࡱࡱࡒࡦࡳࡥࠨᓕ"))
    plugins = item.config.getoption(bstack11l1l1l_opy_ (u"ࠢࡱ࡮ࡸ࡫࡮ࡴࡳࠣᓖ"))
    report = outcome.get_result()
    bstack111111l11l_opy_(item, call, report)
    if bstack11l1l1l_opy_ (u"ࠣࡲࡼࡸࡪࡹࡴࡠࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱࡰ࡭ࡷࡪ࡭ࡳࠨᓗ") not in plugins or bstack11ll1111_opy_():
        return
    summary = []
    driver = getattr(item, bstack11l1l1l_opy_ (u"ࠤࡢࡨࡷ࡯ࡶࡦࡴࠥᓘ"), None)
    page = getattr(item, bstack11l1l1l_opy_ (u"ࠥࡣࡵࡧࡧࡦࠤᓙ"), None)
    try:
        if (driver == None):
            driver = threading.current_thread().bstackSessionDriver
    except:
        pass
    item._driver = driver
    if (driver is not None):
        bstack11111lll1l_opy_(item, report, summary, bstack11111l1l11_opy_)
    if (page is not None):
        bstack11111l111l_opy_(item, report, summary, bstack11111l1l11_opy_)
def bstack11111lll1l_opy_(item, report, summary, bstack11111l1l11_opy_):
    if report.when == bstack11l1l1l_opy_ (u"ࠫࡸ࡫ࡴࡶࡲࠪᓚ") and report.skipped:
        bstack111ll11l1l_opy_(report)
    if report.when in [bstack11l1l1l_opy_ (u"ࠧࡹࡥࡵࡷࡳࠦᓛ"), bstack11l1l1l_opy_ (u"ࠨࡴࡦࡣࡵࡨࡴࡽ࡮ࠣᓜ")]:
        return
    if not bstack11lll1l1ll_opy_():
        return
    try:
        if (str(bstack11111l1l11_opy_).lower() != bstack11l1l1l_opy_ (u"ࠧࡵࡴࡸࡩࠬᓝ")):
            item._driver.execute_script(
                bstack11l1l1l_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࡟ࡦࡺࡨࡧࡺࡺ࡯ࡳ࠼ࠣࡿࠧࡧࡣࡵ࡫ࡲࡲࠧࡀࠠࠣࡵࡨࡸࡘ࡫ࡳࡴ࡫ࡲࡲࡓࡧ࡭ࡦࠤ࠯ࠤࠧࡧࡲࡨࡷࡰࡩࡳࡺࡳࠣ࠼ࠣࡿࠧࡴࡡ࡮ࡧࠥ࠾ࠥ࠭ᓞ") + json.dumps(
                    report.nodeid) + bstack11l1l1l_opy_ (u"ࠩࢀࢁࠬᓟ"))
        os.environ[bstack11l1l1l_opy_ (u"ࠪࡔ࡞࡚ࡅࡔࡖࡢࡘࡊ࡙ࡔࡠࡐࡄࡑࡊ࠭ᓠ")] = report.nodeid
    except Exception as e:
        summary.append(
            bstack11l1l1l_opy_ (u"ࠦ࡜ࡇࡒࡏࡋࡑࡋ࠿ࠦࡆࡢ࡫࡯ࡩࡩࠦࡴࡰࠢࡰࡥࡷࡱࠠࡴࡧࡶࡷ࡮ࡵ࡮ࠡࡰࡤࡱࡪࡀࠠࡼ࠲ࢀࠦᓡ").format(e)
        )
    passed = report.passed or report.skipped or (report.failed and hasattr(report, bstack11l1l1l_opy_ (u"ࠧࡽࡡࡴࡺࡩࡥ࡮ࡲࠢᓢ")))
    bstack1ll1111111_opy_ = bstack11l1l1l_opy_ (u"ࠨࠢᓣ")
    bstack111ll11l1l_opy_(report)
    if not passed:
        try:
            bstack1ll1111111_opy_ = report.longrepr.reprcrash
        except Exception as e:
            summary.append(
                bstack11l1l1l_opy_ (u"ࠢࡘࡃࡕࡒࡎࡔࡇ࠻ࠢࡉࡥ࡮ࡲࡥࡥࠢࡷࡳࠥࡪࡥࡵࡧࡵࡱ࡮ࡴࡥࠡࡨࡤ࡭ࡱࡻࡲࡦࠢࡵࡩࡦࡹ࡯࡯࠼ࠣࡿ࠵ࢃࠢᓤ").format(e)
            )
        try:
            if (threading.current_thread().bstackTestErrorMessages == None):
                threading.current_thread().bstackTestErrorMessages = []
        except Exception as e:
            threading.current_thread().bstackTestErrorMessages = []
        threading.current_thread().bstackTestErrorMessages.append(str(bstack1ll1111111_opy_))
    if not report.skipped:
        passed = report.passed or (report.failed and hasattr(report, bstack11l1l1l_opy_ (u"ࠣࡹࡤࡷࡽ࡬ࡡࡪ࡮ࠥᓥ")))
        bstack1ll1111111_opy_ = bstack11l1l1l_opy_ (u"ࠤࠥᓦ")
        if not passed:
            try:
                bstack1ll1111111_opy_ = report.longrepr.reprcrash
            except Exception as e:
                summary.append(
                    bstack11l1l1l_opy_ (u"࡛ࠥࡆࡘࡎࡊࡐࡊ࠾ࠥࡌࡡࡪ࡮ࡨࡨࠥࡺ࡯ࠡࡦࡨࡸࡪࡸ࡭ࡪࡰࡨࠤ࡫ࡧࡩ࡭ࡷࡵࡩࠥࡸࡥࡢࡵࡲࡲ࠿ࠦࡻ࠱ࡿࠥᓧ").format(e)
                )
            try:
                if (threading.current_thread().bstackTestErrorMessages == None):
                    threading.current_thread().bstackTestErrorMessages = []
            except Exception as e:
                threading.current_thread().bstackTestErrorMessages = []
            threading.current_thread().bstackTestErrorMessages.append(str(bstack1ll1111111_opy_))
        try:
            if passed:
                item._driver.execute_script(
                    bstack11l1l1l_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࡢࡩࡽ࡫ࡣࡶࡶࡲࡶ࠿ࠦࡻ࡝ࠌࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠥࡥࡨࡺࡩࡰࡰࠥ࠾ࠥࠨࡡ࡯ࡰࡲࡸࡦࡺࡥࠣ࠮ࠣࡠࠏࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠨࡡࡳࡩࡸࡱࡪࡴࡴࡴࠤ࠽ࠤࢀࡢࠊࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠧࡲࡥࡷࡧ࡯ࠦ࠿ࠦࠢࡪࡰࡩࡳࠧ࠲ࠠ࡝ࠌࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠢࡥࡣࡷࡥࠧࡀࠠࠨᓨ")
                    + json.dumps(bstack11l1l1l_opy_ (u"ࠧࡶࡡࡴࡵࡨࡨࠦࠨᓩ"))
                    + bstack11l1l1l_opy_ (u"ࠨ࡜ࠋࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࡿ࡟ࠎࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࡾࠤᓪ")
                )
            else:
                item._driver.execute_script(
                    bstack11l1l1l_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰࡥࡥࡹࡧࡦࡹࡹࡵࡲ࠻ࠢࡾࡠࠏࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠨࡡࡤࡶ࡬ࡳࡳࠨ࠺ࠡࠤࡤࡲࡳࡵࡴࡢࡶࡨࠦ࠱ࠦ࡜ࠋࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠤࡤࡶ࡬ࡻ࡭ࡦࡰࡷࡷࠧࡀࠠࡼ࡞ࠍࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠣ࡮ࡨࡺࡪࡲࠢ࠻ࠢࠥࡩࡷࡸ࡯ࡳࠤ࠯ࠤࡡࠐࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠦࡩࡧࡴࡢࠤ࠽ࠤࠬᓫ")
                    + json.dumps(str(bstack1ll1111111_opy_))
                    + bstack11l1l1l_opy_ (u"ࠣ࡞ࠍࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࢁࡡࠐࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࢀࠦᓬ")
                )
        except Exception as e:
            summary.append(bstack11l1l1l_opy_ (u"ࠤ࡚ࡅࡗࡔࡉࡏࡉ࠽ࠤࡋࡧࡩ࡭ࡧࡧࠤࡹࡵࠠࡢࡰࡱࡳࡹࡧࡴࡦ࠼ࠣࡿ࠵ࢃࠢᓭ").format(e))
def bstack11111lll11_opy_(test_name, error_message):
    try:
        bstack11111l11ll_opy_ = []
        bstack1111l11l1_opy_ = os.environ.get(bstack11l1l1l_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡓࡐࡆ࡚ࡆࡐࡔࡐࡣࡎࡔࡄࡆ࡚ࠪᓮ"), bstack11l1l1l_opy_ (u"ࠫ࠵࠭ᓯ"))
        bstack1l1ll1lll1_opy_ = {bstack11l1l1l_opy_ (u"ࠬࡴࡡ࡮ࡧࠪᓰ"): test_name, bstack11l1l1l_opy_ (u"࠭ࡥࡳࡴࡲࡶࠬᓱ"): error_message, bstack11l1l1l_opy_ (u"ࠧࡪࡰࡧࡩࡽ࠭ᓲ"): bstack1111l11l1_opy_}
        bstack11111llll1_opy_ = os.path.join(tempfile.gettempdir(), bstack11l1l1l_opy_ (u"ࠨࡲࡺࡣࡵࡿࡴࡦࡵࡷࡣࡪࡸࡲࡰࡴࡢࡰ࡮ࡹࡴ࠯࡬ࡶࡳࡳ࠭ᓳ"))
        if os.path.exists(bstack11111llll1_opy_):
            with open(bstack11111llll1_opy_) as f:
                bstack11111l11ll_opy_ = json.load(f)
        bstack11111l11ll_opy_.append(bstack1l1ll1lll1_opy_)
        with open(bstack11111llll1_opy_, bstack11l1l1l_opy_ (u"ࠩࡺࠫᓴ")) as f:
            json.dump(bstack11111l11ll_opy_, f)
    except Exception as e:
        logger.debug(bstack11l1l1l_opy_ (u"ࠪࡉࡷࡸ࡯ࡳࠢ࡬ࡲࠥࡶࡥࡳࡵ࡬ࡷࡹ࡯࡮ࡨࠢࡳࡰࡦࡿࡷࡳ࡫ࡪ࡬ࡹࠦࡰࡺࡶࡨࡷࡹࠦࡥࡳࡴࡲࡶࡸࡀࠠࠨᓵ") + str(e))
def bstack11111l111l_opy_(item, report, summary, bstack11111l1l11_opy_):
    if report.when in [bstack11l1l1l_opy_ (u"ࠦࡸ࡫ࡴࡶࡲࠥᓶ"), bstack11l1l1l_opy_ (u"ࠧࡺࡥࡢࡴࡧࡳࡼࡴࠢᓷ")]:
        return
    if (str(bstack11111l1l11_opy_).lower() != bstack11l1l1l_opy_ (u"࠭ࡴࡳࡷࡨࠫᓸ")):
        bstack11111111l_opy_(item._page, report.nodeid)
    passed = report.passed or report.skipped or (report.failed and hasattr(report, bstack11l1l1l_opy_ (u"ࠢࡸࡣࡶࡼ࡫ࡧࡩ࡭ࠤᓹ")))
    bstack1ll1111111_opy_ = bstack11l1l1l_opy_ (u"ࠣࠤᓺ")
    bstack111ll11l1l_opy_(report)
    if not report.skipped:
        if not passed:
            try:
                bstack1ll1111111_opy_ = report.longrepr.reprcrash
            except Exception as e:
                summary.append(
                    bstack11l1l1l_opy_ (u"ࠤ࡚ࡅࡗࡔࡉࡏࡉ࠽ࠤࡋࡧࡩ࡭ࡧࡧࠤࡹࡵࠠࡥࡧࡷࡩࡷࡳࡩ࡯ࡧࠣࡪࡦ࡯࡬ࡶࡴࡨࠤࡷ࡫ࡡࡴࡱࡱ࠾ࠥࢁ࠰ࡾࠤᓻ").format(e)
                )
        try:
            if passed:
                bstack1l11l1l1l_opy_(item._page, bstack11l1l1l_opy_ (u"ࠥࡴࡦࡹࡳࡦࡦࠥᓼ"))
            else:
                error_message = bstack11l1l1l_opy_ (u"ࠫࠬᓽ")
                if bstack1ll1111111_opy_:
                    bstack1111l1lll_opy_(item._page, str(bstack1ll1111111_opy_), bstack11l1l1l_opy_ (u"ࠧ࡫ࡲࡳࡱࡵࠦᓾ"))
                    bstack1l11l1l1l_opy_(item._page, bstack11l1l1l_opy_ (u"ࠨࡦࡢ࡫࡯ࡩࡩࠨᓿ"), str(bstack1ll1111111_opy_))
                    error_message = str(bstack1ll1111111_opy_)
                else:
                    bstack1l11l1l1l_opy_(item._page, bstack11l1l1l_opy_ (u"ࠢࡧࡣ࡬ࡰࡪࡪࠢᔀ"))
                bstack11111lll11_opy_(report.nodeid, error_message)
        except Exception as e:
            summary.append(bstack11l1l1l_opy_ (u"࡙ࠣࡄࡖࡓࡏࡎࡈ࠼ࠣࡊࡦ࡯࡬ࡦࡦࠣࡸࡴࠦࡵࡱࡦࡤࡸࡪࠦࡳࡦࡵࡶ࡭ࡴࡴࠠࡴࡶࡤࡸࡺࡹ࠺ࠡࡽ࠳ࢁࠧᔁ").format(e))
try:
    from typing import Generator
    import pytest_playwright.pytest_playwright as p
    @pytest.fixture
    def page(context: BrowserContext, request: pytest.FixtureRequest) -> Generator[Page, None, None]:
        page = context.new_page()
        request.node._page = page
        yield page
except:
    pass
def pytest_addoption(parser):
    parser.addoption(bstack11l1l1l_opy_ (u"ࠤ࠰࠱ࡸࡱࡩࡱࡕࡨࡷࡸ࡯࡯࡯ࡐࡤࡱࡪࠨᔂ"), default=bstack11l1l1l_opy_ (u"ࠥࡊࡦࡲࡳࡦࠤᔃ"), help=bstack11l1l1l_opy_ (u"ࠦࡆࡻࡴࡰ࡯ࡤࡸ࡮ࡩࠠࡴࡧࡷࠤࡸ࡫ࡳࡴ࡫ࡲࡲࠥࡴࡡ࡮ࡧࠥᔄ"))
    try:
        import pytest_selenium.pytest_selenium
    except:
        parser.addoption(bstack11l1l1l_opy_ (u"ࠧ࠳࠭ࡥࡴ࡬ࡺࡪࡸࠢᔅ"), action=bstack11l1l1l_opy_ (u"ࠨࡳࡵࡱࡵࡩࠧᔆ"), default=bstack11l1l1l_opy_ (u"ࠢࡤࡪࡵࡳࡲ࡫ࠢᔇ"),
                         help=bstack11l1l1l_opy_ (u"ࠣࡆࡵ࡭ࡻ࡫ࡲࠡࡶࡲࠤࡷࡻ࡮ࠡࡶࡨࡷࡹࡹࠢᔈ"))
def bstack1l1l1ll1ll_opy_(log):
    if not (log[bstack11l1l1l_opy_ (u"ࠩࡰࡩࡸࡹࡡࡨࡧࠪᔉ")] and log[bstack11l1l1l_opy_ (u"ࠪࡱࡪࡹࡳࡢࡩࡨࠫᔊ")].strip()):
        return
    active = bstack1l1l11l1l1_opy_()
    log = {
        bstack11l1l1l_opy_ (u"ࠫࡱ࡫ࡶࡦ࡮ࠪᔋ"): log[bstack11l1l1l_opy_ (u"ࠬࡲࡥࡷࡧ࡯ࠫᔌ")],
        bstack11l1l1l_opy_ (u"࠭ࡴࡪ࡯ࡨࡷࡹࡧ࡭ࡱࠩᔍ"): datetime.datetime.utcnow().isoformat() + bstack11l1l1l_opy_ (u"࡛ࠧࠩᔎ"),
        bstack11l1l1l_opy_ (u"ࠨ࡯ࡨࡷࡸࡧࡧࡦࠩᔏ"): log[bstack11l1l1l_opy_ (u"ࠩࡰࡩࡸࡹࡡࡨࡧࠪᔐ")],
    }
    if active:
        if active[bstack11l1l1l_opy_ (u"ࠪࡸࡾࡶࡥࠨᔑ")] == bstack11l1l1l_opy_ (u"ࠫ࡭ࡵ࡯࡬ࠩᔒ"):
            log[bstack11l1l1l_opy_ (u"ࠬ࡮࡯ࡰ࡭ࡢࡶࡺࡴ࡟ࡶࡷ࡬ࡨࠬᔓ")] = active[bstack11l1l1l_opy_ (u"࠭ࡨࡰࡱ࡮ࡣࡷࡻ࡮ࡠࡷࡸ࡭ࡩ࠭ᔔ")]
        elif active[bstack11l1l1l_opy_ (u"ࠧࡵࡻࡳࡩࠬᔕ")] == bstack11l1l1l_opy_ (u"ࠨࡶࡨࡷࡹ࠭ᔖ"):
            log[bstack11l1l1l_opy_ (u"ࠩࡷࡩࡸࡺ࡟ࡳࡷࡱࡣࡺࡻࡩࡥࠩᔗ")] = active[bstack11l1l1l_opy_ (u"ࠪࡸࡪࡹࡴࡠࡴࡸࡲࡤࡻࡵࡪࡦࠪᔘ")]
    bstack1l11l11l_opy_.bstack1l11llll1l_opy_([log])
def bstack1l1l11l1l1_opy_():
    if len(store[bstack11l1l1l_opy_ (u"ࠫࡨࡻࡲࡳࡧࡱࡸࡤ࡮࡯ࡰ࡭ࡢࡹࡺ࡯ࡤࠨᔙ")]) > 0 and store[bstack11l1l1l_opy_ (u"ࠬࡩࡵࡳࡴࡨࡲࡹࡥࡨࡰࡱ࡮ࡣࡺࡻࡩࡥࠩᔚ")][-1]:
        return {
            bstack11l1l1l_opy_ (u"࠭ࡴࡺࡲࡨࠫᔛ"): bstack11l1l1l_opy_ (u"ࠧࡩࡱࡲ࡯ࠬᔜ"),
            bstack11l1l1l_opy_ (u"ࠨࡪࡲࡳࡰࡥࡲࡶࡰࡢࡹࡺ࡯ࡤࠨᔝ"): store[bstack11l1l1l_opy_ (u"ࠩࡦࡹࡷࡸࡥ࡯ࡶࡢ࡬ࡴࡵ࡫ࡠࡷࡸ࡭ࡩ࠭ᔞ")][-1]
        }
    if store.get(bstack11l1l1l_opy_ (u"ࠪࡧࡺࡸࡲࡦࡰࡷࡣࡹ࡫ࡳࡵࡡࡸࡹ࡮ࡪࠧᔟ"), None):
        return {
            bstack11l1l1l_opy_ (u"ࠫࡹࡿࡰࡦࠩᔠ"): bstack11l1l1l_opy_ (u"ࠬࡺࡥࡴࡶࠪᔡ"),
            bstack11l1l1l_opy_ (u"࠭ࡴࡦࡵࡷࡣࡷࡻ࡮ࡠࡷࡸ࡭ࡩ࠭ᔢ"): store[bstack11l1l1l_opy_ (u"ࠧࡤࡷࡵࡶࡪࡴࡴࡠࡶࡨࡷࡹࡥࡵࡶ࡫ࡧࠫᔣ")]
        }
    return None
bstack1l1l1lll11_opy_ = bstack1l1ll1111l_opy_(bstack1l1l1ll1ll_opy_)
def pytest_runtest_call(item):
    try:
        global CONFIG
        global bstack11111l11l1_opy_
        if bstack11111l11l1_opy_:
            driver = getattr(item, bstack11l1l1l_opy_ (u"ࠨࡡࡧࡶ࡮ࡼࡥࡳࠩᔤ"), None)
            bstack1lll1l1ll1_opy_ = bstack1111ll111_opy_.bstack1l1lllll_opy_(CONFIG, bstack11ll1lll1l_opy_(item.own_markers))
            item._a11y_started = bstack1111ll111_opy_.bstack1l1llll111_opy_(driver, bstack1lll1l1ll1_opy_)
        if not bstack1l11l11l_opy_.on() or bstack11111l1ll1_opy_ != bstack11l1l1l_opy_ (u"ࠩࡳࡽࡹ࡫ࡳࡵࠩᔥ"):
            return
        global current_test_uuid, bstack1l1l1lll11_opy_
        bstack1l1l1lll11_opy_.start()
        bstack1l1l111ll1_opy_ = {
            bstack11l1l1l_opy_ (u"ࠪࡹࡺ࡯ࡤࠨᔦ"): uuid4().__str__(),
            bstack11l1l1l_opy_ (u"ࠫࡸࡺࡡࡳࡶࡨࡨࡤࡧࡴࠨᔧ"): datetime.datetime.utcnow().isoformat() + bstack11l1l1l_opy_ (u"ࠬࡠࠧᔨ")
        }
        current_test_uuid = bstack1l1l111ll1_opy_[bstack11l1l1l_opy_ (u"࠭ࡵࡶ࡫ࡧࠫᔩ")]
        store[bstack11l1l1l_opy_ (u"ࠧࡤࡷࡵࡶࡪࡴࡴࡠࡶࡨࡷࡹࡥࡵࡶ࡫ࡧࠫᔪ")] = bstack1l1l111ll1_opy_[bstack11l1l1l_opy_ (u"ࠨࡷࡸ࡭ࡩ࠭ᔫ")]
        threading.current_thread().current_test_uuid = current_test_uuid
        _1l1ll11111_opy_[item.nodeid] = {**_1l1ll11111_opy_[item.nodeid], **bstack1l1l111ll1_opy_}
        bstack1111l1111l_opy_(item, _1l1ll11111_opy_[item.nodeid], bstack11l1l1l_opy_ (u"ࠩࡗࡩࡸࡺࡒࡶࡰࡖࡸࡦࡸࡴࡦࡦࠪᔬ"))
    except Exception as err:
        print(bstack11l1l1l_opy_ (u"ࠪࡉࡽࡩࡥࡱࡶ࡬ࡳࡳࠦࡩ࡯ࠢࡳࡽࡹ࡫ࡳࡵࡡࡵࡹࡳࡺࡥࡴࡶࡢࡧࡦࡲ࡬࠻ࠢࡾࢁࠬᔭ"), str(err))
def pytest_runtest_setup(item):
    if bstack11ll11lll1_opy_():
        atexit.register(bstack111111ll1_opy_)
        try:
            item.config.hook.pytest_selenium_runtest_makereport = bstack111ll1lll1_opy_
        except Exception as err:
            threading.current_thread().testStatus = bstack11l1l1l_opy_ (u"ࠫࡵࡧࡳࡴࡧࡧࠫᔮ")
    try:
        if not bstack1l11l11l_opy_.on():
            return
        bstack1l1l1lll11_opy_.start()
        uuid = uuid4().__str__()
        bstack1l1l111ll1_opy_ = {
            bstack11l1l1l_opy_ (u"ࠬࡻࡵࡪࡦࠪᔯ"): uuid,
            bstack11l1l1l_opy_ (u"࠭ࡳࡵࡣࡵࡸࡪࡪ࡟ࡢࡶࠪᔰ"): datetime.datetime.utcnow().isoformat() + bstack11l1l1l_opy_ (u"࡛ࠧࠩᔱ"),
            bstack11l1l1l_opy_ (u"ࠨࡶࡼࡴࡪ࠭ᔲ"): bstack11l1l1l_opy_ (u"ࠩ࡫ࡳࡴࡱࠧᔳ"),
            bstack11l1l1l_opy_ (u"ࠪ࡬ࡴࡵ࡫ࡠࡶࡼࡴࡪ࠭ᔴ"): bstack11l1l1l_opy_ (u"ࠫࡇࡋࡆࡐࡔࡈࡣࡊࡇࡃࡉࠩᔵ"),
            bstack11l1l1l_opy_ (u"ࠬ࡮࡯ࡰ࡭ࡢࡲࡦࡳࡥࠨᔶ"): bstack11l1l1l_opy_ (u"࠭ࡳࡦࡶࡸࡴࠬᔷ")
        }
        threading.current_thread().current_hook_uuid = uuid
        store[bstack11l1l1l_opy_ (u"ࠧࡤࡷࡵࡶࡪࡴࡴࡠࡶࡨࡷࡹࡥࡩࡵࡧࡰࠫᔸ")] = item
        store[bstack11l1l1l_opy_ (u"ࠨࡥࡸࡶࡷ࡫࡮ࡵࡡ࡫ࡳࡴࡱ࡟ࡶࡷ࡬ࡨࠬᔹ")] = [uuid]
        if not _1l1ll11111_opy_.get(item.nodeid, None):
            _1l1ll11111_opy_[item.nodeid] = {bstack11l1l1l_opy_ (u"ࠩ࡫ࡳࡴࡱࡳࠨᔺ"): [], bstack11l1l1l_opy_ (u"ࠪࡪ࡮ࡾࡴࡶࡴࡨࡷࠬᔻ"): []}
        _1l1ll11111_opy_[item.nodeid][bstack11l1l1l_opy_ (u"ࠫ࡭ࡵ࡯࡬ࡵࠪᔼ")].append(bstack1l1l111ll1_opy_[bstack11l1l1l_opy_ (u"ࠬࡻࡵࡪࡦࠪᔽ")])
        _1l1ll11111_opy_[item.nodeid + bstack11l1l1l_opy_ (u"࠭࠭ࡴࡧࡷࡹࡵ࠭ᔾ")] = bstack1l1l111ll1_opy_
        bstack11111ll111_opy_(item, bstack1l1l111ll1_opy_, bstack11l1l1l_opy_ (u"ࠧࡉࡱࡲ࡯ࡗࡻ࡮ࡔࡶࡤࡶࡹ࡫ࡤࠨᔿ"))
    except Exception as err:
        print(bstack11l1l1l_opy_ (u"ࠨࡇࡻࡧࡪࡶࡴࡪࡱࡱࠤ࡮ࡴࠠࡱࡻࡷࡩࡸࡺ࡟ࡳࡷࡱࡸࡪࡹࡴࡠࡵࡨࡸࡺࡶ࠺ࠡࡽࢀࠫᕀ"), str(err))
def pytest_runtest_teardown(item):
    try:
        global bstack11l11l1l_opy_
        if getattr(item, bstack11l1l1l_opy_ (u"ࠩࡢࡥ࠶࠷ࡹࡠࡵࡷࡥࡷࡺࡥࡥࠩᕁ"), False):
            logger.info(bstack11l1l1l_opy_ (u"ࠥࡅࡺࡺ࡯࡮ࡣࡷࡩࠥࡺࡥࡴࡶࠣࡧࡦࡹࡥࠡࡧࡻࡩࡨࡻࡴࡪࡱࡱࠤ࡭ࡧࡳࠡࡧࡱࡨࡪࡪ࠮ࠡࡒࡵࡳࡨ࡫ࡳࡴ࡫ࡱ࡫ࠥ࡬࡯ࡳࠢࡤࡧࡨ࡫ࡳࡴ࡫ࡥ࡭ࡱ࡯ࡴࡺࠢࡷࡩࡸࡺࡩ࡯ࡩࠣ࡭ࡸࠦࡵ࡯ࡦࡨࡶࡼࡧࡹ࠯ࠢࠥᕂ"))
            driver = getattr(item, bstack11l1l1l_opy_ (u"ࠫࡤࡪࡲࡪࡸࡨࡶࠬᕃ"), None)
            bstack1l11111111_opy_ = item.cls.__name__ if not item.cls is None else None
            bstack1111ll111_opy_.bstack11l11lll1_opy_(driver, bstack1l11111111_opy_, item.name, item.module.__name__, item.path, bstack11l11l1l_opy_)
        if not bstack1l11l11l_opy_.on():
            return
        bstack1l1l111ll1_opy_ = {
            bstack11l1l1l_opy_ (u"ࠬࡻࡵࡪࡦࠪᕄ"): uuid4().__str__(),
            bstack11l1l1l_opy_ (u"࠭ࡳࡵࡣࡵࡸࡪࡪ࡟ࡢࡶࠪᕅ"): datetime.datetime.utcnow().isoformat() + bstack11l1l1l_opy_ (u"࡛ࠧࠩᕆ"),
            bstack11l1l1l_opy_ (u"ࠨࡶࡼࡴࡪ࠭ᕇ"): bstack11l1l1l_opy_ (u"ࠩ࡫ࡳࡴࡱࠧᕈ"),
            bstack11l1l1l_opy_ (u"ࠪ࡬ࡴࡵ࡫ࡠࡶࡼࡴࡪ࠭ᕉ"): bstack11l1l1l_opy_ (u"ࠫࡆࡌࡔࡆࡔࡢࡉࡆࡉࡈࠨᕊ"),
            bstack11l1l1l_opy_ (u"ࠬ࡮࡯ࡰ࡭ࡢࡲࡦࡳࡥࠨᕋ"): bstack11l1l1l_opy_ (u"࠭ࡴࡦࡣࡵࡨࡴࡽ࡮ࠨᕌ")
        }
        _1l1ll11111_opy_[item.nodeid + bstack11l1l1l_opy_ (u"ࠧ࠮ࡶࡨࡥࡷࡪ࡯ࡸࡰࠪᕍ")] = bstack1l1l111ll1_opy_
        bstack11111ll111_opy_(item, bstack1l1l111ll1_opy_, bstack11l1l1l_opy_ (u"ࠨࡊࡲࡳࡰࡘࡵ࡯ࡕࡷࡥࡷࡺࡥࡥࠩᕎ"))
    except Exception as err:
        print(bstack11l1l1l_opy_ (u"ࠩࡈࡼࡨ࡫ࡰࡵ࡫ࡲࡲࠥ࡯࡮ࠡࡲࡼࡸࡪࡹࡴࡠࡴࡸࡲࡹ࡫ࡳࡵࡡࡷࡩࡦࡸࡤࡰࡹࡱ࠾ࠥࢁࡽࠨᕏ"), str(err))
@pytest.hookimpl(hookwrapper=True)
def pytest_fixture_setup(fixturedef, request):
    if not bstack1l11l11l_opy_.on():
        yield
        return
    start_time = datetime.datetime.now()
    if bstack111ll11ll1_opy_(fixturedef.argname):
        store[bstack11l1l1l_opy_ (u"ࠪࡧࡺࡸࡲࡦࡰࡷࡣࡲࡵࡤࡶ࡮ࡨࡣ࡮ࡺࡥ࡮ࠩᕐ")] = request.node
    elif bstack111ll1l1ll_opy_(fixturedef.argname):
        store[bstack11l1l1l_opy_ (u"ࠫࡨࡻࡲࡳࡧࡱࡸࡤࡩ࡬ࡢࡵࡶࡣ࡮ࡺࡥ࡮ࠩᕑ")] = request.node
    outcome = yield
    try:
        fixture = {
            bstack11l1l1l_opy_ (u"ࠬࡴࡡ࡮ࡧࠪᕒ"): fixturedef.argname,
            bstack11l1l1l_opy_ (u"࠭ࡲࡦࡵࡸࡰࡹ࠭ᕓ"): bstack11ll1111ll_opy_(outcome),
            bstack11l1l1l_opy_ (u"ࠧࡥࡷࡵࡥࡹ࡯࡯࡯ࠩᕔ"): (datetime.datetime.now() - start_time).total_seconds() * 1000
        }
        bstack11111l1lll_opy_ = store[bstack11l1l1l_opy_ (u"ࠨࡥࡸࡶࡷ࡫࡮ࡵࡡࡷࡩࡸࡺ࡟ࡪࡶࡨࡱࠬᕕ")]
        if not _1l1ll11111_opy_.get(bstack11111l1lll_opy_.nodeid, None):
            _1l1ll11111_opy_[bstack11111l1lll_opy_.nodeid] = {bstack11l1l1l_opy_ (u"ࠩࡩ࡭ࡽࡺࡵࡳࡧࡶࠫᕖ"): []}
        _1l1ll11111_opy_[bstack11111l1lll_opy_.nodeid][bstack11l1l1l_opy_ (u"ࠪࡪ࡮ࡾࡴࡶࡴࡨࡷࠬᕗ")].append(fixture)
    except Exception as err:
        logger.debug(bstack11l1l1l_opy_ (u"ࠫࡊࡾࡣࡦࡲࡷ࡭ࡴࡴࠠࡪࡰࠣࡴࡾࡺࡥࡴࡶࡢࡪ࡮ࡾࡴࡶࡴࡨࡣࡸ࡫ࡴࡶࡲ࠽ࠤࢀࢃࠧᕘ"), str(err))
if bstack11ll1111_opy_() and bstack1l11l11l_opy_.on():
    def pytest_bdd_before_step(request, step):
        try:
            _1l1ll11111_opy_[request.node.nodeid][bstack11l1l1l_opy_ (u"ࠬࡺࡥࡴࡶࡢࡨࡦࡺࡡࠨᕙ")].bstack111l111lll_opy_(id(step))
        except Exception as err:
            print(bstack11l1l1l_opy_ (u"࠭ࡅࡹࡥࡨࡴࡹ࡯࡯࡯ࠢ࡬ࡲࠥࡶࡹࡵࡧࡶࡸࡤࡨࡤࡥࡡࡥࡩ࡫ࡵࡲࡦࡡࡶࡸࡪࡶ࠺ࠡࡽࢀࠫᕚ"), str(err))
    def pytest_bdd_step_error(request, step, exception):
        try:
            _1l1ll11111_opy_[request.node.nodeid][bstack11l1l1l_opy_ (u"ࠧࡵࡧࡶࡸࡤࡪࡡࡵࡣࠪᕛ")].bstack1l1l111l11_opy_(id(step), Result.failed(exception=exception))
        except Exception as err:
            print(bstack11l1l1l_opy_ (u"ࠨࡇࡻࡧࡪࡶࡴࡪࡱࡱࠤ࡮ࡴࠠࡱࡻࡷࡩࡸࡺ࡟ࡣࡦࡧࡣࡸࡺࡥࡱࡡࡨࡶࡷࡵࡲ࠻ࠢࡾࢁࠬᕜ"), str(err))
    def pytest_bdd_after_step(request, step):
        try:
            bstack1l11l1l1ll_opy_: bstack1l1l1llll1_opy_ = _1l1ll11111_opy_[request.node.nodeid][bstack11l1l1l_opy_ (u"ࠩࡷࡩࡸࡺ࡟ࡥࡣࡷࡥࠬᕝ")]
            bstack1l11l1l1ll_opy_.bstack1l1l111l11_opy_(id(step), Result.passed())
        except Exception as err:
            print(bstack11l1l1l_opy_ (u"ࠪࡉࡽࡩࡥࡱࡶ࡬ࡳࡳࠦࡩ࡯ࠢࡳࡽࡹ࡫ࡳࡵࡡࡥࡨࡩࡥࡳࡵࡧࡳࡣࡪࡸࡲࡰࡴ࠽ࠤࢀࢃࠧᕞ"), str(err))
    def pytest_bdd_before_scenario(request, feature, scenario):
        global bstack11111l1ll1_opy_
        try:
            if not bstack1l11l11l_opy_.on() or bstack11111l1ll1_opy_ != bstack11l1l1l_opy_ (u"ࠫࡵࡿࡴࡦࡵࡷ࠱ࡧࡪࡤࠨᕟ"):
                return
            global bstack1l1l1lll11_opy_
            bstack1l1l1lll11_opy_.start()
            if not _1l1ll11111_opy_.get(request.node.nodeid, None):
                _1l1ll11111_opy_[request.node.nodeid] = {}
            bstack1l11l1l1ll_opy_ = bstack1l1l1llll1_opy_.bstack111l111ll1_opy_(
                scenario, feature, request.node,
                name=bstack111ll111ll_opy_(request.node, scenario),
                bstack1l1l1l1ll1_opy_=bstack1llllll11l_opy_(),
                file_path=feature.filename,
                scope=[feature.name],
                framework=bstack11l1l1l_opy_ (u"ࠬࡖࡹࡵࡧࡶࡸ࠲ࡩࡵࡤࡷࡰࡦࡪࡸࠧᕠ"),
                tags=bstack111ll1l11l_opy_(feature, scenario)
            )
            _1l1ll11111_opy_[request.node.nodeid][bstack11l1l1l_opy_ (u"࠭ࡴࡦࡵࡷࡣࡩࡧࡴࡢࠩᕡ")] = bstack1l11l1l1ll_opy_
            bstack11111l1111_opy_(bstack1l11l1l1ll_opy_.uuid)
            bstack1l11l11l_opy_.bstack1l11l1ll1l_opy_(bstack11l1l1l_opy_ (u"ࠧࡕࡧࡶࡸࡗࡻ࡮ࡔࡶࡤࡶࡹ࡫ࡤࠨᕢ"), bstack1l11l1l1ll_opy_)
        except Exception as err:
            print(bstack11l1l1l_opy_ (u"ࠨࡇࡻࡧࡪࡶࡴࡪࡱࡱࠤ࡮ࡴࠠࡱࡻࡷࡩࡸࡺ࡟ࡣࡦࡧࡣࡧ࡫ࡦࡰࡴࡨࡣࡸࡩࡥ࡯ࡣࡵ࡭ࡴࡀࠠࡼࡿࠪᕣ"), str(err))
def bstack111111lll1_opy_(bstack111111l1l1_opy_):
    if bstack111111l1l1_opy_ in store[bstack11l1l1l_opy_ (u"ࠩࡦࡹࡷࡸࡥ࡯ࡶࡢ࡬ࡴࡵ࡫ࡠࡷࡸ࡭ࡩ࠭ᕤ")]:
        store[bstack11l1l1l_opy_ (u"ࠪࡧࡺࡸࡲࡦࡰࡷࡣ࡭ࡵ࡯࡬ࡡࡸࡹ࡮ࡪࠧᕥ")].remove(bstack111111l1l1_opy_)
def bstack11111l1111_opy_(bstack1111111lll_opy_):
    store[bstack11l1l1l_opy_ (u"ࠫࡨࡻࡲࡳࡧࡱࡸࡤࡺࡥࡴࡶࡢࡹࡺ࡯ࡤࠨᕦ")] = bstack1111111lll_opy_
    threading.current_thread().current_test_uuid = bstack1111111lll_opy_
@bstack1l11l11l_opy_.bstack1111l11ll1_opy_
def bstack111111l11l_opy_(item, call, report):
    global bstack11111l1ll1_opy_
    try:
        if report.when == bstack11l1l1l_opy_ (u"ࠬࡩࡡ࡭࡮ࠪᕧ"):
            bstack1l1l1lll11_opy_.reset()
        if report.when == bstack11l1l1l_opy_ (u"࠭ࡣࡢ࡮࡯ࠫᕨ"):
            if bstack11111l1ll1_opy_ == bstack11l1l1l_opy_ (u"ࠧࡱࡻࡷࡩࡸࡺࠧᕩ"):
                _1l1ll11111_opy_[item.nodeid][bstack11l1l1l_opy_ (u"ࠨࡨ࡬ࡲ࡮ࡹࡨࡦࡦࡢࡥࡹ࠭ᕪ")] = bstack11ll1lll11_opy_(report.stop)
                bstack1111l1111l_opy_(item, _1l1ll11111_opy_[item.nodeid], bstack11l1l1l_opy_ (u"ࠩࡗࡩࡸࡺࡒࡶࡰࡉ࡭ࡳ࡯ࡳࡩࡧࡧࠫᕫ"), report, call)
                store[bstack11l1l1l_opy_ (u"ࠪࡧࡺࡸࡲࡦࡰࡷࡣࡹ࡫ࡳࡵࡡࡸࡹ࡮ࡪࠧᕬ")] = None
            elif bstack11111l1ll1_opy_ == bstack11l1l1l_opy_ (u"ࠦࡵࡿࡴࡦࡵࡷ࠱ࡧࡪࡤࠣᕭ"):
                bstack1l11l1l1ll_opy_ = _1l1ll11111_opy_[item.nodeid][bstack11l1l1l_opy_ (u"ࠬࡺࡥࡴࡶࡢࡨࡦࡺࡡࠨᕮ")]
                bstack1l11l1l1ll_opy_.set(hooks=_1l1ll11111_opy_[item.nodeid].get(bstack11l1l1l_opy_ (u"࠭ࡨࡰࡱ࡮ࡷࠬᕯ"), []))
                exception, bstack1l1l1l1l11_opy_ = None, None
                if call.excinfo:
                    exception = call.excinfo.value
                    bstack1l1l1l1l11_opy_ = [call.excinfo.exconly(), report.longreprtext]
                bstack1l11l1l1ll_opy_.stop(time=bstack11ll1lll11_opy_(report.stop), result=Result(result=report.outcome, exception=exception, bstack1l1l1l1l11_opy_=bstack1l1l1l1l11_opy_))
                bstack1l11l11l_opy_.bstack1l11l1ll1l_opy_(bstack11l1l1l_opy_ (u"ࠧࡕࡧࡶࡸࡗࡻ࡮ࡇ࡫ࡱ࡭ࡸ࡮ࡥࡥࠩᕰ"), _1l1ll11111_opy_[item.nodeid][bstack11l1l1l_opy_ (u"ࠨࡶࡨࡷࡹࡥࡤࡢࡶࡤࠫᕱ")])
        elif report.when in [bstack11l1l1l_opy_ (u"ࠩࡶࡩࡹࡻࡰࠨᕲ"), bstack11l1l1l_opy_ (u"ࠪࡸࡪࡧࡲࡥࡱࡺࡲࠬᕳ")]:
            bstack1l1l111l1l_opy_ = item.nodeid + bstack11l1l1l_opy_ (u"ࠫ࠲࠭ᕴ") + report.when
            if report.skipped:
                hook_type = bstack11l1l1l_opy_ (u"ࠬࡈࡅࡇࡑࡕࡉࡤࡋࡁࡄࡊࠪᕵ") if report.when == bstack11l1l1l_opy_ (u"࠭ࡳࡦࡶࡸࡴࠬᕶ") else bstack11l1l1l_opy_ (u"ࠧࡂࡈࡗࡉࡗࡥࡅࡂࡅࡋࠫᕷ")
                _1l1ll11111_opy_[bstack1l1l111l1l_opy_] = {
                    bstack11l1l1l_opy_ (u"ࠨࡷࡸ࡭ࡩ࠭ᕸ"): uuid4().__str__(),
                    bstack11l1l1l_opy_ (u"ࠩࡶࡸࡦࡸࡴࡦࡦࡢࡥࡹ࠭ᕹ"): datetime.datetime.utcfromtimestamp(report.start).isoformat() + bstack11l1l1l_opy_ (u"ࠪ࡞ࠬᕺ"),
                    bstack11l1l1l_opy_ (u"ࠫ࡭ࡵ࡯࡬ࡡࡷࡽࡵ࡫ࠧᕻ"): hook_type
                }
            _1l1ll11111_opy_[bstack1l1l111l1l_opy_][bstack11l1l1l_opy_ (u"ࠬ࡬ࡩ࡯࡫ࡶ࡬ࡪࡪ࡟ࡢࡶࠪᕼ")] = datetime.datetime.utcfromtimestamp(report.stop).isoformat() + bstack11l1l1l_opy_ (u"࡚࠭ࠨᕽ")
            bstack111111lll1_opy_(_1l1ll11111_opy_[bstack1l1l111l1l_opy_][bstack11l1l1l_opy_ (u"ࠧࡶࡷ࡬ࡨࠬᕾ")])
            bstack11111ll111_opy_(item, _1l1ll11111_opy_[bstack1l1l111l1l_opy_], bstack11l1l1l_opy_ (u"ࠨࡊࡲࡳࡰࡘࡵ࡯ࡈ࡬ࡲ࡮ࡹࡨࡦࡦࠪᕿ"), report, call)
            if report.when == bstack11l1l1l_opy_ (u"ࠩࡶࡩࡹࡻࡰࠨᖀ"):
                if report.outcome == bstack11l1l1l_opy_ (u"ࠪࡪࡦ࡯࡬ࡦࡦࠪᖁ"):
                    bstack1l1l111ll1_opy_ = {
                        bstack11l1l1l_opy_ (u"ࠫࡺࡻࡩࡥࠩᖂ"): uuid4().__str__(),
                        bstack11l1l1l_opy_ (u"ࠬࡹࡴࡢࡴࡷࡩࡩࡥࡡࡵࠩᖃ"): bstack1llllll11l_opy_(),
                        bstack11l1l1l_opy_ (u"࠭ࡦࡪࡰ࡬ࡷ࡭࡫ࡤࡠࡣࡷࠫᖄ"): bstack1llllll11l_opy_()
                    }
                    _1l1ll11111_opy_[item.nodeid] = {**_1l1ll11111_opy_[item.nodeid], **bstack1l1l111ll1_opy_}
                    bstack1111l1111l_opy_(item, _1l1ll11111_opy_[item.nodeid], bstack11l1l1l_opy_ (u"ࠧࡕࡧࡶࡸࡗࡻ࡮ࡔࡶࡤࡶࡹ࡫ࡤࠨᖅ"))
                    bstack1111l1111l_opy_(item, _1l1ll11111_opy_[item.nodeid], bstack11l1l1l_opy_ (u"ࠨࡖࡨࡷࡹࡘࡵ࡯ࡈ࡬ࡲ࡮ࡹࡨࡦࡦࠪᖆ"), report, call)
    except Exception as err:
        print(bstack11l1l1l_opy_ (u"ࠩࡈࡼࡨ࡫ࡰࡵ࡫ࡲࡲࠥ࡯࡮ࠡࡪࡤࡲࡩࡲࡥࡠࡱ࠴࠵ࡾࡥࡴࡦࡵࡷࡣࡪࡼࡥ࡯ࡶ࠽ࠤࢀࢃࠧᖇ"), str(err))
def bstack11111lllll_opy_(test, bstack1l1l111ll1_opy_, result=None, call=None, bstack1llll1111l_opy_=None, outcome=None):
    file_path = os.path.relpath(test.fspath.strpath, start=os.getcwd())
    bstack1l11l1l1ll_opy_ = {
        bstack11l1l1l_opy_ (u"ࠪࡹࡺ࡯ࡤࠨᖈ"): bstack1l1l111ll1_opy_[bstack11l1l1l_opy_ (u"ࠫࡺࡻࡩࡥࠩᖉ")],
        bstack11l1l1l_opy_ (u"ࠬࡺࡹࡱࡧࠪᖊ"): bstack11l1l1l_opy_ (u"࠭ࡴࡦࡵࡷࠫᖋ"),
        bstack11l1l1l_opy_ (u"ࠧ࡯ࡣࡰࡩࠬᖌ"): test.name,
        bstack11l1l1l_opy_ (u"ࠨࡤࡲࡨࡾ࠭ᖍ"): {
            bstack11l1l1l_opy_ (u"ࠩ࡯ࡥࡳ࡭ࠧᖎ"): bstack11l1l1l_opy_ (u"ࠪࡴࡾࡺࡨࡰࡰࠪᖏ"),
            bstack11l1l1l_opy_ (u"ࠫࡨࡵࡤࡦࠩᖐ"): inspect.getsource(test.obj)
        },
        bstack11l1l1l_opy_ (u"ࠬ࡯ࡤࡦࡰࡷ࡭࡫࡯ࡥࡳࠩᖑ"): test.name,
        bstack11l1l1l_opy_ (u"࠭ࡳࡤࡱࡳࡩࠬᖒ"): test.name,
        bstack11l1l1l_opy_ (u"ࠧࡴࡥࡲࡴࡪࡹࠧᖓ"): bstack1l11l11l_opy_.bstack1l1l1l1lll_opy_(test),
        bstack11l1l1l_opy_ (u"ࠨࡨ࡬ࡰࡪࡥ࡮ࡢ࡯ࡨࠫᖔ"): file_path,
        bstack11l1l1l_opy_ (u"ࠩ࡯ࡳࡨࡧࡴࡪࡱࡱࠫᖕ"): file_path,
        bstack11l1l1l_opy_ (u"ࠪࡶࡪࡹࡵ࡭ࡶࠪᖖ"): bstack11l1l1l_opy_ (u"ࠫࡵ࡫࡮ࡥ࡫ࡱ࡫ࠬᖗ"),
        bstack11l1l1l_opy_ (u"ࠬࡼࡣࡠࡨ࡬ࡰࡪࡶࡡࡵࡪࠪᖘ"): file_path,
        bstack11l1l1l_opy_ (u"࠭ࡳࡵࡣࡵࡸࡪࡪ࡟ࡢࡶࠪᖙ"): bstack1l1l111ll1_opy_[bstack11l1l1l_opy_ (u"ࠧࡴࡶࡤࡶࡹ࡫ࡤࡠࡣࡷࠫᖚ")],
        bstack11l1l1l_opy_ (u"ࠨࡨࡵࡥࡲ࡫ࡷࡰࡴ࡮ࠫᖛ"): bstack11l1l1l_opy_ (u"ࠩࡓࡽࡹ࡫ࡳࡵࠩᖜ"),
        bstack11l1l1l_opy_ (u"ࠪࡧࡺࡹࡴࡰ࡯ࡕࡩࡷࡻ࡮ࡑࡣࡵࡥࡲ࠭ᖝ"): {
            bstack11l1l1l_opy_ (u"ࠫࡷ࡫ࡲࡶࡰࡢࡲࡦࡳࡥࠨᖞ"): test.nodeid
        },
        bstack11l1l1l_opy_ (u"ࠬࡺࡡࡨࡵࠪᖟ"): bstack11ll1lll1l_opy_(test.own_markers)
    }
    if bstack1llll1111l_opy_ in [bstack11l1l1l_opy_ (u"࠭ࡔࡦࡵࡷࡖࡺࡴࡓ࡬࡫ࡳࡴࡪࡪࠧᖠ"), bstack11l1l1l_opy_ (u"ࠧࡕࡧࡶࡸࡗࡻ࡮ࡇ࡫ࡱ࡭ࡸ࡮ࡥࡥࠩᖡ")]:
        bstack1l11l1l1ll_opy_[bstack11l1l1l_opy_ (u"ࠨ࡯ࡨࡸࡦ࠭ᖢ")] = {
            bstack11l1l1l_opy_ (u"ࠩࡩ࡭ࡽࡺࡵࡳࡧࡶࠫᖣ"): bstack1l1l111ll1_opy_.get(bstack11l1l1l_opy_ (u"ࠪࡪ࡮ࡾࡴࡶࡴࡨࡷࠬᖤ"), [])
        }
    if bstack1llll1111l_opy_ == bstack11l1l1l_opy_ (u"࡙ࠫ࡫ࡳࡵࡔࡸࡲࡘࡱࡩࡱࡲࡨࡨࠬᖥ"):
        bstack1l11l1l1ll_opy_[bstack11l1l1l_opy_ (u"ࠬࡸࡥࡴࡷ࡯ࡸࠬᖦ")] = bstack11l1l1l_opy_ (u"࠭ࡳ࡬࡫ࡳࡴࡪࡪࠧᖧ")
        bstack1l11l1l1ll_opy_[bstack11l1l1l_opy_ (u"ࠧࡩࡱࡲ࡯ࡸ࠭ᖨ")] = bstack1l1l111ll1_opy_[bstack11l1l1l_opy_ (u"ࠨࡪࡲࡳࡰࡹࠧᖩ")]
        bstack1l11l1l1ll_opy_[bstack11l1l1l_opy_ (u"ࠩࡩ࡭ࡳ࡯ࡳࡩࡧࡧࡣࡦࡺࠧᖪ")] = bstack1l1l111ll1_opy_[bstack11l1l1l_opy_ (u"ࠪࡪ࡮ࡴࡩࡴࡪࡨࡨࡤࡧࡴࠨᖫ")]
    if result:
        bstack1l11l1l1ll_opy_[bstack11l1l1l_opy_ (u"ࠫࡷ࡫ࡳࡶ࡮ࡷࠫᖬ")] = result.outcome
        bstack1l11l1l1ll_opy_[bstack11l1l1l_opy_ (u"ࠬࡪࡵࡳࡣࡷ࡭ࡴࡴ࡟ࡪࡰࡢࡱࡸ࠭ᖭ")] = result.duration * 1000
        bstack1l11l1l1ll_opy_[bstack11l1l1l_opy_ (u"࠭ࡦࡪࡰ࡬ࡷ࡭࡫ࡤࡠࡣࡷࠫᖮ")] = bstack1l1l111ll1_opy_[bstack11l1l1l_opy_ (u"ࠧࡧ࡫ࡱ࡭ࡸ࡮ࡥࡥࡡࡤࡸࠬᖯ")]
        if result.failed:
            bstack1l11l1l1ll_opy_[bstack11l1l1l_opy_ (u"ࠨࡨࡤ࡭ࡱࡻࡲࡦࡡࡷࡽࡵ࡫ࠧᖰ")] = bstack1l11l11l_opy_.bstack1l111ll11l_opy_(call.excinfo.typename)
            bstack1l11l1l1ll_opy_[bstack11l1l1l_opy_ (u"ࠩࡩࡥ࡮ࡲࡵࡳࡧࠪᖱ")] = bstack1l11l11l_opy_.bstack1111ll11ll_opy_(call.excinfo, result)
        bstack1l11l1l1ll_opy_[bstack11l1l1l_opy_ (u"ࠪ࡬ࡴࡵ࡫ࡴࠩᖲ")] = bstack1l1l111ll1_opy_[bstack11l1l1l_opy_ (u"ࠫ࡭ࡵ࡯࡬ࡵࠪᖳ")]
    if outcome:
        bstack1l11l1l1ll_opy_[bstack11l1l1l_opy_ (u"ࠬࡸࡥࡴࡷ࡯ࡸࠬᖴ")] = bstack11ll1111ll_opy_(outcome)
        bstack1l11l1l1ll_opy_[bstack11l1l1l_opy_ (u"࠭ࡤࡶࡴࡤࡸ࡮ࡵ࡮ࡠ࡫ࡱࡣࡲࡹࠧᖵ")] = 0
        bstack1l11l1l1ll_opy_[bstack11l1l1l_opy_ (u"ࠧࡧ࡫ࡱ࡭ࡸ࡮ࡥࡥࡡࡤࡸࠬᖶ")] = bstack1l1l111ll1_opy_[bstack11l1l1l_opy_ (u"ࠨࡨ࡬ࡲ࡮ࡹࡨࡦࡦࡢࡥࡹ࠭ᖷ")]
        if bstack1l11l1l1ll_opy_[bstack11l1l1l_opy_ (u"ࠩࡵࡩࡸࡻ࡬ࡵࠩᖸ")] == bstack11l1l1l_opy_ (u"ࠪࡪࡦ࡯࡬ࡦࡦࠪᖹ"):
            bstack1l11l1l1ll_opy_[bstack11l1l1l_opy_ (u"ࠫ࡫ࡧࡩ࡭ࡷࡵࡩࡤࡺࡹࡱࡧࠪᖺ")] = bstack11l1l1l_opy_ (u"࡛ࠬ࡮ࡩࡣࡱࡨࡱ࡫ࡤࡆࡴࡵࡳࡷ࠭ᖻ")  # bstack111111ll11_opy_
            bstack1l11l1l1ll_opy_[bstack11l1l1l_opy_ (u"࠭ࡦࡢ࡫࡯ࡹࡷ࡫ࠧᖼ")] = [{bstack11l1l1l_opy_ (u"ࠧࡣࡣࡦ࡯ࡹࡸࡡࡤࡧࠪᖽ"): [bstack11l1l1l_opy_ (u"ࠨࡵࡲࡱࡪࠦࡥࡳࡴࡲࡶࠬᖾ")]}]
        bstack1l11l1l1ll_opy_[bstack11l1l1l_opy_ (u"ࠩ࡫ࡳࡴࡱࡳࠨᖿ")] = bstack1l1l111ll1_opy_[bstack11l1l1l_opy_ (u"ࠪ࡬ࡴࡵ࡫ࡴࠩᗀ")]
    return bstack1l11l1l1ll_opy_
def bstack11111ll1ll_opy_(test, bstack1l11ll11l1_opy_, bstack1llll1111l_opy_, result, call, outcome, bstack111111llll_opy_):
    file_path = os.path.relpath(test.fspath.strpath, start=os.getcwd())
    hook_type = bstack1l11ll11l1_opy_[bstack11l1l1l_opy_ (u"ࠫ࡭ࡵ࡯࡬ࡡࡷࡽࡵ࡫ࠧᗁ")]
    hook_name = bstack1l11ll11l1_opy_[bstack11l1l1l_opy_ (u"ࠬ࡮࡯ࡰ࡭ࡢࡲࡦࡳࡥࠨᗂ")]
    hook_data = {
        bstack11l1l1l_opy_ (u"࠭ࡵࡶ࡫ࡧࠫᗃ"): bstack1l11ll11l1_opy_[bstack11l1l1l_opy_ (u"ࠧࡶࡷ࡬ࡨࠬᗄ")],
        bstack11l1l1l_opy_ (u"ࠨࡶࡼࡴࡪ࠭ᗅ"): bstack11l1l1l_opy_ (u"ࠩ࡫ࡳࡴࡱࠧᗆ"),
        bstack11l1l1l_opy_ (u"ࠪࡲࡦࡳࡥࠨᗇ"): bstack11l1l1l_opy_ (u"ࠫࢀࢃࠧᗈ").format(bstack111ll11lll_opy_(hook_name)),
        bstack11l1l1l_opy_ (u"ࠬࡨ࡯ࡥࡻࠪᗉ"): {
            bstack11l1l1l_opy_ (u"࠭࡬ࡢࡰࡪࠫᗊ"): bstack11l1l1l_opy_ (u"ࠧࡱࡻࡷ࡬ࡴࡴࠧᗋ"),
            bstack11l1l1l_opy_ (u"ࠨࡥࡲࡨࡪ࠭ᗌ"): None
        },
        bstack11l1l1l_opy_ (u"ࠩࡶࡧࡴࡶࡥࠨᗍ"): test.name,
        bstack11l1l1l_opy_ (u"ࠪࡷࡨࡵࡰࡦࡵࠪᗎ"): bstack1l11l11l_opy_.bstack1l1l1l1lll_opy_(test, hook_name),
        bstack11l1l1l_opy_ (u"ࠫ࡫࡯࡬ࡦࡡࡱࡥࡲ࡫ࠧᗏ"): file_path,
        bstack11l1l1l_opy_ (u"ࠬࡲ࡯ࡤࡣࡷ࡭ࡴࡴࠧᗐ"): file_path,
        bstack11l1l1l_opy_ (u"࠭ࡲࡦࡵࡸࡰࡹ࠭ᗑ"): bstack11l1l1l_opy_ (u"ࠧࡱࡧࡱࡨ࡮ࡴࡧࠨᗒ"),
        bstack11l1l1l_opy_ (u"ࠨࡸࡦࡣ࡫࡯࡬ࡦࡲࡤࡸ࡭࠭ᗓ"): file_path,
        bstack11l1l1l_opy_ (u"ࠩࡶࡸࡦࡸࡴࡦࡦࡢࡥࡹ࠭ᗔ"): bstack1l11ll11l1_opy_[bstack11l1l1l_opy_ (u"ࠪࡷࡹࡧࡲࡵࡧࡧࡣࡦࡺࠧᗕ")],
        bstack11l1l1l_opy_ (u"ࠫ࡫ࡸࡡ࡮ࡧࡺࡳࡷࡱࠧᗖ"): bstack11l1l1l_opy_ (u"ࠬࡖࡹࡵࡧࡶࡸ࠲ࡩࡵࡤࡷࡰࡦࡪࡸࠧᗗ") if bstack11111l1ll1_opy_ == bstack11l1l1l_opy_ (u"࠭ࡰࡺࡶࡨࡷࡹ࠳ࡢࡥࡦࠪᗘ") else bstack11l1l1l_opy_ (u"ࠧࡑࡻࡷࡩࡸࡺࠧᗙ"),
        bstack11l1l1l_opy_ (u"ࠨࡪࡲࡳࡰࡥࡴࡺࡲࡨࠫᗚ"): hook_type
    }
    bstack11111l1l1l_opy_ = bstack1l11llll11_opy_(_1l1ll11111_opy_.get(test.nodeid, None))
    if bstack11111l1l1l_opy_:
        hook_data[bstack11l1l1l_opy_ (u"ࠩࡷࡩࡸࡺ࡟ࡳࡷࡱࡣ࡮ࡪࠧᗛ")] = bstack11111l1l1l_opy_
    if result:
        hook_data[bstack11l1l1l_opy_ (u"ࠪࡶࡪࡹࡵ࡭ࡶࠪᗜ")] = result.outcome
        hook_data[bstack11l1l1l_opy_ (u"ࠫࡩࡻࡲࡢࡶ࡬ࡳࡳࡥࡩ࡯ࡡࡰࡷࠬᗝ")] = result.duration * 1000
        hook_data[bstack11l1l1l_opy_ (u"ࠬ࡬ࡩ࡯࡫ࡶ࡬ࡪࡪ࡟ࡢࡶࠪᗞ")] = bstack1l11ll11l1_opy_[bstack11l1l1l_opy_ (u"࠭ࡦࡪࡰ࡬ࡷ࡭࡫ࡤࡠࡣࡷࠫᗟ")]
        if result.failed:
            hook_data[bstack11l1l1l_opy_ (u"ࠧࡧࡣ࡬ࡰࡺࡸࡥࡠࡶࡼࡴࡪ࠭ᗠ")] = bstack1l11l11l_opy_.bstack1l111ll11l_opy_(call.excinfo.typename)
            hook_data[bstack11l1l1l_opy_ (u"ࠨࡨࡤ࡭ࡱࡻࡲࡦࠩᗡ")] = bstack1l11l11l_opy_.bstack1111ll11ll_opy_(call.excinfo, result)
    if outcome:
        hook_data[bstack11l1l1l_opy_ (u"ࠩࡵࡩࡸࡻ࡬ࡵࠩᗢ")] = bstack11ll1111ll_opy_(outcome)
        hook_data[bstack11l1l1l_opy_ (u"ࠪࡨࡺࡸࡡࡵ࡫ࡲࡲࡤ࡯࡮ࡠ࡯ࡶࠫᗣ")] = 100
        hook_data[bstack11l1l1l_opy_ (u"ࠫ࡫࡯࡮ࡪࡵ࡫ࡩࡩࡥࡡࡵࠩᗤ")] = bstack1l11ll11l1_opy_[bstack11l1l1l_opy_ (u"ࠬ࡬ࡩ࡯࡫ࡶ࡬ࡪࡪ࡟ࡢࡶࠪᗥ")]
        if hook_data[bstack11l1l1l_opy_ (u"࠭ࡲࡦࡵࡸࡰࡹ࠭ᗦ")] == bstack11l1l1l_opy_ (u"ࠧࡧࡣ࡬ࡰࡪࡪࠧᗧ"):
            hook_data[bstack11l1l1l_opy_ (u"ࠨࡨࡤ࡭ࡱࡻࡲࡦࡡࡷࡽࡵ࡫ࠧᗨ")] = bstack11l1l1l_opy_ (u"ࠩࡘࡲ࡭ࡧ࡮ࡥ࡮ࡨࡨࡊࡸࡲࡰࡴࠪᗩ")  # bstack111111ll11_opy_
            hook_data[bstack11l1l1l_opy_ (u"ࠪࡪࡦ࡯࡬ࡶࡴࡨࠫᗪ")] = [{bstack11l1l1l_opy_ (u"ࠫࡧࡧࡣ࡬ࡶࡵࡥࡨ࡫ࠧᗫ"): [bstack11l1l1l_opy_ (u"ࠬࡹ࡯࡮ࡧࠣࡩࡷࡸ࡯ࡳࠩᗬ")]}]
    if bstack111111llll_opy_:
        hook_data[bstack11l1l1l_opy_ (u"࠭ࡲࡦࡵࡸࡰࡹ࠭ᗭ")] = bstack111111llll_opy_.result
        hook_data[bstack11l1l1l_opy_ (u"ࠧࡥࡷࡵࡥࡹ࡯࡯࡯ࡡ࡬ࡲࡤࡳࡳࠨᗮ")] = bstack11ll1ll1l1_opy_(bstack1l11ll11l1_opy_[bstack11l1l1l_opy_ (u"ࠨࡵࡷࡥࡷࡺࡥࡥࡡࡤࡸࠬᗯ")], bstack1l11ll11l1_opy_[bstack11l1l1l_opy_ (u"ࠩࡩ࡭ࡳ࡯ࡳࡩࡧࡧࡣࡦࡺࠧᗰ")])
        hook_data[bstack11l1l1l_opy_ (u"ࠪࡪ࡮ࡴࡩࡴࡪࡨࡨࡤࡧࡴࠨᗱ")] = bstack1l11ll11l1_opy_[bstack11l1l1l_opy_ (u"ࠫ࡫࡯࡮ࡪࡵ࡫ࡩࡩࡥࡡࡵࠩᗲ")]
        if hook_data[bstack11l1l1l_opy_ (u"ࠬࡸࡥࡴࡷ࡯ࡸࠬᗳ")] == bstack11l1l1l_opy_ (u"࠭ࡦࡢ࡫࡯ࡩࡩ࠭ᗴ"):
            hook_data[bstack11l1l1l_opy_ (u"ࠧࡧࡣ࡬ࡰࡺࡸࡥࡠࡶࡼࡴࡪ࠭ᗵ")] = bstack1l11l11l_opy_.bstack1l111ll11l_opy_(bstack111111llll_opy_.exception_type)
            hook_data[bstack11l1l1l_opy_ (u"ࠨࡨࡤ࡭ࡱࡻࡲࡦࠩᗶ")] = [{bstack11l1l1l_opy_ (u"ࠩࡥࡥࡨࡱࡴࡳࡣࡦࡩࠬᗷ"): bstack11ll1l1l11_opy_(bstack111111llll_opy_.exception)}]
    return hook_data
def bstack1111l1111l_opy_(test, bstack1l1l111ll1_opy_, bstack1llll1111l_opy_, result=None, call=None, outcome=None):
    bstack1l11l1l1ll_opy_ = bstack11111lllll_opy_(test, bstack1l1l111ll1_opy_, result, call, bstack1llll1111l_opy_, outcome)
    driver = getattr(test, bstack11l1l1l_opy_ (u"ࠪࡣࡩࡸࡩࡷࡧࡵࠫᗸ"), None)
    if bstack1llll1111l_opy_ == bstack11l1l1l_opy_ (u"࡙ࠫ࡫ࡳࡵࡔࡸࡲࡘࡺࡡࡳࡶࡨࡨࠬᗹ") and driver:
        bstack1l11l1l1ll_opy_[bstack11l1l1l_opy_ (u"ࠬ࡯࡮ࡵࡧࡪࡶࡦࡺࡩࡰࡰࡶࠫᗺ")] = bstack1l11l11l_opy_.bstack1l1l1ll1l1_opy_(driver)
    if bstack1llll1111l_opy_ == bstack11l1l1l_opy_ (u"࠭ࡔࡦࡵࡷࡖࡺࡴࡓ࡬࡫ࡳࡴࡪࡪࠧᗻ"):
        bstack1llll1111l_opy_ = bstack11l1l1l_opy_ (u"ࠧࡕࡧࡶࡸࡗࡻ࡮ࡇ࡫ࡱ࡭ࡸ࡮ࡥࡥࠩᗼ")
    bstack1l1l1ll111_opy_ = {
        bstack11l1l1l_opy_ (u"ࠨࡧࡹࡩࡳࡺ࡟ࡵࡻࡳࡩࠬᗽ"): bstack1llll1111l_opy_,
        bstack11l1l1l_opy_ (u"ࠩࡷࡩࡸࡺ࡟ࡳࡷࡱࠫᗾ"): bstack1l11l1l1ll_opy_
    }
    bstack1l11l11l_opy_.bstack1l1l1l1111_opy_(bstack1l1l1ll111_opy_)
def bstack11111ll111_opy_(test, bstack1l1l111ll1_opy_, bstack1llll1111l_opy_, result=None, call=None, outcome=None, bstack111111llll_opy_=None):
    hook_data = bstack11111ll1ll_opy_(test, bstack1l1l111ll1_opy_, bstack1llll1111l_opy_, result, call, outcome, bstack111111llll_opy_)
    bstack1l1l1ll111_opy_ = {
        bstack11l1l1l_opy_ (u"ࠪࡩࡻ࡫࡮ࡵࡡࡷࡽࡵ࡫ࠧᗿ"): bstack1llll1111l_opy_,
        bstack11l1l1l_opy_ (u"ࠫ࡭ࡵ࡯࡬ࡡࡵࡹࡳ࠭ᘀ"): hook_data
    }
    bstack1l11l11l_opy_.bstack1l1l1l1111_opy_(bstack1l1l1ll111_opy_)
def bstack1l11llll11_opy_(bstack1l1l111ll1_opy_):
    if not bstack1l1l111ll1_opy_:
        return None
    if bstack1l1l111ll1_opy_.get(bstack11l1l1l_opy_ (u"ࠬࡺࡥࡴࡶࡢࡨࡦࡺࡡࠨᘁ"), None):
        return getattr(bstack1l1l111ll1_opy_[bstack11l1l1l_opy_ (u"࠭ࡴࡦࡵࡷࡣࡩࡧࡴࡢࠩᘂ")], bstack11l1l1l_opy_ (u"ࠧࡶࡷ࡬ࡨࠬᘃ"), None)
    return bstack1l1l111ll1_opy_.get(bstack11l1l1l_opy_ (u"ࠨࡷࡸ࡭ࡩ࠭ᘄ"), None)
@pytest.fixture(autouse=True)
def second_fixture(caplog, request):
    yield
    try:
        if not bstack1l11l11l_opy_.on():
            return
        places = [bstack11l1l1l_opy_ (u"ࠩࡶࡩࡹࡻࡰࠨᘅ"), bstack11l1l1l_opy_ (u"ࠪࡧࡦࡲ࡬ࠨᘆ"), bstack11l1l1l_opy_ (u"ࠫࡹ࡫ࡡࡳࡦࡲࡻࡳ࠭ᘇ")]
        bstack1l1l1l1l1l_opy_ = []
        for bstack11111ll11l_opy_ in places:
            records = caplog.get_records(bstack11111ll11l_opy_)
            bstack111111ll1l_opy_ = bstack11l1l1l_opy_ (u"ࠬࡺࡥࡴࡶࡢࡶࡺࡴ࡟ࡶࡷ࡬ࡨࠬᘈ") if bstack11111ll11l_opy_ == bstack11l1l1l_opy_ (u"࠭ࡣࡢ࡮࡯ࠫᘉ") else bstack11l1l1l_opy_ (u"ࠧࡩࡱࡲ࡯ࡤࡸࡵ࡯ࡡࡸࡹ࡮ࡪࠧᘊ")
            bstack111111l1ll_opy_ = request.node.nodeid + (bstack11l1l1l_opy_ (u"ࠨࠩᘋ") if bstack11111ll11l_opy_ == bstack11l1l1l_opy_ (u"ࠩࡦࡥࡱࡲࠧᘌ") else bstack11l1l1l_opy_ (u"ࠪ࠱ࠬᘍ") + bstack11111ll11l_opy_)
            bstack1111111lll_opy_ = bstack1l11llll11_opy_(_1l1ll11111_opy_.get(bstack111111l1ll_opy_, None))
            if not bstack1111111lll_opy_:
                continue
            for record in records:
                if bstack11lll1l11l_opy_(record.message):
                    continue
                bstack1l1l1l1l1l_opy_.append({
                    bstack11l1l1l_opy_ (u"ࠫࡹ࡯࡭ࡦࡵࡷࡥࡲࡶࠧᘎ"): datetime.datetime.utcfromtimestamp(record.created).isoformat() + bstack11l1l1l_opy_ (u"ࠬࡠࠧᘏ"),
                    bstack11l1l1l_opy_ (u"࠭࡬ࡦࡸࡨࡰࠬᘐ"): record.levelname,
                    bstack11l1l1l_opy_ (u"ࠧ࡮ࡧࡶࡷࡦ࡭ࡥࠨᘑ"): record.message,
                    bstack111111ll1l_opy_: bstack1111111lll_opy_
                })
        if len(bstack1l1l1l1l1l_opy_) > 0:
            bstack1l11l11l_opy_.bstack1l11llll1l_opy_(bstack1l1l1l1l1l_opy_)
    except Exception as err:
        print(bstack11l1l1l_opy_ (u"ࠨࡇࡻࡧࡪࡶࡴࡪࡱࡱࠤ࡮ࡴࠠࡴࡧࡦࡳࡳࡪ࡟ࡧ࡫ࡻࡸࡺࡸࡥ࠻ࠢࡾࢁࠬᘒ"), str(err))
def bstack1ll11l111_opy_(driver_command, response):
    if driver_command == bstack11l1l1l_opy_ (u"ࠩࡶࡧࡷ࡫ࡥ࡯ࡵ࡫ࡳࡹ࠭ᘓ"):
        bstack1l11l11l_opy_.bstack111l1ll1l_opy_({
            bstack11l1l1l_opy_ (u"ࠪ࡭ࡲࡧࡧࡦࠩᘔ"): response[bstack11l1l1l_opy_ (u"ࠫࡻࡧ࡬ࡶࡧࠪᘕ")],
            bstack11l1l1l_opy_ (u"ࠬࡺࡥࡴࡶࡢࡶࡺࡴ࡟ࡶࡷ࡬ࡨࠬᘖ"): store[bstack11l1l1l_opy_ (u"࠭ࡣࡶࡴࡵࡩࡳࡺ࡟ࡵࡧࡶࡸࡤࡻࡵࡪࡦࠪᘗ")]
        })
def bstack111111ll1_opy_():
    global bstack11111lll1_opy_
    bstack1l11l11l_opy_.bstack1l1l1l11l1_opy_()
    for driver in bstack11111lll1_opy_:
        try:
            driver.quit()
        except Exception as e:
            pass
def bstack1lll1lll1_opy_(self, *args, **kwargs):
    bstack11l1ll11l_opy_ = bstack1l111l1l_opy_(self, *args, **kwargs)
    bstack1l11l11l_opy_.bstack1ll11llll1_opy_(self)
    return bstack11l1ll11l_opy_
def bstack1l1l1l111_opy_(framework_name):
    global bstack1lllll1ll1_opy_
    global bstack1l1l1llll_opy_
    bstack1lllll1ll1_opy_ = framework_name
    logger.info(bstack1lll1111_opy_.format(bstack1lllll1ll1_opy_.split(bstack11l1l1l_opy_ (u"ࠧ࠮ࠩᘘ"))[0]))
    try:
        from selenium import webdriver
        from selenium.webdriver.common.service import Service
        from selenium.webdriver.remote.webdriver import WebDriver
        if bstack11lll1l1ll_opy_():
            Service.start = bstack1l1l11l1_opy_
            Service.stop = bstack1l1l1ll1l_opy_
            webdriver.Remote.__init__ = bstack1ll1ll1l11_opy_
            webdriver.Remote.get = bstack11l1ll11_opy_
            if not isinstance(os.getenv(bstack11l1l1l_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡑ࡛ࡗࡉࡘ࡚࡟ࡑࡃࡕࡅࡑࡒࡅࡍࠩᘙ")), str):
                return
            WebDriver.close = bstack11lll1ll1_opy_
            WebDriver.quit = bstack1111l1l1_opy_
            WebDriver.getAccessibilityResults = getAccessibilityResults
            WebDriver.bstack1lll1l1lll_opy_ = getAccessibilityResults
            WebDriver.getAccessibilityResultsSummary = getAccessibilityResultsSummary
            WebDriver.bstack1l1ll11lll_opy_ = getAccessibilityResultsSummary
        if not bstack11lll1l1ll_opy_() and bstack1l11l11l_opy_.on():
            webdriver.Remote.__init__ = bstack1lll1lll1_opy_
        bstack1l1l1llll_opy_ = True
    except Exception as e:
        pass
    bstack1lll111ll_opy_()
    if os.environ.get(bstack11l1l1l_opy_ (u"ࠩࡖࡉࡑࡋࡎࡊࡗࡐࡣࡔࡘ࡟ࡑࡎࡄ࡝࡜ࡘࡉࡈࡊࡗࡣࡎࡔࡓࡕࡃࡏࡐࡊࡊࠧᘚ")):
        bstack1l1l1llll_opy_ = eval(os.environ.get(bstack11l1l1l_opy_ (u"ࠪࡗࡊࡒࡅࡏࡋࡘࡑࡤࡕࡒࡠࡒࡏࡅ࡞࡝ࡒࡊࡉࡋࡘࡤࡏࡎࡔࡖࡄࡐࡑࡋࡄࠨᘛ")))
    if not bstack1l1l1llll_opy_:
        bstack1111l111l_opy_(bstack11l1l1l_opy_ (u"ࠦࡕࡧࡣ࡬ࡣࡪࡩࡸࠦ࡮ࡰࡶࠣ࡭ࡳࡹࡴࡢ࡮࡯ࡩࡩࠨᘜ"), bstack11lll11ll_opy_)
    if bstack1ll1111ll1_opy_():
        try:
            from selenium.webdriver.remote.remote_connection import RemoteConnection
            RemoteConnection._get_proxy_url = bstack1lll11lll1_opy_
        except Exception as e:
            logger.error(bstack1ll11l11ll_opy_.format(str(e)))
    if bstack11l1l1l_opy_ (u"ࠬࡶࡹࡵࡧࡶࡸࠬᘝ") in str(framework_name).lower():
        if not bstack11lll1l1ll_opy_():
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
def bstack1111l1l1_opy_(self):
    global bstack1lllll1ll1_opy_
    global bstack1l1ll1ll1_opy_
    global bstack1l1l1l1ll_opy_
    try:
        if bstack11l1l1l_opy_ (u"࠭ࡰࡺࡶࡨࡷࡹ࠭ᘞ") in bstack1lllll1ll1_opy_ and self.session_id != None and bstack1111l11l_opy_(threading.current_thread(), bstack11l1l1l_opy_ (u"ࠧࡵࡧࡶࡸࡘࡺࡡࡵࡷࡶࠫᘟ"), bstack11l1l1l_opy_ (u"ࠨࠩᘠ")) != bstack11l1l1l_opy_ (u"ࠩࡶ࡯࡮ࡶࡰࡦࡦࠪᘡ"):
            bstack1l1l111l_opy_ = bstack11l1l1l_opy_ (u"ࠪࡴࡦࡹࡳࡦࡦࠪᘢ") if len(threading.current_thread().bstackTestErrorMessages) == 0 else bstack11l1l1l_opy_ (u"ࠫ࡫ࡧࡩ࡭ࡧࡧࠫᘣ")
            bstack1l1ll111l_opy_ = bstack1l1lll1l1l_opy_(bstack11l1l1l_opy_ (u"ࠬࡹࡥࡵࡕࡨࡷࡸ࡯࡯࡯ࡕࡷࡥࡹࡻࡳࠨᘤ"), bstack11l1l1l_opy_ (u"࠭ࠧᘥ"), bstack1l1l111l_opy_, bstack11l1l1l_opy_ (u"ࠧ࠭ࠢࠪᘦ").join(
                threading.current_thread().bstackTestErrorMessages), bstack11l1l1l_opy_ (u"ࠨࠩᘧ"), bstack11l1l1l_opy_ (u"ࠩࠪᘨ"))
            bstack1ll111111_opy_(logger, True)
            if self != None:
                self.execute_script(bstack1l1ll111l_opy_)
        threading.current_thread().testStatus = bstack11l1l1l_opy_ (u"ࠪࠫᘩ")
    except Exception as e:
        logger.debug(bstack11l1l1l_opy_ (u"ࠦࡊࡸࡲࡰࡴࠣࡻ࡭࡯࡬ࡦࠢࡰࡥࡷࡱࡩ࡯ࡩࠣࡷࡹࡧࡴࡶࡵ࠽ࠤࠧᘪ") + str(e))
    bstack1l1l1l1ll_opy_(self)
    self.session_id = None
def bstack1ll1ll1l11_opy_(self, command_executor,
             desired_capabilities=None, browser_profile=None, proxy=None,
             keep_alive=True, file_detector=None, options=None):
    global CONFIG
    global bstack1l1ll1ll1_opy_
    global bstack1ll11l1ll1_opy_
    global bstack1l1l1l1l1_opy_
    global bstack1lllll1ll1_opy_
    global bstack1l111l1l_opy_
    global bstack11111lll1_opy_
    global bstack1l1ll1ll1l_opy_
    global bstack11l111111_opy_
    global bstack11111l11l1_opy_
    global bstack11l11l1l_opy_
    CONFIG[bstack11l1l1l_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࡗࡉࡑࠧᘫ")] = str(bstack1lllll1ll1_opy_) + str(__version__)
    command_executor = bstack1llllllll_opy_(bstack1l1ll1ll1l_opy_)
    logger.debug(bstack111111l11_opy_.format(command_executor))
    proxy = bstack1ll1ll11l1_opy_(CONFIG, proxy)
    bstack1111l11l1_opy_ = 0
    try:
        if bstack1l1l1l1l1_opy_ is True:
            bstack1111l11l1_opy_ = int(os.environ.get(bstack11l1l1l_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤࡖࡌࡂࡖࡉࡓࡗࡓ࡟ࡊࡐࡇࡉ࡝࠭ᘬ")))
    except:
        bstack1111l11l1_opy_ = 0
    bstack1ll1lll11_opy_ = bstack1l1ll1llll_opy_(CONFIG, bstack1111l11l1_opy_)
    logger.debug(bstack1l11l1ll1_opy_.format(str(bstack1ll1lll11_opy_)))
    bstack11l11l1l_opy_ = CONFIG.get(bstack11l1l1l_opy_ (u"ࠧࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࡵࠪᘭ"))[bstack1111l11l1_opy_]
    if bstack11l1l1l_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱࡌࡰࡥࡤࡰࠬᘮ") in CONFIG and CONFIG[bstack11l1l1l_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࡍࡱࡦࡥࡱ࠭ᘯ")]:
        bstack11l11l11l_opy_(bstack1ll1lll11_opy_, bstack11l111111_opy_)
    if desired_capabilities:
        bstack1l11llll1_opy_ = bstack1l1ll1l1ll_opy_(desired_capabilities)
        bstack1l11llll1_opy_[bstack11l1l1l_opy_ (u"ࠪࡹࡸ࡫ࡗ࠴ࡅࠪᘰ")] = bstack1ll111l111_opy_(CONFIG)
        bstack1111l11ll_opy_ = bstack1l1ll1llll_opy_(bstack1l11llll1_opy_)
        if bstack1111l11ll_opy_:
            bstack1ll1lll11_opy_ = update(bstack1111l11ll_opy_, bstack1ll1lll11_opy_)
        desired_capabilities = None
    if options:
        bstack1ll1l1ll_opy_(options, bstack1ll1lll11_opy_)
    if not options:
        options = bstack1ll11lllll_opy_(bstack1ll1lll11_opy_)
    if bstack1111ll111_opy_.bstack1lll11l11_opy_(CONFIG, bstack1111l11l1_opy_) and bstack1111ll111_opy_.bstack1l11lll1_opy_(bstack1ll1lll11_opy_, options):
        bstack11111l11l1_opy_ = True
        bstack1111ll111_opy_.set_capabilities(bstack1ll1lll11_opy_, CONFIG)
    if proxy and bstack1llll1lll_opy_() >= version.parse(bstack11l1l1l_opy_ (u"ࠫ࠹࠴࠱࠱࠰࠳ࠫᘱ")):
        options.proxy(proxy)
    if options and bstack1llll1lll_opy_() >= version.parse(bstack11l1l1l_opy_ (u"ࠬ࠹࠮࠹࠰࠳ࠫᘲ")):
        desired_capabilities = None
    if (
            not options and not desired_capabilities
    ) or (
            bstack1llll1lll_opy_() < version.parse(bstack11l1l1l_opy_ (u"࠭࠳࠯࠺࠱࠴ࠬᘳ")) and not desired_capabilities
    ):
        desired_capabilities = {}
        desired_capabilities.update(bstack1ll1lll11_opy_)
    logger.info(bstack1ll11ll1_opy_)
    if bstack1llll1lll_opy_() >= version.parse(bstack11l1l1l_opy_ (u"ࠧ࠵࠰࠴࠴࠳࠶ࠧᘴ")):
        bstack1l111l1l_opy_(self, command_executor=command_executor,
                  options=options, keep_alive=keep_alive, file_detector=file_detector)
    elif bstack1llll1lll_opy_() >= version.parse(bstack11l1l1l_opy_ (u"ࠨ࠵࠱࠼࠳࠶ࠧᘵ")):
        bstack1l111l1l_opy_(self, command_executor=command_executor,
                  desired_capabilities=desired_capabilities, options=options,
                  browser_profile=browser_profile, proxy=proxy,
                  keep_alive=keep_alive, file_detector=file_detector)
    elif bstack1llll1lll_opy_() >= version.parse(bstack11l1l1l_opy_ (u"ࠩ࠵࠲࠺࠹࠮࠱ࠩᘶ")):
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
        bstack1l1llll11l_opy_ = bstack11l1l1l_opy_ (u"ࠪࠫᘷ")
        if bstack1llll1lll_opy_() >= version.parse(bstack11l1l1l_opy_ (u"ࠫ࠹࠴࠰࠯࠲ࡥ࠵ࠬᘸ")):
            bstack1l1llll11l_opy_ = self.caps.get(bstack11l1l1l_opy_ (u"ࠧࡵࡰࡵ࡫ࡰࡥࡱࡎࡵࡣࡗࡵࡰࠧᘹ"))
        else:
            bstack1l1llll11l_opy_ = self.capabilities.get(bstack11l1l1l_opy_ (u"ࠨ࡯ࡱࡶ࡬ࡱࡦࡲࡈࡶࡤࡘࡶࡱࠨᘺ"))
        if bstack1l1llll11l_opy_:
            bstack1llll1111_opy_(bstack1l1llll11l_opy_)
            if bstack1llll1lll_opy_() <= version.parse(bstack11l1l1l_opy_ (u"ࠧ࠴࠰࠴࠷࠳࠶ࠧᘻ")):
                self.command_executor._url = bstack11l1l1l_opy_ (u"ࠣࡪࡷࡸࡵࡀ࠯࠰ࠤᘼ") + bstack1l1ll1ll1l_opy_ + bstack11l1l1l_opy_ (u"ࠤ࠽࠼࠵࠵ࡷࡥ࠱࡫ࡹࡧࠨᘽ")
            else:
                self.command_executor._url = bstack11l1l1l_opy_ (u"ࠥ࡬ࡹࡺࡰࡴ࠼࠲࠳ࠧᘾ") + bstack1l1llll11l_opy_ + bstack11l1l1l_opy_ (u"ࠦ࠴ࡽࡤ࠰ࡪࡸࡦࠧᘿ")
            logger.debug(bstack11ll1lll_opy_.format(bstack1l1llll11l_opy_))
        else:
            logger.debug(bstack1l1l1ll11_opy_.format(bstack11l1l1l_opy_ (u"ࠧࡕࡰࡵ࡫ࡰࡥࡱࠦࡈࡶࡤࠣࡲࡴࡺࠠࡧࡱࡸࡲࡩࠨᙀ")))
    except Exception as e:
        logger.debug(bstack1l1l1ll11_opy_.format(e))
    bstack1l1ll1ll1_opy_ = self.session_id
    if bstack11l1l1l_opy_ (u"࠭ࡰࡺࡶࡨࡷࡹ࠭ᙁ") in bstack1lllll1ll1_opy_:
        threading.current_thread().bstackSessionId = self.session_id
        threading.current_thread().bstackSessionDriver = self
        threading.current_thread().bstackTestErrorMessages = []
        bstack1l11l11l_opy_.bstack1ll11llll1_opy_(self)
    bstack11111lll1_opy_.append(self)
    if bstack11l1l1l_opy_ (u"ࠧࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࡵࠪᙂ") in CONFIG and bstack11l1l1l_opy_ (u"ࠨࡵࡨࡷࡸ࡯࡯࡯ࡐࡤࡱࡪ࠭ᙃ") in CONFIG[bstack11l1l1l_opy_ (u"ࠩࡳࡰࡦࡺࡦࡰࡴࡰࡷࠬᙄ")][bstack1111l11l1_opy_]:
        bstack1ll11l1ll1_opy_ = CONFIG[bstack11l1l1l_opy_ (u"ࠪࡴࡱࡧࡴࡧࡱࡵࡱࡸ࠭ᙅ")][bstack1111l11l1_opy_][bstack11l1l1l_opy_ (u"ࠫࡸ࡫ࡳࡴ࡫ࡲࡲࡓࡧ࡭ࡦࠩᙆ")]
    logger.debug(bstack1lll11ll_opy_.format(bstack1l1ll1ll1_opy_))
def bstack11l1ll11_opy_(self, url):
    global bstack1l11l1l11_opy_
    global CONFIG
    try:
        bstack1l1lll1lll_opy_(url, CONFIG, logger)
    except Exception as err:
        logger.debug(bstack111lll11_opy_.format(str(err)))
    try:
        bstack1l11l1l11_opy_(self, url)
    except Exception as e:
        try:
            bstack1ll1111lll_opy_ = str(e)
            if any(err_msg in bstack1ll1111lll_opy_ for err_msg in bstack1ll1ll11ll_opy_):
                bstack1l1lll1lll_opy_(url, CONFIG, logger, True)
        except Exception as err:
            logger.debug(bstack111lll11_opy_.format(str(err)))
        raise e
def bstack111lllll_opy_(item, when):
    global bstack11ll1l1ll_opy_
    try:
        bstack11ll1l1ll_opy_(item, when)
    except Exception as e:
        pass
def bstack1ll1l111l_opy_(item, call, rep):
    global bstack1l1111l1_opy_
    global bstack11111lll1_opy_
    name = bstack11l1l1l_opy_ (u"ࠬ࠭ᙇ")
    try:
        if rep.when == bstack11l1l1l_opy_ (u"࠭ࡣࡢ࡮࡯ࠫᙈ"):
            bstack1l1ll1ll1_opy_ = threading.current_thread().bstackSessionId
            bstack11111l1l11_opy_ = item.config.getoption(bstack11l1l1l_opy_ (u"ࠧࡴ࡭࡬ࡴࡘ࡫ࡳࡴ࡫ࡲࡲࡓࡧ࡭ࡦࠩᙉ"))
            try:
                if (str(bstack11111l1l11_opy_).lower() != bstack11l1l1l_opy_ (u"ࠨࡶࡵࡹࡪ࠭ᙊ")):
                    name = str(rep.nodeid)
                    bstack1l1ll111l_opy_ = bstack1l1lll1l1l_opy_(bstack11l1l1l_opy_ (u"ࠩࡶࡩࡹ࡙ࡥࡴࡵ࡬ࡳࡳࡔࡡ࡮ࡧࠪᙋ"), name, bstack11l1l1l_opy_ (u"ࠪࠫᙌ"), bstack11l1l1l_opy_ (u"ࠫࠬᙍ"), bstack11l1l1l_opy_ (u"ࠬ࠭ᙎ"), bstack11l1l1l_opy_ (u"࠭ࠧᙏ"))
                    os.environ[bstack11l1l1l_opy_ (u"ࠧࡑ࡛ࡗࡉࡘ࡚࡟ࡕࡇࡖࡘࡤࡔࡁࡎࡇࠪᙐ")] = name
                    for driver in bstack11111lll1_opy_:
                        if bstack1l1ll1ll1_opy_ == driver.session_id:
                            driver.execute_script(bstack1l1ll111l_opy_)
            except Exception as e:
                logger.debug(bstack11l1l1l_opy_ (u"ࠨࡇࡵࡶࡴࡸࠠࡪࡰࠣࡷࡪࡺࡴࡪࡰࡪࠤࡸ࡫ࡳࡴ࡫ࡲࡲࡓࡧ࡭ࡦࠢࡩࡳࡷࠦࡰࡺࡶࡨࡷࡹ࠳ࡢࡥࡦࠣࡷࡪࡹࡳࡪࡱࡱ࠾ࠥࢁࡽࠨᙑ").format(str(e)))
            try:
                bstack1lll11l1ll_opy_(rep.outcome.lower())
                if rep.outcome.lower() != bstack11l1l1l_opy_ (u"ࠩࡶ࡯࡮ࡶࡰࡦࡦࠪᙒ"):
                    status = bstack11l1l1l_opy_ (u"ࠪࡪࡦ࡯࡬ࡦࡦࠪᙓ") if rep.outcome.lower() == bstack11l1l1l_opy_ (u"ࠫ࡫ࡧࡩ࡭ࡧࡧࠫᙔ") else bstack11l1l1l_opy_ (u"ࠬࡶࡡࡴࡵࡨࡨࠬᙕ")
                    reason = bstack11l1l1l_opy_ (u"࠭ࠧᙖ")
                    if status == bstack11l1l1l_opy_ (u"ࠧࡧࡣ࡬ࡰࡪࡪࠧᙗ"):
                        reason = rep.longrepr.reprcrash.message
                        if (not threading.current_thread().bstackTestErrorMessages):
                            threading.current_thread().bstackTestErrorMessages = []
                        threading.current_thread().bstackTestErrorMessages.append(reason)
                    level = bstack11l1l1l_opy_ (u"ࠨ࡫ࡱࡪࡴ࠭ᙘ") if status == bstack11l1l1l_opy_ (u"ࠩࡳࡥࡸࡹࡥࡥࠩᙙ") else bstack11l1l1l_opy_ (u"ࠪࡩࡷࡸ࡯ࡳࠩᙚ")
                    data = name + bstack11l1l1l_opy_ (u"ࠫࠥࡶࡡࡴࡵࡨࡨࠦ࠭ᙛ") if status == bstack11l1l1l_opy_ (u"ࠬࡶࡡࡴࡵࡨࡨࠬᙜ") else name + bstack11l1l1l_opy_ (u"࠭ࠠࡧࡣ࡬ࡰࡪࡪࠡࠡࠩᙝ") + reason
                    bstack111lll1l1_opy_ = bstack1l1lll1l1l_opy_(bstack11l1l1l_opy_ (u"ࠧࡢࡰࡱࡳࡹࡧࡴࡦࠩᙞ"), bstack11l1l1l_opy_ (u"ࠨࠩᙟ"), bstack11l1l1l_opy_ (u"ࠩࠪᙠ"), bstack11l1l1l_opy_ (u"ࠪࠫᙡ"), level, data)
                    for driver in bstack11111lll1_opy_:
                        if bstack1l1ll1ll1_opy_ == driver.session_id:
                            driver.execute_script(bstack111lll1l1_opy_)
            except Exception as e:
                logger.debug(bstack11l1l1l_opy_ (u"ࠫࡊࡸࡲࡰࡴࠣ࡭ࡳࠦࡳࡦࡶࡷ࡭ࡳ࡭ࠠࡴࡧࡶࡷ࡮ࡵ࡮ࠡࡥࡲࡲࡹ࡫ࡸࡵࠢࡩࡳࡷࠦࡰࡺࡶࡨࡷࡹ࠳ࡢࡥࡦࠣࡷࡪࡹࡳࡪࡱࡱ࠾ࠥࢁࡽࠨᙢ").format(str(e)))
    except Exception as e:
        logger.debug(bstack11l1l1l_opy_ (u"ࠬࡋࡲࡳࡱࡵࠤ࡮ࡴࠠࡨࡧࡷࡸ࡮ࡴࡧࠡࡵࡷࡥࡹ࡫ࠠࡪࡰࠣࡴࡾࡺࡥࡴࡶ࠰ࡦࡩࡪࠠࡵࡧࡶࡸࠥࡹࡴࡢࡶࡸࡷ࠿ࠦࡻࡾࠩᙣ").format(str(e)))
    bstack1l1111l1_opy_(item, call, rep)
notset = Notset()
def bstack1l1ll11l_opy_(self, name: str, default=notset, skip: bool = False):
    global bstack1l1l11l1l_opy_
    if str(name).lower() == bstack11l1l1l_opy_ (u"࠭ࡤࡳ࡫ࡹࡩࡷ࠭ᙤ"):
        return bstack11l1l1l_opy_ (u"ࠢࡃࡴࡲࡻࡸ࡫ࡲࡔࡶࡤࡧࡰࠨᙥ")
    else:
        return bstack1l1l11l1l_opy_(self, name, default, skip)
def bstack1lll11lll1_opy_(self):
    global CONFIG
    global bstack11llll11_opy_
    try:
        proxy = bstack1ll1111l_opy_(CONFIG)
        if proxy:
            if proxy.endswith(bstack11l1l1l_opy_ (u"ࠨ࠰ࡳࡥࡨ࠭ᙦ")):
                proxies = bstack1111l1l1l_opy_(proxy, bstack1llllllll_opy_())
                if len(proxies) > 0:
                    protocol, bstack1lllllllll_opy_ = proxies.popitem()
                    if bstack11l1l1l_opy_ (u"ࠤ࠽࠳࠴ࠨᙧ") in bstack1lllllllll_opy_:
                        return bstack1lllllllll_opy_
                    else:
                        return bstack11l1l1l_opy_ (u"ࠥ࡬ࡹࡺࡰ࠻࠱࠲ࠦᙨ") + bstack1lllllllll_opy_
            else:
                return proxy
    except Exception as e:
        logger.error(bstack11l1l1l_opy_ (u"ࠦࡊࡸࡲࡰࡴࠣ࡭ࡳࠦࡳࡦࡶࡷ࡭ࡳ࡭ࠠࡱࡴࡲࡼࡾࠦࡵࡳ࡮ࠣ࠾ࠥࢁࡽࠣᙩ").format(str(e)))
    return bstack11llll11_opy_(self)
def bstack1ll1111ll1_opy_():
    return (bstack11l1l1l_opy_ (u"ࠬ࡮ࡴࡵࡲࡓࡶࡴࡾࡹࠨᙪ") in CONFIG or bstack11l1l1l_opy_ (u"࠭ࡨࡵࡶࡳࡷࡕࡸ࡯ࡹࡻࠪᙫ") in CONFIG) and bstack11l111lll_opy_() and bstack1llll1lll_opy_() >= version.parse(
        bstack1ll1l11ll1_opy_)
def bstack111ll1lll_opy_(self,
               executablePath=None,
               channel=None,
               args=None,
               ignoreDefaultArgs=None,
               handleSIGINT=None,
               handleSIGTERM=None,
               handleSIGHUP=None,
               timeout=None,
               env=None,
               headless=None,
               devtools=None,
               proxy=None,
               downloadsPath=None,
               slowMo=None,
               tracesDir=None,
               chromiumSandbox=None,
               firefoxUserPrefs=None
               ):
    global CONFIG
    global bstack1ll11l1ll1_opy_
    global bstack1l1l1l1l1_opy_
    global bstack1lllll1ll1_opy_
    CONFIG[bstack11l1l1l_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࡙ࡄࡌࠩᙬ")] = str(bstack1lllll1ll1_opy_) + str(__version__)
    bstack1111l11l1_opy_ = 0
    try:
        if bstack1l1l1l1l1_opy_ is True:
            bstack1111l11l1_opy_ = int(os.environ.get(bstack11l1l1l_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡑࡎࡄࡘࡋࡕࡒࡎࡡࡌࡒࡉࡋࡘࠨ᙭")))
    except:
        bstack1111l11l1_opy_ = 0
    CONFIG[bstack11l1l1l_opy_ (u"ࠤ࡬ࡷࡕࡲࡡࡺࡹࡵ࡭࡬࡮ࡴࠣ᙮")] = True
    bstack1ll1lll11_opy_ = bstack1l1ll1llll_opy_(CONFIG, bstack1111l11l1_opy_)
    logger.debug(bstack1l11l1ll1_opy_.format(str(bstack1ll1lll11_opy_)))
    if CONFIG.get(bstack11l1l1l_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࡎࡲࡧࡦࡲࠧᙯ")):
        bstack11l11l11l_opy_(bstack1ll1lll11_opy_, bstack11l111111_opy_)
    if bstack11l1l1l_opy_ (u"ࠫࡵࡲࡡࡵࡨࡲࡶࡲࡹࠧᙰ") in CONFIG and bstack11l1l1l_opy_ (u"ࠬࡹࡥࡴࡵ࡬ࡳࡳࡔࡡ࡮ࡧࠪᙱ") in CONFIG[bstack11l1l1l_opy_ (u"࠭ࡰ࡭ࡣࡷࡪࡴࡸ࡭ࡴࠩᙲ")][bstack1111l11l1_opy_]:
        bstack1ll11l1ll1_opy_ = CONFIG[bstack11l1l1l_opy_ (u"ࠧࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࡵࠪᙳ")][bstack1111l11l1_opy_][bstack11l1l1l_opy_ (u"ࠨࡵࡨࡷࡸ࡯࡯࡯ࡐࡤࡱࡪ࠭ᙴ")]
    import urllib
    import json
    bstack1ll111l1_opy_ = bstack11l1l1l_opy_ (u"ࠩࡺࡷࡸࡀ࠯࠰ࡥࡧࡴ࠳ࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮࠲ࡨࡵ࡭࠰ࡲ࡯ࡥࡾࡽࡲࡪࡩ࡫ࡸࡄࡩࡡࡱࡵࡀࠫᙵ") + urllib.parse.quote(json.dumps(bstack1ll1lll11_opy_))
    browser = self.connect(bstack1ll111l1_opy_)
    return browser
def bstack1lll111ll_opy_():
    global bstack1l1l1llll_opy_
    try:
        from playwright._impl._browser_type import BrowserType
        BrowserType.launch = bstack111ll1lll_opy_
        bstack1l1l1llll_opy_ = True
    except Exception as e:
        pass
def bstack111111l111_opy_():
    global CONFIG
    global bstack1lll1l111_opy_
    global bstack1l1ll1ll1l_opy_
    global bstack11l111111_opy_
    global bstack1l1l1l1l1_opy_
    CONFIG = json.loads(os.environ.get(bstack11l1l1l_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡆࡓࡓࡌࡉࡈࠩᙶ")))
    bstack1lll1l111_opy_ = eval(os.environ.get(bstack11l1l1l_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡍࡘࡥࡁࡑࡒࡢࡅ࡚࡚ࡏࡎࡃࡗࡉࠬᙷ")))
    bstack1l1ll1ll1l_opy_ = os.environ.get(bstack11l1l1l_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣࡍ࡛ࡂࡠࡗࡕࡐࠬᙸ"))
    bstack1ll1llll_opy_(CONFIG, bstack1lll1l111_opy_)
    bstack1111ll1l1_opy_()
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
    if (bstack11l1l1l_opy_ (u"࠭ࡨࡵࡶࡳࡔࡷࡵࡸࡺࠩᙹ") in CONFIG or bstack11l1l1l_opy_ (u"ࠧࡩࡶࡷࡴࡸࡖࡲࡰࡺࡼࠫᙺ") in CONFIG) and bstack11l111lll_opy_():
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
        logger.debug(bstack11l1l1l_opy_ (u"ࠨࡒ࡯ࡩࡦࡹࡥࠡ࡫ࡱࡷࡹࡧ࡬࡭ࠢࡳࡽࡹ࡫ࡳࡵ࠯ࡥࡨࡩࠦࡴࡰࠢࡵࡹࡳࠦࡰࡺࡶࡨࡷࡹ࠳ࡢࡥࡦࠣࡸࡪࡹࡴࡴࠩᙻ"))
    bstack11l111111_opy_ = CONFIG.get(bstack11l1l1l_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡖࡸࡦࡩ࡫ࡍࡱࡦࡥࡱࡕࡰࡵ࡫ࡲࡲࡸ࠭ᙼ"), {}).get(bstack11l1l1l_opy_ (u"ࠪࡰࡴࡩࡡ࡭ࡋࡧࡩࡳࡺࡩࡧ࡫ࡨࡶࠬᙽ"))
    bstack1l1l1l1l1_opy_ = True
    bstack1l1l1l111_opy_(bstack1ll111llll_opy_)
if (bstack11ll11lll1_opy_()):
    bstack111111l111_opy_()
@bstack1l11ll1ll1_opy_(class_method=False)
def bstack1111l111l1_opy_(hook_name, event, bstack11111ll1l1_opy_=None):
    if hook_name not in [bstack11l1l1l_opy_ (u"ࠫࡸ࡫ࡴࡶࡲࡢࡪࡺࡴࡣࡵ࡫ࡲࡲࠬᙾ"), bstack11l1l1l_opy_ (u"ࠬࡺࡥࡢࡴࡧࡳࡼࡴ࡟ࡧࡷࡱࡧࡹ࡯࡯࡯ࠩᙿ"), bstack11l1l1l_opy_ (u"࠭ࡳࡦࡶࡸࡴࡤࡳ࡯ࡥࡷ࡯ࡩࠬ "), bstack11l1l1l_opy_ (u"ࠧࡵࡧࡤࡶࡩࡵࡷ࡯ࡡࡰࡳࡩࡻ࡬ࡦࠩᚁ"), bstack11l1l1l_opy_ (u"ࠨࡵࡨࡸࡺࡶ࡟ࡤ࡮ࡤࡷࡸ࠭ᚂ"), bstack11l1l1l_opy_ (u"ࠩࡷࡩࡦࡸࡤࡰࡹࡱࡣࡨࡲࡡࡴࡵࠪᚃ"), bstack11l1l1l_opy_ (u"ࠪࡷࡪࡺࡵࡱࡡࡰࡩࡹ࡮࡯ࡥࠩᚄ"), bstack11l1l1l_opy_ (u"ࠫࡹ࡫ࡡࡳࡦࡲࡻࡳࡥ࡭ࡦࡶ࡫ࡳࡩ࠭ᚅ")]:
        return
    node = store[bstack11l1l1l_opy_ (u"ࠬࡩࡵࡳࡴࡨࡲࡹࡥࡴࡦࡵࡷࡣ࡮ࡺࡥ࡮ࠩᚆ")]
    if hook_name in [bstack11l1l1l_opy_ (u"࠭ࡳࡦࡶࡸࡴࡤࡳ࡯ࡥࡷ࡯ࡩࠬᚇ"), bstack11l1l1l_opy_ (u"ࠧࡵࡧࡤࡶࡩࡵࡷ࡯ࡡࡰࡳࡩࡻ࡬ࡦࠩᚈ")]:
        node = store[bstack11l1l1l_opy_ (u"ࠨࡥࡸࡶࡷ࡫࡮ࡵࡡࡰࡳࡩࡻ࡬ࡦࡡ࡬ࡸࡪࡳࠧᚉ")]
    elif hook_name in [bstack11l1l1l_opy_ (u"ࠩࡶࡩࡹࡻࡰࡠࡥ࡯ࡥࡸࡹࠧᚊ"), bstack11l1l1l_opy_ (u"ࠪࡸࡪࡧࡲࡥࡱࡺࡲࡤࡩ࡬ࡢࡵࡶࠫᚋ")]:
        node = store[bstack11l1l1l_opy_ (u"ࠫࡨࡻࡲࡳࡧࡱࡸࡤࡩ࡬ࡢࡵࡶࡣ࡮ࡺࡥ࡮ࠩᚌ")]
    if event == bstack11l1l1l_opy_ (u"ࠬࡨࡥࡧࡱࡵࡩࠬᚍ"):
        hook_type = bstack111ll1ll11_opy_(hook_name)
        uuid = uuid4().__str__()
        bstack1l11ll11l1_opy_ = {
            bstack11l1l1l_opy_ (u"࠭ࡵࡶ࡫ࡧࠫᚎ"): uuid,
            bstack11l1l1l_opy_ (u"ࠧࡴࡶࡤࡶࡹ࡫ࡤࡠࡣࡷࠫᚏ"): bstack1llllll11l_opy_(),
            bstack11l1l1l_opy_ (u"ࠨࡶࡼࡴࡪ࠭ᚐ"): bstack11l1l1l_opy_ (u"ࠩ࡫ࡳࡴࡱࠧᚑ"),
            bstack11l1l1l_opy_ (u"ࠪ࡬ࡴࡵ࡫ࡠࡶࡼࡴࡪ࠭ᚒ"): hook_type,
            bstack11l1l1l_opy_ (u"ࠫ࡭ࡵ࡯࡬ࡡࡱࡥࡲ࡫ࠧᚓ"): hook_name
        }
        store[bstack11l1l1l_opy_ (u"ࠬࡩࡵࡳࡴࡨࡲࡹࡥࡨࡰࡱ࡮ࡣࡺࡻࡩࡥࠩᚔ")].append(uuid)
        bstack1111l11111_opy_ = node.nodeid
        if hook_type == bstack11l1l1l_opy_ (u"࠭ࡂࡆࡈࡒࡖࡊࡥࡅࡂࡅࡋࠫᚕ"):
            if not _1l1ll11111_opy_.get(bstack1111l11111_opy_, None):
                _1l1ll11111_opy_[bstack1111l11111_opy_] = {bstack11l1l1l_opy_ (u"ࠧࡩࡱࡲ࡯ࡸ࠭ᚖ"): []}
            _1l1ll11111_opy_[bstack1111l11111_opy_][bstack11l1l1l_opy_ (u"ࠨࡪࡲࡳࡰࡹࠧᚗ")].append(bstack1l11ll11l1_opy_[bstack11l1l1l_opy_ (u"ࠩࡸࡹ࡮ࡪࠧᚘ")])
        _1l1ll11111_opy_[bstack1111l11111_opy_ + bstack11l1l1l_opy_ (u"ࠪ࠱ࠬᚙ") + hook_name] = bstack1l11ll11l1_opy_
        bstack11111ll111_opy_(node, bstack1l11ll11l1_opy_, bstack11l1l1l_opy_ (u"ࠫࡍࡵ࡯࡬ࡔࡸࡲࡘࡺࡡࡳࡶࡨࡨࠬᚚ"))
    elif event == bstack11l1l1l_opy_ (u"ࠬࡧࡦࡵࡧࡵࠫ᚛"):
        bstack1l1l111l1l_opy_ = node.nodeid + bstack11l1l1l_opy_ (u"࠭࠭ࠨ᚜") + hook_name
        _1l1ll11111_opy_[bstack1l1l111l1l_opy_][bstack11l1l1l_opy_ (u"ࠧࡧ࡫ࡱ࡭ࡸ࡮ࡥࡥࡡࡤࡸࠬ᚝")] = bstack1llllll11l_opy_()
        bstack111111lll1_opy_(_1l1ll11111_opy_[bstack1l1l111l1l_opy_][bstack11l1l1l_opy_ (u"ࠨࡷࡸ࡭ࡩ࠭᚞")])
        bstack11111ll111_opy_(node, _1l1ll11111_opy_[bstack1l1l111l1l_opy_], bstack11l1l1l_opy_ (u"ࠩࡋࡳࡴࡱࡒࡶࡰࡉ࡭ࡳ࡯ࡳࡩࡧࡧࠫ᚟"), bstack111111llll_opy_=bstack11111ll1l1_opy_)
def bstack1111l111ll_opy_():
    global bstack11111l1ll1_opy_
    if bstack11ll1111_opy_():
        bstack11111l1ll1_opy_ = bstack11l1l1l_opy_ (u"ࠪࡴࡾࡺࡥࡴࡶ࠰ࡦࡩࡪࠧᚠ")
    else:
        bstack11111l1ll1_opy_ = bstack11l1l1l_opy_ (u"ࠫࡵࡿࡴࡦࡵࡷࠫᚡ")
@bstack1l11l11l_opy_.bstack1111l11ll1_opy_
def bstack1111l11l11_opy_():
    bstack1111l111ll_opy_()
    if bstack11l111lll_opy_():
        bstack11lll111l_opy_(bstack1ll11l111_opy_)
    bstack11l1lll1ll_opy_ = bstack11l1ll11ll_opy_(bstack1111l111l1_opy_)
bstack1111l11l11_opy_()