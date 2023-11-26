"""General installation information"""


class _bm:
    from logging import basicConfig, DEBUG, INFO, WARN, ERROR, CRITICAL
    from os.path import exists, abspath
    from json import load, dumps
    from typing import Union
    from os import listdir

    from ._external import create, enable, disable, close, run

    class LoggingLevel:
        pass

    defaultData: dict = {
        "cache": {
            "errors": {},
            "global": {
                "configMethodValues": {}
            },
            "info": {},
            "main": {},
            "requests": {
                "verifiableTimesChecked": 0,
                "verifiableNetworkList": {},
                "connectedTimesChecked": 0,
                "connectedNetworkList": {}
            },
            "sys.info": {},
            "sys": {}
        },
        "config": {
            "errors": {},
            "global": {
                "config": {
                     "runConfigMethodAlways": False,
                     "configMethodCheck": 20
                } 
            },
            "info": {},
            "main": {},
            "requests": {
                "defaultHttpVerificationMethod": True,
                "defaultVerificationMethod": True,
                "verifiableCachingCheck": 20,
                "connectedCachingCheck": 20,
                "verifiableCaching": False,
                "connectedCaching": False
            },
            "sys.info": {},
            "sys": {}
        }
    }

    openData           = None
    actualConfig: dict = defaultData['config']


author:            str = str('feetbots')
"""The current owner of tooltils"""
author_email:      str = str('pheetbots@gmail.com')
"""The email of the current owner of tooltils"""
maintainer:        str = str('feetbots')
"""The current sustainer of tooltils"""
maintainer_email:  str = str('pheetbots@gmail.com')
"""The email of the current sustainer of tooltils"""
version:           str = str('1.5.3')
"""The current installation version"""
released:          str = str('25/11/2023')
"""The release date of the current version"""
description:       str = str('A lightweight python utility package built on the standard library')
"""The short description of tooltils"""
classifiers: list[str] = [
    "Programming Language :: Python :: 3",
    "Programming Language :: Python :: 3.7",
    "Programming Language :: Python :: 3.12",
    "License :: OSI Approved :: MIT License",
    "Operating System :: OS Independent"
]
"""The list of PyPi style tooltils classifiers"""
homepage:          str = str('https://github.com/feetbots/tooltils')
"""The current home website of tooltils"""
homepage_issues:   str = str('https://github.com/feetbots/tooltils/issues')
"""The current issues directory of the home website of tooltils"""
location:          str = str('/'.join(__file__.split('/')[:-1]) + '/')
"""The path of the current installation of tooltils"""

if not _bm.exists(location + 'data.json'):
    with open(location + 'data.json', 'a+') as _f:
        _f.write(_bm.dumps(_bm.defaultData, indent=4))

_location: str = '/'.join(location.split('/')[:-2]) + f'/tooltils-{version}.dist-info/'

with open(_location + 'LICENSE') as _f:
    _lt = _f.read()

with open(_location + 'METADATA') as _f:
    _ld = _f.read().split('LICENSE')[1]

license:   tuple[str] = (str('MIT License'), str(_lt))
"""The name and content of the currently used license in a tuple pair (name, content)"""
long_description: str = str(_ld)
"""The long description of tooltils"""

def _getData():
    if _bm.openData is None:
        _configMethods()

    return _bm.openData

def _loadCache(module: str='') -> dict:
    _f = _getData()
    data: dict = _bm.load(_f)['cache']
    _f.seek(0)

    if module == '':
        return data
    else:
        return data[module]

def _editCache(module: str, option: dict, subclass: str='') -> None:
    _f = _getData()
    data = _bm.load(_f)

    if subclass:
        data['cache'][module][subclass].update(option)
    else:
        data['cache'][module].update(option)

    _f.seek(0)
    _f.truncate()
    _f.write(_bm.dumps(data, indent=4))
    _f.seek(0)

def _deleteCacheKey(module: str, key: str, subclass: str='') -> None:
    _f = _getData()
    data = _bm.load(_f)

    if subclass:
        keys = data['cache'][module][subclass].keys()
    else:
        keys = data['cache'][module].keys()

    for i in list(keys):
        if key == i:
            if subclass:
                data['cache'][module][subclass].pop(i)
            else:
                data['cache'][module].pop(i)

    _f.seek(0)
    _f.truncate()
    _f.write(_bm.dumps(data, indent=4))
    _f.seek(0)

