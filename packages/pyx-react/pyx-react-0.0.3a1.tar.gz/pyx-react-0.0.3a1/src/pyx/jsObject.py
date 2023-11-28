
# A class representing a browser event object
# Should be stored only in the user object
class JSObject:
    def __init__(self, id, user):
        self.user = user
        self.id = id
        self.cache = {}
    
    def request_attr(self, key):
        if key in self.cache:
            ret = self.cache[key]
            if isinstance(ret, dict):
                newObj = JSObject(None, self.user)
                newObj.load(ret)
                self.cache[key] = newObj
                return newObj
            else:
                return ret
        ret = self.user.request({'type': 'jsobj_getattr', 'id': self.id, 'key': key})
        if isinstance(ret, dict) and '__jsobj__' in ret:
            ret = JSObject(ret['__jsobj__'], self.user)
        self.cache[key] = ret
        return ret
        
    def __getattr__(self, key):
        return self.request_attr(key)

    def __getitem__(self, key):
        return self.request_attr(key)
    
    def load(self, data):
        self.cache = data
    
    def empty_cache(self):
        self.cache = {}

    def __del__(self):
        self.user.emit('jsobj_del', {'id': self.id})

class JSObjectWithTracker(JSObject):
    def __init__(self, id, user, tracker_root=None, tracker_dir=[]):
        super().__init__(id, user)
        self.tracker_root = tracker_root
        self.tracker_dir = tracker_dir

    def request_attr(self, key):
        if key in self.cache:
            ret = self.cache[key]
            if isinstance(ret, dict):
                newObj = JSObject(None, self.user)
                newObj.load(ret)
                self.cache[key] = newObj
                return newObj
            else:
                return ret
        ret = self.user.request({'type': 'jsobj_getattr', 'id': self.id, 'key': key})
        if isinstance(ret, dict) and '__jsobj__' in ret:
            ret = JSObjectWithTracker(ret['__jsobj__'], self.user, self.tracker_root, self.tracker_dir + [key])
        self.cache[key] = ret
        if self.tracker_root:
            cache = self.tracker_root
            if hasattr(cache, '__func__'):
                cache = cache.__func__
            if not hasattr(cache, '__preload_props__'):
                cache.__preload_props__ = {}
            current = cache.__preload_props__
            for k in self.tracker_dir:
                if k not in current:
                    current[k] = {}
                current = current[k]
            current[key] = {}
        return ret

