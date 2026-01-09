import pytest
from fastapi.testclient import TestClient
from src.main import app
from src.models.task import Task


def test_create_task_integration(client: TestClient):
    """
    Integration test for creating a task via the API.
    """
    user_id = "test_user_123"

    response = client.post(
        f"/api/{user_id}/tasks",
        json={
            "title": "Integration Test Task",
            "description": "Integration test description",
            "completed": False,
            "user_id": user_id
        }
    )

    assert response.status_code == 201
    data = response.json()
    assert data["title"] == "Integration Test Task"
    assert data["description"] == "Integration test description"
    assert data["completed"] is False
    assert data["user_id"] == user_id
    assert "id" in data
    assert "created_at" in data
    assert "updated_at" in data


def test_get_tasks_integration(client: TestClient):
    """
    Integration test for getting all tasks for a user via the API.
    """
    user_id = "test_user_123"

    # Create a task first
    client.post(
        f"/api/{user_id}/tasks",
        json={
            "title": "Get Tasks Test",
            "description": "Get tasks test description",
            "completed": False,
            "user_id": user_id
        }
    )

    response = client.get(f"/api/{user_id}/tasks")

    assert response.status_code == 200
    data = response.json()
    assert len(data) >= 1
    task_found = False
    for task in data:
        if task["title"] == "Get Tasks Test":
            task_found = True
            assert task["user_id"] == user_id
            break
    assert task_found, "Expected task not found in response"


def test_get_specific_task_integration(client: TestClient):
    """
    Integration test for getting a specific task via the API.
    """
    user_id = "test_user_123"

    # Create a task first
    create_response = client.post(
        f"/api/{user_id}/tasks",
        json={
            "title": "Specific Task Test",
            "description": "Specific task test description",
            "completed": False,
            "user_id": user_id
        }
    )

    assert create_response.status_code == 201
    created_task = create_response.json()
    task_id = created_task["id"]

    response = client.get(f"/api/{user_id}/tasks/{task_id}")

    assert response.status_code == 200
    data = response.json()
    assert data["id"] == task_id
    assert data["title"] == "Specific Task Test"
    assert data["user_id"] == user_id


def test_update_task_integration(client: TestClient):
    """
    Integration test for updating a task via the API.
    """
    user_id = "test_user_123"

    # Create a task first
    create_response = client.post(
        f"/api/{user_id}/tasks",
        json={
            "title": "Original Task",
            "description": "Original description",
            "completed": False,
            "user_id": user_id
        }
    )

    assert create_response.status_code == 201
    created_task = create_response.json()
    task_id = created_task["id"]

    # Update the task
    response = client.put(
        f"/api/{user_id}/tasks/{task_id}",
        json={
            "title": "Updated Task",
            "description": "Updated description",
            "completed": True
        }
    )

    assert response.status_code == 200
    data = response.json()
    assert data["id"] == task_id
    assert data["title"] == "Updated Task"
    assert data["description"] == "Updated description"
    assert data["completed"] is True


def test_delete_task_integration(client: TestClient):
    """
    Integration test for deleting a task via the API.
    """
    user_id = "test_user_123"

    # Create a task first
    create_response = client.post(
        f"/api/{user_id}/tasks",
        json={
            "title": "Delete Test Task",
            "description": "Delete test description",
            "completed": False,
            "user_id": user_id
        }
    )

    assert create_response.status_code == 201
    created_task = create_response.json()
    task_id = created_task["id"]

    # Verify task exists
    get_response = client.get(f"/api/{user_id}/tasks/{task_id}")
    assert get_response.status_code == 200

    # Delete the task
    response = client.delete(f"/api/{user_id}/tasks/{task_id}")
    assert response.status_code == 200
    assert response.json() == {"message": "Task deleted successfully"}

    # Verify task no longer exists
    get_response_after_delete = client.get(f"/api/{user_id}/tasks/{task_id}")
    assert get_response_after_delete.status_code == 404


