class State:
    """
    :type transitions: list(transition)
    """

    def __init__(self, state_type, transitions, last_state):
        self.stateType = state_type
        self.last_state = last_state
        if transitions:
            self.transitions = transitions
        else:
            self.transitions = []

    def add_transition(self, next_transition):
        self.transitions.append(next_transition)

    def add_multiple_transitions(self, next_transitions):
        self.transitions.extend(next_transitions)