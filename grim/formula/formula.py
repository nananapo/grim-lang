from grim.formula.types import ClassType


class Formula:  # 式

    def __init__(self, *, value=None):
        self.value = value  # Formulaが入る可能性もある(入ったら優先)

    def __str__(self):
        return "Formula<" + str(self.value)+">"

    def get_type(self):
        return ClassType.TYPE_FORMULA
