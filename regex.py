import sys
import pprint
from pattern import Pattern
def main():
    regex = build_regex("attttb")
    print match(regex,  "attttb")


def match(re, string):
    """
    :type re: State
    """
    states = [re]
    if can_match_empty_string(states):
        return True
    for char in string:
        states = expand_states(states, char)
        states = advance_none_states(states)
        for s in states:
            if s.stateType == "match":
                return True
    return False

def can_match_empty_string(states):
    states = advance_none_states(states)
    for s in states:
            if s.stateType == "match":
                return True
    return False
def expand_states(active_states, char):
    new_states = []
    start_state = None
    for state in active_states:
        for t in state.transitions:
            if t.char == char or t.char == "any":
                new_states.append(t.next_state)
        if state.stateType == "start":
            start_state = state
    active_states = [start_state]
    active_states.extend(new_states)
    return active_states


def advance_none_states(states):
    for state in states:
        for transition in state.transitions:
            if transition.char is None:
                states.append(transition.next_state)
    return states


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
            transition = Transition("any", state)
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