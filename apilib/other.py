from baselib.utils import Api_rpc
import yaml




class Budget(Api_rpc):


    def setCategory(self,sessionId,name,orderNum=0):
        #创建科目大类,return 大类Id

        params_yaml = """
        sessionId: {sessionId}
        name: {name}
        orderNum: {orderNum}
        """.format(sessionId=sessionId,name=name,orderNum=orderNum)

        self._run_api('budget_setCategory', params_yaml)

        return self.test.rpc_result
