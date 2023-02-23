from typing import Union

from fastapi import FastAPI
from pydantic import BaseModel
import mysql.connector

db = mysql.connector.connect(
    host="localhost",
    user="user",
    password="mypassword",
    database="APITest"
)

app = FastAPI()


class Task(BaseModel):
    task: str
    importance: str
    completed: bool


@app.get("/tasks")
def read_tasks():

    cursor = db.cursor()

    cursor.execute("SELECT * FROM TableAPI")

    results = cursor.fetchall()

    tasks = []
    for row in results:
        id = row[0]
        task = row[1]
        importance = row[2]
        completed = bool(row[3])
        tasks.append({"id": id, "task": task, "importance": importance, "completed": completed})

    cursor.close()

    return tasks


@app.post("/tasks")
def create_task(task: Task):

    cursor = db.cursor()

    sql = "INSERT INTO TableAPI (Task, Importance, Completed) VALUES (%s, %s, %s)"
    values = (task.task, task.importance, task.completed)
    cursor.execute(sql, values)
    db.commit()

    task_id = cursor.lastrowid

    cursor.close()

    return {"id": task_id, **task.dict()}


@app.put("/tasks/{task_id}")
def update_task(task_id: int, task: Task):
    cursor = db.cursor()

    sql = "UPDATE TableAPI SET Task=%s, Importance=%s, Completed=%s WHERE Id=%s"
    values = (task.task, task.importance, task.completed, task_id)
    cursor.execute(sql, values)
    db.commit()

    cursor.close()

    return {"id": task_id, **task.dict()}


@app.delete("/tasks/{task_id}")
def delete_task(task_id: int):
    cursor = db.cursor()

    sql = "DELETE FROM TableAPI WHERE Id=%s"
    values = (task_id,)
    cursor.execute(sql, values)
    db.commit()
