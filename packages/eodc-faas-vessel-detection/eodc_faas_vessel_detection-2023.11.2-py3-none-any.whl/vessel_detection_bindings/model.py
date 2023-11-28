import os
import logging
import pyproj

from pathlib import Path
from typing import Optional, Union
from pydantic import BaseModel

logger = logging.getLogger(__name__)

from argo_workflows.model.io_argoproj_workflow_v1alpha1_workflow_create_request import (
    IoArgoprojWorkflowV1alpha1WorkflowCreateRequest,
)

legacy_path = Path(os.path.dirname(os.path.abspath(__file__))) / "workflow.yaml"
        
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


class VesselDetectionWorkflow(IoArgoprojWorkflowV1alpha1WorkflowCreateRequest):
    """ Vessel detection workflow creation request. """
    
    def __init__(self, *args, **kwargs):
        __file__ = "/vessel_detection/bindings/python/vessel_detection_bindings/workflow.yaml"
        with open(__file__) as f:
            manifest = yaml.safe_load(f.read())
        super().__init__(manifest=manifest, *args, **kwargs)

    @property
    def name(self):
        try:
            return self["manifest"]["metadata"]["name"]
        except KeyError:
            return None 
                
    @property
    def namespace(self):
        try:
            return self["manifest"]["metadata"]["namespace"]
        except KeyError:
            return None
        
    @property
    def job_id(self):
        try:
            return self["manifest"]["spec"]["arguments"]["parameters"][0]["value"]
        except KeyError:
            return None
        
    def set_names(self, name):
        self["manifest"]["metadata"]["name"] = name
        return name
            
    def set_namespace(self, namespace):
        self["manifest"]["metadata"]["namespace"] = namespace
        return namespace
    
    def set_job_id(self, job_id):
        self["manifest"]["spec"]["arguments"]["parameters"][0]["value"] = job_id
        return job_id
    
    def set_output_directory(self, output_dir):
        self["manifest"]["spec"]["arguments"]["parameters"][1]["value"] = output_dir
        return output_dir

    def set_detection_paramters(self, detection_parameters: VesselDetectionParameters):
        self["manifest"]["spec"]["arguments"]["parameters"][1]["value"] = detection_parameters.dict()
        return detection_parameters