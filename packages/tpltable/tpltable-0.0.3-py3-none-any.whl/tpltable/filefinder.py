import os
import re
import numpy as np

"""
该部分代码旨在搜索目标目录下的特定文件
"""


class FSummery:
    """
    该类用于对搜索结果进行汇总
    """
    CLS = 0
    RELPATH = 1
    FNAME = 2
    FTYPE = 3
    # ---------------
    CLSDIR = 5
    FDIR = 6
    FNAMETYPE = 7
    FPATH = 8

    def __init__(self, root_path: str, ndarray_data: np.ndarray):
        """

        :param root_path:
        :param ndarray_data: cls, relpath, fname, ftype
        """
        self.root_path = root_path
        self.data = ndarray_data

    def __str__(self):
        return f"<{self.__class__.__name__} root={self.root_path}>\ncls\t\trelpath\t\tfname\t\tftype\n" + str(self.data)

    def _list_add_root(self, rel_list, abspath=True):
        if abspath:
            return [os.path.join(self.root_path, rel) for rel in rel_list]
        else:
            return rel_list

    def tolist(self, val_type: int, abspath=True):
        """
        将搜索结果转换为list
        :param val_type: int 0 - 8, 参考类属性
        :param abspath: 当val_type不为FNAME, FTYPE和FNAMETYPE时有效, 为True时返回绝对路径, 为False时返回相对路径
        :return:
        """
        # val types: 0 - 8
        if val_type <= self.FTYPE:
            if val_type in (self.FNAME, self.FTYPE):
                return self.data[:, val_type].tolist()
            return self._list_add_root(self.data[:, val_type].tolist(), abspath)

        _vCLSDIR_list = self.data[:, self.CLS].tolist()
        if val_type == self.CLSDIR:
            return self._list_add_root(_vCLSDIR_list, abspath)
        _vFDIR_list = [os.path.join(_vCLSDIR, relpath) for _vCLSDIR, relpath in zip(_vCLSDIR_list, self.data[:, self.RELPATH].tolist())]
        if val_type == self.FDIR:
            return self._list_add_root(_vFDIR_list, abspath)
        _vFNAMETYPE_list = [fname + ftype for fname, ftype in zip(self.data[:, self.FNAME].tolist(), self.data[:, self.FTYPE].tolist())]
        if val_type == self.FNAMETYPE:
            return _vFNAMETYPE_list
        _vFPATH_list = [os.path.join(_vFDIR, fnametype) for _vFDIR, fnametype in zip(_vFDIR_list, _vFNAMETYPE_list)]
        if val_type == self.FPATH:
            return self._list_add_root(_vFPATH_list, abspath)
        raise ValueError(f"val_type: {val_type} is not valid.")

    def todict(self, key_type: int, val_type: int, abspath=None, key_abspath=True, val_abspath=True):
        """
        将搜索结果转换为dict
        :param key_type:
        :param val_type:
        :param abspath:
        :param key_abspath:
        :param val_abspath:
        :return:
        """
        # 注意检查key的重复
        # key & val types: 0 - 8
        if abspath is not None:
            key_abspath = abspath
            val_abspath = abspath
        keys = self.tolist(key_type, key_abspath)
        vals = self.tolist(val_type, val_abspath)

        # check key
        if len(keys) != len(set(keys)):
            raise ValueError(f"keys: {keys}\n\t is not unique.")
        return dict(zip(keys, vals))