def _loadConfig(module: str='') -> dict:
    if module == '':
        return _bm.actualConfig
    else:
        return _bm.actualConfig[module]

#def _editConfig(module: str, option: dict, subclass: str='') -> None:
#    _f = _getData()
#    data: dict = _bm.load(_f)
#
#    if subclass:
#        data['config'][module][subclass].update(option)
#    else:
#        data['config'][module].update(option)
#
#    _f.seek(0)
#    _f.truncate()
#    _f.write(_bm.dumps(data, indent=4))
#    _f.seek(0)

def clearCache(module: str=None) -> None:
    """Clear the file cache of tooltils or a specific module within"""

    module: str = str(module).lower()
    _f          = _getData()
    wdata: dict = _bm.load(_f)

    if module == 'none':
        data: dict = _bm.defaultData['cache']
    else:
        data: dict = wdata['cache']

        try:
            data.update(_bm.defaultData['cache'][module])
        except KeyError:
            raise FileNotFoundError('Cache module not found')
        
    wdata['cache'] = data

    _f.seek(0)
    _f.truncate(0)
    _f.write(_bm.dumps(wdata, indent=4))
    _f.seek(0)

def clearConfig(module: str=None) -> None:
    """Revert the config of tooltils or a specific module within"""

    module: str = str(module).lower()
    _f          = _getData()
    wdata: dict = _bm.load(_f)

    if module == 'none':
        data: dict = _bm.defaultData['config']
    else:
        data: dict = wdata['config']

        try:
            data.update(_bm.defaultData['config'][module])
        except KeyError:
            raise FileNotFoundError('Config module not found')
        
    wdata['config'] = data

    _f.seek(0)
    _f.truncate(0)
    _f.write(_bm.dumps(wdata, indent=4))
    _f.seek(0)

def clearData() -> None:
    """Clear the cache and config of tooltils"""

    _f         = _getData()
    data: dict = _bm.load(_f)
    data.update(_bm.defaultData)

    _f.seek(0)
    _f.truncate(0)
    _f.write(_bm.dumps(data, indent=4))
    _f.seek(0)

