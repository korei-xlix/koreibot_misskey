#!/usr/bin/python
# coding: UTF-8
#####################################################
# ::Project  : Korei Bot Win
# ::Admin    : Korei (@korei-xlix)
# ::github   : https://github.com/korei-xlix/koreibot_win/
# ::Class    : グローバル値
#####################################################

#####################################################
class gVal() :

#############################
# ※ユーザ自由変更※
	DEF_TIMEZONE = 9										# 9=日本時間 最終更新日補正用
	DEF_MOJI_ENCODE = 'utf-8'								#文字エンコード

#############################
# システム情報
	#データversion(文字)
	DEF_CONFIG_VER = "1"

	STR_SystemInfo = {
		"Client_Name"	: "これーぼっと",
		"github"		: "",
		"Admin"			: "",
		"PythonVer"		: 0,
		"HostName"		: "",
		
		"EXT_FilePath"	: None,
		
		"RunMode"		: "normal"
			# normal= 通常モード
			# setup = セットアップモード
			# init  = 全初期化モード
			# clear = データクリア
	}

#############################
# ユーザ情報
	STR_UserInfo = {
		"Account"		: "",			#Twitterアカウント名
		"id"			: "",			#Twitter ID(番号)
		
		"TrendTag"		: "",			#トレンドタグ設定
		"QuestionTag"	: "",			#質問タグ設定
		"VipTag"		: "",			#VIPリツイート 対象タグ
		"DelTag"		: "",			#削除ツイート  対象タグ
		
		"ListID"		: None,			#リスト通知 リストID
		"ListName"		: None,			#リスト通知 リスト名
		
		"AutoRemove"	: False,		#自動リムーブ True=有効
		"mListID"		: None,			#相互フォローリスト リストID
		"mListName"		: None,			#相互フォローリスト リスト名
		"fListID"		: None,			#片フォロワーリスト リストID
		"fListName"		: None,			#片フォロワーリスト リスト名
		
		"Traffic"		: False,		#Twitterにトラヒックを報告するか
		
		"AutoSeq"		: 0,			#自動監視シーケンス
		
		"mfvstop"		: False,		#相互いいね停止 true=有効
		"mfvstop_date"	: None			#相互いいね停止 開始日
	}

#############################
# 時間情報
	STR_Time = {
										# 各実行時間
		"run"			: None,			# コマンド実行
		"autorun"		: None,			# 自動監視
		"autoseq"		: None,			# 自動監視シーケンス
		"reaction"		: None,			# リアクション受信
		"mffavo"		: None,			# 相互フォローリストいいね
		"flfavo"		: None,			# フォロワー支援いいね
		"list_clear"	: None,			# リスト通知クリア
		"auto_remove"	: None,			# 自動リムーブ
		"send_favo"		: None,			# いいね情報送信
		"auto_delete"	: None,			# 自動削除
		"vip_ope"		: None,			# VIP監視
		"del_tweet"		: None,			# 削除ツイート
		"tl_follow"		: None,			# タイムラインフォロー
		"keywordsrch"	: None,			# キーワードいいね
		"send_ren"		: None,			# 連ファボ送信
		
		"TimeDate"		: None			# システム時間
	}

