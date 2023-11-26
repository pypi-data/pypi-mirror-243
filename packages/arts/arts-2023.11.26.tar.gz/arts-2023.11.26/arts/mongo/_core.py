from copy import deepcopy
from pymongo import MongoClient  # 代码提示

from arts.vtype import uniset, empset, SysEmpty, ToolPool, OrmIndexError


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

    def _deepcopy(self, obj):
        if obj in (uniset, empset):
            return obj
        return deepcopy(obj)

    def __and__(self, obj):  # 交集
        a = self._deepcopy(self.where)
        b = self._deepcopy(obj.where)
        if a is uniset: return Factory(b)
        if b is uniset: return Factory(a)
        if a and b:  # a和b有可能是empset
            if set(a) & set(b):
                return Factory({'$and': [a, b]})
            return Factory({**a, **b})
        return Factory(empset)
    
    def __or__(self, obj):  # 并集
        a = self._deepcopy(self.where)
        b = self._deepcopy(obj.where)
        if a is empset: return Factory(b)
        if b is empset: return Factory(a)
        if a is uniset or b is uniset:
            return Factory(uniset)
        return Factory({'$or': [a, b]})
    
    def __sub__(self, obj): return self & (~ obj)  # 差集

    def __invert__(self):  # 补集
        w = self.where
        if w is uniset: return Factory(empset)
        if w is empset: return Factory(uniset)
        return Factory({'$nor': [w]})
    
    def ParseWhere(self):
        where  = self._deepcopy(self.where)
        if where is uniset: return {}
        if where is empset: return {'$and': [{'a':1}, {'a':2}]}
        return where

class moBase():
    def __init__(self, *lis, **dic):
        self.lis = lis
        self.dic = dic

class contain_all(moBase): ...
class contain_any(moBase): ...
class contain_none(moBase): ...
class isin(moBase): ...
class notin(moBase): ...
def re(s, i=False):
    if i:
        return {'$regex': s, '$options': 'i'}
    return {'$regex': s}

def GetFiField(obj:'Filter'):
    return object.__getattribute__(obj, 'field')

class Filter():
    _variable = True

    def __init__(self, field:str):
        self.field = field
        self._variable = False
    
    def __setattr__(self, name, value):
        assert object.__getattribute__(self, '_variable')
        object.__setattr__(self, name, value)
    
    def __getattribute__(self, field): return Filter(f"{GetFiField(self)}.{field}")
    __getitem__ = __getattribute__

    def __lt__(self, obj): return Factory({GetFiField(self): {'$lt': obj}})  # <
    def __le__(self, obj): return Factory({GetFiField(self): {'$lte': obj}})  # <=
    def __gt__(self, obj): return Factory({GetFiField(self): {'$gt': obj}})  # >
    def __ge__(self, obj): return Factory({GetFiField(self): {'$gte': obj}})  # >=
    def __ne__(self, obj): return Factory({GetFiField(self): {'$ne': obj}})  # !=

    def __eq__(self, obj):
        if isinstance(obj, contain_all):
            lis = obj.lis
            if len(lis) == 1: return Factory({GetFiField(self): {'$elemMatch':{'$eq':lis[0]}}})
            if len(lis) > 1: return Factory({'$and': [{GetFiField(self): {'$elemMatch':{'$eq':x}}} for x in set(lis)]})
            return Factory(uniset)
        
        elif isinstance(obj, contain_any):
            lis = obj.lis
            if len(lis) == 1: return Factory({GetFiField(self): {'$elemMatch':{'$eq':lis[0]}}})
            if len(lis) > 1: return Factory({'$or': [{GetFiField(self): {'$elemMatch':{'$eq':x}}} for x in set(lis)]})
            return Factory(empset)
        
        elif isinstance(obj, contain_none):
            lis = obj.lis
            if lis: return Factory({'$nor': [{GetFiField(self): {'$elemMatch':{'$eq':x}}} for x in set(lis)]})
            return Factory(uniset)
        
        elif isinstance(obj, isin):
            lis = obj.lis
            if not lis: return Factory(empset)
            if len(lis) == 1: return Factory({GetFiField(self): lis[0]})
            return Factory({GetFiField(self): {'$in': lis}})
        
        elif isinstance(obj, notin):
            lis = obj.lis
            if not lis: return Factory(uniset)
            if len(lis) == 1: return Factory({GetFiField(self): {'$ne': lis[0]}})
            return Factory({GetFiField(self): {'$nin': lis}})
        
        return Factory({GetFiField(self): obj})


