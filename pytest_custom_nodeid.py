import re
import json
import pytest


def pytest_addoption(parser):
    group = parser.getgroup("custom-nodeid", "custom rename nodeid and name")
    group.addoption("--rename",
                    action="store",
                    default="off",
                    choices=["on", "off"],
                    help="open rename testcase name and nodeid"
                    )
    group.addoption("--skip", dest="skip", action="append", default=[],
                    help="list of Nodeid to skip (excluding IDS)")
    group.addoption("--skip-json", dest="json", action="store", default=False,
                    help="JSON file of nodeid to skip (excluding IDS)")


@pytest.mark.trylast
def pytest_collection_modifyitems(items):
    value = items[0].config.getvalue("rename")
    if value == "on":
        group_pattern = r"{([\w:]+)}"
        for item in items:
            item.name = item.name.encode("utf-8").decode("unicode_escape")
            item._nodeid = item.nodeid.encode("utf-8").decode("unicode_escape")
            rename = re.search(group_pattern, item.name)
            if rename:
                group_name = rename.group(1)
                ids = item.callspec.id.encode("utf-8").decode("unicode_escape").split("{")[0]
                item.name = ids
                item._nodeid = group_name + "::" + ids


class Skip:
    pattern = r"([\w:]+)::"
    status = dict()


def pytest_report_teststatus(report, config):
    if report.when == "call" and report.failed:
        fspath = re.search(Skip.pattern, report.nodeid).group(1)
        Skip.status.setdefault(fspath, True)


def pytest_runtest_setup(item):
    fspath = re.search(Skip.pattern, item.nodeid).group(1)
    if Skip.status.get(fspath, None) and fspath in getattr(Skip, "skip", None):
        pytest.skip("The previous use case fails and the subsequent use case skips")


def pytest_configure(config):
    data = []
    file = config.getoption("json")
    if file:
        with open(file, r'r') as f:
            data.extend(json.load(f)["skip"])

    skip = config.getoption("skip")
    if skip:
        data.extend(skip)
    setattr(Skip, "skip", data)


