"""Module for components."""


class Component:
    """Class for components."""

    def __init__(self, name=None):
        """Constructor for Component.
        Args:
            name: name of the component
            """
        self.name = name


class Node(Component):
    """Class for storing nodes."""

    def __init__(self, bus, name=None, base_v=None, base_p=None,
                 voltage=1.0, angle=0.0,
                 v_min=0.9, v_max=1.1):
        """ Node constructor.
        Args:
            bus: Unique identifier of the node
            name: Name of the node
            base_v: base voltage for the node
            base_p: base power for the node
            voltage: voltage at the node
            angle: voltage angle at the node
            v_min: minimum voltage at the node
            v_max: maximum voltage at the node
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
        self.bus = bus


class Generator(Node):
    """Class for generators."""

    def __init__(self, bus, name=None, base_v=None, base_p=None,
                 voltage=1.0, angle=0.0,
                 active_power=0.0, reactive_power=0.0,
                 v_min=0.9, v_max=1.1, x=None,
                 n_gen=1, inertia=0, Kd=None,
                 Kp=0, Ti=0, R=0, Tw=0, Ty=0):
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
            x: Internal reactance
            n_gen: Number of generators for aggregated generators
            inertia: Inertia constant
            Kd: Damping constant
            Kp: Governor proportional constant
            Ti: Governor integral time
            R: Governor droop
            Tw: Penstock water time
            Ty: Servo time constant
            """
        super().__init__(bus, name, base_v, base_p, voltage, angle,
                         v_min, v_max)
        self.active_power = active_power
        self.reactive_power = reactive_power
        self.x = x
        self.n_gen = n_gen
        self.inertia = inertia*n_gen
        self.Kd = Kd*n_gen
        self.Kp = Kp
        self.Ti = Ti
        self.R = R
        self.Tw = Tw
        self.Ty = Ty


class Load(Node):
    """Class for loads."""

    def __init__(self, bus, name=None, base_v=None, base_p=None,
                 voltage=1.0, angle=0.0,
                 active_power=0.0, reactive_power=0.0,
                 v_min=0.9, v_max=1.1, freq_dep=0):
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
            freq_dep: Frequency dependency
            """
        super().__init__(bus, name, base_v, base_p, voltage, angle,
                         v_min, v_max)
        self.active_power = active_power
        self.reactive_power = reactive_power
        self.freq_dep = freq_dep


class Edge:
    """Class for edges."""

    def __init__(self, f_bus, t_bus, name=None, rating=None):
        """Edge constructor
        Args:
            name: Name of the edge
            f_bus: The bus it is coming from
            t_bus: The bus it is going to.
            rating: The rating of the edge
            """
        self.f_bus = f_bus
        self.t_bus = t_bus
        self.name = name


class Line(Edge):
    """Class for lines."""

    def __init__(self, f_bus, t_bus, name=None, rating=None, x=0.0, r=0.0,
                 z_base=None):
        """ Line constructor
        Args:
            name: Name of the line
            f_bus: The bus the line is coming from
            t_bus: The bus the line is going to
            rating: The rating of the line
            x: The reactance of the line
            r: The resistance of the line
            z_base: The base impedance of the line
            """
        super().__init__(f_bus=f_bus, t_bus=t_bus, name=name)
        self.x = x
        self.r = r
        self.z_base = z_base
