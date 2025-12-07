from sqlalchemy.orm import Session
from app.models import User,Task
from app.schemas import UserCreate,TaskCreate
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"],deprecated = "auto")


#User Crud

def get_user_by_email(db: Session, email: str):
    return db.query(User).filter(User.email==email).first()

def create_user(db:Session,user:UserCreate):
        hashed_pw = pwd_context.hash(user.password)
        new_user = User(
              email = user.email,
              password = hashed_pw
        
        )

        db.add(new_user)
        db.commit()
        db.refresh(new_user)

        return new_user

# task Crud

def create_task(db:Session,task:TaskCreate,user_id:int):
      
      new_task = Task(
            title = task.title,
            status ="todo",
            user_id = user_id,
            description = task.description
        )

      db.add(new_task)
      db.commit()
      db.refresh(new_task)

      return new_task

def get_user_tasks(db: Session, user_id: int):
   
    return (
        db.query(Task)
        .filter(Task.user_id == user_id,Task.status=="todo")
        .all()
    )


def get_progress_tasks(db: Session, user_id: int):
    return (
        db.query(Task)
        .filter(Task.user_id == user_id, Task.status == "progress")
        .all()
    )







def get_completed_tasks(db: Session, user_id: int):
   
    return (
        db.query(Task)
        .filter(Task.user_id == user_id, Task.status == "done")
        .all()
    )

def update_task_status(db: Session, task_id: int, new_status: str, user_id: int):

    allowed_status = ["todo","progress","done"]
    if new_status not in allowed_status:
         return None
  
    task = (
        db.query(Task)
        .filter(Task.id == task_id, Task.user_id == user_id)
        .first()
    )

    if task is None:
        return None

    task.status = new_status
    db.commit()
    db.refresh(task)

    return task


def get_tasks_by_status(db: Session, user_id: int, status: str):
    return (
        db.query(Task)
        .filter(Task.user_id == user_id, Task.status == status)
        .all()
    )























































































































































































def delete_completed_task(db: Session, task_id: int, user_id: int):
 
    task = (
        db.query(Task)
        .filter(
            Task.id == task_id,
            Task.user_id == user_id,
            Task.status == "done"
        )
        .first()
    )

    if task is None:
        return None

    db.delete(task)
    db.commit()
    return True