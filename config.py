
import os

from dotenv import load_dotenv

base_dir = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(base_dir, '.env'))

_DEF_VAL = {
    'LOCAL_DB': 'sqlite:///' + os.path.join(base_dir, 'data', 'gtfs.db'),
    'LOG_DIR': os.path.join(base_dir, 'logs'),
    "GTFS_DIR": os.path.join(base_dir, 'data', 'gtfs'),
}


class Config(object):
    DEFAULTS = _DEF_VAL

    DEBUG = os.environ.get('DEBUG', True)

    LOG_TO_STDOUT = os.environ.get('LOG_TO_STDOUT') is not None

    LOG_DIR = os.environ.get('LOG_DIR', _DEF_VAL['LOG_DIR'])
    GTFS_DIR = os.environ.get('GTFS_DIR', _DEF_VAL['GTFS_DIR'])

    DB_URI = os.environ.get('DB_URI', _DEF_VAL['LOCAL_DB'])
