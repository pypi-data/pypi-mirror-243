from copy import deepcopy
from motor.motor_asyncio import AsyncIOMotorClient as MongoClient  # 代码提示
from arts.vtype import uniset, empset, SysEmpty, ToolPool, OrmIndexError
from arts.mongo._core import Factory, contain_all, contain_any, contain_none, isin, notin, re
from arts.mongo._core import Filter, mc, MakeSlice, all_columns, upList, mup


repairUpsert = False
# pymongo官方bug
# cannot infer query fields to set, path 'a' is matched twice, full error: {'index': 0, 'code': 54, 'errmsg': "cannot infer query fields to set, path 'a' is matched twice"}

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
    
    def insert(self, data):
        conn:MongoClient = self.conn_pool.get()
        sheet = conn[self.db_name][self.sheet_name]
        if type(data) is dict:
            future = sheet.insert_one(data)
            # r = await sheet.insert(data)
            # r.inserted_id
        else:
            future = sheet.insert_many(data)
            # r = await sheet.insert([line1, line2])
            # r.inserted_ids
        self.conn_pool.put(conn)
        return future

    def delete(self):
        return MakeSlice(self._deleteBase)

    async def _deleteBase(self, key):
        conn:MongoClient = self.conn_pool.get()
        sheet = conn[self.db_name][self.sheet_name]
        # [::]
        if isinstance(key, slice):
            L, R, S = key.start, key.stop, key.step or 1
            if S in [None,1]:
                if (L in [None,1] and R in [None,-1]) or (L == -1 and R == 1):
                    r = await sheet.delete_many(ParseWhere(self))
                    self.conn_pool.put(conn)
                    return r
                    # r.acknowledged, r.deleted_count
        # [1]且无排序
        if key == 1 and not self._ParseOrder():
            r = await sheet.delete_one(ParseWhere(self))
            self.conn_pool.put(conn)
            return r
            # r.acknowledged, r.deleted_count
        # 其它情况
        try:
            ids = await self['_id'][key]
        except OrmIndexError:
            condition = Factory(empset).ParseWhere()
            r = await sheet.delete_one(condition)
            self.conn_pool.put(conn)
            return r
        else:
            if isinstance(ids, list):
                condition = (mc._id == isin(*ids)).ParseWhere()
                r = await sheet.delete_many(condition)
                self.conn_pool.put(conn)
                return r
            else:
                condition = (mc._id == ids['_id']).ParseWhere()
                r = await sheet.delete_one(condition)
                self.conn_pool.put(conn)
                return r

    def update(self, data:dict=None):
        return MakeSlice(self._updateBase, data=data, default=None)
    
    async def _updateBase(self, key, data=None, default=None):
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
                    r = await sheet.update_many(ParseWhere(self), data_)
                    if repairUpsert and not r.matched_count and default:
                        r = await sheet.update_many(empsetCondi, {'$setOnInsert':default}, upsert=True)
                    self.conn_pool.put(conn)
                    return r
                    # r.acknowledged, r.matched_count
                    # matched_count 与 modified_count 的区别:
                    ## matched_count 表示匹配到的数目, 如果是update_one, 则 matched_count in [0, 1]
                    ## modified_count 表示数据有变化的数目
                    ## 如果一条数据修改前和修改后一致(例如:把3修改成3), 则不会统计到modified_count中
        # [1]且无排序
        if key == 1 and not self._ParseOrder():
            r = await sheet.update_one(ParseWhere(self), data_)
            if repairUpsert and not r.matched_count and default:
                r = await sheet.update_one(empsetCondi, {'$setOnInsert':default}, upsert=True)
            self.conn_pool.put(conn)
            return r
            # r.acknowledged, r.matched_count
        # 其它情况
        try:
            ids = await self['_id'][key]
        except OrmIndexError:
            if repairUpsert and default:
                r = await sheet.update_one(empsetCondi, {'$setOnInsert':default}, upsert=True)
            else:
                r = await sheet.update_one(empsetCondi, {'$set':{}})
            self.conn_pool.put(conn)
            return r
        else:
            if isinstance(ids, list):
                if ids:
                    ids = [x['_id'] for x in ids]
                    condition = (mc._id == isin(*ids)).ParseWhere()
                    r = await sheet.update_many(condition, data_)
                    self.conn_pool.put(conn)
                    return r
                else:
                    if repairUpsert and default:
                        r = await sheet.update_many(empsetCondi, {'$setOnInsert':default}, upsert=True)
                    else:
                        r = await sheet.update_many(empsetCondi, {'$set':{}})
                    self.conn_pool.put(conn)
                    return r
            else:
                condition = (mc._id == ids['_id']).ParseWhere()
                r = await sheet.update_one(condition, data_)
                self.conn_pool.put(conn)
                return r
    
    async def len(self):
        conn:MongoClient = self.conn_pool.get()
        sheet = conn[self.db_name][self.sheet_name]
        tatal = await sheet.count_documents(ParseWhere(self))
        self.conn_pool.put(conn)
        return tatal
    
    def get(self, index, default=None):
        try:
            return self[index]
        except IndexError:
            return default

    async def _find_one(self, key):
        index = key
        if index < 0: index = await self.len() + index + 1
        if index < 1: raise OrmIndexError(f"index({key}) out of range")
        skip = index - 1
        conn:MongoClient = self.conn_pool.get()
        sheet = conn[self.db_name][self.sheet_name]
        sh = sheet.find(ParseWhere(self), self._ParseColumns())
        if sort:= self._ParseOrder():
            sh = sh.sort(sort)
        if skip: sh = sh.skip(skip)
        r = await sh.limit(1).to_list(1)
        self.conn_pool.put(conn)
        if r:
            return r[0]
        else:
            raise OrmIndexError(f"index({key}) out of range")
            # 没有的话引发OrmIndexError错误. 已被self.update和self.delete调用

    async def _find_many(self, key):
        # 没有的话返回空列表, 但不要报错. 已被self.update和self.delete调用
        L, R, S = key.start, key.stop, key.step or 1
        tL, tR, tS = type(L), type(R), type(S)
        assert {tL, tR, tS} <= {int, type(None)}
        assert 0 not in (L, R)
        assert S > 0
        lenSheet = float('inf')
        if '-' in f"{L}{R}":  # -是负号
            lenSheet = await self.len()
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
            r = [x async for x in sh]
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
    
    def __getitem__(self, key):
        # 索引取值
        if isinstance(key, int):
            return self._find_one(key)
        # 切片取值
        if isinstance(key, slice):
            return self._find_many(key)
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

    async def get_sheet_names(self):
        conn:MongoClient = self.conn_pool.get()
        sheets = await conn[self.db_name].list_collection_names()
        self.conn_pool.put(conn)
        return sheets
    
    async def len(self): return len(await self.get_sheet_names())

    async def __iter__(self):
        async for x in self.get_sheet_names():
            yield x
    
    async def delete_all_sheets(self):
        conn:MongoClient = self.conn_pool.get()
        db = conn[self.db_name]
        r = [await db.drop_collection(name) for name in db.list_collection_names()]
        self.conn_pool.put(conn)
        return r

    async def delete_sheets(self, *names):
        conn:MongoClient = self.conn_pool.get()
        db = conn[self.db_name]
        r = [await db.drop_collection(name) for name in names]
        self.conn_pool.put(conn)
        return r

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
    
    async def get_db_names(self):
        conn:MongoClient = self.conn_pool.get()
        dbs = await conn.list_database_names()
        self.conn_pool.put(conn)
        return dbs
    
    async def len(self): return len(await self.get_db_names())

    async def __iter__(self):
        async for x in self.get_db_names():
            yield x
    
    async def delete_all_dbs(self):
        conn:MongoClient = self.conn_pool.get()
        dbs:list = conn.list_database_names()
        try:
            dbs.remove('admin')
        except:
            pass
        r = [await conn.drop_database(db_name) for db_name in dbs]
        self.conn_pool.put(conn)
        return r

    async def delete_dbs(self, *names):
        conn:MongoClient = self.conn_pool.get()
        r = [await conn.drop_database(db_name) for db_name in names]
        self.conn_pool.put(conn)
        return r

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