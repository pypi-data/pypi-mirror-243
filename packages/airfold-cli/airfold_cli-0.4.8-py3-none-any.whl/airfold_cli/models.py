from enum import Enum
from typing import List, Optional

from pydantic import BaseModel, Field


class Project(BaseModel, frozen=True):
    id: str
    name: str


class Organization(BaseModel):
    id: str
    name: str

    class Config:
        allow_population_by_field_name = True


class Permission(BaseModel):
    Effect: str
    Action: str
    Resource: str


class UserPermissions(BaseModel):
    org_id: str = Field(..., alias="orgId")
    user_perms: list[Permission] = Field(..., alias="userPerms")
    roles: list[str]

    class Config:
        allow_population_by_field_name = True


class UserProfile(BaseModel):
    id: str
    fname: str
    lname: str
    email: str
    avatar: Optional[str] = None
    full_name: str = Field(..., alias="fullName")
    organizations: List[Organization]
    permissions: List[UserPermissions]

    class Config:
        allow_population_by_field_name = True


class ProjectProfile(BaseModel):
    project_id: str = Field(..., alias="projectId")
    org_id: str = Field(..., alias="orgId")
    permissions: List[Permission]

    class Config:
        allow_population_by_field_name = True


class OverwriteType(str, Enum):
    always = "always"
    never = "never"
    auto = "auto"

    def __str__(self):
        return self.value


class Config(BaseModel, frozen=True):
    endpoint: str
    org_id: str
    proj_id: str
    key: str


class CommandType(str, Enum):
    CREATE = "CREATE"
    DELETE = "DELETE"
    REPLACE = "REPLACE"
    RENAME = "RENAME"
    UNDELETE = "UNDELETE"
    FAIL = "FAIL"
    UPDATE = "UPDATE"


class Command(BaseModel, frozen=True):
    cmd: CommandType
    args: list[dict]


class OutputDataFormat(str, Enum):
    JSON = "json"
    NDJSON = "ndjson"

    def __str__(self):
        return self.value
