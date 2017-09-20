import os
import re

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

class GitInfo():
    user = 'user'
    password = 'password'
    branch = 'master'

    def __init__(self, config = None):

        if(config):
            self.config = config
        else:
            self.config = '/buildbot/.buildbot/config'

        config_file = open(self.config)
        lines = config_file.read().splitlines()
        config_file.close()
        for line in lines:
            if(re.match('GIT_USER=', line)):
                self.user = line.replace('GIT_USER=', '')
            if(re.match('GIT_PASS=', line)):
                self.password = line.replace('GIT_PASS=', '')
            if(re.match('GIT_BRANCH=', line)):
                self.branch = line.replace('GIT_BRANCH=', '')

    def login(self):
        return '{0}:{1}'.format(self.user, self.password)

class BuildBotInfo():
    workdir = './git-poller'
    buildername = 'promax-linux'
    wwwip = '127.0.0.1'
    wwwport = '8010'
    title = 'Promax'

    def __init__(self, config = None):

        if(config):
            self.config = config
        else:
            self.config = '/buildbot/.buildbot/config'

        config_file = open(self.config)
        lines = config_file.read().splitlines()
        config_file.close()
        for line in lines:
            if(re.match('BB_WORKDIR=', line)):
                self.workdir = line.replace('BB_WORKDIR=', '')
            if(re.match('BB_BUILDERNAME==', line)):
                self.buildername = line.replace('BB_BUILDERNAME=', '')
            if(re.match('BB_WWWIP=', line)):
                self.wwwip = line.replace('BB_WWWIP=', '')
            if(re.match('BB_WWWPORT=', line)):
                self.wwwport = int(line.replace('BB_WWWPORT=', ''))
            if(re.match('BB_TITLE=', line)):
                self.title = line.replace('BB_TITLE=', '')


if __name__ == '__main__':
  g = GitInfo()
  bb = BuildBotInfo()
  print('GIT_USER={0}'.format(g.user))
  print('GIT_PASS={0}'.format(g.password))
  print('GIT_BRANCH={0}'.format(g.branch))
  print('BB_WORKDIR={0}'.format(bb.workdir))
  print('BB_BUILDERNAME={0}'.format(bb.buildername))
  print('BB_WWWIP={0}'.format(bb.wwwip))
  print('BB_WWWPORT={0}'.format(bb.wwwport))
  print('BB_TITLE={0}'.format(bb.title))