class MakeSlice():
    def __init__(self, func, *vs, **kvs):
        self.func = func
        self.vs = vs
        self.kvs = kvs
    
    def __getitem__(self, key):
        return self.func(key, *self.vs, **self.kvs)

class upList(): ...
class mup:
    class push(upList):  # 添加
        name = '$push'
        def __init__(self, *vs):
            self.value = {"$each":list(vs)}
    
    class add(upList):  # 不存在时才添加
        name = '$addToSet'
        def __init__(self, *vs):
            self.value = {"$each":list(vs)}

    class inc(upList):  # 自增:inc(1), 自减:inc(-1)
        name = '$inc'
        def __init__(self, value):
            self.value = value

    class pull(upList):  # 从数组field内删除一个等于value值
        name = '$pull'
        def __init__(self, value):
            self.value = value

    class rename(upList):  # 修改字段名称
        name = '$rename'
        def __init__(self, value):
            self.value = value

    class _(upList):  # 删除键
        name = '$unset'
        value = 1
    unset = delete = _()

    class _(upList):
        name = '$pop'
        def __init__(self, value):
            self.value = value
    popfirst = _(-1)  # 删除数组第1个元素, 和Python相反, -1代表最前面
    poplast = _(1)  # 删除数组最后1个元素


repairUpsert = False
# pymongo官方bug
# cannot infer query fields to set, path 'a' is matched twice, full error: {'index': 0, 'code': 54, 'errmsg': "cannot infer query fields to set, path 'a' is matched twice"}


class all_columns: ...


