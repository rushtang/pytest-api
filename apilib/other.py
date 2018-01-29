from baselib.utils import Api_rpc,params_anchor
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
        code: {code}
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
        anchor=params_anchor(updateContent)

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
        print(params_yaml)
        if is_result==True:
            self._run_api('budget_updateSubject', params_yaml)
            return self.test.rpc_result
        else:
            self._run_api('budget_updateSubject', params_yaml,is_result=False)
            return self.test.rpc_error
