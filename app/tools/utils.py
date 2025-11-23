#encoding:utf-8
import re
from datetime import datetime, timedelta
import random
import sys
from typing import List
from openpyxl import Workbook
from lunardate import LunarDate
from io import BytesIO

def return_img_stream(file_path):
    """
    工具函数:
    获取本地图片流
    :param file_path:文件单张图片的本地绝对路径
    :return: 图片流
    """
    import base64
    with open(file_path, "rb") as image_file:
        data = base64.b64encode(image_file.read()).decode('utf-8')
    # 获取文件扩展名
    file_extension = file_path.split('.')[-1]
    mime_type = f'image/{file_extension}' if file_extension in ['png', 'jpg', 'jpeg', 'gif'] else 'application/octet-stream'
    return f'data:{mime_type};base64,{data}'

def sanitize(value):
    if isinstance(value, str):
        return value.encode('utf-8', errors='replace').decode('latin1')
    return value
def generate_excel(data)->BytesIO:
    # 创建Excel文件（内存中）
    output = BytesIO()
    workbook = Workbook()
    workbook.encoding = 'latin-1'
    worksheet = workbook.active
    
    # 写入表头
    headers = list(data[0].keys())
    worksheet.append(headers)

    # 写入数据
    for row_data in data:
        worksheet.append(list(row_data.values()))

    workbook.save(output)
    output.seek(0)
    return output
def is_expire(input_date:datetime):
    if not input_date:
        return False
    return input_date < datetime.now()
def is_expire_after(input_date:datetime,hour=0,minute=0,second=0):
    if not input_date:
        return False
    return input_date < datetime.now() + timedelta(hours=hour, minutes=minute, seconds=second)
    
def convert_lunar_date(date_str, is_lunar)->str:
    # 解析输入日期
    now = datetime.now()
    input_date = datetime.strptime(date_str, "%Y-%m-%d")
    if is_lunar:
        d= LunarDate.fromSolarDate(now.year, input_date.month, input_date.day)
    else:
        d= datetime(now.year, input_date.month, input_date.day)
    return f"{d.year}-{d.month}-{d.day}"
names = ['星辰','晨曦','流光','若水','归途','初阳','南风','北岸','空白','繁花','清岚','星阑','云舟','青墨','烟川','沉羽','林疏','子默','南笙','北洛','景行','光霁','思远','文舟','安言','墨尘','轻舟','深雪','微光','苍梧','流年','飞鸿','景澄','玄清','慕白','归鸿','听松','若溪','静瑶','昭然','风吟','望舒','知秋','凌霄','楚歌','空谷','云归','素衣','青崖','沧浪','晨熙','景和','梓墨','玄戈','澄澈','夜阑','书遥','忘忧','云渺','景深','沧海','青衫','烟雨','星沉','空山','归人','景曜','玄霜','青禾']
def generateNickName(name:str):
    # 从names中随机选择一个名称然后和传入的名称组合成新的名称
    return random.choice(names)+name

def convert_timestamp_to_datetime(timestamp) -> datetime:
    """
    通用方法，自动处理以毫秒或秒为单位的时间戳
    
    Args:
        timestamp: 时间戳（可以是秒或毫秒单位）
        
    Returns:
        datetime: 转换后的datetime对象
    """
    # 判断时间戳单位：如果大于1e10，则认为是毫秒单位
    if timestamp > 1e10:
        # 毫秒单位，需要转换为秒
        timestamp_seconds = timestamp / 1000
    else:
        # 秒单位，直接使用
        timestamp_seconds = timestamp
    
    return datetime.fromtimestamp(timestamp_seconds)


def get_strings_params(text: str) -> list:
    """
    提取字符串中所有被{}包裹的内容
    
    Args:
        text (str): 输入的字符串
        
    Returns:
        list: 包含所有被{}包裹内容的列表
    """
    # 使用正则表达式查找所有被{}包裹的内容
    pattern = r'\{([^}]+)\}'
    matches = re.findall(pattern, text)
    return matches
def replace_str_params(text: str, **kwargs) -> str:
    """
    将字符串中被{}包裹的占位符替换为可变参数中对应的值
    
    Args:
        text (str): 包含占位符的原始字符串，占位符格式为 {key}
        **kwargs: 可变参数，键值对形式，用于替换占位符
        
    Returns:
        str: 替换占位符后的新字符串
        
    Example:
        >>> replace_braced_placeholders("Hello {name}, you are {age} years old", name="Alice", age=25)
        'Hello Alice, you are 25 years old'
    """
    result = text
    for key, value in kwargs.items():
        placeholder = f"{{{key}}}"
        result = result.replace(placeholder, str(value))
    return result


def tree(items, parentid=0)->List[object]:
    """
    优化后的树形结构生成函数，使用空间换时间策略
    时间复杂度: O(n)
    空间复杂度: O(n)
    """
    # 预处理：建立父子关系映射，用空间换时间
    children_map = {}
    item_dict = {}
    
    # 一次遍历构建映射关系
    for item in items:
        # 将item转换为字典并存储
        item_dict[item.id] = item.to_mini_dict()
        
        # 建立父节点到子节点的映射
        pid = item.parentId
        if pid not in children_map:
            children_map[pid] = []
        children_map[pid].append(item.id)
    
    def build_tree(pid):
        """递归构建树结构"""
        tree_items = []
        # 从映射中直接获取子节点，避免每次都遍历整个列表
        child_ids = children_map.get(pid, [])
        for cid in child_ids:
            item_data = item_dict[cid]
            # 递归构建子树
            item_data['children'] = build_tree(cid)
            tree_items.append(item_data)
        return tree_items
    
    return build_tree(parentid)

def loadClass(class_name):
    '''
    class_name: app.infra.models.infra_template,InfraTemplate
    '''
    model_path, model_class_name = class_name.rsplit(',', 1)  # 分割路径和类名
    module = __import__(model_path, fromlist=[model_class_name])      # 动态导入模块
    model_class = getattr(module, model_class_name)# 获取类对象
    return model_class