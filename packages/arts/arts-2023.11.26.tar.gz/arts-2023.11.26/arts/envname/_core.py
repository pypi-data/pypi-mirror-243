import sys
from arts.moduledb import ModuleDB, File
from arts import envname


try:
    import platform
    EnvName = platform.processor() or 'null'
except:
    EnvName = 'null'

sheet: File = ModuleDB(envname, depth=1)['sheet_1']

EnvName = sheet.setdefault('EnvName', EnvName)


def _ParseCmd():
    kws = sys.argv[1:]
    if kws:
        kw = kws[0].lower()

        # 创建环境名称
        if kw == 'set' and len(kws) > 1:
            sheet['EnvName'] = kws[1]
            print('创建成功!')
        
        # 查看环境名称
        elif kw == 'read':
            print(EnvName)
    else:
        print('''指令集:
envname set <名称> | 创建环境名称
envname read       | 查看环境名称
''')