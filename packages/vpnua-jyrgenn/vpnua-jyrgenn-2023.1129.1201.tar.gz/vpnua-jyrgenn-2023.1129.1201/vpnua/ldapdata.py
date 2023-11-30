#!/bin/echo not directly executable: 

# Functions retrieving, processing, and writing user data from/to LDAP,
# including in particular the nwHasLimes field.

import os
import re
import sys
import json
import time
import ldap3
import datetime

from .basedefs import *


# attributes needed to determine the account's intern/extern status
status_attrs = ["aktivStudent", "employeeType", "aktivSonstig", "employeeNumberFirma"]


class LDAPQueryError(Exception):
    """An exception to be thrown on LDAP connection errors."""

    def __init__(self, message, connection=None):
        self.connection = connection
        self.message = message

    def __str__(self):
        if connection:
            return self.message + ": " + str(self.conn.result)
        return self.message


class LDAPConnection:
    """A class to handle an LDAP connection; we may want to have more than one.

    The immediate example is to open localhost (on netz-limes) for
    reading, kruemel for writing.

    """


    def __init__(self, ldapsrv):
        """Initialise an LDAPConnection using a server entry from the config.

        The server entry is itself a Config object.
        """
        # set the LDAP config attributes on self for convenience
        self.ad = False
        self.__dict__.update(ldapsrv)
        # LDAP attribute names differ between OpenLDAP and the AD
        # LDAP. In general, dealing with this is the user's
        # responsibility, but we use the username attribute
        # ourselves, so let us have a unified interface for that.
        if self.ad:
            self.uid_attr = "sAMAccountName"
        else:
            self.uid_attr = "uid"
        # Now create the actual server connection.
        server = ldap3.Server(self.hostname, port=self.port,
                              use_ssl=self.use_ssl)
        passwd = getsecret(self.secrets_key, config.secrets_filename)
        debug("Credentials:", self.user, passwd)
        self.conn = ldap3.Connection(server,
                                     password=passwd,
                                     user=self.user, auto_bind=True,
                                     read_only=self.read_only,
                                     auto_referrals=False)
        

    def set_limes(self, account, limes_details):
        """Set the Limes details "nwHasLimes" for account.

        `limes_details` is a data structure that contains the
        nwHasLimes data. It is not in any way checked if it makes
        sense, so it better should.

        """
        time.sleep(0.2)         # don't overrun the LDAP server
        
        # It is good form to set the modify date of the nwHasLimes entry.
        now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
        limes_details["modifyDate"] = now

        j_encoded = json.dumps(limes_details, sort_keys=True,
                               separators=(",", ":"))
        entryDN = f"uid={account},{self.base}"
        if self.conn.modify(
                entryDN, {F_NWHASLIMES: [(ldap3.MODIFY_REPLACE, j_encoded)]}):
            debug("modified", account)
            pass
        else:
            raise LDAPQueryError(f"modify {account} failed",
                                 connection=self.conn.result)

    def all_accounts(self):
        """Generator: return all account names."""
        if not self.conn.search(self.base, "(uid=*)", attributes=["uid"]):
            raise LDAPQueryError(f"LDAP query failed", self.conn.result)
        for entry in self.conn.response:
            yield entry["attributes"]["uid"][0]

    def all_accounts_attrs(self, attrs=[]):
        """Generator: return all accounts and selected attributes."""
        attributes = [*attrs, "uid"]
        if not self.conn.search(self.base, "(uid=*)", attributes=attributes):
            raise LDAPQueryError(f"LDAP query failed", self.conn.result)
        for entry in self.conn.response:
            yield entry["attributes"]


    def all_nwhaslimes_accounts(self, *, ext_status=False, more_attrs=[]):
        """Generator: return all account names with an nwHasLimes attribute.

        Return (uid, nwHasLimes, more_attrs) tuples. nwHasLimes is already
        decoded from JSON. The third element is a hash containing the attributes.

        If more_attrs contains "*", all attributes are requested.

        """
        if "*" in more_attrs:
            requested_attrs = ["*"]
            get_all_attrs = True
        else:
            get_all_attrs = False
            requested_attrs = ["uid", F_NWHASLIMES]
            if ext_status:
                requested_attrs = list(set([*requested_attrs, *status_attrs]))
            requested_attrs = list(set([*requested_attrs, *more_attrs]))
        if not self.conn.search(self.base, "(&(uid=*)(nwHasLimes=*))",
                                attributes=requested_attrs):
            raise LDAPQueryError(f"LDAP query failed", self.conn.result)
        for entry in self.conn.response:
            attrs = entry["attributes"]
            yield attrs["uid"][0], json.loads(attrs[F_NWHASLIMES]), attrs


    def all_vpn_active(self, ext_status=True, more_attrs=[]):
        """Generator: return all account names with active VPN access.

        Return (uid, nwHasLimes) tuples. nwHasLimes is already
        decoded from JSON.

        """
        for uid, nwHasLimes, attrs in self.all_nwhaslimes_accounts(ext_status=True,
                                                                   more_attrs=more_attrs):
            if nwHasLimes.get("active"):
                if ext_status:
                    ext = self.account_status_extern(uid, attrs)
                    if more_attrs:
                        yield uid, nwHasLimes, ext, attrs
                    else:
                        yield uid, nwHasLimes, ext
                else:
                    if more_attrs:
                        yield uid, nwHasLimes, attrs
                    else:
                        yield uid, nwHasLimes


    def account_by_name(self, name):
        """Search by person name, i.e. cn and cnnormal.

        Try to normalise the name as found in e.g. the file names of
        VPN application forms and find the result in the directory.
        The result can be ambiguous or empty.

        Return a list of candidates as tuples of
        the form (cn, uid, mainEmail, nwHasLimes) or None.

        """
        normal, parts = normalise_name(name)
        search_term = f"(|(cn=*{name})(cnNormal=*{normal}))"
        debug(f"account by name {name}, normal {normal}, search {search_term}")

        wanted_attrs = ["cn", "uid", F_MAINEMAIL, F_NWHASLIMES]
        success = self.conn.search(self.base, search_term, attributes=wanted_attrs)
        if not success:
            return None
        
        entries = list(self.conn.response)
        result = []                     # tuples (cn, uid, mainEmail, nwHasLimes)
        for entry in entries:
            attrs = entry["attributes"]
            cn = attrs["cn"][0]
            uid = attrs["uid"][0]
            email = attrs[F_MAINEMAIL]
            nwhl_attr = attrs[F_NWHASLIMES]
            nwHasLimes = json.loads(nwhl_attr) if nwhl_attr else None
            debug("Entry:", cn, uid, email, nwHasLimes)
            result.append((cn, uid, email, nwHasLimes))
        return result


    def account_all_attrs(self, uid):
        """Return all attributes of an account."""
        qstring = f"({self.uid_attr}={uid})"
        if not self.conn.search(self.base, qstring, attributes=["*"]):
            raise LDAPQueryError(f"LDAP query failed", self.conn)
        for entry in self.conn.response:
            debug("entry all_attrs", entry)
            return entry["attributes"]

            
    def account_attrs(self, uid, *attrs):
        """Get the specified attributes for the account `uid`."""
        debug("filter =", f"({self.uid_attr}={uid})")
        if not self.conn.search(self.base, f"({self.uid_attr}={uid})",
                                attributes=attrs):
            debug(f"LDAP query: nothing for '{uid}'")
            return None
        debug("response:", self.conn.response)
        debug("len resp:", len(self.conn.response))
        return self.conn.response[0]["attributes"]

    def account_exists(self, uid):
        """Return true iff the account with the specified uid exists."""
        result = self.account_attrs(uid, "uid")
        debug("check account_exists:", uid, "result:", result)
        return result

    def get_nwHasLimes(self, uid):
        """Get the nwHasLimes attribute for the account with uid.

        Return the decoded data structure or None.
        """
        attributes = self.account_attrs(uid, F_NWHASLIMES)
        nwHasLimes = attributes[F_NWHASLIMES]
        if nwHasLimes:
            return json.loads(nwHasLimes)
        else:
            return None

    def find_entries(self, filter, attrs):
        """Find LDAP entries for `filter`, return attributes.

        filter must be an LDAP filter expression.

        """
        self.conn.search(self.base, filter, attributes=attrs)
        for entry in self.conn.response:
            yield entry["attributes"]

    def account_status_extern(self, account, attrs=None):
        """Return False for all internal accounts, the status for others."""
        if attrs is None:
            attrs = self.account_all_attrs(account)
        status = account_status(attrs)
        status_l = status.lower()
        for tag in ("student", "angestellt", "beamtet", "cfm", "praktikant",
                    "azubi", "stipendiat"):
            if tag in status_l:
                return False
        return status

    def has_zone7_access(self, uid):
        """Return True iff uid has access to Zone7 file shares."""
        assert self.ad, "must use an AD ldap connection"
        ad_attrs = self.account_attrs(uid, "memberOf")
        if ad_attrs:
            groups = ad_attrs["memberOf"]
            for group in groups:
                if group.startswith(zone7_group_start):
                    return True
        return False


