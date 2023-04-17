#!/usr/bin/python
# coding: UTF-8
#####################################################
# ::Project  : Korei Bot Win
# ::Admin    : Korei (@korei-xlix)
# ::github   : https://github.com/korei-xlix/koreibot_win/
# ::Class    : ログ処理
#####################################################
# 書式:
#	A :	gVal.OBJ_L.Log( "A", wRes )				致命的エラー: プログラム停止 ロジックエラーなどソフト側の問題
#	B :	gVal.OBJ_L.Log( "B", wRes )				内部的エラー: プログラム停止か実行不可 コール先からのエラー
#	C :	gVal.OBJ_L.Log( "C", wRes )				外部のエラー: プログラム停止か実行不可 外部モジュールやハードの問題
#	D :	gVal.OBJ_L.Log( "D", wRes )				潜在的エラー: ユーザ入力など予想外 or 後に問題を起こす可能性がある
#	E :	gVal.OBJ_L.Log( "E", wRes )				不明なエラー: 判断がつかないエラー ありえないルートなど
#
#	S:	gVal.OBJ_L.Log( "S", wRes, "<理由>" )	システム    : botの実行、停止、再起動
#	SC:	gVal.OBJ_L.Log( "SC", wRes, "<理由>" )	システム    : システムの設定変更
#	SR:	gVal.OBJ_L.Log( "SR", wRes, "<理由>" )	システム    : システムの規制制御、自律制御
#	R:	gVal.OBJ_L.Log( "R", wRes, "<理由>" )	ユーザ      : ユーザ登録、削除、抹消
#	RC:	gVal.OBJ_L.Log( "RC", wRes, "<理由>" )	ユーザ      : ユーザ設定変更
#	RR:	gVal.OBJ_L.Log( "RR", wRes, "<理由>" )	ユーザ      : ユーザ個別の規制制御、自律制御
#	T:	gVal.OBJ_L.Log( "T", wRes, "<理由>" )	トラヒック  : システムトラヒック、期間トラヒック、通信トラヒック(統計)
#
#	P :	gVal.OBJ_L.Log( "P", wRes )				データベース操作
#	N :	gVal.OBJ_L.Log( "N", wRes, "<理由>" )	非表示の情報
#	X :	gVal.OBJ_L.Log( "X", wRes )				テスト用ログ
#
#####################################################

from osif import CLS_OSIF
from filectrl import CLS_File
from gval import gVal
#####################################################
class CLS_Mylog():
#####################################################

#############################
# ログレベル 日本語ローカライズ
	DEF_STR_LEVEL = {
		"A"			: "",
		"B"			: "",
		"C"			: "",
		"D"			: "",
		"E"			: "",
		
		"S"			: "",
		"SC"		: "",
		"SR"		: "",
		"R"			: "",
		"RC"		: "",
		"RR"		: "",
		"T"			: "",
		
		"P"			: "",
		"N"			: "",
		"X"			: "",
		
		"0"			: "",
		"(dummy)"	: ""
	}

#############################
# ログ表示モード
	DEF_STR_VIEW_LEVEL = {
		"F"			: "",		# 全ログ
		"A"			: "",		# 全ログ(期間)
		"V"			: "",		# 運用ログ
		"R"			: "",		# 運用ログ(操作のみ)
		"T"			: "",		# トラヒック
		"U"			: "",		# ユーザログ
		"E"			: "",		# 異常ログ
		"(dummy)"	: ""
	}

	DEF_VIEW_CONSOLE = True		#デフォルトのコンソール表示
	DEF_OUT_FILE     = False	#デフォルトのファイル出力
	DEF_LEVEL_SIZE   = 2



