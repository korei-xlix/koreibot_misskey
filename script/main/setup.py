#!/usr/bin/python
# coding: UTF-8
#####################################################
# ::Project  : Korei Bot Win
# ::Admin    : Korei (@korei-xlix)
# ::github   : https://github.com/korei-xlix/koreibot_win/
# ::Class    : セットアップ
#####################################################
from mylog import CLS_Mylog

from osif import CLS_OSIF
from filectrl import CLS_File
from db_if import CLS_DB_IF
from twitter_if import CLS_Twitter_IF
from gval import gVal
#####################################################
class CLS_Setup():
#####################################################

#####################################################
# 初期化
#####################################################
	def __init__(self):
		return



#####################################################
# セットアップ
#####################################################
	def Setup( self, inData ):
		#############################
		# 応答形式の取得
		#   "Result" : False, "Class" : None, "Func" : None, "Reason" : None, "Responce" : None
		wRes = CLS_OSIF.sGet_Resp()
		wRes['Class'] = "CLS_Setup"
		wRes['Func']  = "Setup"
		
		CLS_OSIF.sPrn( "セットアップモードで起動しました" + '\n' )
		
		#############################
		# DBに接続
		gVal.OBJ_DB_IF = CLS_DB_IF()
		wSubRes = gVal.OBJ_DB_IF.Connect( inData )
		if wSubRes['Result']!=True :
			return False
		if wSubRes['Responce']!=True :
			##テーブルがない= 初期化してない
			##DB初期化
			self.__initDB( gVal.OBJ_DB_IF.OBJ_DB )
			CLS_OSIF.sPrn( "データベースを初期化しました" + '\n' )
		
		#############################
		# ユーザチェック
		wSubRes = gVal.OBJ_DB_IF.CheckUserData()
		if wSubRes['Result']!=True :
			gVal.OBJ_DB_IF.Close()
			
			wSubRes['Reason'] = "ユーザチェックに失敗しました: " + wSubRes['Reason'] + '\n'
			CLS_OSIF.sErr( wSubRes )
			return False
		
		wTwitterAccount = wSubRes['Responce']['Account']
		#############################
		# ユーザありの場合
		if wSubRes['Responce']['detect']==True :
			wStr = "ユーザ " + wTwitterAccount + " は既に登録されています。キーの変更をおこないますか？" + '\n'
			CLS_OSIF.sPrn( wStr )
			wSelect = CLS_OSIF.sInp( "変更する？(y/N)=> " )
			if wSelect!="y" :
				###キャンセル
				wStr = "ユーザデータは正常でした。" + '\n'
				CLS_OSIF.sPrn( wStr )
				
				gVal.OBJ_DB_IF.Close()
				wRes['Result'] = True
				return wRes
		
		### ※ユーザ変更あり
		
		#############################
		# ログオブジェクトの生成
		gVal.OBJ_L = CLS_Mylog()
		
		#############################
		# Twitterキーの入力と接続テスト
		gVal.OBJ_Tw_IF = CLS_Twitter_IF()
		wSubRes = gVal.OBJ_Tw_IF.SetTwitter( wTwitterAccount )
		if wSubRes['Result']!=True :
			gVal.OBJ_DB_IF.Close()
			
			wSubRes['Reason'] = "Twitterキーの入力と接続テストに失敗しました :" + wSubRes['Reason'] + '\n'
			CLS_OSIF.sErr( wSubRes )
			return False
		
		#############################
		# ユーザを登録、もしくは更新する
		wSubRes = gVal.OBJ_DB_IF.SetUserData( wSubRes['Responce'] )
		if wSubRes['Result']!=True :
			gVal.OBJ_DB_IF.Close()
			
			wSubRes['Reason'] = wSubRes['Reason'] + ": ユーザ登録に失敗しました。" + '\n'
			CLS_OSIF.sErr( wSubRes )
			return False
		
		#############################
		# データ追加
		if gVal.STR_SystemInfo['EXT_FilePath']!=None and \
		   gVal.STR_SystemInfo['EXT_FilePath']!="" :
			wSubRes = self.Add( inData, inDBconn=False )
			if wSubRes!=True :
				gVal.OBJ_DB_IF.Close()
				
				wSubRes['Reason'] = "データ追加に失敗しました: " + wSubRes['Reason'] + '\n'
				CLS_OSIF.sErr( wSubRes )
				return False
		
		#############################
		# 終わり
		gVal.OBJ_DB_IF.Close()
		return True



#####################################################
# 全初期化
#   作業ファイルとDBを全て初期化する
#####################################################
	def AllInit( self, inData ):
		#############################
		# 応答形式の取得
		#   "Result" : False, "Class" : None, "Func" : None, "Reason" : None, "Responce" : None
		wRes = CLS_OSIF.sGet_Resp()
		wRes['Class'] = "CLS_Setup"
		wRes['Func']  = "AllInit"
		
		#############################
		# 実行の確認
		wStr = "データベースと全ての作業ファイルをクリアします。" + '\n'
		CLS_OSIF.sPrn( wStr )
		wSelect = CLS_OSIF.sInp( "よろしいですか？(y/N)=> " )
		if wSelect!="y" :
			##キャンセル
			return True
		
		#############################
		# DBに接続 (接続情報の作成)
		gVal.OBJ_DB_IF = CLS_DB_IF()
		wSubRes = gVal.OBJ_DB_IF.Connect( inData )
		if wSubRes['Result']!=True :
			return False
		
		#############################
		# DB初期化
		self.__initDB( gVal.OBJ_DB_IF.OBJ_DB )
		CLS_OSIF.sPrn( "データベースを初期化しました" + '\n' )
		
		#############################
		# 終わり
		gVal.OBJ_DB_IF.Close()
		CLS_OSIF.sPrn( "全初期化が正常終了しました。" )
		
		#############################
		# セットアップの確認
		wStr = "続いてセットアップを続行しますか。" + '\n'
		CLS_OSIF.sPrn( wStr )
		wSelect = CLS_OSIF.sInp( "セットアップする？(y/N)=> " )
		if wSelect!="y" :
			##キャンセル
			return True
		
		###入力の手間を省くため、パスワードを引き継ぐ
		self.Setup( inData )
		return True



