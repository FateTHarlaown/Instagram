# -*- coding: utf-8 -*-
from Intasgraph import app
from qiniu import Auth, put_data
import qiniu.config

access_key = app.config['QINIU_ACCESS_KEY']
secret_key = app.config['QINIU_SECRET_KEY']
q = Auth(access_key, secret_key)
bucketname = 'rabbithell'
domain = app.config['QINIU_DOMAIN']


def qiniu_upload_file(source, name):
    token = q.upload_token(bucketname, name)
    ret, info = put_data(token, name, source.stream)
    print type(info.status_code), ret
    if info.status_code == 200:
        return domain + name
    return None
