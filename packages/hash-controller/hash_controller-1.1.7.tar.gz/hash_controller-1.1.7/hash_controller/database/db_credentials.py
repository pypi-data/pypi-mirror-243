from typing import Optional
from pydantic import BaseModel


class DataBaseCredentials(BaseModel):
    db_user: Optional[str]
    db_pass: Optional[str]
    db_host: Optional[str]
    db_port: Optional[int]
