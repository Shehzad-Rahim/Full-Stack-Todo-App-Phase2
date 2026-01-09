import pytest
from sqlmodel import Session
from src.models.task import Task, TaskCreate, TaskUpdate
from src.api.routes.tasks import (
    create_task, read_tasks, read_task, update_task, delete_task, toggle_task_completion
)


def test_create_task(session: Session):
    """
    Test creating a task for a specific user.
    """
    user_id = "test_user_123"

    task_create = TaskCreate(
        title="Test Task",
        description="Test Description",
        completed=False,
        user_id=user_id
    )

    created_task = create_task(user_id=user_id, task=task_create, db_session=session)

    assert created_task.title == "Test Task"
    assert created_task.description == "Test Description"
    assert created_task.completed is False
    assert created_task.user_id == user_id
    assert created_task.id is not None


def test_read_tasks(session: Session):
    """
    Test reading all tasks for a specific user.
    """
    user_id = "test_user_123"

    # Create a task first
    task_create = TaskCreate(
        title="Test Task",
        description="Test Description",
        completed=False,
        user_id=user_id
    )
    create_task(user_id=user_id, task=task_create, db_session=session)

    # Read tasks for the user
    tasks = read_tasks(user_id=user_id, db_session=session)

    assert len(tasks) == 1
    assert tasks[0].title == "Test Task"
    assert tasks[0].user_id == user_id


def test_read_specific_task(session: Session):
    """
    Test reading a specific task for a specific user.
    """
    user_id = "test_user_123"

    # Create a task first
    task_create = TaskCreate(
        title="Test Task",
        description="Test Description",
        completed=False,
        user_id=user_id
    )
    created_task = create_task(user_id=user_id, task=task_create, db_session=session)

    # Read the specific task
    read_task_result = read_task(user_id=user_id, id=created_task.id, db_session=session)

    assert read_task_result.id == created_task.id
    assert read_task_result.title == "Test Task"
    assert read_task_result.user_id == user_id


def test_update_task(session: Session):
    """
    Test updating a specific task for a specific user.
    """
    user_id = "test_user_123"

    # Create a task first
    task_create = TaskCreate(
        title="Original Task",
        description="Original Description",
        completed=False,
        user_id=user_id
    )
    created_task = create_task(user_id=user_id, task=task_create, db_session=session)

    # Update the task
    task_update = TaskUpdate(
        title="Updated Task",
        description="Updated Description",
        completed=True
    )
    updated_task = update_task(
        user_id=user_id, id=created_task.id, task=task_update, db_session=session
    )

    assert updated_task.id == created_task.id
    assert updated_task.title == "Updated Task"
    assert updated_task.description == "Updated Description"
    assert updated_task.completed is True


def test_delete_task(session: Session):
    """
    Test deleting a specific task for a specific user.
    """
    user_id = "test_user_123"

    # Create a task first
    task_create = TaskCreate(
        title="Test Task",
        description="Test Description",
        completed=False,
        user_id=user_id
    )
    created_task = create_task(user_id=user_id, task=task_create, db_session=session)

    # Verify task exists
    existing_task = read_task(user_id=user_id, id=created_task.id, db_session=session)
    assert existing_task.id == created_task.id

    # Delete the task
    delete_result = delete_task(user_id=user_id, id=created_task.id, db_session=session)
    assert delete_result == {"message": "Task deleted successfully"}

    # Verify task no longer exists
    with pytest.raises(Exception):  # This would typically be an HTTPException in the actual API
        read_task(user_id=user_id, id=created_task.id, db_session=session)


def test_toggle_task_completion(session: Session):
    """
    Test toggling the completion status of a task.
    """
    user_id = "test_user_123"

    # Create a task first
    task_create = TaskCreate(
        title="Test Task",
        description="Test Description",
        completed=False,
        user_id=user_id
    )
    created_task = create_task(user_id=user_id, task=task_create, db_session=session)

    # Verify initial state
    initial_task = read_task(user_id=user_id, id=created_task.id, db_session=session)
    assert initial_task.completed is False

    # Toggle completion to True
    from src.models.task import TaskToggle
    task_toggle = TaskToggle(completed=True)
    toggled_task = toggle_task_completion(
        user_id=user_id, id=created_task.id, task_toggle=task_toggle, db_session=session
    )

    assert toggled_task.id == created_task.id
    assert toggled_task.completed is True

    # Toggle completion back to False
    task_toggle_false = TaskToggle(completed=False)
    toggled_task_false = toggle_task_completion(
        user_id=user_id, id=created_task.id, task_toggle=task_toggle_false, db_session=session
    )

    assert toggled_task_false.id == created_task.id
    assert toggled_task_false.completed is False


def test_user_isolation_read_tasks(session: Session):
    """
    Test that users can only read their own tasks.
    """
    user1_id = "user1_123"
    user2_id = "user2_456"

    # Create tasks for user1
    task_create1 = TaskCreate(
        title="User1 Task",
        description="User1 Description",
        completed=False,
        user_id=user1_id
    )
    create_task(user_id=user1_id, task=task_create1, db_session=session)

    # Create tasks for user2
    task_create2 = TaskCreate(
        title="User2 Task",
        description="User2 Description",
        completed=False,
        user_id=user2_id
    )
    create_task(user_id=user2_id, task=task_create2, db_session=session)

    # Each user should only see their own tasks
    user1_tasks = read_tasks(user_id=user1_id, db_session=session)
    user2_tasks = read_tasks(user_id=user2_id, db_session=session)

    assert len(user1_tasks) == 1
    assert user1_tasks[0].title == "User1 Task"
    assert user1_tasks[0].user_id == user1_id

    assert len(user2_tasks) == 1
    assert user2_tasks[0].title == "User2 Task"
    assert user2_tasks[0].user_id == user2_id


def test_user_isolation_read_specific_task(session: Session):
    """
    Test that users cannot read tasks belonging to other users.
    """
    user1_id = "user1_123"
    user2_id = "user2_456"

    # Create a task for user1
    task_create = TaskCreate(
        title="User1 Task",
        description="User1 Description",
        completed=False,
        user_id=user1_id
    )
    created_task = create_task(user_id=user1_id, task=task_create, db_session=session)

    # User2 should not be able to read user1's task
    with pytest.raises(Exception):  # This would typically be an HTTPException in the actual API
        read_task(user_id=user2_id, id=created_task.id, db_session=session)