def account_status(attrs):
    """Return some sensible description of the person's status.

    Unfortunately, this has to be concluded from several attributes of the
    person's record.

    """
    st_map = {
        "Studentische Hilfskraft": "StudHK",
    }
    status = []

    astud = attrs.get("aktivStudent")
    if astud and astud[0] == "Y":
        status.append("Student*in")
    employeetype = attrs.get("employeeType")
    #debug("employeetype is", employeetype)
    for employee in (employeetype or []):
        status.append(st_map.get(employee) or employee)
    sonstige = attrs.get("aktivSonstig")
    if sonstige:
        status.append("Extern")
    firma_emp = attrs.get("employeeNumberFirma")
    if firma_emp:
        status.append(firma_emp[0].split(".")[0])
    return ",".join(status)
    

def get_rule_enddate(data, rulename):
    """Return a specific rule endDate from the nwHasLimes data, or None."""
    if not data:
        return None
    rules = data.get(F_RULES)
    if not rules:
        return None
    rule = rules.get(rulename)
    if not rule:
        return None
    enddate = rule.get(F_ENDDATE)
    return enddate                      # may still be None, in theory


def has_permission(data, rulename):
    """Return True iff nwHasLimes data contains permission according to rulename."""
    today = datetime.datetime.now().strftime("%Y-%m-%d")
    enddate = get_rule_enddate(data, rulename)
    return enddate and enddate >= today


