＜格納ファイルの概要説明＞
ここに格納されているファイル類は、
pythonを用いて、さまざまな日付のフォーマットを
yyyy-mm-ddの日付型に変換するスクリプトと、pytestによるテストスクリプト、
そのスクリプトを実行するためのDocker実行環境の設定ファイルになります。
丸ごとcloneして、ローカルのDockerにて、
設定ファイルを元にDockerイメージ・コンテナ作成を行うことで、
ローカルのDocker実行環境にて、スクリプトのテストを行うことができます。
※ローカルに、docker(docker-desktop)がインストールされている必要があります。


＜各ファイルの説明＞
/docker-python
docker-compose.yml ：Docker Composeの設定ファイル
Dockerfile ：Dockerイメージの設定ファイル

/task
data_file.csv ：日付フォーマット変換テストデータのcsvファイル
taskformat_use_pandas.py ：pandasライブラリを使用した日付フォーマット変換スクリプト
taskformat.py ：最初に作成した日付フォーマット変換スクリプト
testpython_fromfile.py  ：pytest実行スクリプト
wareki_data.csv  ：和暦データ変換用データのcsvファイル


＜日付フォーマット変換スクリプトについて＞
taskformat.py・taskformat_use_pandas.py
どちらのスクリプトも、
 $ python スクリプトファイル名.py
にて、単体で実行できます。
(その場合は標準入出力を使用して、
スクリプト実行後、
標準入力：変換前文字列を入力で、
標準出力：変換後文字列の出力となります。)

pytest(testpython_fromfile.py)での実行時は、
 $ pytest -v testpython_fromfile.py --durations=0
にて、両スクリプトとも実行され、
テストデータの入力として、data_file.csvを使用して、
taskformat.py -> test_2関数に対応
taskformat_use_pandas.py -> test_1関数に対応
という形でテスト実行されます。


どちらのスクリプトも、対応できる日付のフォーマットとして、
数字が(区切り文字などで区切られていても、)
年月日の順で並んでいる必要があります。
対応できる年の桁数については、
４桁もしくは、２桁となっていますが、
taskformat.pyについては、
1000 <= 年数 <= 9999
となっており、
taskformat_use_pandas.pyについては、
1678 <= 年数 <= 2262
となっています。
2桁の年数については、どちらも、
73(年) -> 2073(年)
74(年) -> 1974(年)
と解釈して、変換を行います。



＜Docker実行環境について＞
実行環境：
Docker image - amazonlinux:latestを元にして作成
container_name - 'pythontest'
pyenv - python 3.12.4 (pyenv - local)
container login user - root
working_dir - /root/opt/task
mountdir - docker-python/task -> /root/opt/task



＜ローカルのDockerで、実行環境を作成してテストを実行する際の操作手順＞

1.docker-pythonフォルダをgit-hubより、ローカルの任意のフォルダにcloneする。

2.ローカルのdocker(docker-desktop)を起動した状態で、コマンドライン(ターミナル・コマンドプロンプト等)で、
  ローカルにcloneしたdocker-pythonフォルダへ移動
  $ cd (cloneしたフォルダまでのパス)/docker-python

3.Docker設定ファイルを元に、Dockerイメージを生成すると同時に、それを元にしたコンテナを作成・起動する。
  コマンドラインにて、
  $ docker compose up -d --build

4.生成されたDockerイメージと、コンテナの状態を確認する。
  $ docker image ls
  $ docker container ls
  
5.起動したコンテナ(pythontest)にログインする。(以降のコマンドライン操作は、自動的にコンテナ内操作に切り替わります。)
  $ docker compose exec pythontest bash

6.コンテナ(pythontest)内にて、pytestを実行する。(コンテナログイン時のディレクトリ「/root/opt/task」 で、そのまま実行します。)
  (Docker内)$ pytest -v testpython_fromfile.py --durations=0
  
  test_1 : taskformat_use_pandas.py のテスト
  test_2 : taskformat.py のテスト
　
　※下記のようになっていれば、テスト成功です。


======================================= test session starts ========================================
　　　　　　　　　　　　　　　　　　　　　　　　　　　　(中略)
testpython_fromfile.py::test_1 PASSED                                                        [ 50%]
testpython_fromfile.py::test_2 FAILED                                                        [100%]

============================================= FAILURES =============================================
______________________________________________ test_2 ______________________________________________

　　　　　　　　　　　　　　　　　　　　　　　　　　　　(中略)

===================================== short test summary info ======================================
FAILED testpython_fromfile.py::test_2 - AssertionError: assert '2024-06-05' == None
=================================== 1 failed, 1 passed in 0.70s ====================================

7.テスト実行が完了し出力内容の確認を行ったら、コンテナ(pythontest)からログアウトします。
  (Docker内)$ exit
  
8.ログアウトした後も、コンテナ自体は起動しているため、
  コンテナを停止する場合は、(コンテナ自体の削除は行わない場合、)
  $ docker stop pythontest

  停止後、再度、起動する場合は、
  $ docker start pythontest 
  (起動後、ログインする場合は、再度、
  $ docker compose exec pythontest bash)
  
  起動しているコンテナを停止して、削除する場合は、
  $ docker compose down
  
9.コンテナ削除後も、生成したDockerイメージは残っているため、
  再度、コンテナを作成・起動する場合は、
  $ docker compose up -d 
  
  生成したDockerイメージ自体を削除する場合は、
  $ docker image ls
  にて、削除するDockerイメージのimageidを確認して、
  
  $ docker image rm [imageid]
  にて、対象のDockerイメージの削除を行います。



※コンテナやDockerイメージを削除しても、設定ファイル(docker-compose.yml・Dockerfile)や、
　マウントしているフォルダ(docker-python/task)やその中のファイルは、残りますので、
　再度、docker-pythonフォルダで、
　$ docker compose up -d --build
　を実行することで、Dockerイメージ・コンテナの作成・起動が可能です。



