"""Product Service - Integration Tests - Following STRICT TDD"""

# isort: skip_file

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from fastapi.testclient import TestClient
from src.main import app


def test_health_check_returns_200():
    """Test 1: Health check endpoint returns 200"""
    client = TestClient(app)
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == {"status": "healthy"}


def test_get_product_by_id_found():
    """Test 2: GET /product/{id} returns product with ETag header"""
    client = TestClient(app)

    # In Spring example, they mock a product with ID 1
    # For now, we'll test that endpoint exists and returns proper structure
    response = client.get("/product/1")

    assert response.status_code == 200
    assert response.headers.get("ETag") == '"1"'
    assert response.headers.get("Location") == "/product/1"

    data = response.json()
    assert data["id"] == 1
    assert data["name"] == "Product Name"
    assert data["quantity"] == 10
    assert data["version"] == 1


def test_get_product_by_id_not_found():
    """Test 3: GET /product/{id} returns 404 for non-existent product"""
    client = TestClient(app)

    response = client.get("/product/999")

    assert response.status_code == 404


def test_create_product():
    """Test 4: POST /product creates new product with version 1"""
    client = TestClient(app)

    product_data = {"name": "New Product", "quantity": 25}

    response = client.post("/product", json=product_data)

    assert response.status_code == 201
    assert response.headers.get("ETag") == '"1"'

    data = response.json()
    assert data["name"] == "New Product"
    assert data["quantity"] == 25
    assert data["version"] == 1
    assert "id" in data
    assert data["id"] is not None

    # Location header should point to created resource
    assert response.headers.get("Location") == f"/product/{data['id']}"


def test_update_product_with_version():
    """Test 5: PUT /product/{id} updates product and increments version"""
    client = TestClient(app)

    # First create a product to update
    product_data = {"name": "Test Product", "quantity": 10}
    create_response = client.post("/product", json=product_data)
    created_product = create_response.json()
    product_id = created_product["id"]

    # Update the product with version header (If-Match)
    update_data = {"name": "Updated Product", "quantity": 20}
    response = client.put(
        f"/product/{product_id}", json=update_data, headers={"If-Match": "1"}
    )

    assert response.status_code == 200
    assert response.headers.get("ETag") == '"2"'  # Version should increment
    assert response.headers.get("Location") == f"/product/{product_id}"

    data = response.json()
    assert data["id"] == product_id
    assert data["name"] == "Updated Product"
    assert data["quantity"] == 20
    assert data["version"] == 2  # Version incremented from 1 to 2


def test_delete_product():
    """Test 6: DELETE /product/{id} removes product successfully"""
    client = TestClient(app)

    # First create a product to delete
    product_data = {"name": "Product to Delete", "quantity": 5}
    create_response = client.post("/product", json=product_data)
    product_id = create_response.json()["id"]

    # Delete the product
    response = client.delete(f"/product/{product_id}")

    assert response.status_code == 200

    # Verify it's actually deleted
    get_response = client.get(f"/product/{product_id}")
    assert get_response.status_code == 404


def test_update_product_version_conflict():
    """Test 7: PUT /product/{id} returns 409 on version mismatch"""
    client = TestClient(app)

    # First create a product
    product_data = {"name": "Original Product", "quantity": 10}
    create_response = client.post("/product", json=product_data)
    product_id = create_response.json()["id"]

    # Try to update with wrong version (should be 1, we send 2)
    update_data = {"name": "Updated Product", "quantity": 20}
    response = client.put(
        f"/product/{product_id}",
        json=update_data,
        headers={"If-Match": "2"},  # Wrong version!
    )

    assert response.status_code == 409  # Conflict


def test_update_product_not_found():
    """Test 8: PUT /product/{id} returns 404 for non-existent product"""
    client = TestClient(app)

    update_data = {"name": "Updated Product", "quantity": 20}
    response = client.put("/product/9999", json=update_data, headers={"If-Match": "1"})

    assert response.status_code == 404


def test_delete_product_not_found():
    """Test 9: DELETE /product/{id} returns 404 for non-existent product"""
    client = TestClient(app)

    response = client.delete("/product/9999")

    assert response.status_code == 404