#####################################################
# ロギング
#####################################################
###	def Log( self, inLevel, inRes, inText=None, inARR_Data=[], inViewConsole=DEF_VIEW_CONSOLE, inOutFile=DEF_OUT_FILE ):
	def Log( self, inLevel, inRes, inText=None, inARR_Data=[], inID=None, inViewConsole=DEF_VIEW_CONSOLE, inOutFile=DEF_OUT_FILE ):
		#############################
		# ログ文字セット
		wSTR_Log = {
			"LogClass" : None,
			"LogFunc"  : None,
			"Reason"   : None }
		
		#############################
		# ログレベルのチェック
		wLevel = inLevel
		if wLevel==None or wLevel=="" :
			wLevel = "0"
		###大文字変換
		try:
			wLevel = wLevel.upper()
		except ValueError as err :
			wLevel = "0"
		###定義チェック
		if wLevel not in self.DEF_STR_LEVEL :
			wLevel = "0"
		
		#############################
		# ログクラスのチェック
		if "Class" not in inRes :
			wLogClass = "(none)"
		else:
			wLogClass = inRes['Class']
		
		if wLogClass==None or wLogClass=="" :
			wLogClass = "(none)"
		
		#############################
		# ログファンクのチェック
		if "Func" not in inRes :
			wLogFunc = "(none)"
		else:
			wLogFunc = inRes['Func']
		
		if wLogFunc==None or wLogFunc=="" :
			wLogFunc = "(none)"
		
		#############################
		# 理由のチェック
		if inText!=None :
			wReason = str( inText )
		elif "Reason" not in inRes :
			wReason = "(none)"
		else:
			wReason = str( inRes['Reason'] )
		
		if wReason=="None" or wReason=="" :
			wReason = "(none)"
		### ' を　'' に置き換える
		wReason = wReason.replace( "'", "''" )
		
		#############################
		# 構造体に突っ込む
		wSTR_Log['LogClass'] = wLogClass
		wSTR_Log['LogFunc'] = wLogFunc
		wSTR_Log['Reason'] = wReason
		
		#############################
		# 時間を取得
		wTD = CLS_OSIF.sGetTime()
		### wTD['TimeDate']
		if wTD['Result']!=True :
			###時間取得失敗  時計壊れた？
			CLS_OSIF.sPrn( "CLS_Mylog: Log: PC時間の取得に失敗しました" )
			wCHR_TimeDate = "1901-01-01 00:00:00"
			
			###いちおデータベースにも記録する
			wQy = "insert into tbl_log_data values ("
			wQy = wQy + "'" + gVal.STR_UserInfo['Account'] + "',"
			wQy = wQy + "'" + wCHR_TimeDate + "',"
			wQy = wQy + "'C',"
			wQy = wQy + "'CLS_Mylog',"
			wQy = wQy + "'Log',"
			wQy = wQy + "'CLS_OSIF.sGetTime is failed' "
			wQy = wQy + ") ;"
			
			wResDB = gVal.OBJ_DB_IF.RunQuery( wQy, False )
			if wResDB['Result']!=True :
				wRes['Reason'] = "Run Query is failed"
				gVal.OBJ_L.Log( "C", wRes )
		
		else:
			wCHR_TimeDate = str(wTD['TimeDate'])
		
		#############################
		# データベースに記録する
		wQy = "insert into tbl_log_data values ("
		wQy = wQy + "'" + gVal.STR_UserInfo['Account'] + "',"
		wQy = wQy + "'" + wCHR_TimeDate + "',"
		wQy = wQy + "'" + wLevel + "',"
		wQy = wQy + "'" + wSTR_Log['LogClass'] + "',"
		wQy = wQy + "'" + wSTR_Log['LogFunc'] + "',"
		wQy = wQy + "'" + wSTR_Log['Reason'] + "' "
		if (wLevel=="R" or wLevel=="RC" or wLevel=="RR" ) and inID!=None :
			wQy = wQy + ", '" + str(inID) + "' "
		wQy = wQy + ") ;"
		
		wResDB = gVal.OBJ_DB_IF.RunQuery( wQy, False )
		if wResDB['Result']!=True :
			wRes['Reason'] = "Run Query is failed"
			gVal.OBJ_L.Log( "C", wRes )
			##以後の記録処理は継続する
		
		#############################
		# ログの組み立て
		if wLevel=="A" or wLevel=="B" or wLevel=="C" or wLevel=="D" or wLevel=="E" :
			wLevelTag = "*" + wLevel
		else:
			wNumSpace = self.DEF_LEVEL_SIZE - len( wLevel )
			wLevelTag = wLevel + " " * wNumSpace
		
		if ( wLevel=="S" or wLevel=="SC" or wLevel=="SR" or \
		     wLevel=="R" or wLevel=="RC" or wLevel=="RR" or \
		     wLevel=="T" or wLevel=="N" ) \
		   and inText!=None :
			wOutLog = wLevelTag + ": " + wSTR_Log['Reason']
		else:
			wOutLog = wLevelTag + ": "
			wOutLog = wOutLog + wSTR_Log['LogClass'] + ": "
			wOutLog = wOutLog + wSTR_Log['LogFunc'] + ": "
			wOutLog = wOutLog + wSTR_Log['Reason']
		
		#############################
		# データの組み立て
		wData = []
		if len(inARR_Data)>0 :
			###ブランク文字
			wBlank = " " * len( wCHR_TimeDate )
			###データのセット
			for wLine in inARR_Data :
				wIncLine = wBlank + ' ' + wLine + '\n'
				wData.append( wIncLine )
		
		#############################
		# コンソールに表示する
		# = システムログに出る
		wFLG_View = False
		
		### A・B・X（致命的エラー・テストログ）
		###   =表示
		if wLevel=="A" or wLevel=="B" or wLevel=="X" :
			wFLG_View = True
		
		### S・SC・SR・TS（運用ログ・トラヒック）
		###   =テキストが設定されていれば表示
		elif wLevel=="S" or wLevel=="SC" or wLevel=="SR" or wLevel=="T" :
			if  inText!=None :
				wFLG_View = True
		
		### R・RC・RR（ユーザ操作）
		###   =表示
		elif wLevel=="R" or wLevel=="RC" or wLevel=="RR" :
			wFLG_View = True
		
		### P・N（データベース操作・非表示の情報）
		###   =非表示
		elif wLevel=="P" or wLevel=="N" :
			wFLG_View = False
		
		### その他はコントロールオプションに従う
		else :
			if inViewConsole==True :
				wFLG_View = True
		
		if wFLG_View==True :
			CLS_OSIF.sPrn( wOutLog )
			for wLineData in wData :
				CLS_OSIF.sPrn( wLineData )
		
		#############################
		# ファイル書き出し
		if inOutFile==True :
			wFileRes = self.__writeFile( wCHR_TimeDate, wOutLog, wData )
		
		return wOutLog



