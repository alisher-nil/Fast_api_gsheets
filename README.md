
![Static Badge](https://img.shields.io/badge/python-1c4161?logo=python&logoColor=3776AB)
![Static Badge](https://img.shields.io/badge/FastAPI-005571?logo=fastapi)
![Static Badge](https://img.shields.io/badge/SQLAlchemy-ed745f?logo=sqlalchemy&logoColor=D71F00)
![Static Badge](https://img.shields.io/badge/pydantic-8a123a?logo=pydantic&logoColor=E92063)
![Static Badge](https://img.shields.io/badge/pytest-0a597a?logo=pytest&logoColor=0A9EDC)

# QRkot_spreadseets
# About

This project is a backend for a charity fund written in Python using the FastAPI framework.
It provides an API for managing users, maintaining charity projects and donations.
It's mostly the same as [charity fund project](https://github.com/alisher-nil/cat_charity_fund) but adds an endpoint to create a report in google sheets using google API.


## Table of Contents
- [Installation](#installation)
- [Usage](#usage)
- [Author](#author)
- [API](#api)

## Installation
1. Clone the repository

```bash
git clone https://github.com/alisher-nil/cat_charity_fund.git
```

2. Navigate to the project directory:

```bash
cd cat_charity_fund
```

3. Create a virtual environment:

```bash
python3 -m venv venv
```
4. Activate the virtual environment:
* Linux/macOS

    ```bash
    source venv/bin/activate
    ```

* Windows

    ```bash
    source venv/scripts/activate
    ```

5. Upgrade PIP and install required dependencies:

```bash
python3 -m pip install --upgrade pip
pip install -r requirements.txt
```

6. Adjust environment variables in `.env` file.

Example provided in `.env.example`

## Usage
To run the project use the following command from the project's root directory:
```bash
uvicorn app.main:app --reload
```
By default the project will be available at `localhost:8000/`

## API
API documentation can be found at [localhost:8000/docs/](localhost:8000/docs/) for Swagger and [localhost:8000/redoc/](localhost:8000/redoc/) for Redoc.

### Users
Users are implemented with bearer transport and JWT strategy.

## Author
Please feel free to contact me with any questions or feedback:

- Email: alisher.nil@gmail.com
- GitHub: [alisher-nil](https://github.com/alisher-nil/)
