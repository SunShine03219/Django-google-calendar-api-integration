#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys


#
#
# Code added to print the root of the project when lauchning the application
#


# get the path of the current file
current_file = os.path.abspath(__file__)

# get the parent directory of the current file
parent_dir = os.path.dirname(current_file)

# continue getting parent directories until we find the one with the settings file
while not os.path.exists(os.path.join(parent_dir, 'settings.py')):
    parent_dir = os.path.dirname(parent_dir)
    if parent_dir == os.path.dirname(parent_dir):
        # We have reached the root directory and didn't find the settings file
        break

# print the root directory
print("Root directory:", parent_dir)
    
#
#
# Code added to print the root of the project when lauchning the application
#


def main():
    """Run administrative tasks."""
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ProjectGo.settings')
    
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(sys.argv)


if __name__ == '__main__':
    main()


