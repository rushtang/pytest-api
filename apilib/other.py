from baselib.utils import Api_rpc
import yaml




class Budget(Api_rpc):


    def listCategory (self,sessionId,keyword="",pageNo=0,pageSize=10):
        #科目大类列表,返回列表项为CategoryItem:{id：大类Id、name：大类名称}
        #keyword:'' 表示查全部
        params_yaml = """
        sessionId: {sessionId}
        keyword : '{keyword}'
        pageNo: {pageNo}
        pageSize: {pageSize}
        """.format(sessionId=sessionId,keyword=keyword,pageNo=pageNo,pageSize=pageSize)

        self._run_api('budget_listCategory', params_yaml)

        return self.test.rpc_result

    def addSubject (self,sessionId,categoryId,subject,code="",orderNum=0,is_result=True):
        #创建科目,返回科目Id

        params_yaml = """
        sessionId: {sessionId}
        categoryId : '{categoryId}'
        subject: {subject}
        code: '{code}'
        orderNum: {orderNum}
        """.format(sessionId=sessionId,categoryId=categoryId,subject=subject,code=code,orderNum=orderNum)
        if is_result==True:
            self._run_api('budget_addSubject', params_yaml)
            return self.test.rpc_result
        else:
            self._run_api('budget_addSubject', params_yaml,is_result=False)
            return self.test.rpc_error

    def updateSubject (self,sessionId,subjectId,updateContent=None,is_result=True):
        #更改科目,返回None, updateContent 更新内部
        """{
      String subject; //科目名称 （没有更新就不填）
      int categoryId; //大类Id  （没有更新就不填）
      String code; //自定义代码  （没有更新就不填）
      int orderNum; //排序号（没有更新就不填)
        }"""
        anchor=self.params_anchor(updateContent)
        anchor_yaml="""
        anchor: &anchor {{ {} }}
        """.format(anchor)


        params_yaml = """
        sessionId: {sessionId}
        subjectId : {subjectId}
        updateContent: 
            *anchor
        """.format(sessionId=sessionId,subjectId=subjectId)

        params_yaml=anchor_yaml+params_yaml

        if is_result==True:
            self._run_api('budget_updateSubject', params_yaml)
            return self.test.rpc_result
        else:
            self._run_api('budget_updateSubject', params_yaml,is_result=False)
            return self.test.rpc_error

    def deleteSubject(self,sessionId,subjectId,is_result=True):
        #删除科目,返回None

        params_yaml = """
        sessionId: {sessionId}
        subjectId: {subjectId}
        """.format(sessionId=sessionId,subjectId=subjectId)
        if is_result==True:
            return self._run_api('budget_deleteSubject', params_yaml)
        else:
            return self._run_api('budget_deleteSubject', params_yaml,is_result=False)


    def recoverSubject(self,sessionId,subjectId,is_result=True):
        #恢复科目,返回None

        params_yaml = """
        sessionId: {sessionId}
        subjectId: {subjectId}
        """.format(sessionId=sessionId,subjectId=subjectId)
        if is_result==True:
            return self._run_api('budget_recoverSubject', params_yaml)
        else:
            return self._run_api('budget_recoverSubject', params_yaml,is_result=False)

    def getSubject(self,sessionId,subjectId,is_result=True):
         #恢复科目,返回 SubjectItem{
         #   int id; //科目Id
         #   String name; //科目名称
         #   String code; //自定义码
         #   int categoryId; //大类Id
         #   String categoryName; //大类名称
         #   int orderNum; //排序号
         #   long createTime; //创建时间
         #   int status; //状态（0 正常，1 停用，2 删除
         #   int creator; //创建者
         # }

        params_yaml = """
        sessionId: {sessionId}
        subjectId: {subjectId}
        """.format(sessionId=sessionId,subjectId=subjectId)
        if is_result==True:
            return self._run_api('budget_getSubject', params_yaml)
        else:
            return self._run_api('budget_getSubject', params_yaml,is_result=False)

    def listSubject(self,sessionId,query,pageNo=0,pageSize=30):
        #获取科目列表，返回为Pagination<SubjectItem>
        #query{
           #    String name; //科目名称（可选）
           #    int categoryId; //大类Id （可选）
           #    int code; //自定义代码（可选）
           #    int status; //状态（0 正常，1 停用，2 删除）
           # }
        anchor = self.params_anchor(query)
        anchor_yaml = """
        anchor: &anchor {{ {} }}
        """.format(anchor)

        params_yaml = """
        sessionId: {sessionId}
        pageNo: {pageNo}
        pageSize: {pageSize}
        query: 
            *anchor
        """.format(sessionId=sessionId,pageNo=pageNo,pageSize=pageSize)


        params_yaml=anchor_yaml+params_yaml

        return self._run_api('budget_listSubject', params_yaml)

    def setUserAuth(self, sessionId, userId,subjectId,codes):
        # 设置科目限权,返回None

        params_yaml = """
        sessionId: {sessionId}
        userId: {userId}
        updateItems: 
            - {{ subjectId: {subjectId} }}
        """.format(sessionId=sessionId, userId=userId,subjectId=subjectId)
        params=yaml.load(params_yaml)
        params['updateItems'].append({'codes':codes})


        params_yaml = yaml.dump(params)
        print(params_yaml)
        return self._run_api('budget_setUserAuth', params_yaml)

    def listMySubject(self, sessionId, userId=0,pageNo=0,pageSize=30):
        # 获取科目限权表,返回 Pagination<SubjectAuthItem>

        params_yaml = """
        sessionId: {sessionId}
        userId: {userId}
        pageNo: {pageNo}
        pageSize: {pageSize}
            
        """.format(sessionId=sessionId, userId=userId,pageNo=pageNo,pageSize=pageSize)

        return self._run_api('budget_listMySubject', params_yaml)

