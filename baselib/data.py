import pymysql
from datetime import datetime,timedelta
from faker import Factory
from baselib.utils import delete_exec
from baselib.http import Jsonrpc
from apilib.base import User
import random,pytest


@pytest.fixture()
def cleandata_suit():
    test=Jsonrpc()
    delete_exec(test)



class Base_test():


    @pytest.fixture(scope='function',autouse=True)
    def clean_case(self):
        delete_exec(self.test)

    @property
    def test(self):
        return Jsonrpc()

    @property
    def user0(self):
        return User(self.test, num=0)



def sql_exe(test,sql,db='xw'):
    print('exe SQL:'+sql)

    # host ='192.168.1.158'
    # port =20002
    # user ='test'
    # password ='69uqWcB0fKoS57RQjTCh'

    host = test.config.get("mysql.host")
    port = test.config.get("mysql.port")
    user = test.config.get("mysql.user")
    password = test.config.get("mysql.password")


    db = pymysql.connect(host=host,port=port,user=user,password=password,db=db,
                         cursorclass=pymysql.cursors.DictCursor,charset='utf8mb4'
                         )

    cursor = db.cursor()

    cursor.execute(sql)

    data = cursor.fetchall()

    db.commit()

    db.close()
    print('exe sql result:'+str(data))
    return data





fake = Factory.create()
from faker import Faker

fake = Faker("zh_CN")

def mobile_random():
    mobile=random.choice(['139','188','185','136','158','151','135'])+"".join(random.choice("0123456789") for i in range(8))
    return mobile