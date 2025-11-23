class MenuTree:
    @staticmethod
    def ToTree(items,parentid='0',search = ''):
        tree=[] 
        for item in items:
            if item.ParentId==parentid:
                jitem=item.to_basic_dict()
                jitem['Children']=MenuTree.ToTree(items,item.Id,search)
                if search:
                    if search in item.Name:
                        tree.append(jitem)
                    else:
                        for child in jitem['Children']:
                            if search in child['Name']:
                                tree.append(child)
                else:
                    tree.append(jitem)
        tree.sort(key=lambda x:x['Sort'])
        return tree
    @staticmethod
    def ToTreeLower(items,parentid=0):
        tree=[] 
        for item in items:
            if item.parentId==parentid:
                jitem=item.to_mini_dict()
                jitem['children']=MenuTree.ToTreeLower(items,item.id)
                tree.append(jitem)
        tree.sort(key=lambda x:x['sort'])
        return tree
    
    @staticmethod
    def ToTreeLowerJson(items,parentid='0'):
        tree=[] 
        for jitem in items:
            if jitem['ParentId']==parentid:                
                jitem['children']=MenuTree.ToTreeLowerJson(items,jitem['Id'])
                tree.append(jitem)
        tree.sort(key=lambda x:x['Sort'])
        return tree
    
    @staticmethod
    def ToTreeLowerAnt(items,parentid=0):
        tree=[] 
        for item in items:
            if item.ParentId==parentid:
                jitem=item.to_basic_dict_lower_ant()
                jitem['children']=MenuTree.ToTreeLowerAnt(items,item.Id)
                tree.append(jitem)
        tree.sort(key=lambda x:x['sort'])
        return tree
    def get_trees(self,
                  data,
                  key_column='Id',
                  parent_column='TreePId',
                  child_column='children'
                  ):
        """
            :param data: 数据列表
            :param key_column: 主键字段，默认id
            :param parent_column: 父ID字段名，父ID默认从0开始
            :param child_column: 子列表字典名称
            :param fields: 挑选部分字段
            :return:数结构
        """
        data_dic = {d.get(key_column) : d for d in data}  # 以自己的权限主键为键,以新构建的字典为值,构造新的字典

        data_tree_list = []  # 整个数据大列表
        for d_id, d_dic in data_dic.items():
            pid = d_dic.get(parent_column)  # 取每一个字典中的父id
            if not pid:  # 父id=0，就直接加入数据大列表
                data_tree_list.append(d_dic)
            else:  # 父id>0 就加入父id队对应的那个的节点列表
                try:  # 判断异常代表有子节点，增加子节点列表=[]
                    data_dic[pid][child_column].append(d_dic)
                except KeyError:
                    if data_dic.get(pid) is None:
                        data_tree_list.append(d_dic)
                    else:
                        data_dic[pid][child_column] = []
                        data_dic[pid][child_column].append(d_dic)
        return data_tree_list

    def recursion(self,
                  data,
                  l=None):
        """
        :param data:
        :param l:
        :return:
        """
        if l is None:
            l = []
        for i in data:
            if 'children' in i:
                children=i.pop('children')
                l.append(i)
                self.recursion(children,l)
            else:
                l.append(i)
        return l

