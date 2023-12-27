#!/usr/bin/env python3

'''
Task model
'''

from typing import Optional
from datetime import datetime
from pydantic import BaseModel, Field
import uuid

class TaskBase(BaseModel):
    '''
    Base model for Task
    '''
    id: str = Field(default_factory=lambda: str(uuid.uuid4()), alias='_id', description='Unique identifier for the task')
    title: str 
    description: Optional[str]
    completed: Optional[bool] = False
    created_at: Optional[datetime] = Field(default_factory=datetime.utcnow, alias='createdAt',description='Date and time when the task was created')

    class Config:
        allow_population_by_field_name = True

class TaskCreate(TaskBase):
    '''
    Model for creating a task
    '''
    title: str
    description: Optional[str]
    completed: Optional[bool] = False
    created_at: Optional[datetime] = Field(default_factory=datetime.utcnow, alias='createdAt',description='Date and time when the task was created')

    class Config:
        allow_population_by_field_name = True

class TaskUpdate(TaskBase):
    '''
    Model for updating a task
    '''
    updated_at: Optional[datetime] = Field(default_factory=datetime.utcnow, alias='updatedAt',description='Date and time when the task was updated')
    class Config:
        allow_population_by_field_name = True
