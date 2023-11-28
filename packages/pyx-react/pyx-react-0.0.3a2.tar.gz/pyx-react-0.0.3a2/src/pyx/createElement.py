
from .hashid import hashID
from PIL import Image
import os

def convert(obj):
    if hasattr(obj, '__render__'):
        return {'__renderable__': hashID(obj)}
    elif isinstance(obj, list):
        return [convert(item) for item in obj]
    elif isinstance(obj, dict):
        return {k: convert(v) for k, v in obj.items()}
    elif isinstance(obj, tuple):
        return tuple(convert(item) for item in obj)
    elif isinstance(obj, set):
        return {convert(item) for item in obj}
    elif hasattr(obj, '__call__'):  # Event Handler
        obj_hash = hashID(obj)
        cache = obj
        if hasattr(obj, '__func__'):
            cache = obj.__func__
        preload_props = {}
        if hasattr(cache, '__preload_props__'):
            preload_props = cache.__preload_props__  
        return {'__callable__': obj_hash, '__preload__': preload_props}
    elif isinstance(obj, Image.Image):
        if not os.path.exists('./public/images'):
            os.makedirs('./public/images')
        with open(f'./public/images/{hashID(obj)}.png', 'wb') as f:
            obj.save(f, format='PNG')
        return "images/" + f"{hashID(obj)}.png"
    else:
        return obj

# TODO: Remove from map when there's no more dependants
# ex) check reference count

def createElement(tag, props, *children):
    return {
        'tag': tag,
        'props': convert(props),
        'children': convert(children)
    }
