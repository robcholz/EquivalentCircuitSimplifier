import uuid
from typing import List, Union, Dict

from component import Component, Wire
from components import Resistor
from pin import Pin


def print_circuit(description: str, circuit: List[Component]):
    print("{}: {}".format(description, [(str(com)) for com in circuit]))


class Solver:
    def __init__(self, bypass_open_component: bool, connections: List[Union[Component, Wire]], terminals: List[str]):
        self._bypass_open_component: bool = bypass_open_component
        self._connections: List[Union[Component, Wire]] = connections
        self._terminals: List[str] = terminals

    def solve(self) -> List[Component]:
        self._merge(self._connections, self._terminals)
        print_circuit("Original circuit", self._connections)
        if self._bypass_open_component is False:
            self._exclude_open_component(self._connections, self._terminals)
        self._remove_short_circuit(self._connections)
        print()
        while not self._solve_step(self._connections):
            print_circuit("Iteration", self._connections)
            print()
        return self._connections

    @staticmethod
    def _get_nodes(components: List[Component]) -> Dict[str, List[Component]]:
        nodes: Dict[str, List[Component]] = {}  # pin_id and connected components
        for component in components:
            for pin in component.pins():
                nodes.setdefault(pin.get_pin_id(), list())
                nodes.get(pin.get_pin_id()).append(component)
        return nodes

    def _exclude_open_component(self, components: List[Component], terminals: List[str]):
        nodes: Dict[str, List[Component]] = self._get_nodes(components)
        remove_list = []
        for terminal in terminals:
            nodes.setdefault(terminal, [])
            nodes.get(terminal).append(Resistor(str(uuid.uuid4()), str(uuid.uuid4()), 0))
        for node_name, node_components in nodes.items():
            if len(node_components) == 1:
                remove_list.append(node_components[0])
        for remove in remove_list:
            components.remove(remove)
        print_circuit("> Removed the open-circuit component", remove_list)
        print_circuit("Circuit after removing the open-circuit component", components)

    @staticmethod
    def _remove_short_circuit(components: List[Component]):
        remove_list = []
        for component in components:
            tar = component.pins()[0]
            count = 0
            for pin in component.pins():
                if tar.is_connected_to(pin):
                    count += 1
            if count == len(component.pins()):
                remove_list.append(component)

        for rm in remove_list:
            components.remove(rm)

        print_circuit("> Removed the short-circuit component", remove_list)
        print_circuit("Circuit after removing the short-circuit component", components)

    def _solve_step(self, components: List[Component]) -> bool:
        nodes: Dict[str, List[Component]] = self._get_nodes(components)
        for node_name, node_components in nodes.items():
            if len(node_components) == 2:
                left = node_components[0]
                right = node_components[1]
                # prevent from optimizing terminal node
                if left.is_series_to(right) and not (node_name in self._terminals):
                    eq_component = left.on_series(right)
                    if eq_component is None:
                        break
                    components.remove(left)
                    components.remove(right)
                    components.append(eq_component)
                    print_circuit("> Removed the in-series component", [left, right])
                    return False
            if len(node_components) >= 2:
                left = node_components[0]
                for right in node_components:
                    if left is not right:
                        if left.is_parallel_to(right):
                            eq_component = left.on_parallel(right)
                            if eq_component is None:
                                break
                            components.remove(left)
                            components.remove(right)
                            components.append(eq_component)
                            print_circuit("> Removed the in-parallel component", [left, right])
                            return False
        return True

    @staticmethod
    def _merge(connections: List[Union[Component, Wire]], terminals: List[str]):
        merges: List[Wire] = list()
        components: List[Component] = list()

        for connection in connections:
            if isinstance(connection, Wire):
                merges.append(connection)
            if isinstance(connection, Component):
                components.append(connection)

        for equivalent_network in merges:
            # Choose a random node in the Wire
            target_network: Pin = equivalent_network.left()
            replace_network: Pin = equivalent_network.right()
            # avoid the optimization of the terminals
            if replace_network.get_pin_id() in terminals:
                target_network = equivalent_network.right()
                replace_network = equivalent_network.left()
            for component in components:
                for pin in component.pins():
                    if pin.get_pin_id() == replace_network.get_pin_id():
                        pin.set_pin_id(target_network.get_pin_id())

        connections.clear()
        connections.extend(components)
