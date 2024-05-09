from fastapi import FastAPI, HTTPException
from uuid import UUID, uuid4
from typing import List
from pydantic import BaseModel

app = FastAPI()

class activity(BaseModel):
    name:str
    status:str
    id: UUID

class activityUpdate(BaseModel):
    name: str
    status: str

activity_list ={
    UUID('c500d2da-f05e-4cec-971e-d1c8f03ecb98'):activity(id=UUID('c500d2da-f05e-4cec-971e-d1c8f03ecb98'),name='Boxing Training',status='1')
}
@app.get('/')
def landing_get():
    return('Main:Page')

@app.get('/todo')
def get_activity_list():
    return (list(activity_list.values()))

@app.get('/todo/user')
def user_todo_activity(userid:UUID):
    userActivity = [activity for activity in activity_list.values() if activity.id == userid]
    return userActivity

@app.get('/todo/search/{activity_id}')
def specific_todo_activity(activity_id: UUID):
    specificActivity = activity_list.get(activity_id)
    if not specificActivity:
        raise HTTPException(status_code=404,detail='Searched activity not found')
    return specificActivity

@app.post('/add')
def add(activity):
    activity_list[activity.id] = activity
    return {activity, 'New activity added!'}

@app.delete('/delete/{activity_id}')
def delete(UUID):
    if UUID in activity_list:
        del activity_list[UUID]
        return {'Success':True,'Message':'Activity deleted!'}
    else:
        return {'Success':False, 'Message':'Activity not found!'}

@app.put('/todo/update/{activity_id}')
def update(UUID, activityUpdate):
    if UUID not in activity_list:
        raise HTTPException(detail = 'Activity not found')
    if activityUpdate.name:
        activity_list[UUID].name = activityUpdate.name
    if activityUpdate.status:
        activity_list[UUID].status = activityUpdate.status
    return {'Success':True,'Message': 'Updated activity updated!'}
