import platform
import json,os,re
import csv,time

class CodeUtil():
    @staticmethod
    def mkdir(path):
        if os.path.exists(path)==False:
            os.makedirs(path)    
    @staticmethod
    def IsWindows():
        sysstr = platform.system()
        return sysstr == "Windows"
    @staticmethod
    def GetOSPath(*args):
        return "/".join(args)

    @staticmethod
    def RemoveFile(file_path):
        if os.path.exists(file_path):
            os.remove(file_path)
    @staticmethod
    def ExistKeyInFile(file_path,key):
        try:
            file_obj = open(file_path, 'r', encoding='utf-8')
            all_text=file_obj.read()
            if all_text and all_text.index(key)>=0:
                print('exist',key)
                return True
        except Exception:
            pass
        return False
    @staticmethod
    def AppendString(file_path, content):
        CodeUtil.WriteTo(file_path,'\r'+content)
    @staticmethod
    def AppendLine(file_path, content):
        CodeUtil.WriteTo(file_path,'\n'+content)
    @staticmethod
    def WriteTo(file_path, content):
        directory = os.path.dirname(file_path)
        if directory:
            os.makedirs(directory, exist_ok=True) 
        with open(file_path, 'a+', encoding='utf-8') as f:
            f.write(content)
    @staticmethod
    def WriteToModel(file_path, content,model='w'):
        if not model:
            model='w'
        directory = os.path.dirname(file_path)
        if directory:
            os.makedirs(directory, exist_ok=True) 
        with open(file_path, model, encoding='utf-8') as f:
            f.write(content)
    @staticmethod
    def OvedrideWriteTo(file_path, content):
        file_obj = open(file_path, 'w', encoding='utf-8')
        file_obj.write(content)
        file_obj.close() 
    
    @staticmethod
    def LoadJson(file_path):
        with open(file_path, 'r', encoding='utf-8') as load_image:
            imageNames = json.load(load_image)
            load_image.close()
        return imageNames
    @staticmethod
    def ReadFileLines(file_path):
        with open(file_path,'r', encoding='utf-8') as r:
            lines=r.readlines()
            r.close()
            return lines
    @staticmethod
    def ReadFile(file_path):
        t=file_path
        if CodeUtil.IsWindows():
            t=t.replace('/', '\\')
        with open(t,'r', encoding='utf-8') as r:
            lines=r.read()
            r.close()
            return lines
    @staticmethod
    def str2Hump(text):
        '''转换为大驼峰ReadFile'''
        arr = filter(None, text.lower().split('_'))
        res = ''
        for i in arr:
            res =  res + i[0].upper() + i[1:]
        return res
    @staticmethod
    def str2MiniHump(text):
        '''转换小驼峰readFile'''
        arr = filter(None, text.lower().split('_'))
        res = ''
        for i in arr:
            res =  res + i[0].upper() + i[1:]
        return res[0].lower() + res[1:]