class sheet_orm():
    _variable = True

    def __init__(self, conn_pool:ToolPool, db_name:str, sheet_name:str, where=None, columns=all_columns, _sort=None):
        assert columns
        self.conn_pool = conn_pool
        self.db_name = db_name
        self.sheet_name = sheet_name
        self.where = where or Factory(uniset)
        self.columns = columns  # str型 或 tuple型 或 all_columns, 都是不可变的
        self._sort = deepcopy(_sort or {})
            # {A:True, B:False, C:1, D:0}
            # bool(value) == True 表示升序
            # bool(value) == False 表示降序
        self._variable = False

    def __setattr__(self, name, value):
        assert self._variable
        object.__setattr__(self, name, value)

    def __getattr__(self, name):
        conn:MongoClient = self.conn_pool.get()
        return conn[self.db_name][self.sheet_name].__getattribute__(name)

    def __repr__(self):
        return f'coolmongo.sheet_orm("{self.db_name}.{self.sheet_name}")'
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

    def _ParseColumns(self):
        cols = self.columns
        if cols is all_columns: return None
        if isinstance(cols, tuple):
            cols = dict.fromkeys(cols, 1)
        else:
            cols = {cols:1}
        cols.setdefault('_id', 0)
        return cols

    def order(self, **rule): return self._copy(_sort={**rule})

    def _ParseOrder(self):
        if self._sort:
            return [(k, 1 if v else -1) for k,v in self._sort.items()]
        return []
    
    def __add__(self, data):
        conn:MongoClient = self.conn_pool.get()
        sheet = conn[self.db_name][self.sheet_name]
        if type(data) is dict:
            r = sheet.insert_one(data)  # 分配到的 _id 为 str(r)
        else:
            r = sheet.insert_many(data)  # r.acknowledged, r.inserted_ids
        self.conn_pool.put(conn)
        return r

    def delete(self):
        return MakeSlice(self._deleteBase)

    def _deleteBase(self, key):
        conn:MongoClient = self.conn_pool.get()
        sheet = conn[self.db_name][self.sheet_name]
        # [::]
        if isinstance(key, slice):
            L, R, S = key.start, key.stop, key.step or 1
            if S in [None,1]:
                if (L in [None,1] and R in [None,-1]) or (L == -1 and R == 1):
                    r = sheet.delete_many(ParseWhere(self))
                    self.conn_pool.put(conn)
                    return r
                    # r.acknowledged, r.deleted_count
        # [1]且无排序
        if key == 1 and not self._ParseOrder():
            r = sheet.delete_one(ParseWhere(self))
            self.conn_pool.put(conn)
            return r
            # r.acknowledged, r.deleted_count
        # 其它情况
        try:
            ids = self['_id'][key]
        except OrmIndexError:
            condition = Factory(empset).ParseWhere()
            r = sheet.delete_one(condition)
            self.conn_pool.put(conn)
            return r
        else:
            if isinstance(ids, list):
                condition = (mc._id == isin(*ids)).ParseWhere()
                r = sheet.delete_many(condition)
                self.conn_pool.put(conn)
                return r
            else:
                condition = (mc._id == ids['_id']).ParseWhere()
                r = sheet.delete_one(condition)
                self.conn_pool.put(conn)
                return r

    def update(self, data:dict=None):
        return MakeSlice(self._updateBase, data=data, default=None)
    
    def _updateBase(self, key, data=None, default=None):
        data_ = {'$set':{}}
        for k,v in (data or {}).items():
            if isinstance(v, upList):
                data_.setdefault(v.name, {})[k] = v.value
            else:
                data_['$set'][k] = v
        conn:MongoClient = self.conn_pool.get()
        sheet = conn[self.db_name][self.sheet_name]
        empsetCondi = Factory(empset).ParseWhere()
        # [::]
        if isinstance(key, slice):
            L, R, S = key.start, key.stop, key.step or 1
            if S in [None,1]:
                if (L in [None,1] and R in [None,-1]) or (L == -1 and R == 1):
                    r = sheet.update_many(ParseWhere(self), data_)
                    if repairUpsert and not r.matched_count and default:
                        r = sheet.update_many(empsetCondi, {'$setOnInsert':default}, upsert=True)
                    self.conn_pool.put(conn)
                    return r
                    # r.acknowledged, r.matched_count
                    # matched_count 与 modified_count 的区别:
                    ## matched_count 表示匹配到的数目, 如果是update_one, 则 matched_count in [0, 1]
                    ## modified_count 表示数据有变化的数目
                    ## 如果一条数据修改前和修改后一致(例如:把3修改成3), 则不会统计到modified_count中
        # [1]且无排序
        if key == 1 and not self._ParseOrder():
            r = sheet.update_one(ParseWhere(self), data_)
            if repairUpsert and not r.matched_count and default:
                r = sheet.update_one(empsetCondi, {'$setOnInsert':default}, upsert=True)
            self.conn_pool.put(conn)
            return r
            # r.acknowledged, r.matched_count
        # 其它情况
        try:
            ids = self['_id'][key]
        except OrmIndexError:
            if repairUpsert and default:
                r = sheet.update_one(empsetCondi, {'$setOnInsert':default}, upsert=True)
            else:
                r = sheet.update_one(empsetCondi, {'$set':{}})
            self.conn_pool.put(conn)
            return r
        else:
            if isinstance(ids, list):
                if ids:
                    ids = [x['_id'] for x in ids]
                    condition = (mc._id == isin(*ids)).ParseWhere()
                    r = sheet.update_many(condition, data_)
                    self.conn_pool.put(conn)
                    return r
                else:
                    if repairUpsert and default:
                        r = sheet.update_many(empsetCondi, {'$setOnInsert':default}, upsert=True)
                    else:
                        r = sheet.update_many(empsetCondi, {'$set':{}})
                    self.conn_pool.put(conn)
                    return r
            else:
                condition = (mc._id == ids['_id']).ParseWhere()
                r = sheet.update_one(condition, data_)
                self.conn_pool.put(conn)
                return r
    
    def __len__(self):
        conn:MongoClient = self.conn_pool.get()
        sheet = conn[self.db_name][self.sheet_name]
        tatal = sheet.count_documents(ParseWhere(self))
        self.conn_pool.put(conn)
        return tatal
    
    def get(self, index, default=None):
        try:
            return self[index]
        except IndexError:
            return default

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
            if index < 0: index = len(self) + index + 1
            if index < 1: raise OrmIndexError(f"index({key}) out of range")
            skip = index - 1
            conn:MongoClient = self.conn_pool.get()
            sheet = conn[self.db_name][self.sheet_name]
            sh = sheet.find(ParseWhere(self), self._ParseColumns())
            if sort:= self._ParseOrder():
                sh = sh.sort(sort)
            if skip: sh = sh.skip(skip)
            r = list(sh.limit(1))
            self.conn_pool.put(conn)
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
                conn:MongoClient = self.conn_pool.get()
                sheet = conn[self.db_name][self.sheet_name]
                sh = sheet.find(ParseWhere(self), self._ParseColumns())
                if sort:= self._ParseOrder():
                    sh = sh.sort(sort)
                if skip: sh = sh.skip(skip)
                if isinstance(size, int): sh = sh.limit(size)
                r = list(sh)
                self.conn_pool.put(conn)
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
        if isinstance(key, (str, tuple)) or key is all_columns:
            return self._copy(columns=key)
        # Factory
        if isinstance(key, Factory):
            return self._copy(where=self.where & key)
        raise TypeError(key)

