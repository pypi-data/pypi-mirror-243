from copy import deepcopy
from collections import deque
from pymysql import connect  # 代码提示
from pymysql.cursors import DictCursor
from json import dumps as jsonDumps


class TRUE:
    def __bool__(self): return True

class FALSE:
    def __bool__(self): return False

uniset = TRUE()
empset = FALSE()
SysEmpty = FALSE()

class OrmIndexError(IndexError):
    def __repr__(self):
        return 'OrmIndexError'

def jsonChinese(data): return jsonDumps(data, ensure_ascii=False)

class ToolPool():
    def __init__(self, mktool, minlen:int=0, maxlen=None):
        self.mktool = mktool
        self.pool = deque([mktool() for i in range(minlen or 0)], maxlen=maxlen)
    
    def put(self, obj):
        obj['cursor'].close()
        self.pool.append(obj)
    
    def get(self, db_name=''):
        try:
            obj = self.pool.popleft()
            conn = obj['conn']
            conn.ping(reconnect=True)
            conn.commit()  # pymysql只有在commit时才会获取数据库的最新状态
            obj['cursor'] = conn.cursor(cursor=DictCursor)
        except:
            obj = self.mktool()
        if db_name and obj['db_name'] != db_name:
            obj['cursor'].execute(f'use {db_name}')
            obj['db_name'] = db_name
        return obj

class ORM():
    def __init__(self, mkconn):
        def _():
            conn:connect = mkconn()
            return dict(
                conn = conn,
                cursor = conn.cursor(cursor=DictCursor),
                db_name = ''
            )
        self.conn_pool = ToolPool(mktool=_, minlen=1, maxlen=1)
        # 当增删改查报错时, conn不再放回连接池, 以避免含有残留数据
    
    def get_dbs(self):
        obj = self.conn_pool.get()
        obj['cursor'].execute("show databases")  # 非本地操作, 需要连接到数据库
        r = list(obj['cursor'].fetchall())
        self.conn_pool.put(obj)
        return r
    
    def get_db_names(self): return [x['Database'] for x in self.get_dbs()]

    def __len__(self): return len(self.get_dbs())

    def __contains__(self, db_name): return db_name in self.get_db_names()

    def __iter__(self):
        yield from self.get_db_names()
    
    def __getitem__(self, key):
        if isinstance(key, str):
            return db_orm(conn_pool=self.conn_pool, db_name=key)
        elif isinstance(key, tuple):
            return [db_orm(conn_pool=self.conn_pool, db_name=x) for x in key]
        elif isinstance(key, slice):
            assert key.start is key.stop is key.step is None
            return [db_orm(conn_pool=self.conn_pool, db_name=x) for x in self.get_db_names()]
        else:
            raise TypeError(key)
    
    def close(self):
        obj = self.conn_pool.get()
        r = obj['conn'].close()  # 关闭后就不必再放回self.conn_pool了
        return r or True

class db_orm():
    def __init__(self, conn_pool:ToolPool, db_name):
        self.conn_pool = conn_pool
        self.db_name = db_name

    def __repr__(self):
        return f'coolmysql.db_orm("{self.db_name}")'
    __str__ = __repr__

    def get_sheet_names(self):
        obj = self.conn_pool.get(self.db_name)
        sql = f'select table_name as TableName from information_schema.tables where table_schema = "{self.db_name}"'
        obj['cursor'].execute(sql)
        r = [x['TableName'] for x in list(obj['cursor'].fetchall())]
        self.conn_pool.put(obj)
        return r

    def __len__(self): return len(self.get_sheet_names())

    def __contains__(self, sheet_name): return sheet_name in self.get_sheet_names()

    def __iter__(self):
        yield from self.get_sheet_names()

    def __getitem__(self, key):
        if isinstance(key, str):
            return sheet_orm(conn_pool=self.conn_pool, db_name=self.db_name, sheet_name=key)
        elif isinstance(key, tuple):
            return [sheet_orm(conn_pool=self.conn_pool, db_name=self.db_name, sheet_name=x) for x in key]
        elif isinstance(key, slice):
            assert key.start is key.stop is key.step is None
            sheets = self.get_sheet_names()
            return [sheet_orm(conn_pool=self.conn_pool, db_name=self.db_name, sheet_name=x) for x in sheets]
        else:
            raise TypeError(key)
        
    def close(self):
        obj = self.conn_pool.get()
        r = obj['conn'].close()
        return r or True

