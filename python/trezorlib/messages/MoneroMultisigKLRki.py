# Automatically generated by pb2py
# fmt: off
from .. import protobuf as p

if __debug__:
    try:
        from typing import Dict, List, Optional
        from typing_extensions import Literal  # noqa: F401
    except ImportError:
        Dict, List, Optional = None, None, None  # type: ignore


class MoneroMultisigKLRki(p.MessageType):

    def __init__(
        self,
        K: bytes = None,
        L: bytes = None,
        R: bytes = None,
        ki: bytes = None,
    ) -> None:
        self.K = K
        self.L = L
        self.R = R
        self.ki = ki

    @classmethod
    def get_fields(cls) -> Dict:
        return {
            1: ('K', p.BytesType, 0),
            2: ('L', p.BytesType, 0),
            3: ('R', p.BytesType, 0),
            4: ('ki', p.BytesType, 0),
        }