#############################
# トラヒック情報
	STR_TrafficInfo = {
		"upddate"			: None,	# 記録日時(更新)
		
		"run"				: {0:0,1:"bot実行回数"},
		"run_time"			: {0:0,1:"実行時間"},
		"run_api"			: {0:0,1:"api実行回数"},
		"run_ope"			: {0:0,1:"自動監視実施回数"},
		
		"timeline"			: {0:0,1:"タイムライン取得数"},
		
		"myfollow"			: {0:0,1:"フォロー者数"},
		"p_myfollow"		: {0:0,1:"フォロー実施数"},
		"d_myfollow"		: {0:0,1:"リムーブ実施数"},
		
		"follower"			: {0:0,1:"フォロワー数"},
		"p_follower"		: {0:0,1:"フォロワー獲得数"},
		"d_follower"		: {0:0,1:"被リムーブ者数"},
		
		"r_reaction"		: {0:0,1:"リアクション受信回数"},
		"r_rep"				: {0:0,1:"リプライ受信回数"},
		"r_retweet"			: {0:0,1:"リツイート受信回数"},
		"r_iret"			: {0:0,1:"引用リツイ受信回数"},
		"r_favo"			: {0:0,1:"いいね受信回数"},
		"r_in"				: {0:0,1:"リアクション受信回数(F内)"},
		"r_out"				: {0:0,1:"リアクション受信回数(F外)"},
		"r_vip"				: {0:0,1:"リアクション受信回数(VIP)"},
		
		"s_run"				: {0:0,1:"検索実施数"},
		"s_hit"				: {0:0,1:"検索ヒット数"},
		"s_favo"			: {0:0,1:"検索時いいね数"},
		
		"favo"				: {0:0,1:"いいね数"},
		"p_favo"			: {0:0,1:"いいね実施回数"},
		"d_favo"			: {0:0,1:"いいね解除回数"},
		"p_tweet"			: {0:0,1:"ツイート送信回数"},
		
		"db_req"			: {0:0,1:"DB request回数"},
		"db_ins"			: {0:0,1:"DB insert回数"},
		"db_up"				: {0:0,1:"DB update回数"},
		"db_del"			: {0:0,1:"DB delete回数"},
		
	}

#############################
# ウェイト情報
	STR_WaitInfo = {
		"zanNum"			: 0,	#残り処理数
		"zanCount"			: 0,	#カウント数(0でウェイト処理)
		"setZanCount"		: 0,	#カウント数(セット値)
		"waitSec"			: 5,	#待ち時間(秒)
		"Skip"				: False	#スキップ待機
	}



