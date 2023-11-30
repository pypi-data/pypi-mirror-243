"""
The aurori project

Copyright (C) 2022  Marcus Drobisch,

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU Affero General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU Affero General Public License for more details.

You should have received a copy of the GNU Affero General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""

__authors__ = ["Marcus Drobisch"]
__contact__ = "aurori@fabba.space"
__credits__ = []
__license__ = "AGPLv3+"

import hashlib
import bcrypt
from datetime import datetime 
from sqlalchemy import Boolean, Column, DateTime, Integer, String, LargeBinary
from sqlalchemy.ext.hybrid import hybrid_property, hybrid_method

from aurori.database import SQLModelBase
from aurori.utils import unicode_string_to_bytes


class UserBase(SQLModelBase):
    __abstract__ = True
    __tablename__ = 'users'
    # nonvolatile data stored in the db
    id = Column(Integer, primary_key=True, autoincrement=True)
    _password_hash = Column(LargeBinary(60), nullable=False)
    _pin_hash = Column(LargeBinary(60))
    _salt = Column(String(128))
    _api_key_hash = Column(String(256), nullable=True, default=None)
    email = Column(String(120), index=True, unique=True)
    username = Column(String(120), index=True, unique=True)
    firstname = Column(String(120), default="")
    lastname = Column(String(120), default="")
    organization = Column(String(120), default="")
    phone = Column(String(64), default="")
    account_created_date = Column(DateTime, default=datetime.utcnow)
    last_login_date = Column(DateTime, default=datetime.utcnow)
    password_reset_expired_date = Column(DateTime, default=datetime.utcnow)
    password_reset_hash = Column(String(128), default="")
    account_verified = Column(Boolean, default=False)
    account_activated = Column(Boolean, default=False)
    account_locked = Column(Boolean, default=False)
    ldap = Column(Boolean, default=False)
    ldap_dn = Column(String(64), default="")
    ldap_username = Column(String(64), default="")
    admin = Column(Boolean, default=False)
    pinAttempts = Integer()
    loginAttempts = Integer()

    def __init__(self, email, password, isAdmin=False, skip_password=False):
        self.email = email
        if skip_password is False:
            self.password = password
        self.admin = isAdmin

    def __repr__(self):
        return '<User {} {} {}>'.format(self.firstname, self.lastname,
                                          self.email)

    @hybrid_property
    def password(self):
        return self._password_hash

    @password.setter
    def password(self, plaintext_password):
        password_bytes = unicode_string_to_bytes(plaintext_password)
        salt = bcrypt.gensalt(rounds=12, prefix=b'2b')
        self._password_hash =  bcrypt.hashpw(password_bytes, salt)

    @hybrid_method
    def checkPassword(self, plaintext_password):
        return bcrypt.checkpw(unicode_string_to_bytes(plaintext_password),self.password)

    @hybrid_property
    def pin(self):
        return self._pin_hash

    @pin.setter
    def pin(self, plaintext_pin):
        pin_bytes = unicode_string_to_bytes(plaintext_pin)
        salt = bcrypt.gensalt(rounds=12, prefix=b'2b')
        self._password_hash =  bcrypt.hashpw(pin_bytes, salt)

    @hybrid_method
    def checkPin(self, plaintext_pin):
        return bcrypt.checkpw(unicode_string_to_bytes(plaintext_pin),self.pin)


    @hybrid_property
    def api_key(self):
        return self._api_key_hash

    @api_key.setter
    def api_key(self, plaintext_api_key):
        self._api_key_hash = hashlib.sha512(
            plaintext_api_key.encode('utf8')).hexdigest()

    @hybrid_method
    def check_api_key(self, plaintext_api_key):
        return hashlib.sha512(plaintext_api_key).hexdigest() == self.api_key

    # checks if user has a certain permission
    @hybrid_method
    def has_permission(self, permission_to_check):
        for permission_group in self.permission_groups:
            for permission in permission_group.permissions:
                if type(permission_to_check) is str:
                    permission_key = permission_to_check
                else:
                    permission_key = str(permission_to_check.__module__).split(
                        '.')[1] + '.' + permission_to_check.__name__
                if permission.name == permission_key:
                    return True
        return False
