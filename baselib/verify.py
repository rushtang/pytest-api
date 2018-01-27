




def verify_equal(test,field_expect,field_result):
    #field_expect,field_result都为键值对
    print('verify_equal: \n'+str(field_expect))
    if len(field_expect)==0:
        test.assert_equals(field_expect,field_result,msg=field_expect)
    for key, value in field_expect.items():
        test.assert_equals(value, field_result[key], msg=key+' expect: '+str(value)+'----result: '+str(field_result[key])
                           +'\n field_expect: \n {} \n field_result: \n {}'.format(field_expect,field_result)
                           )



def verify_similar(test,field_expect,field_result):
    # field_expect,field_result都为键值对
    print('verify_similar: \n' + str(field_expect))
    if len(field_expect) == 0:
        test.assert_equals(field_expect, field_result, msg=field_expect)
    for key, value in field_expect.items():
        test.assert_equals(type(value), type(field_result[key]), msg=key + ':' + str(value))



def verify_Pagination(test,totalCount,expect_objects,result):
    #totalCount为int，objects为list，元素为dict
    # 默认objects内的元素是为有序的
    test.assert_equals(totalCount, result['totalCount'], msg=result)
    if len(expect_objects)!=0:
        for index,expect_object in enumerate(expect_objects):
            verify_equal(test,expect_object,result['objects'][index])


def verfiy_empty(test,field_result,is_empty=False):
    print(field_result)
    if field_result is None:
        assert is_empty==True
    else:
        L=len(field_result)
        if is_empty==False:
            test.assert_not_equals(L,0,msg='field_result is empty')
        else:
            test.assert_equals(L,0,msg='field_result not is empty')