from pydantic import BaseModel
from typing import Optional

class PortForward(BaseModel):
    protocol: str
    config_mode: str
    internal_ip: str
    internal_port: str
    external_port: str
    external_ipv4_address: str
    status: str

    @property
    def is_rdp(self) -> bool:
        return self.internal_port == "3389"

    @property
    def connection_string(self) -> str:
        return f"{self.external_ipv4_address}:{self.external_port}"

    class Config:
        alias_generator = lambda s: s.replace('_', ' ').title()
        populate_by_name = True