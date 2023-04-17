#!/usr/bin/python
# coding: UTF-8
#####################################################
# ::Project  : Korei Bot Win
# ::Admin    : Korei (@korei-xlix)
# ::github   : https://github.com/korei-xlix/koreibot_win/
# ::Class    : てすと用
#####################################################
from osif import CLS_OSIF
from mydisp import CLS_MyDisp
from gval import gVal
#####################################################
class CLS_Test():
#####################################################
	OBJ_Parent = ""				#親クラス実体
	
#####################################################
# Init
#####################################################
	def __init__( self, parentObj=None ):
		#############################
		# 応答形式の取得
		#   "Result" : False, "Class" : None, "Func" : None, "Reason" : None, "Responce" : None
		wRes = CLS_OSIF.sGet_Resp()
		wRes['Class'] = "CLS_Test"
		wRes['Func']  = "__init__"
		
		if parentObj==None :
			###親クラス実体の未設定
			wRes['Reason'] = "You have not set the parent class entity for parentObj"
			gVal.OBJ_L.Log( "A", wRes )
			return
		
		self.OBJ_Parent = parentObj
		return



#####################################################
#			wSubRes = cls.OBJ_TwitterMain.TestRun()
###			wTime = CLS_OSIF.sGetTimeformat_Twitter( "2021-10-06T12:23:44.000Z" )
###			print( str(wTime['TimeDate']) )
#
###			wSubRes = cls.OBJ_TwitterMain.CircleWeekend()
#
#			wSubRes = gVal.OBJ_Tw_IF.GetTweetLookup( "1473387112351559680" )
#			print( str(wSubRes) )
##			wTwitterRes = gVal.OBJ_Tw_IF.GetTweetLookup( "1516980757394190337" )
##			if wTwitterRes['Result']!=True :
##				wRes['Reason'] = "Twitter API Error: " + wTwitterRes['Reason']
##				gVal.OBJ_L.Log( "B", wRes )
##				return wRes
###			print( wTwitterRes['Responce'] )
###
###			print( "zzz: " + str(wTwitterRes['Responce']) )
##
##			d = {'k1': 1, 'k2': 2, 'k3': 3}
##			print( str(d) )
##			removed_value = d.pop('k1')
##			print( str(d) )
###			wSubRes = gVal.OBJ_DB_IF.GetRecordNum( "tbl_favouser_data" )
###			print( str(wSubRes) )

##			wSubRes = self.OBJ_Twitter.GetListMember( gVal.STR_UserInfo['ListName'] )
##			if wSubRes['Result']!=True :
##				wRes['Reason'] = "xxxx: " + wSubRes['Reason']
##				gVal.OBJ_L.Log( "B", wRes )
##				return wRes

##			wARR_Dict = {}
##			wARR_Dict.update({ "test1" : 1 })
##			wARR_Dict.update({ "test2" : 2 })
##			wARR_Dict.update({ "test3" : 3 })
##			wARR_Dict.update({ "test4" : 4 })
##			if "test2" in wARR_Dict :
##				print("OK")
##			else:
##				print("NG")
##			
##			if "test5" in wARR_Dict :
##				print("OK")
##			else:
##				print("NG")

###			wSubRes = gVal.OBJ_Tw_IF.ViewList_User( "korei_comm" )

######		
#			wTweetRes = gVal.OBJ_Tw_IF.Tweet( "てすとついーと２" )
#			wTweetRes = gVal.OBJ_Tw_IF.GetSearch( inQuery="てすとついーと２" )
#			print(str( wTweetRes ))
######		
#			wSubRes = gVal.OBJ_Tw_IF.GetLists( "korei_xlix" )
#			print(str( wSubRes ))
######		
#			wTweetRes = gVal.OBJ_Tw_IF.GetSearch( "togenohito " + '\n' + "お願い リスト vtuber をフォローするには当アカウント korei_xlix もフォローしてください。" )
#			print(str( wTweetRes ))
######		
##			wGetListsRes = gVal.OBJ_Tw_IF.GetLists( "account" )
##			print(str( wGetListsRes['Responce'] ))
######		

#####################################################
# TEST
#####################################################
	def Test(self):
		#############################
		# 応答形式の取得
		#   "Result" : False, "Class" : None, "Func" : None, "Reason" : None, "Responce" : None
		wRes = CLS_OSIF.sGet_Resp()
		wRes['Class'] = "CLS_TwitterMain"
		wRes['Func']  = "TestRun"
		
		#############################
		# Twitter情報取得
		wFavoRes = self.OBJ_Parent.GetTwitterInfo()
		if wFavoRes['Result']!=True :
			wRes['Reason'] = "GetTwitterInfo is failed"
			gVal.OBJ_L.Log( "B", wRes )
			return wRes
		
#		#############################
#		# いいね解除（●フル自動監視）
#		wSubRes = self.OBJ_Parent.OBJ_TwitterFavo.RemFavo()
#		if wSubRes['Result']!=True :
#			wRes['Reason'] = "RemFavo"
#			gVal.OBJ_L.Log( "B", wRes )
#			return wRes
		
#		#############################
#		# リストいいね（●フル自動監視）
#		wSubRes = self.OBJ_Parent.OBJ_TwitterFavo.ListFavo( inFLG_Test=True )
#		if wSubRes['Result']!=True :
#			wRes['Reason'] = "ListFavo"
#			gVal.OBJ_L.Log( "B", wRes )
#			return wRes
		
#		#############################
#		# フォロワーいいね
#		wSubRes = self.OBJ_Parent.OBJ_TwitterFavo.FollowerFavo( inTest=True )
#		if wSubRes['Result']!=True :
#			wRes['Reason'] = "FollowerFavo"
#			gVal.OBJ_L.Log( "B", wRes )
#			return wRes
		

###		wTweetRes = gVal.OBJ_Tw_IF.GetMyMentionLookup()

#		wTweetRes = gVal.OBJ_Tw_IF.GetUserFavolist( "1449704371881603075", 1 )
##		print(str( wTweetRes['Responce'] ))
##		wKeylist = list( wTweetRes['Responce'].keys() )
##		for wID in wTweetRes['Responce'] :
#		for wROW in wTweetRes['Responce'] :
#			print( str( wROW ) + '\n' )
#			print( "----------" + '\n' )


#		wStr = "@korei_xlix へろーーー"
#
#		wIndex = wStr.find(" ")
#
#		print(wStr[1:wIndex] + ":::" )
#		### korei_xlix:::


#		wSubRes = self.OBJ_Parent.OBJ_TwitterReaction.ReactionCheck()
#		wSubRes = self.OBJ_Parent.OBJ_TwitterReaction.VIP_ReactionCheck()
#		wSubRes = self.OBJ_Parent.OBJ_TwitterReaction.ReactionResult()


#		wSubRes = self.OBJ_Parent.OBJ_TwitterAdmin.RemoveCautionUser( inFLR_Recheck=True )

###		wSubRes = gVal.OBJ_Tw_IF.GetTweetLookup( "1616592525489508353" )
		wSubRes = gVal.OBJ_Tw_IF.GetFollowIDList( "1429385181899542530" )
		print( str(wSubRes) )



		#############################
		# 完了
		wRes['Result'] = True
		return wRes



