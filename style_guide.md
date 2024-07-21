# Server Coding Style Guide

## Table of Contents
- [Naming Conventions](#naming-conventions)
- [Code Layout](#code-layout)
- [Imports](#imports)
- [Comments](#comments)
- [Functions](#functions)
- [Error Handling](#error-handling)

## Naming Conventions

- **Variables and Function Names**: Use `snake_case` for variable and function names.
    ```python
    def calculate_score():
        user_score = 10
        return user_score
    ```

- **Classes and Models**: Use `CamelCase` for class and model names.
    ```python
    class UserModel:
        pass
    ```

- **Constants and Global Variables**: Use `UPPER_SNAKE_CASE` for constants, global variables, and keys.
    ```python
    API_KEY = "your_api_key"
    ```

## Code Layout

- **Indentation**: Use 4 spaces per indentation level.
    ```python
    def my_function():
        if True:
            print("Hello, World!")
    ```

- **Maximum Line Length**: Limit all lines to a maximum of 79 characters.
    ```python
    # Good
    message = "This is a sample string that is within the 79 character limit."

    # Bad
    message = "This is a sample string that exceeds the 79 character limit which is not recommended."
    ```

- **Blank Lines**: Use 2 blank lines to separate top-level function and class definitions.
    ```python
    class MyClass:
        pass

  
    def my_function():
        pass
    ```

## Imports

- **Import Order**: Follow this order - standard library imports, related third-party imports, local application/library-specific imports.
    ```python
    import os
    import sys

    import requests

    from mymodule import my_function
    ```

- **Importing Specific Modules**: Import only what you need.
    ```python
    # Good
    from mymodule import my_function

    # Bad
    from mymodule import *
    ```

## Comments

- **Inline Comments**: Use inline comments sparingly.
    ```python
    x = x + 1  # Increment x by 1
    ```

- **Block Comments**: Use block comments to explain code that is complex.
    ```python
    # This function does something very complex.
    # It requires multiple steps to achieve its goal.
    def complex_function():
        pass
    ```

- **Docstrings**: Use docstrings for all public modules, functions, classes, and methods.
    ```python
    def my_function():
        """
        This is a sample function.
        """
        pass
    ```

## Functions

- **Function Length**: Keep functions short and focused on a single task.
    ```python
    def short_function():
        pass

    # Bad
    def long_function():
        # many lines of code
        pass
    ```

- **Function Parameters**: Keep the number of function parameters to a minimum.
    ```python
    def function_with_few_params(param1, param2):
        pass
    ```

## Error Handling

- **Using Exceptions Properly**: Use exceptions to handle errors.
    ```python
    try:
        value = my_function()
    except ValueError:
        print("Invalid value")
    ```

- **Handling Exceptions**: Handle exceptions properly.
    ```python
    try:
        value = my_function()
    except ValueError as e:
        print(f"Error: {e}")
    ```