#############################
# Timeline調整数
	DEF_STR_TLNUM = {
		
		"forAutoAllRunSec"		: 14400,				# 自動監視 全実行期間         4時間  60x60x4
		"forAutoSeqSec"			: 86400,				# 自動監視シーケンスリセット  1日    60x60x24
		"forAutoSeqSecSleep"	: 10,					# 自動監視シーケンス スリープ時間
		
														# いいね管理
		"favoTweetLine"		: 40,						#   いいね時 対象ユーザツイート取得ライン数
		"favoCancelNum"		: 8,						#   いいね時 連続スキップでキャンセル
		"autoRepFavo"		: True,						#   自動おかえしいいね True=有効
		"getUserTimeLine"	: 80,						#   相手ユーザ取得タイムライン数
		
														# 周回待ち要
		"defWaitCount"		: 16,						#   デフォルト待ち回数
		"defWaitSec"		: 5,						#   デフォルト待ち時間(秒)
		"defWaitSkip"		: 10,						#   デフォルトスキップ時間(秒)
		"defLongWaitSec"	: 60,						#   デフォルト 長い待ち時間(秒)
		"defPeriodSec"		: 86400,					#   デフォルト期間   1日  (60x60x24)x1
		
														# リアクションチェック
		"reactionTweetLine"			: 40,				#   リアクションチェック時の自ツイート取得ライン数
		"reactionTweetLine_Short"	: 8,				#   リアクションチェック時の自ツイート取得ライン数(ショート時)
		"forReactionSec"			: 3600,				#   リアクションまでの期間   1時間  60x60
		"forReactionTweetSec"		: 259200,			#   リアクションに反応するツイート期間 3日  (60x60x24)x3
		"forReactionListUserRand"	: 20,				#   相互フォローリスト・片フォローリスト ランダム実施値 パーセンテージ (1-100)   20％で実施
		
		"forVipOperationSec"		: 3600,				#   VIPリアクション監視までの期間   1時間  60x60x1
		"vipReactionTweetLine"		: 20,				#   VIPリアクションチェック時のツイート取得ライン数
		"forVipReactionTweetSec"	: 86400,			#   リアクションに反応するツイート期間 1日  60x60x24
		
														# リストいいね
		"forListFavoSec"				: 86400,		#   リストいいねまでの期間   1日  60x60x24
		
														# 自動キーワードいいね
		"forAutoKeywordSearchFavoSec"	: 86400,		#   キーワードいいねまでの期間   1日  60x60x24
		
														# フォロワー支援いいね
		"forFollowerFavoSec"				: 14400,	#   フォロワー支援いいねまでの期間   4時間  60x60x4
		"forFollowerFavoMListMutualSec"		: 43200,	#   相互フォローリスト 相互フォローの いいね期間  12時間  60x60x12
		"forFollowerFavoMListMyFollowSec"	: 28800,	#   相互フォローリスト 片フォロー者の いいね期間   8時間  60x60x8
		
		"forFollowerFavoFListSec"			: 115200,	#   片フォロワーリスト処理期間                     32時間  60x60x32
		"forFollowerFavoFListIntimeSec"		: 86400,	#   片フォロワーリスト・期間内の いいね期間        1日  60x60x24
		"forFollowerFavoFListOverSec"		: 172800,	#   片フォロワーリスト・期間外の いいね期間        2日 (60x60x24)x2
		"forFollowerFavoFListpfavoSec"		: 432000,	#   片フォロワーリスト・期間外時 いいね実行からの期間  5日 (60x60x24)x5
		
		"forFollowerFavoMutualSec"			: 14400,	#   相互フォローの いいね期間                      4時間  60x60x4
		"forFollowerFavoFollowerSec"		: 115200,	#   フォロワー期間                                 32時間  60x60x32
		"forFollowerFavoIntimeSec"			: 86400,	#   フォロワー・期間内の いいね期間                1日  60x60x24
		"forFollowerFavoOverSec"			: 172800,	#   フォロワー・期間外の いいね期間                2日 (60x60x24)x2
		"forFollowerFavoHarfMyfollowSec"	: 288000,	#   片フォロー者の いいね期間                      3日+8時間 (60x60x24)x3+(60x60x8)
		
		"forFollowerFavoHarfMyfollowCnt"	: 5,		#   片フォロー者 初回無条件実施回数
		"forFollowerFavoHarfMyfollowRand"	: 10,		#   片フォロー者 ランダム実施値 パーセンテージ (1-100)   30％で実施
		"forFollowerFavoHarfMyfollowRunSec"	: 86400,	#   片フォロー者の いいね実施期間                  1日  60x60x24
		
###		"forFollowerFavoNonFollowerSec"		: 259200,	#   非絡みユーザの いいね実施間隔                  3日  (60x60x24)x3
###		"forFollowerFavoNonFollowerSec"		: 432000,	#   非絡みユーザの いいね実施間隔                  5日  (60x60x24)x5
###		"forFollowerFavoNonFollowerCnt"		: 5,		#   非絡みユーザのいいね ランダム実施値 パーセンテージ (1-100)   5％で実施
###		"forFollowerFavoNonFollowerCnt"		: 10,		#   非絡みユーザのいいね ランダム実施値 パーセンテージ (1-100)   5％で実施
###		
														# 自動いいね
		"forAutoFavoTweetSec"				: 86400,	#   対象ツイート期間       1日  60x60x24
		"forAutoFavoReturnFavoSec"			: 3600,		#   お返しいいねへの期間   1時間  60x60x1
		"forAutoFavoListFavoSec"			: 86400,	#   リストいいねへの期間   1日  (60x60x24)x1
		"forAutoFavoLevelCCnt"				: 2,		#   レベルC以前の場合、1度でいいねする数
		"forAutoFavoLevelRunRand"			: 10,		#   レベルによる中止 ランダム実施値 パーセンテージ (1-100)   10％で実施
		"forAutoFavoTweet_B_Sec"			: 14400,	#   非からみツイートのいいね期間   4時間  60x60x4
		
		"forRemFavoSec"				: 172800,			# いいね解除までの期間 2日 (60x60x24)x2
		
		"forListFavoAutoRemoveSec"			: 345600,	#   リストいいね 自動リムーブまでの期間   4日  (60x60x24)x4
		"forListFavoAutoRemoveSec_Short"	: 43200,	#   リストいいね 自動リムーブまでの期間(短期)   12時間  (60x60x12)
		"forCheckAutoRemoveSec"		: 14400,			#   自動リムーブチェック期間 4時間  (60x60x4)
###		"forOverListFavoCount"		: 3,				#   外部いいね数(1ユーザ)
###		"forOverListFavoCount"		: 2,				#   外部いいね数(1ユーザ)
		"forOverListFavoCount"		: 1,				#   外部いいね数(1ユーザ)
		"forCheckAutoDeleteSec"		: 172800,			#   自動削除チェック期間 2日 (60x60x24)x2
		
		"forAutoRemoveByeBye_ShortSec"		: 172800,	#   完全追い出し期間(短期)          2日  (60x60x24)x2
		"forAutoRemoveByeBye_ShortCnt"		: 5,		#   完全追い出し期間(短期)になるいいね受信回数(以下で短期)
		"forAutoRemoveByeByeSec"			: 432000,	#   完全追い出し期間                5日  (60x60x24)x5
		"forAutoRemoveReleaseSec"			: 86400,	#   完全追い出し期間(さよなら)      1日  (60x60x24)
		"forAutoRemoveIgnoreCompletelySec"	: 432000,	#   完全スルーのため追い出し期間    5日  (60x60x24)x5
		
		"forAutoRemoveIgnoreCompletelyCnt"	: 4,		#   いいねがない場合の無条件追い出しまでのいいね実施回数
		"forAutoRemoveReliefCnt"			: 3,		#   自動リムーブから救済される 今週いいね回数
###		"forAutoRemoveReliefSec"			: 86400,	#   レベルG-が引き揚げられる いいね期間    1日  (60x60x24)
		"forReFollowerPastRfavoCnt"			: 4,		#   レベルG-の再フォローを許容する、過去のいいね受信数
		
		"forAutoUserRemoveSec"			: 2592000,		# ユーザ削除までの期間                 30日 (60x60x24)x30
		"forFavoDataDelSec"				: 7776000,		# いいね情報削除までの期間             90日 (60x60x24)x90
		"forFavoDataDelHardSec"			: 34214400,		# いいね情報削除までの期間(残しデータ) 396日 (60x60x24)x396
		"forFavoDataDelLevelFSec"		: 259200,		# いいね情報削除までの期間(レベルF)     3日 (60x60x24)x3
		
		"forAutoTweetDeleteCycleSec"	: 14400,		# 自動ツイート削除 実施期間           4時間 (60x60x4)
###		"forAutoTweetDeleteSec"			: 3600,			# 自動ツイート削除期間                1時間 (60x60)
		"forAutoTweetDeleteSec"			: 86400,		# 自動ツイート削除期間                  1日 (60x60x24)x1
		"forAutoTweetDeleteCount"		: 2,			# 自動ツイート削除範囲  n x 200
		
														# いいね送信
		"favoSendsSec"		: 604800,					# いいね送信までの期間      7日 (60x60x24)x7
		"favoSendsCnt"		: 3,						# いいね送信対象 いいね回数
		"LEVEL_B_Cnt"		: 5,						# レベルB昇格までのトロフィー獲得回数
		
														# 連ファボ制御
		"forRenFavoResetSec"	: 57600,				#   連ファボリセット時間                  16時間 (60x60x16)
###		"renFavoUpCnt"			: 5,					#   連ファボ判定計上数(1タイムライン中の新規いいね数)  超えたら1カウント
		"renFavoUpCnt"			: 10,					#   連ファボ判定計上数(1タイムライン中の新規いいね数)  超えたら1カウント
		"renFavoBotCnt"			: 3,					#   連ファボ判定個数(1タイムライン中のいいね数)        超えたらBot判定
###		"forRenFavoReiineRand"	: 10,					#   Bot判定ユーザに対するいいね返信率 パーセンテージ (1-100)   10％で実施
		"forRenFavoReiineRand"	: 20,					#   Bot判定ユーザに対するいいね返信率 パーセンテージ (1-100)   10％で実施
		"renFavoBotNoactionCnt"	: 10,					#   連ファボ無反応カウント数                           超えたらBot判定+リアクション拒否
		"forRenFavoBotFavoSec"	: 259200,				#   連ファボリセット時間                  3日 (60x60x24)x3
		
														# ユーザ管理
		"forGetUserSec"			: 600,					#   ユーザ取得間隔  10分  60x10
		"forFollowerConfirmSec"	: 86400,				#   フォロワー状態の更新 期間   1日  (60x60x24)x1
		
														# キーワードいいね
		"KeywordTweetLen"			: 80,				#   キーワードいいねツイート取得数
		"KeywordTweetLen_LongCircle"	: 2,			#   キーワードいいねツイート取得数
		"forKeywordTweetSec"		: 28800,			#   キーワードいいね いいね期間   8時間  60x60x8
		"forKeywordObjectTweetSec"	: 86400,			#   キーワードいいね 対象いいね期間   1日  (60x60x24)x1
		
		"sendListUsersCaution"		: True,				# リスト登録チェック時警告を送信するか  True=送信
#		"sendListUsersCaution"		: False,			# リスト登録チェック時警告を送信するか  True=送信
		"checkListUnfollower"		: True,				# リスト登録チェック時 フォロワーでないユーザへ警告を送信するか  True=送信
#		"checkListUnfollower"		: False,			# リスト登録チェック時 フォロワーでないユーザへ警告を送信するか  True=送信
###		"forDeleteCautionTweetSec"	: 172800,			# 警告メッセージを削除する期間        2日 (60x60x24)x2
		"forDeleteCautionTweetSec"	: 100800,			# 警告メッセージを削除する期間     28時間 (60x60x28)
		
		"forTimelineFollowSec"			: 14400,		# タイムラインフォロー チェック期間 4時間  (60x60x4)
###		"TimelineFollowNum"				: 2,			#   フォローする最大人数
		"TimelineFollowNum"				: 5,			#   フォローする最大人数
		"TimelineFollowTweetLine"		: 200,			#   ツイート取得ライン数
		"TimelineFollowTweetLine_Skip"	: 40,			#   ツイート取得ライン 先頭スキップ数
		"TimelineFollowFavoCheckNum"	: 32,			#   いいね、リツイート、引用リツイートのチェック回数(Limit)
		"forAutoReFollowCnt"			: 10,			# 1回の自動監視で実施する自動再フォロー実行数(最大12)
		"forAutoReFollowFollowCnt"		: 3,			# 1回の再フォロー処理で自動フォローするユーザ数
		
		"forMultiFavoStopReleaseSec"	: 172800,		# 相互いいね停止期間(自動解除)  2日 (60x60x24)x2
		
###		"resetAPISec"		: 900,						# APIリセット周期 15分 60x15
		"resetAPISec"		: 600,						# APIリセット周期 10分 60x10
		"forLockLimSec"		: 120,						# 排他保持時間     2分 60x2 
		"logShortLen"		: 100,						# ログ表示 ショートモード
		
		"(dummy)"			: ""
	}

