from sqlalchemy import Column, String, Text

from app.core.constants import PROJECT_NAME_MAX_LENGTH
from app.core.db import Base
from app.models.mixins import FundMixin


class CharityProject(Base, FundMixin):
    name = Column(String(PROJECT_NAME_MAX_LENGTH), nullable=False)
    description = Column(Text, nullable=False)