#####################################################
# データ追加モード
#####################################################
	def Add( self, inData, inWordOnly=False, inDBconn=True ):
		#############################
		# 応答形式の取得
		#   "Result" : False, "Class" : None, "Func" : None, "Reason" : None, "Responce" : None
		wRes = CLS_OSIF.sGet_Resp()
		wRes['Class'] = "CLS_Setup"
		wRes['Func']  = "Add"
		
		if inWordOnly==False :
			CLS_OSIF.sPrn( "〇 追加データをデータベースに追加します" + '\n' )
		else:
			CLS_OSIF.sPrn( "● 禁止ワードをデータベースに追加します" + '\n' )
		
		#############################
		# データアーカイブのあるフォルダの存在チェック
		if CLS_File.sExist( gVal.STR_SystemInfo['EXT_FilePath'] )!=True :
			## フォルダがないと失敗扱い
			wRes['Reason'] = "アーカイブのフォルダがありません: path=" + str( gVal.STR_SystemInfo['EXT_FilePath'] )
			CLS_OSIF.sErr( wRes )
			return False
		
		#############################
		# デフォルトの除外ユーザ・文字の読み出し
		# ・除外ファイルの解凍
		# ・読み出し
		# ・解凍の削除
		
		###デフォルト除外文字ファイルの解凍
		#    アーカイブのフォルダパス
		#    アーカイブ解凍先
		wExcWordArc_Path      = str( gVal.STR_SystemInfo['EXT_FilePath'] ) + gVal.DEF_STR_FILE['ExcWordArc']
		wMelt_ExcWordArc_Path = str( gVal.STR_SystemInfo['EXT_FilePath'] ) + gVal.DEF_STR_FILE['Melt_ExcWordArc_path']
		if CLS_File.sArciveMelt( inSrcPath=wExcWordArc_Path, inDstPath=wMelt_ExcWordArc_Path )!=True :
			wRes['Reason'] = "デフォルト除外文字ファイルの解凍に失敗しました: srcpath=" + wExcWordArc_Path + " dstpath=" + wMelt_ExcWordArc_Path
			CLS_OSIF.sErr( wRes )
			return False
		
		###ローカルに読み出し
		#    除外データ 文字列ファイル
		wFilePath = str( gVal.STR_SystemInfo['EXT_FilePath'] ) + gVal.DEF_STR_FILE['Melt_ExcWordArc_path'] + gVal.DEF_STR_FILE['Melt_ExcWord']
		wARR_ExcWord = []
		if CLS_File.sReadFile( wFilePath, outLine=wARR_ExcWord )!=True :
			wRes['Reason'] = "解凍ファイルが見つかりません: path=" + wFilePath
			CLS_OSIF.sErr( wRes )
			return False
		
		#    除外データ 文字列ファイル
		wFilePath = str( gVal.STR_SystemInfo['EXT_FilePath'] ) + gVal.DEF_STR_FILE['Melt_ExcWordArc_path'] + gVal.DEF_STR_FILE['Melt_ExcProf']
		wARR_ExcProf = []
		if CLS_File.sReadFile( wFilePath, outLine=wARR_ExcProf )!=True :
			wRes['Reason'] = "解凍ファイルが見つかりません: path=" + wFilePath
			CLS_OSIF.sErr( wRes )
			return False
		
		if inWordOnly==False :
			#    禁止ユーザ
			wFilePath = str( gVal.STR_SystemInfo['EXT_FilePath'] ) + gVal.DEF_STR_FILE['Melt_ExcWordArc_path'] + gVal.DEF_STR_FILE['Melt_ExcUser']
			wARR_ExcUser = []
			if CLS_File.sReadFile( wFilePath, outLine=wARR_ExcUser )!=True :
				wRes['Reason'] = "解凍ファイルが見つかりません: path=" + wFilePath
				CLS_OSIF.sErr( wRes )
				return False
			
			#    リストいいね指定ファイル
			wFilePath = str( gVal.STR_SystemInfo['EXT_FilePath'] ) + gVal.DEF_STR_FILE['Melt_ExcWordArc_path'] + gVal.DEF_STR_FILE['Melt_ListFavo']
			wARR_ListFavo = []
			if CLS_File.sReadFile( wFilePath, outLine=wARR_ListFavo )!=True :
				wRes['Reason'] = "解凍ファイルが見つかりません: path=" + wFilePath
				CLS_OSIF.sErr( wRes )
				return False
		
		###解凍したフォルダ削除
		if CLS_File.sRmtree( wMelt_ExcWordArc_Path )!=True :
			wRes['Reason'] = "解凍フォルダの削除に失敗しました: path=" + wMelt_ExcWordArc_Path
			CLS_OSIF.sErr( wRes )
			return False
		
		#############################
		# DBに接続 (接続情報の作成)
		if inDBconn==True :
			gVal.OBJ_DB_IF = CLS_DB_IF()
			wSubRes = gVal.OBJ_DB_IF.Connect( inData )
			if wSubRes['Result']!=True or wSubRes['Responce']!=True :
				return False
		
		#############################
		# ログオブジェクトの生成
		gVal.OBJ_L = CLS_Mylog()
		
		#############################
		# Twitterデータ取得
		wTwitterDataRes = gVal.OBJ_DB_IF.GetTwitterData( gVal.STR_UserInfo['Account'] )
		if wTwitterDataRes['Result']!=True :
			wRes['Reason'] = "GetTwitterData is failed"
			CLS_OSIF.sErr( wRes )
			return False
		
		#############################
		# Twitterに接続
		gVal.OBJ_Tw_IF = CLS_Twitter_IF()
		wTwitterRes = gVal.OBJ_Tw_IF.Connect( wTwitterDataRes['Responce'] )
		if wTwitterRes['Result']!=True :
			wRes['Reason'] = "Twitterの接続失敗: reason=" + wResTwitter['Reason']
			gVal.OBJ_L.Log( "B", wRes )
			CLS_OSIF.sErr( wRes )
			return False
		
		#############################
		# 除外ユーザ名、文字、プロファイルの設定
		wSubRes = gVal.OBJ_DB_IF.SetExeWord( wARR_ExcWord )
		if wSubRes['Result']!=True :
			return False
		
		wSubRes = gVal.OBJ_DB_IF.SetExeProf( wARR_ExcProf )
		if wSubRes['Result']!=True :
			return False
		
		if inWordOnly==False :
			#############################
			# 禁止ユーザの設定
			
			CLS_OSIF.sPrn( "〇 禁止ユーザの設定中..." + '\n' )
			#############################
			# 登録データを作成する
			wARR_Word = {}
			wListNo = 1
			for wLine in wARR_ExcUser :
				### コメントアウトはスキップ
				wIfind = wLine.find("#")
				if wIfind==0 :
					continue
				
				wARR_Line = wLine.split(",")
				### 要素数が少ないのは除外
