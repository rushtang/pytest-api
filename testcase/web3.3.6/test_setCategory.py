import pytest,sys

sys.path.append(r'C:\Users\Administrator\PycharmProjects\pytest_demo')

from baselib.data import Base_test
from apilib.base import User
from apilib.other import Budget




class Test_setCategory(Base_test):

    @property
    def user0(self):
        return User(self.test,num=0)

    @pytest.fixture()
    def user1(self):
        return User(self.test,num=1)


    def test_case1(self,user1):
        print(self.user0.sessionid)

        print(user1.sessionid)
        # Budget(self.test).setCategory(self.user0.sessionid,name='默认名字')





