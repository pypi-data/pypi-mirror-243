# Base definitions for all submodules. This may still get reshuffled a bit.

import os
import sys

from .config import Config
from .utils import *

# field names of attributes, to avoid typos
F_NWHASLIMES = "nwHasLimes"
F_INTRANET = "static-intranet"
F_PROXY = "static-proxy"
F_OFFVDI = "static-officeportal"
F_STDVDI = "static-vdiportal"
F_SPECIAL = "special"
F_RULES = "rules"
F_ENDDATE = "endDate"
F_MAINEMAIL = "mainEmail"
F_DATUMEX = "DatumEx"

# name start of AD groups for Zone7 file share permission
zone7_group_start = "CN=Rolle-Z7-"


# This is a default config meant to be amended/replaced by something
# outside of the codebase.
config = Config(
    # Base URL of the Limes API.
    limesapi_base = "https://netz-limes.charite.de/limes-api",

    # Definition of an LDAP server to use.
    ldap_info = Config(
        hostname = "info.charite.de",
        port = 636,
        use_ssl = True,
        read_only = True,
        base = "cn=Personen,dc=charite.de",
        user = "uid=adminnw,cn=Personen,dc=charite.de",
        secrets_key = "ldap/adminnw",
    ),

    secrets_filename = os.path.join(os.environ.get('HOME'), "etc/secrets")
)

HOME = os.environ.get("HOME")
VPNUACONF = os.environ.get("VPNUACONF")
CONFIGFILE = "vpnua.conf"

# The config file 'vpnua.conf' is always searched for in the current
# directory. If an environment variable VPNUACONF is defined, its
# contents is used as another directory to search for the config.
# After that, the default places "$HOME/etc" and "$HOME/lib/python3"
# are used. See load_config().

config_path = []
if VPNUACONF:
    config_path.append(VPNUACONF)
config_path.extend([
    ".",
    os.path.join(os.path.dirname(__file__), ".."), # i.e. in the same directory
                                                   # as the library
    os.path.join(HOME, "etc"),
    os.path.join(HOME, "lib/python3"),
])

def load_config(pathname=None):
    """Load the VPN User Admin configuration file.

    If no pathname of a configuration file is supplied, load a a configuration
    from the standard list of directories, which is:
      - the current directory
      - a pathname in the environment variable VPNUACONF if present,
      - $HOME/etc/
      - $HOME/lib/python3

    The first vpnua.conf in one of these directories (or the file in
    VPNUACONF, if its value refers directly to a file) is loaded and
    none else. If none is found, a warning is printed to stderr and
    the standard builtin configuration is used. (tbd maybe rather
    throw an exception instead?)

    Return the resulting config.

    """
    if pathname:
        return config.load_from(pathname)
    for elem in config_path:
        if os.path.exists(elem):
            if os.path.isdir(elem):
                elem = os.path.join(elem, CONFIGFILE)
            if os.path.exists(elem):
                config.load_from(elem)
                debug("loaded config from", elem)
                return config
    print(f"vpnua: no config file found in {':'.join(config_path)}"
          + ", using builtin config", file=sys.stderr)
    return config


