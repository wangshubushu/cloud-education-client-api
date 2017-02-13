import keystone_api
import nova_api
import glance_api
import polltask_api

HOST = ''
CLASSROOM = ''
USERNAME = ''
PASSWORD = ''
STU_IMAGE_PREFIX = 'stu'

def init_handle(host, classroom, username, password):
    global HOST, CLASSROOM, USERNAME, PASSWORD
    HOST = host
    CLASSROOM = classroom
    USERNAME = username
    PASSWORD = password
    keystone_api.login(host, username, password, classroom) 
    glance_api.init_glance_client(keystone_api.url_for('image'), 
                        keystone_api.FirstUser['firstuser'].token.id)

def list_student_vms():
    return nova_api.list_vms()

def shutdown_student_compute():
    """It will shutdown the student vm and the device which 
       the vm has been loaded in.
    """
    vms = nova_api.list_vms()
    nova_api.shutdown_vms(vms)
    devices = polltask_api.list_device()
    if len(devices) == 0:
        return
    device_ids = [d.id for d in devices if d.id]
    polltask_api.poweroff_device(device_ids)

def reboot_student_vms():
    vms = nova_api.list_vms()
    nova_api.restart_vms(vms)

def shutdown_student_compute_and_cloud_host():
    global HOST
    shutdown_student_compute()
    polltask_api.poweroff_host(HOST)

def reboot_cloud_host():
    global HOST
    polltask_api.reboot_host(HOST)

def list_images(to_dict=True):
    return glance_api.get_image_list(name_prefix=STU_IMAGE_PREFIX, 
                                        to_dict=to_dict)

def reboot_vm_with_image(image_id, vm=None):
    if vm is None:
        vms = nova_api.list_vms()
        for vm in vms:
            nova_api.image_rebuild(vm, image_id)
    else:
        nova_api.image_rebuild(vm, image_id)

def set_student_image(image_id=None):
    pass

if __name__ == "__main__":
    init_handle('192.168.20.100', 'class', 'teacher', 'www111') 
    #vms = list_student_vms()
    #print "vms: ", vms
    #shutdown_student_compute()
    #reboot_student_vms()
    #shutdown_student_compute_and_cloud_host()
    #reboot_cloud_host()
    images = list_images()
    print "images: ", images
    if images:
        reboot_vm_with_image(images[0]['id'])
