from grim.formula.types import ClassType

#計算は出来ない
class NameClass:
    def __init__(self,name):
        self.name = name

    def get_type(self):
        return ClassType.TYPE_NAME