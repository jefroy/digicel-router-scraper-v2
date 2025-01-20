from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

class PortForward(BaseModel):
    # Fields from router UI
    config_mode: str = Field(..., alias="Configuration Mode")
    external_ipv4_address: str = Field(..., alias="External IPv4 Address")
    external_port: str = Field(..., alias="External Port")
    internal_port: str = Field(..., alias="Internal Port")
    protocol: str = Field(..., alias="Protocol")
    internal_ip: str = Field(..., alias="Internal IPv4 Address")
    status: str = Field(..., alias="PCP Server Result Code")
    allow_proposal: str = Field(..., alias="Allow PCP Port Proposal [Y/N]")

    # Database fields
    host_name: Optional[str] = None
    is_active: bool = True
    created_at: Optional[datetime] = None

    @property
    def is_rdp(self) -> bool:
        return self.internal_port == "3389"

    @property
    def connection_string(self) -> str:
        return f"{self.external_ipv4_address}:{self.external_port}"

    def to_supabase(self) -> dict:
        """Convert to Supabase format"""
        return {
            "config_mode": self.config_mode,
            "external_ipv4_address": self.external_ipv4_address,
            "external_port": self.external_port,
            "internal_port": self.internal_port,
            "protocol": self.protocol,
            "internal_ip": self.internal_ip,
            "status": self.status,
            "allow_proposal": self.allow_proposal.upper(),  # Convert 'Y'/'N' to proper format
            "host_name": self.host_name,
            "is_active": self.is_active,
            "created_at": self.created_at.isoformat() if self.created_at else datetime.utcnow().isoformat()
        }

    class Config:
        populate_by_name = True