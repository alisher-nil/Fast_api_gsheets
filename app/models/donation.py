from sqlalchemy import Column, ForeignKey, Integer, Text

from app.core.db import Base
from app.models.mixins import FundMixin


class Donation(Base, FundMixin):
    comment = Column(Text)
    user_id = Column(Integer, ForeignKey("user.id"), nullable=False)