#####################################################
# ファイルへの書き出し
#####################################################
	def __writeFile( self, inTimeDate, inLog, inARR_Data=[] ):
		#############################
		# ユーザフォルダの存在チェック
		wLogPath = gVal.DEF_STR_FILE['LogBackup_path']
		if CLS_File.sExist( wLogPath )!=True :
			###フォルダがなければ諦める
			return False
		
		#############################
		# ログフォルダの作成
		if CLS_File.sExist( wLogPath )!=True :
			###まだ未生成なら諦める
			return False
		
		#############################
		# ファイル名、フルパスの生成
		wFilePath = inTimeDate.split(" ")
		wFilePath_Date = wFilePath[0]
		wFilePath_Date = wFilePath_Date.replace( "-", "" )
		wFilePath_Time = wFilePath[1]
		wFilePath_Time = wFilePath_Time.replace( ":", "" )
		
		wFilePath = wFilePath_Date + "_" + wFilePath_Time + ".log"
		wLogPath = wLogPath + "/" + wFilePath
		
		wSetLine = []
		#############################
		# 1行目
		wLine = inTimeDate + ' ' + inLog + '\n'
		wSetLine.append( wLine )
		
		#############################
		# 2行目以降
		if len(inARR_Data)>0 :
			for wLineData in inARR_Data :
				wSetLine.append( wLineData )
		
		#############################
		# ファイル追加書き込み
		wRes = CLS_File.sAddFile( wLogPath, wSetLine, inExist=False )
		if wRes!=True :
			###失敗
			return False
		
		return True



