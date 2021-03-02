pytest-custom-nodeid: pytest plugin
==============

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
  - nodeid: `group_name::ids`

支持自定义分组 :`{分组名}` 或者 `{文件::Class}`

对测试用例名和nodeid进行重命名,方便多个参数化运行同一个测试类使用,也方便基于pytest-xdist的loadscope负载策略使用

对测试用例名和nodeid改为UTF-8编码,使其支持显示中文

因为`pytest-xdist`在使用`-x`(遇到失败就停止)时,如果任一用例失败将导致整个并发都停止运行

支持跳过机制,选中的组名将在该组首个用例运行失败后将剩下该组的用例所有跳过,

这功能在场景测试等存在用例依赖的测试集里面尤其好用,避免应该前序用例失败,无谓执行后续用例

格式:
    - 测试名: 进行参数化时的ids参数值
    - nodeid: `首字母大写分组名::ids名`


install
=====

`pip install pytest-custom-nodeid`

Usage
=====

command line:`pytest --rename={on:off} --skip=group_name --skip-json=absolute_path`

options:
- `--rename` It is used to open the plug-in, rename the marked use cases, code the unmarked use cases only, and close "off" by default
- `--skip` If it fails, the subsequent use case will be skipped. The tag name is needed here. 
  example: if the tag in IDS is '{login}', the skip tag is '--skip=login`
- `--skip-json` When there are too many tags to be marked, it can be stored in a JSON file. 
  Here you need to enter the absolute address, which can be used with 'skip'. The two tags will be combined. 
  
[JSON format](./demo.json)

tip: 
1. It supports running with pytest xdist, and can be concurrent with class according to loadscope policy
2. Use `{...}` as a marker custom grouping.
3. Support "{ filename::classname }" format for multi-level settings
4. `Skip` and `skip-json` are case-sensitive
5. Do not use '-x' in pytest-xdist. If the use case fails, the rest of the use cases will stop running

[JSON格式](./demo.json)

选项:
- `--rename`: 用于开启该插件,将对使用了标记的用例进行重命名,未标记的仅做编码处理,默认为"off"关闭
- `--skip`: 失败跳过后续用例,此处需要使用标记名作为标记.例如 ids中标记: `{Login}` 则跳过标记为:`--skip=Login` 
- `--skip-json`: 在需要标记的数量过多时,可用json文件存储.此处需要输入绝对地址,可与`skip`使用,两者标记将合并

小贴士:
1. skip和skip-json 大小写敏感
2. 在`parametrize`函数ids中,使用 `{...}` 分组标记
3. 支持pytest-xdist插件并发运行,可以按loadscope策略以class为单位进行并发   
4. 支持"{filename::classname}"这种格式进行多级设置
5. 请勿在pytest-xdist中使用`-x`,使用后若用例失败将导致其余用例全部停止运行

![](./images/allure1.png)


Demo
=====

```python
import pytest


@pytest.mark.parametrize("group", 
                         ["world", "hello", "hello", "hello", "world", "world"], 
                         ids=["group_4{group_1}", "group_5{group_2}", "group_6{file::class}", 
                              "group_7{group_1}", "group_8{group_2}", "group_9{file::class}"])
def test_05(group):
    a = "hello"
    assert a == group
```

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


`skip`标记到的分组,前序用例失败将导致后续用例跳过

使用了loadscope负载策略,因为存在三个组,所以会分成3组并发运行,并且nodeid将重命名为:
- group_1::group_4
- group_2::group_5
- file::class::group_6
- group_1::group_7
- group_2::group_8
- file::class::group_9