class FileFinder:
    def __init__(self, target_path: str, default_types=()):
        if target_path == '':
            target_path = os.getcwd()
        self.dir = target_path
        self.dftypes = self._types_format(*default_types)

    @staticmethod
    def _types_format(*types):
        new_types = []
        for _t in types:
            _t = _t.lower()
            if _t[0] != '.':
                _t = '.' + _t
            new_types.append(_t)
        return new_types

    @staticmethod
    def _match_fname(target_fname: str, pattern: str = None, exclude: str = None, *std_types):
        fnameb, ftype = os.path.splitext(target_fname)
        if ftype.lower() in std_types:
            flag = True
            if pattern:
                flag = re.match(pattern, fnameb)

            if flag and exclude:
                flag = not re.match(exclude, fnameb)

            return flag
        return False

    @staticmethod
    def _pack_finfo(root_dir, fpath) -> tuple:
        """
        例如
        root_dir = 'D:\Python\PycharmProjects\PyUtils'
        fpath = 'D:\Python\PycharmProjects\PyUtils\aa\filefinder.py'
        返回: 'D:\Python\PycharmProjects\PyUtils', 'aa', "", 'filefinder', '.py'
        例如
        root_dir = 'D:\Python\PycharmProjects\PyUtils'
        fpath = 'D:\Python\PycharmProjects\PyUtils\aa\bb\cc\filefinder.py'
        返回: 'D:\Python\PycharmProjects\PyUtils', 'aa', "bb\cc", 'filefinder', '.py'
        :param root_dir:
        :param fpath:
        :return:
        """
        relpath = os.path.relpath(fpath, root_dir)
        relpaths = os.path.split(os.path.dirname(relpath))
        clsname = relpaths[0]
        relpath = os.path.join(*relpaths[1:])
        fnameb, ftype = os.path.splitext(os.path.basename(fpath))
        return clsname, relpath, fnameb, ftype

    _last_log = []

    @property
    def log(self) -> str:
        # return self._last_log
        return '\n'.join(self._last_log)

    def _new_log(self, msg=None):
        if msg:
            self._last_log = [msg]
        else:
            self._last_log = []

    def _log(self, msg):
        self._last_log.append(msg)

    def find(self, *added_types, pattern: str = None, exclude: str = None):
        """
        在target_path下寻找特定类型的文件, 会递归搜索子目录
        :param added_types: 可以添加额外的类型, 加不加.都可以
        :param pattern: str, 目标文件名的正则表达筛选
        :param exclude: str, 目标文件名的正则排除筛选
        :return: ndarray clsname(file's cls define), relpath(compare to clsname), fname, ftype
        """
        # Step 1: format type in types
        # Step 2: walk through with pattern & exclude
        # Step 3: build-up ndarray
        # --------------------
        # 1:
        types = self.dftypes.copy() + self._types_format(*added_types)
        self._new_log(f"----------------------| {self.__class__.__name__} Log ---------------------->:\n"
                      f"Param: types: {types}, pattern: {pattern}, exclude: {exclude}")

        # 2、3:
        new_data = []
        target_list, clsnames = os.listdir(self.dir), []
        # 目标目录
        self._log(f'Find Start at {self.dir}')
        for fname in target_list:
            fpath = os.path.join(self.dir, fname)
            if os.path.isfile(fpath):
                if self._match_fname(fname, pattern, exclude, *types):
                    new_data.append(self._pack_finfo(self.dir, fpath))
                    # log
                    self._log(f'Add file {fname}')
                else:
                    # log
                    self._log(f'File {fname} is not matched.')
            elif os.path.isdir(fpath):
                clsnames.append(fname)
                # log
                self._log(f'Find cls {fname}')

        # 目标子目录(clsname)
        for clsname in clsnames:
            # log
            self._log(f'Find in {clsname} ----------------------------------------------------')
            clsdir = os.path.join(self.dir, clsname)
            # walk instead of listdir
            for root, dirs, files in os.walk(clsdir):
                for fname in files:
                    fpath = os.path.join(root, fname)
                    if self._match_fname(fname, pattern, exclude, *types):
                        new_data.append(self._pack_finfo(self.dir, fpath))
                        # log
                        self._log(f'Add file {fname}')
                    else:
                        # log
                        self._log(f'File {fname} is not matched.')

        return FSummery(self.dir, np.array(new_data))


def tHWEXCEL_find(target_path: str) -> tuple:
    """
    寻找目标目录下的环网柜excel文件, 返回summery和log
    :param target_path:
    :return:
    """
    ff = FileFinder(target_path)
    fdata = ff.find('xls', 'xlsx', pattern='^10[kK][vV].*线', exclude=r'^~.*')

    return fdata, ff.log


if __name__ == '__main__':
    summery, log = tHWEXCEL_find(r'')
    print(summery)
    print(log)
