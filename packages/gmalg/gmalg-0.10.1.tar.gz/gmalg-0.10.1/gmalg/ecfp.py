import math
from typing import Callable, Tuple, Type

from . import errors
from .base import Hash
from .utils import inverse, sqrt_4u3, sqrt_8u1, sqrt_8u5

__all__ = [
    "ECDLP",
    "EllipticCurve",
    "EllipticCurveCipher",
]


class EllipticCurve:
    """Elliptic Curve (Fp)"""

    INF = (-1, -1)

    @staticmethod
    def isinf(x: int, y: int) -> bool:
        """Check if a point is a infinite point."""

        return x < 0 or y < 0

    def __init__(self, p: int, a: int, b: int) -> None:
        """Elliptic Curve (Fp)

        y^2 = x^3 + ax + b (mod p)

        Raises:
            InvalidArgumentError: p is not a prime number.
        """

        self.p = p
        self.a = a
        self.b = b

        self.bitlength = self.p.bit_length()
        self.length = (self.bitlength + 7) >> 3

        self._u, self._r = divmod(self.p, 8)
        if self._r == 1:
            self.get_y = self._get_y_8u1
        elif self._r == 3:
            self._u = self._u * 2
            self.get_y = self._get_y_4u3
        elif self._r == 5:
            self.get_y = self._get_y_8u5
        elif self._r == 7:
            self._u = self._u * 2 + 1
            self.get_y = self._get_y_4u3
        else:
            raise errors.InvalidArgumentError(f"0x{p:x} is not a prime number.")

    def isvalid(self, x: int, y: int) -> bool:
        """Verify if a point is on the curve."""

        if x >= self.p or y >= self.p:
            return False

        if (y * y - x * x * x - self.a * x - self.b) % self.p != 0:
            return False

        return True

    def add(self, x1: int, y1: int, x2: int, y2: int) -> Tuple[int, int]:
        """Add two points. Negative numbers means infinite point."""

        a = self.a
        p = self.p

        if self.isinf(x1, y1):
            return x2, y2
        if self.isinf(x2, y2):
            return x1, y1
        if x1 == x2:
            if y1 + y2 == p:
                return -1, -1
            elif y1 == y2:
                lam = (3 * x1 * x1 + a) * inverse(2 * y1, p)
            else:
                raise errors.UnknownError(f"0x{y1:x} and 0x{y2:x} is neither equal nor opposite.")
        else:
            if x2 > x1:
                lam = (y2 - y1) * inverse(x2 - x1, p)
            else:
                lam = (y1 - y2) * inverse(x1 - x2, p)

        x3 = (lam * lam - x1 - x2) % p
        y3 = (lam * (x1 - x3) - y1) % p

        return x3, y3

    def sub(self, x1: int, y1: int, x2: int, y2: int) -> Tuple[int, int]:
        """Sub two points."""

        return self.add(x1, y1, x2, self.p - y2)

    def mul(self, k: int, x: int, y: int) -> Tuple[int, int]:
        """Scalar multiplication by k."""

        xk = -1
        yk = -1

        for i in f"{k:b}":
            xk, yk = self.add(xk, yk, xk, yk)
            if i == "1":
                xk, yk = self.add(xk, yk, x, y)

        return xk, yk

    def get_y_sqr(self, x: int) -> int:
        return (x * x * x + self.a * x + self.b) % self.p

    def _get_y_4u3(self, x: int) -> int:
        return sqrt_4u3(self.get_y_sqr(x), self.p, self._u)

    def _get_y_8u5(self, x: int) -> int:
        return sqrt_8u5(self.get_y_sqr(x), self.p, self._u)

    def _get_y_8u1(self, x: int) -> int:
        return sqrt_8u1(self.get_y_sqr(x), self.p, self._u)

    def get_y(self, x: int) -> int:
        """Get one of valid y of given x, -1 means no solution."""
        raise errors.UnknownError("Unknown Error.")

    def itob(self, i: int) -> bytes:
        """Convert domain elements to bytes."""

        return i.to_bytes(self.length, "big")

    def btoi(self, b: bytes) -> int:
        """Convert bytes to domain elements"""

        return int.from_bytes(b, "big")