class logger():
    """Create a logging instance for tooltils modules only"""

    def enable(self) -> None:
        _bm.enable(self._logger, self.enabled, self.closed)

    def disable(self) -> None:
        _bm.disable(self._logger, self.enabled, self.closed)
    
    def close(self) -> None:
        _bm.close(self._logger, self.closed)

    @property
    def module(self) -> str:
        """What module the logging is enabled for"""

        return self._module
    
    @module.setter
    def module(self, value):
        raise AttributeError('Module property cannot be changed')

    @property
    def level(self) -> _bm.Union[str, int, _bm.LoggingLevel]:
        """What level of logging is being used"""

        return self._level
    
    @level.setter
    def level(self, value):
        raise AttributeError('Level property cannot be changed')
    
    @property
    def level2(self) -> _bm.Union[str, int, _bm.LoggingLevel]:
        """What max level of logging is being used"""

        return self._level2
    
    @level2.setter
    def level2(self, value):
        raise AttributeError('Level2 property cannot be changed')

    @property
    def enabled(self) -> bool:
        """Whether the logger is enabled"""

        return self._enabled
    
    @enabled.setter
    def enabled(self, value):
        raise AttributeError('Enabled property cannot be changed')

    @property
    def closed(self) -> bool:
        """Whether the logger has been closed"""

        return self._closed
    
    @closed.setter
    def closed(self, value):
        raise AttributeError('Closed property cannot be changed')
    
    def enable(self) -> None:
        """Enable the logger instance"""

        self._enabled = not _bm.enable(self._logger, self.enabled, self.closed)
    
    def disable(self) -> None:
        """Disable the logger instance"""

        self._enabled = bool(_bm.disable(self._logger, self.enabled, self.closed))
    
    def close(self) -> None:
        """Close the logger instance"""
        
        self._disabled = True
        self._closed   = not _bm.close(self._logger, self.closed)

    def __init__(self, 
                 module: str='ALL', 
                 level: _bm.Union[str, int, _bm.LoggingLevel]='ALL',
                 level2: _bm.Union[str, int, _bm.LoggingLevel]='ALL'
                 ) -> None:
        if type(level) is str: level = level.upper()
        if type(level2) is str: level2 = level2.upper()
        
        if type(module) is not str:
            raise TypeError('Module must be a valid \'str\' instance')
        elif module not in ('', 'ALL', 'MAIN', 'REQUESTS', 'SYS'):
            raise ValueError('Unknown module \'{}\''.format(module))
        else:
            self._module: str = module.upper()

            if module == '' or module == 'ALL' or module == 'MAIN':
                self._module: str = 'tooltils'
            else:
                self._module: str = 'tooltils.' + module.lower()

        for i in (('level', level), ('level2', level2)):
            if not isinstance(i[1], (str, int, _bm.DEBUG, _bm.INFO, _bm.WARN,
                                     _bm.ERROR, _bm.CRITICAL)):
                raise TypeError(f'{i[0]} must be a valid \'str\', \'int\' or \'logging\' level instance')
            elif i[1] not in ('ALL', 'DEBUG', 'INFO', 'WARN', 'ERROR', 'CRITICAL', 10, 20, 30, 40, 50):
                raise ValueError('Invalid level \'{}\''.format(i[1]))
            else:
                if i[0] == 'level':
                    if level == 'ALL':
                        self._level = _bm.DEBUG
                    else:
                        self._level = level
                else:
                    if level2 == 'ALL':
                        self._level2 = _bm.CRITICAL
                    else:
                        self._level2 = level2

        self._logger  = _bm.create(self._module, self._level, self._level2)
        self._closed  = False
        self._enabled = True

        _bm.basicConfig(format=
                        '[%(asctime)s] [{}/%(levelname)s]: %(message)s'.format(self._module),
                        datefmt='%I:%M:%S')

    def __str__(self) -> str:
        module: str = 'ALL' if not self.module else self.module.upper()
        state:  str = 'on' if self.enabled else 'off'

        return f'<Logger instance: [{state}] -> [{module}]>'

def _getFiles(dir: str) -> list:
    fileList: list = []

    for i in _bm.listdir(location + dir):
        fileList.append(location + ('' if not dir else dir + '/') + i)
        
    return fileList

def _getLines():
    lines:  int = 0
    files: list = _getFiles('') + _getFiles('requests') + _getFiles('sys')

    for i in ('README.md', 'API.md', 'CHANGELOG.md', 'test.py', 'LICENSE', '.DS_Store',
            '__pycache__', '.git'):
        try:
            files.remove(location + i)
        except ValueError:
            continue

    for i in files:
        try:
            with open(i) as _f:
                lines += len(_f.readlines())
        except (IsADirectoryError, UnicodeDecodeError):
            pass
    
    return lines


lines: int = int(_getLines())
"""The amount of lines of code in this tooltils installation"""

del _getFiles, _getLines, _f, _lt, _ld

def _configMethods():
    _f           = open(location + 'data.json', 'r+')
    _bm.openData = _f
    data: dict   = _bm.load(_f)
    _f.            seek(0)
    funcs: dict  = data['cache']['global']['configMethodValues']

    for k, v in data['config'].items():
        for k2, v2 in v.items():
            if type(v2) is str and '$f' in v2:
                try:
                    statement: str = v2.split(' ')[1].split('(')
                    funcName:  str = statement[0]
                    args:      str = '[' + statement[1][:-1] + ']'

                    if funcName in tuple(funcs.keys()) and funcs[funcName][1] < data[
                        'config']['global']['config']['configMethodCheck']:
                        funcs[funcName] = (funcs[funcName][0], funcs[funcName][1] + 1)
                        _editCache('global', {"configMethodValues": funcs})
                    else:
                        value = _bm.run(funcName, args)

                        funcs.update({funcName: (value, 1)})
                        _editCache('global', {"configMethodValues": funcs})
                except:
                    value = None
            else:
                value = v2

            _bm.actualConfig[k][k2] = value

    return _f
