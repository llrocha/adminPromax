import os
import re
import sh
import subprocess


class BaseControls():
    def __init__(self, geo):
        self.geo = geo


class ApacheControls(BaseControls):
    def __init__(self, geo):
        super(self.__class__, self).__init__(geo)

    def status(self):
        return str(sh.grep(sh.ps('-ef'), 'httpd'))

    def start(self):
        return subprocess.check_output(['/amb/boot/S80_httpd_promax_h1'])

    def stop(self):
        return subprocess.check_output(['/amb/boot/K80_httpd_promax_h1'])

    def config_files(self):
        mask = '.*\.conf'
        files = ''
        try:
            dir = '/{0}/etc/apache/promax/'.format(self.geo)
            for config_file in os.listdir(dir):
                if(re.match(mask, config_file)):
                    if(files):
                        files = files + ';' + config_file
                    else:
                        files = config_file
        except FileNotFoundError as e:
            files = "File Not Found Error ({0}): {1}".format(e.errno, e.strerror)

        return files

    def configfile_content(self, file):
        config_file = '/{0}/etc/apache/promax/{1}'.format(self.geo, file.replace('_', '.'))
        if(os.path.isfile(config_file)):
            return subprocess.check_output(['cat', config_file])
        else:
            return 'This file does not exists! [{0}]'.format(config_file)

    def instances(self):
        geo = None

        for dir in os.listdir('/'):
            if(re.match('^[a-z][a-z0-9]$', dir)):
                if(geo):
                    geo = geo + ';' + dir
                else:
                    geo = dir

        return geo


class DataBaseControls(BaseControls):
    def __init__(self, geo):
        super(self.__class__, self).__init__(geo)
    

class BuildBotControls(BaseControls):
    def __init__(self, geo):
        super(self.__class__, self).__init__(geo)


class EnvironControls(BaseControls):
    def __init__(self, geo):
        super(self.__class__, self).__init__(geo)

    def environ():
        return subprocess.check_output(['set'])

    def diskusage():
        return subprocess.check_output(['df', '-h'])

    def memory():
        return subprocess.check_output(['egrep', '"Mem|Cache|Swap"', '/proc/meminfo'])


class JobsControls(BaseControls):
    def __init__(self, geo):
        super(self.__class__, self).__init__(geo)

    def startjob(job):
        pass

    def stopjob(job):
        pass

    def jobs(job):
        pass


class ServerControls():
    """
    """

    def __init__(self, geo):
        super(self.__class__, self).__init__(geo)
        self.modules = []

    def register_class(cls):
        self.modules.append(cls)

    def unregister_class(cls):
        self.modules.remove(cls)