#############################
# 連ファボ スコア
###	DEF_STR_REN_SCORE = {
###		"NoFollowScore"		: 15,			# 非絡みになるスコア
###		
###		"Score_Normal"		: 1,			# 通常ツイート ←いいね
###		"Score_Retweet"		: 3,			# リツイート
###		"Score_Quoted"		: 5,			# 引用リツイート
###		"Score_Reply"		: 5,			# リプライ（他者）
###		"Score_Question"	: 7,			# 質問 ←いいね
###		"Score_Delete"		: 9				# 削除 ←いいね
###	}

#############################
# ユーザレベル(親密度)            *   ..いいね支援対象
#                                   * ..おかえしいいね
	DEF_STR_USER_LEVEL = {
		"A"		: "",			# * *  A : フォロー者(フォロー時リストあり・著名人など)  *自動リムーブしない
								#          フォロー時、リストを設定してた場合
		"A+"	: "",			# * *  A+: フォロー者 手動でVIP設定したアカウント        *自動リムーブしない
								#          手動でVIP設定したとき
		"B+"	: "",			# * *  B+: 相互フォロー 規定回以上トロフィー獲得者       *自動リムーブしない
								#          
		"B"		: "",			# * *  B : 相互フォロー トロフィー獲得者
								#          相互フォロー中にトロフィーを獲得した場合
		"C"		: "",			# * *  C : 相互フォロー(トロフィーを獲得して相互フォローに自動昇格したアカウント)
								#          片フォロワー時にトロフィーを獲得して、相互になった場合
		"C+"	: "",			# * *  C+: 相互フォロー 元フォロー者 もしくは 手動でリフォローしたアカウント
								#          フォローした、もしくはフォローされた時点で、相互フォローになった場合
		"C-"	: "",			#      C-: 相互時にリムーブされたことがあるアカウント
								#          相互フォロー中、リムーブされた場合（結果フォロー者あり・フォローなし）
		"D"		: "",			# *    D : 自発的フォロー者
								#          自発的にフォローした場合
		"D+"	: "",			# *    D+: 自動フォロー
								#          botから自動的にフォローした場合
		"D-"	: "",			#      D-: 自発的リムーブ者
								#          フォローしてたけど、自発的にリムーブした場合
		"E"		: "",			# * *  E : フォロワー
								#          フォローされた場合
		"E+"	: "",			#      E+: フォローしたけどリフォローしてもらえなかったアカウント
								#          フォローしてたけど、時間経過でリムーブした場合（フォロー者なし・フォローなし）
		"E-"	: "",			#      E-: リムーブされたことがあるアカウント
								#          フォローされてたけど、リムーブされた場合（フォロー者なし・フォローなし）
		"F"		: "",			#      F : 非フォロワーでいいねされたことがあるアカウント
								#          非フォロワーでいいねされた場合
###		"F+"	: "",			#      F+: フォロワーだけど完全スルー期間が過ぎたため、無視しているアカウント
###								#          片フォロワー状態で 登録から規定日数、あるいは最終いいねから規定日数過ぎた
###		"G"		: "",			#   R  G : 相互フォロー あまり絡みなくない人
###								#          botが自動設定した
###		"G+"	: "",			#   R  G+: 相互フォロー あまり絡みなくない人
###								#          手動で設定する
###		"H"		: "",			#   R  H : 片フォロワー あまり絡みなくない人
###								#          botが自動設定した
###		"H+"	: "",			#   R  H+: 片フォロワー あまり絡みなくない人
###								#          手動で設定する
###		"H-"	: "",			#      H-: G、G+、H、H+でリムーブされたことのあるアカウント
###								#          F+からリムーブされたアカウント
		"G"		: "",			#      G : フォロワーだけど完全スルー期間が過ぎたため、無視しているアカウント
								#          片フォロワー状態で 登録から規定日数、あるいは最終いいねから規定日数過ぎた
		"G-"	: "",			#      G-: 追い出したことがあるフォロワー  Gからリムーブされたフォロワー
								#          追い出しした場合  G状態でリムーブされた場合
		"L"		: "",			#      L : 非フォロワーでリストだけ登録したことがあるアカウント(リスト乞食)
								#          対象アカウント
		"Z"		: "",			#      Z : ブロックされたアカウント
								#          被ブロックを検知した場合
###		"Z-"	: "",			#      Z-: 追い出したことがあるフォロワー  F+からリムーブされたフォロワー
###								#          追い出しした場合  F+状態でリムーブされた場合
		"(dummy)"			: ""
	}

