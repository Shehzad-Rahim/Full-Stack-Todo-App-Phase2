from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session, select
from typing import List
from ...models.task import Task, TaskCreateRequest, TaskRead, TaskUpdate, TaskToggle
from ...database.connection import get_session  # Updated import
from ...api.deps import get_db_session
from ...auth.deps import validate_user_id, get_user_id_from_cookie  # Import the validation dependency
import uuid


router = APIRouter()


@router.post("/tasks", response_model=TaskRead, status_code=status.HTTP_201_CREATED)
def create_task(
    *,
    user_id: str = Depends(get_user_id_from_cookie),  # Get user_id from cookie
    task: TaskCreateRequest,
    db_session: Session = Depends(get_db_session)
):
    """
    Create a new task for the authenticated user.

    Args:
        user_id: The ID of the user creating the task (extracted from HttpOnly cookie)
        task: Task creation data
        db_session: Database session dependency

    Returns:
        TaskRead: The created task with its ID and timestamps
    """
    # Create the task with the validated input
    db_task = Task(
        title=task.title,
        description=task.description,
        completed=task.completed,
        user_id=user_id
    )

    db_session.add(db_task)
    db_session.commit()
    db_session.refresh(db_task)

    return db_task


@router.get("/tasks", response_model=List[TaskRead])
def read_tasks(
    *,
    user_id: str = Depends(get_user_id_from_cookie),  # Get user_id from cookie
    db_session: Session = Depends(get_db_session)
):
    """
    Get all tasks for the authenticated user.

    Args:
        user_id: The ID of the user whose tasks to retrieve (extracted from HttpOnly cookie)
        db_session: Database session dependency

    Returns:
        List[TaskRead]: List of tasks belonging to the user
    """
    # Query tasks for the specific user only
    statement = select(Task).where(Task.user_id == user_id)
    tasks = db_session.exec(statement).all()

    return tasks


@router.get("/tasks/{id}", response_model=TaskRead)
def read_task(
    *,
    user_id: str = Depends(get_user_id_from_cookie),  # Get user_id from cookie
    id: int,
    db_session: Session = Depends(get_db_session)
):
    """
    Get a specific task for the authenticated user.

    Args:
        user_id: The ID of the user (extracted from HttpOnly cookie)
        id: The ID of the task to retrieve
        db_session: Database session dependency

    Returns:
        TaskRead: The requested task

    Raises:
        HTTPException: 404 if task doesn't exist for the user
    """
    # Query task for the specific user only
    statement = select(Task).where(Task.id == id, Task.user_id == user_id)
    db_task = db_session.exec(statement).first()

    if not db_task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found for this user"
        )

    return db_task


@router.put("/tasks/{id}", response_model=TaskRead)
def update_task(
    *,
    user_id: str = Depends(get_user_id_from_cookie),  # Get user_id from cookie
    id: int,
    task: TaskUpdate,
    db_session: Session = Depends(get_db_session)
):
    """
    Update a specific task for the authenticated user.

    Args:
        user_id: The ID of the user (extracted from HttpOnly cookie)
        id: The ID of the task to update
        task: Task update data
        db_session: Database session dependency

    Returns:
        TaskRead: The updated task

    Raises:
        HTTPException: 404 if task doesn't exist for the user
    """
    # Query task for the specific user only
    statement = select(Task).where(Task.id == id, Task.user_id == user_id)
    db_task = db_session.exec(statement).first()

    if not db_task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found for this user"
        )

    # Update task fields based on provided data
    task_data = task.model_dump(exclude_unset=True)
    for field, value in task_data.items():
        setattr(db_task, field, value)

    # Update the updated_at timestamp
    from datetime import datetime, timezone
    db_task.updated_at = datetime.now(timezone.utc)

    db_session.add(db_task)
    db_session.commit()
    db_session.refresh(db_task)

    return db_task


@router.delete("/tasks/{id}")
def delete_task(
    *,
    user_id: str = Depends(get_user_id_from_cookie),  # Get user_id from cookie
    id: int,
    db_session: Session = Depends(get_db_session)
):
    """
    Delete a specific task for the authenticated user.

    Args:
        user_id: The ID of the user (extracted from HttpOnly cookie)
        id: The ID of the task to delete
        db_session: Database session dependency

    Returns:
        dict: Success message

    Raises:
        HTTPException: 404 if task doesn't exist for the user
    """
    # Query task for the specific user only
    statement = select(Task).where(Task.id == id, Task.user_id == user_id)
    db_task = db_session.exec(statement).first()

    if not db_task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found for this user"
        )

    db_session.delete(db_task)
    db_session.commit()

    return {"message": "Task deleted successfully"}


@router.patch("/tasks/{id}/complete", response_model=TaskRead)
def toggle_task_completion(
    *,
    user_id: str = Depends(get_user_id_from_cookie),  # Get user_id from cookie
    id: int,
    task_toggle: TaskToggle,
    db_session: Session = Depends(get_db_session)
):
    """
    Toggle the completion status of a specific task for the authenticated user.

    Args:
        user_id: The ID of the user (extracted from HttpOnly cookie)
        id: The ID of the task to update
        task_toggle: Completion status toggle data
        db_session: Database session dependency

    Returns:
        TaskRead: The updated task with toggled completion status

    Raises:
        HTTPException: 404 if task doesn't exist for the user
    """
    # Query task for the specific user only
    statement = select(Task).where(Task.id == id, Task.user_id == user_id)
    db_task = db_session.exec(statement).first()

    if not db_task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found for this user"
        )

    # Toggle the completion status
    db_task.completed = task_toggle.completed

    # Update the updated_at timestamp
    from datetime import datetime, timezone
    db_task.updated_at = datetime.now(timezone.utc)

    db_session.add(db_task)
    db_session.commit()
    db_session.refresh(db_task)

    return db_task