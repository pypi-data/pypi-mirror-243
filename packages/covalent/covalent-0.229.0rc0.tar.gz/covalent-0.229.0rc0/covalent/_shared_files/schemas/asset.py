# Copyright 2021 Agnostiq Inc.
#
# This file is part of Covalent.
#
# Licensed under the Apache License 2.0 (the "License"). A copy of the
# License may be obtained with this software package or at
#
#     https://www.apache.org/licenses/LICENSE-2.0
#
# Use of this file is prohibited except in compliance with the License.
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""FastAPI models for /api/v1/resultv2 endpoints"""

from typing import Optional

from pydantic import BaseModel


class AssetSchema(BaseModel):
    digest_alg: Optional[str] = None
    digest: Optional[str] = None
    uri: Optional[str] = None
    remote_uri: Optional[str] = None

    # Size of the asset in bytes
    size: Optional[int] = 0


class AssetUpdate(BaseModel):
    remote_uri: Optional[str] = None
    size: Optional[int] = None
    digest_alg: Optional[str] = None
    digest: Optional[str] = None
