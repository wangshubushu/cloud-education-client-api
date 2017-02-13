import os
import sys

import polltaskclient as polltask_client
import keystone_api
import logger
from keystone_api import *

LOG = logger.get_logger("polltask")

def polltaskclient(version='1'):
    token= FirstUser['firstuser'].token.id
    url = u'http://%s:10002' % FirstUser['serverip']
    ip_address=FirstUser['serverip']
    LOG.info("Polltaskclient init.")
    return polltask_client.Client(version, url,
                               token=token,
                               ip_address=ip_address,
                               insecure=False,
                               cacert=None)

def list_device():
    """get all device list.
    """
    LOG.info("Get all device list.")
    return polltaskclient().device.list()

def poweroff_device(device):
    """Close the device needs to be passed to a ID.
    """
    LOG.info("Close the deivce.")
    return polltaskclient().device.poweroff_device(device)

def reboot_device(device):
    """Restart the device needs to be passed to a ID.
    """
    LOG.info("Restart the device.")
    return polltaskclient().device.reboot_device(device)

def reboot_host(host=None):
    """Restart the server needs to be passed
        to the host name or IP address.
    """
    LOG.info("Restart the server.")
    return polltaskclient().device.reboot_host(host=host)

def poweroff_host(host=None):
    """Close the server needs to be passed
       to a host name or IP address.
    """
    LOG.info("Power off the server.")
    return polltaskclient().device.poweroff_host(host=host)


if __name__=="__main__":
    username = 'admin'
    password = 'admin'
    tenant = 'admin'
    ip = '192.168.3.150'
    k = keystone_api.login(ip, username, password, tenant)
    print list_device() 
