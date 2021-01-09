'''
@Description:
@Version: 1.0
@Autor: Demoon
@Date: 1970-01-01 08:00:00
LastEditors: Please set LastEditors
LastEditTime: 2021-01-09 16:03:26
'''
#  基础模块
import sys
import time
import os
from DeeplTrans import DeeplTrans

if __name__ == '__main__':
    # 定义为全局变量，方便其他模块使用
    global RUN_EVN
    try:
        RUN_EVN = sys.argv[1]
    except Exception:
        pass
    depts = DeeplTrans(True)
    org_path = './files/org/'
    out_path = './files/output/'
    for root, dirs, files in os.walk(org_path):
        for fname in files:
            org_file = os.path.join(root, fname)
            out_file = os.path.join(out_path, fname)
            with open(org_file, 'r', encoding='utf-8') as f:
                with open(out_file, 'a', encoding='utf-8') as nf:
                    line = f.readline()
                    while line:
                        try:
                            res = depts.runTranslate(line)
                        except Exception:
                            os.system('wideband_link_refresh.bat')
                            time.sleep(3)   # 等3秒 怕连不上
                            res = depts.runTranslate(line)
                        nf.writelines(res + "\n")
                        line = f.readline()
            os.remove(org_file)
