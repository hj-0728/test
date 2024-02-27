import requests


def get_access_token():
    """
    测试获取access_token
    """
    url = "https://oapi.dingtalk.com/gettoken?appkey=dingvhjoxjuky063hfrz&appsecret=VBcbx9OJOkxmrKr6nKt05_YBJYVrT2z7Bja4tMrysu-LasyHEp0ffu9S7msEEP5v"
    resp = requests.get(url=url)
    json_data = resp.json()
    return json_data['access_token']


def test_get_k12_dept_list():
    """
    获取家校通讯录部门
    """
    access_token = get_access_token()
    data = {
        # 'dept_id': 1,
        'super_id': 414759300,
        'page_no': 1,
        'page_size': 30
    }
    url = 'https://oapi.dingtalk.com/topapi/edu/dept/list?access_token=' + access_token
    resp = requests.post(url, json=data)
    json_data = resp.json()
    print(json_data)


def test_get_k12_user_list():
    """
    获取家校通讯录部门
    """
    access_token = get_access_token()
    data = {
        # 'dept_id': 414571429,
        'dept_id': 414393570,
        # 'dept_id': 1,
        'role': 'student',
        'page_no': 1,
        'page_size': 30
    }
    url = 'https://oapi.dingtalk.com/topapi/edu/user/list?access_token=' + access_token
    resp = requests.post(url, json=data)
    json_data = resp.json()
    print(json_data)


def test_get_dept_list():
    """
    获取通讯录部门
    """
    access_token = get_access_token()
    data = {
        # 'dept_id': 1,
        # 'super_id': 414759300,
        # 'page_no': 1,
        # 'page_size': 30
    }
    url = 'https://oapi.dingtalk.com/topapi/v2/department/listsub?access_token=' + access_token
    resp = requests.post(url, json=data)
    json_data = resp.json()
    print(json_data)


def test_get_user_list():
    """
    获取通讯录用户
    """
    access_token = get_access_token()
    data = {
        # 'dept_id': 414571429,
        'dept_id': 415683209,
        # 'dept_id': 1,
        'cursor': 0,
        # 'page_no': 1,
        'size': 30
    }
    url = 'https://oapi.dingtalk.com/topapi/v2/user/list?access_token=' + access_token
    resp = requests.post(url, json=data)
    json_data = resp.json()
    print(json_data)


def test_get_user_info():
    access_token = get_access_token()
    data = {
        'userid': 1805260804734828,
    }
    url = 'https://oapi.dingtalk.com/topapi/v2/edu/user/get?access_token=' + access_token
    resp = requests.post(url, json=data)
    json_data = resp.json()
    print(json_data)