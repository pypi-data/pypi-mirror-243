"""
Internet requesting access methods - http.client version (alpha)

A slightly different version, extending the functionality of the `urllib`
implentation with features similar to the `http` module of Python.

By default this module is slightly faster, but can see up to a 2x speed increase
when the `https` parameter is passed as False. Though this is bad practice for the average user.
"""


class _bm:
    from ssl import (create_default_context, get_default_verify_paths, SSLError, 
                     SSLCertVerificationError, CERT_NONE)
    from http.client import (HTTPSConnection, HTTPConnection, InvalidURL, 
                             RemoteDisconnected)
    from json import dumps, loads, JSONDecodeError
    from gzip import decompress, BadGzipFile
    from socket import create_connection
    from urllib.parse import urlencode
    from shutil import copyfileobj
    from base64 import b64encode
    from socket import gaierror
    from os.path import exists

    from ..errors import (ConnectionError, ConnectionTimeoutExpired, NoHttpConnection,
                          StatusCodeError, SSLCertificateFailed)
    from ..info import _loadCache, _loadConfig, _editCache, _deleteCacheKey, version
    from ..sys import getCurrentWifiName
    from ..sys.info import platform

    class FileDescriptorOrPath:
        pass
    
    class url_response:
        pass

    class HTTP_Port:
        pass

    def propertyTest(value, types: tuple, name: str):
        if value is None:
            return types[0]()
        elif not isinstance(value, types):
            raise TypeError(name + ' must be a valid \'' + types[0].__name__ + '\' instance')
        else:
            return value

    def prep_url(url: str, 
                 data: dict=None,
                 https: bool=True,
                 order: bool=False
                 ) -> str:

        if data is None:
            data = {}
        elif type(data) is not dict:
            raise TypeError('Data must be a valid dictionary instance')

        try:
            if url[-1] == '/':
                url = url[:-1]

            st = url.strip().startswith
        except AttributeError:
            raise TypeError('URL must be a valid \'str\' instance')
        except IndexError:
            raise ValueError('URL must contain a valid http link')

        if data != {}:
            url += '?' + _bm.urlencode(data, doseq=order, safe='/')
        if url[0] == '/':
            raise ValueError('URL must be a http type instance, not a file path')
        elif url.startswith('file:///'):
            raise ValueError('URL must be a http type instance, not a file path')
        elif not st('https://') and not st('http://'):
            if https:
                url = 'https://' + url
            else:
                url = 'http://' + url
        
        return url

    def ctx(verify: bool=True, cert: str=None):
        try:
            if type(cert) is not str and (
                cert is not None and not cert is type(tuple)):
                raise TypeError('Certificate must be a valid file path')
            elif cert is None:
                cert: str = _bm.get_default_verify_paths().cafile

            if not verify:
                cert = None

            ctx = _bm.create_default_context(cafile=cert)
            ctx.set_alpn_protocols(['https/1.1'])
        except (FileNotFoundError, IsADirectoryError, _bm.SSLError):
            raise FileNotFoundError('Not a valid certificate file path')
        
        if not verify:         
            ctx.check_hostname = False
            ctx.verify_mode    = _bm.CERT_NONE
            ctx.                 set_ciphers('RSA')
        
        return ctx
    
    def connected() -> bool:
        caching: bool = bool(_bm._loadConfig('requests')["connectedCaching"])
        wifiName: str = _bm.getCurrentWifiName()
        result:  bool = True

        if wifiName is None:
            return False

        if caching:
            configData: dict = _bm._loadConfig('requests')
            cacheData:  dict = _bm._loadCache('requests')

            if cacheData["connectedTimesChecked"] >= configData["connectedCachingCheck"]:
                _bm._editCache('requests', {"connectedTimesChecked": 0})
                _bm._deleteCacheKey('requests', wifiName, 'connectedNetworkList')
            else:
                if wifiName in list(cacheData["connectedNetworkList"].keys()):
                    _bm._editCache('requests', 
                    {"connectedTimesChecked": cacheData["connectedTimesChecked"] + 1})

                    return cacheData["connectedNetworkList"][wifiName]

        try:
            # have fallback method incase create_connection() doesn't work
            # conn = _bm.socket(_bm.AF_INET, _bm.SOCK_STREAM)
            # conn.settimeout(3)
            # conn.connect(('3.227.133.255', 80))
            # conn.close()
            _bm.create_connection(('3.227.133.255', 80), 3).close()
        except (TimeoutError, OSError):
            result: bool = False

        if caching:
            _bm._editCache('requests', {wifiName: result}, 'connectedNetworkList')
            _bm._editCache('requests', {"connectedTimesChecked": 1})

        return result


