import logging

from pathlib import Path
from typing import Optional, Union
from pydantic import BaseModel

logger = logging.getLogger(__name__)
        
class VesselDetectionParameters(BaseModel):
    """Pydantic model of sen2like supported parameters."""

    collection_id: str = "SENTINEL1_GRD"
    bbox: Optional[Union[tuple[float, ...], list[float], str]]

    # datetime needs to be formatted as required by
    # https://pystac-client.readthedocs.io/en/latest/api.html#pystac_client.Client.search
    datetime: Optional[str]

    stac_url: str
    user_workspace: Path
    
    recall: bool = True

    @property
    def root_path(self) -> Path:
        return self.user_workspace / "VESSEL"

    @property
    def output_path(self) -> Path:
        return self.root_path / "output"

    @property
    def snap_path(self) -> Path:
        return self.root_path / "SNAP"

    @property
    def tmp_path(self) -> Path:
        return self.root_path / "tmp"
