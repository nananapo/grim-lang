
class BuiltIn:

    #ビルトイン関数 TODO 演算
    BUILT_IN_FUNCS = set([
        #入出力
        "input",
        "print",
        #終了して値を返す
        "return",
        #特別な関数
        "__assign",
        "__plus",
        "__minus",
        "__mul",
        "__div"
        #TODO int string number
    ])

    MARK = set([
        "",":",";",")"
    ])