###				if len(wARR_Line)!=3 :
				if len(wARR_Line)!=4 :
					continue
				
				wVip = False
				wOpe = False
				### データ登録
				### 通報あり
				wReport = True if wARR_Line[0]=="***" else False
				if wReport==True :
					### 通報ありの場合、VIP、VIP監視ではなくなる
					wVip = False
					wOpe = False
				else:
					### 通報なしの場合、VIP有効
					wVip = True
					wOpe = True if wARR_Line[1]=="***" else False
				
				### フォロー監視あり
				wFollow = True if wARR_Line[2]=="***" else False
				
				### ユーザ名
###				wUser = wARR_Line[2]
				wUser = wARR_Line[3]
				
				### Twitterからユーザ情報を取得する
				wUserInfoRes = gVal.OBJ_Tw_IF.GetUserinfo( inScreenName=wUser )
				if wUserInfoRes['Result']!=True :
					continue
				
				wUserID = str( wUserInfoRes['Responce']['id'] )
				
				### データ登録
				wCell = {
					"list_number"	: wListNo,
					"id"			: wUserID,
					"screen_name"	: wUser,
					"report"		: wReport,
					"vip"			: wVip,
					"ope"			: wOpe,
					"follow"		: wFollow,
					"rel_date"		: str( gVal.DEF_TIMEDATE ),
					"memo"			: ""
				}
				wARR_Word.update({ wUserID : wCell })
				wListNo += 1
			
			wSubRes = gVal.OBJ_DB_IF.SetExeUser( wARR_Word )
			if wSubRes['Result']!=True :
				return False
			
			CLS_OSIF.sPrn( "〇 リストいいね指定の設定中..." + '\n' )
			#############################
			# リストいいね指定の設定
			
			#############################
			# 登録データを作成する
			wARR_Data = {}
			wListNo = 1
			for wLine in wARR_ListFavo :
				
				### コメントアウトはスキップ
				wIfind = wLine.find("#")
				if wIfind==0 :
					continue
				
				wARR_Line = wLine.split(",")
				### 要素数が少ないのは除外
				if len(wARR_Line)!=6 :
					continue
				
				### データ登録
				### フォロー/フォロワー含むか
				wARR_Line[0] = True if wARR_Line[0]=="***" else False
				### 警告
				wARR_Line[1] = True if wARR_Line[1]=="***" else False
				### センシティブツ
				wARR_Line[2] = True if wARR_Line[2]=="***" else False
				### 自動リムーブ
				wARR_Line[3] = True if wARR_Line[3]=="***" else False
				
				wListName   = wARR_Line[5]
				wScreenName = wARR_Line[4]
				
				CLS_OSIF.sPrn( "user= " + wScreenName + " list= " + wListName + " 設定中..." )
				
				### Twitterからユーザ情報を取得する
				wUserInfoRes = gVal.OBJ_Tw_IF.GetUserinfo( inScreenName=wScreenName )
				if wUserInfoRes['Result']!=True :
					continue
				
				wUserID = str( wUserInfoRes['Responce']['id'] )
				
				### Twitterからリスト情報を取得する
				wListRes = gVal.OBJ_Tw_IF.GetLists( inScreenName=wScreenName )
				if wListRes['Result']!=True :
					continue
				wListID = None
				wKeylist = list( wListRes['Responce'].keys() )
				for wKey in wKeylist :
					if wListRes['Responce'][wKey]['name']!=wListName :
						continue
					wListID = str( wListRes['Responce'][wKey]['id'] )
					break
				if wListID==None :
					continue
				
				wCell = {
					"list_number"	: wListNo,
					"id"			: wListID,
					"list_name"		: wListName,
					"user_id"		: wUserID,
					"screen_name"	: wScreenName,
					"valid"			: True,
					"follow"		: wARR_Line[0],
					"caution"		: wARR_Line[1],
					"sensitive"		: wARR_Line[2],
					"auto_rem"		: wARR_Line[3],
					"update"		: False
				}
				
				wARR_Data.update({ wListID : wCell })
				wListNo += 1
			
			wSubRes = gVal.OBJ_DB_IF.SetListFavo( wARR_Data )
			if wSubRes['Result']!=True :
				return False
		
		#############################
		# DBを閉じる
		if inDBconn==True :
			gVal.OBJ_DB_IF.Close()
		
		#############################
		# 正常終了
		CLS_OSIF.sPrn( "〇 データの追加が正常終了しました。" )
		return True



