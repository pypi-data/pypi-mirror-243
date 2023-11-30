import os
import sys
import time

log_r=os.path.abspath(os.path.dirname(__file__))
rootpath=os.path.split(log_r)[0]
sys.path.append(os.path.split(log_r)[0])
import logging
from logging import handlers


def _handle_log(log_path,log_name="KYAT"):
    '''

    :param log_path:
    :return:
    '''
    log_file_name = time.strftime("%Y%m%d", time.localtime())
    log_dir = os.path.join(log_path, '{}_ky{}.log'.format(log_file_name, log_name))
    kyAAT = logging.getLogger(name=log_name)

    if not kyAAT.handlers:
        pycharm = logging.StreamHandler()

        file = handlers.TimedRotatingFileHandler(filename=log_dir, when='D', encoding='utf-8', interval=1,
                                                 backupCount=10)

        fmt = '\033[35m' + '%(levelname)s   %(asctime)s %(name)s-%(filename)s-%(funcName)s-[line:%(lineno)d]：' + \
              '\033[0m\033[34m' + '%(message)s\033[0m'
        # filefmt = '%(asctime)s-%(name)s-%(levelname)s-%(filename)s-%(funcName)s-[line:%(lineno)d]：%(message)s'
        filefmt = '%(levelname)s    %(asctime)s-%(filename)s-%(funcName)s-[line:%(lineno)d]: %(message)s'

        kyAAT.setLevel(logging.DEBUG)
        log_fmt = logging.Formatter(fmt=fmt)
        log_fmt2 = logging.Formatter(fmt=filefmt)

        pycharm.setFormatter(fmt=log_fmt)
        file.setFormatter(fmt=log_fmt2)

        kyAAT.addHandler(pycharm)
        kyAAT.addHandler(file)
    return kyAAT


