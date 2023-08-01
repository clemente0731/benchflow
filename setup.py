from setuptools import setup, find_packages
import os
import shutil


def move_configs_and_requirements():
    # 删除已经存在的目标目录
    if os.path.exists("benchflow/configs"):
        shutil.rmtree("benchflow/configs")

    if os.path.exists("benchflow/requirements"):
        shutil.rmtree("benchflow/requirements")

    # 移动configs目录到benchflow目录下
    shutil.copytree("configs", "benchflow/configs")
    # 移动requirements目录到benchflow目录下
    shutil.copytree("requirements", "benchflow/requirements")


def clean_pycache():
    for root, dirs, files in os.walk(".", topdown=False):
        for name in files:
            if (
                name.endswith(".pyc")
                or name.endswith(".pyo")
                or name.endswith("__pycache__")
            ):
                os.remove(os.path.join(root, name))
                print(f"Removed pycache file: {os.path.join(root, name)}")
        for name in dirs:
            if name == "__pycache__":
                os.rmdir(os.path.join(root, name))
                print(f"Removed pycache directory: {os.path.join(root, name)}")


def read_requirements(file_path):
    with open(file_path) as f:
        print("benchflow install_requires:", f.read().splitlines())
        return f.read().splitlines()


def pre_setup():
    clean_pycache()
    move_configs_and_requirements()


pre_setup()

setup(
    name="benchflow",
    version="1.0.0",
    packages=find_packages(exclude=["tests"]),
    include_package_data=True,
    package_data={"benchflow": ["configs/*.csv", "requirements/*.txt"]},
    install_requires=read_requirements("./requirements.txt"),
    entry_points={
        "console_scripts": [
            "benchflow = benchflow:run_benchflow",
        ],
    },
    author="clemente0620",
    author_email="clemente0620@gmail.com",
    description="A platform tool for model benchmark and accuracy validation",
    long_description="A platform tool for model benchmark and accuracy validation, providing performance evaluation and model comparison",
    url="https://www.ikun.com/benchflow",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
