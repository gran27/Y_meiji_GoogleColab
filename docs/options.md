# Options
オプションとは実行するときに設定することで、プログラムを変更せずに値を簡単に設定できるものである。  
本プログラムのオプションは5つある。
## 基本のコマンド
- 基本は以下のように実行すればよい。
- **Google Colabでは実行するとき`!`を先頭につける必要があるので注意**
- 動画ファイル名は実行するとき必ず必要である。
```
# python run.py {ファイル名}  
# 例
python run.py data/XXXXX.MTS
```

## オプション
### output
- `-o`または`--output`で結果のファイル形式を選べる。
- あまり使わないかも
- csvかtxtのみ対応。
- デフォルトはcsv
```
# python run.py {ファイル名} {-o 形式}  
# 例（txt形式で出力したいとき（どっちでもOK））
python run.py data/XXXXX.MTS --output txt
python run.py data/XXXXX.MTS -o txt  
# 例（何も設定しないときはデフォルトのcsvになる）
python run.py data/XXXXX.MTS
```
### shift
- `--shift`で動画の何秒後から評価するかを設定できる。小数で指定可能。
- **マウス検出の精度の問題上、マウスを置く時間をあらかじめ確認しておいて、なるべく設定するようにしてほしい。**
- デフォルトは0秒（はじめから8分間評価する）
```
# python run.py {ファイル名} {--shift 小数}  
# 例（動画を0:05.5のところから評価するとき（8:05.5まで評価される））
python run.py data/XXXXX.MTS --shift 5.5  
# 例（何も設定しないときはスタートから8分間評価する）
python run.py data/XXXXX.MTS
```
### outspeed
- `--outspeed`で結果の動画を何倍速にするか設定できる。**自然数のみ設定可能（小数は対応していない）**
- 動画の容量を小さくしたいときや確認作業で役立つかも？
- デフォルトは1（等速）
```
# python run.py {ファイル名} {--outspeed 自然数}  
# 例（結果の動画を2倍速で保存したいとき）
python run.py data/XXXXX.MTS --outspeed 2
# 例（何も設定しないときは等速の動画が保存される）
python run.py data/XXXXX.MTS
```
### yth
- `--yth`でY迷路の検出精度を多少変えられる。**0.1以下の小数で設定すること。**
- 例えば0.05にすると2倍の量のフレームから検出するので精度が期待できる分、処理も2倍の時間がかかる。
- 0.01～0.1くらいで設定するのがオススメ。
- デフォルトは0.1
```
# python run.py {ファイル名} {--yth 小数}  
# 例
python run.py data/XXXXX.MTS --yth 0.05
# 例（何も設定しないときはデフォルトで処理）
python run.py data/XXXXX.MTS
```
### weights
- `--weights`でマウスの検出モデルを設定できる。
- これは新しいモデルを作った時に設定するぐらいだと思う。
- 一応、今後のために用意した。
- デフォルトは`model/best.pt`
```
# python run.py {ファイル名} {--weights モデルのパス}  
# 例（best2.ptをモデルに使いたいとき）
python run.py data/XXXXX.MTS --weights model/best2.pt
# 例（何も設定しないときはmodel/best.ptで処理、普段はこれでOK）
python run.py data/XXXXX.MTS
```
## オプションの組み合わせ
- 以上のコマンドは組み合わせて使えるので希望に合わせて設定する。
- オプションを指定するとき順番は気にしなくていい。（`--shift 4 --yth 0.05`でも`--yth 0.05 --shift 4`でも問題なし）
```
# 例（00001.MTSの解析で、スタートから9秒の位置から解析し、3倍速の動画を出力し、Y迷路の検出精度を少し上げたいとき）
python run.py data/00001.MTS --shift 9 --outspeed 3 --yth 0.03
```
