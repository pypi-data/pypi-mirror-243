# Utility functions not concerned with user data in LDAP, Limes, AD, or Redis.

import os
import re
import sys
import datetime
import unicodedata
from contextlib import contextmanager

Debug = False

def debug(*args):
    """Print debug output if the `Debug` variable is set to true."""
    if Debug:
        print("DBG", *list(map(str, args)), file=sys.stderr)


def check_date_soft(arg):
    """Match an ISO 8601 date string and return a date object (or false on fail).

    In contrast to the other check_date() function below, the program is not
    terminated when the check fails.

    """
    match = re.match("^(\d\d\d\d)-(\d\d)-(\d\d)$", arg)
    if match:
        try:
            year_s, month_s, day_s = match.group(1, 2, 3)
            date = datetime.date(int(year_s), int(month_s), int(day_s))
            return True
        except Exception as e:
            pass
    return False


def str2int(s):
    """Return integer if string is int-valued, else None."""
    try:
        return int(s)
    except:
        return None


def dn_field(dn, fieldname, mult_as_list=False):
    """Return field(s) named `fieldname` from an LDAP `dn` string.

    If there are multiple fields of that name, return them as a comma-separated
    string (for easier printing), or as a list if `mult_as_list` is true.

    """
    fieldname_l = fieldname.lower()
    result = []
    for field in dn.split(","):
        try:
            name, value = field.split("=")
            if name.lower() == fieldname_l:
                result.append(value)
        except Exception as e:
            raise ValueError(f"cannot split {repr(dn)}, {' '.join(e.args)}")
    if mult_as_list:
        return result
    return ",".join(result)


def accounts_from_file(fname, sep=None, ignore_column_header=False):
    """Generator: Read lines from file, use first field as account name.

    If separator `sep` is not None, split the line on it (e.g. for CSV files).
    Otherwise, split on whitespace. Comment lines (/^\s*#/) and empty lines are
    ignored.

    If `ignore_column_header` is true, the first line of the file is assumed to
    be a column header and will be ignored.

    """

    ignore_one_line = ignore_column_header
    if fname == "-":
        fname = "/dev/stdin"
    with open(fname) as f:
        for line in f:
            if ignore_one_line:
                ignore_one_line = False
                continue
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            yield line.split(sep, 1)[0].strip().lower()


def check_date(datestring, label=""):
    """Check a date string of the form YYYY-mm-dd.

    The string must be formatted correctly, and the date must not be
    before the year 2021 or after the year 2099. If the date string
    is not correct, the program is terminated.

    """
    match = re.match("^([0-9][0-9][0-9][0-9])-([0-9][0-9])-([0-9][0-9])$", datestring)
    if label:
        label = f" ({repr(label)})"
    try:
        if not match:
            raise Exception("invalid format")
        year, month, day = match.groups()
        if not ("2021" <= year <= "2099"):
            raise Exception("bad year")
        datetime.datetime(int(year), int(month), int(day))
    except Exception as e:
        sys.exit(f"{sys.argv[0]}: invalid date string '{datestring}'{label}: " + str(e))



def read_choice(prompt, default=None):
    answer = ""
    try:
        tprint(prompt, end="", flush=True)
        answer = input().strip().lower() or default
    except EOFError:
        tprint()
        return None
    return answer


def read_num_choice(prompt, default=None):
    answer = ""
    try:
        tprint(prompt, end="", flush=True)
        answer = input().strip() or default
    except EOFError:
        tprint("*EOF*")
        return None
    try:
        return int(answer)
    except:
        tprint()
        return None


def tprint(*args, **kwargs):
    """Print things to the terminal for user interaction."""
    with open("/dev/tty", "w") as tty:
        print(*args, **kwargs, file=tty)


def getsecret(key, secrets_file):
    """Get a secret tagged with `key` from the secrets file `fname`.

    The file consist of lines of the form `_key_:_value_`, so the key
    may not contain a colon. Whitespace is significant except at the end
    of the line, where it will be stripped, so the secret may not end
    with whitespace. 

    If the key is found, the value is returned. Otherwise, a `KeyError`
    exception is raised.

    """
    with open(secrets_file) as f:
        for line in f:
            tag, *value = line.split(":", 1)
            if value and tag == key:
                return value[0].lstrip(":").rstrip()
    raise KeyError(f"cannot find secret for '{key}' in '{secrets_file}'")


def normalise_name(name):

    """(Try to) normalise a name; replace umlauts etc., remove special chars.

    Return a tuple with the normalised form and a list of the name parts.

    """
    # character replacement map -- replace umlauts and accented characters
    # appropriately; replace some special chars by nothing
    cmap = dict(ä="ae", ö="oe", ü="ue", Ä="ae", Ö="oe", Ü="ue", ß="ss", é="e",
                è="e", á="a", í="i", ó="o", ú="u")
    cmap.update({ " ": "", "-": "", ".": "", "_": "" })

    name = unicodedata.normalize("NFC", name.strip())
    # change "lastname, firstname" to "firstname lastname"
    match = re.search("([^,]+)\\s*,\\s*(.*)", name)
    if match:
        name = (match.group(2) + " " + match.group(1)).strip()

    # remove some special chars, replace umlauts and (some) accented characters
    result = []
    for ch in name:
        new_ch = cmap.get(ch)
        debug(f"ch {ch}, new_ch {new_ch}")
        result.append((ch if new_ch is None else new_ch).lower())
    return "".join(result), name.split()


@contextmanager
def rewriting_file(fpath):
    """This is a context manager for rewriting a possibly existing file.

    To prevent data loss in case of an interruption, the data is
    written to a temporary file in the same directory at first,
    which is then moved to the original file name.

    """
    f = None
    try:
        tempfile = fpath + ".temp"
        f = open(tempfile, "x")
        yield f
    finally:
        if f:
            f.close()
            os.rename(tempfile, fpath)
        
                
# EOF
