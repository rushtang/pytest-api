from baselib.utils import Api_rpc
import yaml




class User(Api_rpc):

    def __init__(self,test,num=0):
        super(User, self).__init__(test)
        self._num=num
        if str(num)=='0':
            self.account=test.config.get('employee_user_admin')
        else:
            self.account = test.config.get('employee_user'+str(num))
        self._session=None

    @property
    def sessionid(self):
        if self._session==None:
            self._session=self.login(self.account)

        return self._session

    @property
    def id(self):
        return self.getProfile(self.sessionid)


    def login(self,account):

        params_yaml = """
        account: {account}
        password: '123456'
        """.format(account=account)

        result=self._run_api('user_login',params_yaml)

        #返回sessionId
        return self.test.rpc_result

    def getProfile(self,sessionId,get='id'):
        params_yaml = """
            sessionId: {sessionId}
            """.format(sessionId=sessionId)
        self._run_api('user_getProfile', params_yaml)

        # 通常返回 id  nickname  mobile  employeeId
        return self.test.rpc_result[get]

