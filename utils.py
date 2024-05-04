
def prettyDict(d, indent=0):
    """
    Prints a dictionary in a pretty format with indentation.

    Args:
        d (dict): The dictionary to be printed.
        indent (int, optional): The number of spaces to indent each level. Defaults to 0.
    """
    for key, value in d.items():
        print('  ' * indent + str(key))
        if isinstance(value, dict):
            prettyDict(value, indent+1)
        else:
            print('  ' * (indent+1) + str(value))
    print('\n')