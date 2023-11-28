#!/usr/bin/env python3
# coding = utf8
"""
@ Author : ZeroSeeker
@ e-mail : zeroseeker@foxmail.com
@ GitHub : https://github.com/ZeroSeeker
@ Gitee : https://gitee.com/ZeroSeeker
"""
from lazysdk import lazyrequests
from lazysdk import lazyfile
import hashlib
import urllib3
import random
import envx
import json
import time
default_salt_file_name = 'salt.env'


def make_salt(
        salt_file_name: str = default_salt_file_name,
        salt_length: int = 30,
        overwrite: bool = False
):
    """
    生成盐
    :param salt_file_name: 生成的文件名
    :param salt_length: 生成盐的长度
    :param overwrite: 是否覆盖
    """
    random_ak = ''.join(random.sample('abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789', salt_length))
    salt_file_content = f'salt={random_ak}'
    if envx.read(salt_file_name) and not overwrite:
        return {
            'code': 1,
            'msg': '文件已存在'
        }
    else:
        print(envx.basic(salt_file_name)['env_path'])
        lazyfile.save(
            file_name=salt_file_name.split('.')[0],
            content=salt_file_content,
            postfix=salt_file_name.split('.')[1],
            path=envx.basic(salt_file_name)['env_path'],
            overwrite=overwrite
        )
        return {
            'code': 0,
            'msg': 'ok',
            'salt_str': random_ak,
            'salt_dir': envx.basic(salt_file_name)['file_dir'],
            'salt_file_name': salt_file_name,
            'salt_length': salt_length
        }


def make_sk(
        ak: str,
        salt_str: str = None,
        salt_file_name: str = default_salt_file_name,
):
    """
    输入 ak 生成 sk
    :param ak: 明码
    :param salt_str: 加密盐字符串（优先使用）
    :param salt_file_name: 加密盐文件名，内容格式为：salt=XXXX，默认为：salt.env
    return: sk 生成的密码
    """
    if salt_str:
        pass
    else:
        salt_str = envx.read(salt_file_name)['salt']
    local_content = 'ak=%s;salt=%s' % (ak, salt_str)
    d5 = hashlib.sha256()
    d5.update(local_content.encode(encoding='UTF-8'))  # update添加时会进行计算
    return d5.hexdigest()


def make_signer(
        ak: str,
        sk: str,
        data: dict
):
    """
    生成签名
    :param ak: 身份识别码
    :param sk: 身份密码
    :param data:
        ts: 必填，时间戳,使用int(time.time())方法生成
        method: 必填，请求方法：GET/POST
        url: 必填，请求的url，例如 https://...
        query: 必填，请求要发送的数据，为json格式
    如果data数据中包含sk、sign，在签名时会自动剔除

    正确签名返回：{'code': 0, 'msg': 'success', 'data': '签名内容'}
    """
    data['ak'] = ak
    data_keys = list(data.keys())
    if 'ts' not in data_keys:
        return {'code': 1, 'msg': 'ts required', 'data': ''}
    if 'method' not in data_keys:
        return {'code': 1, 'msg': 'method required', 'data': ''}
    if 'url' not in data_keys:
        return {'code': 1, 'msg': 'url required', 'data': ''}
    if 'query' not in data_keys:
        return {'code': 1, 'msg': 'query required', 'data': ''}
    data_keys.sort()  # 升序
    data_str = ''
    for each_key in data_keys:
        if each_key == 'query' and type(each_key) == 'dict':
            temp_str = '%s=%s;' % (each_key, json.dumps(data[each_key]))
        else:
            if each_key == 'sk':
                continue
            elif each_key == 'sign':
                continue
            else:
                temp_str = '%s=%s;' % (each_key, data[each_key])
        data_str += temp_str
    data_str += 'sk=%s;' % sk
    d5 = hashlib.sha256()
    d5.update(data_str.encode(encoding='UTF-8'))  # update添加时会进行计算
    return {'code': 0, 'msg': 'success', 'data': d5.hexdigest()}


def make_sign_request(
        ak: str,
        sk: str,
        data: dict,
        verify: bool = True
):
    """
    自动签名并发起请求
    :param ak: 身份识别码
    :param sk: 身份密码
    :param data:
        ts: 必填，时间戳,使用int(time.time())方法生成
        method: 必填，请求方法：GET/POST
        url: 必填，请求的url，例如 https://...
        query: 必填，请求要发送的数据，为json格式
        如果data数据中包含sk、sign，在签名时会自动剔除
    :param verify: 是否验证ssl证书

    正确返回：{'code': 0, 'msg': 'success', 'data': '...'}
    """
    data['ts'] = int(time.time())
    sign_res = make_signer(
        ak=ak,
        sk=sk,
        data=data
    )
    if sign_res['code'] == 0:
        data['sign'] = sign_res['data']
        if verify is False:
            urllib3.disable_warnings()
            return lazyrequests.lazy_requests(
                method=data['method'],
                url=data['url'],
                json=data,
                verify=False,
                return_json=True
            )
        else:
            return lazyrequests.lazy_requests(
                method=data['method'],
                url=data['url'],
                json=data,
                return_json=True
            )
    else:
        return sign_res