#####################################################
# ログの表示
#####################################################
	def View( self, inShortMode=True, inViewMode="A" ):
		#############################
		# 運用モード
		wViewMode = inViewMode.upper()
		if inViewMode not in self.DEF_STR_VIEW_LEVEL :
			wViewMode = "A"
		###大文字変換
		try:
			wViewMode = wViewMode.upper()
		except ValueError as err :
			wViewMode = "A"
		
		#############################
		# 画面クリア
		CLS_OSIF.sDispClr()
		
		#############################
		# ヘッダ表示
		wStr = "--------------------" + '\n'
		wStr = wStr + " ログの表示" + '\n'
		wStr = wStr + "--------------------" + '\n'
		CLS_OSIF.sPrn( wStr )
		
		#############################
		# ログ取得
		### wViewMode=V 運用ログ
		if wViewMode=="V" :
			wQy = "select * from tbl_log_data where "
			wQy = wQy + "twitterid = '" + gVal.STR_UserInfo['Account'] + "' and "
			wQy = wQy + "( "
			wQy = wQy + "level = 'S' or "
			wQy = wQy + "level = 'SC' or "
			wQy = wQy + "level = 'SR' or "
			wQy = wQy + "level = 'RR' or "
			wQy = wQy + "level = 'T' or "
			wQy = wQy + "level = 'P' or "
			wQy = wQy + "level = 'N' "
			wQy = wQy + ") and "
			wQy = wQy + "( regdate > now() - interval '2 week' ) "
			wQy = wQy + "order by regdate DESC ;"
		
		### wViewMode=R 運用ログ(操作のみ)
		if wViewMode=="R" :
			wQy = "select * from tbl_log_data where "
			wQy = wQy + "twitterid = '" + gVal.STR_UserInfo['Account'] + "' and "
			wQy = wQy + "( "
			wQy = wQy + "level = 'S' or "
			wQy = wQy + "level = 'SC' or "
			wQy = wQy + "level = 'SR' or "
			wQy = wQy + "level = 'RR' or "
			wQy = wQy + "level = 'N' "
			wQy = wQy + ") and "
			wQy = wQy + "( regdate > now() - interval '2 week' ) "
			wQy = wQy + "order by regdate DESC ;"
		
		### wViewMode=T トラヒック
		if wViewMode=="T" :
			wQy = "select * from tbl_log_data where "
			wQy = wQy + "twitterid = '" + gVal.STR_UserInfo['Account'] + "' and "
			wQy = wQy + "level = 'T' and "
			wQy = wQy + "( regdate > now() - interval '2 week' ) "
			wQy = wQy + "order by regdate DESC ;"
		
		### wViewMode=E 異常ログ
		elif wViewMode=="E" :
			wQy = "select * from tbl_log_data where "
			wQy = wQy + "twitterid = '" + gVal.STR_UserInfo['Account'] + "' and "
			wQy = wQy + "( "
			wQy = wQy + "level = 'A' or "
			wQy = wQy + "level = 'B' or "
			wQy = wQy + "level = 'C' or "
			wQy = wQy + "level = 'D' or "
			wQy = wQy + "level = 'E' or "
			wQy = wQy + "level = 'X' or "
			wQy = wQy + "level = '0' "
			wQy = wQy + ") and "
			wQy = wQy + "( regdate > now() - interval '2 week' ) "
			wQy = wQy + "order by regdate DESC ;"
		
		### wViewMode=U ユーザ操作ログ
		elif wViewMode=="U" :
			wQy = "select * from tbl_log_data where "
			wQy = wQy + "twitterid = '" + gVal.STR_UserInfo['Account'] + "' and "
			wQy = wQy + "( "
			wQy = wQy + "level = 'R' or "
			wQy = wQy + "level = 'RC' "
			wQy = wQy + ") and "
			wQy = wQy + "( regdate > now() - interval '2 week' ) "
			wQy = wQy + "order by regdate DESC ;"
		
		### wViewMode=F 全ログ
		elif wViewMode=="F" :
			wQy = "select * from tbl_log_data where "
			wQy = wQy + "twitterid = '" + gVal.STR_UserInfo['Account'] + "' "
			wQy = wQy + "order by regdate DESC ;"
		
		### wViewMode=A 全ログ(期間)
		else:
			wQy = "select * from tbl_log_data where "
			wQy = wQy + "twitterid = '" + gVal.STR_UserInfo['Account'] + "' and "
			wQy = wQy + "( regdate > now() - interval '2 week' ) "
			wQy = wQy + "order by regdate DESC ;"
		
		wResDB = gVal.OBJ_DB_IF.RunQuery( wQy, False )
		if wResDB['Result']!=True :
			wRes['Reason'] = "Run Query is failed"
			gVal.OBJ_L.Log( "B", wRes )
			return False
		
		#############################
		# 辞書型に整形
		wARR_Log = gVal.OBJ_DB_IF.ChgDict( wResDB['Responce'] )
		
		#############################
		# ログ表示長のセット
		wOutLen = len(wARR_Log)
		if wOutLen==0 :
			wStr = "ログがありません。処理を中止します。" + '\n'
			CLS_OSIF.sPrn( wStr )
			return True
		
