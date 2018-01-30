import pytest
import sys
sys.path.append(r'C:\Users\Administrator\PycharmProjects\pytest_demo')

from baselib.data import Base_test
from apilib.base import User
from apilib.other import Budget
from baselib.verify import verify_equal,verify



class Test_listCategory(Base_test):
    #budget_listCategory

    def test_case1(self):
        #查全部
        result=Budget(self.test).listCategory(self.user0.sessionid,keyword='')

        print('科目大类列表:\n',result)

    def test_case2(self):
        #关键字查询

        result = Budget(self.test).listCategory(self.user0.sessionid, keyword='大类1')

        print('科目大类查询时返回项:\n', result)


class Test_addSubject(Base_test):

    @pytest.fixture(scope="class")
    def categoryId(self):
        result = Budget(self.test).listCategory(self.user0.sessionid)
        return result['objects'][0]['id']


    def test_case1(self,categoryId):
        #正常添加科目
        subjectId=Budget(self.test).addSubject(self.user0.sessionid,categoryId,subject='科目1',code='233')
        print('添加的科目ID为\n',subjectId)

        field_expect=Budget(self.test).getSubject(self.user0.sessionid,subjectId)['id']
        verify.assert_eq(field_expect,subjectId)

    def test_case_exp1(self,categoryId):
        #科目编号已存在
        error = Budget(self.test).addSubject(self.user0.sessionid, categoryId, subject='科目XX', code='233',is_result=False)

        print('期望报科目编号已存在的错误\n', error)
        verify.assert_jsonrpc_error_code(error,-29640)


    def test_case_exp2(self,categoryId):
        #科目名称已存在
        error = Budget(self.test).addSubject(self.user0.sessionid, categoryId, subject='科目1', code='280',is_result=False)
        print('期望报科目名称已存在的错误\n',error)
        verify.assert_jsonrpc_error_code(error, -29639)


    def test_case_exp3(self):
        #科目分类不存在
        categoryId=1122
        error = Budget(self.test).addSubject(self.user0.sessionid, categoryId, subject='科目2', code='300',is_result=False)
        print('期望报科目分类不存在的错误\n',error)
        verify.assert_jsonrpc_error_code(error, -29638)


class Test_updateSubject(Base_test):

    @property
    def Category(self):
        result=Budget(self.test).listCategory(self.user0.sessionid)
        return result['objects']

    @pytest.fixture(scope="class")
    def subjectId(self):
        categoryId=self.Category[0]['id']
        result = Budget(self.test).addSubject(self.user0.sessionid,categoryId,subject='科目1',code='233')
        return result

    def test_case1(self,subjectId):
        #正常更改科目,更改为空
        field_expect=Budget(self.test).getSubject(self.user0.sessionid,subjectId)
        result=Budget(self.test).updateSubject(self.user0.sessionid,subjectId,updateContent=None)
        field_result=Budget(self.test).getSubject(self.user0.sessionid,subjectId)
        verify_equal(field_expect=field_expect,field_result=field_result)

    def test_case2(self,subjectId):
        #正常更改科目,全部更改
        categoryId = self.Category[1]['id']
        updateContent={'subject':'更新科目名字','categoryId':categoryId,'code':'333','orderNum':9}
        result=Budget(self.test).updateSubject(self.user0.sessionid,subjectId,updateContent=updateContent)

        field_expect = {'name': '更新科目名字', 'categoryId': categoryId, 'code': '333', 'orderNum': 9}
        field_result=Budget(self.test).getSubject(self.user0.sessionid,subjectId)

        verify_equal(field_expect=field_expect,field_result=field_result)
    def test_case_exp1(self,subjectId):
        #异常更改科目,-29638: 科目分类不存在
        categoryId = 666
        updateContent={'categoryId':categoryId}

        error=Budget(self.test).updateSubject(self.user0.sessionid,subjectId,updateContent=updateContent,is_result=False)
        print('#异常更改科目,-29638: 科目分类不存在\n',error)

    def test_case_exp2(self,subjectId):
        #异常更改科目,-29639:科目名称已存在

        updateContent = {'subject': '更新科目名字'}

        error=Budget(self.test).updateSubject(self.user0.sessionid,subjectId,updateContent=updateContent,is_result=False)
        print('#异常更改科目,-29639:科目名称已存在\n',error)

    def test_case_exp3(self):
        #异常更改科目,-29637: 科目不存在
        subjectId=1100
        updateContent = None

        error=Budget(self.test).updateSubject(self.user0.sessionid,subjectId,updateContent=updateContent,is_result=False)
        print('#异常更改科目,-29637: 科目不存在\n',error)

class Test_deleteSubject (Base_test):

    @property
    def Category(self):
        result=Budget(self.test).listCategory(self.user0.sessionid)
        return result['objects']

    @pytest.fixture()
    def subjectId(self):
        categoryId=self.Category[0]['id']
        result = Budget(self.test).addSubject(self.user0.sessionid,categoryId,subject='科目1',code='233')
        return result

    def test_case1(self,subjectId):
        #正常删除科目
        result=Budget(self.test).deleteSubject(self.user0.sessionid,subjectId)
        field_expect={'status':2}
        field_result=Budget(self.test).getSubject(self.user0.sessionid,subjectId)
        verify_equal(field_expect=field_expect,field_result=field_result)

    def test_case_exp1(self):
        #异常删除科目,科目不存在时
        subjectId=555
        error = Budget(self.test).deleteSubject(self.user0.sessionid, subjectId,is_result=False)
        print('-29637: 科目不存在:\n',error)


class Test_recoverSubject(Base_test):

    @property
    def Category(self):
        result=Budget(self.test).listCategory(self.user0.sessionid)
        return result['objects']

    @pytest.fixture(scope='class')
    def subjectId(self):
        categoryId=self.Category[0]['id']
        result = Budget(self.test).addSubject(self.user0.sessionid,categoryId,subject='科目1',code='233')
        return result

    def test_case1(self,subjectId):
        #正常恢复科目
        Budget(self.test).deleteSubject(self.user0.sessionid, subjectId)

        result=Budget(self.test).recoverSubject(self.user0.sessionid,subjectId)

        field_expect = {'status': 0}
        field_result = Budget(self.test).getSubject(self.user0.sessionid, subjectId)
        verify_equal(field_expect=field_expect, field_result=field_result)

    def test_case_exp1(self,subjectId):
        #异常恢复科目，科目状态不正确时

        error=Budget(self.test).recoverSubject(self.user0.sessionid,subjectId,is_result=False)
        print('-29635: 科目状态不正确:\n',error)

    def test_case_exp2(self):
        #异常恢复科目,科目不存在时
        subjectId=555
        error = Budget(self.test).recoverSubject(self.user0.sessionid, subjectId,is_result=False)
        print('-29637: 科目不存在:\n',error)


