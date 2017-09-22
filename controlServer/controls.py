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
        config_file = '/{0}/etc/apache/promax/{1}'.format(self.geo, file.replace('%', '.'))
        if(os.path.isfile(config_file)):
            return subprocess.check_output(['cat', config_file])
        else:
            return 'This file does not exists! [{0}]'.format(config_file)

    def log_files(self):
        files = ''
        try:
            dir = '/{0}/promax/log/httpd/'.format(self.geo)
            for log_file in os.listdir(dir):
                if(files):
                    files = files + ';' + log_file
                else:
                    files = log_file
        except FileNotFoundError as e:
            files = "File Not Found Error ({0}): {1}".format(e.errno, e.strerror)

        return files

    def logfile_content(self, file):
        log_file = '/{0}/promax/log/httpd/{1}'.format(self.geo, file.replace('%', '.'))
        if(os.path.isfile(log_file)):
            return subprocess.check_output(['cat', log_file])
        else:
            return 'This file does not exists! [{0}]'.format(log_file)

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

    def status(self):
        return str(sh.grep(sh.ps('-ef'), 'buildbot'))

    def startmaster(self):
        return subprocess.check_output(['/buildbot/buildbot/buildbot.promax.master.sh', '-s'])

    def startworker(self):
        return subprocess.check_output(['/buildbot/buildbot/buildbot.promax.worker.sh', '-s'])        

    def stopmaster(self):
        return subprocess.check_output(['/buildbot/buildbot/buildbot.promax.master.sh', '-k'])

    def stopworker(self):
        return subprocess.check_output(['/buildbot/buildbot/buildbot.promax.worker.sh', '-k'])

    def config_files(self):
        mask = '.*\.cfg'
        files = ''
        try:
            dir = '/buildbot/buildbot/'.format(self.geo)
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
        config_file = '/buildbot/buildbot/{0}'.format(file.replace('%', '.'))
        if(os.path.isfile(config_file)):
            return subprocess.check_output(['cat', config_file])
        else:
            return 'This file does not exists! [{0}]'.format(config_file)

    def log_files(self, instance='master'):
        mask = '.*\.log'
        files = ''
        try:
            dir = '/buildbot/bb-{0}/{0}/'.format(instance)
            for log_file in os.listdir(dir):
                if(re.match(mask, log_file)):
                    if(files):
                        files = files + ';' + log_file
                    else:
                        files = log_file
        except FileNotFoundError as e:
            files = "File Not Found Error ({0}): {1}".format(e.errno, e.strerror)

        return files

    def logfile_content(self, instance='master', file='twistd.log'):
        log_file = '/buildbot/bb-{0}/{0}/{1}'.format(instance, file.replace('%', '.'))
        if(os.path.isfile(log_file)):
            return subprocess.check_output(['cat', log_file])
        else:
            return 'This file does not exists! [{0}]'.format(log_file)

    def instances(self):
        geo = None

        for dir in os.listdir('/'):
            if(re.match('^[a-z][a-z0-9]$', dir)):
                if(geo):
                    geo = geo + ';' + dir
                else:
                    geo = dir

        return geo


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

