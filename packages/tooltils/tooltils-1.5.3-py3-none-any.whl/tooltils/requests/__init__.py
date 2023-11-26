"""Internet requesting access methods"""


class _bm:
    from ssl import (SSLContext, SSLError, SSLCertVerificationError,
                     create_default_context, get_default_verify_paths, CERT_NONE)
    from socket import gaierror #, socket, AF_INET, SOCK_STREAM 
    from json import JSONDecodeError, loads, dumps
    from urllib.error import URLError, HTTPError
    from http.client import RemoteDisconnected
    from gzip import decompress, BadGzipFile
    from os.path import abspath, exists
    from urllib.parse import urlencode
    from shutil import copyfileobj
    import urllib.request as u

    from ..errors import (ConnectionError, ConnectionTimeoutExpired, NoHttpConnection,
                          StatusCodeError, SSLCertificateFailed)
    from ..info import _loadCache, _loadConfig, _editCache, _deleteCacheKey, version
    from ..sys import getCurrentWifiName
    from ..sys.info import platform
    
    class FileDescriptorOrPath:
        pass
    
    class url_response:
        pass

    class certifs:
        pass

    def propertyTest(value, types: tuple, name: str):
        if value is None:
            return types[0]()
        elif not isinstance(value, types):
            raise TypeError(name + ' must be a valid \'' + value.__name__ + '\' instance')
        else:
            return value

import tooltils.requests.http as http


status_codes: dict[int, str] = _bm.StatusCodeError.status_codes
"""List of official valid HTTP response status codes (100-511)"""
defaultVerificationMethod    = bool(_bm._loadConfig('requests')['defaultVerificationMethod'])

def where() -> _bm.certifs:
    """Return default certificate file and path locations used by Python"""

    data = _bm.get_default_verify_paths()

    class certifs:
        cafile: str = data.cafile
        """The .pem name of the default certificate file"""
        capath: str = data.capath
        """The location of the default certificate file path"""

    return certifs

def connected() -> bool:
    """Get the connectivity status of the currently connected wifi network"""
    
    return http._bm.connected()

def ctx(verify: bool=True, cert: str=None):
    """Create a custom SSLContext instance"""

    return http._bm.ctx(verify, cert)

def prep_url(url: str, 
             data: dict=None,
             https: bool=True,
             order: bool=False
             ) -> str:
    """Configure a URL making it viable for requests"""

    return http._bm.prep_url(url, data, https, order)

def verifiable() -> bool:
    """Determine whether requests can be verified with a valid ssl 
    certificate on the current connection"""

    caching: bool = bool(_bm._loadConfig('requests')["verifiableCaching"])
    wifiName: str = _bm.getCurrentWifiName()

    if wifiName is None:
        return False
    
    if caching:
        configData: dict = _bm._loadConfig('requests')
        cacheData:  dict = _bm._loadCache('requests')

        if cacheData["verifiableTimesChecked"] >= configData["verifiableCachingCheck"]:
            _bm._editCache('requests', {"verifiableTimesChecked": 0})
            _bm._deleteCacheKey('requests', wifiName, 'verifiableNetworkList')
        else:
            if wifiName in list(cacheData["verifiableNetworkList"].keys()):
                _bm._editCache('requests', 
                {"verifiableTimesChecked": cacheData["verifiableTimesChecked"] + 1})

                return cacheData["verifiableNetworkList"][wifiName]

    try:
        request('httpbin.org/get', 'HEAD').send()

        result: bool = True
    except (_bm.ConnectionError, _bm.SSLCertificateFailed):
        result: bool = False

    if caching:
        _bm._editCache('requests', {wifiName: result}, 'verifiableNetworkList')
        _bm._editCache('requests', {"verifiableTimesChecked": 1})

    return result

class NoRedirects(_bm.u.HTTPRedirectHandler):
    """An opener to prevent redirects in urllib requests"""

    def redirect_request(self, req, fp, code, msg, headers, newurl) -> None:
        return None

