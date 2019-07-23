# Automatically generated by pb2py
# fmt: off
import protobuf as p

if __debug__:
    try:
        from typing import Dict, List, Optional
        from typing_extensions import Literal  # noqa: F401
    except ImportError:
        Dict, List, Optional = None, None, None  # type: ignore


class StellarSetOptionsOp(p.MessageType):
    MESSAGE_WIRE_TYPE = 215

    def __init__(
        self,
        source_account: str = None,
        inflation_destination_account: str = None,
        clear_flags: int = None,
        set_flags: int = None,
        master_weight: int = None,
        low_threshold: int = None,
        medium_threshold: int = None,
        high_threshold: int = None,
        home_domain: str = None,
        signer_type: int = None,
        signer_key: bytes = None,
        signer_weight: int = None,
    ) -> None:
        self.source_account = source_account
        self.inflation_destination_account = inflation_destination_account
        self.clear_flags = clear_flags
        self.set_flags = set_flags
        self.master_weight = master_weight
        self.low_threshold = low_threshold
        self.medium_threshold = medium_threshold
        self.high_threshold = high_threshold
        self.home_domain = home_domain
        self.signer_type = signer_type
        self.signer_key = signer_key
        self.signer_weight = signer_weight

    @classmethod
    def get_fields(cls) -> Dict:
        return {
            1: ('source_account', p.UnicodeType, 0),
            2: ('inflation_destination_account', p.UnicodeType, 0),
            3: ('clear_flags', p.UVarintType, 0),
            4: ('set_flags', p.UVarintType, 0),
            5: ('master_weight', p.UVarintType, 0),
            6: ('low_threshold', p.UVarintType, 0),
            7: ('medium_threshold', p.UVarintType, 0),
            8: ('high_threshold', p.UVarintType, 0),
            9: ('home_domain', p.UnicodeType, 0),
            10: ('signer_type', p.UVarintType, 0),
            11: ('signer_key', p.BytesType, 0),
            12: ('signer_weight', p.UVarintType, 0),
        }