if __name__ == "__main__":
    data = [{'Id': 1, 'BusiMenuId': 1, 'MenuGrpId': 1, 'MenuFuncId': 1, 'Name': 'dsadasd', 'TreePId': 0, 'Icon': '', 'Level': 1,
             'Remark': '', 'IsActive': '', 'IsInsideLink': '', 'IsNotSugOpen': '', 'IsShowHeadMenu': '', 'DisplayIndex': 1,
             'IsEnableAppMarket': '', 'AppStamp': 1, 'AppIcon': '', 'AppSystem': 1, 'AppCategory': 1, 'AppDetailURL': '',
             'AppSummary': '', 'IterationId': 1, 'CreateUser': '152', 'CreateDate': '2022-04-22 14:35:33', 'LastModifiedUser':
                 '152', 'LastModifiedDate': '2022-04-22 14:35:33', 'IsNew': '', 'IsScenario': 1, 'IsWhiteTest': True, 'AppStampV2': ''},
            {'Id': 2, 'BusiMenuId': 1, 'MenuGrpId': 1, 'MenuFuncId': 1, 'Name': '', 'TreePId': 8, 'Icon': '', 'Level': 1, 'Remark': '', 'IsActive': '', 'IsInsideLink': '', 'IsNotSugOpen': '', 'IsShowHeadMenu': '', 'DisplayIndex': 1, 'IsEnableAppMarket': '', 'AppStamp': 1, 'AppIcon': '', 'AppSystem': 1, 'AppCategory': 1, 'AppDetailURL': '', 'AppSummary': '', 'IterationId': 1, 'CreateUser': '152', 'CreateDate': '2022-04-22 14:41:29', 'LastModifiedUser': '152', 'LastModifiedDate': '2022-04-22 14:41:29', 'IsNew': '', 'IsScenario': 1, 'IsWhiteTest': True, 'AppStampV2': ''}, {'Id': 3, 'BusiMenuId': 1, 'MenuGrpId': 1, 'MenuFuncId': 1, 'Name': '', 'TreePId': 1, 'Icon': '', 'Level': 1, 'Remark': '', 'IsActive': '', 'IsInsideLink': '', 'IsNotSugOpen': '', 'IsShowHeadMenu': '', 'DisplayIndex': 1, 'IsEnableAppMarket': '', 'AppStamp': 1, 'AppIcon': '', 'AppSystem': 1, 'AppCategory': 1, 'AppDetailURL': '', 'AppSummary': '', 'IterationId': 1, 'CreateUser': '152', 'CreateDate': '2022-04-22 14:42:05', 'LastModifiedUser': '152', 'LastModifiedDate': '2022-04-22 14:42:05', 'IsNew': '', 'IsScenario': 1, 'IsWhiteTest': True, 'AppStampV2': ''}, {'Id': 4, 'BusiMenuId': 1, 'MenuGrpId': 1, 'MenuFuncId': 1, 'Name': '', 'TreePId': 1, 'Icon': '', 'Level': 1, 'Remark': '', 'IsActive': '', 'IsInsideLink': '', 'IsNotSugOpen': '', 'IsShowHeadMenu': '', 'DisplayIndex': 1, 'IsEnableAppMarket': '', 'AppStamp': 1, 'AppIcon': '', 'AppSystem': 1, 'AppCategory': 1, 'AppDetailURL': '', 'AppSummary': '', 'IterationId': 1, 'CreateUser': '152', 'CreateDate': '2022-04-22 14:43:40', 'LastModifiedUser': '152', 'LastModifiedDate': '2022-04-22 14:43:40', 'IsNew': '', 'IsScenario': 1, 'IsWhiteTest': True, 'AppStampV2': ''}, {'Id': 5, 'BusiMenuId': 1, 'MenuGrpId': 1, 'MenuFuncId': 1, 'Name': '', 'TreePId': 1, 'Icon': '', 'Level': 1, 'Remark': '', 'IsActive': '', 'IsInsideLink': '', 'IsNotSugOpen': '', 'IsShowHeadMenu': '', 'DisplayIndex': 1, 'IsEnableAppMarket': '', 'AppStamp': 1, 'AppIcon': '', 'AppSystem': 1, 'AppCategory': 1, 'AppDetailURL': '', 'AppSummary': '', 'IterationId': 1, 'CreateUser': '152', 'CreateDate': '2022-04-22 14:45:05', 'LastModifiedUser': '152', 'LastModifiedDate': '2022-04-22 14:45:05', 'IsNew': '', 'IsScenario': 1, 'IsWhiteTest': True, 'AppStampV2': ''}, {'Id': 6, 'BusiMenuId': 1, 'MenuGrpId': 1, 'MenuFuncId': 1, 'Name': '', 'TreePId': 1, 'Icon': '', 'Level': 1, 'Remark': '', 'IsActive': '', 'IsInsideLink': '', 'IsNotSugOpen': '', 'IsShowHeadMenu': '', 'DisplayIndex': 1, 'IsEnableAppMarket': '', 'AppStamp': 1, 'AppIcon': '', 'AppSystem': 1, 'AppCategory': 1, 'AppDetailURL': '', 'AppSummary': '', 'IterationId': 1, 'CreateUser': '152', 'CreateDate': '2022-04-22 14:49:57', 'LastModifiedUser': '152', 'LastModifiedDate': '2022-04-22 14:49:57', 'IsNew': '', 'IsScenario': 1, 'IsWhiteTest': True, 'AppStampV2': ''}, {'Id': 7, 'BusiMenuId': 1, 'MenuGrpId': 1, 'MenuFuncId': 1, 'Name': '', 'TreePId': 1, 'Icon': '', 'Level': 1, 'Remark': '', 'IsActive': '', 'IsInsideLink': '', 'IsNotSugOpen': '', 'IsShowHeadMenu': '', 'DisplayIndex': 1, 'IsEnableAppMarket': '', 'AppStamp': 1, 'AppIcon': '', 'AppSystem': 1, 'AppCategory': 1, 'AppDetailURL': '', 'AppSummary': '', 'IterationId': 1, 'CreateUser': '152', 'CreateDate': '2022-04-22 14:51:20', 'LastModifiedUser': '152', 'LastModifiedDate': '2022-04-22 14:51:20', 'IsNew': '', 'IsScenario': 1, 'IsWhiteTest': True, 'AppStampV2': ''}, {'Id': 8, 'BusiMenuId': 1, 'MenuGrpId': 1, 'MenuFuncId': 1, 'Name': '', 'TreePId': 1, 'Icon': '', 'Level': 1, 'Remark': '', 'IsActive': '', 'IsInsideLink': '', 'IsNotSugOpen': '', 'IsShowHeadMenu': '', 'DisplayIndex': 1, 'IsEnableAppMarket': '', 'AppStamp': 1, 'AppIcon': '', 'AppSystem': 1, 'AppCategory': 1, 'AppDetailURL': '', 'AppSummary': '', 'IterationId': 1, 'CreateUser': '152', 'CreateDate': '2022-04-22 14:53:45', 'LastModifiedUser': '152', 'LastModifiedDate': '2022-04-22 14:53:45', 'IsNew': '', 'IsScenario': 1, 'IsWhiteTest': True, 'AppStampV2': ''}, {'Id': 9, 'BusiMenuId': 1, 'MenuGrpId': 1, 'MenuFuncId': 1, 'Name': '测试数据{{now}}', 'TreePId': 1, 'Icon': '测试数据{{now}}', 'Level': 1, 'Remark': '测试数据{{now}}', 'IsActive': '1', 'IsInsideLink': '1', 'IsNotSugOpen': '1', 'IsShowHeadMenu': '1', 'DisplayIndex': 1, 'IsEnableAppMarket': '1', 'AppStamp': 1, 'AppIcon': '测试数据{{now}}', 'AppSystem': 1, 'AppCategory': 1, 'AppDetailURL': '测试数据{{now}}', 'AppSummary': '测试数据{{now}}', 'IterationId': 1, 'CreateUser': '43', 'CreateDate': '2022-04-22 16:28:31', 'LastModifiedUser': '43', 'LastModifiedDate': '2022-04-22 16:28:31', 'IsNew': '1', 'IsScenario': 1, 'IsWhiteTest': True, 'AppStampV2': '测试数据{{now}}'}]
    a = MenuTree().get_trees(data)
    # b= recursion(a)
    print(a)