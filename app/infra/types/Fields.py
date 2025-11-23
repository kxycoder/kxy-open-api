from datetime import datetime
import json
import sys
from app.common.code_tool import CodeUtil
from typing import List
import re

from app.infra.models.infra_table import InfraTable
from app.infra.models.infra_table_fields import InfraTableFields

create_desc={
    'createuser':'创建人',
    'createdate':'创建时间',
    'lastmodifieduser':'修改人',
    'lastmodifieddate':'修改时间'
}
class Field():
    def __init__(self,):
        self.FieldName:str=''
        self.Description=''
        self.DataType='varchar'
        self.Length=0
        self.CanNull=True
        self.IsPrimaryKey=False
        self.IsAutoIncrement=False
        self.ShowInTable=True
        self.ShowInForm=True
        self.ShowDetail=True
        self.ShowInSerch=True
        self.DictType=''
        self.HtmlType=''
        self.Example=''
    def Set(self,fileName, des, dataType, isAutoIncrement, length, CanNull,isPrimaryKey=False):
        self.FieldName:str=fileName
        self.Description=des.strip()
        self.DataType=dataType
        self.Length=length
        self.CanNull=CanNull
        self.IsPrimaryKey=isPrimaryKey
        self.IsAutoIncrement=isAutoIncrement
        self.ShowInTable=False
        self.ShowInForm=False
        self.ShowDetail=False
        self.ShowInSerch=False
        if not des:
            self.Description=fileName    
        if not self.IsCreateInfo() and not self.IsMarkField() and not dataType=='text':
            self.ShowInTable=True
            self.ShowInForm=True
            self.ShowDetail=True
            self.ShowInSerch=True
        if self.IsMarkField():
            self.HtmlType='textarea'
        if dataType=='text':
            self.HtmlType='editor'
        if isPrimaryKey:
            self.ShowInForm=False
            self.ShowDetail=False
            self.ShowInSerch=False
    def GetJsonData(self):
        return {"FieldName":self.FieldName,"Description":self.Description,"DataType":self.DataType,"Length":self.Length,"CanNull":self.CanNull,"IsPrimaryKey":self.IsPrimaryKey,"IsAutoIncrement":self.IsAutoIncrement,"ShowInTable":self.ShowInTable,"ShowInForm":self.ShowInForm,"ShowDetail":self.ShowDetail,"ShowInSerch":self.ShowInSerch}
 
    def InitWithData(self,jsonData):
        self.FieldName=jsonData.get('FieldName')
        self.Description=jsonData.get('Description')
        self.DataType=jsonData.get('DataType')
        self.Length=jsonData.get('Length')
        self.CanNull=jsonData.get('CanNull')
        self.IsPrimaryKey=jsonData.get('IsPrimaryKey')
        self.IsAutoIncrement=jsonData.get('IsAutoIncrement')
        self.ShowInTable=jsonData.get('ShowInTable')
        self.ShowInForm=jsonData.get('ShowInForm')
        self.ShowDetail=jsonData.get('ShowDetail')
        self.ShowInSerch=jsonData.get('ShowInSerch')
    @staticmethod
    def InitWithEntity(fieldInfo:InfraTableFields):
        field = Field()
        field.FieldName=fieldInfo.fieldName
        field.Description=fieldInfo.description.strip()
        field.DataType=fieldInfo.dataType
        field.Length=fieldInfo.length
        field.CanNull=fieldInfo.canNull
        field.IsPrimaryKey=fieldInfo.isPrimaryKey
        field.IsAutoIncrement=fieldInfo.isAutoIncrement
        field.ShowInTable=fieldInfo.showInTable==1
        field.ShowInForm=fieldInfo.showInForm==1
        field.ShowDetail=fieldInfo.showDetail==1
        field.ShowInSerch=fieldInfo.showInSerch==1
        field.DictType = fieldInfo.dictType
        field.HtmlType = fieldInfo.htmlType
        field.Example = fieldInfo.example
        return field
        
    def IsCreateInfo(self):
        fieldName = self.FieldName.lower()
        return fieldName in ['isdelete','createuser', 'createdate', 'lastmodifieduser', 'lastmodifieddate','created_at','create_uid','updated_uid','updated_at','deleted','creator','updater','update_time','create_time','tenant_id']
    def GetCreateDes(self):
        return create_desc[self.FieldName.lower()]
    def GetDescription(self):
        if self.IsCreateInfo():
            return self.GetCreateDes()
        else:
            return self.Description
    def NameMiniTuoFeng(self):
        return CodeUtil.str2MiniHump(self.FieldName)
    def NameBigTuoFeng(self):
        return CodeUtil.str2Hump(self.FieldName)
    def IsInt(self):
        return self.DataType in ['int','tinyint','smallint','bigint','mediumint','mediumint']
    def IsString(self):
        return self.DataType in ['varchar','char','text']
    def IsNumber(self):
        return self.DataType in ['decimal','numeric']
    def IsDate(self):
        return self.DataType in ['date','timestamp','datetime']
    def IsMarkField(self):
        lowerField = self.FieldName.lower()
        if 'mark' in lowerField or 'content' in lowerField or 'remark' in lowerField:
            return True
        return False
    def PythonSqlAchemyTypeStr(self):
        result = ''
        if self.DataType=='bigint':
            result = 'BigInteger'
        elif self.IsInt():
            result = 'Integer'
        elif self.DataType == 'datetime':
            result = 'DateTime'
        else:
            result = 'String'
            if self.Length != None:
                result += f'({self.Length})'
        return result
    def PythonTypeStr(self):
        result = 'str'
        if self.IsInt():
            result = 'int'
        return result
    def JavaTypeStr(self):
        result = ''
        if self.IsString():
            result = 'String'
        elif self.IsDate():
            result = 'Date'
        elif self.IsInt():
            if 'date' in self.FieldName or 'time' in self.FieldName:
                result = 'Long'
            else:
                result = 'Integer'
        elif self.IsNumber():
            result = 'BigDecimal'
        return result
    def ReactTypeStr(self)->str:
        result = ''
        if self.IsString():
            result = 'string'
        elif self.IsDate():
            result = 'Date'
        elif self.IsInt() or self.IsNumber():
            result = 'number'
        else:
            result = 'string'
        return result
    def ApiFoxTypeStr(self):
        result = ''
        if self.IsString():
            result = 'string'
        elif self.IsDate():
            result = 'datetime'
        elif self.IsInt() or self.IsNumber():
            result = 'integer'
        return result