#####################################################
# クリア
#   一部のDBを初期化する
#####################################################
	def testClear( self, inData ):
		#############################
		# 応答形式の取得
		#   "Result" : False, "Class" : None, "Func" : None, "Reason" : None, "Responce" : None
		wRes = CLS_OSIF.sGet_Resp()
		wRes['Class'] = "CLS_Setup"
		wRes['Func']  = "testClear"
		
		#############################
		# 実行の確認
		wSelect = CLS_OSIF.sInp( "test clear run (y/N)=> " )
		if wSelect!="y" :
			##キャンセル
			return True
		
		#############################
		# DBに接続 (接続情報の作成)
		gVal.OBJ_DB_IF = CLS_DB_IF()
		wSubRes = gVal.OBJ_DB_IF.Connect( inData )
		if wSubRes['Result']!=True :
			return False
		
		#############################
		# DB初期化
		self.__create_TBL_TIME_DATA( gVal.OBJ_DB_IF.OBJ_DB )
		self.__create_TBL_LOG_DATA( gVal.OBJ_DB_IF.OBJ_DB )
		self.__create_TBL_TRAFFIC_DATA( gVal.OBJ_DB_IF.OBJ_DB )
		self.__create_TBL_FAVOUSER_DATA( gVal.OBJ_DB_IF.OBJ_DB )
		
		#############################
		# ログオブジェクトの生成
		gVal.OBJ_L = CLS_Mylog()
		
		#############################
		# tbl_time_infoの初期化
		gVal.OBJ_DB_IF.AutoInsert_TimeInfo()
		
		#############################
		# 終わり
		gVal.OBJ_DB_IF.Close()
		CLS_OSIF.sPrn( "clear complete !!!" )
		
		return True



#####################################################
# Pingテスト
#####################################################
	def Ping( self, inHost=None ):
		#############################
		# 応答形式の取得
		#   "Result" : False, "Class" : None, "Func" : None, "Reason" : None, "Responce" : None
		wRes = CLS_OSIF.sGet_Resp()
		wRes['Class'] = "CLS_Setup"
		wRes['Func']  = "Ping"
		
		#############################
		# Pingテスト
		gVal.OBJ_Tw_IF = CLS_Twitter_IF()
		wSubRes = gVal.OBJ_Tw_IF.Ping( inHost=inHost )
		if wSubRes['Result']!=True :
			wSubRes['Reason'] = "Twitterキーの入力と接続テストに失敗しました :" + wSubRes['Reason'] + '\n'
			CLS_OSIF.sErr( wSubRes )
			return False
		
		CLS_OSIF.sPrn( "-- Ping正常 --" )
		
		#############################
		# 終わり
		return True



#####################################################
# データベースの初期化
#####################################################
	def __initDB( self, inDBobj ):
		self.__create_TBL_USER_DATA( inDBobj )
		self.__create_TBL_TWITTER_DATA( inDBobj )
		self.__create_TBL_TIME_DATA( inDBobj )
		self.__create_TBL_FAVOUSER_DATA( inDBobj )
		self.__create_TBL_LOG_DATA( inDBobj )
		self.__create_TBL_TRAFFIC_DATA( inDBobj )
		self.__create_TBL_EXC_WORD( inDBobj )
		self.__create_TBL_EXC_PROF( inDBobj )
		self.__create_TBL_EXC_USER( inDBobj )
		self.__create_TBL_CAUTION_TWEET( inDBobj )
		self.__create_TBL_SEARCH_WORD( inDBobj )
		self.__create_TBL_LIST_FAVO( inDBobj )
		return True

	#####################################################
	def __allDrop( self, inDBobj ):
		wQy = "drop table if exists tbl_user_data ;"
		inOBJ_DB.RunQuery( wQy )
		wQy = "drop table if exists tbl_twitter_data ;"
		inOBJ_DB.RunQuery( wQy )
		wQy = "drop table if exists tbl_time_data ;"
		inOBJ_DB.RunQuery( wQy )
		wQy = "drop table if exists tbl_favouser_data ;"
		inOBJ_DB.RunQuery( wQy )
		wQy = "drop table if exists tbl_log_data ;"
		inOBJ_DB.RunQuery( wQy )
		wQy = "drop table if exists tbl_traffic_data ;"
		inOBJ_DB.RunQuery( wQy )
		wQy = "drop table if exists tbl_exc_word ;"
		inOBJ_DB.RunQuery( wQy )
		wQy = "drop table if exists tbl_exc_prof ;"
		inOBJ_DB.RunQuery( wQy )
		wQy = "drop table if exists tbl_exc_user ;"
		inOBJ_DB.RunQuery( wQy )
		wQy = "drop table if exists tbl_caution_tweet ;"
		inOBJ_DB.RunQuery( wQy )
		wQy = "drop table if exists tbl_search_word ;"
		inOBJ_DB.RunQuery( wQy )
		wQy = "drop table if exists tbl_list_favo ;"
		inOBJ_DB.RunQuery( wQy )
		return True



