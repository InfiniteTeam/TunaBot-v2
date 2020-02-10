def aliases(prefix, aliases):
    names = aliases
    for x in names:
        names[names.index(x)] = prefix+names[names.index(x)]
    return tuple(names)

def arguments(message):
    args = message.split(" ")[1:]
    return args

def color():
    color = {'main':0x5b50fa, 'yellow':0xffbb00, 'red':0xf04747, 'green':0x43b581, 'orange':0xf26522}
    return color