class Table():
    def __init__(self,tableName,des:str=''):
        self.TableName:str=tableName
        self.Fields:List[Field]=[]
        self.ModalName=CodeUtil.str2Hump(tableName)
        self.PrimaryKey=None
        self.TableDes= des
        self.field_array=None
        self.ParentPath=''
        self.ParentFolder=''
        self.Params = {}
        self.FieldNames ={}
        self.SubJoinMany = 1
        self.TreeParentColumn = ''
        self.TreeNameColumn = ''
        self.PageType='normal'
        self.ChildrenField=''
        self.Childrens:List[Table]=[]
        self.DictDatas = []
        self.DictTypes = {}
        if not des:
            self.TableDes=tableName
    @classmethod
    def InitWithData(cls, tableInfo: InfraTable, fields: List[InfraTableFields],dictTypes_dict,dictTypeDatas):
        table = cls(tableInfo.tableName, tableInfo.tableDes)
        # 设置表的基本信息
        if tableInfo.templateParam:
            table.Params = tableInfo.templateParam
        table.PageType = tableInfo.pageType
        table.SubJoinMany = tableInfo.subJoinMany
        table.TreeParentColumn = tableInfo.treeParentColumn
        table.TreeNameColumn = tableInfo.treeNameColumn
        table.ChildrenField = tableInfo.childrenField
        table.DictDatas = dictTypeDatas
        table.DictTypes = dictTypes_dict
        
        
        # 初始化字段列表
        table.Fields = []
        for field_info in fields:
            field = Field.InitWithEntity(field_info)
            table.Fields.append(field)
            table.FieldNames[field.FieldName.lower()] = field
            # 如果该字段是主键，则设置为主键字段
            if field.IsPrimaryKey:
                table.PrimaryKey = field
        
        return table
    def Has(self,fieldName):
        return fieldName in self.FieldNames
    def GetField(self,fieldName):
        return self.FieldNames[fieldName.lower()]
    def FieldsArray(self):
        if self.field_array is None:
            self.field_array=[field.FieldName for field in self.Fields]
        return self.field_array
    def SetPrimaryKey(self,key):
        fields=list(filter(lambda f:f.FieldName ==key, self.Fields))
        if fields:
            self.PrimaryKey=fields[0]
            fields[0].IsPrimaryKey=True
            fields[0].ShowInForm=False
            fields[0].ShowDetail=False
            fields[0].ShowInSerch=False
    def SetTableDes(self,des):
        self.TableDes=des
    def AddField(self,fileName, des, dataType, IsAutoIncrement, length, CanNull):
        f=Field()
        f.Set(fileName,des,dataType,IsAutoIncrement,length,CanNull)
        
        self.Fields.append(f)
        return f
    def GetJsonData(self):        
        return {
            "TableName":self.TableName,
            "PrimaryKey":self.PrimaryKey.FieldName,
            "TableDes":self.TableDes,
            "Fields":[item.GetJsonData() for item in self.Fields],
            "PageModel":'antSimple',
            "ParentPath":'',
            "ParentFolder":'',
            "DataBaseName":'',
        }
    def LoadJson(self,jsonData):
        self.TableName=jsonData["TableName"]
        self.ModalName=CodeUtil.str2Hump(self.TableName)
        self.PrimaryKey=jsonData.get("PrimaryKey","")
        self.TableDes=jsonData.get('TableDes',self.TableName)
        self.ParentFolder=jsonData.get('ParentFolder','')
        self.ParentPath=jsonData.get('ParentPath','')

        for field in jsonData['Fields']:
            f=Field()
            f.InitWithData(field)
            self.Fields.append(f)
            if f.FieldName==self.PrimaryKey:
                self.PrimaryKey=f
    @staticmethod
    def ParseTables(script:str):
        lines = script.split('\n')
        table = None
        tables:List[Table] = []
        begin = False
        for line in lines:
            try:
                line=line.strip()
                lowerLine = line.lower()
                if lowerLine.startswith("create table"):
                    tableName = line.split()[2].replace('`', '')
                    table = Table(tableName)
                    
                    begin = True
                    continue
                if begin == False:
                    continue
                
                if line is None or line == '' or lowerLine.startswith('unique key') or lowerLine.startswith('key'):
                    continue
                if 'ENGINE' in line[0:15]:
                    td = re.search(r'COMMENT\s*=\s*["\']([^"\']+)["\']', line)
                    if td:
                        tddes = td[1]
                        table.SetTableDes(tddes)
                    tables.append(table)
                    begin = False
                    continue
                    
                elif 'primary key' in lowerLine:
                    s = re.search(r'PRIMARY KEY \(`(.*?)`\)', line)
                    fieldName=s[1]
                    table.SetPrimaryKey(fieldName)
                else:
                    fieldInfo = line.split()
                    fieldName = fieldInfo[0].replace('`', '')
                    dbtype = ''
                    try:
                        if 'decimal' in fieldInfo[1]:
                            dbtype = 'decimal'
                            length = int(re.search(r'\((\d+).*?\)', 'decimal(18,  3)')[1])
                        else:
                            l = re.search(r'(.*?)\((.*?)\)', fieldInfo[1])
                            if l:
                                dbtype = l[1]
                                length = int(l[2])
                            else:
                                dbtype = fieldInfo[1]
                                length = 0
                    except Exception as e:
                        if not dbtype:
                            dbtype='varchar'
                        length=0
                    des = ''
                    c = re.search(r'COMMENT \'(.*?)\',', line)
                    if c:
                        des = c[1]
                    Auto = False
                    if 'AUTO_INCREMENT' in line:
                        Auto = True
                    CanNull = True
                    if fieldInfo[2] == 'NOT':
                        CanNull = False
                    table.AddField(fieldName, des, dbtype, Auto, length, CanNull)
            except Exception as e:
                raise Exception(f"解析{line} 出错：{e}")
        return tables
