#!/usr/bin/python

import sys
from pattern import Pattern
from transition import Transition
from state import State


def main():
    if len(sys.argv) < 3:
        print "Usage regex.py <regular expression> <string>"
        sys.exit(0)
    p = build_regex(sys.argv[1])
    result = match(p, sys.argv[2])
    print result


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
            if (t.match is True and t.char == char) or t.char == "any" or (t.match is False and t.char != char):
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
    if char == "\\":
        re.index += 1
        char = re.get_current_token()
        for current in states:
            state = State("inner", None, current)
            transition = Transition(char, state)
            current.add_transition(transition)
            return_states.append(state)
    elif char == "[":
        set_of_chars = []
        re.index += 1
        current_char = re.get_current_token()
        m = True
        if current_char == "^":
            m = False
            re.index += 1
            current_char = re.get_current_token()
        while current_char != "]":
            set_of_chars.append(current_char)
            re.index += 1
            current_char = re.get_current_token()
        for current in states:
            state = State("inner", None, current)
            for new_char in set_of_chars:
                transition = Transition(new_char, state, m)
                current.add_transition(transition)
                return_states.append(state)
    elif char == ".":
        for current in states:
            state = State("inner", None, current)
            transition = Transition("any", state)
            current.add_transition(transition)
            return_states.append(state)
    elif char == "*":
        for current in states:
            last_state = current.last_state
            if last_state is None:
                raise SyntaxError("Invalid Token " + char)
            last_state_transitions = last_state.transitions
            last_state.transitions = []
            zero_transition = Transition(None, current)
            last_state.add_transition(zero_transition)
            for transition in last_state_transitions:
                if transition.char is not None:
                    char_to_match = transition.char
                    same_transition = Transition(char_to_match, last_state)
                    last_state.add_transition(same_transition)

            return_states.append(current)
    elif char == "+":
        for current in states:
            last_state = current.last_state
            if last_state is None:
                raise SyntaxError("Invalid Token " + char)
            new_transitions = []
            for transition in last_state.transitions:
                    char_to_match = transition.char
                    same_transition = Transition(char_to_match, last_state)
                    new_transitions.append(same_transition)
            last_state.add_multiple_transitions(new_transitions)
            return_states.append(current)
    elif char == "?":
        for current in states:
            last_state = current.last_state
            skip_char_transition = Transition(None, current)
            last_state.add_transition(skip_char_transition)
            return_states.append(current)
    elif char == "!":
        re.index += 1
        char = re.get_current_token()
        for current in states:
            state = State("inner", None, current)
            transition = Transition(char, state, False)
            current.add_transition(transition)
            return_states.append(state)
    else:
        for current in states:
            state = State("inner", None, current)
            transition = Transition(char, state)
            current.add_transition(transition)
            return_states.append(state)
    re.index += 1
    return return_states

if __name__ == '__main__':
    main()