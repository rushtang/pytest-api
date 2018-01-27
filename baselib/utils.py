from baselib.http import Jsonrpc
import yaml,os



class Api_rpc():
    def __init__(self,test):
        self.URL=test.config.get('http.url')

        self.test=test

    def _run_api(self,method,params_yaml, URL=None, is_result=True):
        params = yaml.load(params_yaml)
        if URL == None:
            URL = self.URL
        test=self.test
        test.jsonrpc(URL, method, **params)
        test.assert_http_status_ok('http 状态码正确')
        if is_result == True:
            test.assert_jsonrpc_has_result('返回应该有result')
            return test.rpc_result
        else:
            test.assert_jsonrpc_has_error('返回应该有error')
            return test.rpc_error


def mysql_exec(test,source,db='xw'):
    mysql_sys = test.config.get("mysql.sys")
    host = test.config.get("mysql.host")
    port = test.config.get("mysql.port")
    user = test.config.get("mysql.user")
    password = test.config.get("mysql.password")

    try:
        command = '{sys} -h {host} -u{user} -p{password} -P {port} -D {db} < {source}'.format(sys=mysql_sys, host=host,
                                                                                              user=user,
                                                                                              password=password,
                                                                                              port=port,
                                                                                              db=db, source=source)
        os.system(command)
        print('清除成功！')
    except:
        raise SystemError("sql执行错误")


def delete_exec(test):
    delete_sql=test.config.get("mysql.delete")
    mysql_exec(test, delete_sql)




