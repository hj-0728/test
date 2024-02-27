from datetime import datetime
from typing import Optional

from infra_basic.basic_model import VersionedModel
from infra_utility.datetime_helper import local_now


class PeopleRelationshipModel(VersionedModel):
    subject_people_id: str
    object_people_id: str
    relationship: str
    started_on: datetime = local_now()
    ended_on: Optional[datetime]
