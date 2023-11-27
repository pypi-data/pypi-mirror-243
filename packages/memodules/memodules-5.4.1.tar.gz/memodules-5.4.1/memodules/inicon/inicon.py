# region	|=-=-=-=|Import  Section|=-=-=-=|
from collections import namedtuple
import re
# endregion
# 			|=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=|

# region	|=-=-=-=|Setup Section|=-=-=-=|
__all__ = [
    'INIsNotFound',
    'INI',
    'AbsTrue',
    'AbsFalse',
    'AbsTrueFalse',
    'StrBool',
    'str_bool'
]
Encoding = namedtuple('Encode', ['SJIS', 'UTF8'])('shift-jis', 'utf-8')
# endregion
# 			|=-=-=-=-=-=-=-=-=-=-=-=-=-=-=|


# iniファイルない時用の例外
class INIsNotFound(Exception):
    # .iniファイル必要なのに無いやで。ってやつ

    def __str__(self):
        return '404 Not Found'


class INI:
    'キーダブり対応版'
    def __init__(self, filepath=None, encoding=Encoding.SJIS):
        'キーダブり対応版'
        # filepathがNoneじゃないなら
        if filepath is not None:
            # config管理用の箱用意
            self.config = namedtuple('Config', ['export'])(filepath)
            # 属性file_pathとconfigのexport項目 = filepath
            self.file_path = filepath
        # エンコードキー
        self.chrdec = encoding
        # コンテキストフラグ初期化
        self._context = False
        # .iniの内容入れる用
        self.ini_content = {}
        # ダブりセクションキー: 一時リネームした個数
        self._already_exist = {}
        # 一時リネームしたキー名: 元のキー名
        self._exist_lower = {}

    def _keys(self, ini_contents: dict):
        # 例外回避
        assert isinstance(ini_contents, dict), '正しいアイテムを渡してください。'
        # 渡されたdictのキー取得＆リスト化して返す
        return [k for k in ini_contents.keys()]

    def _ini_item(self, item, value):
        return f'{item}={value}'

    def _item(self, sect, items):
        name, value = items
        section = self.isexist(sect)
        self.ini_content[section][name] = value if str_bool(
            value) is None else str_bool(value)

    def _section(self, name):
        # nameがself.ini_contentに既に存在してるなら
        if name in self.ini_content:
            # self._already_existに既に存在してるなら
            if name in self._already_exist:
                # ダブりでリネームした個数に + 1
                self._already_exist[name] += 1
            else:
                # ダブりでリネームした個数 = 1で新規追加
                self._already_exist[name] = 1

        # 既に存在してるならsection = リネーム名, 否でsection = name
        section = self.isexist(name)
        # self.ini_contentのsectionの項目を新規作成
        self.ini_content[section] = {}

    def _section_wrapp(self, key):
        return f'[{key}]'

    def _write_section(self, section, wrapp=False):
        result = \
            self._exist_lower[section] if section in self._exist_lower \
            else section
        return self._section_wrapp(result) if wrapp else result

    def export(self):
        with open(self.config.export, 'w') as f:
            sections = self._keys(self.ini_content)
            for section in sections:
                f.write(f'{self._write_section(section, wrapp=True)}\n')
                item_dict = self.ini_content[section]
                items = self._keys(item_dict)
                for item in items:
                    f.write(f'{self._ini_item(item, item_dict[item])}\n')

                f.write('\n')

    def isexist(self, key):
        if key in self._already_exist:
            result = f'{key}{self._already_exist[key]}'
            self._exist_lower[result] = key
        else:
            result = key

        return result

    def read(self, ini_file=None):
        current_section = None
        if self._context:
            content = self.file
        elif ini_file is not None:
            content = ini_file
        else:
            raise INIsNotFound

        for cont in content:
            if cont.startswith('['):
                sect = re.sub(r'\[|\]|\n', '', cont)
                self._section(sect)
                current_section = sect
            elif '=' in cont:
                item = cont.split('=')
                for i in range(len(item)):
                    item[i] = re.sub(
                        r'\n', '', item[i]
                    ) if '\n' in item[i] else item[i]
                self._item(current_section, (item[0], item[1]))

        return self.ini_content

    def __getitem__(self, key):
        if len(key) == 2:
            section, item = key
            if section in self.ini_content:
                if item in self.ini_content[section]:
                    return self.ini_content[section][item]
                else:
                    return self.ini_content[section]
            else:
                return None
        elif key == '*':
            return self.ini_content
        else:
            if key in self.ini_content:
                return self.ini_content[key]
            else:
                return None

    def __setitem__(self, key, value):
        if len(key) == 2:
            section, item = key
            if section in self.ini_content:
                if item in self.ini_content[section]:
                    self.ini_content[section][item] = value
                elif isinstance(value, dict):
                    itemkey, itemvalue = value
                    self.ini_content[section][itemkey] = itemvalue
                else:
                    self.ini_content[section][item] = value
        else:
            if key in self.ini_content:
                self.ini_content[key][value] = {}

    def __enter__(self):
        self._context = True
        self.file = open(self.file_path, encoding=self.chrdec)
        self.read()

        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.file.close()


