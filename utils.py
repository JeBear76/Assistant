
def prettyDict(d, indent=0):
    for key, value in d.items():
      print('  ' * indent + str(key))
      if isinstance(value, dict):
         prettyDict(value, indent+1)
      else:
         print('  ' * (indent+1) + str(value))
    print('\n')