import inspect
from kxy.framework.mapper import Mapper

import os
import importlib

# 获取当前目录下所有.py文件（排除__init__.py）
api_files = [f for f in os.listdir(os.path.dirname(__file__)) if f.endswith(".py") and f != "__init__.py"]

# 动态加载每个文件中的路由
for file in api_files:
    module_name = file[:-3]  # 去掉.py后缀
    module = importlib.import_module(f".{module_name}", package="app.mall.services")
    # 遍历模块中的所有成员
    for name, obj in inspect.getmembers(module):
        # 筛选出类对象，且属于当前模块（排除import的类）
        if inspect.isclass(obj) and obj.__module__ == module.__name__:
            Mapper.register(obj)