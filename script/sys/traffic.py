#!/usr/bin/python
# coding: UTF-8
#####################################################
# ::Project  : Korei Bot Win
# ::Admin    : Korei (@korei-xlix)
# ::github   : https://github.com/korei-xlix/koreibot_win/
# ::Class    : トラヒック
#####################################################

from osif import CLS_OSIF
from mydisp import CLS_MyDisp
from gval import gVal
#####################################################
class CLS_Traffic():
#####################################################
	DEF_KOMOKU_LEN     = 32			#
	DEF_KOMOKU_NUM_LEN = 16			#

#####################################################
# トラヒックセット
#####################################################
	@classmethod
	def sP( cls, inTag, inCnt=1, inFLG_Add=True ):
		#############################
		# 応答形式の取得
		#   "Result" : False, "Class" : None, "Func" : None, "Reason" : None, "Responce" : None
		wRes = CLS_OSIF.sGet_Resp()
		wRes['Class'] = "CLS_Traffic"
		wRes['Func']  = "P"
		
		#############################
		# チェック
		if inTag not in gVal.STR_TrafficInfo :
			wRes['Reason'] = "Tag is not in gVal.STR_TrafficInfo: tag=" + str(inTag)
			gVal.OBJ_L.Log( "A", wRes )
			return wRes
		
		gVal.STR_TrafficInfo['upddate'] = str( gVal.STR_Time['TimeDate'] )
		if inFLG_Add==True :
			gVal.STR_TrafficInfo[inTag][0] += inCnt
		else:
			gVal.STR_TrafficInfo[inTag][0] = inCnt
		
		wRes['Result'] = True
		return wRes



#####################################################
# トラヒック情報の取得
#####################################################
	@classmethod
	def sGet(cls):
		#############################
		# 応答形式の取得
		#   "Result" : False, "Class" : None, "Func" : None, "Reason" : None, "Responce" : None
		wRes = CLS_OSIF.sGet_Resp()
		wRes['Class'] = "CLS_Traffic"
		wRes['Func']  = "Get"
		
		#############################
		# 時間を取得
		wTD = CLS_OSIF.sGetTime()
		if wTD['Result']!=True :
			###時間取得失敗  時計壊れた？
			wRes['Reason'] = "PC time get is failer"
			gVal.OBJ_L.Log( "C", wRes )
			return wRes
		### wTD['TimeDate']
		wARR_TD = str( wTD['TimeDate'] )
		wARR_TD = wARR_TD.split(" ")
		wARR_TD = wARR_TD[0]
		
		#############################
		# DBの今日のトラヒック情報取得
		wQy = "select * from tbl_traffic_data where "
		wQy = wQy + "twitterid = '" + gVal.STR_UserInfo['Account'] + "' "
		wQy = wQy + " and day = '" + wARR_TD + "';"
		
		wResDB = gVal.OBJ_DB_IF.RunQuery( wQy, False )
		if wResDB['Result']!=True :
			wRes['Reason'] = "Run Query is failed"
			gVal.OBJ_L.Log( "C", wRes )
			return wRes
		
		#############################
		# 辞書型に整形
		wARR_RateTraffic = gVal.OBJ_DB_IF.ChgDict( wResDB['Responce'] )
		
		#############################
		# 今日の記録がなければ
		#   =空行を作成する
		if len(wARR_RateTraffic)==0 :
			#############################
			# DBに空行を挿入
			wResIns = cls.sChg( wTD['TimeDate'] )
			if wResIns['Result']!=True :
				##失敗
				wRes['Reason'] = "sChg is failed"
				gVal.OBJ_L.Log( "B", wRes )
				return wRes
		
		#############################
		# 今日の記録があれば
		# [0]を今日とする
		else:
			wARR_RateTraffic = wARR_RateTraffic[0]
			
			wKeylist = list( gVal.STR_TrafficInfo.keys() )
			for wKey in wKeylist :
				if wKey=="upddate" :
					gVal.STR_TrafficInfo[wKey] = wTD['TimeDate']
				else:
					if wKey in wARR_RateTraffic :
						gVal.STR_TrafficInfo[wKey][0] = wARR_RateTraffic[wKey]
					else:
						gVal.STR_TrafficInfo[wKey][0] = 0
		
		#############################
		# 正常終了
		wRes['Result'] = True
		return wRes



