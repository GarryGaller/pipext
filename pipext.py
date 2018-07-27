#--------------------------------------
"""
Script      : pipext.py
Author      : Garry Galler
Copyright(C): Garry Galler, 2017.  All rights reserved
Version     : 1.0.2
Date        : 27.07.2017
"""
#--------------------------------------
__version__ = '1.0.2'
__author__ = 'Garry Galler'
#--------------------------------------

import os,sys
#from pip import get_installed_distributions
from pip._internal.utils.misc import get_installed_distributions, get_installed_version
#from pip.utils import get_installed_version
#from pip.commands.list import ListCommand
from pip._internal.commands.list import ListCommand
import pip
import argparse
from pprint import pprint
from collections import OrderedDict

def requries(dist):
    """Вспомогательная функция для стрингификации объекта Requirement.parse"""
    results = []
    result = ''
    # [Requirement.parse('six>=1.9.0'), ...]
    for req in dist.requires():
        result += req.name
        # [('>=', '1.9.0')]
        if req.specs:
            result += req.specs[0][0]
            result += req.specs[0][1]
        results.append(result)
        result = ''
    return results or ''


def get_list_modules(select,
                    noformat=None,
                    not_required=False,
                    local_only=False,
                    user_only=False,
                    editables_only=False,
                    ): 
    """Получить расширенный список всех инсталлированных модулей"""
    
    list_modules = []
    distribs = get_installed_distributions(
        local_only=local_only,
        user_only=user_only,
        editables_only=editables_only
        )
    #-------------------------------
    cmd = ListCommand() 
    if '-o' in select:
        options,args = cmd.parser.parse_args(select)
        distribs = cmd.get_outdated(distribs,options)
    
    if '-u' in select:
        options,args = cmd.parser.parse_args(select)
        distribs = cmd.get_uptodate(distribs,options)
    #------------------------------
    list_not_required = []
    if not_required == 1:
        options,args = cmd.parser.parse_args(select)
        distribs = cmd.get_not_required(distribs,options)
    elif not_required == 2:
        for dist in distribs:
            if requries(dist) == "":
                list_not_required.append(dist)    
        distribs = list_not_required
        del list_not_required 
    #-------------------------------
    if noformat == 'name':
        for dist in distribs:
            list_modules.append(dist.project_name)
        list_modules.sort()
    
    elif noformat == 'egg':
        for dist in distribs:
            list_modules.append(dist.egg_name())
        list_modules.sort()
    
    elif noformat is None:
        for dist in distribs:
            list_modules.append({
            '0 Package':dist.project_name, 
            '1 Version':dist.version, 
            '2 Location':dist.location, 
            '3 Latest':str(dist.latest_version) if set(select) & {'-o','-u'} else str(None),
            '4 Type':str(dist.latest_filetype) if set(select) & {'-o','-u'} else str(None),
            '5 Python':str(dist.py_version)  if set(select) & {'-o','-u'} else str(None),
            '6 Depends':str(requries(dist))
            })
    
        list_modules.sort(key=lambda x:x['0 Package'].lower())   
    
    return list_modules 


def update_modules(select,install_opts,distribs=None,exclude=None,extended_opts=None): 
    """Обновить все модули либо только указанные в списке
    >> update_modules(['-o'],['--upgrade'])
    >> update_modules(None,['--upgrade'])
    >> update_modules(None,['--upgrade'],['comtypes','cssselect','pony'])
    """
    if extended_opts is None:
        extended_opts = (False,False,False,False)
    
    if not distribs:
        distribs = [name for name in get_list_modules(select,'name',*extended_opts)]
    
    if isinstance(exclude,(list,set,tuple)):
        distribs = set([i.lower() for i in distribs]) - set([i.lower() for i in exclude])
        
    if not distribs:
        return print('No modules of the specified type were found.')
    
    for dist_name in distribs:
        pip.main(['install',*install_opts, dist_name])
        
#-----------------------
def tabulate(modules,columns):           
    # вычисление отступов
    #-----------------------
    headers = OrderedDict()
    separator = {}
    sformat = ''
    
    for line in modules:
        for key in ('0 Package','1 Version','2 Location','3 Latest', '4 Type','5 Python','6 Depends'):
            if headers.get(key) is None:
                headers[key] = []
            headers[key].append(len(line[key]))
        
    for key,val in headers.items():
        headers[key] = max(val) + 2  
        if headers[key] < len(key) + 2:
            headers[key] = len(key) + 2
        
    headers = list(headers.items()) # преобразуем в список кортежей
    # создание строки форматирования для заголовков
    for i in columns:
        sformat += '{' + headers[i][0] + ':' + str(headers[i][1])  +'}'
        separator.update({headers[i][0]:(headers[i][1]-2) * '-'})
        # создание строки сепаратора
    sep = sformat.format(**separator)
    return (headers,sformat,sep)

