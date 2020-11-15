class Formula:  # 式

    def __init__(self, assign=None, value=None):
        self.assign = assign
        self.value = value if value != None else []

    def only_value(self):
        return self.assign == None

    def is_dynamic_assign(self):
        return self.assign[0] == ":"

    def get_assign(self):
        return self.assign if not self.is_dynamic_assign() else self.assign[1::]

    def __str__(self):
        return "Formula" + str(self.value)
