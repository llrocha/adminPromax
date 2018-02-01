import os
import re
import sh
import glob
import subprocess
from buildbot.config import GitInfo, BuildBotInfo


class BaseControls():

    def __init__(self, geo):
        self.geo = geo

    def instances(self):

        self.geos = glob.glob('/[a-z][a-z0-9]/')
        self.geos = [ x.strip('/') for x in self.geos ]
        self.geos = ';'.join(self.geos)

        return self.geos


class ApacheControls(BaseControls):
    def __init__(self, geo):
        super(self.__class__, self).__init__(geo)

    def status(self):
        r = ''
        command = 'ps -ef'
        ps = os.popen(command).read()
        for item in ps:
            if(re.search('httpd', item)):
                r += (item + '\n')
        if(len(r) == 0):
            r = 'Apache está inativo!'
        return r

    def start(self):
        command = '/amb/boot/S80_httpd_promax_{0}'.format(self.geo)
        return os.popen(command).read()

    def stop(self):
        command = '/amb/boot/K80_httpd_promax_{0}'.format(self.geo)
        return os.popen(command).read()

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
            command = 'cat {0}'.format(config_file)
            return os.popen(command).read()
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
            command = 'cat {0}'.format(log_file)
            return os.popen(command).read()
        else:
            return 'This file does not exists! [{0}]'.format(log_file)


class DataBaseControls(BaseControls):
    def __init__(self, geo = ''):
        super(self.__class__, self).__init__(geo)

    def list_available_dat(self):
        result = os.popen('ls -d /dev/mapper/vgpromax_??-dat').read()
        if (len(result) == 0):
           result = 'Sem bases disponíveis.'
           return result
        
        return result


    def mount_dat(self, fs = ''):
        umount = 'umount /{0}/promax/dat >/dev/null 2>&1'.format(self.geo) 
        mount = 'mount {0} /{1}/promax/dat >/dev/null 2>&1'.format(fs, self.geo)
        os.popen(umount).read()
        result = os.popen(mount).read()
        if (len(result) == 0):
           result = 'File system montado com sucesso.'
           return result
        
        return result

    

class BuildBotControls(BaseControls):
    geo = ''

    def __init__(self, geo = ''):
        super(self.__class__, self).__init__(geo)

    def status(self):
        result = os.popen('ps -ef|grep -v grep|grep buildbot').read()
        if (len(result) == 0):
           result = 'Serviço inativo!'
           return result
        
        return result

    def stop(self):
        master = self.stopmaster()
        worker = self.stopworker()

        result = 'Erro ao parar os serviços!'
        if (master and worker):
            result = 'Sucesso serviços parados!'
        elif(not master):
            result = 'Não foi possível parar o MASTER!'
        elif(not worker):
            result = 'Não foi possível parar o WORKER!'

        return result        

    def start(self):
        master = self.startmaster()
        worker = self.startworker()

        result = 'Erro ao iniciar os serviços!'
        if (master and worker):
            result = 'Sucesso serviços ativos!'
        elif(not master):
            result = 'Não foi possível iniciar o MASTER!'
        elif(not worker):
            result = 'Não foi possível iniciar o WORKER!'

        return result
                        
    def startmaster(self):
        result = os.popen('/buildbot/buildbot/buildbot.promax.master.sh -s >/dev/null 2>&1;echo $?').read()
        try:
            result = int(result[0])
        except ValueError:
            result = 0

        return not bool(result)

    def startworker(self):
        result = os.popen('/buildbot/buildbot/buildbot.promax.worker.sh -s >/dev/null 2>&1;echo $?').read()
        try:
            result = int(result[0])
        except ValueError:
            result = 0

        return not bool(result)

    def stopmaster(self):
        result = os.popen('/buildbot/buildbot/buildbot.promax.master.sh -k >/dev/null 2>&1;echo $?').read()
        try:
            result = int(result[0])
        except ValueError:
            result = 0

        return not bool(result)

    def stopworker(self):
        result = os.popen('/buildbot/buildbot/buildbot.promax.worker.sh -k >/dev/null 2>&1;echo $?').read()
        try:
            result = int(result[0])
        except ValueError:
            result = 0

        return not bool(result)

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
            command = 'cat ' + config_file
            return os.popen(command).read()
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
            command = 'cat' + log_file
            return os.popen(command).read()
        else:
            return 'This file does not exists! [{0}]'.format(log_file)

    def list_branches(self):
        dir = '/buildbot/gitpoller-workdir/2A/'
        os.chdir(dir)
        command = 'git branch -r'
        result = os.popen(command).read()
        result = result.replace('\n', ';').replace(' ', '')
        return result.strip(';')


class EnvironControls(BaseControls):
    def __init__(self, geo = ''):
        super(self.__class__, self).__init__(geo)

    def environ(self):
        command = 'set'
        return os.popen(command).read()

    def diskusage(self):
        command = 'df -h'
        return os.popen(command).read()

    def memory(self):
        command = 'egrep "Mem|Cache|Swap" /proc/meminfo'
        return os.popen(command).read()

    def environment_tree(self):
        root = '/' + self.geo
        command = 'find ' + root + ' -type d'
        return os.popen(command).read()

    def list_dir(self, dir = ''):
        dir = dir.strip('/')
        dir = '/{0}/'.format(dir)

        if(os.path.isdir(dir)):
            try:
                command = 'ls -l {0}|grep -v "^total"'.format(dir)
                result = os.popen(command).read()
            except Exception as e:
                result = 'Erro ao listar diretório!'
        else:
            result = 'Diretório não existente!'

        return result

    def build_promax(self, path = 'buildenv'):
        command = 'cd {0};./criar_geo.sh {1} {0} 2>&1'.format(path, self.geo)
        return os.popen(command).read()

class JobsControls(BaseControls):
    def __init__(self, geo = ''):
        super(self.__class__, self).__init__(geo)

    def startjob(self, job):
        pass

    def stopjob(self, job):
        pass

    def jobs(self, job):
        pass


class ServerControls():
    """
    """
    def __init__(self):
        #super(self.__class__, self).__init__(geo)

        self.geos = glob.glob('/[a-z][a-z0-9]/')
        self.geos = [ x.strip('/') for x in self.geos ]
        
        self.classes = [
            'BaseControls',
            'ApacheControls',
            'DataBaseControls',
            'BuildBotControls',
            'EnvironControls',
            'JobsControls',
        ]

        self.factory = {}
        for geo in self.geos: 
            geo_factory = {}
            for class_name in self.classes:
                klass = globals()[class_name]
                obj = klass(geo)
                geo_factory[class_name] = obj
            self.factory[geo] = geo_factory

    def register_class(self, class_name):
        klass = globals()[class_name]
        obj = klass(self.geo)
        self.factory[class_name] = obj

    def unregister_class(self, class_name):
        self.factory.pop(class_name)

