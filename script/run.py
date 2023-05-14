#!/usr/bin/python
# coding: UTF-8
#####################################################
# ::Project  : Korei Bot Misskey
# ::Admin    : Korei (@korei-xlix)
# ::github   : https://github.com/korei-xlix/koreibot_misskey/
# ::Class    : 実行処理
#####################################################
import sys

sys.path.append('api')
sys.path.append('db')
sys.path.append('func')
sys.path.append('func')
sys.path.append('main')
sys.path.append('sys')

#####################################################
from main import CLS_Main
from gval import gVal
#####################################################
OBJ_MAIN = CLS_Main()
OBJ_MAIN.Run()		#メインスレッド起動






'''
WEBサーバ
cron
　　misskey bot



python3
postgreSQL
misskey API
botアカウント(別途)



スレッド化する


コンソールスレッド
	ユーザコンソールからの指示を待ち受け、実行する。

タイムラインスレッド
	定期的にタイムラインをロードし、リアクションを拾ったら、受信アクションに詰める。

リアクションスレッド
	定期的に受信アクションを監視し、順番にリアクションを実施する。

受信アクション
	タイムラインから受信したアクションを受け取り、リアクションスレッドに渡すバッファ。






ログDB化

登録日付
検知日時

スレッド
クラス
関数
タグ
コメント
ダンプ出力(ファイル)

ログのファイルダンプ対応（解析しにくいよね！）



できること

・ノートの文字にリアクションで反応する
	コンソールから自在に登録可能とする
	複数ランダムにできる

・定期・時限ツイート

・自動クリップ

・自動フォロー


'''



