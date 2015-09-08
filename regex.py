import sys
from pattern import Pattern
def main():
    regex = build_regex("abbd*e")
    print match(regex,  "abbdddddddeasdijfjk")

def match(re, string):
    """
    :type re: State
    """

    states = [re]
    new_states = []
    for char in string:
        for state in states:
            for transition in state.transitions:
                if transition.char == char or transition.char is None:
                    if transition.next_state.stateType == "match":
                        return True
                    new_states.append(transition.next_state)
            if state.stateType != "start":
                states.remove(state)
        states.extend(new_states)
        new_states = []
    return False


def build_regex(reString):
    re = Pattern(reString, 0)

    start = State("start", None, None)
    states = [start]
    while len(re.string) > re.index:
        states = add_transition(re, states)
    for current in states:
        current.stateType = "match"
    return start


def add_transition(re, states):
    char = re.get_current_token()
    return_states = []
    if char == ".":
        for current in states:
            state = State("inner", None, current)
            transition = Transition(None, state)
            current.add_transition(transition)
            return_states.append(state)
    elif char == "*":
        for current in states:
            last_state = current.last_state
            if len(last_state.transitions) > 1:
                raise SyntaxError("Invalid Token " + char)
            char_to_match = last_state.transitions[0].char
            last_state.transitions = []
            zero_transition = Transition(None, current)
            same_transition = Transition(char_to_match, last_state)
            last_state.add_multiple_transitions([zero_transition, same_transition])
            return_states.append(current)
    else:
        for current in states:
            state = State("inner", None, current)
            transition = Transition(char, state)
            current.add_transition(transition)
            return_states.append(state)
    re.index += 1
    return return_states


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


class Transition:
    """
    :type next_state: State
    """

    def __init__(self, char, next_state):
        self.char = char
        self.next_state = next_state


if __name__ == '__main__':
    main()