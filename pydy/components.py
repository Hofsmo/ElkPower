"""Module for components."""


class Component:
    """Class for components."""

    def __init__(self, name):
        """Constructor for Component.
        Args:
            name: name of the component
            """


class Node(Component):
    """Class for storing nodes."""

    def __init__(self, name, base_v, base_p, voltage, angle,
                 v_min, v_max):
        """ Node constructor.
        Args:
            name: Name of the node
            base_v: base voltage for the node
            base_p: base power for the node
            voltage: voltage at the node
            angle: voltage angle at the node
            v_min: minimum voltage at the node
            v_max: maximum volta at the node
            """
        super().__init__(name)
        self.base_v = base_v
        self.base_p = base_p
        self.voltage = voltage
        self.angle = angle
        self.v_min = v_min
        self.v_max = name
        self.base_v = base_v
        self.base_p = base_p
        self.voltage = voltage
        self.angle = angle
        self.v_min = v_min
        self.v_max = v_max


class Generator(Node):
    """Class for generators."""

    def __init__(self, name, base_v, base_p, voltage, angle,
                 active_power, reactive_power, v_min, v_max, rating):
        """
        Generator constructor.
        Args:
            name: Name of the generator
            base_v: base voltage
            base_p: base power
            voltage: Voltage
            angle: Voltage angle
            active_power: Active power production
            reactive_power: reactive power production
            v_min: minimum voltage
            v_max: maximum voltage
            rating: the rating of the machine
            """
        super().__init__(name, base_v, base_p, voltage, angle,
                         voltage, angle, v_min, v_max)
        self.active_power = active_power
        self.reactive_power = reactive_power
        self.rating = rating