#####################################################
# テーブル作成: TBL_USER_DATA
#####################################################
	def __create_TBL_USER_DATA( self, inOBJ_DB, inTBLname="tbl_user_data" ):
		#############################
		# テーブルのドロップ
		wQy = "drop table if exists " + inTBLname + ";"
		inOBJ_DB.RunQuery( wQy )
		
		#############################
		# テーブル枠の作成
		wQy = "create table " + inTBLname + "("
		wQy = wQy + "twitterid   TEXT  NOT NULL,"		# 記録したユーザ(Twitter ID)
		wQy = wQy + "regdate     TIMESTAMP,"			# 登録日時
		wQy = wQy + "locked      BOOL  DEFAULT false,"	# 排他ロック true=ロックON
		wQy = wQy + "lok_date    TIMESTAMP,"			# 排他日時
		wQy = wQy + "get_date    TIMESTAMP,"			# 排他獲得日時
		wQy = wQy + "rel_date    TIMESTAMP,"			# 排他解除日時
		wQy = wQy + "trendtag    TEXT  NOT NULL,"		# トレンド送信タグ
		wQy = wQy + "list_id     TEXT  NOT NULL,"		# リスト通知 リストID(数値)
		wQy = wQy + "list_name   TEXT  NOT NULL,"		# リスト通知 リスト名
		wQy = wQy + "autoremove  BOOL  DEFAULT false,"	# 自動リムーブ true=ON
		wQy = wQy + "mlist_id    TEXT  NOT NULL,"		# 相互フォローリスト リストID(数値)
		wQy = wQy + "mlist_name  TEXT  NOT NULL,"		# 相互フォローリスト リスト名
		wQy = wQy + "flist_id    TEXT  NOT NULL,"		# 片フォロワーリスト リストID(数値)
		wQy = wQy + "flist_name  TEXT  NOT NULL,"		# 片フォロワーリスト リスト名
		wQy = wQy + "viptag      TEXT  NOT NULL,"		# VIPリツイート タグ
		wQy = wQy + "auto_seq    INTEGER DEFAULT 0,"	# 自動監視シーケンス
		wQy = wQy + "mfvstop      BOOL  DEFAULT false,"	# 相互いいね停止 true=有効
		wQy = wQy + "mfvstop_date TIMESTAMP,"			# 相互いいね停止 開始日
		wQy = wQy + "questiontag  TEXT  NOT NULL,"		# 質問タグ
		wQy = wQy + "deltag       TEXT  NOT NULL,"		# 削除タグ
		wQy = wQy + " PRIMARY KEY ( twitterid ) ) ;"
		
		inOBJ_DB.RunQuery( wQy )
		return



#####################################################
# テーブル作成: TBL_TWITTER_DATA
#####################################################
	def __create_TBL_TWITTER_DATA( self, inOBJ_DB, inTBLname="tbl_twitter_data" ):
		#############################
		# テーブルのドロップ
		wQy = "drop table if exists " + inTBLname + ";"
		inOBJ_DB.RunQuery( wQy )
		
		#############################
		# テーブル枠の作成
		wQy = "create table " + inTBLname + "("
		wQy = wQy + "twitterid   TEXT  NOT NULL,"		# 記録したユーザ(Twitter ID)
		wQy = wQy + "apikey      TEXT  NOT NULL,"		# Twitter Devで取ったAPI key
		wQy = wQy + "apisecret   TEXT  NOT NULL,"		# Twitter Devで取ったAPI secret
		wQy = wQy + "acctoken    TEXT  NOT NULL,"		# Twitter Devで取ったAccess Token Key
		wQy = wQy + "accsecret   TEXT  NOT NULL,"		# Twitter Devで取ったAccess Token secret
		wQy = wQy + "bearer      TEXT  NOT NULL,"		# Twitter Devで取ったbearer
		wQy = wQy + " PRIMARY KEY ( twitterid ) ) ;"
		
		inOBJ_DB.RunQuery( wQy )
		return



#####################################################
# テーブル作成: TBL_TIME_DATA
#####################################################
	def __create_TBL_TIME_DATA( self, inOBJ_DB, inTBLname="tbl_time_data" ):
		#############################
		# テーブルのドロップ
		wQy = "drop table if exists " + inTBLname + ";"
		inOBJ_DB.RunQuery( wQy )
		
		#############################
		# テーブル枠の作成
		wQy = "create table " + inTBLname + "("
		wQy = wQy + "twitterid    TEXT  NOT NULL,"		# 記録したユーザ(Twitter ID)
		wQy = wQy + "run          TIMESTAMP,"			# コマンド実行
		wQy = wQy + "autorun      TIMESTAMP,"			# 自動監視
		wQy = wQy + "autoseq      TIMESTAMP,"			# 自動監視シーケンス
		wQy = wQy + "reaction     TIMESTAMP,"			# リアクション受信
		wQy = wQy + "mffavo       TIMESTAMP,"			# 相互フォローリストいいね
		wQy = wQy + "flfavo       TIMESTAMP,"			# フォロワー支援いいね
		wQy = wQy + "list_clear   TIMESTAMP,"			# リスト通知クリア
		wQy = wQy + "auto_remove  TIMESTAMP,"			# 自動リムーブ
		wQy = wQy + "send_favo    TIMESTAMP,"			# いいね情報送信
		wQy = wQy + "auto_delete  TIMESTAMP,"			# 自動削除
		wQy = wQy + "vip_ope      TIMESTAMP,"			# VIP監視
		wQy = wQy + "del_tweet    TIMESTAMP,"			# 削除ツイート
		wQy = wQy + "tl_follow    TIMESTAMP,"			# タイムラインフォロー
		wQy = wQy + "keywordsrch  TIMESTAMP,"			# 自動キーワードいいね
		wQy = wQy + "send_ren     TIMESTAMP,"			# 連ファボ送信
		wQy = wQy + " PRIMARY KEY ( twitterid ) ) ;"
		
		inOBJ_DB.RunQuery( wQy )
		return



