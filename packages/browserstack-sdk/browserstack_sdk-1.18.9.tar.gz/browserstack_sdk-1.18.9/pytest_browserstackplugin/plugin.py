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
from browserstack_sdk.__init__ import (bstack1llll1l1ll_opy_, bstack1l1lll1111_opy_, update, bstack1lll11lll_opy_,
                                       bstack1l1ll1l111_opy_, bstack1ll11111_opy_, bstack11lll1ll1_opy_, bstack1111llll_opy_,
                                       bstack1ll1ll1l11_opy_, bstack1l1ll1l11l_opy_, bstack1l11lll1_opy_, bstack1lllll1l1_opy_,
                                       bstack1l1ll11lll_opy_, getAccessibilityResults, getAccessibilityResultsSummary)
from browserstack_sdk._version import __version__
from bstack_utils.capture import bstack1l11ll1lll_opy_
from bstack_utils.config import Config
from bstack_utils.constants import bstack1ll11ll11_opy_, bstack111111l1l_opy_, bstack11l1lll11_opy_, bstack11llllll1_opy_, \
    bstack1ll1ll1ll1_opy_
from bstack_utils.helper import bstack11111l11_opy_, bstack1l1l11lll_opy_, bstack11l1llllll_opy_, bstack1ll11111ll_opy_, \
    bstack11lll1l111_opy_, \
    bstack11ll11llll_opy_, bstack1lll1ll1l_opy_, bstack1ll1lll1_opy_, bstack11ll11l1l1_opy_, bstack1l11ll11_opy_, Notset, \
    bstack1ll1l111_opy_, bstack11ll11111l_opy_, bstack11lll1l1ll_opy_, Result, bstack11lll11l11_opy_, bstack11lll1l1l1_opy_, bstack1l1l1ll111_opy_, \
    bstack1ll11lll11_opy_, bstack1l1lll1l1_opy_, bstack111l1l1l1_opy_
from bstack_utils.bstack11l1l1ll11_opy_ import bstack11l1lll111_opy_
from bstack_utils.messages import bstack1l1l1l11l_opy_, bstack1ll1l1l111_opy_, bstack1llllll11_opy_, bstack11ll1l1l1_opy_, bstack1lll11ll1l_opy_, \
    bstack1ll1l1111l_opy_, bstack11l111lll_opy_, bstack111l1l1ll_opy_, bstack1ll1l1lll_opy_, bstack1ll1ll1l1_opy_, \
    bstack1ll1l1lll1_opy_, bstack1111l11l1_opy_
from bstack_utils.proxy import bstack1l111lll1_opy_, bstack111l1ll11_opy_
from bstack_utils.bstack11ll1ll1_opy_ import bstack111ll11l1l_opy_, bstack111ll111ll_opy_, bstack111ll1l1l1_opy_, bstack111l1llll1_opy_, \
    bstack111ll1l11l_opy_, bstack111ll11l11_opy_, bstack111ll11ll1_opy_, bstack111l1111_opy_, bstack111ll11111_opy_
from bstack_utils.bstack11l1ll111_opy_ import bstack1l1l111l_opy_
from bstack_utils.bstack1l11l11l1_opy_ import bstack1ll1lll1l_opy_, bstack1lllllll1_opy_, bstack1ll1111111_opy_, \
    bstack1111ll1l1_opy_, bstack1l1ll111l_opy_
from bstack_utils.bstack1l1l1l111l_opy_ import bstack1l1l111ll1_opy_
from bstack_utils.bstack1ll11ll1l1_opy_ import bstack11l1ll11_opy_
import bstack_utils.bstack1111lll1_opy_ as bstack1ll111l11_opy_
bstack1l11l11ll_opy_ = None
bstack1l11ll1ll_opy_ = None
bstack111l111l1_opy_ = None
bstack111l111ll_opy_ = None
bstack111l11111_opy_ = None
bstack1l11lllll_opy_ = None
bstack1llll1111l_opy_ = None
bstack1ll111ll11_opy_ = None
bstack11l111111_opy_ = None
bstack1l1lll11ll_opy_ = None
bstack111llllll_opy_ = None
bstack1l1l1l1ll_opy_ = None
bstack1lll11l111_opy_ = None
bstack11ll11ll1_opy_ = bstack11l1ll_opy_ (u"࠭ࠧᒲ")
CONFIG = {}
bstack1ll11ll111_opy_ = False
bstack1lll1l1l1_opy_ = bstack11l1ll_opy_ (u"ࠧࠨᒳ")
bstack1l1111ll_opy_ = bstack11l1ll_opy_ (u"ࠨࠩᒴ")
bstack1ll11l1ll1_opy_ = False
bstack11l1l1111_opy_ = []
bstack1l11llll1_opy_ = bstack111111l1l_opy_
bstack11111ll11l_opy_ = bstack11l1ll_opy_ (u"ࠩࡳࡽࡹ࡫ࡳࡵࠩᒵ")
bstack111111llll_opy_ = False
bstack11l1llll_opy_ = {}
logger = logging.getLogger(__name__)
logging.basicConfig(level=bstack1l11llll1_opy_,
                    format=bstack11l1ll_opy_ (u"ࠪࡠࡳࠫࠨࡢࡵࡦࡸ࡮ࡳࡥࠪࡵࠣ࡟ࠪ࠮࡮ࡢ࡯ࡨ࠭ࡸࡣ࡛ࠦࠪ࡯ࡩࡻ࡫࡬࡯ࡣࡰࡩ࠮ࡹ࡝ࠡ࠯ࠣࠩ࠭ࡳࡥࡴࡵࡤ࡫ࡪ࠯ࡳࠨᒶ"),
                    datefmt=bstack11l1ll_opy_ (u"ࠫࠪࡎ࠺ࠦࡏ࠽ࠩࡘ࠭ᒷ"),
                    stream=sys.stdout)
store = {
    bstack11l1ll_opy_ (u"ࠬࡩࡵࡳࡴࡨࡲࡹࡥࡨࡰࡱ࡮ࡣࡺࡻࡩࡥࠩᒸ"): []
}
def bstack1lll111l1_opy_():
    global CONFIG
    global bstack1l11llll1_opy_
    if bstack11l1ll_opy_ (u"࠭࡬ࡰࡩࡏࡩࡻ࡫࡬ࠨᒹ") in CONFIG:
        bstack1l11llll1_opy_ = bstack1ll11ll11_opy_[CONFIG[bstack11l1ll_opy_ (u"ࠧ࡭ࡱࡪࡐࡪࡼࡥ࡭ࠩᒺ")]]
        logging.getLogger().setLevel(bstack1l11llll1_opy_)
try:
    from playwright.sync_api import (
        BrowserContext,
        Page
    )
except:
    pass
import json
_1l1l111l11_opy_ = {}
current_test_uuid = None
def bstack1l1ll1l11_opy_(page, bstack1l1l1ll1l_opy_):
    try:
        page.evaluate(bstack11l1ll_opy_ (u"ࠣࡡࠣࡁࡃࠦࡻࡾࠤᒻ"),
                      bstack11l1ll_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࡠࡧࡻࡩࡨࡻࡴࡰࡴ࠽ࠤࢀࠨࡡࡤࡶ࡬ࡳࡳࠨ࠺ࠡࠤࡶࡩࡹ࡙ࡥࡴࡵ࡬ࡳࡳࡔࡡ࡮ࡧࠥ࠰ࠥࠨࡡࡳࡩࡸࡱࡪࡴࡴࡴࠤ࠽ࠤࢀࠨ࡮ࡢ࡯ࡨࠦ࠿࠭ᒼ") + json.dumps(
                          bstack1l1l1ll1l_opy_) + bstack11l1ll_opy_ (u"ࠥࢁࢂࠨᒽ"))
    except Exception as e:
        print(bstack11l1ll_opy_ (u"ࠦࡪࡾࡣࡦࡲࡷ࡭ࡴࡴࠠࡪࡰࠣࡴࡱࡧࡹࡸࡴ࡬࡫࡭ࡺࠠࡴࡧࡶࡷ࡮ࡵ࡮ࠡࡰࡤࡱࡪࠦࡻࡾࠤᒾ"), e)
def bstack11lllll1_opy_(page, message, level):
    try:
        page.evaluate(bstack11l1ll_opy_ (u"ࠧࡥࠠ࠾ࡀࠣࡿࢂࠨᒿ"), bstack11l1ll_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࡤ࡫ࡸࡦࡥࡸࡸࡴࡸ࠺ࠡࡽࠥࡥࡨࡺࡩࡰࡰࠥ࠾ࠥࠨࡡ࡯ࡰࡲࡸࡦࡺࡥࠣ࠮ࠣࠦࡦࡸࡧࡶ࡯ࡨࡲࡹࡹࠢ࠻ࠢࡾࠦࡩࡧࡴࡢࠤ࠽ࠫᓀ") + json.dumps(
            message) + bstack11l1ll_opy_ (u"ࠧ࠭ࠤ࡯ࡩࡻ࡫࡬ࠣ࠼ࠪᓁ") + json.dumps(level) + bstack11l1ll_opy_ (u"ࠨࡿࢀࠫᓂ"))
    except Exception as e:
        print(bstack11l1ll_opy_ (u"ࠤࡨࡼࡨ࡫ࡰࡵ࡫ࡲࡲࠥ࡯࡮ࠡࡲ࡯ࡥࡾࡽࡲࡪࡩ࡫ࡸࠥࡧ࡮࡯ࡱࡷࡥࡹ࡯࡯࡯ࠢࡾࢁࠧᓃ"), e)
def pytest_configure(config):
    bstack1ll1l11l1_opy_ = Config.get_instance()
    config.args = bstack11l1ll11_opy_.bstack1111l1l11l_opy_(config.args)
    bstack1ll1l11l1_opy_.bstack1l11111l1_opy_(bstack111l1l1l1_opy_(config.getoption(bstack11l1ll_opy_ (u"ࠪࡷࡰ࡯ࡰࡔࡧࡶࡷ࡮ࡵ࡮ࡔࡶࡤࡸࡺࡹࠧᓄ"))))
@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    bstack1111111ll1_opy_ = item.config.getoption(bstack11l1ll_opy_ (u"ࠫࡸࡱࡩࡱࡕࡨࡷࡸ࡯࡯࡯ࡐࡤࡱࡪ࠭ᓅ"))
    plugins = item.config.getoption(bstack11l1ll_opy_ (u"ࠧࡶ࡬ࡶࡩ࡬ࡲࡸࠨᓆ"))
    report = outcome.get_result()
    bstack11111lllll_opy_(item, call, report)
    if bstack11l1ll_opy_ (u"ࠨࡰࡺࡶࡨࡷࡹࡥࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࡵࡲࡵࡨ࡫ࡱࠦᓇ") not in plugins or bstack1l11ll11_opy_():
        return
    summary = []
    driver = getattr(item, bstack11l1ll_opy_ (u"ࠢࡠࡦࡵ࡭ࡻ࡫ࡲࠣᓈ"), None)
    page = getattr(item, bstack11l1ll_opy_ (u"ࠣࡡࡳࡥ࡬࡫ࠢᓉ"), None)
    try:
        if (driver == None):
            driver = threading.current_thread().bstackSessionDriver
    except:
        pass
    item._driver = driver
    if (driver is not None):
        bstack11111l1l11_opy_(item, report, summary, bstack1111111ll1_opy_)
    if (page is not None):
        bstack11111l11l1_opy_(item, report, summary, bstack1111111ll1_opy_)
def bstack11111l1l11_opy_(item, report, summary, bstack1111111ll1_opy_):
    if report.when == bstack11l1ll_opy_ (u"ࠩࡶࡩࡹࡻࡰࠨᓊ") and report.skipped:
        bstack111ll11111_opy_(report)
    if report.when in [bstack11l1ll_opy_ (u"ࠥࡷࡪࡺࡵࡱࠤᓋ"), bstack11l1ll_opy_ (u"ࠦࡹ࡫ࡡࡳࡦࡲࡻࡳࠨᓌ")]:
        return
    if not bstack11l1llllll_opy_():
        return
    try:
        if (str(bstack1111111ll1_opy_).lower() != bstack11l1ll_opy_ (u"ࠬࡺࡲࡶࡧࠪᓍ")):
            item._driver.execute_script(
                bstack11l1ll_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࡤ࡫ࡸࡦࡥࡸࡸࡴࡸ࠺ࠡࡽࠥࡥࡨࡺࡩࡰࡰࠥ࠾ࠥࠨࡳࡦࡶࡖࡩࡸࡹࡩࡰࡰࡑࡥࡲ࡫ࠢ࠭ࠢࠥࡥࡷ࡭ࡵ࡮ࡧࡱࡸࡸࠨ࠺ࠡࡽࠥࡲࡦࡳࡥࠣ࠼ࠣࠫᓎ") + json.dumps(
                    report.nodeid) + bstack11l1ll_opy_ (u"ࠧࡾࡿࠪᓏ"))
        os.environ[bstack11l1ll_opy_ (u"ࠨࡒ࡜ࡘࡊ࡙ࡔࡠࡖࡈࡗ࡙ࡥࡎࡂࡏࡈࠫᓐ")] = report.nodeid
    except Exception as e:
        summary.append(
            bstack11l1ll_opy_ (u"ࠤ࡚ࡅࡗࡔࡉࡏࡉ࠽ࠤࡋࡧࡩ࡭ࡧࡧࠤࡹࡵࠠ࡮ࡣࡵ࡯ࠥࡹࡥࡴࡵ࡬ࡳࡳࠦ࡮ࡢ࡯ࡨ࠾ࠥࢁ࠰ࡾࠤᓑ").format(e)
        )
    passed = report.passed or report.skipped or (report.failed and hasattr(report, bstack11l1ll_opy_ (u"ࠥࡻࡦࡹࡸࡧࡣ࡬ࡰࠧᓒ")))
    bstack111l1111l_opy_ = bstack11l1ll_opy_ (u"ࠦࠧᓓ")
    bstack111ll11111_opy_(report)
    if not passed:
        try:
            bstack111l1111l_opy_ = report.longrepr.reprcrash
        except Exception as e:
            summary.append(
                bstack11l1ll_opy_ (u"ࠧ࡝ࡁࡓࡐࡌࡒࡌࡀࠠࡇࡣ࡬ࡰࡪࡪࠠࡵࡱࠣࡨࡪࡺࡥࡳ࡯࡬ࡲࡪࠦࡦࡢ࡫࡯ࡹࡷ࡫ࠠࡳࡧࡤࡷࡴࡴ࠺ࠡࡽ࠳ࢁࠧᓔ").format(e)
            )
        try:
            if (threading.current_thread().bstackTestErrorMessages == None):
                threading.current_thread().bstackTestErrorMessages = []
        except Exception as e:
            threading.current_thread().bstackTestErrorMessages = []
        threading.current_thread().bstackTestErrorMessages.append(str(bstack111l1111l_opy_))
    if not report.skipped:
        passed = report.passed or (report.failed and hasattr(report, bstack11l1ll_opy_ (u"ࠨࡷࡢࡵࡻࡪࡦ࡯࡬ࠣᓕ")))
        bstack111l1111l_opy_ = bstack11l1ll_opy_ (u"ࠢࠣᓖ")
        if not passed:
            try:
                bstack111l1111l_opy_ = report.longrepr.reprcrash
            except Exception as e:
                summary.append(
                    bstack11l1ll_opy_ (u"࡙ࠣࡄࡖࡓࡏࡎࡈ࠼ࠣࡊࡦ࡯࡬ࡦࡦࠣࡸࡴࠦࡤࡦࡶࡨࡶࡲ࡯࡮ࡦࠢࡩࡥ࡮ࡲࡵࡳࡧࠣࡶࡪࡧࡳࡰࡰ࠽ࠤࢀ࠶ࡽࠣᓗ").format(e)
                )
            try:
                if (threading.current_thread().bstackTestErrorMessages == None):
                    threading.current_thread().bstackTestErrorMessages = []
            except Exception as e:
                threading.current_thread().bstackTestErrorMessages = []
            threading.current_thread().bstackTestErrorMessages.append(str(bstack111l1111l_opy_))
        try:
            if passed:
                item._driver.execute_script(
                    bstack11l1ll_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࡠࡧࡻࡩࡨࡻࡴࡰࡴ࠽ࠤࢀࡢࠊࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠣࡣࡦࡸ࡮ࡵ࡮ࠣ࠼ࠣࠦࡦࡴ࡮ࡰࡶࡤࡸࡪࠨࠬࠡ࡞ࠍࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠦࡦࡸࡧࡶ࡯ࡨࡲࡹࡹࠢ࠻ࠢࡾࡠࠏࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠥࡰࡪࡼࡥ࡭ࠤ࠽ࠤࠧ࡯࡮ࡧࡱࠥ࠰ࠥࡢࠊࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠧࡪࡡࡵࡣࠥ࠾ࠥ࠭ᓘ")
                    + json.dumps(bstack11l1ll_opy_ (u"ࠥࡴࡦࡹࡳࡦࡦࠤࠦᓙ"))
                    + bstack11l1ll_opy_ (u"ࠦࡡࠐࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࡽ࡝ࠌࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࢃࠢᓚ")
                )
            else:
                item._driver.execute_script(
                    bstack11l1ll_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࡣࡪࡾࡥࡤࡷࡷࡳࡷࡀࠠࡼ࡞ࠍࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠦࡦࡩࡴࡪࡱࡱࠦ࠿ࠦࠢࡢࡰࡱࡳࡹࡧࡴࡦࠤ࠯ࠤࡡࠐࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠢࡢࡴࡪࡹࡲ࡫࡮ࡵࡵࠥ࠾ࠥࢁ࡜ࠋࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠨ࡬ࡦࡸࡨࡰࠧࡀࠠࠣࡧࡵࡶࡴࡸࠢ࠭ࠢ࡟ࠎࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠤࡧࡥࡹࡧࠢ࠻ࠢࠪᓛ")
                    + json.dumps(str(bstack111l1111l_opy_))
                    + bstack11l1ll_opy_ (u"ࠨ࡜ࠋࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࡿ࡟ࠎࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࡾࠤᓜ")
                )
        except Exception as e:
            summary.append(bstack11l1ll_opy_ (u"ࠢࡘࡃࡕࡒࡎࡔࡇ࠻ࠢࡉࡥ࡮ࡲࡥࡥࠢࡷࡳࠥࡧ࡮࡯ࡱࡷࡥࡹ࡫࠺ࠡࡽ࠳ࢁࠧᓝ").format(e))
