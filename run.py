#!/usr/bin/python
# coding: UTF-8
#####################################################
# ::Project  : Korei Bot Win
# ::Admin    : Korei (@korei-xlix)
# ::github   : https://github.com/korei-xlix/koreibot_win/
# ::Class    : 実行処理
#####################################################
import sys
sys.path.append('script')

sys.path.append('script/api')
sys.path.append('script/data')
sys.path.append('script/disp')
sys.path.append('script/func')
sys.path.append('script/oslib')
sys.path.append('script/sys')

from main_console import CLS_Main_Console
from gval import gVal
#####################################################
CLS_Main_Console.sRun()		#コンソール起動




コンソールスレッド
ユーザコンソールからの指示を待ち受け、実行する。

タイムラインスレッド
定期的にタイムラインをロードし、リアクションを拾ったら、受信アクションに詰める。

リアクションスレッド
定期的に受信アクションを監視し、順番にリアクションを実施する。

受信アクション
タイムラインから受信したアクションを受け取り、リアクションスレッドに渡すバッファ。






from concurrent.futures import ThreadPoolExecutor
import time

def make_udon(kind):
    print('  %sうどんを作ります。' % kind)
    time.sleep(3)
    return kind + 'うどん'

kinds = ['たぬき', 'かけ', 'ざる', 'きつね', '天ぷら', '肉']
executor = ThreadPoolExecutor(max_workers=3)
futures = []

for kind in kinds:
    print('%sうどん オーダー入りました。' % kind)
    future = executor.submit(make_udon, kind)
    futures.append(future)

for future in futures:
    print('%sお待たせしました。' % future.result())

executor.shutdown()