#--------------------------------------    
# обработка завершения программы по Ctrl+C
#-------------------------------------- 
_old_excepthook = sys.excepthook

def on_exit_by_ctrl_c(exctype, value, traceback):
    if exctype == KeyboardInterrupt:
        sys.stdout.write('\nExecution aborted\n')
        sys.exit(0)    
    else:
        _old_excepthook(exctype, value, traceback)

sys.excepthook = on_exit_by_ctrl_c

#===============================
# обоработка аргументов командной строки
#===============================
def argument_parse(argv=None):
    description = """
Script      : %(prog)s
Author      : {author}
Copyright(C): {author}, 2017.  All rights reserved
Version     : {version}""" .format(
    author=__author__,version= __version__
)
    
    parser = argparse.ArgumentParser(
        formatter_class = argparse.RawDescriptionHelpFormatter,
        description = description,
       )
    parser.add_argument('-s','--select', 
                    type = str,  
                    nargs = '+',
                    help = """Module selection type: 
                    a|all|full     - all installed (by default), 
                    o|out|outdated - outdated,
                    u|up|uptodate  -  uptodated
                    """)
    
    group_main = parser.add_mutually_exclusive_group()
    group_main.add_argument('--raw',
                    type = str,
                    help = "Raw options")
    
    group_main.add_argument('-i','--install',
                    type = str,
                    nargs = '+',
                    help = """List of parameters to update.
                    u,U,upgrade:  --upgrade,-U; 
                    if,if-needed: --upgrade-strategy only-if-needed;
                    eager:        --upgrade-strategy eager;
                    f,force:      -U --force-reinstall;
                    i,ignore:     --ignore-installed;
                    """)
    
    group_i = parser.add_argument_group('install')
    group_i.add_argument('-m','--modules',
                    type = str,
                    nargs = '+',
                    help = 'The list of modules to update.'
                    )
    
    group_i.add_argument('-e','--exclude',
                    type = str,
                    nargs = '+',
                    help = 'The list of modules to exclude from the update. Only option -U')
    
    group_i.add_argument('--no-deps', 
                    action = 'store_true',  
                    default = False,  
                    help = "Don't install package dependencies.")
    
    group_c = parser.add_mutually_exclusive_group()
    group_c.add_argument('-c','--columns',
                    type = int,
                    nargs = '+',
                    help = """List of the number of columns to display in the range 0-6.
                    By default, when using --select=all displayed columns 0,1,2,6,
                    when using --select=out - extended version - 0,1,3,4,5,6 - without the Location column.""")
    
    group_c.add_argument('-C',
                    type = int,
                    nargs = '+',
                    help = """List of columns to exclude.""")
    
    
    parser.add_argument('--pre', 
                    action = 'store_true',  
                    default = False,  
                    help = "Include pre-release and development versions. By default, pip only finds stable versions.")
    
    group_f = parser.add_mutually_exclusive_group()
    group_f.add_argument('-f','--format',
                    type = str,
                    nargs = '+',
                    default = ['header'],
                    help = """List of output formatting options: 
                    header|head|h - to show headings,
                    separator|sep|s - to separate lines.""")
    
    group_f.add_argument('-F','--no-format', 
                    type = str,  
                    help = """Output only a list of names. 
                    name - for standard names, 
                    egg - names in the format egg, 
                    count - output only the number of modules""")
    
    group_nr = parser.add_mutually_exclusive_group()
    group_nr.add_argument('--not-req', 
                    action = 'store_true',  
                    default = False,  
                    help = "List packages that are not dependencies of installed packages (original option).")
    
    group_nr.add_argument('--not-req2', 
                    action = 'store_true',  
                    default = False,  
                    help = "List of packages that do not have dependencies.")
    
    group_t = parser.add_mutually_exclusive_group()
    group_t.add_argument('--editable', 
                    action = 'store_true',  
                    default = False,  
                    help = "List editable projects.")
    
    group_t.add_argument('--user', 
                    action = 'store_true',  
                    default = False,  
                    help = "Only output packages installed in user-site.")
    
    group_t.add_argument('--local', 
                    action = 'store_true',  
                    default = False,  
                    help = "If in a virtualenv that has global access, do not list globally-installed packages.")
    
    parser.add_argument('--test', 
                    action = 'store_true',  
                    default = False,
                    help = "Test options")
    
    parser.add_argument('-v','--version', 
                    type = str,  
                    help = "The version of the installed module: --version pip")

    
    return parser,vars(parser.parse_args(argv))

