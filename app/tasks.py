from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from database import get_db
from app.auth import get_current_user
from app import crud
from app.schemas import TaskCreate, TaskUpdate, TaskResponse

router = APIRouter(
    prefix="/tasks",
    tags=["Tasks"]
)


# Create a Task
@router.post("/", response_model=TaskResponse)
def create_task(
    task: TaskCreate,
    db: Session = Depends(get_db),
    current_user: int = Depends(get_current_user)
):
    return crud.create_task(db, task, current_user.id)


# Get ALL non-completed tasks
@router.get("/", response_model=list[TaskResponse])
def get_tasks(
    db: Session = Depends(get_db),
    current_user: int = Depends(get_current_user)
):
    return crud.get_user_tasks(db, current_user.id)


# Get TODO tasks only
@router.get("/todo", response_model=list[TaskResponse])
def get_todo_tasks(
    db: Session = Depends(get_db),
    current_user: int = Depends(get_current_user)
):
    return crud.get_tasks_by_status(db, current_user.id, "todo")


# Get IN-PROGRESS tasks only
@router.get("/progress", response_model=list[TaskResponse])
def get_progress_tasks(
    db: Session = Depends(get_db),
    current_user: int = Depends(get_current_user)
):
    return crud.get_tasks_by_status(db, current_user.id, "progress")


# Get completed tasks
@router.get("/completed", response_model=list[TaskResponse])
def get_completed_tasks(
    db: Session = Depends(get_db),
    current_user: int = Depends(get_current_user)
):
    return crud.get_completed_tasks(db, current_user.id)


# Update task status
@router.put("/{task_id}", response_model=TaskResponse)
def update_task_status(
    task_id: int,
    task_update: TaskUpdate,
    db: Session = Depends(get_db),
    current_user: int = Depends(get_current_user)
):
    updated_task = crud.update_task_status(
        db, task_id, task_update.status, current_user.id
    )

    if not updated_task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found or not allowed"
        )

    return updated_task


# Delete completed task
@router.delete("/{task_id}")
def delete_complete_task(
    task_id: int,
    db: Session = Depends(get_db),
    current_user: int = Depends(get_current_user)
):
    deleted = crud.delete_completed_task(db, task_id, current_user.id)

    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Task not found"
        )

    return {"message": "Task deleted successfully"}
