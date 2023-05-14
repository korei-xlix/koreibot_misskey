# samafeald bot misskey
**～取扱説明書 兼 設計仕様書～**  


# システム概要 <a name="aSystemSummary"></a>
python3で作成したmisskey支援用botです。  





# 目次 <a name="aMokuji"></a>
* [システム概要](#aSystemSummary)
* [前提](#aPremise)
* [デフォルトエンコードの確認](#aDefEncode)
* [セットアップ手順](#aSetup)
* [起動方法](#aStart)
* [アップデート手順](#aUpdate)
* [運用方法](#aHowtoUnyou)
* [機能説明](#aFunction)
* [本リポジトリの規約](#aRules)
* [参考記事](#aReference)




# 前提 <a name="aPremise"></a>
* python3（v3.8.5で確認）
* MySQL（MariaDB）（Linux版）
* Linux（開発はcugwin環境）
* misskeyアカウント
* githubアカウント
* デフォルトエンコード：utf-8




# デフォルトエンコードの確認　★初回のみ <a name="aDefEncode"></a>
本ソフトはデフォルトエンコード**utf-8**で動作することを前提に設計してます。
utf-8以外のエンコードでは誤動作を起こす場合があります。
pythonのデフォルトエンコードを確認したり、utf-8に設定する方法を示します。

```
# python
>>> import sys
>>> sys.getdefaultencoding()
'utf-8'
  utf-8が表示されればOKです。

>> exit
  ここでCtrl+Z を入力してリターンで終了します。
```

もしutf-8でなければWindowsの環境変数に PYTHONUTF8=1 を追加します。  
「スタート」→「システムの詳細設定 で検索」→「詳細設定」→「環境変数」  
ここに **変数名=PYTHONUTF8、変数値=1** を追加する。  
設定したら上記エンコードの確認を再実行して確認しましょう。  




# セットアップ手順 <a name="aSetup"></a>

## python3ライブラリのインストール <a name="aSetup_python3lib"></a>
python3の処理で必要なライブラリをインストールします。  
python3の本体はCygwinと一緒にインストールされてるはずです。  
  
なお、Galaxy Fleetで使うライブラリは以下の通りです。  
* python-dateutil 
* psycopg2
* apt-cyg（apt-getのcygwin版）
* procps（apt-cygでインストール）
* websockets
* misskey.py
* mysql-connector-python



以下手順です。  
* 1.以下のコマンドでpythonの動作テストしてみます。  
```
$ python -V
Python 3.8.2
  ※Windowsの場合、python3ではなく、pythonらしいです  
```

* 2.pip3でライブラリをインストールします。  
```
$ pip3 install websockets misskey.py python-dateutil psycopg2 mysql-connector-python


～中略～

$ pip3 list
～以下省略～
```

* 3.apt-cygと、apt-cygを使ってprocpsライブラリをインストールします。  
```
wgetでapt-cygを取得する
$ cd 
$ wget https://raw.githubusercontent.com/transcode-open/apt-cyg/master/apt-cyg
$ chmod 755 apt-cyg
$ mv apt-cyg /usr/local/bin

システム系コマンドのために
$ apt-cyg install procps
```



## エンコードの確認と設定 <a name="aSetup_endode"></a>
念のためデフォルトエンコードを確認しておきます。  
  
Galaxy FleetはOSのエンコードが uft-8 でないと動作しません。  
Cygwinはデフォルトでutf-8なので問題ないはずです。  

* 1.コマンドを入力します。  
```
$ python3
>>> import sys
>>> sys.getdefaultencoding()
'utf-8'

ここでuft-8がでればOKです。

以下はpython3コンソールの終了コマンドです。
>>> exit
[ctrl+D] ※キー入力で終了
```
  utf-8であれば、ここでスキップできます。  

* 2.もしutf-8でなかったらプロファイルにエンコードを追加します。  
```
viエディタを起動します。
$ vi /home/[Cygwinユーザ]/.bash_profile

ファイルの最後に以下を追加します。
export LANG=ja_JP.UTF-8

viエディタを終了します。
:wq
```

* 3.追加したら以下を実行して、プロファイルを読み込ませます。  
```
$ source ~/.bash_profile
```

* 4. 再度1項を実行して、utf-8に変更されたか確認します。  



## MySQLのインストール <a name="aSetup_mysql"></a>
MySQLをインストールします。  

*1. cygwin SETUPで必要なライブラリをセットアップする。  
	* mysql
	* mysql-common
	* mysql-server

*2. 以下コマンドを実行してインストールする。  

```
$ mysql_install_db

To start mysqld at boot time you have to copy
support-files/mysql.server to the right place for your system
～～～～～～
http://dev.mysql.com
Consider joining MariaDB's strong and vibrant community:
https://mariadb.org/get-involved/
```

*3. MySQLを起動する。  
```
$ mysqld_safe --datadir='/var/lib/mysql' &

$ ps -ef
     UID     PID    PPID  TTY        STIME COMMAND
   Korei    1773    1683 pty0     09:18:25 /usr/bin/ps
   Korei    1682       1 ?        09:07:10 /usr/bin/mintty
   Korei    1368       1 ?          May  2 /usr/sbin/nginx
   Korei    1369    1368 ?          May  2 /usr/sbin/nginx
   Korei    1683    1682 pty0     09:07:10 /usr/bin/bash
   Korei    1772    1710 pty0     09:18:02 /usr/sbin/mysqld
   Korei    1710    1683 pty0     09:18:00 /usr/bin/sh
```

*4. テストログインする。  
	初期はパスワードなし  
```
$ mysql -u root

Welcome to the MariaDB monitor.  Commands end with ; or \g.
Your MariaDB connection id is 8
Server version: 10.3.14-MariaDB Source distribution

Copyright (c) 2000, 2018, Oracle, MariaDB Corporation Ab and others.

Type 'help;' or '\h' for help. Type '\c' to clear the current input statement.

MariaDB [(none)]>


MariaDB [(none)]> exit
Bye
```

*5.rootのパスワードを変更する。  
```
$ mysqladmin -u root password '[パスワード]'
$ mysql -u root -p
Enter password:

Welcome to the MariaDB monitor.  Commands end with ; or \g.
Your MariaDB connection id is 10
Server version: 10.3.14-MariaDB Source distribution

Copyright (c) 2000, 2018, Oracle, MariaDB Corporation Ab and others.

Type 'help;' or '\h' for help. Type '\c' to clear the current input statement.

MariaDB [(none)]> exit
Bye
```

*6. 終了する。  
```
$ kill 1772
-bash: kill: (1772) - No such process
[1]+  終了                  mysqld_safe --datadir='/var/lib/mysql'

killコマンドは何度か実行する必要がある？
```

*6.設定ファイルのバックアップと変更。（エンコードの変更）  

```
エンコードの確認
$ mysql -u root -p
Enter password:

$ show variables like 'char%';


MariaDB [(none)]> status
--------------
mysql  Ver 15.1 Distrib 10.3.14-MariaDB, for CYGWIN (x86_64) using  EditLine wrapper

Connection id:          8
Current database:
Current user:           root@localhost
SSL:                    Not in use
Current pager:          stdout
Using outfile:          ''
Using delimiter:        ;
Server:                 MariaDB
Server version:         10.3.14-MariaDB Source distribution
Protocol version:       10
Connection:             Localhost via UNIX socket
Server characterset:    latin1
Db     characterset:    latin1


※Server、Dbが latin1 なので変更する。exitで抜ける。


設定ファイルのテンプレートをバックアップする
$ cp -p /etc/my.cnf.d/server.cnf /etc/my.cnf.d/server.cnf.org


設定ファイルを編集する
$ sudo vi /etc/my.cnf.d/server.cnf


以下を[mysqld]に以下を追加する。
[mysqld]
character-set-server = utf8


エンコードが変更されたことを確認する。

まずサービス起動
$ mysqld_safe --datadir='/var/lib/mysql' &

$ show variables like 'char%';

MariaDB [(none)]> status

--------------
mysql  Ver 15.1 Distrib 10.3.14-MariaDB, for CYGWIN (x86_64) using  EditLine wrapper

Server characterset:    utf8
Db     characterset:    utf8
```



## botで使うデータベース作成
botで使うユーザ、データベースを作成します。  


$ mysql -u root -p


### DB作成
mysql > CREATE DATABASE [データベース名] CHARACTER SET utf8;

mysql > CREATE DATABASE samafealdbot CHARACTER SET utf8;



### ユーザ作成

mysql > CREATE USER '[ユーザ名]'@'[ホスト名]' IDENTIFIED BY '[パスワード]';

mysql > CREATE USER 'samafealdbot'@'localhost' IDENTIFIED BY '8YALkVbloDOp';



### ユーザ権限付与

mysql > GRANT ALL PRIVILEGES ON * . * TO '[ユーザ名]'@'[ホスト名]';
mysql > GRANT CREATE, DROP, DELETE, INSERT, SELECT, UPDATE ON * . * TO '[ユーザ名]'@'[ホスト名]';

mysql > GRANT CREATE, DROP, DELETE, INSERT, SELECT, UPDATE ON * . * TO 'samafealdbot'@'localhost';





show databases;


select host, user from mysql.user;



show tables;





$ mysql -h localhost -u samafealdbot -p samafealdbot

Welcome to the MariaDB monitor.  Commands end with ; or \g.
Your MariaDB connection id is 13
Server version: 10.3.14-MariaDB Source distribution

Copyright (c) 2000, 2018, Oracle, MariaDB Corporation Ab and others.

Type 'help;' or '\h' for help. Type '\c' to clear the current input statement.

MariaDB [(none)]>









## botで使うデータベース作成
botで使うデータベースを作成します。  
	```
	# createuser -U postgres koreibot
	# createdb -U postgres -O koreibot koreibot
	パスワードはスーパーユーザ[postgres]のものです
	
	スーパーユーザ[postgres]でログインする
	# psql postgres -U postgres
	
	データベースのパスワードを設定する。
	=> alter role koreibot with password '[DBパスワード]';
	=> alter role koreibot with login;
	=> \q  
	この操作でDBのユーザ名、データベース名は koreibot になります。
	
	# psql -U koreibot koreibot
	[DBパスワード]でログインする
	
	=>
	
	=> \q
	　※エラーがでなければOKです
	```



4. botソースの管理アプリとしてWindows版のgithubデスクトップを使います。  
	1. githubデスクトップをインストールします。  
		　　[githubデスクトップ](https://desktop.github.com)  

	2. githubの自分のアカウントに本家リポジトリをFork（コピー）する。  
		　　[botリポジトリ](https://github.com/korei-xlix/koreibot_win)  
		の右上あたりの[Fork]ボタンを押してください。  
		すると、自分のアカウントに[自垢名 / koreibot_win]というリポジトリができます。  

	3. githubデスクトップで1項でForkしたリポジトリから自PCにクローンをダウンロードします。  
		githubデスクトップのCurrent repository→Add→Cloneを選択します。  
		任意のフォルダを選択してCloneを押してください。  

	4. 自分のブランチを作ります。  
		githubデスクトップのCurrent branch→New branchで任意の名前を入力します。  



## 初期起動
bashのコマンドラインを起動します。  
koreibotのカレントにショートカット koreibot.ch があるので、お使いください。  

```
$ bash koreibot.sh init
```

1. 以下を入力します。  
	```
	# cd [Koreibotのインストールフォルダ]
	# python run.py init
	```

2. データベースの全初期化と、ユーザ登録を実施します。画面に従って入力します。  
	以下の情報が必要となります。
	
	* koreibotのデータベースパスワード
	* Twitterアカウント名
	* Twitter Devで取ったAPI key
	* Twitter Devで取ったAPI secret key
	* Twitter Devで取ったAccess token
	* Twitter Devで取ったAccess token secret

**セットアップはここで完了です**  

3. botを起動します。  
```
$ bash koreibot.sh start
```
  
**起動すると、コンソール画面が起動します。**  

4. コンソールで初期設定を行ってください。  

* トレンドタグを設定してください。  
  設定しておくと、フォロワー、非フォロワー関わらず、いいねフォロワーの週間ランキングが発行できます。  

* VIPタグを設定してください。  
  設定しておくと、VIPユーザがこのタグでツイートした際に、botが自動リツイートします。  

* リスト通知を設定してください。  
  設定しておくと、フォロワー、非フォロワー関わらず、いいねした際にリスト通知を発行します。  
  Twitterでリスト通知用のリストを作成してください。  

* 自動リムーブを設定してください。  
  設定しておくと、フォローした際に相互フォローリストにフォロワーを追加します。  
  また、フォローされた場合、片フォロワーリストにフォロワーを追加します。  
  Twitterでフォロワーリスト、非フォロワーリストを作成してください。  

特に不要ならそのまま使用できます。  
  



# 起動方法 <a name="aStart"></a>
koreibotのカレントにショートカット koreibot.ch があるので、お使いください。  

```
$ bash koreibot.sh start
```

**起動すると、コンソール画面が起動します。**  
  

## オプション起動

以下は各調整用のオプション起動です。  

#### テストモード起動
	テストモードで起動します。  
	**開発時に使用ください。**  
	```
	# python run.py test [データベースhostname] [データベースname] [データベースusername] [データベースパスワード] [twitterアカウント名]
	```

#### ユーザセットアップ
	Twitterのアカウントを追加したり、APIを変更する際に使用ください。  
	```
	# python run.py setup [データベースhostname] [データベースname] [データベースusername] [データベースパスワード]
	
	一緒にキーワードを追加する場合
	# python run.py setup [データベースhostname] [データベースname] [データベースusername] [データベースパスワード] [ファイルパス名(相対パス)]
	```

#### 除外データの追加
	除外データを追加する際に使用ください。  
	除外データは以下のテキストを編集します。  
	```
	\datta\DEF_ExcWordArc
	
	プロフィール、ユーザ名の除外
	　　DEF_ExcUser.txt
	
	ツイート文の除外
	　　DEF_ExcWord.txt
	
	アクションリツイートのデータ
	　　DEF_ActionRetweet.txt
	```
	
	以下のコマンドでデータベースに追加されます。  
	```
	# python run.py add [データベースhostname] [データベースname] [データベースusername] [データベースパスワード] [twitterアカウント名] [ファイルパス名(相対パス)]
	```
  
	以下の場合、禁止ワードのみが追加されます。  
	```
	# python run.py word [データベースhostname] [データベースname] [データベースusername] [データベースパスワード] [twitterアカウント名] [ファイルパス名(相対パス)]
	```

#### 全初期化
	botのデータベースを全て初期化します。アップデートでDBの構成が変更された際に使用ください。  
	```
	# python run.py init [データベースhostname] [データベースname] [データベースusername] [データベースパスワード]
	```




# アップデート手順 <a name="aUpdate"></a>
botリポジトリのmasterから最新版をpullする方法です。  

1. githubデスクトップを起動します。  

2. 自分のKoreibotリポジトリを選択し、Current branchをクリックします。  

3. New branchをクリックし、バックアップ用のブランチを作成します。  
	名前はわかりやすいように。

4. ブランチを[main]に切り替えます。  

5. [Fetch Origin]をクリックします。  

6. [Puch]をクリックします。  
	ここまでで、自分のリポジトリの[main]と、自PCのソースに最新が反映されてます。  

> **もし不具合があったら...？**  
>	3項で保存したブランチに切り替えると、自PC側にアップデート前のソースが戻ってきます。  
>	以後、アップデートがあったら[main]に切り替えて[Fetch]すれば、修正後のソースが反映されます。  




# 機能説明 <a name="aFunction"></a>

botの各機能を以下に説明します。  
コマンドを実行するには、画面のプロンプトに指定のコマンドを入力します。  
コマンドは全て\マークの後、半角英字を入力します。  


## 基本機能
botに使うTwitterアカウントのフォロー者、被フォロワーの状態を記録したり、フォロワーからのいいね情報の記録、フォロワーへのいいね情報の記録をおこないます。  
いいねを受信する回数や頻度に応じて、自動的にフォローさせたり、頻度が低いアカウントをリムーブしてタイムラインの整理をおこなえます。  
また、通知リストを設定しておくことで、いいね受信時にリスト追加することで、botがいいねに反応したことを相手アカウントに通知させることができます。  
基本的に自動監視を実行することで処理させることができます。  


## ユーザレベル
botが認識した各ユーザは、状態やbot（アカウント）に対する振る舞いによってユーザレベルが付与されます。  
ユーザレベルによっては、botからのいいねの待遇が異なったり、レベルが付与された時点で自動フォロー、場合によってはリムーブなどの措置がとられます。  

|レベル  |説明  |
|:--|:--|
|A   |著名人など。自動リムーブしない。  |
|A+  |手動でVIP設定したアカウント。自動リムーブしない。  |
|B+  |相互フォローで、規定回以上トロフィーを獲得した。自動リムーブしない。  |
|B   |相互フォローで、トロフィーを1回以上獲得した。（獲得時既にフォロー済）  |
|C   |相互フォローで、トロフィーを1回以上獲得し、その時点でフォローした。  |
|C+  |相互フォローで、元フォロー者 もしくは 手動でリフォローした。  |
|C-  |相互時にリムーブされたことがある。（現フォローOFF）  |
|D   |自発的フォロー者。（現フォロー者ON・フォロワーOFF）  |
|D+  |botから自動フォロー。（現フォロー者ON・フォロワーOFF）  |
|D-  |自発的にリムーブした。（現フォロー者OFF・フォロワーOFF）  |
|E   |フォロワー。（現フォロー者OFF・フォロワーON）  |
|E+  |フォローしたけどリフォローしてもらえなかった。（現フォロー者OFF・フォロワーOFF）  |
|E-  |リムーブされたことがある。（現フォロー者OFF・フォロワーOFF）  |
|F   |非フォロワーでいいねされたことがある。あるいはいいねしたことがある。  |
|G   |フォロワーだけど完全スルーが過ぎたため無視している。  |
|G-  |追い出したことがあるフォロワー、Gからリムーブされた。  |
|L   |非フォロワーでリストだけ登録したことがある。  |
|Z   |ブロックされたことがある（あるいは継続中）。  |


## トロフィーの付与と、いいね情報の送信
リアクションチェックで、自分のツイートにいいね、リツイート、引用リツイート、メンションしたユーザ、回数を記録し、週間で一定回数のいいねをいただいたアカウントに対してトロフィーを付与します。トロフィーは入賞回数の数値です。トロフィー獲得したら、botがトロフィー獲得者のアカウント名をツイートします。（リプライなので目立ちません）
トロフィーが一定回数蓄積し、それでもフォロワーであり続けた場合、ユーザレベルが昇格して自動フォローされます。  
自動監視を実行することで処理させることができます。  


## 相互フォローリストと、片フォローリスト
botはユーザレベルにより該当ユーザの取り扱いを管理しますが、相互フォローリスト、片フォローリストを設定しておくことで、Twitterリストで確認、順位付けができます。  
自動監視を実行することで処理させることができます。  

#### 相互フォローリスト
自発的にフォローしたアカウント、相互フォローになったアカウントが追加されます。  
他のリストに追加されている、公式アカウントなどは対象外になります。  

#### 片フォローリスト
自発的にフォローしてない、かつフォロワー、もしくは相互フォロー時にリムーブされた、または自発的リムーブしたアカウントが追加されます。  
ここに追加されているアカウントは、少なくともフォロワーです。  


## リストフォローの警告
設定した任意のアカウントや、非フォロワーがリストをフォローした際に、botから自動的に警告ツイートが送信できます。  
送信後にリストフォローを解除されたとき、警告ツイートが自動削除されます。  
また、一定期間をおいてもリストフォローされたままの場合、ブロック→ブロック解除により追い出しがされます。警告ツイートも削除されます。  
自動監視を実行することで処理させることができます。  


## 自動監視【 \a 】
botの動作を1回だけ全て自動でおこないます。  
Twitter情報の取得、禁止ユーザの自動削除、古いいいねの解除、リスト登録チェック、リアクションチェック、リストいいね、フォロワー支援いいね、
いいね情報の送信、検索ワードいいね、古いユーザ情報の削除を一気におこないます。  


## キーワードいいね【 \kk 】
キーワードを含むツイートをしたユーザを抽出し、自動でいいねさせる機能です。  
コマンドを入力すると、キーワードいいねの管理画面が開きます。  
また、ここでキーワードを設定しておくと、自動監視で自動的に本機能が実行されます。  


## リストいいね【\fc】
予めbotにリスト情報を登録しておくことで、リストのタイムラインを取得し、自動でいいねさせることができます。  
コマンドを入力すると、リストいいねの管理画面が開きます。  
また、ここで設定しておくと、自動監視で自動的に本機能が実行されます。  


## ユーザ管理【 \u 】
ユーザ管理をおこなえます。管理状況、TwitterやDBの情報参照ができます。  
関係性をリセットしたり、情報を削除することもできます。  


## 警告ユーザ管理【 \uc 】
リストフォローにより警告されたユーザの管理がおこなえます。  
この画面から強制的に処置をさせることもできます。  


## ログ機能【\l】
運用ログや、ユーザ操作のログが表示できます。  
古いログを消して、CSVにバックアップを取らせることもできます。  

|コマンド  |説明  |
|:--|:--|
|\l   |異常ログを表示します。  |
|\lu  |ユーザ操作やユーザ規制に関するログを表示します。  |
|\lr  |システムの運用に関するログを表示します。  |
|\la  |全ログを表示します。  |
|\lt  |トラヒック情報を表示します。  |
|\lcr  |直近で新しいログを残して、古いログをCSVバックアップして削除します。  |
|\lall  |全ログをCSVバックアップして削除します。  |


## システム情報【\v】
botの全体設定や、botやpythonのバージョンが確認できます。  


## サブコマンドの呼び出し【\conf】
botのシステム設定を変更するためのサブコンソールを表示します。  
通常の運用ではあまり実行することはありません。  


## いいね全解除【\rm】
全てのいいねを解除します。  
解除には時間がかかる場合がありますので、通常は実行しないことをおすすめします。  


## トレンドタグ設定【\tc】
いいね情報を送信する際、設定するハッシュタグを設定します。  
名称は旧機能の名残ですので、気にしないでください。  


## リスト通知設定【\ic】
いいね通知リストの設定をおこないます。  
リスト通知のON/OFF、通知に使用するリストの設定をおこないます。  


## 自動リムーブ【\ac】
自動リムーブの設定をおこないます。
自動リムーブのON/OFF、相互フォローリストに使用するリストの設定、片フォローリストに使用するリストの設定をおこないます。  


## 禁止ユーザ【\uc】
禁止ユーザ、VIPユーザの設定をおこないます。  
禁止ユーザに設定されたユーザへはリアクションなどをおこなわないようになります。通報表示させて、検出時に目立たせることもできます。  
VIPユーザもはサブアカウントや、特殊なアカウントなどに利用できます。リアクションをおこなわないようにしますが、一方的にいいねすることができます。  
さらにVIPユーザのタイムラインを監視させて、リアクションチェックをおこなうこともできます。  


## Twitter APIの変更【\apiconf】
TwitterのAPI情報を変更します。何か変更があった場合にご使用ください。  





# 本リポジトリの規約 <a name="aRules"></a>

* 素材の改造、流用、配布について。  
  * 当ソースの改造、改造物の配布は自由にやってください。  
    その際の著作権は放棄しません。  
  * 未改造物の再配布、クローンしたあと未改造のまま放置することは禁止とします。  
  * 本リポジトリのファイル構成を変えると正常に動作しなくなります。  
    改造の際ご注意ください。  
  * 使用の許諾、謝辞については不要です。

* 著作権について。
  * 本リポジトリはフリーウェア規約に準拠します。  
  * 著作権は放棄しません。
  * 別に著作権表記のある素材の利用については、各自で許諾を取得ください。  

* 免責事項について。
  * 当ソースを使用したことによる不具合、損害について当方は責任を持ちません。  
    全て自己責任でお願いします。  
  * 著作権表記のある素材の再利用により発生したトラブルについては、  
    当方は責任を負いません。各自でご対応ください。  
  * Web上やSNS上、オンライン上で発生した、わたしが関知していないトラブル、損害については、  
    一切責任を負いません。各自でご対応をお願いします。  

* 当ソースの仕様、不具合についての質問は受け付けません。  
  自己解析、自己対応でお願いします。  

* ご意見、ご要望については、開発者ホームページを参照ください。  
  誠意あるメッセージ、ご要望については、励みになります。  




# 参考記事 <a name="aReference"></a>
**※敬称略**  
* [Windows 上の Python で UTF-8 をデフォルトにする（methane）](https://qiita.com/methane/items/9a19ddf615089b071e71)




***
::Project= Korei bot  
::Admin= Korei (@korei-xlix)  
::github= https://github.com/korei-xlix/  
::Homepage= https://koreixlix.wixsite.com/profile  
