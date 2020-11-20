from grim.formula.types import ClassType


class Control:

    SYMBOL = [
        "if"
    ]

    # ifの時
    # processが処理
    # formulaに評価する式を入れる -> 式の最後が評価される -> 結果によって実行
    TYPE_CONTROL_IF = 3  # if文
    TYPE_CONTROL_WHILE = 4  # while文

    def __init__(self, *, formula=None, process=None):
        self.formula = formula
        self.process = process


    def get_type(self):
        return ClassType.TYPE_CONTROL
