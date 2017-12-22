import os
import re
import sh
import subprocess
from buildbot.config import GitInfo, BuildBotInfo


class BaseControls():
    active = ''
    geos = []
    
    def __init__(self, geo):
        if(len(geo) == 0):
            self.geos = os.popen('ls -d /[a-z][a-z0-9]/ 2>/dev/null').readlines()
            self.geos = [ x.strip('\n').strip('/') for x in self.geos ]
            if(len(geos) > 0):
                self.active = geos[0]
        else:
            self.geos.append(geo)
            self.active = geo

    def status(self):
        if (len(self.geos) == 0):
            return 'Sem geografias disponíveis!'
        else:
            return ' '.join(self.geos)

    def instances(self):
        geo = None

        for dir in os.listdir('/'):
            if(re.match('^[a-z][a-z0-9]$', dir)):
                if(geo):
                    geo = geo + ';' + dir
                else:
                    geo = dir

        return geo    


class ApacheControls(BaseControls):
    def __init__(self, geo = ''):
        super(self.__class__, self).__init__(geo)

    def status(self):
        r = ''
        ps = sh.ps('-ef')
        for item in ps.split('\n'):
            if(re.search('httpd', item)):
                r += (item + '\n')
        if(len(r) == 0):
            r = 'Apache está inativo!'
        return r

    def start(self):
        command = '/amb/boot/S80_httpd_promax_{0}'.format(self.active)
        return subprocess.check_output([command])

    def stop(self):
        command = '/amb/boot/K80_httpd_promax_{0}'.format(self.active)
        return subprocess.check_output([command])

    def config_files(self):
        mask = '.*\.conf'
        files = ''
        try:
            dir = '/{0}/etc/apache/promax/'.format(self.active)
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
        config_file = '/{0}/etc/apache/promax/{1}'.format(self.active, file.replace('%', '.'))
        if(os.path.isfile(config_file)):
            return subprocess.check_output(['cat', config_file])
        else:
            return 'This file does not exists! [{0}]'.format(config_file)

    def log_files(self):
        files = ''
        try:
            dir = '/{0}/promax/log/httpd/'.format(self.active)
            for log_file in os.listdir(dir):
                if(files):
                    files = files + ';' + log_file
                else:
                    files = log_file
        except FileNotFoundError as e:
            files = "File Not Found Error ({0}): {1}".format(e.errno, e.strerror)

        return files

    def logfile_content(self, file):
        log_file = '/{0}/promax/log/httpd/{1}'.format(self.active, file.replace('%', '.'))
        if(os.path.isfile(log_file)):
            return subprocess.check_output(['cat', log_file])
        else:
            return 'This file does not exists! [{0}]'.format(log_file)


class DataBaseControls(BaseControls):
    def __init__(self, geo = ''):
        super(self.__class__, self).__init__(geo)
    

class BuildBotControls(BaseControls):
    geo = ''

    def __init__(self, geo = ''):
        super(self.__class__, self).__init__(geo)

    def status(self):
        #return str(sh.grep(sh.ps('-ef'), 'buildbot'))
        result = os.popen('ps -ef|grep -v grep|grep buildbot').readlines()        
        if (len(result) == 0):
           result = 'Serviço inativo!'
           return result
        
        return result[0]

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
        #return subprocess.check_output(['/buildbot/buildbot/buildbot.promax.master.sh', '-s'])
        result = os.popen('/buildbot/buildbot/buildbot.promax.master.sh -s >/dev/null 2>&1;echo $?').readlines()
        try:
            result = int(result[0])
        except ValueError:
            result = 0

        return not bool(result)

    def startworker(self):
        #return subprocess.check_output(['/buildbot/buildbot/buildbot.promax.worker.sh', '-s'])        
        result = os.popen('/buildbot/buildbot/buildbot.promax.worker.sh -s >/dev/null 2>&1;echo $?').readlines()
        try:
            result = int(result[0])
        except ValueError:
            result = 0

        return not bool(result)

    def stopmaster(self):
        #return subprocess.check_output(['/buildbot/buildbot/buildbot.promax.master.sh', '-k'])
        result = os.popen('/buildbot/buildbot/buildbot.promax.master.sh -k >/dev/null 2>&1;echo $?').readlines()
        try:
            result = int(result[0])
        except ValueError:
            result = 0

        return not bool(result)

    def stopworker(self):
        #return subprocess.check_output(['/buildbot/buildbot/buildbot.promax.worker.sh', '-k'])
        result = os.popen('/buildbot/buildbot/buildbot.promax.worker.sh -k >/dev/null 2>&1;echo $?').readlines()
        try:
            result = int(result[0])
        except ValueError:
            result = 0

        return not bool(result)

    def config_files(self):
        mask = '.*\.cfg'
        files = ''
        try:
            dir = '/buildbot/buildbot/'.format(self.active)
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

    def list_branches(self):
        dir = '/buildbot/gitpoller-workdir/2A/'
        os.chdir(dir)
        result = str(sh.git('branch', '-r'))
        return result.replace('\n', ';').replace(' ', '')


class EnvironControls(BaseControls):
    def __init__(self, geo = ''):
        super(self.__class__, self).__init__(geo)

    def environ(self):
        return subprocess.check_output(['set'])

    def diskusage(self):
        return subprocess.check_output(['df', '-h'])

    def memory(self):
        return subprocess.check_output(['egrep', '"Mem|Cache|Swap"', '/proc/meminfo'])

    def environment_tree(self):
        root = '/' + self.active
        return subprocess.check_output(['find', root, '-type', 'd'])

    def list_dir(self, dir = ''):
        if(len(dir) == 0):
            dir = 'h1'
        if(dir[0] != '/'):
            dir = '/' + dir
        if(os.path.isdir(dir)):
            try:
                result = sh.grep(sh.ls(dir, '-l'), '-v', "^total").stdout
            except Exception as e:
                result = 'Erro ao listar diretório!'
        else:
            result = 'Diretório não existente!'

        return result


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

    def __init__(self, geo):
        #super(self.__class__, self).__init__(geo)
        self.geo = geo
        self.classes = [
            #'BaseControls',
            'ApacheControls',
            'DataBaseControls',
            'BuildBotControls',
            'EnvironControls',
            'JobsControls',
        ]
        self.factory = {}
        for class_name in self.classes:
            klass = globals()[class_name]
            obj = klass(self.geo)
            self.factory[class_name] = obj

    def register_class(self, class_name):
        klass = globals()[class_name]
        obj = klass(self.geo)
        self.factory[class_name] = obj

    def unregister_class(self, class_name):
        self.factory.pop(class_name)

