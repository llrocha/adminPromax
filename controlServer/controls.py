import os
import re
import subprocess


class BaseControls():
    def __init__(self, geo):
        self.geo = geo


class ApacheControls(BaseControls):
    def __init__(self, geo):
        super(self.__class__, self).__init__(geo)

    def status(self):
        return subprocess.check_output(['ps', '-ef'])

    def start(self):
        return subprocess.check_output(['/amb/boot/S80_httpd_promax_h1'])

    def stop(self):
        return subprocess.check_output(['/amb/boot/K80_httpd_promax_h1'])

    def config_files(self):
        mask = '.*\.conf'
        r = []
        try:
            for f in os.listdir('/{0}/etc/apache/promax/'.format(self.geo)):
                if(re.match(mask, f)):
                    r.append(f)
        except FileNotFoundError as e:
            r.append("File Not Found Error ({0}): {1}".format(e.errno, e.strerror))
        return r.join(';')

    def configfile_content(self, file):
        f = '/{0}/etc/apache/promax/{1}'.format(self.geo, file)
        if(os.path.isfile(f)):
            return subprocess.check_output(['cat', f])
        else:
            return 'This file does not exists! [{0}]'.format(f)


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