def ParseWhere(obj:sheet_orm):
    return obj.where.ParseWhere()

class db_orm():
    def __init__(self, conn_pool:ToolPool, db_name):
        self.conn_pool = conn_pool
        self.db_name = db_name

    def __getattr__(self, name):
        conn:MongoClient = self.conn_pool.get()
        return conn[self.db_name].__getattribute__(name)

    def __repr__(self):
        return f'coolmongo.db_orm("{self.db_name}")'
    __str__ = __repr__

    def get_sheet_names(self):
        conn:MongoClient = self.conn_pool.get()
        sheets = conn[self.db_name].list_collection_names()
        self.conn_pool.put(conn)
        return sheets
    
    def __len__(self): return len(self.get_sheet_names())

    def __contains__(self, sheet_name): return sheet_name in self.get_sheet_names()

    def __iter__(self):
        yield from self.get_sheet_names()
    
    def __delitem__(self, key):
        conn:MongoClient = self.conn_pool.get()
        db = conn[self.db_name]
        if isinstance(key, str):
            db.drop_collection(key)
        elif isinstance(key, tuple):
            for sheet_name in key:
                db.drop_collection(sheet_name)
        elif isinstance(key, slice):
            assert key.start is key.stop is key.step is None
            for sheet_name in db.list_collection_names():
                db.drop_collection(sheet_name)
        else:
            self.conn_pool.put(conn)
            raise TypeError(key)
        self.conn_pool.put(conn)

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

class ORM():
    def __init__(self, mkconn):
        self.conn_pool = ToolPool(mktool=mkconn, minlen=1, maxlen=1)
        # 当增删改查报错时, conn不再放回连接池, 以避免含有残留数据

    def __getattr__(self, name):
        conn:MongoClient = self.conn_pool.get()
        return conn.__getattribute__(name)
    
    def get_db_names(self):
        conn:MongoClient = self.conn_pool.get()
        dbs = conn.list_database_names()
        self.conn_pool.put(conn)
        return dbs
    
    def __len__(self): return len(self.get_db_names())

    def __contains__(self, db_name): return db_name in self.get_db_names()

    def __iter__(self):
        yield from self.get_db_names()

    def __delitem__(self, key):
        conn:MongoClient = self.conn_pool.get()
        if isinstance(key, str):
            conn.drop_database(key)
        elif isinstance(key, tuple):
            for db_name in key:
                conn.drop_database(db_name)
        elif isinstance(key, slice):
            assert key.start is key.stop is key.step is None
            dbs:list = conn.list_database_names()
            try:
                dbs.remove('admin')
            except:
                pass
            for db_name in dbs:
                conn.drop_database(db_name)
        else:
            self.conn_pool.put(conn)
            raise TypeError(key)
        self.conn_pool.put(conn)
    
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


def creat_Filter(cls_or_self, field) -> Filter:
    return Filter(field=field)

class McType(type):
    __getattribute__ = creat_Filter
    __getitem__ = creat_Filter

class mc(object, metaclass=McType):
    _id = None  # 预设字段提示