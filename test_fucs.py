#!/usr/bin/env python3

email = input("Enter email: ")

def check_email(email):
    try:
        email = email.split('@')
        try:
            domain = email[1].split('.')
        except IndexError:
            return False

        print(len(domain))
        if len(domain) < 2:
            return False

        print(email)
        return True
    except AttributeError as e:
        return False

print(check_email(email))