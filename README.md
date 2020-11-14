# grim-lang


おそらくレポート用


## What's grim-lang

* 変数名/関数名はfun,end,(+-*/%=以外なら何でもOK

  > 0=1
  >
  > print(1/0) #1÷1なので1.0と出力される

  参照順序は 変数 -> 関数 -> ビルトイン関数 -> 数字 なので注意

* 関数を呼ぶ/宣言するとき、引数が無い場合は括弧を省略可

  > #引数あり
  >
  > name = input("what's your name?")
  >
  > #引数なし
  >
  > print("what's your name?")
  >
  > name = input

  括弧を省略しない場合は、括弧は関数名の直後に必要。

  変数名と同じ名前の関数を呼ぶときは、引数が無くても()をつけて呼ぶ必要がある

* 関数の返り値を指定しない場合、最後の式が返される

  > #返り値を指定しない
  >
  > fun cool(name)
  >
  > ​	name + "kana is very cool" #この式が返される
  >
  > end
  >
  > #返り値を指定する
  >
  > fun cool(name)
  >
  > ​	return(name + "kana is very cool")
  >
  > end

* 全ての処理が式 / 全ての式は値を返す

  > japanese =  "Konnitiha" #変数japaneseにKonnnitihaが代入され、 式は右辺の結果を返す
  >
  > "Hello" #文字列Helloが返される



## ビルトイン関数

* main() 返り値:未定義
* input(表示したい式を何個でも) 返り値:入力
* print(表示したい値を何個でも) 返り値:なし
* return(返したい式を一個) 返り値:なし(実行時に式の実行は強制終了されて引数を返す)

## TODO

- [ ] 名前空間

- [ ] 比較記号 , Bool & ! == !=

- [ ] マイナス符号

- [ ] 配列 ex. array[index]

- [ ] if / else / elif

- [ ] 演算順序,演算用の括弧

- [ ] 引数のデフォルト値

- [ ] インタラクティブな実行

- [ ] エスケープシーケンス , 変数を括弧でくくって文字の中に書く記法

- [ ] 参照渡し

- [ ] 関数を実行するときに名前空間を共有する?オプション

- [ ] マルチバイト文字がおかしい

- [ ] コメント #

- [ ] printよりputかな..?(inputだし)

- [ ] 明示的に整数/文字にする関数 , キャストする関数

- [ ] += -= *= /=

- [ ] %

  