defaultHttpVerificationMethod = bool(_bm._loadConfig('requests')['defaultHttpVerificationMethod'])

class request():
    """Prepare and send a http[s] request"""

    def _setVariables(self, url: str, method: str, auth: tuple, 
                      data: dict, headers: dict, cookies: dict, 
                      cert: str, file_name: str, timeout: int, 
                      encoding: str, mask: bool, agent: str, 
                      verify: bool, redirects: bool, https: bool,
                      port: int):
        self.redirects: bool = bool(redirects)
        self.verified:  bool = bool(verify)
        self.https:     bool = bool(https)
        self.mask:      bool = bool(mask)
        self.sent:      bool = False
        self.cookies:   dict = _bm.propertyTest(cookies, (dict), 'Cookies')
        self.data:      dict = _bm.propertyTest(data, (dict), 'Data')
        self.headers: dict[str, str] = _bm.propertyTest(headers, (dict), 'Headers')

        if type(method) is str:
            if method.upper() not in ['GET', 'POST', 'PUT', 'DOWNLOAD',
                                      'HEAD', 'PATCH', 'DELETE']:
                raise ValueError('Invalid http method \'{}\''.format(method))
            else:
                if method.upper() == 'DOWNLOAD':
                    self._method: str = 'GET'
                else:
                    self._method: str = method.upper()

                self.method: str = method.upper()
        else:
            raise TypeError('method must be a valid \'str\' instance')

        if cert is None:
            self.cert: str = _bm.get_default_verify_paths().cafile
        else:
            if type(cert) is not str:
                raise TypeError('Certificate must be a valid \'str\' instance')
            elif not _bm.exists(cert) or cert.split('.')[-1] != 'pem':
                raise FileNotFoundError('Invalid certificate file path')
            elif verify:
                self.cert: str = cert
            else:
                self.cert: str = _bm.get_default_verify_paths().cafile
        if auth is None:
            self.auth = None
        elif len(auth) != 2:
            raise ValueError('Invalid authentication details')
        elif type(auth) is not tuple and type(auth) is not list:
            raise TypeError('Authentiction must be a valid \'tuple\' instance')
        else:
            self.auth: tuple = tuple(auth)
        if type(timeout) is not int and type(timeout) is not float:
            raise TypeError('Timeout must be a valid \'int\' instance')
        elif timeout > 999 or timeout < 1:
            raise ValueError('Timeout cannot be bigger than 999 or smaller than 0 seconds')
        else:
            self.timeout: int = int(timeout)
        try:
            if not _bm.exists(file_name):
                self.file_name: str = file_name
            elif not _bm.exists(url.split('/')[-1]):
                self.file_name: str = url.split('/')[-1]
            else:
                raise FileExistsError('Destination file already exists')
        except TypeError:
            if not _bm.exists(url.split('/')[-1]):
                self.file_name: str = url.split('/')[-1]
            else:
                raise FileExistsError('Destination file already exists')
        if agent is None:
            self.agent: str = f'Python-tooltils/{_bm.version}'
        else:
            self.agent: str = str(agent)
        if mask:
            if _bm.platform.lower() == 'windows':
                self.agent: str = 'Mozilla/5.0 (Windows NT 10.0; ' + \
                                  'rv:10.0) Gecko/20100101 Firefox/10.0'
            elif _bm.platform.lower() == 'macos':
                self.agent: str = f'Mozilla/5.0 (Macintosh; Intel Mac OS ' + \
                                  '10.15; rv:10.0) Gecko/20100101 Firefox/10.0'
            else:
                self.agent: str = 'Mozilla/5.0 (X11; Linux x86_64; rv:10.0) ' + \
                                  'Gecko/20100101 Firefox/10.0'
        if type(encoding) is not str:
            raise TypeError('Encoding must be a valid \'str\' instance')
        else:
            self.encoding: str = encoding
        if port is None:
            if self.https:
                self.port: int = 443
            else:
                self.port: int = 80
        elif type(port) is not int:
            raise TypeError('Port must be a valid \'int\' instance')
        else:
            self.port: int = port

        self.url:   str = _bm.prep_url(url, self.data, self.https)
        self._url:  str = self.url.replace('https://', '').replace('http://', '').split('/')
        self._page: str = '/' + '/'.join(self._url[1:])
    
    def _prepare(self):
        _headers:   dict = {"Accept": "*/*"}
        self._data: dict = None
        
        _headers.update(self.headers)
        self.headers: dict = _headers
        _headers:     dict = {}
        self.headers.update({"User-Agent": self.agent, "Accept-Encoding": "gzip, deflate",
                             "Connection": "close", "Content-Type": "application/json;charset=utf-8"})
        
        if self.auth:
            self.headers.update({"Authorization": "Basic {}".format(
                _bm.b64encode(f'{self.auth[0]}:{self.auth[1]}'.encode()).decode("ascii"))})

        for i in list(self.headers.keys()):
            _headers.update({str(i): str(self.headers[i])})

        for i in list(self.cookies.keys()):
            _headers.update('Cookie', f'{str(i)}={str(self.cookies[i])}')
        
        self.headers: dict = _headers

        if self.https:
            self._req = _bm.HTTPSConnection(self._url[0], self.port, timeout=self.timeout, 
                                            context=_bm.ctx(self.verified, self.cert))
        else:
            self._req = _bm.HTTPConnection(self._url[0], self.port, timeout=self.timeout)
    
    def change(self, headers: dict=None, data: dict=None, cookies: dict=None,
               encoding: str='utf-8') -> None:
        """Change indepedent request information globally"""

        if headers:
            headers = _bm.propertyTest(headers, (dict), 'headers')
        if data:
            data = _bm.propertyTest(data, (dict), 'data')
        if cookies:
            cookies = _bm.propertyTest(cookies, (dict), 'cookies')
        
        self.headers: dict = self.headers.update(headers) if headers else self.headers
        self.data:    dict = data if data else self.data
        self.cookies: dict = cookies if cookies else self.cookies
        self.encoding: str = str(encoding) if encoding else self.encoding
    
    def send(self) -> _bm.url_response:
        """Send the request"""

        if self.sent:
            raise _bm.ConnectionError('The request has already been sent')

        _headers: dict = self.headers
        _data:    dict = self.data
        _cookies: dict = self.cookies
        _encoding: str = self.encoding
        error          = None

        for i in list(_cookies.keys()):
            _headers.update('Cookie', f'{str(i)}={str(_cookies[i])}')
        
        if self.method in ('POST', 'PUT'):
            _data: dict = _bm.dumps(_data).encode()
            _headers.update({"Content-Length": str(len(_data))})

        try:
            self._req.request(self._method, self._page, _data, _headers)
            rdata = self._req.getresponse()

            if rdata.status >= 400:
                if rdata.status not in list(_bm.StatusCodeError.status_codes.keys()):
                    raise _bm.StatusCodeError(reason=f'{rdata.status} - Unofficial http status code')
                else:
                    raise _bm.StatusCodeError(rdata.status)

            if self.redirects and rdata.getheader('location') is not None:
                return request(rdata.getheader('location'), self.method, self.auth, 
                               self.data, self.headers, self.cookies, self.cert, 
                               self.file_name, self.timeout, self.encoding, self.mask, 
                               self.agent, self.verified, self.redirects, self.https,
                               self.port).send()
            
        except _bm.RemoteDisconnected:
            error = _bm.ConnectionError('The server ended the connection without a response')
        except _bm.SSLCertVerificationError:
            error = _bm.SSLCertificateFailed()
        except _bm.gaierror:
            if _bm.connected():
                error = _bm.StatusCodeError(404)
            else:
                error = _bm.NoHttpConnection()
        except OSError as err:
            if 'Errno 65' in str(err):
                error =  ValueError('Invalid URL')
        except _bm.InvalidURL as err:
            if 'nonnumeric port' in str(err):
                error = ValueError('You may not include a colon in the URL object (this includes ports)')
            elif 'control characters':
                error = ValueError('Invalid URL (contains non-transmissible characters)')
        
        self.sent: bool = True
        
        if error:
            raise error

        self.rdata            = rdata
        self.encoding:    str = _encoding
        self.code:        int = rdata.status
        self.reason:      str = _bm.StatusCodeError.status_codes[self.code]
        self.status_code: str = f'{self.code} {self.reason}'
        self.headers:    dict = dict(_headers)

        for i in rdata.getheaders():
            self.headers.update({i[0]: i[1]})
        
        if self.method != 'HEAD':
            if self.method != 'FILE':
                text = rdata.read()

                try:
                    text = _bm.decompress(text)
                except _bm.BadGzipFile:
                    pass

                self.text = text.decode(_encoding)
                self.raw  = text
                self.html = None
                self.path = None
            else:
                with open(self.file_name, 'wb+') as _f:
                    _bm.copyfileobj(rdata, _f)

                self.path: str = _bm.abspath(self.file_name)

            try:
                self.json: dict = _bm.loads(self.text)
            except _bm.JSONDecodeError:
                self.json = None

                try:
                    if self.text[0] == '<' or self.text[-1] == '>':
                        self.html: str = self.text
                except IndexError:
                    self.text = None
                    self.html = None
            except AttributeError:
                self.json = None
                self.text = None
                self.raw  = None
                self.html = None
        else:
            self.text = None
            self.raw  = None
            self.html = None
            self.json = None
            self.path = None
        
        return self

    def __init__(self, 
                 url: str,
                 method: str,
                 auth: tuple=None,
                 data: dict=None,
                 headers: dict=None,
                 cookies: dict=None,
                 cert: _bm.FileDescriptorOrPath=None, 
                 file_name: _bm.FileDescriptorOrPath=None,
                 timeout: int=15, 
                 encoding: str='utf-8',
                 mask: bool=False,
                 agent: str=None,
                 verify: bool=True,
                 redirects: bool=True,
                 https: bool=True,
                 port: _bm.HTTP_Port=None):
        self._setVariables(url, method, auth, data, headers, cookies,
                           cert, file_name, timeout, encoding, mask,
                           agent, verify, redirects, https, port)
        
        self._prepare()
        
    def __str__(self):
        if self.sent:
            code: str = '[' + str(self.code) + ']'
        else:
            code: str = '[Unsent]'

        return '<{} {} {}>'.format(self.method, self.url.split('/')[2], code)

    def read(self):
        """Read the file and return the raw request data"""

        text: str = self.rdata.read()
        self.rdata.seek(0)

        return text

    def readlines(self) -> list:
        """Read the file and return the data as a list split at every newline"""

        text: list = self.rdata.read().decode(self.encoding).splitlines()
        self.rdata.seek(0)

        return text

