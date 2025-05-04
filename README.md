# 🚀 FastAPI + Graphene API

This project is an API built with [FastAPI](https://fastapi.tiangolo.com/) and [Graphene](https://graphene-python.org/), a Python library for building GraphQL APIs.

## 📦 Technologies Used

- **FastAPI** – Modern, high-performance web framework
- **Graphene** – GraphQL framework for Python
- **Uvicorn** – ASGI server for running the app
- **Pydantic** – Data validation
- (optional) **Docker** – For containerization

## 🔧 Getting Started

### 1. Clone the Repository

    git clone https://github.com/your-username/your-repo.git
    cd your-repo

### 2. Create a Virtual Environment and Install Dependencies

    python -m venv venv
    source venv/bin/activate
    pip install -r requirements.txt

### 3. Activate the virtual environment

- On Windows:

        .\venv\Scripts\activate

- On macOS/Linux:

        source venv/bin/activate

### 3. Run the application

    uvicorn app.main:app --reload
