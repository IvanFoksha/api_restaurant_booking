from setuptools import setup, find_packages

setup(
    name="restaurant-booking",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "fastapi>=0.110.0",
        "uvicorn>=0.27.1",
        "sqlmodel>=0.0.16",
        "pydantic>=2.6.3",
        "pydantic-settings>=2.2.1",
        "python-jose[cryptography]>=3.3.0",
        "passlib[bcrypt]>=1.7.4",
        "python-multipart>=0.0.9",
        "email-validator>=2.1.1",
        "psycopg2-binary>=2.9.9",
        "alembic>=1.13.1",
        "python-dotenv>=1.0.1",
    ],
    extras_require={
        "dev": [
            "pytest>=8.0.2",
            "pytest-cov>=4.1.0",
            "httpx>=0.27.0",
            "black>=24.2.0",
            "isort>=5.13.2",
            "flake8>=7.0.0",
            "mypy>=1.8.0",
            "types-requests>=2.31.0.20240311",
        ],
    },
) 