#####################################################
# トラヒック切替
#####################################################
	@classmethod
	def sChg( cls, inTimeDate ):
		#############################
		# 応答形式の取得
		#   "Result" : False, "Class" : None, "Func" : None, "Reason" : None, "Responce" : None
		wRes = CLS_OSIF.sGet_Resp()
		wRes['Class'] = "CLS_Traffic"
		wRes['Func']  = "sChg"
		
		#############################
		# 日時だけ取り出し
		wARR_TD = str( inTimeDate )
		wARR_TD = wARR_TD.split(" ")
		wARR_TD = wARR_TD[0]
		
		wKeylist = list( gVal.STR_TrafficInfo.keys() )
		#############################
		# 空行を挿入
		wQy = "insert into tbl_traffic_data values ("
		wQy = wQy + "'" + gVal.STR_UserInfo['Account'] + "', "	# Twitter ID(数値)
		wQy = wQy + "'" + str( inTimeDate ) + "', "		# 登録日時
		wQy = wQy + "'" + str( inTimeDate ) + "', "		# 記録日時(更新)
		wQy = wQy + "'" + str( wARR_TD ) + "', "		# 記録日
		
		for wKey in wKeylist :
			if wKey=="db_req" or wKey=="db_ins" or wKey=="db_up" or wKey=="db_del" or \
			   wKey=="upddate" :
				continue
			wQy = wQy + "0, "
		
		wQy = wQy + "0, 0, 0, 0 "
		wQy = wQy + ") ;"
		
		wResDB = gVal.OBJ_DB_IF.RunQuery( wQy, False )
		if wResDB['Result']!=True :
			wRes['Reason'] = "Run Query is failed"
			gVal.OBJ_L.Log( "C", wRes )
			return wRes
		
		#############################
		# 初期化
		wKeylist = list( gVal.STR_TrafficInfo.keys() )
		for wKey in wKeylist :
			if wKey=="upddate" :
				gVal.STR_TrafficInfo[wKey] = inTimeDate
			else :
				gVal.STR_TrafficInfo[wKey][0] = 0
		
		#############################
		# insert分のトラヒックを計上する
		cls.sP( "db_req" )
		cls.sP( "db_ins" )
		
		#############################
		# トラヒック切替報告
		gVal.OBJ_L.Log( "T", wRes, "トラヒック切替: " + wARR_TD )
		
		#############################
		# 正常終了
		wRes['Result'] = True
		return wRes



