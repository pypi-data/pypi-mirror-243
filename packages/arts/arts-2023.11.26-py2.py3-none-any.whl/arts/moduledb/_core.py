from pathlib import Path
from tempfile import mkdtemp
from json import loads, dumps
from types import ModuleType
from os.path import abspath
from arts.vtype import CustomDict


root_dir = Path('~/.PyModuleDB').expanduser()
info_file = root_dir / 'info.json'
module_dirs = root_dir / 'module_dirs'

module_dirs.mkdir(parents=True, exist_ok=True)

if info_file.exists():
    info = loads(info_file.read_text('utf8'))
else:
    info = {'modules':{}}
modules = info['modules']


class File(CustomDict):

    path: Path
    level: int
    depth: int
    core: dict

    def __init__(self, path: str|Path, level: int, depth:int):
        # path
        path = str(path)
        assert path[-6:] != '.mfile'
        self.path = path = Path(f"{path}.mfile")
        self.level = level
        self.depth = depth
        # core
        if path.exists():
            # self.core 不要设置 caches 缓存, 否则缓存的 core 不会被自动回收, 会占据大量内存.
            self.core = loads(path.read_text('utf8'))
        else:
            self.core = {}
    
    def save(self):
        self.path.write_text(dumps(self.core, ensure_ascii=False), 'utf8')
    
    additional_actions = save


class Dir:
    
    path: Path
    level: int
    depth: int

    def __init__(self, path: str|Path, level: int, depth:int):
        # path
        path = str(path)
        assert path[-5:] != '.mdir'
        self.path = Path(f"{path}.mdir")
        self.path.mkdir(parents=True, exist_ok=True)
        self.level = level
        self.depth = depth

    def __getitem__(self, name: str):
        path = self.path / name
        level = self.level + 1
        if level == self.depth:
            return File(path=path, level=level, depth=self.depth)
        else:
            return Dir(path=path, level=level, depth=self.depth)


class ModuleDB:

    path: Path
    depth: int

    def __init__(self, module: ModuleType, depth: int=2):
        assert isinstance(module, ModuleType)
        path = modules.get(mpath := abspath(module.__file__))
        if not path:
            path = modules[mpath] = abspath(mkdtemp(dir=module_dirs))
            info_file.write_text(dumps(info, ensure_ascii=False), 'utf8')
        self.path = Path(path)
        self.path.mkdir(exist_ok=True)
        self.depth = depth
    
    def __getitem__(self, name: str) -> Dir|File:
        path = self.path / name
        level = 1
        if level == self.depth:
            return File(path=path, level=level, depth=self.depth)
        else:
            return Dir(path=path, level=level, depth=self.depth)