def test_toggle_task_completion_integration(client: TestClient):
    """
    Integration test for toggling task completion via the API.
    """
    user_id = "test_user_123"

    # Create a task first
    create_response = client.post(
        f"/api/{user_id}/tasks",
        json={
            "title": "Toggle Completion Test",
            "description": "Toggle completion test description",
            "completed": False,
            "user_id": user_id
        }
    )

    assert create_response.status_code == 201
    created_task = create_response.json()
    task_id = created_task["id"]

    # Verify initial state
    get_response = client.get(f"/api/{user_id}/tasks/{task_id}")
    assert get_response.status_code == 200
    initial_data = get_response.json()
    assert initial_data["completed"] is False

    # Toggle completion to True
    response = client.patch(
        f"/api/{user_id}/tasks/{task_id}/complete",
        json={"completed": True}
    )

    assert response.status_code == 200
    data = response.json()
    assert data["id"] == task_id
    assert data["completed"] is True

    # Toggle completion back to False
    response2 = client.patch(
        f"/api/{user_id}/tasks/{task_id}/complete",
        json={"completed": False}
    )

    assert response2.status_code == 200
    data2 = response2.json()
    assert data2["id"] == task_id
    assert data2["completed"] is False


def test_user_isolation_integration(client: TestClient):
    """
    Integration test to ensure users can only access their own tasks.
    """
    user1_id = "user1_123"
    user2_id = "user2_456"

    # Create a task for user1
    create_response = client.post(
        f"/api/{user1_id}/tasks",
        json={
            "title": "User1 Task",
            "description": "User1 task description",
            "completed": False,
            "user_id": user1_id
        }
    )

    assert create_response.status_code == 201
    created_task = create_response.json()
    task_id = created_task["id"]

    # Verify user1 can access their own task
    user1_response = client.get(f"/api/{user1_id}/tasks/{task_id}")
    assert user1_response.status_code == 200

    # Verify user2 cannot access user1's task
    user2_response = client.get(f"/api/{user2_id}/tasks/{task_id}")
    assert user2_response.status_code == 404

    # Verify user2 cannot access user1's task list
    user2_list_response = client.get(f"/api/{user2_id}/tasks")
    assert user2_list_response.status_code == 200
    user2_tasks = user2_list_response.json()
    # User2 should not see user1's task in their list
    for task in user2_tasks:
        assert task["id"] != task_id  # Assuming task_id is unique to user1


def test_error_handling_invalid_input(client: TestClient):
    """
    Integration test for error handling with invalid input.
    """
    user_id = "test_user_123"

    # Try to create a task with an empty title (should fail validation)
    response = client.post(
        f"/api/{user_id}/tasks",
        json={
            "title": "",  # Empty title should fail validation
            "description": "Invalid input test",
            "completed": False,
            "user_id": user_id
        }
    )

    assert response.status_code == 422  # Unprocessable Entity for validation error


def test_get_nonexistent_task(client: TestClient):
    """
    Integration test for attempting to get a nonexistent task.
    """
    user_id = "test_user_123"
    nonexistent_task_id = 999999  # Very high ID unlikely to exist

    response = client.get(f"/api/{user_id}/tasks/{nonexistent_task_id}")

    assert response.status_code == 404
    assert "detail" in response.json()


def test_update_nonexistent_task(client: TestClient):
    """
    Integration test for attempting to update a nonexistent task.
    """
    user_id = "test_user_123"
    nonexistent_task_id = 999999  # Very high ID unlikely to exist

    response = client.put(
        f"/api/{user_id}/tasks/{nonexistent_task_id}",
        json={
            "title": "Updated Task",
            "description": "Updated description",
            "completed": True
        }
    )

    assert response.status_code == 404
    assert "detail" in response.json()


def test_delete_nonexistent_task(client: TestClient):
    """
    Integration test for attempting to delete a nonexistent task.
    """
    user_id = "test_user_123"
    nonexistent_task_id = 999999  # Very high ID unlikely to exist

    response = client.delete(f"/api/{user_id}/tasks/{nonexistent_task_id}")

    assert response.status_code == 404
    assert "detail" in response.json()