class Factory:
    _variable = True

    def __init__(self, where):
        if where is not empset:
            where = where or uniset
        self.where = where
        self._variable = False

    def __setattr__(self, name, value):
        assert self._variable
        object.__setattr__(self, name, value)
    
    def __bool__(self): return True  # 下面有一个 where or Factory(uniset)

    def __and__(self, obj):
        a = self.where
        b = obj.where
        if a is uniset: return Factory(b)
        if b is uniset: return Factory(a)
        if a and b: return Factory(f"({a}) and ({b})")
        return Factory(empset)

    def __or__(self, obj):
        a = self.where
        b = obj.where
        if a is empset: return Factory(b)
        if b is empset: return Factory(a)
        if a is uniset or b is uniset: return Factory(uniset)
        return Factory(f"({a}) or ({b})")

    def __invert__(self):
        w = self.where
        if w is uniset: return Factory(empset)
        if w is empset: return Factory(uniset)
        return Factory(f"not ({w})")

    def __sub__(self, obj): return self & (~ obj)
    
    def __str__(self):
        w = self.where
        if w is uniset: return ''
        if w is empset: return ' where 1 = 2'
        return f" where {w}"


class Filter():
    _variable = True

    def __init__(self, field):
        self.field = field
        self._variable = False
    
    def __setattr__(self, name, value):
        assert self._variable
        object.__setattr__(self, name, value)

    def __eq__(self, obj):
        if obj is None:
            return Factory(f"{self.field} is null")
        return Factory(f"{self.field} = {jsonChinese(obj)}")

    def __ne__(self, obj):
        if obj is None:
            return Factory(f"{self.field} is not null")
        return Factory(f"{self.field} != {jsonChinese(obj)}")

    def __lt__(self, obj): return Factory(f"{self.field} < {jsonChinese(obj)}")
    def __le__(self, obj): return Factory(f"{self.field} <= {jsonChinese(obj)}")
    def __gt__(self, obj): return Factory(f"{self.field} > {jsonChinese(obj)}")
    def __ge__(self, obj): return Factory(f"{self.field} >= {jsonChinese(obj)}")
    def re(self, string): return Factory(f"{self.field} regexp {jsonChinese(string or '')}")

    def isin(self, *lis):
        if not lis: return Factory(empset)
        if len(lis) == 1: return self == lis[0]
        null = False
        type_item = {str:set(), int:set(), float:set()}
        for i, x in enumerate(lis):
            if x is None:
                null = True
            else:
                type_item[type(x)].add(x)
        sumlis = []
        for lis in type_item.values():
            if len(lis) == 1:
                sumlis.append(f"{self.field} = {jsonChinese(list(lis)[0])}")
            elif len(lis) > 1:
                sumlis.append(f"{self.field} in ({', '.join(jsonChinese(x) for x in lis)})")
        if null:
            sumlis.append(f"{self.field} is null")
        if len(sumlis) == 1:
            return Factory(sumlis[0])
        else:
            return Factory(' or '.join(f"({x})" for x in sumlis))

    def notin(self, *lis):
        if not lis: return Factory(uniset)
        if len(lis) == 1: return self != lis[0]
        null = False
        type_item = {str:set(), int:set(), float:set()}
        for i, x in enumerate(lis):
            if x is None:
                null = True
            else:
                type_item[type(x)].add(x)
        sumlis = []
        for lis in type_item.values():
            if len(lis) == 1:
                sumlis.append(f"{self.field} != {jsonChinese(list(lis)[0])}")
            elif len(lis) > 1:
                sumlis.append(f"{self.field} not in ({', '.join(jsonChinese(x) for x in lis)})")
        if null:
            sumlis.append(f"{self.field} is not null")
            sumlis = sumlis[0] if len(sumlis) == 1 else ' and '.join(f"({x})" for x in sumlis)
        else:
            sumlis = sumlis[0] if len(sumlis) == 1 else ' and '.join(f"({x})" for x in sumlis)
            sumlis = f"({sumlis}) or ({self.field} is null)"
        return Factory(sumlis)

class MakeSlice():
    def __init__(self, func, *vs, **kvs):
        self.func = func
        self.vs = vs
        self.kvs = kvs
    
    def __getitem__(self, key):
        return self.func(key, *self.vs, **self.kvs)

