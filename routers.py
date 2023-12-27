#!/usr/bin/env python3

'''
Routes for the API
'''

from fastapi import APIRouter, Body, Request, HTTPException, status
from model import TaskUpdate,TaskBase, TaskCreate
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder

# Create the router
router = APIRouter()

# Get all tasks
@router.get('/', response_description='List all tasks')
async def list_tasks(request: Request):
    '''
    List all tasks
    '''
    Tasks = request.app.mongodb['tasks']
    
    selector = {}
    tasks = []

    async for task in Tasks.find(selector):
        task = TaskBase(**task)
        tasks.append(task)

    return tasks

# Create a task
@router.post('/', response_description='Add a new task')
async def create_task(request: Request, task: TaskCreate = Body(...)):
    '''
    Add a new task
    '''
    Tasks = request.app.mongodb['tasks']

    task = task.dict(by_alias=True)
    
    if (task_exists := await Tasks.find_one({'title': task['title']})) is not None:
        raise HTTPException(status_code=404, detail=f'Task {task["name"]} already exists')
    
    new_task = await Tasks.insert_one(task)

    if (created_task := await Tasks.find_one({'_id': new_task.inserted_id})) is not None:
        return JSONResponse(status_code=status.HTTP_201_CREATED, content=jsonable_encoder(created_task))
    
    raise HTTPException(status_code=400, detail='Something went wrong')

# Update a task
@router.patch('/{task_id}', response_description='Update a task')
async def update_task(task_id: str,request: Request, task: TaskUpdate = Body(...)):
    '''
    Update a task
    '''
    print(task)
    Tasks = request.app.mongodb['tasks']

    if 'title' in task:
        if len(task['title']) == 0:
            raise HTTPException(status_code=404, detail=f'Task title cannot be empty')
        
    if (task_exists := await Tasks.find_one({'_id': task_id})) is None:
        raise HTTPException(status_code=404, detail=f'Task {task_id} not found')
    
    updated_result = await Tasks.update_one({'_id': task_id}, {'$set': task})

    if updated_result.modified_count == 1:
        if (updated_result := await Tasks.find_one({'_id': task_id})) is not None:
            return updated_result
        
    raise HTTPException(status_code=400, detail='Failed to update task')

# Delete a task
@router.delete('/{task_id}', response_description='Delete a task')
async def delete_event(task_id: str, request: Request):
    Tasks = request.app.mongodb['tasks']

    delete_result = await Tasks.delete_one({'_id': task_id})
    if delete_result.deleted_count == 1:
        return JSONResponse(status_code=status.HTTP_204_NO_CONTENT)
    
    raise HTTPException(status_code=404, detail=f'Task {task_id} not found')