# Backend README

# Web Sales System Backend

This is the backend component of the Web Sales System project, built using FastAPI and SQLAlchemy with SQLite as the database.

## Project Structure

- `app/`: Contains the main application code.
  - `main.py`: Entry point of the FastAPI application.
  - `models.py`: SQLAlchemy models for the database.
  - `schemas.py`: Pydantic schemas for request and response validation.
  - `crud.py`: CRUD operations for Product and Order entities.
  - `database.py`: Database connection and session management.
  - `routers/`: Contains the API routers.
    - `sales.py`: RESTful API endpoints for managing products and orders.
- `requirements.txt`: Lists the dependencies required for the backend.

## Setup Instructions

1. **Clone the repository:**
   ```
   git clone <repository-url>
   cd web-sales-system/backend
   ```

2. **Create a virtual environment:**
   ```
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```

3. **Install the required packages:**
   ```
   pip install -r requirements.txt
   ```

4. **Run the application:**
   ```
   uvicorn app.main:app --reload
   ```

## API Usage

The backend provides a RESTful API for managing products and orders. Below are the available endpoints:

### Products

- `GET /products`: Retrieve a list of products.
- `POST /products`: Create a new product.
- `GET /products/{id}`: Retrieve a product by ID.
- `PUT /products/{id}`: Update a product by ID.
- `DELETE /products/{id}`: Delete a product by ID.

### Orders

- `GET /orders`: Retrieve a list of orders.
- `POST /orders`: Create a new order.
- `GET /orders/{id}`: Retrieve an order by ID.
- `PUT /orders/{id}`: Update an order by ID.
- `DELETE /orders/{id}`: Delete an order by ID.

## License

This project is licensed under the MIT License. See the LICENSE file for more details.