def get(url: str, 
        auth: tuple=None,
        data: dict=None,
        headers: dict=None,
        cookies: dict=None,
        cert: _bm.FileDescriptorOrPath=None, 
        timeout: int=15, 
        encoding: str='utf-8',
        mask: bool=False,
        agent: str=None,
        verify: bool=True,
        redirects: bool=True,
        https: bool=True,
        port: _bm.HTTP_Port=None
        ) -> _bm.url_response:
    """Send a GET request"""

    return request(url, 'GET', auth, data, 
                   headers, cookies, cert, None, 
                   timeout, encoding, mask, agent, 
                   verify, redirects, https, port).send()

def post(url: str, 
         auth: tuple=None,
         data: dict=None,
         headers: dict=None,
         cookies: dict=None,
         cert: _bm.FileDescriptorOrPath=None,
         timeout: int=15, 
         encoding: str='utf-8',
         mask: bool=False,
         agent: str=None,
         verify: bool=True,
         redirects: bool=True,
         https: bool=True,
         port: _bm.HTTP_Port=None
         ) -> _bm.url_response:
    """Send a POST request"""

    return request(url, 'POST', auth, data, 
                   headers, cookies, cert, None, 
                   timeout, encoding, mask, agent, 
                   verify, redirects, https, port).send()

