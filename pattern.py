class Pattern:
    string = ""
    index = 0

    def __init__(self, string, index):
        self.string = string
        self.index = index

    def get_current_token(self):
        return self.string[self.index]

    def get_last_token(self):
        return self.string[self.index - 1]
