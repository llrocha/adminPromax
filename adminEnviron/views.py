from django.shortcuts import get_object_or_404, render

from datetime import datetime
from django.views import generic
from django.http import HttpRequest, HttpResponse

from adminClasses.adminClasses import BaseView

from controlServer.controlclient import ExecuteRemoteCommand

import urllib.request
import re
import os

# Create your views here.

def index(request):
    """Renders the 'index' page."""
    assert isinstance(request, HttpRequest)

    context = BaseView(request).context()
    context.update({
            'menu':'adminEnviron',
            'appname':'adminPromax',
            'title':'adminEnviron/Index',
            'year':datetime.now().year,
            'request':request,
        })

    return render(
        request,
        'adminEnviron/index.html',
        context
    )


def monitoramento(request):
    """Renders the 'index' page."""
    assert isinstance(request, HttpRequest)

    context = BaseView(request).context()
    context.update({
            'menu':'adminEnviron',
            'appname':'adminPromax',
            'title':'adminEnviron/Monitoramento',
            'year':datetime.now().year,
            'request':request,
        })

    return render(
        request,
        'adminEnviron/monitoramento.html',
        context
    )


def instancias(request, geo = ''):
    """Renders the 'instancias' page."""
    assert isinstance(request, HttpRequest)

    context = BaseView(request).context()
    geo = context['geo']
    server = context['server']
    port = int(context['port'])

    instancias = ExecuteRemoteCommand(server, port, 'ApacheControls->instances->' + geo)
    instancias = instancias.split(';')

    context.update({
            'menu':'adminEnviron/instancias',
            'appname':'adminPromax',
            'title':'adminEnviron/Instâncias',
            'year':datetime.now().year,
            'request':request,
            'instancias': instancias,
            'errors': []
        })

    return render(
        request,
        'adminEnviron/instancias.html',
        context
    )


def insert_dict(d, l):
    if(len(l)):
        if(not l[0] in d.keys()):
            d[l[0]] = {}
        d[l[0]] = insert_dict(d[l[0]], l[1:])
    else:
        d = {}
    return d


def create_tree(d, l):
    r = ''
    l += 1
    for k, v in d.items():
        
        if(len(v) > 0):
            r += '{0}<li><a href="#">{1}</a>\n{0}  <ul>'.format('\t'*l, k)
            r += create_tree(v, l)
            r += '{0}  </ul>\n{0}</li>'.format('\t'*l)
        else:
            r += '{0}<li>{1}</li>'.format('\t'*l, k)
    return r


def show_tree(request, geo = ''):
    """Renders the 'controle' page."""
    assert isinstance(request, HttpRequest)

    context = BaseView(request).context()
    geografia = context['geo']
    if(len(geo) > 0):
        geografia = geo.strip('/')
    server = context['server']
    port = int(context['port'])
    
    command = 'EnvironControls->environment_tree->{0}'.format(geografia)
    path_list = ExecuteRemoteCommand(server, port, command)
    
    tree = {}    
    for path in path_list.split():
        path = path.split('/')
        path.remove('')
        insert_dict(tree, path)
    
    html_tree = create_tree(tree, 0)

    context.update({
            'menu':'adminEnviron/construcao',
            'appname':'adminPromax',
            'title':'adminEnviron/Index',
            'year':datetime.now().year,
            'request':request,
            'html_tree': html_tree
        })

    return render(
        request,
        'adminEnviron/treeview.html',
        context
    )


