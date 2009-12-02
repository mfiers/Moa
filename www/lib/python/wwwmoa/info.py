### WWWMoa ###############################
### Info / Basic Information About WWWMoa
### Version: 0.1
### Date: November 16, 2009

## Returns a string representing the name of WWWMoa and its current version.
def get_string():
    return get_name() + " " + get_version_string()

## Returns a string representing the name of WWWMoa.
def get_name():
    return "WWWMoa"

## Returns a string representing the version of WWWMoa.
def get_version_string():
    return str(get_version_major()) + "." + str(get_version_minor())

## Returns the major component of the version of WWWMoa.
def get_version_major():
    return 0

## Returns the minor component of the version of WWWMoa.
def get_version_minor():
    return 1
