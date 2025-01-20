from pydantic import BaseModel, Field
from typing import Optional

class PortForward(BaseModel):
    config_mode: str = Field(..., alias="Configuration Mode")
    external_ipv4_address: str = Field(..., alias="External IPv4 Address")
    external_port: str = Field(..., alias="External Port")
    internal_port: str = Field(..., alias="Internal Port")
    protocol: str = Field(..., alias="Protocol")
    internal_ip: str = Field(..., alias="Internal IPv4 Address")
    status: str = Field(..., alias="PCP Server Result Code")
    allow_proposal: str = Field(..., alias="Allow PCP Port Proposal [Y/N]")

    @property
    def is_rdp(self) -> bool:
        return self.internal_port == "3389"

    @property
    def connection_string(self) -> str:
        return f"{self.external_ipv4_address}:{self.external_port}"

    class Config:
        populate_by_name = True