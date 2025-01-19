import argparse
import uuid
from typing import Union, List

from component import Component, Wire
from components import Resistor, Capacitor
from solver import Solver


def process_open_node(pin_id: str) -> str:
    if pin_id != "*":
        return pin_id
    return str(uuid.uuid4())


# e.g. 'e R-20 a'
def parse_component(text: str) -> Union[Component, Wire]:
    slices = text.strip().split(' ')
    left_pin = process_open_node(slices[0])
    right_pin = process_open_node(slices[2])
    slices1 = slices[1].split('-')
    component_type = slices1[0]
    if component_type == 'W':
        return Wire(left_pin, right_pin)
    value = slices1[1]
    if component_type == 'R':
        return Resistor(left_pin, right_pin, float(value))
    if component_type == 'C':
        return Capacitor(left_pin, right_pin, float(value))
    raise Exception("Unrecognized component type: {}".format(component_type))


# e.g. 'e R-20 a,e W a'
def parse_connections(text: str) -> List[Union[Component, Wire]]:
    return [parse_component(item) for item in text.split(",")]


def parse_terminals(text: str) -> List[str]:
    return [item for item in text.strip().split(",")]


def main():
    parser = argparse.ArgumentParser(description="Solve the circuit problem with resistors and capacitors.")

    parser.add_argument('--bypass-open', action='store_true', help="Bypass open-circuit components")
    parser.add_argument('--connections', type=str, help="List of connections (e.g., 'e R-20 a k C-50 m, m W i,e R-50 "
                                                        "*')")
    parser.add_argument("--terminals", type=str, help="List of terminals (e.g. a,b)")
    args = parser.parse_args()

    if len(args.connections) == 0:
        print("Connections are empty!")
        exit(0)

    solver = Solver(bypass_open_component=args.bypass_open, connections=parse_connections(args.connections),
                    terminals=parse_terminals(args.terminals))
    final_circuit = solver.solve()
    print("Solve result: ", [(str(com)) for com in final_circuit])


if __name__ == "__main__":
    main()
