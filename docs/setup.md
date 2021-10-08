# セットアップ
## 1. Googleドライブを開く
- Googleにログインし、Googleドライブを立ち上げる。
## 2. Google Colabの作成
- マイドライブで右クリックし、Google Colabを新規作成する。
- もしなかったら、`アプリを追加`からGoogle Colaboratoryをインストールしてページを更新すれば表示される。
![colab](https://github.com/gran27/Y_meiji_GoogleColab/blob/main/figs/googlecolab.png)
## 3.Googleドライブのマウント
- Google Colabが開いたら、横に三つ並んでいるアイコンの一番右を押し、Googleドライブをマウントする。
![mount](https://github.com/gran27/Y_meiji_GoogleColab/blob/main/figs/mount.png)
- できないときは以下のコマンドを実行する。`Go to this URL in a browser`の横のURLから`Enter your authorization code`に認証コードをコピぺする。
```
from google.colab import drive
drive.mount('/content/drive')
```
## 4. コードの実行
- 以下のコードをまとめてコピペで入力し、再生ボタンで実行する。
```
WORKING_DIR = '/content/drive/MyDrive'
#!mkdir $WORKING_DIR
%cd $WORKING_DIR
!git clone https://github.com/gran27/Y_meiji_GoogleColab
```
![command](https://github.com/gran27/Y_meiji_GoogleColab/blob/main/figs/setup_command.png)
## 5. GPUに変更
- 処理が速くなるようにGPUを使う。
- 先ほどのGoogle Colabの編集>ノートブックの設定>ハードウェアアクセラレータのところをGPUに設定する。
![GPU](https://github.com/gran27/Y_meiji_GoogleColab/blob/main/figs/notebook.png)
![GPU](https://github.com/gran27/Y_meiji_GoogleColab/blob/main/figs/gpu.png)
## 6. 確認
- Googleドライブに戻り、マイドライブにY_meiji_GoogleColabフォルダができていれば完了。
- Google Colabは消してもOK
