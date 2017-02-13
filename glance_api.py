from glanceclient import Client
import logger

LOG = logger.get_logger("glanceclient")

glance = None

def init_glance_client(endpoint, token, version='1'):
    global glance
    try:
        glance = Client(version, endpoint=endpoint, token=token)
        LOG.info("glanceclient init succeed.")
    except Exception as e:
        LOG.error("glanceclient init failed.%s" % e)
        return

def get_image_list(name_prefix='', to_dict=True):
    try:
        images = glance.images.list() 
        LOG.info("Obtain the image list succeed.")
    except Exception as e:
        LOG.error("Obtain the image list failed.%s" % e)
    image_list = [i for i in images]

    if name_prefix:
        image_list = [i for i in image_list if i.name.startswith(name_prefix)]
        
    if to_dict:
        image_list = [i.to_dict() for i in image_list] 

    return image_list

if __name__ == "__main__":
    import keystone_api
    keystone_api.login('192.168.3.33', 'admin', 'admin', 'admin')
    print keystone_api.FirstUser, '\n' 

    image_endpoint = keystone_api.url_for('image')
    init_glance_client(image_endpoint, keystone_api.FirstUser['firstuser'].token.id)
    image_list = get_image_list()
    for image in image_list:
        print image, '\n'

