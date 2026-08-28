# from database import Base
# from sqlalchemy import Boolean,ForeignKey, Column, Integer, String
# from sqlalchemy.orm import relationship

# class TaskModel(Base):
#     __tablename__ = "tasks"

#     id = Column(Integer, primary_key=True, index=True)
#     title= Column(String, nullable=False)
#     description=Column(String, nullable=True)
#     completed=Column(Boolean, default=False)

#     user_id = Column(Integer, ForeignKey("users.id"), nullable=False)

#     owner = relationship("UserModel",back_populates="tasks")

from database import Base
from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship


class TaskModel(Base):
    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    description = Column(String, nullable=True)
    completed = Column(Boolean, default=False)

    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    owner = relationship("UserModel", back_populates="tasks")