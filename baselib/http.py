import  requests,uuid,re,collections,json
from json import JSONDecodeError
import logging,yaml
import pytest,sys


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
            with open(r'C:\Users\Administrator\PycharmProjects\pytest_demo\baselib\config.yaml') as fp:
                self._config=yaml.load(fp.read())

        return self._config

    def config_add(self,ele):
        #ele为键值对
        self.config.update(**ele)





    def _raise_exception(self, msg):

        raise AssertionError(msg)


    def assert_true(self, condition, msg=None):
        if not condition:
            self._raise_exception(msg)

    def assert_false(self, false_condition, msg=None):
        if false_condition:
            self._raise_exception(msg)

    def assert_equals(self, expected, actual, msg=None):
        self.assert_true(expected == actual, msg)

    assert_eq = assert_equals

    def assert_not_equals(self, expected, actual, msg=None):
        self.assert_true(expected != actual, msg)

    assert_ne = assert_not_equals


    def assert_in(self, member, container, msg=None):
        self.assert_true(member in container, msg)

    def assert_not_in(self, member, container, msg=None):
        self.assert_true(member not in container, msg)



    def assert_http_status_code(self, expected_codes, msg=''):
        if self.resp is None:
            raise TimeoutError('需要先运行 http 请求, http_response 为 None')

        if isinstance(expected_codes, collections.Iterable):
            self.assert_in(self.resp.status_code,expected_codes)
        else:
            self.assert_eq(expected_codes, self.resp.status_code, msg)

    def assert_http_status_ok(self, msg=''):
        """2xx"""
        HTTP_OK_CODES = [200, 201, 203, 204, 205, 206, 207, 208, 226]

        self.assert_http_status_code(HTTP_OK_CODES,msg='sever is not ok')

    def assert_greater_than(self, greater, less, msg=None):
        self.assert_true(greater > less, msg)

    assert_gt = assert_greater_than

    def assert_greater_than_equals(self, expected, actual, msg=None):
        self.assert_true(actual >= expected, msg)

    assert_gte = assert_greater_than_equals

    def assert_less_than_equals(self, expected, actual, msg=None):
        self.assert_true(actual <= expected, msg)

    assert_lte = assert_less_than_equals


    def assert_match(self, pattern, s, flags=0, msg=None):
        """使用 re.match 进行匹配断言测试，注意与 assert_search 的区别
        """
        self.assert_true(re.match(pattern, s, flags) is not None, msg)

    def assert_full_match(self, pattern, s, flags=0, msg=None):
        """使用 re.fullmatch 进行匹配断言测试"""
        self.assert_true(re.fullmatch(pattern, s, flags) is not None, msg)

    def assert_search(self, pattern, s, flags=0, msg=None):
        """使用 re.search 进行搜索断言测试"""
        self.assert_true(re.search(pattern, s, flags), msg)




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
        req_log="""{}接口请求---------------------:\n
        {}\n
        """.format(str(method),str(payload))

        logging.info(msg=req_log)

        self.resp = requests.post(url, data=json.dumps(payload), headers=headers)
        try:
            resp_log="""{}接口返回+++++++++++++++++++\n
            {}\n
            """.format(str(method),self.resp.text)
            logging.info(msg=resp_log)

        except JSONDecodeError as e:
            raise TimeoutError('服务器返回的数据不是 JSON 格式, 返回的原始文本是:\n{}\n{}'.format('-' * 80, self.resp.text)) from e
        self.resp_json = self.resp.json()

        return self.resp


    def assert_jsonrpc_has_error(self, msg=''):
        self.assert_in('error', self.resp_json, msg)

    def assert_jsonrpc_has_result(self, msg=''):
        self.assert_in('result', self.resp_json, msg)

    def assert_jsonrpc_error_code(self, expected_code, msg=''):
        self.assert_in('code', self.rpc_error, '当获取 jsonrpc["error"]["code"] 字段时出错')
        self.assert_eq(expected_code, self.rpc_error['code'], msg)









