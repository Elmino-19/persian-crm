import re
from django.template.defaultfilters import truncatechars

regex = r"^M(?:d|r|s)(?:\.|\s)|^Mrs(?:\.|\s)|^Miss(?:\.|\s)|^PhD(?:\.|\s)|^Dr(?:\.|\s)|^Eng(?:\.|\s)"


def parse_full_name(full_name: str) -> tuple:
    """
    Parses a full name string to extract the first name, middle name, and last name.
    It also handles common name prefixes like Dr., Mr., Mrs., etc.

    This function cleans the input string by removing extra whitespace and line breaks.
    It then identifies and separates a name prefix if one exists.
    The remaining name is split into parts to identify the first, middle, and last names.

    Args:
        full_name (str): The full name string to be parsed.

    Returns:
        tuple: A tuple containing the first name, middle name, and last name.
               If the input is empty, it returns a tuple of empty strings.
    """
    first_name = middle_name = last_name = ''

    if full_name:
        # Remove line breaks and multiple spaces
        full_name = ''.join(full_name.splitlines())
        full_name = re.sub(' +', ' ', full_name)

        # Find and process name prefixes
        prefix = re.findall(regex, full_name, re.IGNORECASE)
        if prefix:
            prefix = prefix[0].rstrip()
            full_name = re.sub(prefix, '', full_name).lstrip()
            prefix = prefix.capitalize()

        # Split the name into parts
        splitted_name = full_name.split(" ")
        splitted_name = list(filter(None, splitted_name))

        # Assign first, middle, and last names
        if len(splitted_name) == 1:
            first_name = splitted_name[0]
        elif len(splitted_name) == 2:
            first_name = splitted_name[0]
            last_name = splitted_name[1]
        else:
            first_name = splitted_name[0]
            middle_name = truncatechars(" ".join(splitted_name[1:-1]), 90)
            last_name = splitted_name[-1]

        # Add the prefix back to the first name
        if prefix:
            first_name = f"{prefix} {first_name}"

    return first_name, middle_name, last_name


def parse_contacts_name(obj) -> None:
    full_name = ' '.join(filter(None, (obj.first_name, obj.middle_name, obj.last_name)))
    obj.first_name, obj.middle_name, obj.last_name = parse_full_name(full_name)