#####################################################
# トラヒック情報の記録
#####################################################
	@classmethod
	def sSet(cls):
		#############################
		# 応答形式の取得
		#   "Result" : False, "Class" : None, "Func" : None, "Reason" : None, "Responce" : None
		wRes = CLS_OSIF.sGet_Resp()
		wRes['Class'] = "CLS_Traffic"
		wRes['Func']  = "Set"
		
		wRes['Responce'] = {
			"Chg"	: False,	#トラヒック切替
			"Rep"	: False		#トラヒック報告
		}
		#############################
		# 時間を取得
		wTD = CLS_OSIF.sGetTime()
		if wTD['Result']!=True :
			###時間取得失敗  時計壊れた？
			wRes['Reason'] = "PC time get is failer"
			gVal.OBJ_L.Log( "C", wRes )
			return wRes
		### wTD['TimeDate']
		wARR_NowTD = str( wTD['TimeDate'] )
		wARR_NowTD = wARR_NowTD.split(" ")
		wARR_NowTD = wARR_NowTD[0]
		
		wKeylist = list( gVal.STR_TrafficInfo.keys() )
		#############################
		# 更新
		wQy = "update tbl_traffic_data set "
		for wKey in wKeylist :
			if wKey=="upddate" :
				continue
			wQy = wQy + wKey + " = " + str( gVal.STR_TrafficInfo[wKey][0] ) + ", "
		
		wQy = wQy + "upddate = '" + str( gVal.STR_TrafficInfo['upddate'] ) + "' "
		wQy = wQy + "where twitterid = '" + gVal.STR_UserInfo['Account'] + "'"
		wQy = wQy + " and day = '" + str( wARR_NowTD ) + "' ;"
		
		wResDB = gVal.OBJ_DB_IF.RunQuery( wQy, False )
		if wResDB['Result']!=True :
			wRes['Reason'] = "Run Query is failed"
			gVal.OBJ_L.Log( "C", wRes )
			return wRes
		
		#############################
		# 月が変わったか
		wARR_TD = str( gVal.STR_TrafficInfo['upddate'] )
		wARR_TD = wARR_TD.split(" ")
		wARR_TD = wARR_TD[0]
		
		if wARR_NowTD!=wARR_TD :
			### 月=変わった
			###   DBに空行を挿入
			wResIns = cls.sChg( wTD['TimeDate'] )
			if wResIns['Result']!=True :
				##失敗
				wRes['Reason'] = "sChg is failed"
				gVal.OBJ_L.Log( "B", wRes )
				return wRes
		
		#############################
		# 正常終了
		wRes['Result'] = True
		return wRes



