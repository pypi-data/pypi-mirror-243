import re

import numpy as np

from tpltable import BookTableF, Pipe, pFunc, tHWEXCEL_find, AData

# Format In ----------------------------------
summery, _ = tHWEXCEL_find(r"C:\Users\22290\Desktop\tpltable 数据")
fpaths = summery.tolist(summery.FPATH)


btf = BookTableF(r'C:\Users\22290\Desktop\tpltable 数据\a.xlsx')
print(btf.format)                           # 看一下模板的格式
ad = AData()                                # 模板匹配区域化结果数据 Template Matched Area's Result Data

# 导入所有表格数据
for fpath in fpaths:
    _ = btf.readf(fpath, simplify=False)    # 格式化读入数据

    ad.append(_)                            # 记录数据

# 检查数据
print(ad)
# ad.toexcel().save('test.xlsx')              # 导出数据到excel
# print(ad.tolist())                        # list of dict like {"$XXX": ...}       # 太大了,就不放出来了
# print(ad.todict(item_ndim=2))             # dict of 1d/2d ndarray                 # 太大了,就不放出来了
# print(ad.tondarray().shape)                 # (kind of format, data count, len(format))

# Pipe ----------------------------------
@pFunc('$fTIME')
def get_time(rname) -> str:
    _ = re.split(r'[：:]', rname)
    assert len(_) >= 1, f'can not split {rname}'
    return _[-1]

@pFunc('$fAUTHOR')
def get_name(rname) -> str:
    _ = re.split(r'[：:]', rname)
    assert len(_) >= 1, f'can not split {rname}'
    return _[-1]


@pFunc('$HW_NAME', '$HW_NAME$LINE_NAME')
def get_line_name(rname) -> (str, str):
    rname = re.sub(r'\s', '', rname)
    _ = re.findall(r'10[kK][vV]\w+线[\w#]+环网柜', rname)
    if not _:
        return rname, None
    _ = _[0]
    _ = _[4:-3]
    index = _.find('线')
    if index == -1:
        return rname, None
    return _[index + 1:], _[:index + 1]


def newline(rname) -> str:
    """
    为过长的目标自动换行
    :param rname:
    :return:
    """
    # 假定长度超过7的为过长,需要每7个字符换行
    if len(rname) < 7:
        return rname
    _ = []
    for i in range(0, len(rname), 7):
        _.append(rname[i:i + 7])
    return '\n'.join(_)


@pFunc()
def reshape(data: np.ndarray) -> np.ndarray:
    """
    对数据进行reshape,并清除空数据
    :param data: ndarray of dict
    :return:
    """
    data = data.reshape(-1)
    # 去除空{}数据
    data = data[data != {}]
    return data.reshape((-1, 1))


pipe = Pipe(btf.format)
pipe += get_name
pipe += get_time
pipe += get_line_name
pipe.add(newline, '$HW_DTU_ftNAME')
pipe.add(newline, '$HW_PROTECT_ftNAME')
pipe.add(newline, '$HW_ftNAME')
pipe += reshape
print(pipe.format)

new_data = pipe(
    np.array(ad.tolist()).reshape((-1, 1))
)

# Format Out ----------------------------------
o_btf = BookTableF(r'C:\Users\22290\Desktop\tpltable 数据\c.xlsx')
o_btf.writef(new_data).save('d.xlsx')
