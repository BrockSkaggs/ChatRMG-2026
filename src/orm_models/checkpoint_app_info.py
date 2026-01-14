from orm_models.base import Base
from sqlalchemy import Column, String, DateTime

class CheckpointAppInfo(Base):
    __tablename__ = "checkpoint_app_info"

    # Define your columns and relationships here
    thread_id = Column(String, primary_key=True)
    thread_name = Column(String(255), nullable=True)
    user_name = Column(String(255), nullable=True)
    created_on = Column(DateTime, nullable=True)

    def __repr__(self):
        return f"<CheckpointAppInfo(thread_id={self.thread_id}, thread_name={self.thread_name}, user_name={self.user_name}, created_on={self.created_on})>"