from setuptools import setup, find_packages

setup(
    name='tympy',
    version='0.0.13',
    packages=find_packages(include=["tympy*"]),
    description='A Python library for observing output and execution times of scripts.',
    author='Nidal Iguer',
    author_email='hello@inidal.dev',
    url='https://github.com/inidal/tympy',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
    ],
    python_requires='>=3.6',
)
