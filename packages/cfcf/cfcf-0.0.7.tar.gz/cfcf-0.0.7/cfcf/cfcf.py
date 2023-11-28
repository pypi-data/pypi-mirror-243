import os
from pathlib import Path
import shutil
import ulid

COMPLETE_CACHE_FLAG = "__CF2_COMPLETE_CACHE__"
CACHE_DIR_FLAG = "__CF2_CACHE_DIR__"

class CollisionFreeCache:
    def __init__(self, base_path, initializer, *args, **kwargs) -> None:
        self.base_path = base_path
        self.initializer = initializer
        self.initializer_args = args
        self.initializer_kwargs = kwargs
    
    def init(self):
        path = Path(self.base_path) / str(ulid.new())
        os.makedirs(path / CACHE_DIR_FLAG)
        if self.initializer != None:
            wd = os.getcwd()
            os.chdir(path)
            self.initializer(*self.initializer_args, **self.initializer_kwargs)
            os.chdir(wd)
        os.makedirs(path / COMPLETE_CACHE_FLAG)
        return path
    
    def get(self):
        complete_cache = None
        base_path = Path(self.base_path)
        if os.path.exists(base_path):
            for f in sorted(os.listdir(base_path), reverse=True):
                p = base_path / f
                if len(f) == 26 and os.path.isdir(p) and os.path.exists(p / COMPLETE_CACHE_FLAG):
                    complete_cache = p
                    break
        if complete_cache == None:
            complete_cache = self.init()
        return complete_cache.absolute()
    
    def invalidate_all(self):
        base_path = Path(self.base_path)
        for f in sorted(os.listdir(base_path)):
            p = base_path / f
            if len(f) == 26 and os.path.isdir(p) and os.path.exists(p / COMPLETE_CACHE_FLAG):
                os.rmdir(p / COMPLETE_CACHE_FLAG)
    
    def remove_all(self):
        self.invalidate_all()
        base_path = Path(self.base_path)
        for f in sorted(os.listdir(base_path)):
            p = base_path / f
            if len(f) == 26 and os.path.isdir(p) and os.path.exists(p / CACHE_DIR_FLAG):
                shutil.rmtree(p, ignore_errors=True)