###		if inShortMode==True :
		if inShortMode==True and  wViewMode!="F" :
			wOutLen = gVal.DEF_STR_TLNUM['logShortLen']
		
		#############################
		# ログ表示
		wKeylist = wARR_Log.keys()
		wIndex = 0
		for wKey in wKeylist :
			wTD    = str(wARR_Log[wKey]['regdate'])
			wBlank = " " * len( wTD ) + " "
			
			if wViewMode=="U" :
				### ユーザ記録
				wLine = wTD + " " + wARR_Log[wKey]['reason']
				CLS_OSIF.sPrn( wLine )
			else:
				### ユーザ記録以外
				wLine = wTD + " " + wARR_Log[wKey]['level'] + " "
				wLine = wLine + "[" + wARR_Log[wKey]['log_class'] + "] "
				wLine = wLine + "[" + wARR_Log[wKey]['log_func'] + "]"
				CLS_OSIF.sPrn( wLine )
				
				wLine = wBlank + wARR_Log[wKey]['reason']
				CLS_OSIF.sPrn( wLine )
			
			wIndex += 1
			if wOutLen<=wIndex :
				break
		
		return True

#############################
#	twitterid   TEXT  NOT NULL
#	level       CHAR(1) DEFAULT '-'
#	log_class   TEXT  NOT NULL
#	log_func    TEXT  NOT NULL
#	reason      TEXT  NOT NULL
#	regdate     TIMESTAMP
#############################



#####################################################
# 個別ログ取得
#####################################################
	def GetLog( self, inID ):
		wARR_Log = {}
		
		#############################
		# データベースを取得
		wQy = "select * from tbl_log_data "
#		wQy = wQy + "where ( level = 'R' or level = 'RC' or level = 'RR' ) and "
#		wQy = wQy + "id = " + str(inID) + " and "
		wQy = wQy + "where id = '" + str(inID) + "' and "
		wQy = wQy + "twitterid = '" + gVal.STR_UserInfo['Account'] + "' "
		wQy = wQy + "order by regdate DESC ;"
		
		wResDB = gVal.OBJ_DB_IF.RunQuery( wQy )
		if wResDB['Result']!=True :
			##失敗
			wRes['Reason'] = "Run Query is failed(1): RunFunc=" + wResDB['RunFunc'] + " reason=" + wResDB['Reason'] + " query=" + wResDB['Query']
			gVal.OBJ_L.Log( "C", wRes )
			return wRes
		
		#############################
		# 辞書型に整形
		wARR_DBData = gVal.OBJ_DB_IF.ChgDict( wResDB['Responce'] )
		
		wKeylist = list( wARR_DBData.keys() )
		for wIndex in wKeylist :
			wLevel = wARR_DBData[wIndex]['level']
			wNumSpace = self.DEF_LEVEL_SIZE - len( wLevel )
			wLevelTag = wLevel + " " * wNumSpace
			
			wCell = {
				"regdate"	: str(wARR_DBData[wIndex]['regdate']),
				"level"		: wLevelTag,
				"log_class"	: wARR_DBData[wIndex]['log_class'],
				"log_func"	: wARR_DBData[wIndex]['log_func'],
				"reason"	: wARR_DBData[wIndex]['reason']
			}
			wARR_Log.update({ wIndex : wCell })
		
		return wARR_Log



