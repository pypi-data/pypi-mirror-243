import json
import os
from pathlib import Path

import yaml
from airfold_common.config import merge_dicts
from airfold_common.utils import dict_from_env, model_hierarchy

from airfold_cli.models import Config, UserPermissions, UserProfile

CONFIG_PATH = Path().cwd() / ".airfold" / "config.yaml"
CONFIG_DIR = os.path.dirname(CONFIG_PATH)
PROJECT_DIR = "airfold"

PREFIX = "AIRFOLD"


def save_config(config: Config) -> str:
    os.makedirs(CONFIG_DIR, exist_ok=True)
    with open(CONFIG_PATH, "w") as f:
        yaml.safe_dump(config.dict(), f)
    return str(CONFIG_PATH)


def load_config() -> Config:
    data = yaml.safe_load(open(CONFIG_PATH))

    env_data: dict = dict_from_env(model_hierarchy(Config), PREFIX)
    merge_dicts(data, env_data)

    return Config(**data)


def normalize_path_args(path: list[str] | str | None) -> list[str]:
    res: list[str]
    if not path:
        path = [os.path.join(os.getcwd(), PROJECT_DIR)]
    if isinstance(path, str):
        res = [path]
    else:
        res = path
    return res


def dump_json(data: dict) -> str:
    return json.dumps(data, indent=2)


def get_org_permissions(user: UserProfile, _org_id: str | None = None) -> UserPermissions | None:
    org_id: str = _org_id or user.organizations[0].id
    for perm in user.permissions:
        if perm.org_id == org_id:
            return perm
    return None


def display_roles(user: UserProfile, org_id: str, proj_id: str) -> str:
    if bool([org for org in user.organizations if org.id == org_id]):
        return "Owner"
    for perm in user.permissions:
        if perm.org_id == org_id:
            roles = perm.roles
            for r in roles:
                if f"projects/{proj_id}" in r:
                    return r
            return ",".join(roles)
    return ""


def set_current_project(proj_id):
    config = load_config()
    conf = Config(**config.dict(exclude={"proj_id"}), proj_id=proj_id)
    save_config(conf)
