class Transition:
    """
    :type next_state: State
    """

    def __init__(self, char, next_state, match=True):
        self.char = char
        self.next_state = next_state
        self.match = match