#####################################################
# ログクリア
#####################################################
	def Clear( self, inAllClear=False ):
		#############################
		# 時間を取得
		wTD = CLS_OSIF.sGetTime()
		if wTD['Result']!=True :
			###時間取得失敗  時計壊れた？
			CLS_OSIF.sPrn( "CLS_Mylog: Clear: PC時間の取得に失敗しました" )
			return False
		wTimeDate = str(wTD['TimeDate'])
		
		#############################
		# 画面クリア
		CLS_OSIF.sDispClr()
		
		#############################
		# ヘッダ表示
		wStr = "--------------------" + '\n'
		wStr = wStr + " ログ退避中" + '\n'
		wStr = wStr + "--------------------" + '\n'
		CLS_OSIF.sPrn( wStr )
		
		#############################
		# 実行の確認
		wStr = "データベースのログを全てファイルに退避したあと、全てクリアします。" + '\n'
		CLS_OSIF.sPrn( wStr )
		wSelect = CLS_OSIF.sInp( "よろしいですか？(y/N)=> " )
		if wSelect!="y" :
			##キャンセル
			CLS_OSIF.sPrn( "中止しました。" )
			return True
		
		#############################
		# 全ログ取得
		wQy = "select * from tbl_log_data where " + \
					"twitterid = '" + gVal.STR_UserInfo['Account'] + "' " + \
					"order by regdate ;"
		
		wResDB = gVal.OBJ_DB_IF.RunQuery( wQy, False )
		if wResDB['Result']!=True :
			wRes['Reason'] = "Run Query is failed"
			gVal.OBJ_L.Log( "B", wRes )
			return False
		
		#############################
		# 辞書型に整形
		wARR_Log = gVal.OBJ_DB_IF.ChgDict( wResDB['Responce'] )
		
		#############################
		# ログ表示長のセット
		wOutLen = len(wARR_Log)
		if wOutLen==0 :
			wStr = "ログがありません。処理を中止します。" + '\n'
			CLS_OSIF.sPrn( wStr )
			return True
		
		wARR_Output = []
		#############################
		# 出力組み立て
		wKeylist = wARR_Log.keys()
		for wKey in wKeylist :
			wTD    = str(wARR_Log[wKey]['regdate'])
			wBlank = " " * len( wTD ) + " "
			
			wLine = wTD + "," + wARR_Log[wKey]['level'] + ","
			wLine = wLine + wARR_Log[wKey]['log_class'] + ","
			wLine = wLine + wARR_Log[wKey]['log_func'] + ","
			wLine = wLine + wARR_Log[wKey]['reason'] + "," + '\n'
			wARR_Output.append( wLine )
		
		#############################
		# ログ出力
		self.__writeLogFile( wTimeDate, inARR_Data=wARR_Output )
		
		#############################
		# ログ消去
		if inAllClear==True :
			### 全ログ消去
			wQy = "delete from tbl_log_data where "
			wQy = wQy + "twitterid = '" + gVal.STR_UserInfo['Account'] + "' "
			wQy = wQy + ";"
		else:
			### エラーと運用のみクリア
			wQy = "delete from tbl_log_data where "
			wQy = wQy + "twitterid = '" + gVal.STR_UserInfo['Account'] + "' and "
			wQy = wQy + "("
			wQy = wQy + "not level = 'R' and "
			wQy = wQy + "not level = 'RC' ) "
			wQy = wQy + ";"
		
		wResDB = gVal.OBJ_DB_IF.RunQuery( wQy, False )
		if wResDB['Result']!=True :
			wRes['Reason'] = "Run Query is failed"
			gVal.OBJ_L.Log( "B", wRes )
			return False
		
		#############################
		# 結果表示
		wStr = "データベースのログを全てクリアしました。" + '\n'
		CLS_OSIF.sPrn( wStr )
		return True



#####################################################
# ログ退避 書き出し
#####################################################
	def __writeLogFile( self, inTimeDate, inARR_Data=[] ):
		#############################
		# ログフォルダの作成
		wLogPath = gVal.DEF_STR_FILE['LogBackup_path']
		if CLS_File.sExist( wLogPath )!=True :
			###まだ未生成なら作成する
			if CLS_File.sMkdir( wLogPath )!=True :
				###作れなければ諦める
				return False
		
		#############################
		# ファイル名、フルパスの生成
		wFilePath = inTimeDate.split(" ")
		wFilePath_Date = wFilePath[0]
		wFilePath_Date = wFilePath_Date.split("-")
		
		wFilePath = wFilePath_Date[0] + wFilePath_Date[1] + ".csv"
		wLogPath = wLogPath + "/" + wFilePath
		
		#############################
		# ファイル追加書き込み
		wRes = CLS_File.sAddFile( wLogPath, inARR_Data, inExist=False )
		if wRes!=True :
			###失敗
			return False
		
		wStr = "ログをファイルに退避しました: " + wFilePath
		CLS_OSIF.sPrn( wStr )
		
		return True



