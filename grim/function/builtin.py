class BuiltIn:

    # ビルトイン関数
    BUILT_IN_FUNCS = set([
        # 入出力
        "input",
        "print",
        # 終了して値を返す
        "return",
        # 特別な関数
        "__assign",
        "__plus",
        "__minus",
        "__mul",
        "__div",
        # キャスト
        "__num",
        "__str",
        # boolean
        "__true",
        "__false",
        "__equal",
        "__larger",
        # checktype
        "__type",
        # string
        "__strin"
    ])

    MARK = set([
        "", ":", ";", ")"
    ])
