import  requests,uuid,re,collections,json
from json import JSONDecodeError
import logging,yaml,os
import pytest,sys
from baselib.verify import verify


class Httptest():

    def __init__(self):
        self.resp=None
        self.resp_json=None
        self.headers=None
        self.url=None
        self.data=None
        self.json=None
        self._config=None

    @property
    def config(self):

        if self._config==None:
            path=os.path.dirname(os.path.realname(__file__))
            configpath=os.path.join(path,'config.yaml')
            with open(configpath) as fp:
                self._config=yaml.load(fp.read())

        return self._config

    def config_add(self,ele):
        #ele为键值对
        self.config.update(**ele)



    def assert_http_status_code(self, expected_codes, msg=''):
        if self.resp is None:
            raise TimeoutError('需要先运行 http 请求, http_response 为 None')

        if isinstance(expected_codes, collections.Iterable):
            verify.assert_in(self.resp.status_code,expected_codes)
        else:
            verify.assert_eq(expected_codes, self.resp.status_code, msg)

    def assert_http_status_ok(self, msg=''):
        """2xx"""
        HTTP_OK_CODES = [200, 201, 203, 204, 205, 206, 207, 208, 226]

        self.assert_http_status_code(HTTP_OK_CODES,msg='sever is not ok')






class Jsonrpc(Httptest):
    """测试 JSONRPC 请求／响应"""


    @property
    def rpc_result(self):
        self.assert_jsonrpc_has_result('当获取 jsonrpc 的 result 字段时出错')
        return self.resp_json['result']

    @property
    def rpc_error(self):
        self.assert_jsonrpc_has_error('当获取 jsonrpc 的 error 字段时出错')
        return self.resp_json['error']


    def jsonrpc(self, url, method, *args, **kwargs):

        headers = {'content-type': 'application/json'}
        payload = {
            "jsonrpc": "2.0",
            "id": uuid.uuid4().hex,
            "method": method,
            "params": args if args else kwargs
        }

        logging.info(msg="""{}接口请求:""".format(str(method)))
        logging.info(msg="""\n{}""".format(str(payload)))

        self.resp = requests.post(url, data=json.dumps(payload), headers=headers)
        try:
            logging.info(msg="""{}接口返回""".format(str(method)))
            logging.info(msg="""\n{}""".format(self.resp.text))

        except JSONDecodeError as e:
            raise TimeoutError('服务器返回的数据不是 JSON 格式, 返回的原始文本是:\n{}\n{}'.format('-' * 80, self.resp.text)) from e
        self.resp_json = self.resp.json()
        logging.info(msg="""\n\n""")
        return self.resp


    def assert_jsonrpc_has_error(self, msg=''):
        verify.assert_in('error', self.resp_json, msg)

    def assert_jsonrpc_has_result(self, msg=''):
        verify.assert_in('result', self.resp_json, msg)

    def assert_jsonrpc_error_code(self, expected_code, msg=''):
        verify.assert_in('code', self.rpc_error, '当获取 jsonrpc["error"]["code"] 字段时出错')
        verify.assert_eq(expected_code, self.rpc_error['code'], msg)









