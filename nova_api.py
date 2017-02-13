#!/usr/bin/env python
# coding=utf-8

from novaclient.v1_1 import client as nova_client
import keystone_api
import logger
from keystone_api import FirstUser, url_for

LOG = logger.get_logger('novaclient')

class APIResourceWrapper(object):
    _attrs = []
 
    def __init__(self, apiresource):
        self._apiresource = apiresource
 
    def __getattr__(self, attr):
        if attr in self._attrs:
            return self._apiresource.__getattribute__(attr)
        else:
            msg = ('Attempted to access unknown attribute "%s" on '
                   'APIResource object of type "%s" wrapping resource of '
                   'type "%s".') % (attr, self.__class__,
                                    self._apiresource.__class__)
            raise AttributeError(attr)
 
    def __repr__(self):
        return "<%s: %s>" % (self.__class__.__name__,
                             dict((attr, getattr(self, attr))
                                  for attr in self._attrs
                                  if hasattr(self, attr)))

class Server(APIResourceWrapper):
    _attrs = ['addresses', 'id', 'image', 'links', 'vcpus', 'rams',
             'metadata', 'name', 'private_ip', 'public_ip', 'status', 'uuid',
             'image_name', 'VirtualInterfaces', 'flavor', 'key_name',
             'tenant_id', 'user_id', 'OS-EXT-STS:power_state',
             'OS-EXT-STS:task_state', 'OS-EXT-SRV-ATTR:instance_name',
             'OS-EXT-SRV-ATTR:host', 'created']

    def __init__(self, apiresource, request):
        super(Server, self).__init__(apiresource)
        self.request = request

    @property
    def internal_name(self):
        return getattr(self, 'OS-EXT-SRV-ATTR:instance_name', "")

    def to_dict(self):
        server_attr_dict = {}
        for attr in self._attrs:
            try:
                server_attr_dict[attr] = getattr(self, attr)
            except Exception as e:
                pass

        return server_attr_dict

def novaclient():
    try:
        c = nova_client.Client(FirstUser['firstuser'].token.user['name'],
                               FirstUser['firstuser'].token.id,
                               project_id=FirstUser['firstuser'].ksclient.tenant_id,
                               auth_url=url_for('compute'),
                               insecure=False)
        LOG.info("novaclient init susseed.")
    except Exception as e:
        LOG.error("novaclient init failed.%s" % e)
        return
    c.client.auth_token = FirstUser['firstuser'].token.id
    c.client.management_url = url_for('compute')

    return c

def list_vms(to_dict=True):
    c = novaclient()

    search_opts = {}
    all_tenants = False
    if all_tenants:
        search_opts['all_tenants'] = True
    else:
        search_opts['project_id'] = FirstUser['firstuser'].ksclient.tenant_id

    try:
        if to_dict:
            servers = [Server(s, FirstUser['firstuser']).to_dict()
                        for s in c.servers.list(True, search_opts)]
        else:
            servers = [Server(s, FirstUser['firstuser'])
                        for s in c.servers.list(True, search_opts)]
        LOG.info("Obtain all of the server succeed.")
    except Exception as e:
        LOG.error("Obtain all of the server failed.%s" % e)
        return

    return servers

def shutdown_vms(vms):
    try:
        for vm in vms:
            novaclient().servers.stop(vm["id"])
        LOG.info("Shutdown all of the server succeed.")
    except Exception as e:
        LOG.error("Shutdown all of the server failed.%s" % e)
        return

def start_vms(vms):
    try:
        for vm in vms:
            novaclient().servers.start(vm["id"])
        LOG.info("Start all of the server succeed.")
    except Exception as e:
        LOG.error("Start all of the server failed.%s" % e)
        return

def restart_vms(vms):
    try:
        for vm in vms:
            novaclient().servers.reboot(vm["id"])
        LOG.info("Restart all of the server succeed.")
    except Exception as e:
        LOG.error("Restart all of the server failed.%s" % e)
        return

def image_rebuild(vm, image_id):
    try:
        novaclient().servers.rebuild(vm["id"], image_id)
        LOG.info("Rebuild the server succeed.")
    except Exception as e:
        LOG.error("Rebuild the server failed.%s" % e)
        return

def image_commit(vm):
    try:
        novaclient().servers.commit(vm.id)
        LOG.info("Commit the server succeed.")
    except Exception as e:
        LOG.erro("Commit the server failed.%s" % e)
        return

if __name__ == '__main__':
    username = 'admin'
    password = 'admin'
    tenant = 'admin'
    ip = '192.168.3.33'
    keystone_api.login(ip, username, password, tenant)
    servers = list_vms()
    #shutdown_vms(servers)
    start_vms(servers)
    #restart_vms(servers)
