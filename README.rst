pytest-custom-nodeid: pytest plugin
=======================================

Support custom grouping. `{group name}` or `{testfile::class}`

Rename testcases name and testcases nodeid, support allure report.

The loadscope load policy based on pytest-xdist is used.

Change testcases nodeid and testcases name encoding to UTF-8 and unicode escape

Because when 'pytest xdist' uses' - x '(stops when it fails), if any use case fails, the whole concurrency will stop running

The skip function is supported. The selected group name will skip all the remaining use cases of the group after the first use case of the group fails to run

This function is particularly useful in scenario testing and other test sets where use cases depend on each other,

to avoid failure of previous use cases and unnecessary execution of subsequent use cases

Format:
  - name: ids
  - nodeid: ``group_name::ids``

install
=======

``pip install pytest-custom-nodeid``

Usage
=====

command line:`pytest --rename={on:off} --skip=group_name --skip-json=absolute_path`

options:

- `--rename` It is used to open the plug-in, rename the marked use cases, code the unmarked use cases only, and close "off" by default
- `--skip` If it fails, the subsequent use case will be skipped. The tag name is needed here.
  example: if the tag in IDS is '{login}', the skip tag is '--skip=login`
- `--skip-json` When there are too many tags to be marked, it can be stored in a JSON file.
  Here you need to enter the absolute address, which can be used with 'skip'. The two tags will be combined

tip:

1. It supports running with pytest xdist, and can be concurrent with class according to loadscope policy
2. Use `{...}` as a marker custom grouping.
3. Support "{ filename::classname }" format for multi-level settings
4. `Skip` and `skip-json` are case-sensitive
5. Do not use '-x' in pytest-xdist. If the use case fails, the rest of the use cases will stop running

Demo
====

.. code-block:: python


    import pytest


    @pytest.mark.parametrize("group",
                             ["world", "hello", "hello", "hello", "world", "world"],
                             ids=["group_4{group_1}", "group_5{group_2}", "group_6{file::class}",
                                  "group_7{group_1}", "group_8{group_2}", "group_9{file::class}"])
    def test_05(group):
        a = "hello"
        assert a == group


cmd line: `pytest --rename=on --skip=group_1 --skip=group_2 --skip=file::class -n=auto --dist=loadscope`

`Skip` marks the group to which the preceding use case fails, causing subsequent use cases to skip

Using the loadscope load policy, because there are three groups, it will be divided into three groups to run concurrently

nodeid will be renamed to

- group_1::group_4
- group_2::group_5
- file::class::group_6
- group_1::group_7
- group_2::group_8
- file::class::group_9