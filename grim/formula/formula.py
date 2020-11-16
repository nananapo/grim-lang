class Formula:  # 式

    def __init__(self, value=None):
        self.value = value

    def __str__(self):
        return "Formula<" + str(self.value)+">"
