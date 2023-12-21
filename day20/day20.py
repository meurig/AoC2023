import math
import time
from pathlib import Path
from queue import SimpleQueue

import pytest


def run():
    with open(Path(__file__).parent / 'Input.txt') as f:
        lines = f.read().split('\n')

    start_time = time.time()
    result = run_state_machine_fixed_times(lines, 1000)
    print(f'Day20 part 1: {result} (in {(time.time() - start_time):.2f}s)')

    start_time = time.time()
    result2 = calc_state_machine_presses_til_on(lines)
    print(f'Day20 part 2: {result2} (in {(time.time() - start_time):.2f}s)')

class Message:
    def __init__(self, sender: 'Node', recipient: 'Node', pulse: bool):
        self.sender = sender
        self.recipient = recipient
        self.pulse = pulse
        pulse_str = 'high' if self.pulse else 'low'
        message_str = f'{self.sender.name} -{pulse_str}> {self.recipient.name}'
        self.message_str = message_str

    def __str__(self):
        return self.message_str

class Node:
    def __init__(self, name, dest_str: str):
        self.name = name
        self.dest_str = dest_str.replace(' ', '')
        self.destinations: list[Node] = []
        self.sources: list[Node] = []

    def __str__(self):
        return f'{self.name} ({[x.name for x in self.sources]} -> {[x.name for x in self.destinations]})'

    def hook_up_destinations(self, nodes: dict[str, 'Node']):
        if self.dest_str == '':
            return
        for dest_name in self.dest_str.replace(' ', '').split(','):
            if dest_name in nodes:
                destination_node = nodes[dest_name]
            else:
                destination_node = Node(dest_name, '')
                nodes[dest_name] = destination_node

            self.destinations.append(destination_node)
            destination_node.add_source(self)

    def add_source(self, node: 'Node'):
        self.sources.append(node)

    def trigger(self, sender,  pulse: bool) -> list[Message]:
        return [ Message(self, dest, pulse) for  dest in self.destinations ]


class FlipFlop(Node):
    def __init__(self, name, dest_str: str):
        super().__init__(name, dest_str)
        self.state = False

    def __str__(self):
        return f'FF: {super().__str__()}'

    def trigger(self, sender,  pulse: bool) -> list[Message]:
        if pulse:
            return []
        self.state = not self.state
        return super().trigger(sender, self.state)


class Conjunction(Node):
    def __init__(self, name, dest_str: str):
        super().__init__(name, dest_str)
        self.state: dict[Node, bool] = {}

    def __str__(self):
        return f'Con: {super().__str__()}'

    def add_source(self, node: 'Node'):
        super().add_source(node)
        self.state[node] = False

    def trigger(self, sender,  pulse: bool) -> list[Message]:
        self.state[sender] = pulse
        if all(self.state.values()):
            return super().trigger(sender, False)
        else:
            return super().trigger(sender, True)

class StateMachine:
    def __init__(self, nodes: dict[str, Node]):
        self.nodes = nodes
        self.message_queue = SimpleQueue[Message]()
        self.button = nodes['button']
        self.high_pulse_count = 0
        self.low_pulse_count = 0
        self.periodicity = {}
        self.presses_until_on = 0
        self.presses = 0

    def put(self, messages: list[Message]):
        for message in messages:
            self.message_queue.put(message)


    def press_button(self) -> (int, int):
        self.presses += 1
        messages = self.button.trigger(None, False)
        self.put(messages)
        self.process_messages_on_queue()
        return self.high_pulse_count, self.low_pulse_count

    def process_messages_on_queue(self):
        while not self.message_queue.empty():
            message = self.message_queue.get()
            new_messages = self.process(message)
            self.put(new_messages)

    def process(self, message: Message) -> list[Message]:
        source = message.sender
        destination = message.recipient
        pulse = message.pulse
        if pulse:
            self.high_pulse_count += 1
        else:
            self.low_pulse_count += 1
        messages = destination.trigger(source, pulse)
        if destination.name == 'ql' and pulse and any(destination.state.values()):  # ql is the input to rx
            self.periodicity[source.name] = self.presses
            if set(self.periodicity.keys()) == {'mf', 'fz', 'fh', 'ss'}:  # these are the inputs to ql
                self.presses_until_on = math.prod(self.periodicity.values())
        return messages

    def reset_counts(self) -> None:
        self.high_pulse_count = 0
        self.low_pulse_count = 0

def create_node(line: str) -> (Node, str):
    name = line.split(' ')[0]
    first_char = name[0]
    node_type = None
    if first_char == '%' or first_char == '&':
        node_type = first_char
        name = name[1:]
    dest_str = line.split('>')[1][1:]
    if not node_type:
        return Node(name, dest_str), name
    elif node_type == '%':
        return FlipFlop(name, dest_str), name
    elif node_type == '&':
        return Conjunction(name, dest_str), name
    else:
        raise ValueError(f'Unexpected node type: {node_type}')

def parse_inputs(lines: list[str]):
    nodes = {}
    for line in lines:
        node, name = create_node(line)
        nodes[name] = node
    nodes['button'] = Node('button', 'broadcaster')

    for node in list(nodes.values()):
        node.hook_up_destinations(nodes)

    return nodes

def run_state_machine_fixed_times(data: list[str], presses: int = 1000) -> int:
    nodes = parse_inputs(data)
    state_machine = StateMachine(nodes)
    for i in range(presses):
        state_machine.press_button()
    return state_machine.high_pulse_count * state_machine.low_pulse_count

def calc_state_machine_presses_til_on(data: list[str]) -> int:
    nodes = parse_inputs(data)
    state_machine = StateMachine(nodes)
    while not state_machine.presses_until_on:
        state_machine.press_button()
    return state_machine.presses_until_on

test_input1 = [
    'broadcaster -> a, b, c',
    '%a -> b',
    '%b -> c',
    '%c -> inv',
    '&inv -> a',
]

test_input2 = [
    'broadcaster -> a',
    '%a -> inv, con',
    '&inv -> b',
    '%b -> con',
    '&con -> output',
]

@pytest.mark.parametrize('data, presses, expected', [
    (test_input1, 1000, 32000000),
    (test_input2, 1000, 11687500),
])
def test_run_state_machine_fixed_times(data, presses, expected):
    actual = run_state_machine_fixed_times(data, presses)
    assert actual == expected

if __name__ == '__main__':
    run()