class request():
    """Prepare and send a http[s] request"""

    def _setVariables(self, url: str, method: str, auth: tuple, 
                      data: dict, headers: dict, cookies: dict, 
                      cert: str, file_name: str, timeout: int, 
                      encoding: str, mask: bool, agent: str, 
                      verify: bool, redirects: bool):
        self.redirects: bool = bool(redirects)
        self.verified:  bool = bool(verify)
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

        self.url:    str = prep_url(url, self.data)
        self._url:   str = self.url.replace('https://', '').replace('http://', '').split('/')
        self.port:   int = 443
        self.https: bool = True
    
    def _prepare(self):
        _headers: dict = {"Accept": "*/*"}
        _headers.update(self.headers)
        self.headers: dict = _headers
        _headers:     dict = {}
        self.headers.update({"User-Agent": self.agent, "Accept-Encoding": "gzip, deflate"})

        for i in list(self.headers.keys()):
            _headers.update({str(i): str(self.headers[i])})

        for i in list(self.cookies.keys()):
            _headers.update('Cookie', f'{str(i)}={str(self.cookies[i])}')
        
        if self.method == 'POST' or self.method == 'PUT':
            _headers.update({"Content-Length": str(len(self.data)),
                             "Accept": "application/json"})
        
        self.headers: dict = _headers
        self._req          = _bm.u.Request(self.url, self.headers, method=self._method)
    
    def send(self) -> _bm.url_response:
        """Send the request"""

        if self.sent:
            raise _bm.ConnectionError('The request has already been sent')

        _data:    dict = self.data
        _encoding: str = self.encoding
        _openers: list = []
        error          = None
        
        if self.method == 'POST' or self.method == 'PUT':
            _data: dict = _bm.dumps(_data).encode()
        
        if self.auth:
            man = _bm.u.HTTPPasswordMgrWithDefaultRealm()
            man.add_password(None, self.url, self.auth[0], self.auth[1])
            _openers.append(_bm.u.HTTPBasicAuthHandler(man))

        if self.redirects:
            _openers.append(NoRedirects)

        if _openers != []:
            _bm.u.install_opener(_bm.u.build_opener(*_openers))

        try:
            rdata = _bm.u.urlopen(self._req, _data, timeout=self.timeout,
                                  context=ctx(self.verified, self.cert))
        except _bm.RemoteDisconnected:
            error = _bm.ConnectionError('The server ended the connection without a response')
        except _bm.SSLCertVerificationError:
            error = _bm.SSLCertificateFailed()
        except _bm.HTTPError as err:
            if err.code not in list(_bm.StatusCodeError.status_codes.keys()):
                error = _bm.StatusCodeError(reason=f'{err.code} - Unofficial http status code')
            else:
                error = _bm.StatusCodeError(err.code)
        except _bm.URLError as err:
            if '[Errno 8]' in str(err):
                if connected():
                    error = _bm.StatusCodeError(404)
                else:
                    error = _bm.NoHttpConnection()
            elif 'ssl' in str(err):
                error = _bm.SSLCertificateFailed()
        except _bm.gaierror:
            if connected():
                error = _bm.StatusCodeError(404)
            else:
                error = _bm.NoHttpConnection()
        except TimeoutError:
            error = _bm.ConnectionTimeoutExpired('The request connection operation timed out')
        except ValueError:
            error = ValueError('Invalid URL \'' + request.url + '\'')

        _bm.u.install_opener(None)
        self.sent: bool = True

        if error:
            raise error

        self.rdata            = rdata
        self.code:        int = rdata.getcode()
        self.reason:      str = status_codes[self.code]
        self.status_code: str = f'{self.code} {self.reason}'
        self.headers:    dict = dict(self.headers)

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
                 verify: bool=defaultVerificationMethod,
                 redirects: bool=True):
        self._setVariables(url, method, auth, data, headers, cookies, 
                           cert, file_name, timeout, encoding, mask, 
                           agent, verify, redirects)
        
        self._prepare()
        
    def __str__(self):
        if self.sent:
            code: str = '[' + str(self.code) + ']'
        else:
            code: str = '[Unsent]'

        return '<{} {} {}>'.format(self.method, self.url.split('/')[2], code)

    def read(self):
        """Read the request file and return the raw data"""

        text: str = self.rdata.read()
        self.rdata.seek(0)

        return text

    def readlines(self) -> list:
        """Read the request file and return the data as a list split at every newline"""

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
        verify: bool=defaultVerificationMethod,
        redirects: bool=True
        ) -> _bm.url_response:
    """Send a GET request"""

    return request(url, 'GET', auth, data, 
                   headers, cookies, cert, 
                   None, timeout, encoding, 
                   mask, agent, verify, redirects).send()

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
         verify: bool=defaultVerificationMethod,
         redirects: bool=True
         ) -> _bm.url_response:
    """Send a POST request"""

    return request(url, 'POST', auth, data, 
                   headers, cookies, cert, 
                   None, timeout, encoding, 
                   mask, agent, verify, redirects).send()

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
             verify: bool=defaultVerificationMethod,
             redirects: bool=True
             ) -> _bm.url_response:
    """Download a file onto the disk"""

    return request(url, 'DOWNLOAD', auth, data, 
                   headers, cookies, cert, 
                   file_name, timeout, encoding, 
                   mask, agent, verify, redirects
                   ).send()

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
         verify: bool=defaultVerificationMethod,
         redirects: bool=True
        ) -> _bm.url_response:
    """Send a HEAD request"""

    return request(url, 'HEAD', auth, data, 
                   headers, cookies, cert, 
                   None, timeout, encoding, 
                   mask, agent, verify, redirects
                   ).send()

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
        verify: bool=defaultVerificationMethod,
        redirects: bool=True
        ) -> _bm.url_response:
    """Send a PUT request"""

    return request(url, 'PUT', auth, data, 
                   headers, cookies, cert, 
                   None, timeout, encoding, 
                   mask, agent, verify, redirects
                   ).send()

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
          verify: bool=defaultVerificationMethod,
          redirects: bool=True
          ) -> _bm.url_response:
    """Send a PATCH request"""

    return request(url, 'PATCH', auth, data, 
                   headers, cookies, cert, 
                   None, timeout, encoding, 
                   mask, agent, verify, redirects
                   ).send()

def delete(url: str, 
           auth: tuple=None,
           data: dict=None,
           headers: dict=None,
           cert: _bm.FileDescriptorOrPath=None,
           cookies: dict=None,
           timeout: int=15, 
           encoding: str='utf-8',
           mask: bool=False,
           verify: bool=defaultVerificationMethod,
           agent: str=None,
           redirects: bool=True
           ) -> _bm.url_response:
    """Send a DELETE request"""
 
    return request(url, 'DELETE', auth, data, 
                   headers, cookies, cert, 
                   None, timeout, encoding, 
                   mask, agent, verify, redirects
                   ).send()
