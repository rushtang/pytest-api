import pymysql
from datetime import datetime,timedelta
from faker import Factory
from baselib.utils import delete_exec
from baselib.http import Jsonrpc
from apilib.base import User
import random,pytest
from functools import wraps


class Singleton(object):
    #单例类
    _instance = None
    def __new__(cls, *args, **kw):
        if not cls._instance:
            cls._instance = super(Singleton, cls).__new__(cls, *args, **kw)
        return cls._instance


class Jsonrpc_Singleton(Jsonrpc,Singleton):
    pass


def singleton(cls):
    #单例装饰器
    instances = {}
    @wraps(cls)
    def getinstance(*args, **kw):
        if cls not in instances:
            instances[cls] = cls(*args, **kw)
        return instances[cls]
    return getinstance

@singleton
class User_singleton(User):
    pass


class Base_test():


    @pytest.fixture(scope='class',autouse=True)
    def clean_data(self):
        delete_exec(self.test)

    @pytest.fixture(scope='function')
    def clean_case(self):
        delete_exec(self.test)


    @property
    def test(self):
        return Jsonrpc_Singleton()

    @property
    def user0(self):
        return User_singleton(self.test, num=0)

    @property
    def user1(self):
        return User_singleton(self.test, num=1)




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