class ECDLP(EllipticCurve):
    """Elliptic Curve Discrete Logarithm Problem"""

    def __init__(self, p: int, a: int, b: int, xG: int, yG: int, n: int, h: int = 1) -> None:
        """Elliptic Curve Discrete Logarithm Problem

        Elliptic Curve (Fp): y^2 = x^3 + ax + b (mod p)

        Base point: (xG, yG)
        Order of the base point: n
        Cofactor: h
        """

        super().__init__(p, a, b)

        self.xG = xG
        self.yG = yG
        self.n = n
        self.h = h

    def kG(self, k: int) -> Tuple[int, int]:
        """Scalar multiplication of G by k."""

        return self.mul(k, self.xG, self.yG)


class EllipticCurveCipher:
    """Elliptic Curve Cipher"""

    def __init__(self, ecdlp: ECDLP, hash_cls: Type[Hash], rnd_fn: Callable[[int], int]) -> None:
        """Elliptic Curve Cipher

        Args:
            ecdlp (ECDLP): ECDLP used in cipher.
            hash_fn (Hash): hash function used in cipher.
            rnd_fn ((int) -> int): random function used to generate k-bit random number.
        """

        self.ecdlp = ecdlp
        self._hash_cls = hash_cls
        self._rnd_fn = rnd_fn

        # used in key exchange
        w = math.ceil(math.ceil(math.log2(self.ecdlp.n)) / 2) - 1
        self._2w = 1 << w
        self._2w_1 = self._2w - 1

    def _hash_fn(self, data: bytes) -> bytes:
        hash_obj = self._hash_cls()
        hash_obj.update(data)
        return hash_obj.value()

    def _randint(self, a: int, b: int) -> int:
        bitlength = b.bit_length()
        while True:
            n = self._rnd_fn(bitlength)
            if n < a or n > b:
                continue
            return n

    def generate_keypair(self) -> Tuple[int, Tuple[int, int]]:
        """Generate key pair."""

        d = self._randint(1, self.ecdlp.n - 2)
        return d, self.ecdlp.kG(d)

    def get_pubkey(self, d: int) -> Tuple[int, int]:
        """Generate public key by secret key d."""

        return self.ecdlp.kG(d)

    def verify_pubkey(self, x: int, y: int) -> bool:
        """Verify if a public key is valid."""

        if self.ecdlp.isinf(x, y):
            return False

        if not self.ecdlp.isvalid(x, y):
            return False

        if not self.ecdlp.isinf(self.ecdlp.mul(self.ecdlp.n, x, y)):
            return False

        return True

    def entity_info(self, id_: bytes, xP: int, yP: int) -> bytes:
        """Generate other entity information bytes.

        Raises:
            DataOverflowError: ID more than 2 bytes.
        """

        ENTL = len(id_) << 3
        if ENTL.bit_length() > 16:
            raise errors.DataOverflowError("ID", "2 bytes")

        itob = self.ecdlp.itob

        Z = bytearray()
        Z.extend(ENTL.to_bytes(2, "big"))
        Z.extend(id_)
        Z.extend(itob(self.ecdlp.a))
        Z.extend(itob(self.ecdlp.b))
        Z.extend(itob(self.ecdlp.xG))
        Z.extend(itob(self.ecdlp.yG))
        Z.extend(itob(xP))
        Z.extend(itob(yP))

        return self._hash_fn(Z)

    def sign(self, message: bytes, d: int, id_: bytes, xP: int = None, yP: int = None) -> Tuple[int, int]:
        """Generate signature on the message.

        Args:
            message (bytes): message to be signed.
            d (int): secret key.
            id_ (bytes): user id.
            xP (int): x of public key
            yP (int): y of public key

        Returns:
            (int, int): (r, s)
        """

        if xP is None or yP is None:
            xP, yP = self.get_pubkey(d)

        e = int.from_bytes(self._hash_fn(self.entity_info(id_, xP, yP) + message), "big")

        ecdlp = self.ecdlp
        n = self.ecdlp.n
        while True:
            k = self._randint(1, n - 1)
            x, _ = ecdlp.kG(k)

            r = (e + x) % n
            if r == 0 or (r + k == n):
                continue

            s = (inverse(1 + d, n) * (k - r * d)) % n
            if s == 0:
                continue

            return r, s

    def verify(self, message: bytes, r: int, s: int, id_: bytes, xP: int, yP: int) -> bool:
        """Verify the signature on the message.

        Args:
            message (bytes): Message to be verified.
            r (int): r
            s (int): s
            id_ (bytes): user id.
            xP (int): x of public key.
            yP (int): y of public key.

        Returns:
            bool: Whether OK.
        """

        ecdlp = self.ecdlp
        n = self.ecdlp.n

        if r < 1 or r > n - 1:
            return False

        if s < 1 or s > n - 1:
            return False

        t = (r + s) % n
        if t == 0:
            return False

        e = int.from_bytes(self._hash_fn(self.entity_info(id_, xP, yP) + message), "big")

        x, _ = ecdlp.add(*ecdlp.kG(s), *ecdlp.mul(t, xP, yP))
        if (e + x) % n != r:
            return False

        return True

    def key_derivation_fn(self, Z: bytes, klen: int) -> bytes:
        """KDF

        Args:
            Z (bytes): secret bytes.
            klen (int): key byte length

        Raises:
            DataOverflowError: klen is too large.
        """

        hash_fn = self._hash_fn
        v = self._hash_cls.hash_length()

        count, tail = divmod(klen, v)
        if count + (tail > 0) > 0xffffffff:
            raise errors.DataOverflowError("Key stream", f"{0xffffffff * v} bytes")

        K = bytearray()
        for ct in range(1, count + 1):
            K.extend(hash_fn(Z + ct.to_bytes(4, "big")))

        if tail > 0:
            K.extend(hash_fn(Z + (count + 1).to_bytes(4, "big"))[:tail])

        return bytes(K)

    def encrypt(self, plain: bytes, xP: int, yP: int) -> Tuple[Tuple[int, int], bytes, bytes]:
        """Encrypt.

        Args:
            data (bytes): plain text to be encrypted.
            xP (int): x of public key.
            yP (int): y of public key.

        Returns:
            (int, int): C1, kG point
            bytes: C2, cipher
            bytes: C3, hash value

        Raises:
            InfinitePointError: Infinite point encountered.

        The return order is `C1, C2, C3`, **NOT** `C1, C3, C2`.
        """

        while True:
            k = self._randint(1, self.ecdlp.n - 1)
            x1, y1 = self.ecdlp.kG(k)  # C1

            if self.ecdlp.isinf(*self.ecdlp.mul(self.ecdlp.h, xP, yP)):
                raise errors.InfinitePointError(f"Infinite point encountered, [0x{self.ecdlp.h:x}](0x{xP:x}, 0x{yP:x})")

            x2, y2 = self.ecdlp.mul(k, xP, yP)
            x2 = self.ecdlp.itob(x2)
            y2 = self.ecdlp.itob(y2)

            t = self.key_derivation_fn(x2 + y2, len(plain))
            if not any(t):
                continue

            C2 = bytes(map(lambda b1, b2: b1 ^ b2, plain, t))
            C3 = self._hash_fn(x2 + plain + y2)

            return (x1, y1), C2, C3

    def decrypt(self, x1: int, y1: int, C2: bytes, C3: bytes, d: int) -> bytes:
        """Decrypt.

        Args:
            x1 (int): x of C1 (kG point).
            y1 (int): y of C1 (kG point).
            C1 (bytes, bytes): kG point
            C2 (bytes): cipher
            C3 (bytes): hash value
            d (int): secret key.

        Returns:
            bytes: plain text.

        Raises:
            PointNotOnCurveError: Invalid C1 point, not on curve.
            InfinitePointError: Infinite point encountered.
            UnknownError: Zero bytes key stream.
            CheckFailedError: Incorrect hash value.
        """

        if not self.ecdlp.isvalid(x1, y1):
            raise errors.PointNotOnCurveError(x1, x2)

        if self.ecdlp.isinf(*self.ecdlp.mul(self.ecdlp.h, x1, y1)):
            raise errors.InfinitePointError(f"Infinite point encountered, [0x{self.ecdlp.h:x}](0x{x1:x}, 0x{y1:x})")

        x2, y2 = self.ecdlp.mul(d, x1, y1)
        x2 = self.ecdlp.itob(x2)
        y2 = self.ecdlp.itob(y2)

        t = self.key_derivation_fn(x2 + y2, len(C2))
        if not any(t):
            raise errors.UnknownError("Zero bytes key stream.")

        M = bytes(map(lambda b1, b2: b1 ^ b2, C2, t))

        if self._hash_fn(x2 + M + y2) != C3:
            raise errors.CheckFailedError("Incorrect hash value.")

        return M

    def _x_bar(self, x: int):
        """Used in key exchange."""

        return self._2w + (x & self._2w_1)

    def begin_key_exchange(self, d: int) -> Tuple[Tuple[int, int], int]:
        """Generate data to begin key exchange.

        Returns:
            (int, int): random point, [r]G, r in [1, n - 1]
            int: t
        """

        ecdlp = self.ecdlp
        n = ecdlp.n

        r = self._randint(1, n)
        x, y = ecdlp.kG(r)
        t = (d + self._x_bar(x) * r) % n

        return (x, y), t

    def get_secret_point(self, t: int, xR: int, yR: int, xP: int, yP: int) -> Tuple[int, int]:
        """Generate session key of klen bytes for initiator.

        Args:
            t (int): generated from `begin_key_exchange`
            xR (int): x of random point from another user.
            yR (int): y of random point from another user.
            xP (int): x of public key of another user.
            yP (int): y of public key of another user.

        Returns:
            (int, int): The same secret point as another user.

        Raises:
            PointNotOnCurveError
            InfinitePointError
        """

        ecdlp = self.ecdlp

        if not ecdlp.isvalid(xR, yR):
            raise errors.PointNotOnCurveError(xR, yR)

        x, y = ecdlp.mul(
            ecdlp.h * t,
            *ecdlp.add(xP, yP, *ecdlp.mul(self._x_bar(xR), xR, yR))
        )

        if ecdlp.isinf(x, y):
            raise errors.InfinitePointError("Infinite point encountered.")

        return x, y

    def generate_skey(self, klen: int, x: int, y: int,
                      id_init: bytes, xP_init: int, yP_init: int,
                      id_resp: bytes, xP_resp: int, yP_resp: int) -> bytes:
        """Generate secret key of klen bytes.

        Args:
            klen (int): key length in bytes to generate.
            x (int): x of secret point.
            y (int): y of secret point.

            id_init (bytes): id bytes of initiator.
            xP_init (int): x of public key of initiator.
            yP_init (int): y of public key of initiator.

            id_resp (bytes): id bytes of responder.
            xP_resp (int): x of public key of responder.
            yP_resp (int): y of public key of responder.

        Returns:
            bytes: secret key of klen bytes.
        """

        Z = bytearray()

        Z.extend(self.ecdlp.itob(x))
        Z.extend(self.ecdlp.itob(y))
        Z.extend(self.entity_info(id_init, xP_init, yP_init))
        Z.extend(self.entity_info(id_resp, xP_resp, yP_resp))

        return self.key_derivation_fn(Z, klen)
