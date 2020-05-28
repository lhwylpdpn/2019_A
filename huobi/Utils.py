# -*- coding: utf-8 -*-
# @author  : Bin
# @time    : 2020/1/13 11:03

import base64
import hmac
import hashlib
import json
import time
import urllib
import datetime
import requests
from urllib import parse

TIMEOUT = 10


# 各种请求,获取数据方式
def http_get_request(url, params, add_to_headers=None):
    while 1:
        headers = {
            "Content-type": "application/x-www-form-urlencoded",
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:53.0) Gecko/20100101 Firefox/53.0'
        }
        if add_to_headers:
            headers.update(add_to_headers)
        post_data = urllib.parse.urlencode(params)
        try:
            response = requests.get(url, post_data, headers=headers, timeout=TIMEOUT)
            if response.status_code == 200:
                return response.json()
            else:
                return {"status": "fail"}
        except Exception as e:
            time.sleep(5)
            print("httpGet failed, detail is:%s" % e)
            #return {"status": "fail", "msg": "%s" % e}


def http_post_request(url, params, add_to_headers=None):
    headers = {
        "Accept": "application/json",
        'Content-Type': 'application/json',
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:53.0) Gecko/20100101 Firefox/53.0'
    }
        
    if add_to_headers:
        headers.update(add_to_headers)
    post_data = json.dumps(params)
    while 1:

        try:
            response = requests.post(url, post_data, headers=headers, timeout=TIMEOUT)
            if response.status_code == 200:
                return response.json()
            else:
                return response.json()
        except Exception as e:
            time.sleep(5)
            print("httpPost failed, detail is:%s" % e)
           # return {"status": "fail", "msg": "%s" % e}


def api_key_get(url, request_path, params, ACCESS_KEY, SECRET_KEY):
    method = 'GET'
    timestamp = datetime.datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%S')
    #print('timestamp',timestamp)
    params.update({'AccessKeyId': ACCESS_KEY,
                   'SignatureMethod': 'HmacSHA256',
                   'SignatureVersion': '2',
                   'Timestamp': timestamp})

    host_url = url
    # host_name = urlparse.urlparse(host_url).hostname
    host_name = urllib.parse.urlparse(host_url).hostname
    host_name = host_name.lower()

    params['Signature'] = create_sign(params, method, host_name, request_path, SECRET_KEY)
    url = host_url + request_path
    return http_get_request(url, params)


def api_key_post(url, request_path, params, ACCESS_KEY, SECRET_KEY):
    method = 'POST'
    timestamp = datetime.datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%S')
    #print('timestamp',timestamp)
    params_to_sign = {'AccessKeyId': ACCESS_KEY,
                      'SignatureMethod': 'HmacSHA256',
                      'SignatureVersion': '2',
                      'Timestamp': timestamp}

    host_url = url
    # host_name = urlparse.urlparse(host_url).hostname
    host_name = urllib.parse.urlparse(host_url).hostname
    host_name = host_name.lower()
    params_to_sign['Signature'] = create_sign(params_to_sign, method, host_name, request_path, SECRET_KEY)
    #print(params_to_sign['Signature'])
    url = host_url + request_path + '?' + urllib.parse.urlencode(params_to_sign)
    #print(url)
    return http_post_request(url, params)


def create_sign(params, method, host_url, request_path, secret_key):
    sorted_params = sorted(params.items(), key=lambda d: d[0], reverse=False)
    encode_params = urllib.parse.urlencode(sorted_params)
    payload = [method, host_url, request_path, encode_params]
    payload = '\n'.join(payload)
    payload = payload.encode(encoding='UTF8')
    #print('payload',payload)
    secret_key = secret_key.encode(encoding='UTF8')
    #print('secret_key',secret_key)
    digest = hmac.new(secret_key, payload, digestmod=hashlib.sha256).digest()
    #print('digest',digest)

    signature = base64.b64encode(digest)
    signature = signature.decode()
    #print('signature',signature)
    return signature