def download(url: str, 
             auth: tuple=None,
             data: dict=None,
             headers: dict=None,
             cookies: dict=None,
             cert: _bm.FileDescriptorOrPath=None,
             file_name: _bm.FileDescriptorOrPath=None,
             timeout: int=15, 
             encoding: str='utf-8',
             mask: bool=False,
             agent: str=None,
             verify: bool=True,
             redirects: bool=True,
             https: bool=True,
             port: _bm.HTTP_Port=None
             ) -> _bm.url_response:
    """Download a file onto the disk"""

    return request(url, 'DOWNLOAD', auth, data, 
                   headers, cookies, cert, file_name, 
                   timeout, encoding, mask, agent, 
                   verify, redirects, https, port).send()

def head(url: str, 
         auth: tuple=None,
         data: dict=None,
         headers: dict=None,
         cookies: dict=None,
         cert: _bm.FileDescriptorOrPath=None, 
         timeout: int=15, 
         encoding: str='utf-8',
         mask: bool=False,
         agent: str=None,
         verify: bool=True,
         redirects: bool=True,
         https: bool=True,
         port: _bm.HTTP_Port=None
         ) -> _bm.url_response:
    """Send a HEAD request"""

    return request(url, 'HEAD', auth, data, 
                   headers, cookies, cert, None, 
                   timeout, encoding, mask, agent, 
                   verify, redirects, https, port).send()

