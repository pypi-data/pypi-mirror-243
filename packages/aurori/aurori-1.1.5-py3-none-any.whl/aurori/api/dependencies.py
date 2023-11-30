from typing import Annotated
from fastapi import Depends
from aurori.users.dependencies import get_manadatory_user, get_optional_user

UserDep = Annotated[dict, Depends(get_manadatory_user)]
OptionalUserDep = Annotated[dict, Depends(get_optional_user)]