def visualizacao(request, dir = ''):
    icons = {
        '*': ['default.png', '[   ]'],
        '7z': ['archive.png', '[   ]'],
        'URL': ['html.png', '[TXT]'],
        'aac': ['audio.png', '[SND]'],
        'ai': ['eps.png', '[   ]'],
        'aif': ['audio.png', '[SND]'],
        'aifc': ['audio.png', '[SND]'],
        'aiff': ['audio.png', '[SND]'],
        'ape': ['audio.png', '[SND]'],
        'asf': ['video.png', '[VID]'],
        'asx': ['video.png', '[VID]'],
        'au': ['audio.png', '[SND]'],
        'avi': ['video.png', '[VID]'],
        'bat': ['script.png', '[TXT]'],
        'bin': ['bin.png', '[HEX]'],
        'bmp': ['bmp.png', '[IMG]'],
        'bz2': ['archive.png', '[HEX]'],
        'c': ['c.png', '[TXT]'],
        'cab': ['archive.png', '[   ]'],
        'cmd': ['script.png', '[TXT]'],
        'cpp': ['cpp.png', '[TXT]'],
        'css': ['css.png', '[TXT]'],
        'csv': ['calc.png', '[TXT]'],
        'deb': ['deb.png', '[PKG]'],
        'dmg': ['package.png', '[PKG]'],
        'doc': ['doc.png', '[DOC]'],
        'docm': ['doc.png', '[DOC]'],
        'docx': ['doc.png', '[DOC]'],
        'dot': ['doc.png', '[DOC]'],
        'dotm': ['doc.png', '[DOC]'],
        'dotx': ['doc.png', '[DOC]'],
        'eps': ['eps.png', '[   ]'],
        'exe': ['exe.png', '[HEX]'],
        'f4a': ['audio.png', '[SND]'],
        'f4b': ['audio.png', '[SND]'],
        'f4p': ['video.png', '[VID]'],
        'f4v': ['video.png', '[VID]'],
        'flac': ['audio.png', '[SND]'],
        'flv': ['video.png', '[VID]'],
        'gif': ['gif.png', '[IMG]'],
        'gz': ['archive.png', '[   ]'],
        'h': ['h.png', '[TXT]'],
        'hex': ['bin.png', '[HEX]'],
        'htm': ['html.png', '[TXT]'],
        'html': ['html.png', '[TXT]'],
        'ico': ['ico.png', '[IMG]'],
        'iff': ['audio.png', '[SND]'],
        'iso': ['cd.png', '[   ]'],
        'it': ['audio.png', '[SND]'],
        'jar': ['java.png', '[TXT]'],
        'jpe': ['jpg.png', '[IMG]'],
        'jpeg': ['jpg.png', '[IMG]'],
        'jpg': ['jpg.png', '[IMG]'],
        'js': ['js.png', '[TXT]'],
        'json': ['js.png', '[TXT]'],
        'log': ['doc.png', '[TXT]'],
        'm3u': ['playlist.png', '[   ]'],
        'm3u8': ['playlist.png', '[   ]'],
        'm4a': ['audio.png', '[SND]'],
        'm4v': ['video.png', '[VID]'],
        'md': ['markdown.png', '[   ]'],
        'mid': ['audio.png', '[SND]'],
        'mkv': ['video.png', '[VID]'],
        'mod': ['audio.png', '[SND]'],
        'mov': ['video.png', '[VID]'],
        'mp3': ['audio.png', '[SND]'],
        'mp4': ['video.png', '[VID]'],
        'mpa': ['audio.png', '[SND]'],
        'mpg': ['video.png', '[VID]'],
        'msg': ['doc.png', '[DOC]'],
        'nfo': ['text.png', '[TXT]'],
        'odt': ['doc.png', '[DOC]'],
        'oga': ['audio.png', '[SND]'],
        'ogg': ['audio.png', '[SND]'],
        'ogv': ['video.png', '[VID]'],
        'pages': ['doc.png', '[DOC]'],
        'pdf': ['pdf.png', '[   ]'],
        'php': ['php.png', '[TXT]'],
        'phtml': ['php.png', '[TXT]'],
        'pkg': ['package.png', '[PKG]'],
        'pls': ['playlist.png', '[   ]'],
        'pls8': ['playlist.png', '[   ]'],
        'png': ['png.png', '[IMG]'],
        'ps': ['ps.png', '[   ]'],
        'psd': ['psd.png', '[   ]'],
        'py': ['py.png', '[TXT]'],
        'ra': ['audio.png', '[SND]'],
        'rar': ['rar.png', '[   ]'],
        'rb': ['rb.png', '[TXT]'],
        'rm': ['video.png', '[VID]'],
        'rpm': ['rpm.png', '[PKG]'],
        'rss': ['rss.png', '[TXT]'],
        'rtf': ['doc.png', '[DOC]'],
        's3m': ['audio.png', '[SND]'],
        'sass': ['css.png', '[TXT]'],
        'scss': ['css.png', '[TXT]'],
        'sh': ['script.png', '[TXT]'],
        'shtml': ['html.png', '[TXT]'],
        'sql': ['sql.png', '[TXT]'],
        'srt': ['video.png', '[VID]'],
        'svg': ['draw.png', '[   ]'],
        'svgz': ['draw.png', '[   ]'],
        'swf': ['video.png', '[VID]'],
        'tar': ['archive.png', '[   ]'],
        'tex': ['doc.png', '[DOC]'],
        'tif': ['tiff.png', '[IMG]'],
        'tiff': ['tiff.png', '[IMG]'],
        'txt': ['text.png', '[TXT]'],
        'url': ['html.png', '[TXT]'],
        'vob': ['video.png', '[VID]'],
        'wav': ['audio.png', '[SND]'],
        'wma': ['audio.png', '[SND]'],
        'wmv': ['video.png', '[VID]'],
        'wpd': ['doc.png', '[DOC]'],
        'wps': ['doc.png', '[DOC]'],
        'xhtml': ['html.png', '[TXT]'],
        'xlam': ['calc.png', '[   ]'],
        'xlr': ['calc.png', '[   ]'],
        'xls': ['calc.png', '[   ]'],
        'xlsm': ['calc.png', '[   ]'],
        'xlsx': ['calc.png', '[   ]'],
        'xltm': ['calc.png', '[   ]'],
        'xltx': ['calc.png', '[   ]'],
        'xm': ['audio.png', '[SND]'],
        'xml': ['xml.png', '[TXT]'],
        'zip': ['zip.png', '[ZIP]']
    }
    """Renders the 'index' page."""
    
    assert isinstance(request, HttpRequest)

    context = BaseView(request).context()
    geografia = context['geo']
    server = context['server']
    port = int(context['port'])


    if(len(dir) == 0):
        dir = '/{0}'.format(geografia)

    if(dir.find('->') > 0):
        dir = dir.split()[0]


    command = 'EnvironControls->list_dir->{0}->{1}'.format(geografia, dir)
    result = ExecuteRemoteCommand(server, port, command)
    result = result.split('\n')
    files = []
    for line in result:
        if(len(line) > 0):
            l = line.split()
            d = {}
            d['icon'] = icons['*'][0]
            d['alt'] = icons['*'][1]            
            if(len(l) >= 8):
                i = l[8].split('.')
                if(l[0][0] == 'd'):
                    d['icon'] = 'folder.png'
                    d['alt'] = '[DIR]'
                else:
                    if(len(i) > 1):
                        if(i[1] in icons.keys()):
                            d['icon'] = icons[i[1]][0]
                            d['alt'] = icons[i[1]][1]

                d['file'] = ' '.join(l[8:])
                d['permissions'] = l[0]
                if(d['permissions'][0] == 'd'):
                    d['dir'] = True
                else:
                    d['dir'] = False
                d['user'] = l[2]
                d['group'] = l[3]
                d['size'] = l[4]
                d['last_modified'] = ' '.join(l[5:8])                
                files.append(d)
            
    path = dir
    if(len(path) == 0):
        path = dir.strip('/')

    context.update({
            'menu':'adminEnviron/visualizacao',
            'appname':'adminPromax',
            'title':'adminEnviron/Index',
            'year':datetime.now().year,
            'request':request,
            'webdav': files,
            'path': dir,
        })

    return render(
        request,
        'adminEnviron/visualizacao.html',
        context
    )


def build_promax(request, geo, dir = ''):
    assert isinstance(request, HttpRequest)

    context = BaseView(request).context()
    geografia = context['geo']
    if(len(geo) > 0):
        geografia = geo.strip('/')
    server = context['server']
    port = int(context['port'])
    build_promax_path = context['build_promax_path']

    command = 'EnvironControls->build_promax->{0}->{1}'.format(geografia, build_promax_path)
    result = ExecuteRemoteCommand(server, port, command)

    context.update({
            'menu':'adminEnviron/visualizacao',
            'appname':'adminPromax',
            'title':'adminEnviron/Index',
            'year':datetime.now().year,
            'request':request,
            'result': result
        })

    return render(
        request,
        'adminEnviron/construcao.html',
        context
    )