#####################################################
# テーブル作成: TBL_LOG_DATA
#####################################################
	def __create_TBL_LOG_DATA( self, inOBJ_DB, inTBLname="tbl_log_data" ):
		#############################
		# テーブルのドロップ
		wQy = "drop table if exists " + inTBLname + ";"
		inOBJ_DB.RunQuery( wQy )
		
		#############################
		# テーブル枠の作成
		wQy = "create table " + inTBLname + "("
		wQy = wQy + "twitterid   TEXT  NOT NULL,"		# 記録したユーザ(Twitter ID)
		wQy = wQy + "regdate     TIMESTAMP,"			# 登録日時
		wQy = wQy + "level       CHAR(2) DEFAULT '-',"	# ログレベル
		wQy = wQy + "log_class   TEXT  NOT NULL,"		# ログクラス
		wQy = wQy + "log_func    TEXT  NOT NULL,"		# ログ関数
		wQy = wQy + "reason      TEXT  NOT NULL,"		# 理由
		wQy = wQy + "id          TEXT "					# ユーザID
		wQy = wQy + " ) ;"
		
		inOBJ_DB.RunQuery( wQy )
		return



#####################################################
# テーブル作成: TBL_FAVOUSER_DATA
#####################################################
	def __create_TBL_FAVOUSER_DATA( self, inOBJ_DB, inTBLname="tbl_favouser_data" ):
		#############################
		# テーブルのドロップ
		wQy = "drop table if exists " + inTBLname + ";"
		inOBJ_DB.RunQuery( wQy )
		
		#############################
		# テーブル枠の作成
		wQy = "create table " + inTBLname + "("
		wQy = wQy + "twitterid     TEXT  NOT NULL,"		# 記録したユーザ(Twitter ID)
		wQy = wQy + "regdate       TIMESTAMP,"			# 登録日時
		wQy = wQy + "upddate       TIMESTAMP,"			# 更新日時(最終)
		wQy = wQy + "flg_save      BOOL  DEFAULT false,"# 自動削除禁止 true=削除しない
		
		wQy = wQy + "id            TEXT  NOT NULL,"		# Twitter ID(数値)
		wQy = wQy + "screen_name   TEXT  NOT NULL,"		# Twitter ユーザ名(英語)
		wQy = wQy + "level_tag     TEXT  NOT NULL,"		# レベルタグ(ユーザの親密度 指標)
		
		wQy = wQy + "send_date     TIMESTAMP,"			# トロフィー送信日時
		wQy = wQy + "send_cnt      INTEGER DEFAULT 0,"	# トロフィー送信回数(累計)
		
		wQy = wQy + "rfavo_id      TEXT  NOT NULL,"		# いいね受信(このユーザがいいねした) ツイートID
		wQy = wQy + "rfavo_date    TIMESTAMP,"			# いいね受信日時
		wQy = wQy + "rfavo_cnt     INTEGER DEFAULT 0,"	# いいね受信回数(総数)
		wQy = wQy + "rfavo_n_cnt   INTEGER DEFAULT 0,"	# いいね受信回数(今周)
		
		wQy = wQy + "pfavo_id      TEXT  NOT NULL,"		# いいね送信(このユーザのツイート) ツイートID
		wQy = wQy + "pfavo_date    TIMESTAMP, "			# いいね送信日時
		wQy = wQy + "pfavo_cnt     INTEGER DEFAULT 0,"	# いいね送信回数(総数)
		
		wQy = wQy + "list_ind_date TIMESTAMP,"			# リスト通知日時
		
		wQy = wQy + "myfollow      BOOL  DEFAULT false,"# フォロー者 true=フォロー者
		wQy = wQy + "myfollow_date TIMESTAMP, "			# フォロー日時
		wQy = wQy + "follower      BOOL  DEFAULT false,"# フォロワー(被フォロー) true=フォロワー
		wQy = wQy + "follower_date TIMESTAMP, "			# 被フォロー日時
		wQy = wQy + "memo          TEXT, "				# 自由記載(メモ)
		wQy = wQy + "renfavo_cnt   INTEGER DEFAULT 0 "	# 連ファボカウント
###		wQy = wQy + "renbot_cnt    INTEGER DEFAULT 0 "	# 非絡み回数
		wQy = wQy + " ) ;"
		
		inOBJ_DB.RunQuery( wQy )
		return



