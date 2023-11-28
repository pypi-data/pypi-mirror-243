import os
from pathlib import Path
import shutil
import json
from .cfcf import CollisionFreeCache

__version__ = '0.0.7'

def get_dir(cache_dir, init_func, *args, **kwargs):
    safe_cache_dir = str(cache_dir).lstrip('/').replace('.', '_.').replace(':', '').replace('\\', '').replace('//', '_/_/')
    return cfcf.CollisionFreeCache(safe_cache_dir, init_func, *args, **kwargs).get()

def _init_file(filename, init_func, *args, **kwargs):
    file_path = init_func(*args, **kwargs)
    if file_path is None:
        return
    if not os.path.exists(filename) or not os.path.samefile(filename, file_path):
        shutil.move(file_path, filename)

def get_file(cache_file, init_func, *args, **kwargs):
    filename = Path(cache_file).name
    args = (filename, init_func) + args
    return get_dir(cache_file, _init_file, *args, **kwargs) / filename

def _init_object(filename, init_func, *args, **kwargs):
    obj = init_func(*args, **kwargs)
    with open(filename, 'w', encoding='UTF-8') as f:
        json.dump(obj, f)

def get_object(cache_name, init_func, *args, **kwargs):
    filename = Path(cache_name).name
    args = (filename, init_func) + args
    with open(get_file(cache_name, _init_object, *args, **kwargs), 'r') as f:
        return json.load(f)

def copy(src, dst=None):
    src = Path(src)
    if dst is None:
        dst = src.name
    if os.path.isdir(dst):
        dst = Path(dst) / src.name
    shutil.copy(src, dst)
    return dst