class sheet_orm():
    _variable = True
    _pk = ''

    def __init__(self, conn_pool:ToolPool, db_name:str, sheet_name:str, where=None, columns='*', _sort=None):
        assert columns  # 不能为空
        self.columns = columns  # str型 或 tuple型
        self.conn_pool = conn_pool
        self.db_name = db_name
        self.sheet_name = sheet_name
        self.where = where or Factory(uniset)
        self._sort = deepcopy(_sort or {})
            # {A:True, B:False, C:1, D:0}
            # bool(value) == True --> 升序
            # bool(value) == False --> 降序
        self._variable = False

    def __setattr__(self, name, value):
        assert self._variable
        object.__setattr__(self, name, value)

    def __repr__(self):
        return f'coolmysql.sheet_orm("{self.db_name}.{self.sheet_name}")'
    __str__ = __repr__

    def _copy(self, where=SysEmpty, columns=SysEmpty, _sort=SysEmpty):
        return sheet_orm(
            conn_pool = self.conn_pool,
            db_name = self.db_name,
            sheet_name = self.sheet_name,
            where = self.where if where is SysEmpty else where,
            columns = self.columns if columns is SysEmpty else columns,
            _sort = self._sort if _sort is SysEmpty else _sort
        )

    def _ParseOrder(self):
        if self._sort:
            return ' order by ' + ', '.join([k if v else f"{k} desc" for k,v in self._sort.items()])
        return ''

    def _ParseColumns(self):
        if type(self.columns) is str:
            return self.columns
        return ', '.join(self.columns)
    
    def update_by_pk(self, data:dict):
        pk = self.get_pk()
        records = {}
        for key, line in data.items():
            for field, value in line.items():
                records.setdefault(field, {})[key] = value
        blocks = []
        for field, kvs in records.items():
            s = [f"{field} = ", '    case']
            for k, v in kvs.items():
                s.append(f"        when {pk} = {jsonChinese(k)} then {jsonChinese(v)}")
            s.append(f"else {field}")
            s.append('end')
            blocks.append('\n'.join(s))
        blocks = ' ,\n'.join(blocks)
        sql = f"update {self.sheet_name} set \n{blocks}"
        r, cursor = self.execute(sql=sql)
        return cursor

    def apply(self, handler):
        return MakeSlice(self._applyBase, handler=handler)
    
    def _applyBase(self, key, handler):
        pk = self.get_pk()
        # 添加主键字段
        cols = raw_columns = self.columns
        if isinstance(cols, str): cols = [cols]
        for x in cols:
            if x.strip() in ('*', pk):
                break
        else:
            self.columns = tuple(list(cols) + [pk])
        # 从数据库提取数据
        lines = self[key]
        object.__setattr__(self, 'columns', raw_columns)  # 恢复用户设定的columns
        if type(lines) is dict:
            lines = [lines]
            r_type = 'dict'
        else:
            r_type = 'list'
        # 处理数据
        records = {}
        for line in lines:
            key = line[pk]
            line2 = line.copy()
            handler(line)
            for k, v in line.items():
                if v != line2.get(k, SysEmpty):
                    records.setdefault(k, {})[key] = v
        if r_type == 'dict':
            lines = lines[0]
        # 更新到数据库
        if records:
            blocks = []
            for field, kvs in records.items():
                s = [f"{field} = ", '    case']
                for k, v in kvs.items():
                    s.append(f"        when {pk} = {jsonChinese(k)} then {jsonChinese(v)}")
                s.append(f"else {field}")
                s.append('end')
                blocks.append('\n'.join(s))
            blocks = ' ,\n'.join(blocks)
            sql = f"update {self.sheet_name} set \n{blocks}"
            self.execute(sql=sql)
            return dict(data=lines)
        else:
            return dict(data=lines)

    def order(self, **rule): return self._copy(_sort={**rule})

    def __add__(self, data):
        if type(data) is dict:
            cols = [f"{x}" for x in data]
            sql = f"insert into {self.sheet_name}({', '.join(cols)}) values ({', '.join(('%s',)*len(cols))})"
            rdata, cursor = self.execute(sql, tuple(data.values()))
            return cursor  # cursor.rowcount, cursor.lastrowid
        else:
            cols = set()
            for x in data: cols |= set(x)
            cols = [f"{x}" for x in cols]
            sql = f"insert into {self.sheet_name}({', '.join(cols)}) values ({', '.join(('%s',)*len(cols))})"
            data = tuple(tuple(x.get(k) for k in cols) for x in data)
            r, cursor = self.executemany(sql, data)
            return cursor

    def delete(self):
        return MakeSlice(self._deleteBase)
        
    def _deleteBase(self, key):
        # [::]
        if isinstance(key, slice):
            L, R, S = key.start, key.stop, key.step or 1
            if S in [None,1]:
                if (L in [None,1] and R in [None,-1]) or (L == -1 and R == 1):
                    rdata, cursor = self.execute(f"delete from {self.sheet_name}{self.where}")
                    return cursor
        # [1]且无排序
        if key == 1 and not self._ParseOrder():
            rdata, cursor = self.execute(f"delete from {self.sheet_name}{self.where} limit 1")
            return cursor
        # 其它情况
        pk = self.get_pk()
        try:
            pks = self[pk][key]
        except OrmIndexError:
            rdata, cursor = self.execute(f"delete from {self.sheet_name} where 1 = 2 limit 1")
        else:
            if isinstance(pks, list):
                if pks:
                    pks = [x[pk] for x in pks]
                    rdata, cursor = self.execute(f"delete from {self.sheet_name}{mc[pk].isin(*pks)}")
                else:
                    rdata, cursor = self.execute(f"delete from {self.sheet_name} where 1 = 2")
            else:
                rdata, cursor = self.execute(f"delete from {self.sheet_name}{mc[pk] == pks[pk]} limit 1")
        return cursor

    def update(self, data):
        return MakeSlice(self._updateBase, data=data)
    
    def _updateBase(self, key, data:dict):
        data = ', '.join([f"{k}={v.field}" if isinstance(v,Filter) else f"{k}={jsonChinese(v)}" for k,v in data.items()])
        # [::]
        if isinstance(key, slice):
            L, R, S = key.start, key.stop, key.step or 1
            if S in [None,1]:
                if (L in [None,1] and R in [None,-1]) or (L == -1 and R == 1):
                    rdata, cursor = self.execute(f"update {self.sheet_name} set {data}{self.where}")
                    return cursor
        # [1]且无排序
        if key == 1 and not self._ParseOrder():
            rdata, cursor = self.execute(f"update {self.sheet_name} set {data}{self.where} limit 1")
            return cursor
        # 其它情况
        pk = self.get_pk()
        try:
            pks = self[pk][key]
        except OrmIndexError:
            rdata, cursor = self.execute(f"update {self.sheet_name} set {data} where 1 = 2 limit 1")
        else:
            if isinstance(pks, list):
                if pks:
                    pks = [x[pk] for x in pks]
                    rdata, cursor = self.execute(f"update {self.sheet_name} set {data}{mc[pk].isin(*pks)}")
                else:
                    rdata, cursor = self.execute(f"update {self.sheet_name} set {data} where 1 = 2")
            else:
                rdata, cursor = self.execute(f"update {self.sheet_name} set {data}{mc[pk] == pks[pk]} limit 1")
        return cursor
    
    def execute(self, sql:str, data=None, commit=True):
        mobj:dict = self.conn_pool.get(self.db_name)
        conn:connect = mobj['conn']
        cursor:DictCursor = mobj['cursor']
        if commit:
            try:
                cursor.execute(sql, data)
                r = list(cursor.fetchall())
                conn.commit()
                self.conn_pool.put(mobj)
                return r, cursor
            except:
                conn.rollback()
                raise
        else:
            cursor.execute(sql, data)
            r = list(cursor.fetchall())
            self.conn_pool.put(mobj)
            return r, cursor
    
    def executemany(self, sql:str, data):
        mobj:dict = self.conn_pool.get(self.db_name)
        conn:connect = mobj['conn']
        cursor:DictCursor = mobj['cursor']
        try:
            cursor.executemany(sql, data)
            r = list(cursor.fetchall())
            conn.commit()
            self.conn_pool.put(mobj)
            return r, cursor
        except:
            conn.rollback()
            raise
    
    def get_pk(self):
        if not self._pk:
            sql = f"select column_name from information_schema.columns where table_schema = '{self.db_name}' and table_name = '{self.sheet_name}' and column_key='PRI' "
            rdata, cursor = self.execute(sql, commit=False)
            data = rdata[0]
            assert len(data) == 1
            _pk = list(data.values())[0]
            object.__setattr__(self, '_pk', rdata[0]['COLUMN_NAME'])
        return self._pk
    
    def get_columns(self, comment=True, type=True):
        need = ['column_name as name']
        if comment: need.append('column_comment as comment')
        if type: need.append('column_type as type')
        need = ', '.join(need)
        sql = f"select {need} from information_schema.columns where table_schema = '{self.db_name}' and table_name = '{self.sheet_name}'"
        rdata, cursor = self.execute(sql, commit=False)
        return rdata
    
    def __len__(self):
        rdata, cursor = self.execute(f"select count(1) as tatal from {self.sheet_name}{self.where}", commit=False)
        return rdata[0]['tatal']
    len = __len__

    def __setitem__(self, key, value):
        if value is None:
            self._deleteBase(key)
        elif isinstance(value, dict):
            self._updateBase(key, data=value)
        else:
            raise TypeError(key)
    
    def __getitem__(self, key):
        # 索引取值
        if isinstance(key, int):
            index = key
            if index < 0: index = len(self) + index + 1  # R索引
            if index < 1: raise OrmIndexError(f"index({key}) out of range")
            skip = index - 1
            parseLimit = f" limit {skip}, 1"
            sql = f"select {self._ParseColumns()} from {self.sheet_name}{self.where}{self._ParseOrder()}{parseLimit}"
            r, cursor = self.execute(sql, commit=False)
            if r:
                return r[0]
            else:
                raise OrmIndexError(f"index({key}) out of range")
                # 没有的话引发OrmIndexError错误. 已被self.update和self.delete调用
        # 切片取值
        if isinstance(key, slice):
            # 没有的话返回空列表, 但不要报错. 已被self.update和self.delete调用
            L, R, S = key.start, key.stop, key.step or 1
            tL, tR, tS = type(L), type(R), type(S)
            assert {tL, tR, tS} <= {int, type(None)}
            assert 0 not in (L, R)
            assert S > 0
            lenSheet = float('inf')
            if '-' in f"{L}{R}":  # -是负号
                lenSheet = len(self)
                if '-' in str(L): L = lenSheet + L + 1  # R索引
                if '-' in str(R): R = lenSheet + R + 1  # R索引
            sliceSort = True  # 正序
            if tL is tR is int and R < L:
                L, R = R, L
                sliceSort = False  # 逆序
            skip = max(1, L or 1) - 1  # 把L转化成skip
            if R is None: R = float('inf')
            size = R - skip
            if skip >= lenSheet: return []
            if size > 0:
                if size == float('inf'):
                    parseLimit = f" limit {skip}, 9999999999999"
                else:
                    parseLimit = f" limit {skip}, {size}"
                sql = f"select {self._ParseColumns()} from {self.sheet_name}{self.where}{self._ParseOrder()}{parseLimit}"
                r, cursor = self.execute(sql, commit=False)
                if sliceSort:
                    if S == 1:
                        return r
                    else:
                        return r[::S]
                else:
                    return r[::-S]
            else:
                return []
        # 限定columns
        # 输入多个字符串, 用逗号隔开, Python会自动打包成tuple
        if isinstance(key, (str, tuple)):
            return self._copy(columns=key)
        # Factory
        if isinstance(key, Factory):
            return self._copy(where=self.where & key)
        raise TypeError(key)
    
    def close(self):
        obj = self.conn_pool.get()
        r = obj['conn'].close()
        return r or True
    
    def _native(self): return f"select {self._ParseColumns()} from {self.sheet_name}{self.where}{self._ParseOrder()}"
    def _deleteNative(self): return f"delete from {self.sheet_name}{self.where}"
    def _updateNative(self, data:dict={}):
        data = ', '.join([f"{k}={v}" for k,v in data.items()]) or '____'
        return f"update {self.sheet_name} set {data}{self.where}"


def creat_Filter(cls_or_self, field) -> Filter:
    return Filter(field=field)

class McType(type):
    __getattribute__ = creat_Filter
    __getitem__ = creat_Filter

class mc(object, metaclass=McType):
    id = None  # 预设字段提示

def _builtFunc(cls_or_self, func):
    def builtFunc(*fields):
        return Filter(field=f"{func}({', '.join(fields)})")
    return builtFunc

class MfType(type):
    __getattribute__ = _builtFunc

class mf(object, metaclass=MfType):
    # 函数名提示
    year = day = month = week = hour = None
    md5 = None
    round = ceil = floor = abs = least = greatest = sign = pi = None
    curdate = curtime = utcdata = utctime = now = localtime = None