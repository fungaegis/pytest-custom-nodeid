from setuptools import setup

"""
author: fungaegis
github: https://github.com/fungaegis/pytest-custom-nodeid
"""
with open("./README.rst", "r") as readme:
    long_description = readme.read()
setup(
    name='pytest-custom-nodeid',
    url='https://github.com/fungaegis/pytest-custom-nodeid',
    version='0.2',
    author="fungaegis",
    author_email="fungaegis@gmail.com",
    description='Custom grouping for pytest-xdist, rename test cases name and test cases nodeid, support allure report',
    long_description=long_description,
    classifiers=[
        'Framework :: Pytest',
        'Programming Language :: Python :: 3',
        'Topic :: Software Development :: Testing',
        'Programming Language :: Python :: 3.7',
    ],
    license='MIT License',
    py_modules=['pytest_custom_nodeid'],
    keywords=[
        'pytest', 'py.test', 'pytest_custom_nodeid', 'concurrency', 'xdist', 'pytest-xdist', 'allure',
        'rename', 'name', 'skip'
    ],

    install_requires=[
        'pytest'
    ],
    entry_points={
        'pytest11': [
            'custom_nodeid = pytest_custom_nodeid',
        ]
    }
)
