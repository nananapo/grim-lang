# grim-lang

![Python application](https://github.com/nananapo/grim-lang/workflows/Python%20application/badge.svg)


## What's grim-lang



プログラムは上から実行されます。

この文章も上から読んでください



#### 文字列

grimは、"か'で囲まれた部分を文字列と認識します。

> "Hello World!"



文字列の途中での改行も可能です。

>"
>
>1
>
>2
>
>3
>
>ダー！
>
>"



文字列中に、文字列の開始記号を含めるには、\を利用します。

> " \\"で文字を囲んだらコメントになります "



改行のための制御文字を表す記号はありません。



#### 数値

プログラム中に入力された数字は、同名の関数や変数が無い場合には数値として扱われます。(詳細は後述)

> 100000



#### 入出力

標準入出力を行う関数が用意されています。

* input
* output



#### 演算子の欠如

この言語には、 =+-*/ などの一般的な演算子は全く定義されていません。(詳細は後述します)

その代わりに、同等の機能を持つ以下の関数が用意されています。

- __assign
- __plus
- __minus
- __mul
- __div



#### 関数の呼び方

関数を呼ぶには、関数の名前を記述します。

> 関数名()

引数が無い場合は、括弧を省略することができます。

関数名と括弧の間にスペースを入れることはできません



##### 引数の指定

> 関数名(引数1 引数2 引数3)

引数を区切るために,をつけたりする必要はありません。(詳細は後述します)



#### 関数の定義

grimでは、3種類の関数を定義することができます。

- fun
- opf
- opm
- opb



最初にfunで定義できる通常の関数について説明します。



関数の定義方法

> fun 名前(引数1 引数2 引数3...)
>
> 処理
>
> end



なお、引数が無い場合は、括弧を省略できます。

> fun 名前
>
> 処理
>
> end

引数がある場合は、名前の直後に括弧を記述する必要があります。



また、可読性を考慮しないならば、以下のように書くことも可能です。

> fun 名前 処理 end

ただし、funと名前、処理、endの間にはスペースが必要です。



##### 値を返す

関数内でreturn関数を実行することによって、処理をそこで終了することができます。

> fun test
>
> ​	処理1
>
> ​	return
>
> ​	実行されない処理
>
> end

return関数に引数を指定することによって値を返すことができます。

引数は何個でも入れられますが、返されるのは最初の値のみです(引数での計算は実行されます)。



return関数を使わずに最後まで到達した場合、最後の処理の結果が返されます。

> fun test
>
> ​	__plus(1 2)
>
> end

上の場合、__plus(1 2)の値3が返ります。



処理が無い場合はVariableNoneという特別なものが返されます。(詳細は後述)

よって、全ての関数は何らかの値を返します。



##### 関数の定義とプログラムの実行

プログラムは上から実行されますが、関数の定義はそれより先に行われます。

> test
>
> fun test
>
> ​	print("test is here")
>
> end

上の場合、testが見つからないというエラーは起こりません。



##### 関数の中に関数を定義する

関数の中に関数を定義することができます。

> parent
>
> fun parent
>
> ​	sub1
>
> ​	sub2
>
> ​	fun sub1
>
> ​		print("sub1")
>
> ​	end
>
> ​	fun sub2
>
> ​		print("sub2")
>
> ​	end
>
> end

上の場合、parentが実行され、sub1、sub2が実行されます。



内部的には、今まで書いてきたプログラム自体がmain関数(呼ぶことはできない)の中に記述されているように扱われています。



### 演算子の定義

grimでは演算子が全く定義されていませんが、新しく関数として定義することができます。



##### 演算子の種類

演算子は3種類あります。

* 前置演算子
* 中置演算子
* 後置演算子



前置演算子は、

> 演算子 右辺

とあったときに、右辺の値を受け取って1つの値を返す関数です。



中置演算子は、

> 左辺 演算子 右辺

とあったときに、左辺と右値を受け取って1つの値を返す関数です。



後置演算子は、

> 左辺 演算子

とあったときに、左辺の値を受け取って1つの値を返す関数です。



##### 演算子関数の定義



前置演算子は次のように定義できます。

> opf 優先順位 演算子名(引数1)
>
> ​	処理
>
> end



中置演算子は次のように定義できます。

> opm 優先順位 演算子名(引数1 引数2)
>
> ​	処理
>
> end



後置演算子は次のように定義できます。

> opb 優先順位 演算子名(引数1)
>
> ​	処理
>
> end



##### 演算子の利用

> op2 tasu(v1 v2)
>
> ​	__plus(v1 v2)
>
> end
>
> print(1 tasu 2)

上では、2つの値を足す"tasu"という名前の演算子を定義しています。



printの中で、

> 1 tasu 2

という様に記述していますが、これは

> tasu(1 2)

と等価です。



#### 演算子の優先順位

演算子には優先順位があります。



##### 処理の区切れ

grimでは、funやend、括弧以外に文(処理)を分割する記号はありません。

grimの処理系では、演算子によってプログラムを解釈しています。



> 以後、+は中置、!は前置演算子
>
> A + B C + D

この場合、A+BとC+Dの間にそれを結ぶ演算子が無いため、二つの独立した処理として扱っています。



> A + B ! C+D

この場合、A+BとC+Dの間に!演算子がありますが、!演算子は右の値と結合するので、二つの独立した処理として扱います。

関数を呼ぶときの引数の区切れも同じ原理で分割し、前から順に引数に割り当てています。





また、**全ての処理は、演算子とその対象の間にスペースを空ける必要があります。**

>A*B 

これは、AとBの間に中置演算子があるように見えますが、grimではA*Bという名前の変数の参照/引数なし関数の呼び出しとして扱われます。




なお、優先順位を上げるために括弧を付けた場合、最初/最後の括弧と値の間にスペースはいりません。

> ( 1 + 2 )
>
> (1 + 2)  ← これでもOK



##### 計算の順序

計算の優先順位は、

> 括弧 > 関数 > 後置,前置演算子 > 中置演算子

と定められています。




式に括弧が含まれていると、左の括弧から順に計算されます。

括弧の中に独立した複数の式がある場合、すべてを計算した後、最後の値を括弧の値として扱います。

> ( 1 + 2 3 + 5 ) 

上の場合は括弧の値は8になります。




値が関数だった場合、引数が計算された後、関数が実行されます。

> fun hoge()
>
> ​	return ("hoge")
>
> end
>
> print(__plus(hoge() "fuga") ← hogefugaと出力される

値は関数の返り値になります。




演算子の説明の前に、以下のような演算子を定義していることとします。

>演算子の種類 : 演算子 : 優先順位 : 操作
>
>中置 : = : 0 : 左辺に右辺を代入して右辺を返す。
>
>中置 : + : 1 : 左辺と右辺を足して結果を返す。
>
>中置 : \- : 1 : 左辺から右辺を引いて結果を返す。
>
>中置 : * : 2 : 左辺に右辺をかけて結果を返す。
>
>中置 : / : 2 : 左辺を右辺で割って結果を返す。
>
>前置 :  plus1 ; 2  : 右辺に1を足して結果を返す。
>
>後置 : div5 : 1 :  左辺を5で割って結果を返す。



後置/前置演算子は、優先順位によって順次計算されていきます。

> plus1 4 div5

上の場合、優先度2のplus1が先に実行され、優先度1のdiv5が次に実行されます。




なお、**優先順位は絶対値で扱われます。**

> opf 10 test1(va1) end
>
> opb -10 test2(va1) end

上の場合、優先順位は同じです。




また、複数個演算子がある場合、値に一番近い前置演算子と後置演算子が比較されます。

> plus1 plus1 plus1 plus1 21 div5 div5

上の場合の処理の流れは以下の通りです。

>plus1 plus1 plus1 22 div5 div5
>
>plus1 plus1 23 div5 div5
>
>plus1 24 duv5 div5
>
>25 duv5 duv5
>
>5 div5
>
>1




**左右ともに同じ優先度の場合、前置演算子が優先されます。**




##### 中置演算子の順序

中置演算子の計算順序も優先順位が考慮されます。

ただし、**前置/後置演算子と同じように優先順位は絶対値で扱われますが、0以下かそれ以外かで動作が変わります**。




優先順位が0以下の場合、右から演算が行われます。

> a = b = 1

上の場合、まずb=1が実行されます。=は左辺値を返すので

> a = 1

となり、aに1が代入されます。




優先順位が0より大きい(0を含まない)場合、左から演算が行われます。

> 1 + 2 + 3

上の場合、まず1+2が実行されます。+は足した結果を返すので、

> 3 + 3

となり、この文は6を返します。




**優先順位が同じで、演算の方向が違う演算子が複数個ある場合、左から演算されます。**




#### 変数

変数は、値の入った名前がある箱です。



##### 代入可能な値

変数には以下のものを代入できます

* 文字列
* 数値
* 真偽値
* VariableNone
* 名前
* 不定



##### 文字列

上記の、"か'で文章を囲むことによって実現できるものです。

ビルトイン関数の__strを利用することで、数値を文字列に変換することができます。

> __str(1000) ← 数値1000は文字列1000に変換される


また、index番目の文字を取り出す関数、__strinが用意されています

> 使い方 : __strin(string index)
>
> __strin("abcde" 0) ← a
>
> __strin("abcde" 5) ← a
>
> __strin("abcde" -5) ← a


##### 数値

数値を表すものです。

ビルトイン関数の__numを利用することで、文字列を数値に変換することができます。

>  __num("-10000") ← 文字列"-10000"は数値の-10000になる

##### 真偽値

真偽値はTrueまたはFalseの状態を持つものです。

ビルトイン関数の__trueでTrue、__falseでFalseのBooleanを取得できます。
> a = __true() ← aにTrueが代入される

二つのものが等しいか調べる__equal、一つ目の数値が二つ目の数値より大きいか調べる__largerでもBooleanを取得できます。
> __equal("hello" "hello") ← True
> __equal("1" 1) ← 型が同じでない場合はFalse
> __equal(__true() __false()) ← False

> __larger(3 1) ← True
> __larger("a" "b") ←数値でないのでエラー

後述のif文を組み合わせることで、>=演算子などを作れるようになります。


##### VariableNone

関数が値を返さない場合にのみ使用される特別な値です。直接指定することはできません。

なにもないことを示します。



#### 変数の定義

名前と不定を説明する前に、変数の定義方法を説明します。

grimには変数の宣言をするキーワードや演算子が無いため、その代わりに関数を使います。

> __assign(変数名 値)

変数名には、直接名前を入力するか、名前の変数を使います。



##### 名前

#TODO 名前周りが非常に言語仕様が曖昧

名前は、値ではなく名前を持ちます。

上記の__assignでは、名前、不定、数値、文字列のどれかを1つめの引数に指定することで、名前なら保存している名前の変数名に、文字列、数値ならその値に引数2の値を割り当てます。


関数を定義するときに引数名の頭に;をつけることで、名前を受け取るような引数を明示的に作ることができます。

> op2 =(;target value)
>
> ​	__assign(target value)
>
> end

上では、左辺の名前に右辺の値を割り当てるような中置演算子=を定義しています。また、演算の結果としては、valueを返しています。

ここから下のプログラム例では、上記の=演算子を利用します。



実際に=を使ってみると、

> aisatu = "Hello World"

この場合、nameにはaisatuという名前が入ります。

valueには"Hello World"という文字列が入っているので、__assignによってaisatuに文字列が代入されます。



一つ目の引数は;nameと指定されていますが、これは;nameという名前の変数ではなくnameという名前の変数になることに注意してください。



次に、変数はどのスコープで名前を束縛されるかについて説明します。



#### スコープ

grimでは、基本的に静的スコープを採用しています。



> name = "John"
>
> fun who
>
> ​	print(name)
>
> end

この場合、whoを実行すると、その上位の関数mainに定義されたnameを参照し、Johnと表示します。



##### 動的スコープの明示

変数を参照するとき、変数名の頭に:をつけることによって動的スコープを利用することができます。

> fun sub1
>
> ​	print(:name)
>
> end
>
> fun sub2
>
> ​	name = "John"
>
> ​	sub1
>
> end

この場合、sub1を実行するとnameが見つからずエラーが出ますが、sub2を実行するとJohnと表示されます。



##### 変数,関数の捜索順序

引数が無い関数の呼び出しと、変数の参照は見分けがつきません。システムは、変数、関数の順に検索します。

名前が関数であることが明示されている場合、関数のみをスコープの設定に応じて検索します。



引数が無い関数の呼び出しの後ろに括弧を書くことで、それが関数の呼び出しであることを明示することができます。

> fun test
>
> end
>
> test()



変数と関数が見つからなかった場合、ビルトイン関数、数値の順に確認します。それでも分からなかった場合は見つからなかったと結論を出します。



##### 名前の演算

名前は、__assignの引数として利用される以外にも使い道があります。

> fun test(va1 va2 ;lambda)
>
> ​	print(lambda(va1 va2))
>
> end
>
> fun +(va1 va2)
>
> ​	__plus(va1 va2)
>
> end
>
> test(1 2 +)

名前の演算は、名前を参照します。上の場合、3と表示されます。



##### 不定

これは変数が見つからないときに一時的に利用されます。演算はできません。



> name = 3

上の場合、=の一つ目の引数に指定された変数nameは、まだどこにも定義されていません。

しかし、システムは変数が見つからなくてもすぐにエラーを出すことはなく、name=3が書かれているスコープで、nameを不定に束縛します。

=の引数に値を渡すときに、不定のnameは不定ではなく、名前がnameな名前を渡します。

処理の終了時に不定が残っている場合、エラーを出します。



#TODO 不定の明示



#### 制御構文

grimでは評価式がtrueの時にのみ式が実行される、if文があります。

> if (評価式)
>
>   Trueの時のみ実行される処理
>
> end

if文は関数と同様に、最後の式の値を返します。

if文が実行されなかった場合はVariableNoneが返されます。

if文の中でreturnを使うと、if文はその値を返します。
> if (__true)
>
>   return(__false)
>
> end

関数の中にif文を書き、その中でreturnしても、関数は終了しません。
>fun test
>
>   if(__true)
>
>       return(__false)
>
>   end
>
>   ここも実行される
>
>end


#### コメント

プログラム中にコメントを書くための文字はありません。

ただし、次のように自分で似たものを作ることができます。

> opf ←(value) end
>
> 処理 ← "コメント" 

#### 命名規則

* 変数名

1. )(:;の使用禁止
2. 空白はダメ

* 関数名

1. )(:;の使用禁止
2. 空白はダメ

