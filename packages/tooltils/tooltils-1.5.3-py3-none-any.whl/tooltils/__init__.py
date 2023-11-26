"""
# tooltils | v1.5.3

A lightweight python utility package built on the standard library

```py
>>> import tooltils
>>> req = tooltils.get('httpbin.org/get')
>>> req
'<GET httpbin.org [200]>
>>> req.url
'https://httpbin.org/get'
>>> req.status_code
'200 OK'
>>> req.headers["User-Agent"]
'Python-tooltils/1.5.3'
```

## API

Read the full documentation within `API.md` included in the project directory
"""


import tooltils.requests as requests
import tooltils.errors as errors
import tooltils.info as info
import tooltils.sys as sys

class _bm:
    from time import time, localtime, gmtime, perf_counter
    from datetime import datetime, timezone, timedelta
    from os.path import abspath, getsize, exists
    from typing import Any, Union
    from io import TextIOWrapper
    from os import mkdir
    
    class EPOCH_seconds:
        pass

    class FileDescriptorOrPath:
        pass

    months: list[str] = [
        'January', 'February', 
        'March', 'April', 
        'May', 'June', 
        'July', 'August', 
        'September', 'October', 
        'November', 'December'
    ]


ANSI_colours: dict[str, int] = {
    "white":  97,
    "cyan":   36,
    "pink":   35,
    "blue":   34,
    "yellow": 33,
    "green":  32,
    "red":    31,
    "gray":   30,
}
"""List of the main colours as ANSI integer codes"""

def length(file: _bm.FileDescriptorOrPath) -> float:
    """Get the length of a wave file in seconds"""

    if type(file) is not str:
        raise TypeError('File must be a valid \'str\' instance')
    if file.split('.')[-1] != 'wav':
        raise ValueError('File is not a WAVE type')
    if not _bm.exists(file):
        raise FileNotFoundError('Could not locate WAVE file')

    try:
        with open(file, encoding='latin-1') as _f:
            _f.seek(28)
            sdata = _f.read(4)
    except IsADirectoryError:
        raise FileNotFoundError('An error occured while opening the WAVE file')

    rate: int = 0
    for i in range(4):
        rate += ord(sdata[i]) * pow(256, i)

    return round((_bm.getsize(file) - 44) * 1000 / rate / 1000, 2)

def style(text: str, 
          colour: str='', 
          fill: bool=False,
          bold: bool=False,
          italic: bool=False,
          crossed: bool=False,
          underline: bool=False,
          double_underline: bool=False,
          flush: bool=True
          ) -> str:
    """Create text in the specified colour and or style"""

    if type(text) is not str:
        raise TypeError('Text must be a valid \'str\' instance')
    if not isinstance(colour, (str, int)):
        raise TypeError('Colour must be a valid \'str\' instance')

    if not colour:
        code = 0
    else:
        code = ANSI_colours.get(colour, colour)

    style: str = ''
    for k, v in {'1': bold, '3': italic, '9': crossed, 
                 '4': underline, '21': double_underline}.items():
        if v:
            style += ';' + k

    if fill:
        code += 10
    if flush:
        sys.call('', shell=True)

    return '\u001b[{0}{1}{2}\u001b[0m'.format(code, style + 'm', text)

