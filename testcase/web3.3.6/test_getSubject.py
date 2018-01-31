import pytest
import sys
sys.path.append(r'C:\Users\Administrator\PycharmProjects\pytest_demo')

from baselib.data import Base_test,fake
from apilib.base import User
from apilib.other import Budget
from baselib.verify import verify_equal
import random



class Test_getSubject(Base_test):

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
        #正常获取科目
        result=Budget(self.test).getSubject(self.user0.sessionid,subjectId)

        field_expect={'id':subjectId,'name':'科目1','code':'233','categoryId':self.Category[0]['id'],'orderNum':0,'status':0}
        print('返回项SubjectItem:\n',result)
        verify_equal(field_expect=field_expect,field_result=result)

    def test_case_exp1(self):
        #异常获取科目，-29637: 科目不存在
        subjectId=665
        error=Budget(self.test).getSubject(self.user0.sessionid,subjectId,is_result=False)
        print('-29637: 科目不存在:\n',error)



class Test_listSubject(Base_test):

    @property
    def Category(self):
        result=Budget(self.test).listCategory(self.user0.sessionid)
        return result['objects']
    @property
    def categoryId(self):
        return self.Category[0]['id']

    @property
    def categoryId2(self):
        return self.Category[1]['id']

    def code_rand(self):
        return random.randrange(100,999)

    @pytest.fixture(scope="class", params=['科目1','科目2','科目3'])
    def cre_subject(self,request):
        #其中科目3是被删除的科目且分类为categoryId2
        if request.param=='科目3':
            subjectId=Budget(self.test).addSubject(self.user0.sessionid, self.categoryId2, subject=request.param,code=self.code_rand())
            Budget(self.test).deleteSubject(self.user0.sessionid,subjectId)
        else:
            Budget(self.test).addSubject(self.user0.sessionid,self.categoryId,subject=request.param,code=self.code_rand())
        return request.param



    def test_data(self,cre_subject):

        print('生成测试数据:{}\n'.format(str(cre_subject)))


    def test_case1(self):
        #正常获取科目列表,查询状态为0 正常的
        query={'status':0}
        result=Budget(self.test).listSubject(self.user0.sessionid,query=query)
        print(result)

        verify_equal(field_expect={'totalCount':2},field_result=result)

    def test_case2(self):
        #正常获取科目列表,查询状态为1 删除的

        query = {'status': 2}
        result = Budget(self.test).listSubject(self.user0.sessionid, query=query)
        print(result)

        verify_equal(field_expect={'totalCount': 1}, field_result=result)

    def test_case3(self):
        #只查询categoryId时

        query = {'categoryId': self.categoryId}
        result = Budget(self.test).listSubject(self.user0.sessionid, query=query)
        print(result)

        verify_equal(field_expect={'totalCount': 2}, field_result=result)

    def test_case4(self):
        #只查询科目名称

        query = {'name': '科目3'}
        result = Budget(self.test).listSubject(self.user0.sessionid, query=query)
        print(result)

        verify_equal(field_expect={'totalCount': 1}, field_result=result)


class Test_setUserAuth(Base_test):

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
        #正常设置一个科目全部权限
        user1Id=self.user1.id
        limitUpper=10000
        codes=[{"code":1001,"limitUpper":limitUpper},{"code":1002,"limitUpper":limitUpper},{"code":1003,"limitUpper":limitUpper},
               {"code":1004,"limitUpper":limitUpper},{"code":1005,"limitUpper":limitUpper},
               {"code":1006,"limitUpper":limitUpper},{"code":1007,"limitUpper":limitUpper}]
        result=Budget(self.test).setUserAuth(self.user0.sessionid,user1Id,subjectId,codes)

class Test_listMySubject(Base_test):

    @property
    def Category(self):
        result=Budget(self.test).listCategory(self.user0.sessionid)
        return result['objects']

    @pytest.fixture()
    def subjectId(self):
        categoryId=self.Category[0]['id']
        result = Budget(self.test).addSubject(self.user0.sessionid,categoryId,subject='科目1',code='233')
        return result

    @pytest.fixture()
    def setUserAuth(self,subjectId):
        #给user1授权
        user1Id = self.user1.id
        limitUpper = 10000
        codes = [{"code": 1001, "limitUpper": limitUpper}, {"code": 1002, "limitUpper": limitUpper},
                 {"code": 1003, "limitUpper": limitUpper},
                 {"code": 1004, "limitUpper": limitUpper}, {"code": 1005, "limitUpper": limitUpper},
                 {"code": 1006, "limitUpper": limitUpper}, {"code": 1007, "limitUpper": limitUpper}]
        result = Budget(self.test).setUserAuth(self.user0.sessionid, user1Id, subjectId, codes)
        return user1Id
    def test_data(self,setUserAuth):

        print('生成测试数据: {}'.format(str(setUserAuth)))


    def test_case1(self):
        #正常获取科目限权表,userId传0时

        result=Budget(self.test).listMySubject(self.user1.sessionid,userId=0)
        print(result)



    def test_case2(self):
        #正常获取科目限权表,userId不为0时

        result=Budget(self.test).listMySubject(self.user0.sessionid,userId=self.user1.id)
        print(result)



