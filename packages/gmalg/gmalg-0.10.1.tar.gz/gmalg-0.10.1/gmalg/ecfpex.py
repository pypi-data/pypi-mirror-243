from . import ecfp


class EllipticCurveEx(ecfp.EllipticCurve):
    """Elliptic Curve (Fp) over extended field."""

    INF2 = ((-1, -1),
            (-1, -1))
    INF4 = ((-1, -1, -1, -1),
            (-1, -1, -1, -1))
    INF12 = ((-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1),
             (-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1))

    def __init__(self, p: int, a: int, b: int) -> None:
        super().__init__(p, a, b)