def bstack11111llll1_opy_(test_name, error_message):
    try:
        bstack111111l1ll_opy_ = []
        bstack11111111_opy_ = os.environ.get(bstack11l1ll_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡑࡎࡄࡘࡋࡕࡒࡎࡡࡌࡒࡉࡋࡘࠨᓞ"), bstack11l1ll_opy_ (u"ࠩ࠳ࠫᓟ"))
        bstack1l1111l1l_opy_ = {bstack11l1ll_opy_ (u"ࠪࡲࡦࡳࡥࠨᓠ"): test_name, bstack11l1ll_opy_ (u"ࠫࡪࡸࡲࡰࡴࠪᓡ"): error_message, bstack11l1ll_opy_ (u"ࠬ࡯࡮ࡥࡧࡻࠫᓢ"): bstack11111111_opy_}
        bstack111111l111_opy_ = os.path.join(tempfile.gettempdir(), bstack11l1ll_opy_ (u"࠭ࡰࡸࡡࡳࡽࡹ࡫ࡳࡵࡡࡨࡶࡷࡵࡲࡠ࡮࡬ࡷࡹ࠴ࡪࡴࡱࡱࠫᓣ"))
        if os.path.exists(bstack111111l111_opy_):
            with open(bstack111111l111_opy_) as f:
                bstack111111l1ll_opy_ = json.load(f)
        bstack111111l1ll_opy_.append(bstack1l1111l1l_opy_)
        with open(bstack111111l111_opy_, bstack11l1ll_opy_ (u"ࠧࡸࠩᓤ")) as f:
            json.dump(bstack111111l1ll_opy_, f)
    except Exception as e:
        logger.debug(bstack11l1ll_opy_ (u"ࠨࡇࡵࡶࡴࡸࠠࡪࡰࠣࡴࡪࡸࡳࡪࡵࡷ࡭ࡳ࡭ࠠࡱ࡮ࡤࡽࡼࡸࡩࡨࡪࡷࠤࡵࡿࡴࡦࡵࡷࠤࡪࡸࡲࡰࡴࡶ࠾ࠥ࠭ᓥ") + str(e))
def bstack11111l11l1_opy_(item, report, summary, bstack1111111ll1_opy_):
    if report.when in [bstack11l1ll_opy_ (u"ࠤࡶࡩࡹࡻࡰࠣᓦ"), bstack11l1ll_opy_ (u"ࠥࡸࡪࡧࡲࡥࡱࡺࡲࠧᓧ")]:
        return
    if (str(bstack1111111ll1_opy_).lower() != bstack11l1ll_opy_ (u"ࠫࡹࡸࡵࡦࠩᓨ")):
        bstack1l1ll1l11_opy_(item._page, report.nodeid)
    passed = report.passed or report.skipped or (report.failed and hasattr(report, bstack11l1ll_opy_ (u"ࠧࡽࡡࡴࡺࡩࡥ࡮ࡲࠢᓩ")))
    bstack111l1111l_opy_ = bstack11l1ll_opy_ (u"ࠨࠢᓪ")
    bstack111ll11111_opy_(report)
    if not report.skipped:
        if not passed:
            try:
                bstack111l1111l_opy_ = report.longrepr.reprcrash
            except Exception as e:
                summary.append(
                    bstack11l1ll_opy_ (u"ࠢࡘࡃࡕࡒࡎࡔࡇ࠻ࠢࡉࡥ࡮ࡲࡥࡥࠢࡷࡳࠥࡪࡥࡵࡧࡵࡱ࡮ࡴࡥࠡࡨࡤ࡭ࡱࡻࡲࡦࠢࡵࡩࡦࡹ࡯࡯࠼ࠣࡿ࠵ࢃࠢᓫ").format(e)
                )
        try:
            if passed:
                bstack1l1ll111l_opy_(getattr(item, bstack11l1ll_opy_ (u"ࠨࡡࡳࡥ࡬࡫ࠧᓬ"), None), bstack11l1ll_opy_ (u"ࠤࡳࡥࡸࡹࡥࡥࠤᓭ"))
            else:
                error_message = bstack11l1ll_opy_ (u"ࠪࠫᓮ")
                if bstack111l1111l_opy_:
                    bstack11lllll1_opy_(item._page, str(bstack111l1111l_opy_), bstack11l1ll_opy_ (u"ࠦࡪࡸࡲࡰࡴࠥᓯ"))
                    bstack1l1ll111l_opy_(getattr(item, bstack11l1ll_opy_ (u"ࠬࡥࡰࡢࡩࡨࠫᓰ"), None), bstack11l1ll_opy_ (u"ࠨࡦࡢ࡫࡯ࡩࡩࠨᓱ"), str(bstack111l1111l_opy_))
                    error_message = str(bstack111l1111l_opy_)
                else:
                    bstack1l1ll111l_opy_(getattr(item, bstack11l1ll_opy_ (u"ࠧࡠࡲࡤ࡫ࡪ࠭ᓲ"), None), bstack11l1ll_opy_ (u"ࠣࡨࡤ࡭ࡱ࡫ࡤࠣᓳ"))
                bstack11111llll1_opy_(report.nodeid, error_message)
        except Exception as e:
            summary.append(bstack11l1ll_opy_ (u"ࠤ࡚ࡅࡗࡔࡉࡏࡉ࠽ࠤࡋࡧࡩ࡭ࡧࡧࠤࡹࡵࠠࡶࡲࡧࡥࡹ࡫ࠠࡴࡧࡶࡷ࡮ࡵ࡮ࠡࡵࡷࡥࡹࡻࡳ࠻ࠢࡾ࠴ࢂࠨᓴ").format(e))
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
    parser.addoption(bstack11l1ll_opy_ (u"ࠥ࠱࠲ࡹ࡫ࡪࡲࡖࡩࡸࡹࡩࡰࡰࡑࡥࡲ࡫ࠢᓵ"), default=bstack11l1ll_opy_ (u"ࠦࡋࡧ࡬ࡴࡧࠥᓶ"), help=bstack11l1ll_opy_ (u"ࠧࡇࡵࡵࡱࡰࡥࡹ࡯ࡣࠡࡵࡨࡸࠥࡹࡥࡴࡵ࡬ࡳࡳࠦ࡮ࡢ࡯ࡨࠦᓷ"))
    parser.addoption(bstack11l1ll_opy_ (u"ࠨ࠭࠮ࡵ࡮࡭ࡵ࡙ࡥࡴࡵ࡬ࡳࡳ࡙ࡴࡢࡶࡸࡷࠧᓸ"), default=bstack11l1ll_opy_ (u"ࠢࡇࡣ࡯ࡷࡪࠨᓹ"), help=bstack11l1ll_opy_ (u"ࠣࡃࡸࡸࡴࡳࡡࡵ࡫ࡦࠤࡸ࡫ࡴࠡࡵࡨࡷࡸ࡯࡯࡯ࠢࡱࡥࡲ࡫ࠢᓺ"))
    try:
        import pytest_selenium.pytest_selenium
    except:
        parser.addoption(bstack11l1ll_opy_ (u"ࠤ࠰࠱ࡩࡸࡩࡷࡧࡵࠦᓻ"), action=bstack11l1ll_opy_ (u"ࠥࡷࡹࡵࡲࡦࠤᓼ"), default=bstack11l1ll_opy_ (u"ࠦࡨ࡮ࡲࡰ࡯ࡨࠦᓽ"),
                         help=bstack11l1ll_opy_ (u"ࠧࡊࡲࡪࡸࡨࡶࠥࡺ࡯ࠡࡴࡸࡲࠥࡺࡥࡴࡶࡶࠦᓾ"))
def bstack1l1l1l1lll_opy_(log):
    if not (log[bstack11l1ll_opy_ (u"࠭࡭ࡦࡵࡶࡥ࡬࡫ࠧᓿ")] and log[bstack11l1ll_opy_ (u"ࠧ࡮ࡧࡶࡷࡦ࡭ࡥࠨᔀ")].strip()):
        return
    active = bstack1l1l1111l1_opy_()
    log = {
        bstack11l1ll_opy_ (u"ࠨ࡮ࡨࡺࡪࡲࠧᔁ"): log[bstack11l1ll_opy_ (u"ࠩ࡯ࡩࡻ࡫࡬ࠨᔂ")],
        bstack11l1ll_opy_ (u"ࠪࡸ࡮ࡳࡥࡴࡶࡤࡱࡵ࠭ᔃ"): datetime.datetime.utcnow().isoformat() + bstack11l1ll_opy_ (u"ࠫ࡟࠭ᔄ"),
        bstack11l1ll_opy_ (u"ࠬࡳࡥࡴࡵࡤ࡫ࡪ࠭ᔅ"): log[bstack11l1ll_opy_ (u"࠭࡭ࡦࡵࡶࡥ࡬࡫ࠧᔆ")],
    }
    if active:
        if active[bstack11l1ll_opy_ (u"ࠧࡵࡻࡳࡩࠬᔇ")] == bstack11l1ll_opy_ (u"ࠨࡪࡲࡳࡰ࠭ᔈ"):
            log[bstack11l1ll_opy_ (u"ࠩ࡫ࡳࡴࡱ࡟ࡳࡷࡱࡣࡺࡻࡩࡥࠩᔉ")] = active[bstack11l1ll_opy_ (u"ࠪ࡬ࡴࡵ࡫ࡠࡴࡸࡲࡤࡻࡵࡪࡦࠪᔊ")]
        elif active[bstack11l1ll_opy_ (u"ࠫࡹࡿࡰࡦࠩᔋ")] == bstack11l1ll_opy_ (u"ࠬࡺࡥࡴࡶࠪᔌ"):
            log[bstack11l1ll_opy_ (u"࠭ࡴࡦࡵࡷࡣࡷࡻ࡮ࡠࡷࡸ࡭ࡩ࠭ᔍ")] = active[bstack11l1ll_opy_ (u"ࠧࡵࡧࡶࡸࡤࡸࡵ࡯ࡡࡸࡹ࡮ࡪࠧᔎ")]
    bstack11l1ll11_opy_.bstack1l1l1l11ll_opy_([log])
def bstack1l1l1111l1_opy_():
    if len(store[bstack11l1ll_opy_ (u"ࠨࡥࡸࡶࡷ࡫࡮ࡵࡡ࡫ࡳࡴࡱ࡟ࡶࡷ࡬ࡨࠬᔏ")]) > 0 and store[bstack11l1ll_opy_ (u"ࠩࡦࡹࡷࡸࡥ࡯ࡶࡢ࡬ࡴࡵ࡫ࡠࡷࡸ࡭ࡩ࠭ᔐ")][-1]:
        return {
            bstack11l1ll_opy_ (u"ࠪࡸࡾࡶࡥࠨᔑ"): bstack11l1ll_opy_ (u"ࠫ࡭ࡵ࡯࡬ࠩᔒ"),
            bstack11l1ll_opy_ (u"ࠬ࡮࡯ࡰ࡭ࡢࡶࡺࡴ࡟ࡶࡷ࡬ࡨࠬᔓ"): store[bstack11l1ll_opy_ (u"࠭ࡣࡶࡴࡵࡩࡳࡺ࡟ࡩࡱࡲ࡯ࡤࡻࡵࡪࡦࠪᔔ")][-1]
        }
    if store.get(bstack11l1ll_opy_ (u"ࠧࡤࡷࡵࡶࡪࡴࡴࡠࡶࡨࡷࡹࡥࡵࡶ࡫ࡧࠫᔕ"), None):
        return {
            bstack11l1ll_opy_ (u"ࠨࡶࡼࡴࡪ࠭ᔖ"): bstack11l1ll_opy_ (u"ࠩࡷࡩࡸࡺࠧᔗ"),
            bstack11l1ll_opy_ (u"ࠪࡸࡪࡹࡴࡠࡴࡸࡲࡤࡻࡵࡪࡦࠪᔘ"): store[bstack11l1ll_opy_ (u"ࠫࡨࡻࡲࡳࡧࡱࡸࡤࡺࡥࡴࡶࡢࡹࡺ࡯ࡤࠨᔙ")]
        }
    return None
bstack1l11l11ll1_opy_ = bstack1l11ll1lll_opy_(bstack1l1l1l1lll_opy_)
def pytest_runtest_call(item):
    try:
        global CONFIG
        global bstack111111llll_opy_
        if bstack111111llll_opy_:
            driver = getattr(item, bstack11l1ll_opy_ (u"ࠬࡥࡤࡳ࡫ࡹࡩࡷ࠭ᔚ"), None)
            bstack111111ll_opy_ = bstack1ll111l11_opy_.bstack1llllll111_opy_(CONFIG, bstack11ll11llll_opy_(item.own_markers))
            item._a11y_started = bstack1ll111l11_opy_.bstack1l1l1lll1_opy_(driver, bstack111111ll_opy_)
        if not bstack11l1ll11_opy_.on() or bstack11111ll11l_opy_ != bstack11l1ll_opy_ (u"࠭ࡰࡺࡶࡨࡷࡹ࠭ᔛ"):
            return
        global current_test_uuid, bstack1l11l11ll1_opy_
        bstack1l11l11ll1_opy_.start()
        bstack1l1l1l1l11_opy_ = {
            bstack11l1ll_opy_ (u"ࠧࡶࡷ࡬ࡨࠬᔜ"): uuid4().__str__(),
            bstack11l1ll_opy_ (u"ࠨࡵࡷࡥࡷࡺࡥࡥࡡࡤࡸࠬᔝ"): datetime.datetime.utcnow().isoformat() + bstack11l1ll_opy_ (u"ࠩ࡝ࠫᔞ")
        }
        current_test_uuid = bstack1l1l1l1l11_opy_[bstack11l1ll_opy_ (u"ࠪࡹࡺ࡯ࡤࠨᔟ")]
        store[bstack11l1ll_opy_ (u"ࠫࡨࡻࡲࡳࡧࡱࡸࡤࡺࡥࡴࡶࡢࡹࡺ࡯ࡤࠨᔠ")] = bstack1l1l1l1l11_opy_[bstack11l1ll_opy_ (u"ࠬࡻࡵࡪࡦࠪᔡ")]
        threading.current_thread().current_test_uuid = current_test_uuid
        _1l1l111l11_opy_[item.nodeid] = {**_1l1l111l11_opy_[item.nodeid], **bstack1l1l1l1l11_opy_}
        bstack111111l1l1_opy_(item, _1l1l111l11_opy_[item.nodeid], bstack11l1ll_opy_ (u"࠭ࡔࡦࡵࡷࡖࡺࡴࡓࡵࡣࡵࡸࡪࡪࠧᔢ"))
    except Exception as err:
        print(bstack11l1ll_opy_ (u"ࠧࡆࡺࡦࡩࡵࡺࡩࡰࡰࠣ࡭ࡳࠦࡰࡺࡶࡨࡷࡹࡥࡲࡶࡰࡷࡩࡸࡺ࡟ࡤࡣ࡯ࡰ࠿ࠦࡻࡾࠩᔣ"), str(err))
def pytest_runtest_setup(item):
    if bstack11ll11l1l1_opy_():
        atexit.register(bstack1lllll111l_opy_)
        try:
            item.config.hook.pytest_selenium_runtest_makereport = bstack111ll11l1l_opy_
        except Exception as err:
            threading.current_thread().testStatus = bstack11l1ll_opy_ (u"ࠨࡲࡤࡷࡸ࡫ࡤࠨᔤ")
    try:
        if not bstack11l1ll11_opy_.on():
            return
        bstack1l11l11ll1_opy_.start()
        uuid = uuid4().__str__()
        bstack1l1l1l1l11_opy_ = {
            bstack11l1ll_opy_ (u"ࠩࡸࡹ࡮ࡪࠧᔥ"): uuid,
            bstack11l1ll_opy_ (u"ࠪࡷࡹࡧࡲࡵࡧࡧࡣࡦࡺࠧᔦ"): datetime.datetime.utcnow().isoformat() + bstack11l1ll_opy_ (u"ࠫ࡟࠭ᔧ"),
            bstack11l1ll_opy_ (u"ࠬࡺࡹࡱࡧࠪᔨ"): bstack11l1ll_opy_ (u"࠭ࡨࡰࡱ࡮ࠫᔩ"),
            bstack11l1ll_opy_ (u"ࠧࡩࡱࡲ࡯ࡤࡺࡹࡱࡧࠪᔪ"): bstack11l1ll_opy_ (u"ࠨࡄࡈࡊࡔࡘࡅࡠࡇࡄࡇࡍ࠭ᔫ"),
            bstack11l1ll_opy_ (u"ࠩ࡫ࡳࡴࡱ࡟࡯ࡣࡰࡩࠬᔬ"): bstack11l1ll_opy_ (u"ࠪࡷࡪࡺࡵࡱࠩᔭ")
        }
        threading.current_thread().current_hook_uuid = uuid
        store[bstack11l1ll_opy_ (u"ࠫࡨࡻࡲࡳࡧࡱࡸࡤࡺࡥࡴࡶࡢ࡭ࡹ࡫࡭ࠨᔮ")] = item
        store[bstack11l1ll_opy_ (u"ࠬࡩࡵࡳࡴࡨࡲࡹࡥࡨࡰࡱ࡮ࡣࡺࡻࡩࡥࠩᔯ")] = [uuid]
        if not _1l1l111l11_opy_.get(item.nodeid, None):
            _1l1l111l11_opy_[item.nodeid] = {bstack11l1ll_opy_ (u"࠭ࡨࡰࡱ࡮ࡷࠬᔰ"): [], bstack11l1ll_opy_ (u"ࠧࡧ࡫ࡻࡸࡺࡸࡥࡴࠩᔱ"): []}
        _1l1l111l11_opy_[item.nodeid][bstack11l1ll_opy_ (u"ࠨࡪࡲࡳࡰࡹࠧᔲ")].append(bstack1l1l1l1l11_opy_[bstack11l1ll_opy_ (u"ࠩࡸࡹ࡮ࡪࠧᔳ")])
        _1l1l111l11_opy_[item.nodeid + bstack11l1ll_opy_ (u"ࠪ࠱ࡸ࡫ࡴࡶࡲࠪᔴ")] = bstack1l1l1l1l11_opy_
        bstack11111l1l1l_opy_(item, bstack1l1l1l1l11_opy_, bstack11l1ll_opy_ (u"ࠫࡍࡵ࡯࡬ࡔࡸࡲࡘࡺࡡࡳࡶࡨࡨࠬᔵ"))
    except Exception as err:
        print(bstack11l1ll_opy_ (u"ࠬࡋࡸࡤࡧࡳࡸ࡮ࡵ࡮ࠡ࡫ࡱࠤࡵࡿࡴࡦࡵࡷࡣࡷࡻ࡮ࡵࡧࡶࡸࡤࡹࡥࡵࡷࡳ࠾ࠥࢁࡽࠨᔶ"), str(err))
def pytest_runtest_teardown(item):
    try:
        global bstack11l1llll_opy_
        if getattr(item, bstack11l1ll_opy_ (u"࠭࡟ࡢ࠳࠴ࡽࡤࡹࡴࡢࡴࡷࡩࡩ࠭ᔷ"), False):
            logger.info(bstack11l1ll_opy_ (u"ࠢࡂࡷࡷࡳࡲࡧࡴࡦࠢࡷࡩࡸࡺࠠࡤࡣࡶࡩࠥ࡫ࡸࡦࡥࡸࡸ࡮ࡵ࡮ࠡࡪࡤࡷࠥ࡫࡮ࡥࡧࡧ࠲ࠥࡖࡲࡰࡥࡨࡷࡸ࡯࡮ࡨࠢࡩࡳࡷࠦࡡࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾࠦࡴࡦࡵࡷ࡭ࡳ࡭ࠠࡪࡵࠣࡹࡳࡪࡥࡳࡹࡤࡽ࠳ࠦࠢᔸ"))
            driver = getattr(item, bstack11l1ll_opy_ (u"ࠨࡡࡧࡶ࡮ࡼࡥࡳࠩᔹ"), None)
            bstack11lllll1l1_opy_ = item.cls.__name__ if not item.cls is None else None
            bstack1ll111l11_opy_.bstack1l1llll1l_opy_(driver, bstack11lllll1l1_opy_, item.name, item.module.__name__, item.path, bstack11l1llll_opy_)
        if not bstack11l1ll11_opy_.on():
            return
        bstack1l1l1l1l11_opy_ = {
            bstack11l1ll_opy_ (u"ࠩࡸࡹ࡮ࡪࠧᔺ"): uuid4().__str__(),
            bstack11l1ll_opy_ (u"ࠪࡷࡹࡧࡲࡵࡧࡧࡣࡦࡺࠧᔻ"): datetime.datetime.utcnow().isoformat() + bstack11l1ll_opy_ (u"ࠫ࡟࠭ᔼ"),
            bstack11l1ll_opy_ (u"ࠬࡺࡹࡱࡧࠪᔽ"): bstack11l1ll_opy_ (u"࠭ࡨࡰࡱ࡮ࠫᔾ"),
            bstack11l1ll_opy_ (u"ࠧࡩࡱࡲ࡯ࡤࡺࡹࡱࡧࠪᔿ"): bstack11l1ll_opy_ (u"ࠨࡃࡉࡘࡊࡘ࡟ࡆࡃࡆࡌࠬᕀ"),
            bstack11l1ll_opy_ (u"ࠩ࡫ࡳࡴࡱ࡟࡯ࡣࡰࡩࠬᕁ"): bstack11l1ll_opy_ (u"ࠪࡸࡪࡧࡲࡥࡱࡺࡲࠬᕂ")
        }
        _1l1l111l11_opy_[item.nodeid + bstack11l1ll_opy_ (u"ࠫ࠲ࡺࡥࡢࡴࡧࡳࡼࡴࠧᕃ")] = bstack1l1l1l1l11_opy_
        bstack11111l1l1l_opy_(item, bstack1l1l1l1l11_opy_, bstack11l1ll_opy_ (u"ࠬࡎ࡯ࡰ࡭ࡕࡹࡳ࡙ࡴࡢࡴࡷࡩࡩ࠭ᕄ"))
    except Exception as err:
        print(bstack11l1ll_opy_ (u"࠭ࡅࡹࡥࡨࡴࡹ࡯࡯࡯ࠢ࡬ࡲࠥࡶࡹࡵࡧࡶࡸࡤࡸࡵ࡯ࡶࡨࡷࡹࡥࡴࡦࡣࡵࡨࡴࡽ࡮࠻ࠢࡾࢁࠬᕅ"), str(err))
@pytest.hookimpl(hookwrapper=True)
def pytest_fixture_setup(fixturedef, request):
    if not bstack11l1ll11_opy_.on():
        yield
        return
    start_time = datetime.datetime.now()
    if bstack111l1llll1_opy_(fixturedef.argname):
        store[bstack11l1ll_opy_ (u"ࠧࡤࡷࡵࡶࡪࡴࡴࡠ࡯ࡲࡨࡺࡲࡥࡠ࡫ࡷࡩࡲ࠭ᕆ")] = request.node
    elif bstack111ll1l11l_opy_(fixturedef.argname):
        store[bstack11l1ll_opy_ (u"ࠨࡥࡸࡶࡷ࡫࡮ࡵࡡࡦࡰࡦࡹࡳࡠ࡫ࡷࡩࡲ࠭ᕇ")] = request.node
    outcome = yield
    try:
        fixture = {
            bstack11l1ll_opy_ (u"ࠩࡱࡥࡲ࡫ࠧᕈ"): fixturedef.argname,
            bstack11l1ll_opy_ (u"ࠪࡶࡪࡹࡵ࡭ࡶࠪᕉ"): bstack11lll1l111_opy_(outcome),
            bstack11l1ll_opy_ (u"ࠫࡩࡻࡲࡢࡶ࡬ࡳࡳ࠭ᕊ"): (datetime.datetime.now() - start_time).total_seconds() * 1000
        }
        bstack11111l1111_opy_ = store[bstack11l1ll_opy_ (u"ࠬࡩࡵࡳࡴࡨࡲࡹࡥࡴࡦࡵࡷࡣ࡮ࡺࡥ࡮ࠩᕋ")]
        if not _1l1l111l11_opy_.get(bstack11111l1111_opy_.nodeid, None):
            _1l1l111l11_opy_[bstack11111l1111_opy_.nodeid] = {bstack11l1ll_opy_ (u"࠭ࡦࡪࡺࡷࡹࡷ࡫ࡳࠨᕌ"): []}
        _1l1l111l11_opy_[bstack11111l1111_opy_.nodeid][bstack11l1ll_opy_ (u"ࠧࡧ࡫ࡻࡸࡺࡸࡥࡴࠩᕍ")].append(fixture)
    except Exception as err:
        logger.debug(bstack11l1ll_opy_ (u"ࠨࡇࡻࡧࡪࡶࡴࡪࡱࡱࠤ࡮ࡴࠠࡱࡻࡷࡩࡸࡺ࡟ࡧ࡫ࡻࡸࡺࡸࡥࡠࡵࡨࡸࡺࡶ࠺ࠡࡽࢀࠫᕎ"), str(err))
if bstack1l11ll11_opy_() and bstack11l1ll11_opy_.on():
    def pytest_bdd_before_step(request, step):
        try:
            _1l1l111l11_opy_[request.node.nodeid][bstack11l1ll_opy_ (u"ࠩࡷࡩࡸࡺ࡟ࡥࡣࡷࡥࠬᕏ")].bstack1111llllll_opy_(id(step))
        except Exception as err:
            print(bstack11l1ll_opy_ (u"ࠪࡉࡽࡩࡥࡱࡶ࡬ࡳࡳࠦࡩ࡯ࠢࡳࡽࡹ࡫ࡳࡵࡡࡥࡨࡩࡥࡢࡦࡨࡲࡶࡪࡥࡳࡵࡧࡳ࠾ࠥࢁࡽࠨᕐ"), str(err))
    def pytest_bdd_step_error(request, step, exception):
        try:
            _1l1l111l11_opy_[request.node.nodeid][bstack11l1ll_opy_ (u"ࠫࡹ࡫ࡳࡵࡡࡧࡥࡹࡧࠧᕑ")].bstack1l11l11l1l_opy_(id(step), Result.failed(exception=exception))
        except Exception as err:
            print(bstack11l1ll_opy_ (u"ࠬࡋࡸࡤࡧࡳࡸ࡮ࡵ࡮ࠡ࡫ࡱࠤࡵࡿࡴࡦࡵࡷࡣࡧࡪࡤࡠࡵࡷࡩࡵࡥࡥࡳࡴࡲࡶ࠿ࠦࡻࡾࠩᕒ"), str(err))
    def pytest_bdd_after_step(request, step):
        try:
            bstack1l1l1l111l_opy_: bstack1l1l111ll1_opy_ = _1l1l111l11_opy_[request.node.nodeid][bstack11l1ll_opy_ (u"࠭ࡴࡦࡵࡷࡣࡩࡧࡴࡢࠩᕓ")]
            bstack1l1l1l111l_opy_.bstack1l11l11l1l_opy_(id(step), Result.passed())
        except Exception as err:
            print(bstack11l1ll_opy_ (u"ࠧࡆࡺࡦࡩࡵࡺࡩࡰࡰࠣ࡭ࡳࠦࡰࡺࡶࡨࡷࡹࡥࡢࡥࡦࡢࡷࡹ࡫ࡰࡠࡧࡵࡶࡴࡸ࠺ࠡࡽࢀࠫᕔ"), str(err))
    def pytest_bdd_before_scenario(request, feature, scenario):
        global bstack11111ll11l_opy_
        try:
            if not bstack11l1ll11_opy_.on() or bstack11111ll11l_opy_ != bstack11l1ll_opy_ (u"ࠨࡲࡼࡸࡪࡹࡴ࠮ࡤࡧࡨࠬᕕ"):
                return
            global bstack1l11l11ll1_opy_
            bstack1l11l11ll1_opy_.start()
            if not _1l1l111l11_opy_.get(request.node.nodeid, None):
                _1l1l111l11_opy_[request.node.nodeid] = {}
            bstack1l1l1l111l_opy_ = bstack1l1l111ll1_opy_.bstack1111lll111_opy_(
                scenario, feature, request.node,
                name=bstack111ll11l11_opy_(request.node, scenario),
                bstack1l1l1l11l1_opy_=bstack1ll11111ll_opy_(),
                file_path=feature.filename,
                scope=[feature.name],
                framework=bstack11l1ll_opy_ (u"ࠩࡓࡽࡹ࡫ࡳࡵ࠯ࡦࡹࡨࡻ࡭ࡣࡧࡵࠫᕖ"),
                tags=bstack111ll11ll1_opy_(feature, scenario)
            )
            _1l1l111l11_opy_[request.node.nodeid][bstack11l1ll_opy_ (u"ࠪࡸࡪࡹࡴࡠࡦࡤࡸࡦ࠭ᕗ")] = bstack1l1l1l111l_opy_
            bstack111111ll1l_opy_(bstack1l1l1l111l_opy_.uuid)
            bstack11l1ll11_opy_.bstack1l1l1ll1ll_opy_(bstack11l1ll_opy_ (u"࡙ࠫ࡫ࡳࡵࡔࡸࡲࡘࡺࡡࡳࡶࡨࡨࠬᕘ"), bstack1l1l1l111l_opy_)
        except Exception as err:
            print(bstack11l1ll_opy_ (u"ࠬࡋࡸࡤࡧࡳࡸ࡮ࡵ࡮ࠡ࡫ࡱࠤࡵࡿࡴࡦࡵࡷࡣࡧࡪࡤࡠࡤࡨࡪࡴࡸࡥࡠࡵࡦࡩࡳࡧࡲࡪࡱ࠽ࠤࢀࢃࠧᕙ"), str(err))
def bstack111111lll1_opy_(bstack11111lll1l_opy_):
    if bstack11111lll1l_opy_ in store[bstack11l1ll_opy_ (u"࠭ࡣࡶࡴࡵࡩࡳࡺ࡟ࡩࡱࡲ࡯ࡤࡻࡵࡪࡦࠪᕚ")]:
        store[bstack11l1ll_opy_ (u"ࠧࡤࡷࡵࡶࡪࡴࡴࡠࡪࡲࡳࡰࡥࡵࡶ࡫ࡧࠫᕛ")].remove(bstack11111lll1l_opy_)
def bstack111111ll1l_opy_(bstack1111111l1l_opy_):
    store[bstack11l1ll_opy_ (u"ࠨࡥࡸࡶࡷ࡫࡮ࡵࡡࡷࡩࡸࡺ࡟ࡶࡷ࡬ࡨࠬᕜ")] = bstack1111111l1l_opy_
    threading.current_thread().current_test_uuid = bstack1111111l1l_opy_
@bstack11l1ll11_opy_.bstack1111l11l1l_opy_
def bstack11111lllll_opy_(item, call, report):
    global bstack11111ll11l_opy_
    try:
        if report.when == bstack11l1ll_opy_ (u"ࠩࡦࡥࡱࡲࠧᕝ"):
            bstack1l11l11ll1_opy_.reset()
        if report.when == bstack11l1ll_opy_ (u"ࠪࡧࡦࡲ࡬ࠨᕞ"):
            if bstack11111ll11l_opy_ == bstack11l1ll_opy_ (u"ࠫࡵࡿࡴࡦࡵࡷࠫᕟ"):
                _1l1l111l11_opy_[item.nodeid][bstack11l1ll_opy_ (u"ࠬ࡬ࡩ࡯࡫ࡶ࡬ࡪࡪ࡟ࡢࡶࠪᕠ")] = bstack11lll11l11_opy_(report.stop)
                bstack111111l1l1_opy_(item, _1l1l111l11_opy_[item.nodeid], bstack11l1ll_opy_ (u"࠭ࡔࡦࡵࡷࡖࡺࡴࡆࡪࡰ࡬ࡷ࡭࡫ࡤࠨᕡ"), report, call)
                store[bstack11l1ll_opy_ (u"ࠧࡤࡷࡵࡶࡪࡴࡴࡠࡶࡨࡷࡹࡥࡵࡶ࡫ࡧࠫᕢ")] = None
            elif bstack11111ll11l_opy_ == bstack11l1ll_opy_ (u"ࠣࡲࡼࡸࡪࡹࡴ࠮ࡤࡧࡨࠧᕣ"):
                bstack1l1l1l111l_opy_ = _1l1l111l11_opy_[item.nodeid][bstack11l1ll_opy_ (u"ࠩࡷࡩࡸࡺ࡟ࡥࡣࡷࡥࠬᕤ")]
                bstack1l1l1l111l_opy_.set(hooks=_1l1l111l11_opy_[item.nodeid].get(bstack11l1ll_opy_ (u"ࠪ࡬ࡴࡵ࡫ࡴࠩᕥ"), []))
                exception, bstack1l11llll1l_opy_ = None, None
                if call.excinfo:
                    exception = call.excinfo.value
                    bstack1l11llll1l_opy_ = [call.excinfo.exconly(), report.longreprtext]
                bstack1l1l1l111l_opy_.stop(time=bstack11lll11l11_opy_(report.stop), result=Result(result=report.outcome, exception=exception, bstack1l11llll1l_opy_=bstack1l11llll1l_opy_))
                bstack11l1ll11_opy_.bstack1l1l1ll1ll_opy_(bstack11l1ll_opy_ (u"࡙ࠫ࡫ࡳࡵࡔࡸࡲࡋ࡯࡮ࡪࡵ࡫ࡩࡩ࠭ᕦ"), _1l1l111l11_opy_[item.nodeid][bstack11l1ll_opy_ (u"ࠬࡺࡥࡴࡶࡢࡨࡦࡺࡡࠨᕧ")])
        elif report.when in [bstack11l1ll_opy_ (u"࠭ࡳࡦࡶࡸࡴࠬᕨ"), bstack11l1ll_opy_ (u"ࠧࡵࡧࡤࡶࡩࡵࡷ࡯ࠩᕩ")]:
            bstack1l1l1lll1l_opy_ = item.nodeid + bstack11l1ll_opy_ (u"ࠨ࠯ࠪᕪ") + report.when
            if report.skipped:
                hook_type = bstack11l1ll_opy_ (u"ࠩࡅࡉࡋࡕࡒࡆࡡࡈࡅࡈࡎࠧᕫ") if report.when == bstack11l1ll_opy_ (u"ࠪࡷࡪࡺࡵࡱࠩᕬ") else bstack11l1ll_opy_ (u"ࠫࡆࡌࡔࡆࡔࡢࡉࡆࡉࡈࠨᕭ")
                _1l1l111l11_opy_[bstack1l1l1lll1l_opy_] = {
                    bstack11l1ll_opy_ (u"ࠬࡻࡵࡪࡦࠪᕮ"): uuid4().__str__(),
                    bstack11l1ll_opy_ (u"࠭ࡳࡵࡣࡵࡸࡪࡪ࡟ࡢࡶࠪᕯ"): datetime.datetime.utcfromtimestamp(report.start).isoformat() + bstack11l1ll_opy_ (u"࡛ࠧࠩᕰ"),
                    bstack11l1ll_opy_ (u"ࠨࡪࡲࡳࡰࡥࡴࡺࡲࡨࠫᕱ"): hook_type
                }
            _1l1l111l11_opy_[bstack1l1l1lll1l_opy_][bstack11l1ll_opy_ (u"ࠩࡩ࡭ࡳ࡯ࡳࡩࡧࡧࡣࡦࡺࠧᕲ")] = datetime.datetime.utcfromtimestamp(report.stop).isoformat() + bstack11l1ll_opy_ (u"ࠪ࡞ࠬᕳ")
            bstack111111lll1_opy_(_1l1l111l11_opy_[bstack1l1l1lll1l_opy_][bstack11l1ll_opy_ (u"ࠫࡺࡻࡩࡥࠩᕴ")])
            bstack11111l1l1l_opy_(item, _1l1l111l11_opy_[bstack1l1l1lll1l_opy_], bstack11l1ll_opy_ (u"ࠬࡎ࡯ࡰ࡭ࡕࡹࡳࡌࡩ࡯࡫ࡶ࡬ࡪࡪࠧᕵ"), report, call)
            if report.when == bstack11l1ll_opy_ (u"࠭ࡳࡦࡶࡸࡴࠬᕶ"):
                if report.outcome == bstack11l1ll_opy_ (u"ࠧࡧࡣ࡬ࡰࡪࡪࠧᕷ"):
                    bstack1l1l1l1l11_opy_ = {
                        bstack11l1ll_opy_ (u"ࠨࡷࡸ࡭ࡩ࠭ᕸ"): uuid4().__str__(),
                        bstack11l1ll_opy_ (u"ࠩࡶࡸࡦࡸࡴࡦࡦࡢࡥࡹ࠭ᕹ"): bstack1ll11111ll_opy_(),
                        bstack11l1ll_opy_ (u"ࠪࡪ࡮ࡴࡩࡴࡪࡨࡨࡤࡧࡴࠨᕺ"): bstack1ll11111ll_opy_()
                    }
                    _1l1l111l11_opy_[item.nodeid] = {**_1l1l111l11_opy_[item.nodeid], **bstack1l1l1l1l11_opy_}
                    bstack111111l1l1_opy_(item, _1l1l111l11_opy_[item.nodeid], bstack11l1ll_opy_ (u"࡙ࠫ࡫ࡳࡵࡔࡸࡲࡘࡺࡡࡳࡶࡨࡨࠬᕻ"))
                    bstack111111l1l1_opy_(item, _1l1l111l11_opy_[item.nodeid], bstack11l1ll_opy_ (u"࡚ࠬࡥࡴࡶࡕࡹࡳࡌࡩ࡯࡫ࡶ࡬ࡪࡪࠧᕼ"), report, call)
    except Exception as err:
        print(bstack11l1ll_opy_ (u"࠭ࡅࡹࡥࡨࡴࡹ࡯࡯࡯ࠢ࡬ࡲࠥ࡮ࡡ࡯ࡦ࡯ࡩࡤࡵ࠱࠲ࡻࡢࡸࡪࡹࡴࡠࡧࡹࡩࡳࡺ࠺ࠡࡽࢀࠫᕽ"), str(err))
def bstack1111l11111_opy_(test, bstack1l1l1l1l11_opy_, result=None, call=None, bstack1l1lll1l1l_opy_=None, outcome=None):
    file_path = os.path.relpath(test.fspath.strpath, start=os.getcwd())
    bstack1l1l1l111l_opy_ = {
        bstack11l1ll_opy_ (u"ࠧࡶࡷ࡬ࡨࠬᕾ"): bstack1l1l1l1l11_opy_[bstack11l1ll_opy_ (u"ࠨࡷࡸ࡭ࡩ࠭ᕿ")],
        bstack11l1ll_opy_ (u"ࠩࡷࡽࡵ࡫ࠧᖀ"): bstack11l1ll_opy_ (u"ࠪࡸࡪࡹࡴࠨᖁ"),
        bstack11l1ll_opy_ (u"ࠫࡳࡧ࡭ࡦࠩᖂ"): test.name,
        bstack11l1ll_opy_ (u"ࠬࡨ࡯ࡥࡻࠪᖃ"): {
            bstack11l1ll_opy_ (u"࠭࡬ࡢࡰࡪࠫᖄ"): bstack11l1ll_opy_ (u"ࠧࡱࡻࡷ࡬ࡴࡴࠧᖅ"),
            bstack11l1ll_opy_ (u"ࠨࡥࡲࡨࡪ࠭ᖆ"): inspect.getsource(test.obj)
        },
        bstack11l1ll_opy_ (u"ࠩ࡬ࡨࡪࡴࡴࡪࡨ࡬ࡩࡷ࠭ᖇ"): test.name,
        bstack11l1ll_opy_ (u"ࠪࡷࡨࡵࡰࡦࠩᖈ"): test.name,
        bstack11l1ll_opy_ (u"ࠫࡸࡩ࡯ࡱࡧࡶࠫᖉ"): bstack11l1ll11_opy_.bstack1l11l1ll1l_opy_(test),
        bstack11l1ll_opy_ (u"ࠬ࡬ࡩ࡭ࡧࡢࡲࡦࡳࡥࠨᖊ"): file_path,
        bstack11l1ll_opy_ (u"࠭࡬ࡰࡥࡤࡸ࡮ࡵ࡮ࠨᖋ"): file_path,
        bstack11l1ll_opy_ (u"ࠧࡳࡧࡶࡹࡱࡺࠧᖌ"): bstack11l1ll_opy_ (u"ࠨࡲࡨࡲࡩ࡯࡮ࡨࠩᖍ"),
        bstack11l1ll_opy_ (u"ࠩࡹࡧࡤ࡬ࡩ࡭ࡧࡳࡥࡹ࡮ࠧᖎ"): file_path,
        bstack11l1ll_opy_ (u"ࠪࡷࡹࡧࡲࡵࡧࡧࡣࡦࡺࠧᖏ"): bstack1l1l1l1l11_opy_[bstack11l1ll_opy_ (u"ࠫࡸࡺࡡࡳࡶࡨࡨࡤࡧࡴࠨᖐ")],
        bstack11l1ll_opy_ (u"ࠬ࡬ࡲࡢ࡯ࡨࡻࡴࡸ࡫ࠨᖑ"): bstack11l1ll_opy_ (u"࠭ࡐࡺࡶࡨࡷࡹ࠭ᖒ"),
        bstack11l1ll_opy_ (u"ࠧࡤࡷࡶࡸࡴࡳࡒࡦࡴࡸࡲࡕࡧࡲࡢ࡯ࠪᖓ"): {
            bstack11l1ll_opy_ (u"ࠨࡴࡨࡶࡺࡴ࡟࡯ࡣࡰࡩࠬᖔ"): test.nodeid
        },
        bstack11l1ll_opy_ (u"ࠩࡷࡥ࡬ࡹࠧᖕ"): bstack11ll11llll_opy_(test.own_markers)
    }
    if bstack1l1lll1l1l_opy_ in [bstack11l1ll_opy_ (u"ࠪࡘࡪࡹࡴࡓࡷࡱࡗࡰ࡯ࡰࡱࡧࡧࠫᖖ"), bstack11l1ll_opy_ (u"࡙ࠫ࡫ࡳࡵࡔࡸࡲࡋ࡯࡮ࡪࡵ࡫ࡩࡩ࠭ᖗ")]:
        bstack1l1l1l111l_opy_[bstack11l1ll_opy_ (u"ࠬࡳࡥࡵࡣࠪᖘ")] = {
            bstack11l1ll_opy_ (u"࠭ࡦࡪࡺࡷࡹࡷ࡫ࡳࠨᖙ"): bstack1l1l1l1l11_opy_.get(bstack11l1ll_opy_ (u"ࠧࡧ࡫ࡻࡸࡺࡸࡥࡴࠩᖚ"), [])
        }
    if bstack1l1lll1l1l_opy_ == bstack11l1ll_opy_ (u"ࠨࡖࡨࡷࡹࡘࡵ࡯ࡕ࡮࡭ࡵࡶࡥࡥࠩᖛ"):
        bstack1l1l1l111l_opy_[bstack11l1ll_opy_ (u"ࠩࡵࡩࡸࡻ࡬ࡵࠩᖜ")] = bstack11l1ll_opy_ (u"ࠪࡷࡰ࡯ࡰࡱࡧࡧࠫᖝ")
        bstack1l1l1l111l_opy_[bstack11l1ll_opy_ (u"ࠫ࡭ࡵ࡯࡬ࡵࠪᖞ")] = bstack1l1l1l1l11_opy_[bstack11l1ll_opy_ (u"ࠬ࡮࡯ࡰ࡭ࡶࠫᖟ")]
        bstack1l1l1l111l_opy_[bstack11l1ll_opy_ (u"࠭ࡦࡪࡰ࡬ࡷ࡭࡫ࡤࡠࡣࡷࠫᖠ")] = bstack1l1l1l1l11_opy_[bstack11l1ll_opy_ (u"ࠧࡧ࡫ࡱ࡭ࡸ࡮ࡥࡥࡡࡤࡸࠬᖡ")]
    if result:
        bstack1l1l1l111l_opy_[bstack11l1ll_opy_ (u"ࠨࡴࡨࡷࡺࡲࡴࠨᖢ")] = result.outcome
        bstack1l1l1l111l_opy_[bstack11l1ll_opy_ (u"ࠩࡧࡹࡷࡧࡴࡪࡱࡱࡣ࡮ࡴ࡟࡮ࡵࠪᖣ")] = result.duration * 1000
        bstack1l1l1l111l_opy_[bstack11l1ll_opy_ (u"ࠪࡪ࡮ࡴࡩࡴࡪࡨࡨࡤࡧࡴࠨᖤ")] = bstack1l1l1l1l11_opy_[bstack11l1ll_opy_ (u"ࠫ࡫࡯࡮ࡪࡵ࡫ࡩࡩࡥࡡࡵࠩᖥ")]
        if result.failed:
            bstack1l1l1l111l_opy_[bstack11l1ll_opy_ (u"ࠬ࡬ࡡࡪ࡮ࡸࡶࡪࡥࡴࡺࡲࡨࠫᖦ")] = bstack11l1ll11_opy_.bstack1l111l1l11_opy_(call.excinfo.typename)
            bstack1l1l1l111l_opy_[bstack11l1ll_opy_ (u"࠭ࡦࡢ࡫࡯ࡹࡷ࡫ࠧᖧ")] = bstack11l1ll11_opy_.bstack1111ll11l1_opy_(call.excinfo, result)
        bstack1l1l1l111l_opy_[bstack11l1ll_opy_ (u"ࠧࡩࡱࡲ࡯ࡸ࠭ᖨ")] = bstack1l1l1l1l11_opy_[bstack11l1ll_opy_ (u"ࠨࡪࡲࡳࡰࡹࠧᖩ")]
    if outcome:
        bstack1l1l1l111l_opy_[bstack11l1ll_opy_ (u"ࠩࡵࡩࡸࡻ࡬ࡵࠩᖪ")] = bstack11lll1l111_opy_(outcome)
        bstack1l1l1l111l_opy_[bstack11l1ll_opy_ (u"ࠪࡨࡺࡸࡡࡵ࡫ࡲࡲࡤ࡯࡮ࡠ࡯ࡶࠫᖫ")] = 0
        bstack1l1l1l111l_opy_[bstack11l1ll_opy_ (u"ࠫ࡫࡯࡮ࡪࡵ࡫ࡩࡩࡥࡡࡵࠩᖬ")] = bstack1l1l1l1l11_opy_[bstack11l1ll_opy_ (u"ࠬ࡬ࡩ࡯࡫ࡶ࡬ࡪࡪ࡟ࡢࡶࠪᖭ")]
        if bstack1l1l1l111l_opy_[bstack11l1ll_opy_ (u"࠭ࡲࡦࡵࡸࡰࡹ࠭ᖮ")] == bstack11l1ll_opy_ (u"ࠧࡧࡣ࡬ࡰࡪࡪࠧᖯ"):
            bstack1l1l1l111l_opy_[bstack11l1ll_opy_ (u"ࠨࡨࡤ࡭ࡱࡻࡲࡦࡡࡷࡽࡵ࡫ࠧᖰ")] = bstack11l1ll_opy_ (u"ࠩࡘࡲ࡭ࡧ࡮ࡥ࡮ࡨࡨࡊࡸࡲࡰࡴࠪᖱ")  # bstack1111111lll_opy_
            bstack1l1l1l111l_opy_[bstack11l1ll_opy_ (u"ࠪࡪࡦ࡯࡬ࡶࡴࡨࠫᖲ")] = [{bstack11l1ll_opy_ (u"ࠫࡧࡧࡣ࡬ࡶࡵࡥࡨ࡫ࠧᖳ"): [bstack11l1ll_opy_ (u"ࠬࡹ࡯࡮ࡧࠣࡩࡷࡸ࡯ࡳࠩᖴ")]}]
        bstack1l1l1l111l_opy_[bstack11l1ll_opy_ (u"࠭ࡨࡰࡱ࡮ࡷࠬᖵ")] = bstack1l1l1l1l11_opy_[bstack11l1ll_opy_ (u"ࠧࡩࡱࡲ࡯ࡸ࠭ᖶ")]
    return bstack1l1l1l111l_opy_
def bstack11111l1lll_opy_(test, bstack1l11l1l1ll_opy_, bstack1l1lll1l1l_opy_, result, call, outcome, bstack11111l11ll_opy_):
    file_path = os.path.relpath(test.fspath.strpath, start=os.getcwd())
    hook_type = bstack1l11l1l1ll_opy_[bstack11l1ll_opy_ (u"ࠨࡪࡲࡳࡰࡥࡴࡺࡲࡨࠫᖷ")]
    hook_name = bstack1l11l1l1ll_opy_[bstack11l1ll_opy_ (u"ࠩ࡫ࡳࡴࡱ࡟࡯ࡣࡰࡩࠬᖸ")]
    hook_data = {
        bstack11l1ll_opy_ (u"ࠪࡹࡺ࡯ࡤࠨᖹ"): bstack1l11l1l1ll_opy_[bstack11l1ll_opy_ (u"ࠫࡺࡻࡩࡥࠩᖺ")],
        bstack11l1ll_opy_ (u"ࠬࡺࡹࡱࡧࠪᖻ"): bstack11l1ll_opy_ (u"࠭ࡨࡰࡱ࡮ࠫᖼ"),
        bstack11l1ll_opy_ (u"ࠧ࡯ࡣࡰࡩࠬᖽ"): bstack11l1ll_opy_ (u"ࠨࡽࢀࠫᖾ").format(bstack111ll111ll_opy_(hook_name)),
        bstack11l1ll_opy_ (u"ࠩࡥࡳࡩࡿࠧᖿ"): {
            bstack11l1ll_opy_ (u"ࠪࡰࡦࡴࡧࠨᗀ"): bstack11l1ll_opy_ (u"ࠫࡵࡿࡴࡩࡱࡱࠫᗁ"),
            bstack11l1ll_opy_ (u"ࠬࡩ࡯ࡥࡧࠪᗂ"): None
        },
        bstack11l1ll_opy_ (u"࠭ࡳࡤࡱࡳࡩࠬᗃ"): test.name,
        bstack11l1ll_opy_ (u"ࠧࡴࡥࡲࡴࡪࡹࠧᗄ"): bstack11l1ll11_opy_.bstack1l11l1ll1l_opy_(test, hook_name),
        bstack11l1ll_opy_ (u"ࠨࡨ࡬ࡰࡪࡥ࡮ࡢ࡯ࡨࠫᗅ"): file_path,
        bstack11l1ll_opy_ (u"ࠩ࡯ࡳࡨࡧࡴࡪࡱࡱࠫᗆ"): file_path,
        bstack11l1ll_opy_ (u"ࠪࡶࡪࡹࡵ࡭ࡶࠪᗇ"): bstack11l1ll_opy_ (u"ࠫࡵ࡫࡮ࡥ࡫ࡱ࡫ࠬᗈ"),
        bstack11l1ll_opy_ (u"ࠬࡼࡣࡠࡨ࡬ࡰࡪࡶࡡࡵࡪࠪᗉ"): file_path,
        bstack11l1ll_opy_ (u"࠭ࡳࡵࡣࡵࡸࡪࡪ࡟ࡢࡶࠪᗊ"): bstack1l11l1l1ll_opy_[bstack11l1ll_opy_ (u"ࠧࡴࡶࡤࡶࡹ࡫ࡤࡠࡣࡷࠫᗋ")],
        bstack11l1ll_opy_ (u"ࠨࡨࡵࡥࡲ࡫ࡷࡰࡴ࡮ࠫᗌ"): bstack11l1ll_opy_ (u"ࠩࡓࡽࡹ࡫ࡳࡵ࠯ࡦࡹࡨࡻ࡭ࡣࡧࡵࠫᗍ") if bstack11111ll11l_opy_ == bstack11l1ll_opy_ (u"ࠪࡴࡾࡺࡥࡴࡶ࠰ࡦࡩࡪࠧᗎ") else bstack11l1ll_opy_ (u"ࠫࡕࡿࡴࡦࡵࡷࠫᗏ"),
        bstack11l1ll_opy_ (u"ࠬ࡮࡯ࡰ࡭ࡢࡸࡾࡶࡥࠨᗐ"): hook_type
    }
    bstack111111ll11_opy_ = bstack1l11ll1l1l_opy_(_1l1l111l11_opy_.get(test.nodeid, None))
    if bstack111111ll11_opy_:
        hook_data[bstack11l1ll_opy_ (u"࠭ࡴࡦࡵࡷࡣࡷࡻ࡮ࡠ࡫ࡧࠫᗑ")] = bstack111111ll11_opy_
    if result:
        hook_data[bstack11l1ll_opy_ (u"ࠧࡳࡧࡶࡹࡱࡺࠧᗒ")] = result.outcome
        hook_data[bstack11l1ll_opy_ (u"ࠨࡦࡸࡶࡦࡺࡩࡰࡰࡢ࡭ࡳࡥ࡭ࡴࠩᗓ")] = result.duration * 1000
        hook_data[bstack11l1ll_opy_ (u"ࠩࡩ࡭ࡳ࡯ࡳࡩࡧࡧࡣࡦࡺࠧᗔ")] = bstack1l11l1l1ll_opy_[bstack11l1ll_opy_ (u"ࠪࡪ࡮ࡴࡩࡴࡪࡨࡨࡤࡧࡴࠨᗕ")]
        if result.failed:
            hook_data[bstack11l1ll_opy_ (u"ࠫ࡫ࡧࡩ࡭ࡷࡵࡩࡤࡺࡹࡱࡧࠪᗖ")] = bstack11l1ll11_opy_.bstack1l111l1l11_opy_(call.excinfo.typename)
            hook_data[bstack11l1ll_opy_ (u"ࠬ࡬ࡡࡪ࡮ࡸࡶࡪ࠭ᗗ")] = bstack11l1ll11_opy_.bstack1111ll11l1_opy_(call.excinfo, result)
    if outcome:
        hook_data[bstack11l1ll_opy_ (u"࠭ࡲࡦࡵࡸࡰࡹ࠭ᗘ")] = bstack11lll1l111_opy_(outcome)
        hook_data[bstack11l1ll_opy_ (u"ࠧࡥࡷࡵࡥࡹ࡯࡯࡯ࡡ࡬ࡲࡤࡳࡳࠨᗙ")] = 100
        hook_data[bstack11l1ll_opy_ (u"ࠨࡨ࡬ࡲ࡮ࡹࡨࡦࡦࡢࡥࡹ࠭ᗚ")] = bstack1l11l1l1ll_opy_[bstack11l1ll_opy_ (u"ࠩࡩ࡭ࡳ࡯ࡳࡩࡧࡧࡣࡦࡺࠧᗛ")]
        if hook_data[bstack11l1ll_opy_ (u"ࠪࡶࡪࡹࡵ࡭ࡶࠪᗜ")] == bstack11l1ll_opy_ (u"ࠫ࡫ࡧࡩ࡭ࡧࡧࠫᗝ"):
            hook_data[bstack11l1ll_opy_ (u"ࠬ࡬ࡡࡪ࡮ࡸࡶࡪࡥࡴࡺࡲࡨࠫᗞ")] = bstack11l1ll_opy_ (u"࠭ࡕ࡯ࡪࡤࡲࡩࡲࡥࡥࡇࡵࡶࡴࡸࠧᗟ")  # bstack1111111lll_opy_
            hook_data[bstack11l1ll_opy_ (u"ࠧࡧࡣ࡬ࡰࡺࡸࡥࠨᗠ")] = [{bstack11l1ll_opy_ (u"ࠨࡤࡤࡧࡰࡺࡲࡢࡥࡨࠫᗡ"): [bstack11l1ll_opy_ (u"ࠩࡶࡳࡲ࡫ࠠࡦࡴࡵࡳࡷ࠭ᗢ")]}]
    if bstack11111l11ll_opy_:
        hook_data[bstack11l1ll_opy_ (u"ࠪࡶࡪࡹࡵ࡭ࡶࠪᗣ")] = bstack11111l11ll_opy_.result
        hook_data[bstack11l1ll_opy_ (u"ࠫࡩࡻࡲࡢࡶ࡬ࡳࡳࡥࡩ࡯ࡡࡰࡷࠬᗤ")] = bstack11ll11111l_opy_(bstack1l11l1l1ll_opy_[bstack11l1ll_opy_ (u"ࠬࡹࡴࡢࡴࡷࡩࡩࡥࡡࡵࠩᗥ")], bstack1l11l1l1ll_opy_[bstack11l1ll_opy_ (u"࠭ࡦࡪࡰ࡬ࡷ࡭࡫ࡤࡠࡣࡷࠫᗦ")])
        hook_data[bstack11l1ll_opy_ (u"ࠧࡧ࡫ࡱ࡭ࡸ࡮ࡥࡥࡡࡤࡸࠬᗧ")] = bstack1l11l1l1ll_opy_[bstack11l1ll_opy_ (u"ࠨࡨ࡬ࡲ࡮ࡹࡨࡦࡦࡢࡥࡹ࠭ᗨ")]
        if hook_data[bstack11l1ll_opy_ (u"ࠩࡵࡩࡸࡻ࡬ࡵࠩᗩ")] == bstack11l1ll_opy_ (u"ࠪࡪࡦ࡯࡬ࡦࡦࠪᗪ"):
            hook_data[bstack11l1ll_opy_ (u"ࠫ࡫ࡧࡩ࡭ࡷࡵࡩࡤࡺࡹࡱࡧࠪᗫ")] = bstack11l1ll11_opy_.bstack1l111l1l11_opy_(bstack11111l11ll_opy_.exception_type)
            hook_data[bstack11l1ll_opy_ (u"ࠬ࡬ࡡࡪ࡮ࡸࡶࡪ࠭ᗬ")] = [{bstack11l1ll_opy_ (u"࠭ࡢࡢࡥ࡮ࡸࡷࡧࡣࡦࠩᗭ"): bstack11lll1l1ll_opy_(bstack11111l11ll_opy_.exception)}]
    return hook_data
def bstack111111l1l1_opy_(test, bstack1l1l1l1l11_opy_, bstack1l1lll1l1l_opy_, result=None, call=None, outcome=None):
    bstack1l1l1l111l_opy_ = bstack1111l11111_opy_(test, bstack1l1l1l1l11_opy_, result, call, bstack1l1lll1l1l_opy_, outcome)
    driver = getattr(test, bstack11l1ll_opy_ (u"ࠧࡠࡦࡵ࡭ࡻ࡫ࡲࠨᗮ"), None)
    if bstack1l1lll1l1l_opy_ == bstack11l1ll_opy_ (u"ࠨࡖࡨࡷࡹࡘࡵ࡯ࡕࡷࡥࡷࡺࡥࡥࠩᗯ") and driver:
        bstack1l1l1l111l_opy_[bstack11l1ll_opy_ (u"ࠩ࡬ࡲࡹ࡫ࡧࡳࡣࡷ࡭ࡴࡴࡳࠨᗰ")] = bstack11l1ll11_opy_.bstack1l11ll111l_opy_(driver)
    if bstack1l1lll1l1l_opy_ == bstack11l1ll_opy_ (u"ࠪࡘࡪࡹࡴࡓࡷࡱࡗࡰ࡯ࡰࡱࡧࡧࠫᗱ"):
        bstack1l1lll1l1l_opy_ = bstack11l1ll_opy_ (u"࡙ࠫ࡫ࡳࡵࡔࡸࡲࡋ࡯࡮ࡪࡵ࡫ࡩࡩ࠭ᗲ")
    bstack1l1l1lll11_opy_ = {
        bstack11l1ll_opy_ (u"ࠬ࡫ࡶࡦࡰࡷࡣࡹࡿࡰࡦࠩᗳ"): bstack1l1lll1l1l_opy_,
        bstack11l1ll_opy_ (u"࠭ࡴࡦࡵࡷࡣࡷࡻ࡮ࠨᗴ"): bstack1l1l1l111l_opy_
    }
    bstack11l1ll11_opy_.bstack1l1l11llll_opy_(bstack1l1l1lll11_opy_)
def bstack11111l1l1l_opy_(test, bstack1l1l1l1l11_opy_, bstack1l1lll1l1l_opy_, result=None, call=None, outcome=None, bstack11111l11ll_opy_=None):
    hook_data = bstack11111l1lll_opy_(test, bstack1l1l1l1l11_opy_, bstack1l1lll1l1l_opy_, result, call, outcome, bstack11111l11ll_opy_)
    bstack1l1l1lll11_opy_ = {
        bstack11l1ll_opy_ (u"ࠧࡦࡸࡨࡲࡹࡥࡴࡺࡲࡨࠫᗵ"): bstack1l1lll1l1l_opy_,
        bstack11l1ll_opy_ (u"ࠨࡪࡲࡳࡰࡥࡲࡶࡰࠪᗶ"): hook_data
    }
    bstack11l1ll11_opy_.bstack1l1l11llll_opy_(bstack1l1l1lll11_opy_)
def bstack1l11ll1l1l_opy_(bstack1l1l1l1l11_opy_):
    if not bstack1l1l1l1l11_opy_:
        return None
    if bstack1l1l1l1l11_opy_.get(bstack11l1ll_opy_ (u"ࠩࡷࡩࡸࡺ࡟ࡥࡣࡷࡥࠬᗷ"), None):
        return getattr(bstack1l1l1l1l11_opy_[bstack11l1ll_opy_ (u"ࠪࡸࡪࡹࡴࡠࡦࡤࡸࡦ࠭ᗸ")], bstack11l1ll_opy_ (u"ࠫࡺࡻࡩࡥࠩᗹ"), None)
    return bstack1l1l1l1l11_opy_.get(bstack11l1ll_opy_ (u"ࠬࡻࡵࡪࡦࠪᗺ"), None)
@pytest.fixture(autouse=True)
def second_fixture(caplog, request):
    yield
    try:
        if not bstack11l1ll11_opy_.on():
            return
        places = [bstack11l1ll_opy_ (u"࠭ࡳࡦࡶࡸࡴࠬᗻ"), bstack11l1ll_opy_ (u"ࠧࡤࡣ࡯ࡰࠬᗼ"), bstack11l1ll_opy_ (u"ࠨࡶࡨࡥࡷࡪ࡯ࡸࡰࠪᗽ")]
        bstack1l11l1l11l_opy_ = []
        for bstack1111l1111l_opy_ in places:
            records = caplog.get_records(bstack1111l1111l_opy_)
            bstack11111l1ll1_opy_ = bstack11l1ll_opy_ (u"ࠩࡷࡩࡸࡺ࡟ࡳࡷࡱࡣࡺࡻࡩࡥࠩᗾ") if bstack1111l1111l_opy_ == bstack11l1ll_opy_ (u"ࠪࡧࡦࡲ࡬ࠨᗿ") else bstack11l1ll_opy_ (u"ࠫ࡭ࡵ࡯࡬ࡡࡵࡹࡳࡥࡵࡶ࡫ࡧࠫᘀ")
            bstack11111ll1ll_opy_ = request.node.nodeid + (bstack11l1ll_opy_ (u"ࠬ࠭ᘁ") if bstack1111l1111l_opy_ == bstack11l1ll_opy_ (u"࠭ࡣࡢ࡮࡯ࠫᘂ") else bstack11l1ll_opy_ (u"ࠧ࠮ࠩᘃ") + bstack1111l1111l_opy_)
            bstack1111111l1l_opy_ = bstack1l11ll1l1l_opy_(_1l1l111l11_opy_.get(bstack11111ll1ll_opy_, None))
            if not bstack1111111l1l_opy_:
                continue
            for record in records:
                if bstack11lll1l1l1_opy_(record.message):
                    continue
                bstack1l11l1l11l_opy_.append({
                    bstack11l1ll_opy_ (u"ࠨࡶ࡬ࡱࡪࡹࡴࡢ࡯ࡳࠫᘄ"): datetime.datetime.utcfromtimestamp(record.created).isoformat() + bstack11l1ll_opy_ (u"ࠩ࡝ࠫᘅ"),
                    bstack11l1ll_opy_ (u"ࠪࡰࡪࡼࡥ࡭ࠩᘆ"): record.levelname,
                    bstack11l1ll_opy_ (u"ࠫࡲ࡫ࡳࡴࡣࡪࡩࠬᘇ"): record.message,
                    bstack11111l1ll1_opy_: bstack1111111l1l_opy_
                })
        if len(bstack1l11l1l11l_opy_) > 0:
            bstack11l1ll11_opy_.bstack1l1l1l11ll_opy_(bstack1l11l1l11l_opy_)
    except Exception as err:
        print(bstack11l1ll_opy_ (u"ࠬࡋࡸࡤࡧࡳࡸ࡮ࡵ࡮ࠡ࡫ࡱࠤࡸ࡫ࡣࡰࡰࡧࡣ࡫࡯ࡸࡵࡷࡵࡩ࠿ࠦࡻࡾࠩᘈ"), str(err))
def bstack11ll1l11_opy_(driver_command, response):
    if driver_command == bstack11l1ll_opy_ (u"࠭ࡳࡤࡴࡨࡩࡳࡹࡨࡰࡶࠪᘉ"):
        bstack11l1ll11_opy_.bstack1lll11ll_opy_({
            bstack11l1ll_opy_ (u"ࠧࡪ࡯ࡤ࡫ࡪ࠭ᘊ"): response[bstack11l1ll_opy_ (u"ࠨࡸࡤࡰࡺ࡫ࠧᘋ")],
            bstack11l1ll_opy_ (u"ࠩࡷࡩࡸࡺ࡟ࡳࡷࡱࡣࡺࡻࡩࡥࠩᘌ"): store[bstack11l1ll_opy_ (u"ࠪࡧࡺࡸࡲࡦࡰࡷࡣࡹ࡫ࡳࡵࡡࡸࡹ࡮ࡪࠧᘍ")]
        })
def bstack1lllll111l_opy_():
    global bstack11l1l1111_opy_
    bstack11l1ll11_opy_.bstack1l1l111111_opy_()
    for driver in bstack11l1l1111_opy_:
        try:
            driver.quit()
        except Exception as e:
            pass
def bstack1ll1l11l_opy_(self, *args, **kwargs):
    bstack1l111l11l_opy_ = bstack1l11l11ll_opy_(self, *args, **kwargs)
    bstack11l1ll11_opy_.bstack111111111_opy_(self)
    return bstack1l111l11l_opy_
def bstack1l1lllll1_opy_(framework_name):
    global bstack11ll11ll1_opy_
    global bstack1111llll1_opy_
    bstack11ll11ll1_opy_ = framework_name
    logger.info(bstack1111l11l1_opy_.format(bstack11ll11ll1_opy_.split(bstack11l1ll_opy_ (u"ࠫ࠲࠭ᘎ"))[0]))
    try:
        from selenium import webdriver
        from selenium.webdriver.common.service import Service
        from selenium.webdriver.remote.webdriver import WebDriver
        if bstack11l1llllll_opy_():
            Service.start = bstack11lll1ll1_opy_
            Service.stop = bstack1111llll_opy_
            webdriver.Remote.__init__ = bstack11lllll11_opy_
            webdriver.Remote.get = bstack1l1l111l1_opy_
            if not isinstance(os.getenv(bstack11l1ll_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣࡕ࡟ࡔࡆࡕࡗࡣࡕࡇࡒࡂࡎࡏࡉࡑ࠭ᘏ")), str):
                return
            WebDriver.close = bstack1ll1ll1l11_opy_
            WebDriver.quit = bstack1ll1l11lll_opy_
            WebDriver.getAccessibilityResults = getAccessibilityResults
            WebDriver.bstack1111l1111_opy_ = getAccessibilityResults
            WebDriver.getAccessibilityResultsSummary = getAccessibilityResultsSummary
            WebDriver.bstack1ll1lll11_opy_ = getAccessibilityResultsSummary
        if not bstack11l1llllll_opy_() and bstack11l1ll11_opy_.on():
            webdriver.Remote.__init__ = bstack1ll1l11l_opy_
        bstack1111llll1_opy_ = True
    except Exception as e:
        pass
    bstack1lll1l11l1_opy_()
    if os.environ.get(bstack11l1ll_opy_ (u"࠭ࡓࡆࡎࡈࡒࡎ࡛ࡍࡠࡑࡕࡣࡕࡒࡁ࡚࡙ࡕࡍࡌࡎࡔࡠࡋࡑࡗ࡙ࡇࡌࡍࡇࡇࠫᘐ")):
        bstack1111llll1_opy_ = eval(os.environ.get(bstack11l1ll_opy_ (u"ࠧࡔࡇࡏࡉࡓࡏࡕࡎࡡࡒࡖࡤࡖࡌࡂ࡛࡚ࡖࡎࡍࡈࡕࡡࡌࡒࡘ࡚ࡁࡍࡎࡈࡈࠬᘑ")))
    if not bstack1111llll1_opy_:
        bstack1l11lll1_opy_(bstack11l1ll_opy_ (u"ࠣࡒࡤࡧࡰࡧࡧࡦࡵࠣࡲࡴࡺࠠࡪࡰࡶࡸࡦࡲ࡬ࡦࡦࠥᘒ"), bstack1ll1l1lll1_opy_)
    if bstack111111lll_opy_():
        try:
            from selenium.webdriver.remote.remote_connection import RemoteConnection
            RemoteConnection._get_proxy_url = bstack1ll1llll11_opy_
        except Exception as e:
            logger.error(bstack1ll1l1111l_opy_.format(str(e)))
    if bstack11l1ll_opy_ (u"ࠩࡳࡽࡹ࡫ࡳࡵࠩᘓ") in str(framework_name).lower():
        if not bstack11l1llllll_opy_():
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
def bstack1ll1l11lll_opy_(self):
    global bstack11ll11ll1_opy_
    global bstack111l1l11_opy_
    global bstack1l11ll1ll_opy_
    try:
        if bstack11l1ll_opy_ (u"ࠪࡴࡾࡺࡥࡴࡶࠪᘔ") in bstack11ll11ll1_opy_ and self.session_id != None and bstack11111l11_opy_(threading.current_thread(), bstack11l1ll_opy_ (u"ࠫࡹ࡫ࡳࡵࡕࡷࡥࡹࡻࡳࠨᘕ"), bstack11l1ll_opy_ (u"ࠬ࠭ᘖ")) != bstack11l1ll_opy_ (u"࠭ࡳ࡬࡫ࡳࡴࡪࡪࠧᘗ"):
            bstack11l1l1l1l_opy_ = bstack11l1ll_opy_ (u"ࠧࡱࡣࡶࡷࡪࡪࠧᘘ") if len(threading.current_thread().bstackTestErrorMessages) == 0 else bstack11l1ll_opy_ (u"ࠨࡨࡤ࡭ࡱ࡫ࡤࠨᘙ")
            bstack1l1lll1l1_opy_(logger, True)
            if self != None:
                bstack1111ll1l1_opy_(self, bstack11l1l1l1l_opy_, bstack11l1ll_opy_ (u"ࠩ࠯ࠤࠬᘚ").join(threading.current_thread().bstackTestErrorMessages))
        threading.current_thread().testStatus = bstack11l1ll_opy_ (u"ࠪࠫᘛ")
    except Exception as e:
        logger.debug(bstack11l1ll_opy_ (u"ࠦࡊࡸࡲࡰࡴࠣࡻ࡭࡯࡬ࡦࠢࡰࡥࡷࡱࡩ࡯ࡩࠣࡷࡹࡧࡴࡶࡵ࠽ࠤࠧᘜ") + str(e))
    bstack1l11ll1ll_opy_(self)
    self.session_id = None
def bstack11lllll11_opy_(self, command_executor,
             desired_capabilities=None, browser_profile=None, proxy=None,
             keep_alive=True, file_detector=None, options=None):
    global CONFIG
    global bstack111l1l11_opy_
    global bstack1ll1ll1l1l_opy_
    global bstack1ll11l1ll1_opy_
    global bstack11ll11ll1_opy_
    global bstack1l11l11ll_opy_
    global bstack11l1l1111_opy_
    global bstack1lll1l1l1_opy_
    global bstack1l1111ll_opy_
    global bstack111111llll_opy_
    global bstack11l1llll_opy_
    CONFIG[bstack11l1ll_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࡗࡉࡑࠧᘝ")] = str(bstack11ll11ll1_opy_) + str(__version__)
    command_executor = bstack1ll1lll1_opy_(bstack1lll1l1l1_opy_)
    logger.debug(bstack11ll1l1l1_opy_.format(command_executor))
    proxy = bstack1l1ll11lll_opy_(CONFIG, proxy)
    bstack11111111_opy_ = 0
    try:
        if bstack1ll11l1ll1_opy_ is True:
            bstack11111111_opy_ = int(os.environ.get(bstack11l1ll_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤࡖࡌࡂࡖࡉࡓࡗࡓ࡟ࡊࡐࡇࡉ࡝࠭ᘞ")))
    except:
        bstack11111111_opy_ = 0
    bstack111lllll1_opy_ = bstack1llll1l1ll_opy_(CONFIG, bstack11111111_opy_)
    logger.debug(bstack111l1l1ll_opy_.format(str(bstack111lllll1_opy_)))
    bstack11l1llll_opy_ = CONFIG.get(bstack11l1ll_opy_ (u"ࠧࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࡵࠪᘟ"))[bstack11111111_opy_]
    if bstack11l1ll_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱࡌࡰࡥࡤࡰࠬᘠ") in CONFIG and CONFIG[bstack11l1ll_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࡍࡱࡦࡥࡱ࠭ᘡ")]:
        bstack1ll1111111_opy_(bstack111lllll1_opy_, bstack1l1111ll_opy_)
    if desired_capabilities:
        bstack1111111l1_opy_ = bstack1l1lll1111_opy_(desired_capabilities)
        bstack1111111l1_opy_[bstack11l1ll_opy_ (u"ࠪࡹࡸ࡫ࡗ࠴ࡅࠪᘢ")] = bstack1ll1l111_opy_(CONFIG)
        bstack1llll11l1_opy_ = bstack1llll1l1ll_opy_(bstack1111111l1_opy_)
        if bstack1llll11l1_opy_:
            bstack111lllll1_opy_ = update(bstack1llll11l1_opy_, bstack111lllll1_opy_)
        desired_capabilities = None
    if options:
        bstack1l1ll1l11l_opy_(options, bstack111lllll1_opy_)
    if not options:
        options = bstack1lll11lll_opy_(bstack111lllll1_opy_)
    if bstack1ll111l11_opy_.bstack1lll111lll_opy_(CONFIG, bstack11111111_opy_) and bstack1ll111l11_opy_.bstack111l11l1_opy_(bstack111lllll1_opy_, options):
        bstack111111llll_opy_ = True
        bstack1ll111l11_opy_.set_capabilities(bstack111lllll1_opy_, CONFIG)
    if proxy and bstack1lll1ll1l_opy_() >= version.parse(bstack11l1ll_opy_ (u"ࠫ࠹࠴࠱࠱࠰࠳ࠫᘣ")):
        options.proxy(proxy)
    if options and bstack1lll1ll1l_opy_() >= version.parse(bstack11l1ll_opy_ (u"ࠬ࠹࠮࠹࠰࠳ࠫᘤ")):
        desired_capabilities = None
    if (
            not options and not desired_capabilities
    ) or (
            bstack1lll1ll1l_opy_() < version.parse(bstack11l1ll_opy_ (u"࠭࠳࠯࠺࠱࠴ࠬᘥ")) and not desired_capabilities
    ):
        desired_capabilities = {}
        desired_capabilities.update(bstack111lllll1_opy_)
    logger.info(bstack1llllll11_opy_)
    if bstack1lll1ll1l_opy_() >= version.parse(bstack11l1ll_opy_ (u"ࠧ࠵࠰࠴࠴࠳࠶ࠧᘦ")):
        bstack1l11l11ll_opy_(self, command_executor=command_executor,
                  options=options, keep_alive=keep_alive, file_detector=file_detector)
    elif bstack1lll1ll1l_opy_() >= version.parse(bstack11l1ll_opy_ (u"ࠨ࠵࠱࠼࠳࠶ࠧᘧ")):
        bstack1l11l11ll_opy_(self, command_executor=command_executor,
                  desired_capabilities=desired_capabilities, options=options,
                  browser_profile=browser_profile, proxy=proxy,
                  keep_alive=keep_alive, file_detector=file_detector)
    elif bstack1lll1ll1l_opy_() >= version.parse(bstack11l1ll_opy_ (u"ࠩ࠵࠲࠺࠹࠮࠱ࠩᘨ")):
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
        bstack11ll11111_opy_ = bstack11l1ll_opy_ (u"ࠪࠫᘩ")
        if bstack1lll1ll1l_opy_() >= version.parse(bstack11l1ll_opy_ (u"ࠫ࠹࠴࠰࠯࠲ࡥ࠵ࠬᘪ")):
            bstack11ll11111_opy_ = self.caps.get(bstack11l1ll_opy_ (u"ࠧࡵࡰࡵ࡫ࡰࡥࡱࡎࡵࡣࡗࡵࡰࠧᘫ"))
        else:
            bstack11ll11111_opy_ = self.capabilities.get(bstack11l1ll_opy_ (u"ࠨ࡯ࡱࡶ࡬ࡱࡦࡲࡈࡶࡤࡘࡶࡱࠨᘬ"))
        if bstack11ll11111_opy_:
            bstack1ll11lll11_opy_(bstack11ll11111_opy_)
            if bstack1lll1ll1l_opy_() <= version.parse(bstack11l1ll_opy_ (u"ࠧ࠴࠰࠴࠷࠳࠶ࠧᘭ")):
                self.command_executor._url = bstack11l1ll_opy_ (u"ࠣࡪࡷࡸࡵࡀ࠯࠰ࠤᘮ") + bstack1lll1l1l1_opy_ + bstack11l1ll_opy_ (u"ࠤ࠽࠼࠵࠵ࡷࡥ࠱࡫ࡹࡧࠨᘯ")
            else:
                self.command_executor._url = bstack11l1ll_opy_ (u"ࠥ࡬ࡹࡺࡰࡴ࠼࠲࠳ࠧᘰ") + bstack11ll11111_opy_ + bstack11l1ll_opy_ (u"ࠦ࠴ࡽࡤ࠰ࡪࡸࡦࠧᘱ")
            logger.debug(bstack1ll1l1l111_opy_.format(bstack11ll11111_opy_))
        else:
            logger.debug(bstack1l1l1l11l_opy_.format(bstack11l1ll_opy_ (u"ࠧࡕࡰࡵ࡫ࡰࡥࡱࠦࡈࡶࡤࠣࡲࡴࡺࠠࡧࡱࡸࡲࡩࠨᘲ")))
    except Exception as e:
        logger.debug(bstack1l1l1l11l_opy_.format(e))
    bstack111l1l11_opy_ = self.session_id
    if bstack11l1ll_opy_ (u"࠭ࡰࡺࡶࡨࡷࡹ࠭ᘳ") in bstack11ll11ll1_opy_:
        threading.current_thread().bstackSessionId = self.session_id
        threading.current_thread().bstackSessionDriver = self
        threading.current_thread().bstackTestErrorMessages = []
        bstack11l1ll11_opy_.bstack111111111_opy_(self)
    bstack11l1l1111_opy_.append(self)
    if bstack11l1ll_opy_ (u"ࠧࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࡵࠪᘴ") in CONFIG and bstack11l1ll_opy_ (u"ࠨࡵࡨࡷࡸ࡯࡯࡯ࡐࡤࡱࡪ࠭ᘵ") in CONFIG[bstack11l1ll_opy_ (u"ࠩࡳࡰࡦࡺࡦࡰࡴࡰࡷࠬᘶ")][bstack11111111_opy_]:
        bstack1ll1ll1l1l_opy_ = CONFIG[bstack11l1ll_opy_ (u"ࠪࡴࡱࡧࡴࡧࡱࡵࡱࡸ࠭ᘷ")][bstack11111111_opy_][bstack11l1ll_opy_ (u"ࠫࡸ࡫ࡳࡴ࡫ࡲࡲࡓࡧ࡭ࡦࠩᘸ")]
    logger.debug(bstack1ll1ll1l1_opy_.format(bstack111l1l11_opy_))
def bstack1l1l111l1_opy_(self, url):
    global bstack11l111111_opy_
    global CONFIG
    try:
        bstack1lllllll1_opy_(url, CONFIG, logger)
    except Exception as err:
        logger.debug(bstack1ll1l1lll_opy_.format(str(err)))
    try:
        bstack11l111111_opy_(self, url)
    except Exception as e:
        try:
            bstack1llll111_opy_ = str(e)
            if any(err_msg in bstack1llll111_opy_ for err_msg in bstack11llllll1_opy_):
                bstack1lllllll1_opy_(url, CONFIG, logger, True)
        except Exception as err:
            logger.debug(bstack1ll1l1lll_opy_.format(str(err)))
        raise e
def bstack11llll1l_opy_(item, when):
    global bstack1l1l1l1ll_opy_
    try:
        bstack1l1l1l1ll_opy_(item, when)
    except Exception as e:
        pass
def bstack1lllll11l_opy_(item, call, rep):
    global bstack1lll11l111_opy_
    global bstack11l1l1111_opy_
    name = bstack11l1ll_opy_ (u"ࠬ࠭ᘹ")
    try:
        if rep.when == bstack11l1ll_opy_ (u"࠭ࡣࡢ࡮࡯ࠫᘺ"):
            bstack111l1l11_opy_ = threading.current_thread().bstackSessionId
            bstack1111111ll1_opy_ = item.config.getoption(bstack11l1ll_opy_ (u"ࠧࡴ࡭࡬ࡴࡘ࡫ࡳࡴ࡫ࡲࡲࡓࡧ࡭ࡦࠩᘻ"))
            try:
                if (str(bstack1111111ll1_opy_).lower() != bstack11l1ll_opy_ (u"ࠨࡶࡵࡹࡪ࠭ᘼ")):
                    name = str(rep.nodeid)
                    bstack1l111lll_opy_ = bstack1ll1lll1l_opy_(bstack11l1ll_opy_ (u"ࠩࡶࡩࡹ࡙ࡥࡴࡵ࡬ࡳࡳࡔࡡ࡮ࡧࠪᘽ"), name, bstack11l1ll_opy_ (u"ࠪࠫᘾ"), bstack11l1ll_opy_ (u"ࠫࠬᘿ"), bstack11l1ll_opy_ (u"ࠬ࠭ᙀ"), bstack11l1ll_opy_ (u"࠭ࠧᙁ"))
                    os.environ[bstack11l1ll_opy_ (u"ࠧࡑ࡛ࡗࡉࡘ࡚࡟ࡕࡇࡖࡘࡤࡔࡁࡎࡇࠪᙂ")] = name
                    for driver in bstack11l1l1111_opy_:
                        if bstack111l1l11_opy_ == driver.session_id:
                            driver.execute_script(bstack1l111lll_opy_)
            except Exception as e:
                logger.debug(bstack11l1ll_opy_ (u"ࠨࡇࡵࡶࡴࡸࠠࡪࡰࠣࡷࡪࡺࡴࡪࡰࡪࠤࡸ࡫ࡳࡴ࡫ࡲࡲࡓࡧ࡭ࡦࠢࡩࡳࡷࠦࡰࡺࡶࡨࡷࡹ࠳ࡢࡥࡦࠣࡷࡪࡹࡳࡪࡱࡱ࠾ࠥࢁࡽࠨᙃ").format(str(e)))
            try:
                bstack111l1111_opy_(rep.outcome.lower())
                if rep.outcome.lower() != bstack11l1ll_opy_ (u"ࠩࡶ࡯࡮ࡶࡰࡦࡦࠪᙄ"):
                    status = bstack11l1ll_opy_ (u"ࠪࡪࡦ࡯࡬ࡦࡦࠪᙅ") if rep.outcome.lower() == bstack11l1ll_opy_ (u"ࠫ࡫ࡧࡩ࡭ࡧࡧࠫᙆ") else bstack11l1ll_opy_ (u"ࠬࡶࡡࡴࡵࡨࡨࠬᙇ")
                    reason = bstack11l1ll_opy_ (u"࠭ࠧᙈ")
                    if status == bstack11l1ll_opy_ (u"ࠧࡧࡣ࡬ࡰࡪࡪࠧᙉ"):
                        reason = rep.longrepr.reprcrash.message
                        if (not threading.current_thread().bstackTestErrorMessages):
                            threading.current_thread().bstackTestErrorMessages = []
                        threading.current_thread().bstackTestErrorMessages.append(reason)
                    level = bstack11l1ll_opy_ (u"ࠨ࡫ࡱࡪࡴ࠭ᙊ") if status == bstack11l1ll_opy_ (u"ࠩࡳࡥࡸࡹࡥࡥࠩᙋ") else bstack11l1ll_opy_ (u"ࠪࡩࡷࡸ࡯ࡳࠩᙌ")
                    data = name + bstack11l1ll_opy_ (u"ࠫࠥࡶࡡࡴࡵࡨࡨࠦ࠭ᙍ") if status == bstack11l1ll_opy_ (u"ࠬࡶࡡࡴࡵࡨࡨࠬᙎ") else name + bstack11l1ll_opy_ (u"࠭ࠠࡧࡣ࡬ࡰࡪࡪࠡࠡࠩᙏ") + reason
                    bstack11l1l11ll_opy_ = bstack1ll1lll1l_opy_(bstack11l1ll_opy_ (u"ࠧࡢࡰࡱࡳࡹࡧࡴࡦࠩᙐ"), bstack11l1ll_opy_ (u"ࠨࠩᙑ"), bstack11l1ll_opy_ (u"ࠩࠪᙒ"), bstack11l1ll_opy_ (u"ࠪࠫᙓ"), level, data)
                    for driver in bstack11l1l1111_opy_:
                        if bstack111l1l11_opy_ == driver.session_id:
                            driver.execute_script(bstack11l1l11ll_opy_)
            except Exception as e:
                logger.debug(bstack11l1ll_opy_ (u"ࠫࡊࡸࡲࡰࡴࠣ࡭ࡳࠦࡳࡦࡶࡷ࡭ࡳ࡭ࠠࡴࡧࡶࡷ࡮ࡵ࡮ࠡࡥࡲࡲࡹ࡫ࡸࡵࠢࡩࡳࡷࠦࡰࡺࡶࡨࡷࡹ࠳ࡢࡥࡦࠣࡷࡪࡹࡳࡪࡱࡱ࠾ࠥࢁࡽࠨᙔ").format(str(e)))
    except Exception as e:
        logger.debug(bstack11l1ll_opy_ (u"ࠬࡋࡲࡳࡱࡵࠤ࡮ࡴࠠࡨࡧࡷࡸ࡮ࡴࡧࠡࡵࡷࡥࡹ࡫ࠠࡪࡰࠣࡴࡾࡺࡥࡴࡶ࠰ࡦࡩࡪࠠࡵࡧࡶࡸࠥࡹࡴࡢࡶࡸࡷ࠿ࠦࡻࡾࠩᙕ").format(str(e)))
    bstack1lll11l111_opy_(item, call, rep)
notset = Notset()
def bstack1ll11111l_opy_(self, name: str, default=notset, skip: bool = False):
    global bstack111llllll_opy_
    if str(name).lower() == bstack11l1ll_opy_ (u"࠭ࡤࡳ࡫ࡹࡩࡷ࠭ᙖ"):
        return bstack11l1ll_opy_ (u"ࠢࡃࡴࡲࡻࡸ࡫ࡲࡔࡶࡤࡧࡰࠨᙗ")
    else:
        return bstack111llllll_opy_(self, name, default, skip)
def bstack1ll1llll11_opy_(self):
    global CONFIG
    global bstack1llll1111l_opy_
    try:
        proxy = bstack1l111lll1_opy_(CONFIG)
        if proxy:
            if proxy.endswith(bstack11l1ll_opy_ (u"ࠨ࠰ࡳࡥࡨ࠭ᙘ")):
                proxies = bstack111l1ll11_opy_(proxy, bstack1ll1lll1_opy_())
                if len(proxies) > 0:
                    protocol, bstack1ll11ll1_opy_ = proxies.popitem()
                    if bstack11l1ll_opy_ (u"ࠤ࠽࠳࠴ࠨᙙ") in bstack1ll11ll1_opy_:
                        return bstack1ll11ll1_opy_
                    else:
                        return bstack11l1ll_opy_ (u"ࠥ࡬ࡹࡺࡰ࠻࠱࠲ࠦᙚ") + bstack1ll11ll1_opy_
            else:
                return proxy
    except Exception as e:
        logger.error(bstack11l1ll_opy_ (u"ࠦࡊࡸࡲࡰࡴࠣ࡭ࡳࠦࡳࡦࡶࡷ࡭ࡳ࡭ࠠࡱࡴࡲࡼࡾࠦࡵࡳ࡮ࠣ࠾ࠥࢁࡽࠣᙛ").format(str(e)))
    return bstack1llll1111l_opy_(self)
def bstack111111lll_opy_():
    return (bstack11l1ll_opy_ (u"ࠬ࡮ࡴࡵࡲࡓࡶࡴࡾࡹࠨᙜ") in CONFIG or bstack11l1ll_opy_ (u"࠭ࡨࡵࡶࡳࡷࡕࡸ࡯ࡹࡻࠪᙝ") in CONFIG) and bstack1l1l11lll_opy_() and bstack1lll1ll1l_opy_() >= version.parse(
        bstack11l1lll11_opy_)
def bstack1lll111l11_opy_(self,
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
    global bstack1ll1ll1l1l_opy_
    global bstack1ll11l1ll1_opy_
    global bstack11ll11ll1_opy_
    CONFIG[bstack11l1ll_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࡙ࡄࡌࠩᙞ")] = str(bstack11ll11ll1_opy_) + str(__version__)
    bstack11111111_opy_ = 0
    try:
        if bstack1ll11l1ll1_opy_ is True:
            bstack11111111_opy_ = int(os.environ.get(bstack11l1ll_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡑࡎࡄࡘࡋࡕࡒࡎࡡࡌࡒࡉࡋࡘࠨᙟ")))
    except:
        bstack11111111_opy_ = 0
    CONFIG[bstack11l1ll_opy_ (u"ࠤ࡬ࡷࡕࡲࡡࡺࡹࡵ࡭࡬࡮ࡴࠣᙠ")] = True
    bstack111lllll1_opy_ = bstack1llll1l1ll_opy_(CONFIG, bstack11111111_opy_)
    logger.debug(bstack111l1l1ll_opy_.format(str(bstack111lllll1_opy_)))
    if CONFIG.get(bstack11l1ll_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࡎࡲࡧࡦࡲࠧᙡ")):
        bstack1ll1111111_opy_(bstack111lllll1_opy_, bstack1l1111ll_opy_)
    if bstack11l1ll_opy_ (u"ࠫࡵࡲࡡࡵࡨࡲࡶࡲࡹࠧᙢ") in CONFIG and bstack11l1ll_opy_ (u"ࠬࡹࡥࡴࡵ࡬ࡳࡳࡔࡡ࡮ࡧࠪᙣ") in CONFIG[bstack11l1ll_opy_ (u"࠭ࡰ࡭ࡣࡷࡪࡴࡸ࡭ࡴࠩᙤ")][bstack11111111_opy_]:
        bstack1ll1ll1l1l_opy_ = CONFIG[bstack11l1ll_opy_ (u"ࠧࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࡵࠪᙥ")][bstack11111111_opy_][bstack11l1ll_opy_ (u"ࠨࡵࡨࡷࡸ࡯࡯࡯ࡐࡤࡱࡪ࠭ᙦ")]
    import urllib
    import json
    bstack1lllll1ll1_opy_ = bstack11l1ll_opy_ (u"ࠩࡺࡷࡸࡀ࠯࠰ࡥࡧࡴ࠳ࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮࠲ࡨࡵ࡭࠰ࡲ࡯ࡥࡾࡽࡲࡪࡩ࡫ࡸࡄࡩࡡࡱࡵࡀࠫᙧ") + urllib.parse.quote(json.dumps(bstack111lllll1_opy_))
    browser = self.connect(bstack1lllll1ll1_opy_)
    return browser
def bstack1lll1l11l1_opy_():
    global bstack1111llll1_opy_
    try:
        from playwright._impl._browser_type import BrowserType
        BrowserType.launch = bstack1lll111l11_opy_
        bstack1111llll1_opy_ = True
    except Exception as e:
        pass
def bstack11111ll1l1_opy_():
    global CONFIG
    global bstack1ll11ll111_opy_
    global bstack1lll1l1l1_opy_
    global bstack1l1111ll_opy_
    global bstack1ll11l1ll1_opy_
    CONFIG = json.loads(os.environ.get(bstack11l1ll_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡆࡓࡓࡌࡉࡈࠩᙨ")))
    bstack1ll11ll111_opy_ = eval(os.environ.get(bstack11l1ll_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡍࡘࡥࡁࡑࡒࡢࡅ࡚࡚ࡏࡎࡃࡗࡉࠬᙩ")))
    bstack1lll1l1l1_opy_ = os.environ.get(bstack11l1ll_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣࡍ࡛ࡂࡠࡗࡕࡐࠬᙪ"))
    bstack1lllll1l1_opy_(CONFIG, bstack1ll11ll111_opy_)
    bstack1lll111l1_opy_()
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
    if (bstack11l1ll_opy_ (u"࠭ࡨࡵࡶࡳࡔࡷࡵࡸࡺࠩᙫ") in CONFIG or bstack11l1ll_opy_ (u"ࠧࡩࡶࡷࡴࡸࡖࡲࡰࡺࡼࠫᙬ") in CONFIG) and bstack1l1l11lll_opy_():
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
        logger.debug(bstack11l1ll_opy_ (u"ࠨࡒ࡯ࡩࡦࡹࡥࠡ࡫ࡱࡷࡹࡧ࡬࡭ࠢࡳࡽࡹ࡫ࡳࡵ࠯ࡥࡨࡩࠦࡴࡰࠢࡵࡹࡳࠦࡰࡺࡶࡨࡷࡹ࠳ࡢࡥࡦࠣࡸࡪࡹࡴࡴࠩ᙭"))
    bstack1l1111ll_opy_ = CONFIG.get(bstack11l1ll_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡖࡸࡦࡩ࡫ࡍࡱࡦࡥࡱࡕࡰࡵ࡫ࡲࡲࡸ࠭᙮"), {}).get(bstack11l1ll_opy_ (u"ࠪࡰࡴࡩࡡ࡭ࡋࡧࡩࡳࡺࡩࡧ࡫ࡨࡶࠬᙯ"))
    bstack1ll11l1ll1_opy_ = True
    bstack1l1lllll1_opy_(bstack1ll1ll1ll1_opy_)
if (bstack11ll11l1l1_opy_()):
    bstack11111ll1l1_opy_()
@bstack1l1l1ll111_opy_(class_method=False)
def bstack1111111l11_opy_(hook_name, event, bstack11111l111l_opy_=None):
    if hook_name not in [bstack11l1ll_opy_ (u"ࠫࡸ࡫ࡴࡶࡲࡢࡪࡺࡴࡣࡵ࡫ࡲࡲࠬᙰ"), bstack11l1ll_opy_ (u"ࠬࡺࡥࡢࡴࡧࡳࡼࡴ࡟ࡧࡷࡱࡧࡹ࡯࡯࡯ࠩᙱ"), bstack11l1ll_opy_ (u"࠭ࡳࡦࡶࡸࡴࡤࡳ࡯ࡥࡷ࡯ࡩࠬᙲ"), bstack11l1ll_opy_ (u"ࠧࡵࡧࡤࡶࡩࡵࡷ࡯ࡡࡰࡳࡩࡻ࡬ࡦࠩᙳ"), bstack11l1ll_opy_ (u"ࠨࡵࡨࡸࡺࡶ࡟ࡤ࡮ࡤࡷࡸ࠭ᙴ"), bstack11l1ll_opy_ (u"ࠩࡷࡩࡦࡸࡤࡰࡹࡱࡣࡨࡲࡡࡴࡵࠪᙵ"), bstack11l1ll_opy_ (u"ࠪࡷࡪࡺࡵࡱࡡࡰࡩࡹ࡮࡯ࡥࠩᙶ"), bstack11l1ll_opy_ (u"ࠫࡹ࡫ࡡࡳࡦࡲࡻࡳࡥ࡭ࡦࡶ࡫ࡳࡩ࠭ᙷ")]:
        return
    node = store[bstack11l1ll_opy_ (u"ࠬࡩࡵࡳࡴࡨࡲࡹࡥࡴࡦࡵࡷࡣ࡮ࡺࡥ࡮ࠩᙸ")]
    if hook_name in [bstack11l1ll_opy_ (u"࠭ࡳࡦࡶࡸࡴࡤࡳ࡯ࡥࡷ࡯ࡩࠬᙹ"), bstack11l1ll_opy_ (u"ࠧࡵࡧࡤࡶࡩࡵࡷ࡯ࡡࡰࡳࡩࡻ࡬ࡦࠩᙺ")]:
        node = store[bstack11l1ll_opy_ (u"ࠨࡥࡸࡶࡷ࡫࡮ࡵࡡࡰࡳࡩࡻ࡬ࡦࡡ࡬ࡸࡪࡳࠧᙻ")]
    elif hook_name in [bstack11l1ll_opy_ (u"ࠩࡶࡩࡹࡻࡰࡠࡥ࡯ࡥࡸࡹࠧᙼ"), bstack11l1ll_opy_ (u"ࠪࡸࡪࡧࡲࡥࡱࡺࡲࡤࡩ࡬ࡢࡵࡶࠫᙽ")]:
        node = store[bstack11l1ll_opy_ (u"ࠫࡨࡻࡲࡳࡧࡱࡸࡤࡩ࡬ࡢࡵࡶࡣ࡮ࡺࡥ࡮ࠩᙾ")]
    if event == bstack11l1ll_opy_ (u"ࠬࡨࡥࡧࡱࡵࡩࠬᙿ"):
        hook_type = bstack111ll1l1l1_opy_(hook_name)
        uuid = uuid4().__str__()
        bstack1l11l1l1ll_opy_ = {
            bstack11l1ll_opy_ (u"࠭ࡵࡶ࡫ࡧࠫ "): uuid,
            bstack11l1ll_opy_ (u"ࠧࡴࡶࡤࡶࡹ࡫ࡤࡠࡣࡷࠫᚁ"): bstack1ll11111ll_opy_(),
            bstack11l1ll_opy_ (u"ࠨࡶࡼࡴࡪ࠭ᚂ"): bstack11l1ll_opy_ (u"ࠩ࡫ࡳࡴࡱࠧᚃ"),
            bstack11l1ll_opy_ (u"ࠪ࡬ࡴࡵ࡫ࡠࡶࡼࡴࡪ࠭ᚄ"): hook_type,
            bstack11l1ll_opy_ (u"ࠫ࡭ࡵ࡯࡬ࡡࡱࡥࡲ࡫ࠧᚅ"): hook_name
        }
        store[bstack11l1ll_opy_ (u"ࠬࡩࡵࡳࡴࡨࡲࡹࡥࡨࡰࡱ࡮ࡣࡺࡻࡩࡥࠩᚆ")].append(uuid)
        bstack111111l11l_opy_ = node.nodeid
        if hook_type == bstack11l1ll_opy_ (u"࠭ࡂࡆࡈࡒࡖࡊࡥࡅࡂࡅࡋࠫᚇ"):
            if not _1l1l111l11_opy_.get(bstack111111l11l_opy_, None):
                _1l1l111l11_opy_[bstack111111l11l_opy_] = {bstack11l1ll_opy_ (u"ࠧࡩࡱࡲ࡯ࡸ࠭ᚈ"): []}
            _1l1l111l11_opy_[bstack111111l11l_opy_][bstack11l1ll_opy_ (u"ࠨࡪࡲࡳࡰࡹࠧᚉ")].append(bstack1l11l1l1ll_opy_[bstack11l1ll_opy_ (u"ࠩࡸࡹ࡮ࡪࠧᚊ")])
        _1l1l111l11_opy_[bstack111111l11l_opy_ + bstack11l1ll_opy_ (u"ࠪ࠱ࠬᚋ") + hook_name] = bstack1l11l1l1ll_opy_
        bstack11111l1l1l_opy_(node, bstack1l11l1l1ll_opy_, bstack11l1ll_opy_ (u"ࠫࡍࡵ࡯࡬ࡔࡸࡲࡘࡺࡡࡳࡶࡨࡨࠬᚌ"))
    elif event == bstack11l1ll_opy_ (u"ࠬࡧࡦࡵࡧࡵࠫᚍ"):
        bstack1l1l1lll1l_opy_ = node.nodeid + bstack11l1ll_opy_ (u"࠭࠭ࠨᚎ") + hook_name
        _1l1l111l11_opy_[bstack1l1l1lll1l_opy_][bstack11l1ll_opy_ (u"ࠧࡧ࡫ࡱ࡭ࡸ࡮ࡥࡥࡡࡤࡸࠬᚏ")] = bstack1ll11111ll_opy_()
        bstack111111lll1_opy_(_1l1l111l11_opy_[bstack1l1l1lll1l_opy_][bstack11l1ll_opy_ (u"ࠨࡷࡸ࡭ࡩ࠭ᚐ")])
        bstack11111l1l1l_opy_(node, _1l1l111l11_opy_[bstack1l1l1lll1l_opy_], bstack11l1ll_opy_ (u"ࠩࡋࡳࡴࡱࡒࡶࡰࡉ࡭ࡳ࡯ࡳࡩࡧࡧࠫᚑ"), bstack11111l11ll_opy_=bstack11111l111l_opy_)
def bstack11111lll11_opy_():
    global bstack11111ll11l_opy_
    if bstack1l11ll11_opy_():
        bstack11111ll11l_opy_ = bstack11l1ll_opy_ (u"ࠪࡴࡾࡺࡥࡴࡶ࠰ࡦࡩࡪࠧᚒ")
    else:
        bstack11111ll11l_opy_ = bstack11l1ll_opy_ (u"ࠫࡵࡿࡴࡦࡵࡷࠫᚓ")
@bstack11l1ll11_opy_.bstack1111l11l1l_opy_
def bstack11111ll111_opy_():
    bstack11111lll11_opy_()
    if bstack1l1l11lll_opy_():
        bstack1l1l111l_opy_(bstack11ll1l11_opy_)
    bstack11l1l1ll11_opy_ = bstack11l1lll111_opy_(bstack1111111l11_opy_)
bstack11111ll111_opy_()