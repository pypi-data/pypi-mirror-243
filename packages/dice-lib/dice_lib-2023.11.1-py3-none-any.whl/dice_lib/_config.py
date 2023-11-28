from dataclasses import dataclass
from enum import Enum
from pathlib import Path
from typing import Any, Dict, List, Optional

from omegaconf import OmegaConf

DEFAULT_DICE_CONFIG_PATH = "/etc/dice/config.yaml"


class ServerStatus(Enum):
    ONLINE = "online"
    OFFLINE = "offline"
    ACTIVE = "active"
    RETIRED = "retired"
    COMMISSIONING = "commissioning"
    DECOMMISSIONING = "decommissioning"


@dataclass
class ComputingElement:
    name: str
    status: str
    ce_type: str


@dataclass
class StorageElement:
    name: str
    status: str
    se_type: str
    endpoints: Dict[str, str]
    root_dir: str


@dataclass
class ComputingGrid:
    site_name: str
    cms_site_name: str
    computing_elements: List[ComputingElement]
    storage_elements: List[StorageElement]
    FTS_SERVERS: List[str]


@dataclass
class Storage:
    mounts: List[str]
    binaries: Optional[Dict[str, str]]
    env: Optional[Dict[str, str]]
    extras: Optional[Dict[str, Any]]
    protocol: Optional[str] = "file://"
    remove_mount_for_native_access: Optional[bool] = False


@dataclass
class LoginNode:
    name: str
    status: ServerStatus
    group: str


@dataclass
class DiceConfig:
    cluster_name: str
    documentation: str
    login_nodes: List[LoginNode]
    computing_grid: ComputingGrid
    storage: Dict[str, Storage]
    glossary: Dict[str, str]
    site_info: Dict[str, Any]
    node_info: Dict[str, Any]


def load_config(config_file: str = DEFAULT_DICE_CONFIG_PATH) -> Any:
    path = Path(config_file)
    if not path.exists():
        raise FileNotFoundError(
            f"DICE config, {config_file}, does not exist. Please contact dice-admin"
        )
    schema = OmegaConf.structured(DiceConfig)
    conf = OmegaConf.load(path)
    merged_conf = OmegaConf.merge(schema, conf)
    return merged_conf
