# The config class, somewhat simplified from the one in jpylib-jyrgenn

class Config:
    """A Config class for configuration variables.

    This is like a dictionary and a namespace combined, so we can get values as
    `config.get("item")` and `config["item"]` and `config.item`, which I find
    most clear and elegant. Supports config files in Python syntax.

    The Config object is initialised with **kwargs, denoting the
    config variables and their values. A loaded config file is run as
    Python code (and so must not contain untrusted contents), and all
    variables defined in its global level are seen as updates to the
    config variables as long as their names do not begin with an
    underscore (_).

    Usage pattern:

        cfg = Config(                             # define default configuration
            threads_max = 10,                     # maximum number of threads
            default_interval = 60,                # check run interval in seconds
        )
        cfg.load_from(config_path)
        ...
        if nthread < cfg.threads_max:
            ...

    The config file is Python code and can look like this:

        # We have plenty of memory, so let's use more threads
        threads_max = 150

        # Also, do it a bit faster
        default_interval = 30

    """
    def __init__(self, **kwargs):
        """Initialize a Config object with the items passed as keyword arguguments."""
        self.__file__ = None            # so far
        self.__dict__.update(kwargs)

    def update(self, new_items):
        """Update the object with a dictionary of new key/value pairs.

        This is similar to the dict.update() method, only keys that start with
        an underscore ("_") are not considered for update.

        """
        for key, value in new_items.items():
            if key.startswith("_"):
                continue
            # We accept unknown variables so we can define some not preconceived
            # data in the config file, e.g. attributes for multiple LDAP servers
            # by their name.
            self.__dict__[key] = value

    def __str__(self):
        """Return a string repr in the form of '<class>(key1=value1, ...)'."""
        return self.__class__.__name__ + "(" + ", ".join(
            ["{}={}".format(k, repr(v)) for k, v in self.__dict__.items()]) \
            + ")"

    def __repr__(self):
        """Return a string repr in the form of '<class>(key1=value1, ...)'."""
        return self.__str__()

    def __getitem__(self, item):
        """Return the item's value from the Config object.

        This is used by the config["item"] syntax.
        """
        return self.__dict__[item]

    def get(self, item, default=None):
        """Return the item's value from the Config object, default if not present."""
        return self.__dict__.get(item, default)

    def items(self):
        """A set-like object providing a view on the Config object's items."""
        return self.__dict__.items()

    def keys(self):
        """A set-like object providing a view on the Config object's top-level keys."""
        return self.__dict__.keys()

    def load_from(self, filename):
        """Read a configuration from `filename` into this Config.

        The file should contain Python code; top-level variables will be
        top-level keys with the respective values in the Config object, except
        those whose name begins with an underscore ("_").

        Return the config object. Raise exception for file open and read errors
        and errors in the config file.

        """
        with open(filename, "r") as f:
            contents = f.read()
        new_locals = {}
        try:
            exec(contents, globals(), new_locals)
        except Exception as e:
            raise type(e)("Error in config file: {}; {}".format(
                filename, e
            ))
        new_locals["__file__"] = filename
        self.update(new_locals)
        return self


