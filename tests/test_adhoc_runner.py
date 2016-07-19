from pyansiwrapper.runner import AdHoc, Task


def test_adhoc():

    AdHoc()\
        .task(Task.module("ping"))\
        .hosts('localhost')\
        .run()


def test_adhost_multiple_tasks():
    AdHoc() \
        .task(Task.module("shell").args("echo $PATH").register('path_var')) \
        .task(Task.module("debug").args({"var": "path_var"})) \
        .hosts('localhost') \
        .run()
