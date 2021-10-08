# Y-meiji for Google Colab
本プログラムは[以前のY-meiji](https://github.com/gran27/Y_meiji)の改良版である。
GPUを使うためGoogle Colab用に改良したので、ローカル上でのセットアップは必要ない。
## Contents
* [Quick Start](#quick-start)
* [How To Use](#how-to-use)
* [Update History](#update-history)
## Quick Start
- 初回のみ[setup.md](docs/setup.md)を見てセットアップする。
## How To Use
**コマンドはすべてあらかじめ入力してあるので、それを利用すればよい。再生ボタンを押すと実行できる。**
### 1. 動画ファイルをdataフォルダに入れる
- セットアップを済ませたアカウントでGoogleにログインし、Googleドライブを立ち上げ、動画ファイルをアップロードしておく。
- MTS形式でも動作する。
### 2. `run.ipynb`の起動
- Y_meiji_GoogleColabフォルダ内の`run.ipynb`をダブルクリックで開く。
### 3.Googleドライブのマウント
- Google Colabが開いたら、横に三つ並んでいるアイコンの一番右を押し、Googleドライブをマウントする。
- 完了したら一応真ん中のアイコンを押して更新しておく。
- エラーが出ず、下の図のようにdriveフォルダが表示されたらOK。
![mount](https://github.com/gran27/Y_meiji_GoogleColab/blob/main/figs/mount.png)
- できないときは以下のコマンドを実行する。`Go to this URL in a browser`の横のURLから`Enter your authorization code`に認証コードをコピぺする。
```
from google.colab import drive
drive.mount('/content/drive')
```
- もし、「セッションが多すぎます」と出たら、`セッションの管理`を押してすべてのセッションを`終了`させる。そして、右上の`接続`を押す。
### 4. 下準備
実行の前に以下のコマンドを実行する。これはGoogle Colabを開いたときにやる。複数の動画を解析するときは毎回やらなくてOK。
```
%cd drive/MyDrive/Y_meiji_GoogleColab
%pip install -qr requirements.txt
```
### 5. 実行
- **GPUになっているか確認すること。やり方は[setup.md](docs/setup.md)の5を参照。**
- オプションの使い方は[options.md](docs/options.md)を参照。
- 例）00892.MTSを開始9秒の位置から評価、結果の動画を2倍速にしたいとき
```
!python run.py data/00892.MTS --shift 9 --outspeed 2 --yth 0.1 --weights model/best.pt
from IPython.display import Image,display_jpeg
display_jpeg(Image('result/00892.jpg'))
```
#### 注意
- -sオプションの数字はマウスを置いた瞬間に合わせること。この時間から8分がカウントされる。
- 開始位置から動画の長さが8分もないときはプログラムが中断される。  
  - 例）動画の長さが8分5秒で`python run.py data/XXXXX.MTS --shift 10`と実行したとき
#### Y迷路の予測の確認
- Google Colabでは予測をすぐに確認できない。そのため「resultフォルダ内の画像を確認しましたか？」と表示されたところで`n`と入力し、大丈夫であるか確認すること。
- 大丈夫であれば`y`と入力する。
- 予測がずれている場合、`--yth`のあとの数字を0.05など少し小さくすると治ることがあるので、再実行して試すとよい。詳しくはオプションの使い方[options.md](docs/options.md)を参照。
- 手動の調整はなしに変更済み
![input](https://github.com/gran27/Y_meiji_GoogleColab/blob/main/figs/yes_no.png)
- 良い例
![example_Y](https://github.com/gran27/Y_meiji_GoogleColab/blob/main/figs/points_auto.png)
- 悪い例
![example_Y](https://github.com/gran27/Y_meiji_GoogleColab/blob/main/figs/points_auto_bad.png)
### 5. 解析を待つ
- 解析中は特に何も表示されないので、気長に待つ。だいたい12分くらいかかる。
- 停止ボタンで中断することができる。resultフォルダに結果がcsvかtxt形式で、動画がmp4で、Y迷路の予測がjpgで保存されている。
![example](https://github.com/gran27/Y_meiji_GoogleColab/blob/main/figs/ex_show.png)
- 中央の赤い円の内側にマウスがいる時は追跡しない。
![red circle](https://github.com/gran27/Y_meiji_GoogleColab/blob/main/figs/incircle.png)

## Update History
- 2021/10/01 ざっくり作成
- 2021/10/04 8分に対応、Y迷路のほぼ自動認識の実装
- 2021/10/05 コードの整理
- 2021/10/06 モデルの作成
- 2021/10/08 Google Colab用に修正