def halve(object: _bm.Union[str, list]) -> list:
    """Return the halves of a string or list"""

    if not isinstance(object, (str, list)):
        raise TypeError('Object must be a valid \'str\' or \'list\' instance')

    i: int = len(object)
    if i % 2 == 0:
        return [object[:i // 2], object[i // 2:]]
    else:
        return [object[:(i // 2 + 1)], object[(i // 2 + 1):]]

def cipher(text: str, shift: int) -> str:
    """A simple caeser cipher"""

    if type(text) is not str:
        raise TypeError('Text must be a valid \'str\' instance')
    elif len(text) > 1:
        raise ValueError('Invalid text')
    if type(shift) is not int:
        raise TypeError('Shift must be a valid \'int\' instance')
    elif shift == 0:
        raise ValueError('Shift must not be 0')

    for i in text:
        start: int = 65 if i.isupper() else 97
        text += chr((ord(i) + shift - (start)) % 26 + (start))

    return halve(text)[1]

def mstrip(text: str,
           values: dict
           ) -> str:
    """Change some text from a dictionary pair of values"""

    if type(text) is not str:
        raise TypeError('Text must be a valid \'str\' instance')
    if type(values) is not dict:
        raise TypeError('Values must be a valid \'dict\' instance ')
    
    for k, v in values.items():
        text = text.replace(k, v)
    
    return text

def date(epoch: _bm.EPOCH_seconds=..., 
         timezone: str='local', 
         format: str='standard'
         ) -> str:
    """Convert epoch to a readable date"""

    if not isinstance(epoch, (int, float)) and epoch != ...:
        raise TypeError('Epoch must be a valid \'int\' or \'float\' instance')
    if type(timezone) is not str:
        raise TypeError('Timezone must be a valid \'str\' instance')
    if type(format) is not str:
        raise TypeError('Format must be a valid \'str\' instance')

    try:
        if epoch == ...:
            epoch = _bm.time()

        tz = timezone
        if tz.lower() == 'local':
            sdate = _bm.localtime(epoch)
        elif tz.lower() == 'gm' or '00:00' in tz.lower():
            sdate = _bm.gmtime(epoch)
        elif tz.startswith('+') or tz.startswith('-'):
            timezone = _bm.timezone(_bm.timedelta(
                       hours=int(tz[:3]), 
                       minutes=int(tz[4:])))
            sdate    = _bm.datetime.fromtimestamp(epoch, 
                       tz=timezone).timetuple()
        else:
            raise ValueError('Invalid timezone')
    except (ValueError, IndexError):
        raise TypeError('Timezone not found')
    except OverflowError:
        raise OverflowError('Epoch timestamp too large')

    def fv(*values) -> tuple:
        return [str(i) if i > 9 else f'0{i}' for i in values]

    if format == 'standard':
        return '{}/{}/{} {}:{}:{}'.format(sdate.tm_year,
               *fv(sdate.tm_mon, sdate.tm_mday, sdate.tm_hour,
               sdate.tm_min, sdate.tm_sec))

    elif format == 'fancy':
        hour: int = sdate.tm_hour % 12 if sdate.tm_hour % 12 != 0 else 12
        end: list = ['th', 'st', 'nd', 'rd', 'th', 'th', 'th', 'th', 'th', 'th'
                     ][int(str(sdate.tm_mday)[-1])]
        if sdate.tm_mday in [11, 12, 13]:
            end: str = 'th'

        return '{}:{} {} on the {}{} of {}, {}'.format(hour, *fv(sdate.tm_min), 
               'PM' if sdate.tm_hour >= 12 else 'AM', sdate.tm_mday, end, 
               _bm.months[sdate.tm_mon - 1], sdate.tm_year)
    else:
        raise TypeError('Format ({}) not found'.format(format))

def epoch(date: str) -> _bm.Union[int, float]:
    """Get epoch from a formatted date (`strftime` etc.)"""

    if type(date) is not str:
        raise TypeError('Date must be a valid \'str\' instance')

    if '/' in date:
        splitDate: list = str(date).split(' ')
    elif '-' in date:
        splitDate: list = str(date).replace('-', '/').split(' ')
    else:
        try:
            # Remove '1st' to avoid stripping Augu[st]
            sdate: list = mstrip(date, 
                          {':': ' ', ' on the': '', 
                           ' of': '', ',': '',
                           'th': '', '1st': '',
                           'nd': '', 'rd': ''}).split(' ')
            hours, minutes, meridan, days, month, year = sdate

            if '1st' in date:
                days = '1'
            if meridan == 'PM':
                hours = str(int(hours) + 12)

            splitDate: list = [year + '/' + str(int(_bm.months.index(month)) + 1)
                               + '/' + days, hours + ':' + minutes + ':00']
        except IndexError:
            raise TypeError('Invalid date argument')

    try:
        sdate = _bm.datetime(*[int(i) for i in splitDate[0].split(
                             '/') + splitDate[1].split(':')])
    except IndexError:
        raise TypeError('Invalid date argument')

    days: int = _bm.datetime(sdate.year, sdate.month, 
                             sdate.day, sdate.hour,
                             sdate.minute, sdate.second).toordinal(
                             ) - _bm.datetime(1970, 1, 1).toordinal() - 1
    # Add 13 hours because of obscure glitch
    hours = days * 24 + sdate.hour + 13
    minutes = hours * 60 + sdate.minute
    epoch = minutes * 60 + sdate.second
    
    return epoch

def squeeze(array: _bm.Union[list, tuple, set, dict],
            item: _bm.Union[_bm.Any, None]=None
            ) -> _bm.Union[list, tuple, set, dict]:
    """Remove empty or the specified item(s) from an array"""
    
    if not isinstance(array, (list, tuple, set, dict)):
        raise TypeError('Array must be a valid iterable container')

    op = type(array)
    if op is not dict:
        array = list(array)

    if item is None:
        if op is dict:
            for i in tuple(array.keys()):
                if not array[i]:
                    array.pop(i)
        
            return array
        else:
            return op(filter(None, array))
    else:
        if op is dict:
            for i in tuple(array.keys()):
                if array[i] == item:
                    array.pop(i)
        else:
            for i, it in enumerate(array):
                if it == item:
                    array.pop(i)

        return op(array)

def reverseDictSearch(array: dict, value: _bm.Any) -> _bm.Any:
    """Find the unknown key(s) of a value in a dictionary"""

    if type(array) is not dict:
        raise TypeError('Array must be a valid dictionary instance')

    # Create an isolated dict inside of the list to avoid
    # duplicate values getting merged/deleted
    swappedDict: list = [{v: k} for (k, v) in array.items()]
    results:     list = []

    for i in range(len(swappedDict)):
        try:
            results.append(swappedDict[i][value])
        except KeyError:
            continue
    else:
        if results == []:
            raise IndexError('There was no key matching the specified value')
        else:
            return results

def getArrayValues(array: _bm.Union[list, tuple, dict]) -> tuple:
    """Recursively obtain all of the values of any keys or items within an array"""

    if not isinstance(array, (list, tuple, dict)):
        raise TypeError('Array must be a valid \'list\', \'tuple\' or \'dict\' instance')

    values: list = []

    if isinstance(array, dict):
        items: list = [i[1] for i in array.items()]
    else:
        items: list = list(array)

    for i in items:
        if isinstance(i, dict):
            for ii in getArrayValues(i):
                values.append(ii) 
        elif isinstance(i, (list, tuple)):
            for ii in i:
                if isinstance(ii, (dict, list, tuple)):
                    for iii in getArrayValues(ii):
                        values.append(iii)
                else:
                    values.append(ii)
        else:
            values.append(i)

    return tuple(values)

def timeTest(method, method2, params: dict={}, params2: dict={}, 
             accuracy: int=10) -> tuple[float]:
    """Run two different methods x amount of times, sum then divide to estimate accurate run-time"""

    avg1: list = []
    avg2: list = []

    if type(accuracy) is not int:
        raise TypeError('Accuracy must be a valid \'int\' instance')
    elif accuracy < 1:
        raise ValueError('Accuracy must be 1 or bigger')
    if not hasattr(method, '__call__') or not hasattr(method2, '__call__'):
        raise TypeError('Methods must be a callable instance')
    if type(params) is not dict or type(params2) is not dict:
        raise TypeError('Params and params2 must be a valid \'dict\' instance')

    for i in range(accuracy):
        start = _bm.perf_counter()
        method(**params)
        one = _bm.perf_counter() - start
        start2 = _bm.perf_counter()
        method2(**params2)
        two = _bm.perf_counter() - start2

        avg1.append(one)
        avg2.append(two)

    one: float = sum(avg1) / accuracy
    two: float = sum(avg2) / accuracy

    return (one, two)

def varName(**vars: dict) -> _bm.Union[str, list[str]]:
    """Get the namespace name of one or more variables"""

    names: list = [x for x in vars]

    if len(names) == 1:
        return names[0]
    else:
        return names

class interpereter():
    """Custom top-level Python interpereter to add niche features from other languages"""

    def _getIndent(self, line: str) -> str:
        return ''.join([' ' for i in range(len(line) - len(line.lstrip()))])

    def _convertTernary(self, line: str) -> _bm.Union[str, None]:
        statement: list = line.split('=')

        try:
            condition: str = statement[1].split('?')[0][1:-1]
            values:   list = statement[1].split('?')[1].split(':')

            return f'{statement[0][:-1]} = {values[0].strip()} if {condition} else {values[1].strip().replace('\n', '')}\n'
        except Exception as error:
            raise error

    def _convertComment(self, line: str) -> _bm.Union[str, None]:
        return self._getIndent(line) + '#' + line.lstrip()[2:]

    def read(self) -> str:
        """Read the output file and return the content as a string"""

        if ''.join(self._interpereted)[-1:] == '\n':
            return ''.join(self._interpereted)[:-1]
        else:
            return ''.join(self._interpereted)
    
    def readlines(self) -> list:
        """Read the output file and return the content as a list containing strings split at every newline"""

        return self._interpereted

    def __init__(self, 
                 file: str,
                 output: str='%(name)s.interpereted.py',
                 override: bool=False):
        if type(file) is not str:
            raise TypeError('File must be a valid \'str\' instance')
        if not _bm.exists(file):
            raise FileNotFoundError('Could not locate Python file')
        if type(output) is not str:
            raise TypeError('Output must be a valid \'str\' instance')

        self.file: str = file
        if '.' in file:
            file: str = '.'.join(file.split('.')[0:-1])
        else:
            file: str = file

        self.output:         str = output % {"name": file}
        self.override:      bool = bool(override)
        self._interpereted: list = []

        if not self.override and _bm.exists(self.output):
            raise FileExistsError('Output file already present')

        try:
            with open(self.file) as _f:
                _content = _f.readlines()
        except IsADirectoryError:
            raise FileNotFoundError('There was a problem locating the file')
        
        for line in _content:
            if line.lstrip()[:2] == '//':
                self._interpereted.append(self._convertComment(line))
            elif line.lstrip()[0] != '#' and line.lstrip()[:2] != '//' and \
                 len(line.split('=')) != 1 and len(line.split('=')[1].split('?')) != 1:
                self._interpereted.append(self._convertTernary(line))
            else:
                self._interpereted.append(line)

        with open(self.output, 'a+') as _f:
            _f.truncate(0)
            _f.writelines(self._interpereted)
        
        self.full_output: str = _bm.abspath(self.output)

    def __str__(self):
        return '<Interpereter instance [{}]>'.format(self.file)