class Generator():
    def __init__(self):
        self.root_tempalte_path="./business/codetools/template"
        self.templatePath=''
        self.FieldFloder=""
        self.FileName=""
    def init(self,table:Table):
        self.TableEntity=table

    def ReadTemplate(self):
        # print(sys.argv[0])
        rootPath=CodeUtil.GetOSPath(self.root_tempalte_path,self.templatePath)
        return CodeUtil.ReadFile(rootPath)
    def replace(self,content,key,value):
        return content.replace(f'#{{{key}}}#',value)

    def ReplaceBaseTableInfo(self,content):
        content=self.replace(content,'modal_name',self.TableEntity.ModalName)
        content=self.replace(content,'model_name',self.TableEntity.ModalName)
        content=self.replace(content,'table_name',self.TableEntity.TableName)
        content=self.replace(content,'table_des',self.TableEntity.TableDes)
        content=self.replace(content,'now',datetime.now().strftime("%Y-%m-%d"))
        lowerName = self.TableEntity.ModalName[0].lower()+self.TableEntity.ModalName[1:]
        content=self.replace(content,'lower_modal_name',lowerName)
        return content

    def Generate(self)->str:
        tempStr=self.ReadTemplate()
        tempStr=self.ReplaceBaseTableInfo(tempStr)
        return tempStr

    def GenerateAndWrite(self,parent_path):
        filePath=self.GenerateFilePath(parent_path)
        content=self.Generate()
        CodeUtil.WriteTo(filePath,content)

    def GenerateFilePath(self,parent_path):
        fileFolder=self.ReplaceBaseTableInfo(self.GetSelfFileFolder())
        fileFolder=CodeUtil.GetOSPath(parent_path, fileFolder)
        CodeUtil.mkdir(fileFolder)
        fileName=self.ReplaceBaseTableInfo(self.FileName)
        return CodeUtil.GetOSPath(fileFolder, fileName)
    def GetSelfFileFolder(self):
        return self.FieldFloder