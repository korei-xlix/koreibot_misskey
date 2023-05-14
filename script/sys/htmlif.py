#!/usr/bin/python
# coding: UTF-8
#####################################################
# ::Project  : Korei Bot Win
# ::Admin    : Korei (@korei-xlix)
# ::github   : https://github.com/korei-xlix/koreibot_win/
# ::Class    : HTML制御
#####################################################
# Private Function:
#   (none)
#
# Instance Function:
#   (none)
#
# Class Function(static):
#   (none)
#
#####################################################
import os
import webbrowser

#####################################################
class CLS_HTMLIF() :

	DEF_MOJI_ENCODE = 'utf-8'								#文字エンコード

#####################################################
# URLオープン
#####################################################
	@classmethod
	def sOpenURL( cls, inURL ):
		try:
			webbrowser.open( inURL )
		except ValueError as err :
			return False
		
		return True