#===============================
# разбор аргументов
#===============================
def main(argv=None):
    parser,options = argument_parse(argv)
    
    if options is None:return
  
    if options['version']:
        return print(get_installed_version(options['version']))
    
    #-----------------------
    # трансформация опций
    #-----------------------
    transforms_i = {
        ('u','U','upgrade'):['--upgrade'],
        ('if','if-needed' ):['--upgrade-strategy','only-if-needed'],
        ('eager'          ):['--upgrade-strategy','eager'],
        ('f','force'      ):['-U','--force-reinstall'],
        ('i','ignore'     ):['--ignore-installed'],
        }
    
    transforms_s = {
        ('a','all','full'     ):[],
        ('o','out','outdated' ):['-o'],
        ('u','up','uptodate'  ):['-u'],
        }
    #-----------------------
    if options['not_req']:
        not_required = 1 
    elif options['not_req2']:
        not_required = 2 
    else:
        not_required = False
    #-----------------------
    select = options['select']
    if select is None:  
        select = []
    else:
         matches = False
         for key,val in transforms_s.items():
            if  set(key) & set(select):
                select = val
                matches = True
         
         if not matches: 
            return parser.print_usage() 
    #-----------------------
    if options['pre']:
        if select:
            select.append('--pre')     
        else:
            print('The --pre option is ignored.\n')
    
    extended_opts = not_required,options['local'], options['user'], options['editable']
    #-----------------------
    
    if options['columns']:
        operation = set.union
        columns = set(options['columns'])
    elif options['C']:    
        operation = set.difference
        columns = set(options['C'])
    else:
        operation = set.union
        columns = set()
    
    if '-o' in select:
        columns = sorted(operation(set([0,1,3,4,5,6]),columns))
    elif '-u' in select:
        columns = sorted(operation(set([0,1,3,4,5]),columns))
    else:
        columns = sorted(operation(set([0,1,2,6]),columns))
    if not columns: return print('Specify at least one column')
    options['columns'] = columns    
    
    if not all(0 <= i < 7 for i in columns):
        return print('[--columns] The column index should be in the range from 0 to 6')
    
    #-------------------------------
    modules = options['modules']
    exclude = options['exclude']
    install_opts = options['raw']
    if install_opts:
        install_opts = install_opts.split()
        options['install'] = install_opts
    else:
        if options['install']:
            install_opts = options['install']
            matches = False
        
            for key,val in transforms_i.items():
                if  set(key) & set(install_opts):
                    install_opts = val
                    matches = True
        
            if not matches: 
                return parser.print_usage()
            if options['no_deps']:
                install_opts.append('--no-deps')     
            
            options['install'] = install_opts
            
            if options['select'] is None:
                select = ['-o']
        else:
            if options['no_deps']:
                print('The --no-deps option is ignored.\n')        
    
    #-----------------------
    options['select'] = select      
    #-----------------------
    if options['test']:
        return pprint(options)
    elif install_opts:
        print('Install|upgrade options:{}\nType:{}\nModules:{}\nExclude:{}'.format(
                install_opts,select,modules,exclude)
            )
        print('-'*20)
        return update_modules(  
            select,
            install_opts,
            modules,
            exclude,
            extended_opts
            )
    
    #-----------------------
    # если не обновление и не тест опций - читаем опции форматирования
    #-----------------------
    format = set(options['format'])
    noformat = options['no_format']
    print_header = {'header','head','h'} & format
    print_sep = {'separator','sep','s'} & format
        
    if noformat not in ['egg','name','count',None]:
        return print('[--no-format] Unknown format. Use egg, name or count.') 
               
    if noformat == 'count':
        return print(len(get_list_modules(select,'name',*extended_opts)))
       
    modules = get_list_modules(select,noformat,*extended_opts)  
    if not modules:
        return print('No modules of the specified type were found.')
    
    if noformat in ['egg','name']:
        for m in modules:        
            print(m)  
        #-----------------------
        # форматированный вывод
        #-----------------------
    else:
        headers,sformat,sep = tabulate(modules,columns)
        #-----------------------
        if print_header:
            print(sep)
            print(sformat.format(**{h[0]:h[0] for h in headers})) 
            print(sep)
            
        for m in modules:
            print(sformat.format(**m))     
            if print_sep:
                print(sep)
    
#===============================
# запуск модуля как скрипт
#===============================
if  __name__== '__main__':
    sys.exit(main())
    

    
