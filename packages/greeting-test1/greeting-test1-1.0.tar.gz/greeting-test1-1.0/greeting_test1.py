#!/usr/bin/env python
def greet_user(name):
    greeting = f"嗨, {name}! Hello, {name}!"
    return greeting

# Example usage
if __name__ == "__main__":
    user_name = input("Please enter your name: ")
    print(greet_user(user_name))
