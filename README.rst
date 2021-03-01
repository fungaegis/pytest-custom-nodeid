pytest-custom-nodeid: pytest plugin
=======================================

Support custom grouping. ``{group name}`` or ``{testfile::class}``

Rename testcases name and testcases nodeid, support allure report.

The loadscope load policy based on pytest-xdist is used.

Change testcases nodeid and testcases name encoding to UTF-8 and unicode escape

Format:
  - name: ids
  - nodeid: ``group_name::ids``

install
=======

``pip install pytest-custom-nodeid``

Usage
=====

command line:``pytest --rename={on:off}``

tip: It supports running with pytest xdist, and can be concurrent with class according to loadscope policy

options:
  - rename: Used to open plugin, default "off"

Use ``{...}`` as a marker custom grouping.

Support "{ filename::classname }" format for multi-level settings

Demo
====

.. code-block:: python


    import pytest


    @pytest.mark.parametrize("group",
                             ["group_4", "group_5", "group_6"],
                             ids=["group_4{group_1}", "group_5{group_2}", "group_6{file:class}"])
    def test_05(group):
        a = "hello"
        b = "world"
        assert a == b


cmcmd line: `pytest --rename=on -n=auto --dist=loadscope`

Using the loadscope load policy, because there are three groups, it will be divided into three groups to run concurrently