#####################################################
# トラヒック情報を報告する
#####################################################
	@classmethod
	def sReport( cls, inCrear=True ):
		#############################
		# 応答形式の取得
		#   "Result" : False, "Class" : None, "Func" : None, "Reason" : None, "Responce" : None
		wRes = CLS_OSIF.sGet_Resp()
		wRes['Class'] = "CLS_Traffic"
		wRes['Func']  = "sReport"
		
		wRes['Responce'] = False
		#############################
		# 時間を取得
		wTD = CLS_OSIF.sGetTime()
		if wTD['Result']!=True :
			###時間取得失敗  時計壊れた？
			wRes['Reason'] = "PC time get is failer"
			gVal.OBJ_L.Log( "C", wRes )
			return wRes
		### wTD['TimeDate']
		wARR_NowTD = str( wTD['TimeDate'] )
		wARR_NowTD = wARR_NowTD.split(" ")
		wARR_NowTD = wARR_NowTD[0]
		
		#############################
		# DBのトラヒック情報取得
		wQy = "select * from tbl_traffic_data where "
		wQy = wQy + "twitterid = '" + gVal.STR_UserInfo['Account'] + "' "
		wQy = wQy + " order by day desc "
		wQy = wQy + " limit " + str(gVal.DEF_STR_TLNUM['trafficReportLimit']) + "; "
		
		wResDB = gVal.OBJ_DB_IF.RunQuery( wQy, False )
		if wResDB['Result']!=True :
			wRes['Reason'] = "Run Query is failed"
			gVal.OBJ_L.Log( "C", wRes )
			return wRes
		
		#############################
		# 辞書型に整形
		wARR_RateTraffic = gVal.OBJ_DB_IF.ChgDict( wResDB['Responce'] )
		
		wReportNum = len( wARR_RateTraffic )
		#############################
		# トラヒック報告がなければ終わり
		if wReportNum==0 :
			wRes['Result'] = True
			return wRes
		
		#############################
		# 報告するトラヒックを組み立てる
		wARR_Traffic = {
			0 : None,
			1 : None,
			2 : None
		}
		
		### 最新の日付のトラヒック
		wARR_Traffic[0] = wARR_RateTraffic[0]
		
		wARR_Komoku = list( gVal.STR_TrafficInfo.keys() )
		
		### 最新の翌日のトラヒック
		if wReportNum>=2 :
			wARR_Traffic[1] = wARR_RateTraffic[1]
			
			### 最新から規定日数の平均トラヒック
			wARR_Traffic[2] = {}
			### 枠作成
			for wKey in wARR_Komoku :
				wARR_Traffic[2].update({ wKey : 0 })
			
			wKeylist = list( wARR_RateTraffic.keys() )
			for wIndex in wKeylist :
				for wKey in wARR_Komoku :
					if wKey=="upddate" :
						continue
					wARR_Traffic[2][wKey] += wARR_RateTraffic[wIndex][wKey]
			
			### 各値を平均値に計算しなおす
			for wKey in wARR_Komoku :
				if wKey=="upddate" :
					continue
				wValHarf = wARR_Traffic[2][wKey] / wReportNum
				wARR_Traffic[2][wKey] = CLS_OSIF.sGetRound( wValHarf )
		
		#############################
		# 表示データの枠
		wARR_ViewTraffic = {}
		
		### 項目列＋1行目:日付
		wListData = " " * cls.DEF_KOMOKU_LEN + "  "
		wListData = wListData + str(wARR_Traffic[0]['upddate'])
		if wReportNum>=2 :
			### 1行目:スペース
			wListNumSpace = cls.DEF_KOMOKU_NUM_LEN - len( str(wARR_Traffic[0]['upddate']) )
			wListData = wListData + " " * wListNumSpace + "  "
			
			### 2行目
			wListData = wListData + str(wARR_Traffic[1]['upddate'])
			wListNumSpace = cls.DEF_KOMOKU_NUM_LEN - len( str(wARR_Traffic[1]['upddate']) )
			wListData = wListData + " " * wListNumSpace + "  "
			
			### 3行目
			wListData = wListData + "直近 " + str(gVal.DEF_STR_TLNUM['trafficReportLimit']) +"件平均"
		
		wARR_ViewTraffic.update({ "***header***" : wListData })
		
		### トラヒックデータ
		for wKey in wARR_Komoku :
			if wKey=="upddate" :
				continue
			
			### 項目
			wCharCnt = CLS_OSIF.sDCharaCount( gVal.STR_TrafficInfo[wKey][1] )
			wListNumSpace = cls.DEF_KOMOKU_LEN - wCharCnt
			wListData = gVal.STR_TrafficInfo[wKey][1] + " " * wListNumSpace + "   "
			
			### 1列目
			wListNumSpace = cls.DEF_KOMOKU_NUM_LEN - len( str(wARR_Traffic[0][wKey]) )
			wListData = wListData + " " * wListNumSpace + str(wARR_Traffic[0][wKey])
			if wReportNum>=2 :
				### 1行目:スペース
				wListData = wListData + "     "
				
				### 2行目
				wListNumSpace = cls.DEF_KOMOKU_NUM_LEN - len( str(wARR_Traffic[1][wKey]) )
				wListData = wListData + " " * wListNumSpace + str(wARR_Traffic[1][wKey]) + "     "
				
				### 3行目
				wListNumSpace = cls.DEF_KOMOKU_NUM_LEN - len( str(wARR_Traffic[2][wKey]) )
				wListData = wListData + " " * wListNumSpace + str(wARR_Traffic[2][wKey])
			
			wTag = "***" + wKey + "***"
			wARR_ViewTraffic.update({ wTag : wListData })
		
		#############################
		# 画面表示
		wResDisp = CLS_MyDisp.sViewDisp( "TrafficReport", inClear=inCrear, inData=wARR_ViewTraffic )
		if wResDisp['Result']==False :
			wRes['Reason'] = "sViewDisp is failed: reason=" + wResDisp['Reason']
			gVal.OBJ_L.Log( "A", wRes )
			return wRes
		
		#############################
		# 1件以上報告した
		if wReportNum>=1 :
			wRes['Responce'] = True
		
		#############################
		# 正常終了
		wRes['Result'] = True
		return wRes



