#!/usr/bin/env python
# coding=utf-8

from keystoneclient.v2_0 import client as keystone_client
from keystoneclient import exceptions as keystone_exceptions
from keystoneclient.v2_0 import tokens

import logger
LOG = logger.get_logger('keystoneclient')

FirstUser = {}

def login(ip, username, password, tenant_name):
    url = 'http://%s:5000/v2.0' % ip 
    auth = KeystoneBackend()
    Flag, User = auth.authenticate(username=username, password=password, tenant_name=tenant_name, auth_url=url)
    #if Flag == u'Invalid':
    #    return Flag, u'连接失败', u"用户名或密码错误.\n\n请重新登录."
    #if Flag == u'Exception':
    #    return Flag, u'连接失败', u"认证错误.\n\n请尝试重新登录."
    #elif Flag == u'IPError':
    #    return Flag, u'连接失败', u"网络错误.\n\n请检查你的网络设置."
    #elif Flag == u'Success': 
    #    FirstUser['firstuser'] = User
    #    FirstUser['serverip'] = ip

    #    return Flag, u'成功!', u'成功登录.'
    if Flag == u'Success':
        FirstUser['firstuser'] = User
        FirstUser['serverip'] = ip

    return Flag

class KeystoneBackend(object):
    def __init__(self):
        pass
    
    def authenticate(self, username=None, password=None,
                     tenant_name=None, auth_url=None, otp=None):
        try:
            ksclient = keystone_client.Client(username=username,
                                            password=password,
                                            tenant_name=None,
                                            auth_url=auth_url,
                                            insecure=False,
                                            timeout=8)
            LOG.info('ksclient init succeed.') 
        except (keystone_exceptions.Unauthorized,
                keystone_exceptions.Forbidden,
                keystone_exceptions.NotFound) as exc:
            LOG.error("ksclient init failed,username or passwd is error.")
            return u'Invalid', None
        except (keystone_exceptions.ClientException,
                keystone_exceptions.AuthorizationFailure) as exc:
            LOG.error("ksclient init failed,connect to the server failed.")
            return u'IPError', None
        except Exception as e:
            LOG.error("ksclient init failed,other error.%s" % e)
            return u'Exception', None

        try:
            tenants = ksclient.tenants.list()
            LOG.info("Obtail the tenant succeed.")
        except:
            LOG.error("Obtail the tenant failed.")
            return u'Exception', None

        while tenants:
            tenant = tenants.pop()
            if tenant.name != tenant_name:
                continue
            try:
                token = ksclient.tokens.authenticate(username=username,
                                                    password=password,
                                                    tenant_id=tenant.id)
                LOG.info("Obtail the token succeed.")
                break
            except Exception as e:
                LOG.error("Obtail the token failed.%s" % e)
                return u'Exception', None

        User = create_user(ksclient, token)
        return u'Success' ,User

def create_user(ksclient, token):
    return User(ksclient=ksclient, token=token)

class User(object):
    def __init__(self, ksclient=None, token=None):
        self.ksclient = ksclient
        self.token = token

def url_for(service_type, endpoint_type=None):
    if endpoint_type is None:
        endpoint_type = 'publicURL'

    fallback_endpoint_type = None

    catalog = FirstUser['firstuser'].token.serviceCatalog
    service = get_service_from_catalog(catalog, service_type)
    if service:
        url = get_url_for_service(service,
                                  'regionone',
                                  endpoint_type)
        if not url and fallback_endpoint_type:
            url = get_url_for_service(service,
                                      'regionone',
                                      fallback_endpoint_type)
        if url:
            server = FirstUser['serverip']
            a = url[:4]
            b = str('//%s' % server)
            c = url.split(':')[2]
            d = [a, b, c]
            m = ':'.join(d)
            return m

def get_service_from_catalog(catalog, service_type):
    if catalog:
        for service in catalog:
            if service['type'] == service_type:
                return service
    return None

def get_url_for_service(service, region, endpoint_type):
    identity_version = get_version_from_service(service)
    for endpoint in service['endpoints']:
        if service['type'] == 'identity' or region == endpoint['region'].lower():
            try:
                if identity_version < 3:
                    return endpoint[endpoint_type]
                else:
                    interface = \
                        ENDPOINT_TYPE_TO_INTERFACE.get(endpoint_type, '')
                    if endpoint['interface'] == interface:
                        return endpoint['url']
            except (IndexError, KeyError):
                return None
    return None

def get_version_from_service(service):
    if service:
        endpoint = service['endpoints'][0]
        if 'interface' in endpoint:
            return 3
        else:
            return 2.0
    return 2.0

ENDPOINT_TYPE_TO_INTERFACE = {
    'publicURL': 'public',
    'internalURL': 'internal',
    'adminURL': 'admin',
}


if __name__ == '__main__':
    username = 'www'
    passwd = 'www111'
    tenant_name = 'w1'
    url = '192.168.3.33'
    ret = login(url, username, passwd, tenant_name)
    print 'ReLogin Status:  %s' % ret
