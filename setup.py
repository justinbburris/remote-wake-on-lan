from setuptools import setup, find_packages

setup(
    name="remote-wake-on-lan",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "fastapi==0.109.2",
        "uvicorn==0.27.1",
        "wakeonlan==3.0.0",
        "python-dotenv==1.0.1",
    ],
    extras_require={
        "dev": [
            "pytest==8.0.0",
            "pytest-cov==4.1.0",
            "httpx==0.26.0",
        ],
    },
)