#####################################################
# テーブル作成: TBL_LIST_FAVO
#####################################################
	def __create_TBL_LIST_FAVO( self, inOBJ_DB, inTBLname="tbl_list_favo" ):
		#############################
		# テーブルのドロップ
		wQy = "drop table if exists " + inTBLname + ";"
		inOBJ_DB.RunQuery( wQy )
		
		#############################
		# テーブル枠の作成
		wQy = "create table " + inTBLname + "("
		wQy = wQy + "twitterid   TEXT  NOT NULL,"		# 記録したユーザ(Twitter ID)
		wQy = wQy + "id          TEXT  NOT NULL,"		# Listのid
		wQy = wQy + "list_name   TEXT  NOT NULL,"		# Listの名前
		wQy = wQy + "user_id     TEXT  NOT NULL,"		# Listのユーザのid
		wQy = wQy + "screen_name TEXT  NOT NULL,"		# Listのユーザのscreen_name
		wQy = wQy + "valid       BOOL  DEFAULT true,"	# 有効か True=有効
		wQy = wQy + "follow      BOOL  DEFAULT false, "	# フォロー者、フォロワーを含める
		wQy = wQy + "caution     BOOL  DEFAULT false, "	# リストフォロー時警告を出す
		wQy = wQy + "sensitive   BOOL  DEFAULT false, "	# センシティブツイートを含める
		wQy = wQy + "auto_rem    BOOL  DEFAULT false "	# 自動リムーブ有効
		wQy = wQy + " ) ;"
		
		inOBJ_DB.RunQuery( wQy )
		return



#####################################################
# テーブル作成: TBL_EXC_WORD
#####################################################
	def __create_TBL_EXC_WORD( self, inOBJ_DB, inTBLname="tbl_exc_word" ):
		#############################
		# テーブルのドロップ
		wQy = "drop table if exists " + inTBLname + ";"
		inOBJ_DB.RunQuery( wQy )
		
		#############################
		# テーブル枠の作成
		wQy = "create table " + inTBLname + "("
		wQy = wQy + "regdate     TIMESTAMP,"			# 登録日時
		wQy = wQy + "word        TEXT  NOT NULL, "		# 禁止ワード
		wQy = wQy + "report      BOOL  DEFAULT false,"	# 通報対象か True=対象
		wQy = wQy + " PRIMARY KEY ( word ) ) ;"
		
		inOBJ_DB.RunQuery( wQy )
		return



#####################################################
# テーブル作成: TBL_EXC_PROF
#####################################################
	def __create_TBL_EXC_PROF( self, inOBJ_DB, inTBLname="tbl_exc_prof" ):
		#############################
		# テーブルのドロップ
		wQy = "drop table if exists " + inTBLname + ";"
		inOBJ_DB.RunQuery( wQy )
		
		#############################
		# テーブル枠の作成
		wQy = "create table " + inTBLname + "("
		wQy = wQy + "regdate     TIMESTAMP,"			# 登録日時
		wQy = wQy + "word        TEXT  NOT NULL, "		# 禁止ワード
		wQy = wQy + "report      BOOL  DEFAULT false,"	# 通報対象か True=対象
		wQy = wQy + " PRIMARY KEY ( word ) ) ;"
		
		inOBJ_DB.RunQuery( wQy )
		return



#####################################################
# テーブル作成: TBL_EXC_USER
#####################################################
	def __create_TBL_EXC_USER( self, inOBJ_DB, inTBLname="tbl_exc_user" ):
		#############################
		# テーブルのドロップ
		wQy = "drop table if exists " + inTBLname + ";"
		inOBJ_DB.RunQuery( wQy )
		
		#############################
		# テーブル枠の作成
		wQy = "create table " + inTBLname + "("
		wQy = wQy + "regdate     TIMESTAMP,"			# 登録日時
		wQy = wQy + "id          TEXT  NOT NULL, "		# Twitter ID(数値)
		wQy = wQy + "screen_name TEXT  NOT NULL, "		# Twitter ユーザ名(英語)
		wQy = wQy + "report      BOOL  DEFAULT false,"	# 通報対象 True=対象
		wQy = wQy + "vip         BOOL  DEFAULT false,"	# VIP扱い  True=VIP
		wQy = wQy + "ope         BOOL  DEFAULT false,"	# リアクション監視  True=監視ON
		wQy = wQy + "follow      BOOL  DEFAULT false,"	# フォロー監視(Mainフォローしてるか)  True=監視ON
		wQy = wQy + "rel_date    TIMESTAMP,"			# 禁止解除日時 (noneは自動解除しない)
		wQy = wQy + "memo        TEXT, "				# 自由記載(メモ)
		wQy = wQy + " PRIMARY KEY ( id ) ) ;"
		
		inOBJ_DB.RunQuery( wQy )
		return



#####################################################
# テーブル作成: TBL_CAUTION_TWEET
#####################################################
	def __create_TBL_CAUTION_TWEET( self, inOBJ_DB, inTBLname="tbl_caution_tweet" ):
		#############################
		# テーブルのドロップ
		wQy = "drop table if exists " + inTBLname + ";"
		inOBJ_DB.RunQuery( wQy )
		
		#############################
		# テーブル枠の作成
		wQy = "create table " + inTBLname + "("
		wQy = wQy + "twitterid   TEXT  NOT NULL,"		# Twitter ID(数値)
		wQy = wQy + "regdate     TIMESTAMP,"			# 登録日時
		wQy = wQy + "tweet_id    TEXT  NOT NULL,"		# ツイートID(数値)
		wQy = wQy + "id          TEXT  NOT NULL,"		# Twitter ID(数値)
		wQy = wQy + "screen_name TEXT  NOT NULL "		# Twitter ユーザ名(英語)
		wQy = wQy + " ) ;"
		
		inOBJ_DB.RunQuery( wQy )
		return