#############################
# ファイルパス
#   ファイルは語尾なし、フォルダは_path
	DEF_STR_FILE = {
									# readme.md ファイルパス
		"Readme"				: "readme.md",
		
									# 除外データアーカイブ ファイル名
		"ExcWordArc"			: "/DEF_ExcWordArc.zip",
									# 除外データアーカイブ 解凍先フォルダパス
		"Melt_ExcWordArc_path"	: "/DEF_ExcWordArc",
									# 除外データ 文字列ファイルパス(フォルダ付き)
		"Melt_ExcWord"			: "/DEF_ExcWordArc/DEF_ExcWord.txt",
									# 禁止ユーザファイルパス(フォルダ付き)
		"Melt_ExcUser"			: "/DEF_ExcWordArc/DEF_ExcUser.txt",
									# 禁止ユーザプロフィールファイルパス(フォルダ付き)
		"Melt_ExcProf"			: "/DEF_ExcWordArc/DEF_ExcProf.txt",
									# リストいいね指定ファイル
		"Melt_ListFavo"			: "/DEF_ExcWordArc/DEF_ListFavo.txt",
		
									# ログの退避フォルダ
		"LogBackup_path"		: "../koreibot_win_log",
		"(dummy)"				: 0
	}

	DEF_DISPPATH = "script/disp/"

	DEF_STR_DISPFILE = {
		"MainConsole"			: DEF_DISPPATH + "main_console.disp",
		"UserAdminConsole"		: DEF_DISPPATH + "useradmin_console.disp",
		"KeywordConsole"		: DEF_DISPPATH + "keyword_console.disp",
		"ListFavoConsole"		: DEF_DISPPATH + "listfavo_console.disp",
		"ExcUserConsole"		: DEF_DISPPATH + "excuser_console.disp",
		"CautionConsole"		: DEF_DISPPATH + "caution_console.disp",
		"UserBConsole"			: DEF_DISPPATH + "userb_console.disp",
		
		"TrafficReport"			: DEF_DISPPATH + "traffic_report.disp",
		
		"SystemConfigConsole"	: DEF_DISPPATH + "system_config_console.disp",
		"SystemViewConsole"		: DEF_DISPPATH + "system_view_console.disp",
		"(dummy)"				: 0
	}

