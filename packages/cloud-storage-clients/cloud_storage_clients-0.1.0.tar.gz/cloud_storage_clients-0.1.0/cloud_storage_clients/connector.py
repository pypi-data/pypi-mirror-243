from dataclasses import dataclass
from typing import Optional


@dataclass
class Connector:
    client_type: str
    bucket: str
    id: Optional[str] = None

    @property
    def key(self):
        if self.id:
            return self.id
        else:
            return f"{self.client_type}/{self.bucket}"
