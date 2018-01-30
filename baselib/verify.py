import re


class Assert_test():


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

    def assert_jsonrpc_has_error(self, resp_json,msg=''):
        self.assert_in('error', resp_json, msg)

    def assert_jsonrpc_has_result(self,resp_json, msg=''):
        self.assert_in('result', resp_json, msg)

    def assert_jsonrpc_error_code(self, rpc_error,expected_code, msg=''):
        self.assert_in('code', rpc_error, '当获取 jsonrpc["error"]["code"] 字段时出错')
        self.assert_eq(expected_code, rpc_error['code'], msg)




verify=Assert_test()




def verify_equal(field_expect,field_result):
    #field_expect,field_result都为键值对
    print('\n+++++++++++++++++++++++   verify_field_expect:   +++++++++++++++++++++++++++++++\n\n')
    print(str(field_expect))
    print('\n\n')
    if len(field_expect)==0:
        verify.assert_equals(field_expect,field_result,msg=field_expect)
    for key, value in field_expect.items():
        verify.assert_equals(value, field_result[key], msg=key+' expect: '+str(value)+'----result: '+str(field_result[key])
                           +'\n field_expect: \n {} \n field_result: \n {}'.format(field_expect,field_result)
                           )



def verify_similar(field_expect,field_result):
    # field_expect,field_result都为键值对
    print('verify_similar: \n' + str(field_expect))
    if len(field_expect) == 0:
        verify.assert_equals(field_expect, field_result, msg=field_expect)
    for key, value in field_expect.items():
        verify.assert_equals(type(value), type(field_result[key]), msg=key + ':' + str(value))



def verify_Pagination(totalCount,expect_objects,result):
    #totalCount为int，objects为list，元素为dict
    # 默认objects内的元素是为有序的
    verify.assert_equals(totalCount, result['totalCount'], msg=result)
    if len(expect_objects)!=0:
        for index,expect_object in enumerate(expect_objects):
            verify_equal(expect_object,result['objects'][index])


def verfiy_empty(field_result,is_empty=False):
    print(field_result)
    if field_result is None:
        assert is_empty==True
    else:
        L=len(field_result)
        if is_empty==False:
            verify.assert_not_equals(L,0,msg='field_result is empty')
        else:
            verify.assert_equals(L,0,msg='field_result not is empty')