import uuid
from dataclasses import dataclass
import pydantic
import re


email_reg = re.compile("^[_A-Za-z0-9]+([_A-Za-z0-9-]+)*@[A-Za-z0-9-]{1,}.[A-Za-z0-9]{1,}")


class User(pydantic.BaseModel):
    email: str

    @pydantic.validator("email")
    def validate_email(cls, value):
        if not re.search(email_reg, value):
            raise ValueError("email not validate")

        return value

