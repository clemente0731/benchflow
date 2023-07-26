from setuptools import setup, find_packages


setup(
    name='benchflow',
    version='1.0.0',
    packages=find_packages(exclude=["tests"]),
    package_data={'benchflow': ['configs/*.csv']},
    include_package_data=True,
    install_requires=[
        # Add any required dependencies here
    ],
    entry_points={
        'console_scripts': [
            'benchflow = benchflow:run_benchflow',
        ],
    },
    author='clemente0620',
    author_email='clemente0620@gmail.com',
    description='A platform tool for model benchmark and accuracy validation',
    long_description='A platform tool for model benchmark and accuracy validation, providing performance evaluation and model comparison',
    url='https://www.ikun.com/benchflow',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
)