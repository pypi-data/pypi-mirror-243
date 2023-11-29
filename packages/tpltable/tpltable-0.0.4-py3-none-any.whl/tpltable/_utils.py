
SRTLEN = 16
IWLEN = 12

def iwPrint(srtname:str, iwmsc:str, *args, sep=' ', end='\n', file=None):
    """
    info Warning Print
    :param srtname: source name
    :param iwmsc: info/warning message
    :param args:
    :param sep:
    :param end:
    :param file:
    """
    srtname = f"[{srtname}]"
    iwmsc = f"[{iwmsc}]"
    # print(f'{srtname:^{SRTLEN}}{iwmsc:^{IWLEN}}', *args, sep=sep, end=end, file=file)  # 居中srtname和iwmsc
    print(f'{srtname:<{SRTLEN}}{iwmsc:<{IWLEN}}', *args, sep=sep, end=end, file=file)