def put(url: str, 
        auth: tuple=None,
        data: dict=None,
        headers: dict=None,
        cookies: dict=None,
        cert: _bm.FileDescriptorOrPath=None, 
        timeout: int=15, 
        encoding: str='utf-8',
        mask: bool=False,
        agent: str=None,
        verify: bool=True,
        redirects: bool=True,
        https: bool=True,
        port: _bm.HTTP_Port=None
        ) -> _bm.url_response:
    """Send a GET request"""

    return request(url, 'PUT', auth, data, 
                   headers, cookies, cert, None, 
                   timeout, encoding, mask, agent, 
                   verify, redirects, https, port).send()

def patch(url: str, 
          auth: tuple=None,
          data: dict=None,
          headers: dict=None,
          cookies: dict=None,
          cert: _bm.FileDescriptorOrPath=None, 
          timeout: int=15, 
          encoding: str='utf-8',
          mask: bool=False,
          agent: str=None,
          verify: bool=True,
          redirects: bool=True,
          https: bool=True,
          port: _bm.HTTP_Port=None
          ) -> _bm.url_response:
    """Send a PATCH request"""

    return request(url, 'PATCH', auth, data, 
                   headers, cookies, cert, None, 
                   timeout, encoding, mask, agent, 
                   verify, redirects, https, port).send()

def delete(url: str, 
           auth: tuple=None,
           data: dict=None,
           headers: dict=None,
           cookies: dict=None,
           cert: _bm.FileDescriptorOrPath=None, 
           timeout: int=15, 
           encoding: str='utf-8',
           mask: bool=False,
           agent: str=None,
           verify: bool=True,
           redirects: bool=True,
           https: bool=True,
           port: _bm.HTTP_Port=None
           ) -> _bm.url_response:
    """Send a DELETE request"""

    return request(url, 'DELETE', auth, data, 
                   headers, cookies, cert, None, 
                   timeout, encoding, mask, agent, 
                   verify, redirects, https, port).send()
