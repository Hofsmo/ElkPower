"""Module for components."""


class Component:
    """Class for components."""

    def __init__(self, name):
        """Constructor for Component.
        Args:
            name: name of the component
            """
        self.name = name


class Node(Component):
    """Class for storing nodes."""

    def __init__(self, name, base_v=None, base_p=None,
                 voltage=1.0, angle=0.0,
                 v_min=0.9, v_max=1.1):
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

    def __init__(self, name, base_v=None, base_p=None,
                 voltage=1.0, angle=0.0,
                 active_power=0.0, reactive_power=0.0,
                 v_min=0.9, v_max=1.1, rating=None):
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
                         v_min, v_max)
        self.active_power = active_power
        self.reactive_power = reactive_power
        self.rating = rating


class Load(Node):
    """Class for loads."""

    def __init__(self, name, base_v=None, base_p=None,
                 voltage=1.0, angle=0.0,
                 active_power=0.0, reactive_power=0.0,
                 v_min=0.9, v_max=1.1):
        """Load constructor.
        Args:
            name: Name of the load
            base_v: base voltage
            base_p: base power
            voltage: voltage
            angle: voltage angle
            active_power: Active power at the load
            reactive_power: Reactive power at the load
            v_min: minimum voltage at the load
            v_max: maximum voltage
            """
        super().__init__(name, base_v, base_p, voltage, angle,
                         v_min, v_max)
        self.active_power = active_power
        self.reactive_power = reactive_power


class Edge:
    """Class for edges."""

    def __init__(self, name, f_bus, t_bus, rating=None):
        """Edge constructor
        Args:
            name: Name of the edge
            f_bus: The bus it is coming from
            t_bus: The bus it is going to.
            rating: The rating of the edge
            """
        self.name = name
        self.f_bus = f_bus
        self.t_bus = t_bus


class Line(Edge):
    """Class for lines."""

    def __init__(self, name, f_bus, t_bus, rating=None, x=0.0, r=0.0):
        """ Line constructor
        Args:
            name: Name of the line
            f_bus: The bus the line is coming from
            t_bus: The bus the line is going to
            rating: The rating of the line
            x: The reactance of the line
            r: The resistnace of the line
            """
        super().__init__(name, f_bus, t_bus)
        self.x = x
        self.r = r