class _StrOrBool:
    def __init__(self, content: '_StrOrBool'):
        self.content = content

    def STRING(self, content: '_StrOrBool' = None):
        ...

    def BOOL(self, content: '_StrOrBool' = None):
        ...

    def __str__(self):
        """
        Example:
            _SubStrOrBool_instance << str('true')
            >>> print(str(_SubStrOrBool_instance))
            bool(True)
        """
        return self.STRING(self.content)

    def __init_true__(self):
        class _true:
            def __init__(subself):
                subself.trues = (True, 1, 'true', '1')

            @property
            def true(subself):
                return subself.trues

            def __contain__(subself, item: str | bool | int):
                if isinstance(item, str):
                    return item.lower() in subself.trues
                else:
                    return item in subself.trues

        return _true()

    def __init_false__(self):
        class _false:
            def __init__(subself):
                subself.falses = (False, 0, 'false', '0', None)

            @property
            def false(subself):
                return subself.falses

            def __contain__(subself, item: str | bool | int):
                if isinstance(item, str):
                    return item.lower() in subself.falses
                else:
                    return item in subself.falses

        return _false()

    def __init_subclass__(cls, *args, **kwargs) -> None:
        super().__init_subclass__(*args, **kwargs)
        cls.true = cls.__init_true__(cls)
        cls.false = cls.__init_false__(cls)

    @property
    def trues(self):
        return self.__init_true__().trues

    @property
    def falses(self):
        return self.__init_false__().falses


class AbsTrue(_StrOrBool):
    def __init__(self, content: _StrOrBool):
        super().__init__(content)

    def __bool__(self) -> bool:
        return self.content in self.true


class AbsFalse(_StrOrBool):
    def __init__(self, content: _StrOrBool):
        super().__init__(content)

    def __bool__(self) -> bool:
        return self.content in self.false


class AbsTrueFalse(_StrOrBool):
    def __init__(self, content: _StrOrBool):
        super().__init__(content)

    def __bool__(self) -> bool:
        if self.content in self.true:
            return True
        elif self.content in self.false:
            return False
        else:
            return None


class StrBool:
    def __new__(cls, content: _StrOrBool, absolute: bool = None):
        if absolute is True:
            self: AbsTrue = AbsTrue(content)
        elif absolute is False:
            self: AbsFalse = AbsFalse(content)
        else:
            self: AbsTrueFalse = AbsTrueFalse(content)

        return self


def str_bool(content: str):
    trues = (True, 1, 'true', '1')
    falses = (False, 0, 'false', '0', None)

    if content.lower() in trues:
        return True
    elif content.lower() in falses:
        return False
    else:
        return None


if __name__ == '__main__':
    print(Encoding)
