# memo

![Static Badge](https://img.shields.io/badge/python-v3.6%7C3.7%7C3.8%7C3.9%7C3.10%7C3.11%7C3.12-blue)


### Overview
The `memo` decorator is a Python tool designed to optimize function performance by caching the results of function calls. This is particularly useful for computationally expensive functions or functions that access external data frequently. By storing the results of previous function calls, subsequent calls with the same arguments can return the cached result instead of re-executing the function, leading to significant performance improvements.

### Installation
```bash
pip install memocache  
```