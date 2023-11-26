"""Package specific exceptions"""


class TooltilsError(Exception):
    """Base class for tooltils specific errors"""

    def __init__(self, message:str=''):
        self.message: str = message
    
    def __str__(self):
        if self.message:
            return self.message
        else:
            return 'A Tooltils error occured'

class TooltilsMainError(TooltilsError):
    """Base class for tooltils main module specific errors"""

    def __init__(self, message:str=''):
        self.message: str = message
    
    def __str__(self):
        if self.message:
            return self.message
        else:
            return 'A tooltils main module error occured'

class TooltilsRequestsError(TooltilsError):
    """Base class for tooltils.requests specific errors"""

    def __init__(self, message:str=''):
        self.message: str = message
    
    def __str__(self):
        if self.message:
            return self.message
        else:
            return 'A tooltils.requests error occured'

class TooltilsSysError(TooltilsError):
    """Base class for tooltils.sys specific errors"""

    def __init__(self, message:str=''):
        self.message: str = message
    
    def __str__(self):
        if self.message:
            return self.message
        else:
            return 'A tooltils.sys error occured'

class TooltilsInfoError(TooltilsError):
    """Base class for tooltils.info specific errors"""

    def __init__(self, message:str=''):
        self.message: str = message
    
    def __str__(self):
        if self.message:
            return self.message
        else:
            return 'A tooltils.info error occured'

class SystemCallError(TooltilsSysError):
    """Base class for tooltils.sys.system() specific errors"""

    def __init__(self, message:str=''):
        self.message: str = message
    
    def __str__(self):
        if self.message:
            return self.message
        else:
            return 'A tooltils.sys.system() error occured'

class ShellCodeError(SystemCallError):
    """Shell command returned non-zero exit code"""

    def __init__(self, 
                 code: int=-1, 
                 message: str=''):
        self.code:    int = code
        self.message: str = message
    
    def __str__(self):
        if self.message:
            return self.message
        elif self.code:
            return f'Shell command returned non-zero exit code {self.code}'
        else:
            return 'Shell command returned non-zero exit code'

class ShellTimeoutExpired(SystemCallError):
    """Shell command timed out"""
    
    def __init__(self, message: str=''):
        self.message: str = message
    
    def __str__(self):
        if self.message:
            return self.message
        else:
            return 'Shell command timed out'

class ShellCommandError(SystemCallError):
    """Shell command exited while in process"""

    def __init__(self, message: str=''):
        self.message: str = message
    
    def __str__(self):
        if self.message:
            return self.message
        else:
            return 'Shell command exited while in process'

class ShellCommandNotFound(SystemCallError):
    """Unable to locate shell command or program"""

    def __init__(self, message: str=''):
        self.message: str = message
    
    def __str__(self):
        if self.message:
            return self.message
        else:
            return 'Unable to locate shell command or program'

class ShellCommandPermissionError(SystemCallError):
    """Denied access to system command or program"""

    def __init__(self, message: str=''):
        self.message: str = message
    
    def __str__(self):
        if self.message:
            return self.message
        else:
            return 'Denied access to system command or program'

class RequestError(TooltilsRequestsError):
    """Base class for tooltils.requests.request() specific errors"""

    def __init__(self, message: str=''):
        self.message: str = message
    
    def __str__(self):
        if self.message:
            return self.message
        else:
            return 'A tooltils.requests.request() error occured'

class ConnectionError(RequestError):
    """Connection to URL failed"""

    def __init__(self, message: str=''):
        self.message: str = message
    
    def __str__(self):
        if self.message:
            return self.message
        else:
            return 'Connection to URL failed'

class ConnectionTimeoutExpired(RequestError):
    """Request read timeout expired"""

    def __init__(self, message: str=''):
        self.message: str = message
    
    def __str__(self):
        if self.message:
            return self.message
        else:
            return 'Request read timeout expired'

class StatusCodeError(RequestError):
    """Status code of URL response is not 200"""

    status_codes: dict[int, str] = {
        100: 'Continue',
        101: 'Switching Protocols',
        102: 'Processing',
        103: 'Early Hints',
        200: 'OK',
        201: 'Created',
        202: 'Accepted',
        203: 'Non-Authoritative Information',
        204: 'No Content',
        205: 'Reset Content',
        206: 'Partial Content',
        207: 'Multi-Status',
        208: 'Already Reported',
        226: 'I\'m Used',
        300: 'Multiple Choices',
        301: 'Moved Permanently',
        302: 'Found',
        303: 'See Other',
        304: 'Not Modified',
        305: 'Use Proxy',
        307: 'Temporary Redirect',
        308: 'Permanent Redirect',
        400: 'Bad Request',
        401: 'Unauthorized',
        402: 'Payment Required',
        403: 'Forbidden',
        404: 'Not Found',
        405: 'Method Not Allowed',
        406: 'Not Acceptable',
        407: 'Proxy Authentication Required',
        408: 'Request Timeout',
        409: 'Conflict',
        410: 'Gone',
        411: 'Content-Length Required',
        412: 'Precondition Failed',
        413: 'Request Entity Too Large',
        414: 'Request URI Too Long',
        415: 'Unsupported Media Type',
        416: 'Requested Range Not Satisfiable',
        417: 'Expectation Failed',
        421: 'Misdirected Request',
        422: 'Unprocessable Content',
        423: 'Locked',
        424: 'Failed Dependency',
        425: 'Too Early',
        426: 'Upgrade Required',
        428: 'Precondition Required',
        429: 'Too Many Requests',
        431: 'Request Header Fields Too Large',
        451: 'Unavailable For Legal Reasons',
        500: 'Internal Server Error',
        501: 'Not Implemented',
        502: 'Bad Gateway',
        503: 'Service Unavailable',
        504: 'Gateway Timeout',
        505: 'HTTP Version Not Supported',
        506: 'Variant Also Negotiates',
        507: 'Insufficient Storage',
        508: 'Loop Detected',
        510: 'Not Extended',
        511: 'Network Authorisation Required',
    }
    """List of valid HTTP response status codes (100-511)"""
    
    def __init__(self, 
                 code: int=0, 
                 reason: str=''):
        self.code:   int = code
        self.reason: str = reason

    def __str__(self):
        if self.reason:
            try:
                code = {v: k for (k, v) in self.status_codes.items(
                        )}[self.reason]

                return '{} {}'.format(code, self.reason)
            except KeyError:
                pass
        elif self.code:
            return '{} {}'.format(self.code, self.status_codes[self.code])
        elif self.code and self.reason:
            return '{} {}'.format(self.code, self.reason)
        else:
            return 'The URL response returned an impassable status code'

class SSLCertificateFailed(RequestError):
    """The currently used SSL certificate could not be used to verify requests"""

    def __init__(self, message: str=''):
        self.message: str = message
    
    def __str__(self):
        if self.message:
            return self.message

        return 'The currently used SSL certificate could not be used to verify requests'

class NoHttpConnection(RequestError):
    """No valid wifi connection could be found for the request"""

    def __init__(self, message: str=''):
        self.message: str = message
    
    def __str__(self):
        if self.message:
            return self.message

        return 'No valid wifi connection could be found for the request'
