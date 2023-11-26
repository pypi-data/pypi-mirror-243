"""System specific methods and information"""


class _bm:
    from subprocess import run, CalledProcessError, TimeoutExpired, DEVNULL
    from typing import NoReturn, Union
    from sys import exit
    
    from ..errors import (ShellCodeError, ShellTimeoutExpired,
                          ShellCommandError, ShellCommandNotFound,
                          ShellCommandPermissionError)
    
    class shell_response:
        pass

import tooltils.sys.info as info


def exit(details: str='', code: int=0) -> _bm.NoReturn:
    """Exit the current thread with details"""

    if type(code) is not int:
        raise TypeError('Exit code must be a valid integer instance')
    if type(details) is not str:
        raise TypeError('Details must be a valid string instance')

    if details == '':
        print('', end='')
    else:
        print(details)

    _bm.exit(code)

def clear() -> None:
    """OS independent terminal clearing"""

    if info.platform == 'Windows':
        _bm.run(['cls'])
    elif info.platform == 'MacOS' or info.platform == 'Linux':
        _bm.run(['clear'])

class system():
    """Call a system program and return some information"""

    def __init__(self, 
                 cmds: _bm.Union[str, list], 
                 shell: bool=False,
                 timeout: int=10, 
                 check: bool=False,
                 capture: bool=True,
                 print: bool=True):
        error = None

        if not isinstance(cmds, (str, list)):
            raise TypeError('Cmds must be a valid \'str\' or \'list\' instance')
        if type(timeout) is not int:
            raise TypeError('Timeout must be a valid \'int\' instance')
        elif timeout > 999 or timeout < 1:
            raise ValueError('Timeout cannot be smaller than 1 or bigger than 999 seconds')
        if print:
            stdout = None
        else:
            capture = False
            stdout = _bm.DEVNULL

        try:
            self.rdata = _bm.run(args=cmds, shell=bool(shell), check=bool(check), 
                                 capture_output=bool(capture), timeout=timeout,
                                 stdout=stdout)
        except _bm.CalledProcessError as err:
            error = _bm.ShellCodeError(err.returncode)
        except _bm.TimeoutExpired:
            error = _bm.ShellTimeoutExpired('Shell command timeout reached and the process expired')
        except FileNotFoundError:
            error = _bm.ShellCommandNotFound('Binary not found in program files')
        except PermissionError:
            error = _bm.ShellCommandPermissionError('Denied access to \'{}\''.format(
                                                    ' '.join(cmds) if type(cmds) is list else cmds))
        except OSError:
            error = _bm.ShellCommandError('An unknown error occured')
        
        if error:
            raise error
        
        self.cmds: _bm.Union[list, str] = cmds
        self.shell:                bool = bool(shell)
        self.timeout:               int = timeout
        self.check:                bool = bool(check)
        self.capture:              bool = bool(capture)
        self.print:                bool = bool(print)
        self.code:                  int = self.rdata.returncode
        self.raw:                 bytes = b''
        self.text:                  str = ''
        self.list_text:       list[str] = []
        self.clean_list_text: list[str] = []

        if capture:
            self.raw:                 bytes = self.rdata.stdout
            self.text:                  str = self.raw.decode()
            self.list_text:       list[str] = self.text.splitlines()
            self.clean_list_text: list[str] = list(filter(None, self.list_text))

    def __str__(self) -> str:
        return f'<System instance [{hex(id(self))}]>'

def check(cmds: _bm.Union[str, list], 
          shell: bool=False, 
          timeout: int=10,
          check: bool=False,
          clean: bool=False,
          listify: bool=True,
          raw: bool=False,
          print: bool=True
          ) -> _bm.Union[str, bytes, list[str]]:
    """Call a system program and return the output"""

    data = system(cmds, shell, timeout, check, print=print)

    if raw:
        return data.raw
    else:
        if listify:
            if clean:
                return data.clean_list_text
            else:
                return data.list_text
        else:
            return data.text

def call(cmds: _bm.Union[str, list], 
         shell: bool=False, 
         timeout: int=10,
         check: bool=False,
         print: bool=True
         ) -> int:
    """Call a system program and return the exit code"""
    
    return system(cmds, shell, timeout, check, False, print).code

def pID(name: str) -> _bm.Union[int, list[int]]:
    """Get the process ID of an app or binary by name"""

    if type(name) is not str:
        raise TypeError('Name must be a valid \'str\' instance')
    elif len(name) == 0:
        raise ValueError('Invalid name')

    if info.platform.lower() in ('macos', 'linux'):
        cname: str = '[' + name[0] + ']' + '' if len(name) == 1 else name[1:]
        pID:  list = [int(i) for i in check(f'ps -ax | awk \'/{cname}/' + '{print $1}\'', True)]

        for i in pID:
            if check(['ps', str(i)])[0].split('/')[-1].lower() == name.lower():
                pID: int = i
                break

    elif info.platform.lower() == 'windows':
        procs: list = check('tasklist', clean=True)
        found: bool = False
        pID:   list = []

        for i in procs:
            if name in i:
                for x in list(filter(None, i.split(' '))):
                    if found:
                        found: bool = False
                        pID.append(int(x))
                        break
                    
                    if '.' in x:
                        for e in ['bat', 'bin', 'cmd', 'com', 'cpl', 'exe', 'gadget', 
                                  'inf1', 'ins', 'inx', 'isu', 'job', 'jse', 'lnk', 
                                  'msc', 'msi', 'msp', 'mst', 'paf', 'pif', 'ps1', 
                                  'reg', 'rgs', 'scr', 'sct', 'shb', 'shs', 'u3p', 
                                  'vb', 'vbe', 'vbs', 'vbscript', 'ws', 'wsf', 'wsh']:
                            if x.split('.')[-1] == e:
                                found: bool = True

    else:
        pID = None
    
    if pID == []:
        pID = None

    return pID

def getCurrentWifiName() -> _bm.Union[str, None]:
    """Get the currently connected wifi name"""

    if info.platform.lower() == 'macos':
        wifiName = check(['/System/Library/PrivateFrameworks/Apple80211.' +
                          'framework/Versions/Current/Resources/airport', '-I'])
            
        if 'AirPort: Off' in wifiName[0]:
            return None
        else:
            return wifiName[12].split('SSID: ')[1]

    elif info.platform.lower() == 'windows':
        return list(filter(None, check('wmic nic get NetConnectionID')))[-1].strip()

    elif info.platform.lower() == 'linux':
        return check(['iwgetid', '--raw'], listify=False)

    else:
        return None
