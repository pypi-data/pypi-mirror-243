from copy import deepcopy


class end: ...

class DFA():
    tree = {}

    ignore_words = set('''
    `-_=~!@#$%^&*()+[ ]\\{}|;\',./:"<>?·！￥…（）—【】、；‘：“，。《》？
    ～＆＠＃”’〝〞＂＇´﹞﹝＞＜«»‹›〔〕〈〉』『〗〖｝｛」「］［︵︷︹︿︽﹁﹃︻︗＼｜／︘︼﹄﹂︾﹀︺︸︶＿﹏﹍﹎
    \n\r \t¦¡\xad¨ˊ¯￣﹋﹉﹊ˋ︴¿ˇ\u3000
'''.lower())

    def __init__(self, *words):
        self.tree = deepcopy(self.tree)
        self.ignore_words = self.ignore_words.copy()
        self.add_words(words)
    
    def add_words(self, words:list|tuple|set|dict):
        ignore_words = self.ignore_words
        for word in set(words):
            if word:
                tree = self.tree
                for x in word.lower():
                    if x not in ignore_words:
                        tree = tree.setdefault(x, {})
                tree[end] = 0

    def add_ignore_words(self, *words:str):
        for x in words:
            self.ignore_words |= set(x)

    def has_any(self, text:str) -> bool:
        text = text.lower()
        for start_i, t in enumerate(text):
            if t not in self.ignore_words:
                if self._find_base(text, start_i):
                    return True
        return False
    
    def find_one(self, text:str) -> str:
        text = text.lower()
        for start_i, t in enumerate(text):
            if t not in self.ignore_words:
                if i := self._find_base(text, start_i):
                    return text[start_i: i] 
        return ''
    
    def find_all(self, text:str) -> list:
        text = text.lower()
        words = []
        done_i = -1
        for start_i, t in enumerate(text):
            if start_i > done_i and t not in self.ignore_words:
                if right := self._find_base(text, start_i):
                    done_i = right - 1
                    words.append(text[start_i: right])
        return words
    
    def sub(self, text:str, repl:str='*', compress=False) -> str:
        done_i = -1
        new_text = []
        content = text.lower()
        if compress:
            for start_i, t in enumerate(content):
                if start_i > done_i and t not in self.ignore_words:
                    if right := self._find_base(content, start_i):
                        new_text.append(text[done_i+1: start_i])
                        new_text.append(repl)
                        done_i = right - 1
        else:
            for start_i, t in enumerate(content):
                if start_i > done_i and t not in self.ignore_words:
                    if right := self._find_base(content, start_i):
                        new_text.append(text[done_i+1: start_i])
                        new_text.append(repl * (right-start_i))
                        done_i = right - 1
        new_text.append(text[done_i+1:])
        return ''.join(new_text)
    
    def _find_base(self, text, start_i):
        tree = self.tree
        for i in range(start_i, len(text)):
            s = text[i]
            if TreeSon := tree.get(s):
                if end in TreeSon:
                    return i + 1  # i 是终止字符的索引, 由于 Python 切片是右开区间, 切片的第 2 个值是 i+1, 即: s[_:i+1]
                else:
                    tree = TreeSon
            elif s not in self.ignore_words:
                return None