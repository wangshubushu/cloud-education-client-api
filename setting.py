import os
import sys

if sys.platform.lower().startswith('linux'):
    log_top_path = '/root/log'
else:
    log_top_path = os.environ['HOMEPATH']

LOG_DEFAULT_FILE = os.path.join(log_top_path, 'education_cloud_api.log')
