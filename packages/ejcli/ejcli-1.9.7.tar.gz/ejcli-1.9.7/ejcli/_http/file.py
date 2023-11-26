import urllib.parse
from ..error import EJError

class FileBackend:
    @staticmethod
    def detect(url):
        return url.startswith('file:')
    def __new__(self, url, *args0, **kwds0):
        import imp
        path = url[5:].split('#', 1)[0]
        if '?' in path:
            path, args = path.split('?', 1)
            args = dict(urllib.parse.parse_qsl(args))
        else:
            args = {}
        path = urllib.parse.unquote(path)
        cls = args.get('class', 'TheBackend')
        try: file = open(path)
        except IOError:
            raise EJError("File not found.")
        mod = imp.load_module('file:'+path, file, path, ('.py', 'r', 1))
        if not hasattr(mod, cls):
            raise EJError("Backend class not found.")
        return getattr(mod, cls)(url, *args0, **kwds0)
