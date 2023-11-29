'''
Date         : 2023-01-17 10:33:06
Author       : BDFD,bdfd2005@gmail.com
Github       : https://github.com/bdfd
LastEditTime : 2023-11-28 14:00:10
LastEditors  : BDFD
Description  : 
FilePath     : \execdata\format\_format_data.py
Copyright (c) 2023 by BDFD, All Rights Reserved. 
'''
import execdata as exe


def fill_zeros(num, full_position=2):
    # exe.format.convint(num)
    result = str(num).zfill(full_position)
    return result