#############################
# 定数
	DEF_LOCK_LOOPTIME = 2									#ロック解除待ち
	DEF_LOCK_WAITCNT  = 30									#  待ち時間: DEF_LOCK_LOOPTIME * DEF_LOCK_WAITCNT
	DEF_TEST_MODE     = "bottest"							#テストモード(引数文字)
	DEF_DATA_BOUNDARY = "|,|"
	
###	DEF_SCREEN_NAME_SIZE = 16
	DEF_SCREEN_NAME_SIZE = 24

	DEF_VAL_DAY  = 86400									# 時間経過: 1日  60x60x24
	DEF_VAL_WEEK = 604800									# 時間経過: 7日  (60x60x24)x7
	
	DEF_TIMEDATE = "1901-01-01 00:00:00"
	DEF_NOTEXT   = "(none)"

	DEF_ADMINLOG_POINT = 12

#############################
# 変数
	FLG_Test_Mode    = False								#テストモード有無
	
	OBJ_Tw_IF = ""											#Twitter I/F
	OBJ_DB_IF = ""											#DB I/F
	OBJ_L     = ""											#ログ用
	
	ARR_ExeWord = {}										# 除外文字データ
	ARR_ExeWordKeys = []
	ARR_ExeProf = {}										# 除外文字データ
	ARR_ExeProfKeys = []
	ARR_ListFavo = {}										# リストいいね指定
	ARR_NotReactionUser = {}								# リアクション禁止ユーザ
	ARR_SearchData = {}										# 検索データ
	ARR_CautionTweet = {}									# 警告ツイート

	VAL_AutoReFollowCnt = 0


