import re
import pytest


def pytest_addoption(parser):
    group = parser.getgroup("custom-nodeid", "custom rename nodeid and name")
    group.addoption("--rename",
                    action="store",
                    default="off",
                    choices=["on", "off"],
                    help="open rename testcase name and nodeid"
                    )


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
                item._nodeid = group_name.capitalize() + "::" + ids