#####################################################
# テーブル作成: TBL_SEARCH_WORD
#####################################################
	def __create_TBL_SEARCH_WORD( self, inOBJ_DB, inTBLname="tbl_search_word" ):
		#############################
		# テーブルのドロップ
		wQy = "drop table if exists " + inTBLname + ";"
		inOBJ_DB.RunQuery( wQy )
		
		#############################
		# テーブル枠の作成
		wQy = "create table " + inTBLname + "("
		wQy = wQy + "twitterid   TEXT  NOT NULL,"		# Twitter ID(数値)
		wQy = wQy + "regdate     TIMESTAMP,"			# 登録日時
		wQy = wQy + "upddate     TIMESTAMP,"			# 検索実行日時
		wQy = wQy + "valid       BOOL  DEFAULT false, "	# 有効 True=有効
		wQy = wQy + "word        TEXT  NOT NULL, "		# 検索ワード(キー)
		wQy = wQy + "hit_cnt     INTEGER DEFAULT 0,"	# 検索ヒット数
		wQy = wQy + "favo_cnt    INTEGER DEFAULT 0, "	# いいね数
		wQy = wQy + "auto_follow BOOL  DEFAULT false "	# 自動フォロー True=有効
		wQy = wQy + " ) ;"
		
		inOBJ_DB.RunQuery( wQy )
		return



#####################################################
# テーブル作成: TBL_TRAFFIC_DATA
#####################################################
	def __create_TBL_TRAFFIC_DATA( self, inOBJ_DB, inTBLname="tbl_traffic_data" ):
		#############################
		# テーブルのドロップ
		wQy = "drop table if exists " + inTBLname + ";"
		inOBJ_DB.RunQuery( wQy )
		
		#############################
		# テーブル枠の作成
		wQy = "create table " + inTBLname + "("
		wQy = wQy + "twitterid   TEXT  NOT NULL,"		# Twitter ID(数値)
		wQy = wQy + "regdate     TIMESTAMP,"			# 登録日時
		wQy = wQy + "upddate     TIMESTAMP,"			# 記録日時(更新)
		wQy = wQy + "day         TEXT  NOT NULL,"		# 記録日
		wQy = wQy + "run         INTEGER DEFAULT 0,"	# bot実行回数
		wQy = wQy + "run_time    NUMERIC DEFAULT 0,"	# 実行時間
		
		wQy = wQy + "run_api     INTEGER DEFAULT 0,"	# api実行回数
		wQy = wQy + "run_ope     INTEGER DEFAULT 0,"	# 自動監視実施回数
		
		###### Twittterトラヒック
		wQy = wQy + "timeline    INTEGER DEFAULT 0,"	# タイムライン取得数(ライン数)
		
		wQy = wQy + "myfollow    INTEGER DEFAULT 0,"	# フォロー者数(報告時)
		wQy = wQy + "p_myfollow  INTEGER DEFAULT 0,"	# フォロー実施数
		wQy = wQy + "d_myfollow  INTEGER DEFAULT 0,"	# リムーブ実施数
		
		wQy = wQy + "follower    INTEGER DEFAULT 0,"	# フォロワー数(報告時)
		wQy = wQy + "p_follower  INTEGER DEFAULT 0,"	# フォロワー獲得数
		wQy = wQy + "d_follower  INTEGER DEFAULT 0,"	# 被リムーブ者数
		
		wQy = wQy + "r_reaction  INTEGER DEFAULT 0,"	# リアクション受信回数(総数)
		wQy = wQy + "r_rep       INTEGER DEFAULT 0,"	# リプライ受信回数
		wQy = wQy + "r_retweet   INTEGER DEFAULT 0,"	# リツイート受信回数
		wQy = wQy + "r_iret      INTEGER DEFAULT 0,"	# 引用リツイート受信回数
		wQy = wQy + "r_favo      INTEGER DEFAULT 0,"	# いいね受信回数
		wQy = wQy + "r_in        INTEGER DEFAULT 0,"	# フォロワーからのアクション受信回数
		wQy = wQy + "r_out       INTEGER DEFAULT 0,"	# フォロワー以外からのアクション受信回数
		wQy = wQy + "r_vip       INTEGER DEFAULT 0,"	# VIP監視アクション受信回数
		
		wQy = wQy + "s_run       INTEGER DEFAULT 0,"	# 検索実施数
		wQy = wQy + "s_hit       INTEGER DEFAULT 0,"	# 検索ヒット数
		wQy = wQy + "s_favo      INTEGER DEFAULT 0,"	# 検索時いいね数
		
		wQy = wQy + "favo        INTEGER DEFAULT 0,"	# いいね数
		wQy = wQy + "p_favo      INTEGER DEFAULT 0,"	# いいね実施回数
		wQy = wQy + "d_favo      INTEGER DEFAULT 0,"	# いいね解除回数
		wQy = wQy + "p_tweet     INTEGER DEFAULT 0,"	# ツイート送信回数
		
		###### DBトラヒック
		wQy = wQy + "db_req INTEGER DEFAULT 0,"			# DB select回数
		wQy = wQy + "db_ins INTEGER DEFAULT 0,"			# DB insert回数
		wQy = wQy + "db_up  INTEGER DEFAULT 0,"			# DB update回数
		wQy = wQy + "db_del INTEGER DEFAULT 0 "			# DB delete回数
		wQy = wQy + " ) ;"
		
		inOBJ_DB.RunQuery( wQy )
		return



