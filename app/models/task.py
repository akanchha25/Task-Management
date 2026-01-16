import enum
from sqlalchemy import Column, Integer, String, Enum, ForeignKey, Table, DateTime, func
from sqlalchemy.orm import relationship
from app.db.base import Base

# 1. Association Table for Many-to-Many (Users <-> Tasks)
task_assignees = Table(
    'task_assignees', Base.metadata,
    Column('user_id', Integer, ForeignKey('users.id')),
    Column('task_id', Integer, ForeignKey('tasks.id'))
)

# 2. Association Table for Task Dependencies (Task <-> Task)
# "blocker" must finish before "blocked"
task_dependencies = Table(
    'task_dependencies', Base.metadata,
    Column('blocker_id', Integer, ForeignKey('tasks.id'), primary_key=True),
    Column('blocked_id', Integer, ForeignKey('tasks.id'), primary_key=True)
)

class TaskStatus(str, enum.Enum):
    TODO = "TODO"
    IN_PROGRESS = "IN_PROGRESS"
    BLOCKED = "BLOCKED"
    DONE = "DONE"

class Task(Base):
    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True, nullable=False)
    description = Column(String, nullable=True)
    status = Column(Enum(TaskStatus), default=TaskStatus.TODO)
    priority = Column(Integer, default=1) # 1=Low, 5=High
    due_date = Column(DateTime(timezone=True), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Foreign Key to Creator
    owner_id = Column(Integer, ForeignKey("users.id"))
    
    # Relationships
    owner = relationship("User", backref="owned_tasks")
    assignees = relationship("User", secondary=task_assignees, backref="assigned_tasks")

    # Self-Referential Relationship (Dependencies)
    blocking_tasks = relationship(
        "Task",
        secondary=task_dependencies,
        primaryjoin=id==task_dependencies.c.blocked_id,
        secondaryjoin=id==task_dependencies.c.blocker_id,
        backref="blocked_by_this_task"
    )