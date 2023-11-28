import numpy as np
from openpyxl import Workbook

class AData:
    """
    用来作为tablef输出数据的载体,
    内部维护的数据结构为
        {
            (workbook_name, worksheet_title): n2darray of {"$xxx": str}
        }

    数据特点:
        每个ndarray中每个dict要么为{},要么它们的keys相同

    """
    def __init__(self, adata:dict={}):
        self._rdata = adata
        self._summery = self._check_doSummery(adata)  # dict {format: list of {"$XXX": str}}

    @property
    def data(self):
        return self._rdata.copy()

    @property
    def summery(self):
        return {k: v.copy() for k, v in self._summery.items()}

    @staticmethod
    def _check_doSummery(rdata) -> dict:
        """
        检查数据结构是否符合要求
        并且生成summery
        :return: dict {format: list of {"$XXX": str}}
        """
        if not isinstance(rdata, dict):
            raise ValueError("adata must be a dict")

        formats = {}
        # 检查每个ndarray中每个dict的keys是否相同
        for (wb_name, ws_title), data in rdata.items():
            if not isinstance(data, np.ndarray):
                raise ValueError("adata's value must be a ndarray")
            if len(data) == 0:
                print(f"Not find ndarray of {rdata}")
                continue
            if data.ndim != 2:
                raise ValueError("adata's value's ndim must be 2")
            for iy in range(len(data)):
                for ix in range(len(data[0])):
                    if not isinstance(data[iy][ix], dict):
                        raise ValueError("adata's value's element must be a dict")
                    keys = tuple(data[iy][ix].keys())
                    for k in keys:
                        if not isinstance(k, str):
                            raise ValueError("adata's value's element's key must be a str")
                        if not k.startswith("$"):
                            raise ValueError("adata's value's element's key must start with '$'")

                    fdata = formats.get(keys)
                    if fdata is not None:
                        fdata += [data[iy][ix]]
                    else:
                        formats[keys] = [data[iy][ix]]
        return formats

    @staticmethod
    def _combine_dict_of_list(d1, d2):
        """
        将两个dict of list合并
        :param d1:
        :param d2:
        :return:
        """
        if not d1:
            return d2
        if not d2:
            return d1
        for k, v in d2.items():
            _v = d1.get(k)
            if _v is None:
                d1[k] = v
            else:
                d1[k] += v
        return d1

    def append(self, adata:dict, ):
        """
        添加数据
        :param adata: dict of n2darray of dict
        """
        new_summery = self._check_doSummery(adata)
        # 检查keys是否重复
        for k in adata.keys():
            if k in self._rdata:
                raise ValueError(f"key {k} already in raw adata")
        # 合并数据
        self._rdata.update(adata)
        self._summery = self._combine_dict_of_list(self._summery, new_summery)

    def extend(self, adatas:list):
        """
        添加数据
        :param adatas: list of dict of n2darray of dict
        """
        for adata in adatas:
            self.append(adata)

    def __len__(self):
        _sum = 0
        for v in self._summery.values():
            _sum += len(v)
        return _sum

    def __str__(self):
        return f"AData({len(self._summery)} kind of format, {len(self)} data count)"

    def __repr__(self):
        return self.__str__()

    def __add__(self, other):
        """
        合并两个AData
        :param other:
        :return:
        """
        new_data = AData(self._rdata)
        new_data.extend(other._rdata)
        return new_data

    def __iadd__(self, other):
        """
        追加一个AData
        :param other:
        :return:
        """
        self.extend(other._rdata)
        return self

    def toexcel(self) -> Workbook:
        """
        将数据转换为excel
        :return: Workbook
        """
        # 使用summery的数据, 每个key对应一个sheet, 且sheet的排头为key
        wb = Workbook()
        # 移除默认的sheet
        wb.remove(wb.active)
        for fmt, data in self._summery.items():
            ws = wb.create_sheet(title=str(hash(fmt)))
            ws.append(list(fmt))
            for d in data:
                _data = []
                for k in fmt:
                    _data.append(d.get(k, ""))
                ws.append(_data)
        return wb

    @staticmethod
    def _to_n2darray(list_dc:dict, fmt:tuple):
        """
        将[{"$xxx":str}, ]按照特定"$"的顺序转换为n2darray
        """
        data = []
        for d in list_dc:
            _data = []
            for k in fmt:
                if k not in d:
                    raise ValueError(f"key {k} not in dict")
                _data.append(d[k])
            data.append(_data)
        return np.array(data)

    def tondarray(self) -> np.ndarray:
        """
        将数据转换为n3darray
        :return: fmt: (kind of fmt, n, len(fmt))
        """
        new_data = []
        for fmt in self._summery.keys():
            data = self._to_n2darray(self._summery[fmt], fmt)
            new_data.append(data)
        return np.array(new_data)

    def todict(self, item_ndim=1) -> dict:
        """
        将数据转换为dict of n2darray
        :param item_ndim: 1 or 2
        :return: dict of n2darray
        """
        assert item_ndim in (1, 2), f"item_ndim must be 1 or 2, not {item_ndim}"
        if item_ndim == 1:
            return {k: np.array(v) for k, v in self._summery.items()}
        else:
            return {k: self._to_n2darray(v, k) for k, v in self._summery.items()}


    def tolist(self) -> list:
        """
        将数据转换为list of dict
        :return:
        """
        new_list = []
        for v_list in self._summery.values():
            new_list += v_list
        return new_list