def set_rule_enddate(data, rulename, enddate):
    """Set a specific rule enddate in the nwHasLimes data.

    Create the dictionaries as necessary on the way.

    """
    if F_RULES not in data:
        data[F_RULES] = {}
    if rulename not in data[F_RULES]:
        data[F_RULES][rulename] = {}
    data[F_RULES][rulename][F_ENDDATE] = enddate


# regexps to match line in rule file
host_svc_re = re.compile("^([a-zA-Z0-9.-]+):([a-zA-Z0-9,]+)")
addr_svc_re = re.compile("^([0-9/.]+):([a-zA-Z0-9,]+)")

C_DOMAIN = ".charite.de"

rulesfile_templ = "/opt/openvpn/rules/special/{uid}-regel"

## TODO: eliminate?
def get_special(uid):
    """Return a string with the special permissions for uid."""
    groups = set()                      # group rules
    hosts = {}                          # host rules, host => [svcs]
    try:
        with open(rulesfile_templ.format(uid=uid)) as spec:
            for line in spec:
                stripped_line = line.strip()
                # skip emtpy lines
                if not stripped_line:
                    continue
                # skip comments (I guess)
                if stripped_line.startswith("#"):
                    continue
                content, *comment = stripped_line.split("#", 1)
                stripped_line = content.strip()
                split_line = stripped_line.split()
                # include line
                if split_line[0].lower() == "include" and len(split_line) == 2:
                    groups.add(split_line[1])
                    continue
                # now finally host:svcs?
                joined_line = "".join(split_line)
                match = host_svc_re.match(joined_line) \
                    or addr_svc_re.match(joined_line)
                if match:
                    host, svcs = match.groups()
                    services = svcs.split(",")
                    if host.endswith(C_DOMAIN):
                        host = host[0:-len(C_DOMAIN)]
                    if host not in hosts:
                        hosts[host] = set()
                    hosts[host] |= set(services)
                else:
                    print(f"get_special({uid}): unrecognised line", line,
                          file=sys.stderr)
    except FileNotFoundError:
        return None
    result = ", ".join([ "Gruppe " + group for group in sorted(groups) ])
    no_comma = not(result)          # need no comma at the start
    for host in sorted(hosts.keys()):
        if not no_comma:
            result += ", "
        no_comma = False
        result += "{host}:{svcs}".format(host=host,
                                         svcs=",".join(hosts[host]))
    return result


def read_account_name(ldapc):
    wanted_attrs = ["cn", "uid", F_MAINEMAIL, F_NWHASLIMES]
    while True:
        account = read_choice("Account: ")
        if not account:
            return None
        entries = ldapc.account_attrs(uid, wanted_attrs)
        for entry in entries:
            attrs = entry["attributes"]
            cn = attrs["cn"][0]
            uid = attrs["uid"][0]
            email = attrs[F_MAINEMAIL]
            nwhl_attr = attrs[F_NWHASLIMES]
            nwHasLimes = json.loads(nwhl_attr) if nwhl_attr else None
            return (cn, uid, email, nwHasLimes)


def choose_account(pretext, candidates, prompt, ldapc, default=None):
    """Choose one of the candidate accounts presented here or None.

    candidates is a list of tuples (cn, uid, email, nwHasLimes); they are
    presented in order with a number, and the user can choose a number. If none
    is chosen (empty answer or the like), return None.
    """
    if not candidates:
        return None
    if len(candidates) == 1:
        return candidates[0]
    tprint(pretext)
    tprint()
    for index, entry in enumerate(candidates, 1):
        cn, uid, email, _ = entry
        tprint(f"   {index:2}) {uid:8} {cn} <{email}>")
    tprint()
    n = read_num_choice(prompt)
    if n is None:
        tprint("keiner ausgewählt\n")
        return read_account_name(ldapc)
    if 1 <= n <= len(candidates):
        return candidates[n-1]
    tprint("ungültig")
    return False


# EOF
