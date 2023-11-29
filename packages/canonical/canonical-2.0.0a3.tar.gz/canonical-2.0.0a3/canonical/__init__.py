# Copyright (C) 2022 Cochise Ruhulessin
#
# All rights reserved. No warranty, explicit or implicit, provided. In
# no event shall the author(s) be liable for any claim or damages.
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
from . import protocols
from .domainname import DomainName
from .emailaddress import EmailAddress
from .hostname import Hostname
from .iso3166 import ISO3166Alpha2
from .phonenumber import Phonenumber
from .resourceidentifier import ResourceIdentifier
from .resourcename import ResourceName
from .stringtype import StringType


__all__: list[str] = [
    'protocols',
    'DomainName',
    'EmailAddress',
    'Hostname',
    'ISO3166Alpha2',
    'Phonenumber',
    'ResourceIdentifier',
    'ResourceName',
    'StringType',
]