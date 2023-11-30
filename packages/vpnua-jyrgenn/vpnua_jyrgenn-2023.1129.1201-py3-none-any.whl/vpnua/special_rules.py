#!/usr/bin/env python3

# Dies ist ein Ansatz zum Lesen und Schreiben der VPN-Berechtigungen; in Zukunft
# soll das mal alle Fragen zu den Berechtigungen beantworten können, wie etwa
# "auf was hat eine Person (oder eine Gruppe von Personen) alles (alles!)
# Zugriff?" oder "Wer hat alles Zugriff auf ...?" und ähnliche. Jetzt in die
# vpnua-lib integriert. [jnic 2020-09][jnic 2022-07][jnic 2022-08][jnic 2022-09]

# TODO:
#  - perhaps move the validity checks into the constructors? easy way out with
#    exceptions regardless of nesting depth, and this may give us cleaner code

import os
import re
import sys
import socket

from .basedefs import *
from .utils import *


# where we are looking for rules and services; this can be changed directly for
# testing code, but that will rarely be necessary in production programs
# But beware, it is vpnua.special_rules.openvpndir!
openvpndir = os.environ.get("OPENVPNDIR") or "/opt/openvpn"

# where the special rules are, relative to the openvpndir
specialrulesdir = "rules/special"

# where the groups rules are, relative to the openvpndir
groupsdir = "rules/groups"

# where the service definitions are, relative to the openvpndir
servicesdir = "services"

# Rule file name suffix, f"{uid}{rule_fsuffix}"
rule_fsuffix = "-regel"

# protocols that can be used in rule files and service definitions
known_protocols = ("tcp", "udp")


# match a port number range like "137-139", have two groups for the
# numbers
port_range_re = re.compile("^([0-9]+)-([0-9]+)$")

# known VPN application form types (MCA is M)
vpn_appl_types = "OMLB"               # O, M, Labor, BIH

# cache resolved group rules
known_group_rules = {}          # group_name => Ruleset


def check_proto(proto):
    """Return protocol name iff this is a valid protocol name, else False."""
    if proto in known_protocols:
        return proto
    return False


def check_port(port):
    """Return port string iff string is a valid port number or range, or false."""

    def in_range(port_number):
        """If port_number is in range, return it, else False."""
        if 0 < port_number < 2**16:
            return port_number
        return False

    try:
        port_number = int(port)
        return str(in_range(port_number))
    except:
        pass

    # could be a port range a-b
    match = port_range_re.match(port)
    if match:
        start = int(match.group(1))
        end = int(match.group(2))
        if in_range(start) and in_range(end) and end >= start:
            return f"{start}-{end}"
    return False




class RuleError(Exception):
    """Class for errors that can occur when reading a rule.

    Main feature is that its __str__ methods returns a formatted string in the
    style of the usual compiler error messages with file name and line number.

    """

    def __init__(self, source, lineno, line, message):
        """Create the RuleError with the context from the RuleFactory."""
        self.source = source
        self.lineno = lineno
        self.line = line
        self.message = message

    def __str__(self):
        return "{source}:{lineno}: {message}\n    in line '{line}'".format_map(
            self.__dict__)


class Ruleset:
    """A container for special rules. Will detect and handle duplicates."""

    def __init__(self, rulefile, factory=None):
        """Initialise the Ruleset with a rule file name and maybe a RuleFactory."""
        self.rulefile = rulefile
        self.factory = factory
        self.rules = []           # rules in an array, in order
        self.rules_by_target = {} # rules by target string


    def add_rule_from_string(self, string, handle_comment="append", source=None):
        """Add a rule from a string.

        If the rule is a duplicate of an existing one, add its comment to the
        existing one, unless otherwise directed by handle_comment.

        """
        for rule in self.factory.from_line(string, source=source):
            # may be more than one!
            self.add_rule(rule, handle_comment=handle_comment, source=source)


    def add_rule(self, rule, handle_comment="append", source=""):
        """Add a rule.

        If the rule is a duplicate of an existing one, add its comment to the
        existing one, unless otherwise directed by handle_comment. If it
        "replace" or "append" or update, call the corresponding Rule method.

        """
        if rule.isComment():
            self.rules.append(rule)
        else:
            target = rule.target_str()
            existing_rule = self.rules_by_target.get(target)
            if existing_rule:
                if handle_comment == "replace":
                    existing_rule.replace_comment(rule.comment)
                elif handle_comment == "append":
                    existing_rule.append_comment(rule.comment)
                elif handle_comment == "update":
                    existing_rule.update_comment(rule)
                else:
                    raise ValueError("invalid value of `handle_comment`: "
                                     + repr(handle_comment))
            else:
                self.rules.append(rule)
                self.rules_by_target[target] = rule


    def remove_rule(self, group=None, host=None, servicename=None, port=None, proto=None):
        """Remove a rule by its attributes."""
        raise NotImplementedError("Ruleset.remove_rule() yet tbd") # TODO


    def resolve_rules(self, keep_comments=False, expand_groups_only=False):
        """Return a new ruleset with INCLUDEs and hostnames resolved.

        The underlying rules are not new, rather modified such that the
        hostnames need not be resolved twice. For this to work, it is necessary
        that the original Ruleset was created with read_groups=True.

        Comments (including empty lines) will be preserved if keep_comments is
        true.

        """
        newRS = Ruleset(self.rulefile)
        for rule in self:
            for subrule in resolve_rule(rule, keep_comments=keep_comments,
                                        expand_groups_only=expand_groups_only):
                if subrule:             # may be None on host name resolution fail
                    newRS.add_rule(subrule)
        return newRS


    def __iter__(self):
        """Make the Ruleset iterable."""
        yield from self.rules


class RuleFactory:
    """A class to make Rule instances.

    Keeps track of filename and line number and of the rules seen so
    far; make sure there are no duplicate rules.

    """

    def __init__(self, source, silent=False, read_groups=False, may_not_exist=False):
        """A RuleFactory is initialised with a rule file name and some context.

        The line number is initialised to zero. The specified source (usually a
        rule file) is the default source to read from using read_from_file() and
        to be used in error messages.

        """
        self.groupsdir = os.path.join(openvpndir, groupsdir)
        self.servicesdir = os.path.join(openvpndir, servicesdir)
        self.source = source
        self.silent = silent
        self.read_groups = read_groups
        self.may_not_exist = may_not_exist

        self.lineno = 0
        self.warnings = []
        self.ruleset = Ruleset(source, self)

        
    def read_from_file(self, source=None):
        """Read rules from the specified source or self.source (rule file).

        The source (regardless of self.source or the one passed explicitly) must
        be something that can be open()ed like a file.

        The rules will be added/updated into the existing Ruleset.

        """
        source = source or self.source
        try:
            with open(source) as f:
                for line in f:
                    for rule in self.from_line(line, source=source):
                        # from_line is a generator and may return more than one
                        self.ruleset.add_rule(rule)
        except FileNotFoundError as e:
            if self.may_not_exist:
                pass
            else:
                raise e
        return self.ruleset


    def warn(self, exc):
        """If the RuleFactory is not silent, print a warning from the passed exception.

        Append the warning to self.warnings.

        """
        if not self.silent:
            print("WARN", exc, file=sys.stderr)
        self.warnings.append(exc)


    def check_servicename(self, servicename):
        """Return servicename iff a service with the given name exists, else False."""
        if os.path.exists(os.path.join(self.servicesdir, servicename)):
            return servicename
        return False


    def check_group(self, groupname):
        """Return groupname iff a group rule with the given name exists, else False."""
        if os.path.exists(os.path.join(self.groupsdir, groupname)):
            return groupname
        return False


    def check_network(self, network, prefix):
        """Return true if this is a valid network/prefixlength description.

        Actually, the return value is normalised to four octets and no redundant
        zeros, if valid

        """
        octets = [0, 0, 0, 0]
        prefixlength = 0
        match = re.match(r"^(\d+)(\.(\d+))?(\.(\d+))?(\.(\d+))?$", network)
        if not match:
            return False
        value = match.group(1)              # must exist, otherwise no match
        num = str2int(value)
        if num is None:
            return False                    # must be int
        if not (0 <= num <= 255):
            return False
        octets[0] = num
        for group in (3, 5, 7):
            value = match.group(group)
            if value:                       # need not exist, as in 10/8
                num = str2int(value)        # but if it does, must be int and in range
                if num is None:
                    return False
                elif 0 <= num <= 255:
                    octets[int(group/2)] = num
                else:
                    return False
        num = str2int(prefix)
        if num is None:                     # prefix length must be int
            return False
        if not (8 <= num <= 32):            # must be in range
            return False
        prefixlength = num
        return "{}.{}.{}.{}/{}".format(*octets, prefixlength) # finally


    def check_host_or_net(self, hostname):
        """Return the name iff a host or network with the given name/description exists.

        Actually, the return value is a normalised value for hostname,
        if that is a valid one, i.e. possibly with .charite.de appended
        or a normalised IP address or network range.

        """
        parts = hostname.split("/")
        if len(parts) == 2:
            return self.check_network(*parts)
        elif len(parts) == 1:
            try:
                if "." not in hostname:
                    hostname += ".charite.de"
                # works for quad octets, too
                ipaddr = socket.gethostbyname(hostname)
                if ipaddr:
                    # we only want to see if there is some IP address; we are
                    # not interested in the exact address or how many there are
                    if re.match(r"^\d+.\d+.\d+.\d+$", hostname):
                        # if it already was an IP address (and not a hostname),
                        # return it normalised
                        return ipaddr
                    return hostname     # we know it's legit now
            except socket.gaierror as e:
                return False
        return False


    def rule_error(self, message, source=None):
        """Return a RuleError exception with the context data.

        The context is what we need for the error message, namely file name,
        line number, line content, and error message.

        """
        if source:
            lineno = 0
        else:
            source = self.source
            lineno = self.lineno
        return RuleError(source, lineno, self.line, message)
        

    def host_rule(self, rule, comment, source=None):
        """Generator: return one or more host rules from the rule entry.

        If there are multiple services/ports in the rule, multiple Rule
        objects will be returned.

        """
        parts = rule.split(":")
        if len(parts) == 2:
            host, services = parts
            checked_host = self.check_host_or_net(host)
            if not checked_host:
                raise self.rule_error(f"Hostname oder Netz ungültig {repr(host)}",
                                      source)
            for servicename in services.split(","):
                checked_servicename = self.check_servicename(servicename)
                if not checked_servicename:
                    raise self.rule_error(f"Service {repr(servicename)} unbekannt", source)
                yield HostRule(checked_host, factory=self,
                               service=Service(checked_servicename),
                               comment=comment)
        elif len(parts) == 3:
            host, ports, proto = parts
            checked_host = self.check_host_or_net(host)
            if not checked_host:
                raise self.rule_error(f"Hostname {repr(host)} unbekannt", source)
            checked_proto = check_proto(proto)
            if not checked_proto:
                raise self.rule_error(f"Protokoll {repr(proto)} ungültig", source)
            for port in ports.split(","):
                checked_port_or_range = check_port(port)
                if not checked_port_or_range:
                    raise self.rule_error(f"Port {repr(port)} ungültig", source)
                ep = Endpoint(checked_proto, *checked_port_or_range.split("-"))
                yield HostRule(checked_host, factory=self,
                               service=Service(endpoints=[ep]),
                               comment=comment)
        else:
            raise self.rule_error("ungültige Regel {repr(rule)}", source)

    def group_rule(self, group, comment, source=None):
        """Create a group rule from group name and comment."""
        if not self.check_group(group):
            raise self.rule_error(f"Gruppe {repr(group)} unbekannt", source)
        yield GroupRule(group, factory=self, comment=comment)


    def from_line(self, line, source=None):
        """Generator: create one or more rules from a line in a rule file.

        That line need not necessary come out of a rule file, of
        course, but must comply with rule file syntax. The line may
        contain a host rule or a group rule or a comment or may even
        be empty (which we treat as a comment).

        If that rule is a host rule with more than one port or
        service (as is not uncommon), several rules are created, so
        this must be a generator, even if it will yield only one
        line most of the time.

        `source` denotes the source of that line, if it is different
        from the current source registered, e.g. synthetic from
        the vpn-spezial-... command. Used for the error messages.

        """
        self.lineno += 1
        self.line = line.strip()

        try:
            rule, *maybe_comment = self.line.split("#", 1)
            if len(maybe_comment) == 0:
                comment = None
            else:
                comment = maybe_comment[0].strip()
            rule = rule.strip()
            ruleparts = rule.split()
            if len(ruleparts) == 0: # empty line or comment only
                yield Comment(comment)
            elif len(ruleparts) == 1:
                yield from self.host_rule(ruleparts[0].lower(), comment, source)
            elif len(ruleparts) == 2:
                if ruleparts[0].lower() == "include":
                    yield from self.group_rule(ruleparts[1], comment, source)
                else:
                    raise self.rule_error(
                        f"Unbekanntes Wort {repr(ruleparts[0])}",
                        source)
            else:
                # so, rule consists of more than two parts => invalid
                raise self.rule_error("Ungültige Regen (mehr als zwei Teile)", source)
        except RuleError as e:
            self.warn(e)
            return None
        

class Endpoint:
    """A single endpoint of a service.

    This is one of possibly multiple elements of a service, a combination of a
    port or port range and a protocol. These will have been checked for validity
    before.

    """

    def __init__(self, protocol, start_port, end_port=None):
        """Create a new Endpoint.

        The end_port number may be used together with the start_port to specify
        a port range. The end_port is still in the range. If the end_port is not
        specified or false, the endpoint is a single port, the start_port.

        """
        self.protocol = protocol
        self.start_port = start_port
        self.end_port = end_port

    def __str__(self):
        if self.end_port:
            return f"{self.start_port}-{self.end_port}:{self.protocol}"
        return f"{self.start_port}:{self.protocol}"


class Service:

    """The service that shall be reached at a target system.

    The name may be unspecified for an anonymous service. It better have an
    Endpoint then. It may also have a name and no endpoints, to add endpoints
    later.

    We don't preserve comments and things here, as it is not intended to rewrite
    the service definitions. This data is mainly to expand the service to
    endpoints on resolving the host rules of a Ruleset.

    """

    def __init__(self, name=None, endpoints=[]):
        """Create a new service definition with a name and zero or more endpoints.

        """
        self.name = name
        self.endpoints = endpoints

    def __str__(self):
        if self.name:
            return self.name
        if self.endpoints:
            return str(self.endpoints[0])
        return None

    def add_endpoint(self, endpoint):
        """Add an Endpoint to the service definition."""
        self.endpoints.append(endpoint)

    def __iter__(self):
        yield from self.endpoints


# the service definitions we know so far, as far as they are named and resolved
# (which is when they are put here, so we don't have to resolve them more than
# once)
resolved_services = {}                     # name => Service


class Rule:
    """This is an abstract base class for the group and host rule classes."""

    def __init__(self, *args, **kwargs):
        raise NotImplementedError(self.__class__.__name__ + " is an abstract base class")
    def __hash__(self):
        # to be able to match rule with the same content but different comments
        # (and/or layout), we must have a hash based on a normalised entry
        """The hash method must be implemented to be independent of a comment."""
        raise NotImplementedError()
    def __str__(self):
        raise NotImplementedError()

    def isHostRule(self):
        return False
    def isGroupRule(self):
        return False
    def isComment(self):
        return False

    def lineno(self):
        if self.factory:
            return self.factory.lineno
        else:
            return 0

    def parse_comment(self):
        """Parse recognisable meta information fields pieces from a comment.

        We hope to find:
          - aclass; one of O, M, L, B
          - agent; person who modified the rule
          - modified; when the rule was modified
          - expiry; until when the rule is approved
          - remark(s); 
        Unfortunately, the class (in the form of ';O;') can be anywhere in the
        string. The others are "agent!modified!remarks..." where one of the
        remarks is "Laufzeit bis <date>" and specifies the expiry date.

        All fields not found are None, or in case of remarks, an emtpy string.
        Multiple remarks separated with "!" are cobbled together like this.

        """
        self.aclass = None
        self.agent = None
        self.modified = None
        self.expiry = None
        self.remark = None
        if not self.comment:            # may be None or empty
            return
        comment = self.comment          # we want to modify this in the process
        remarks = []
        # find the aclass 
        match = re.match("^(.*);(.);(.*)$", comment)
        if match:
            comment = match.group(1) + match.group(3)
            aclass = match.group(2)
            if aclass.upper() in vpn_appl_types:
                self.aclass = aclass.upper()
            else:
                self.factory.warn(
                    f"{self.rulefile}:{self.lineno()}: unknown aclass '{aclass}' in comment")
        for i, part in enumerate(comment.split("!")):
            if i == 0:
                self.agent = part
                continue
            if i == 1 and check_date_soft(part):
                self.modified = part
                continue
            if part.lower().startswith("laufzeit bis"):
                lparts = part.split()
                if len(lparts) == 3 and check_date_soft(lparts[2]):
                    self.expiry = lparts[2]
                    continue
            if part:
                remarks.append(part)
        self.remark = "!".join(remarks)


    def replace_comment(self, new_comment):
        """Replace existing comment by a new one.

        If none exists so far, make this the comment.
        """
        self.comment = new_comment
        self.parse_comment()


    def update_comment(self, other):
        """Update the comment metadata with that of another rule.

        We assume the other_rule is newer, so we take updates from there, but
        keep remarks from the original one.

        """
        def concat(str1, str2, sep):
            """If both str1 and str2 are present, concat them with sep.

            Otherwise, return the one that is present or None.
            """
            if str1:
                if str2:
                    return str1 + sep + str2
                return str1
            return str2

        assert isinstance(other, Rule)
        self.aclass = other.aclass or self.aclass
        self.agent = other.agent or self.agent
        self.modified = other.modified or self.modified
        self.expiry = other.expiry or self.expiry
        self.remark = concat(self.remark, other.remark, "!")
        self.comment = concat(self.comment, other.comment, "#")


    def append_comment(self, comment):
        """Append comment to an existing one, separated by a marker.

        If none exists so far, make this the comment.
        """
        if self.comment and comment:
            self.comment = self.comment + " #" + comment
        elif comment:
            self.comment = comment
        self.parse_comment()

    def str_comment(self):
        result = []
        if self.aclass:
            result.append(";")
            result.append(self.aclass)
            result.append(";")
        if self.agent:
            result.append(self.agent)
            result.append("!")
        if self.modified:
            result.append(self.modified)
            result.append("!")
        if self.expiry:
            result.append("Laufzeit bis ")
            result.append(self.expiry)
            result.append("!")
        if self.remark:
            result.append(self.remark)
            result.append("!")
        if result:
            return " #" + "".join(result)
        return ""        


class HostRule(Rule):
    """This is a rule with a host or network and a service and port+protocol."""
    
    def __init__(self, host, *, factory=None, service=None, comment="", in_group=None):
        """Create a new HostRule with the given parameters.

        `service` is a Service object.
        `in_group` is the name of this group definition this was
        found in, or None (the default). The parameter values have
        already been checked by the caller.

        """
        self.factory = factory
        self.rulefile = factory.source if factory else None
        self.host = host
        self.service = service
        self.comment = comment
        self.in_group = in_group        # name of group this was found in, if so
        self.parse_comment()

    def __str__(self):
        return self.target_str() + self.str_comment()

    def target_str(self):
        """Return the target as a string, for checking duplication."""
        if self.service.name:
            return f"{self.host}:{self.service.name}"
        else:
            # an anonymous service will only have one endpoint
            return f"{self.host}:{self.service.endpoints[0]}"

    def isHostRule(self):
        return True


class GroupRule(Rule):
    """This is a Rule that uses a group of permissions via "INCLUDE"."""

    def __init__(self, name, *, factory=None, comment=""):
        self.factory = factory
        self.rulefile = factory.source if factory else None
        self.name = name                # group name is already checked
        self.comment = comment
        if factory and factory.read_groups:
            found = known_group_rules.get(name)
            if found:
                self.ruleset = found
            else:
                ruleset = get_special_rules(
                    os.path.join(factory.groupsdir, self.name),
                    silent=factory.silent,
                    read_groups=factory.read_groups)
                factory.warnings.extend(ruleset.factory.warnings)
                self.ruleset = ruleset
                known_group_rules[name] = ruleset
        else:
            self.ruleset = None
        self.parse_comment()


    def __str__(self):
        return "INCLUDE " + self.name + self.str_comment()

    def target_str(self):
        """Return the target as a string, for checking duplication."""
        return self.name

    def isGroupRule(self):
        return True


class Comment(Rule):
    """This is a pseudo rule for a comment or empty line.

    Obviously this is not a rule in the original sense, but using this I can use
    real rules and empty/comment lines uniformly without distinguishing them
    explicitly.

    """

    def __init__(self, content=""):
        """Initialise a Comment. If the content is unspecified, the line is empty.
        """
        # have these fields so they can be checked like with any other Rule
        self.aclass = None
        self.agent = None
        self.modified = None
        self.expiry = None
        self.remark = None
        self.comment = content

    def __str__(self):
        if self.comment:
            return "# " + self.comment
        return ""

    def target_str(self):
        return None

    def isComment(self):
        return True


def print_rule(rule, subrules=False, prefix=""):
    print(prefix, rule, sep="")
    if isinstance(rule, GroupRule) and subrules and rule.ruleset:
        for subrule in rule.ruleset:
            print_rule(subrule, subrules, prefix + "> ")


def resolve_rule(rule, keep_comments=False, expand_groups_only=False):
    """Resolve an INCLUDE or a hostname in a Rule as appropiate (generator).

    Yield the rule or multiple rules (in case of a Group rule). The yielded
    rule(s) will all be HostRules with resolved IP addresses. The original rules
    will be modified (in memory) such that the IP addresses need not be resolved
    again. If a host rule cannot be resolved, a warning is printed, and None is
    yielded, such that the caller can continue.

    Comments will be preserved only if keep_comments is true.

    """
    def expand_service(resolved_host, service):
        if service.name:
            for endpoint in resolve_service(service.name):
                yield HostRule(resolved_host, service=Service(endpoints=[endpoint]))
        else:
            yield HostRule(resolved_host, service=service)

    if rule.isHostRule():
        if expand_groups_only:
            yield rule
        else:
            try:
                if not keep_comments:
                    rule.comment = ""
                if "/" in rule.host:        # network
                    yield from expand_service(rule.host, rule.service)
                else:                       # host
                    for result in socket.getaddrinfo(rule.host, None,
                                                     family=socket.AF_INET):
                        yield from expand_service(result[4][0], rule.service)
            except Exception as e:
                print("WARN", e)
    elif rule.isGroupRule():
        if rule.ruleset:
            for subrule in rule.ruleset:
                yield from resolve_rule(subrule, keep_comments=keep_comments)
    elif rule.isComment():
        if keep_comments:
            yield rule


def print_rule_metadata(rule):
    """Print the rule metadata from the structured comment."""
    for field in "aclass", "agent", "modified", "expiry", "remark":
        print(f"metadata: {field:7}  {rule.__dict__.get(field)}")


def rulefile_path(uid_or_fname):
    """Return the rulefile pathname.

    If uid_or_fname ends with the rule file suffix or contains a "/", it is
    considered the rule file path name. Otherwise, it is assumed to be a uid,
    and the rule file path name is constructed using the openvpndir.

    """
    if uid_or_fname.endswith(rule_fsuffix) or "/" in uid_or_fname:
        rulefile = uid_or_fname
    else:
        rulefile = os.path.join(openvpndir, specialrulesdir,
                                uid_or_fname + rule_fsuffix)
    return rulefile


def get_special_rules(uid_or_fname, silent=False,
                      read_groups=False, may_not_exist=False):
    """Get special rules from a rule file.

    The parameter `uid_or_fname` is either a uid (account name) or a
    filename; if it contains a "/" or a "-regel" suffix, it will be
    treated as a file name, otherwise as a uid.

    If this is a file name, it will be used directly. If it is a uid, the actual
    file name will be constructed using the openvpndir, the "special/"
    subdirectory, and the "regel" suffix.

    Returned is a Ruleset. It references the RuleFactory as .factory and the
    list of warnings as .factory.warnings. (A warning is a RuleError exception.)

    Iterating over the Ruleset yields the individual rules. The rules can be of
    class HostRule (also for network ranges), GroupRule, or Comment (for
    comment-only or empty lines).

    If `silent` is False (the default), warnings are also printed as
    generated.

    If `read_groups` is true, the group rules are read in and the contained
    rules are stored as the `ruleset` field of the GroupRules. (This is
    recursive, i.e. group rules INCLUDEd in group rules are read in, too.) This
    enables a later call of the Ruleset's `resolve_rules` method to create a
    copy of the Ruleset that contains only host rules, with all GroupRules
    expanded to host rules.

    """
    rulefile = rulefile_path(uid_or_fname)
    return RuleFactory(rulefile,
                       silent=silent,
                       read_groups=read_groups,
                       may_not_exist=may_not_exist,
    ).read_from_file()


def rewrite_special_rules(ruleset, uid_or_fname=None):
    """Write (or re-write) a rule file from a Ruleset.

    With uid_or_fname unspecified, the rule file path name in the Ruleset is
    used.

    If uid_or_fname is a file path name (containing a "/" or ending in
    "-regel"), it is used. Otherwise it is assumed to be a uid, and the rule
    file path name is contructed using openvpndir.

    """
    if uid_or_fname:
        rulefile = rulefile_path(uid_or_fname)
    else:
        rulefile = ruleset.rulefile

    with rewriting_file(rulefile) as rf:
        for rule in ruleset:
            print(rule, file=rf)


def resolve_service(name):
    """Resolve the servicename into endpoints and return a Service object.

    On error, a FileNotFoundError or RuleError exception may be raised.

    """
    if name not in resolved_services:
        svc = read_service_from_file(name)
        resolved_services[name] = svc
    return resolved_services[name]


def read_service_from_file(name_or_filename):
    """Read a service definition and return it as a Service object.

    If name_or_filename contains a "/", it is considered a pathname to the
    service definition file. Otherwise, it is taken as a service name, and the
    definition file is located relative to the openvpndir.

    """
    if "/" in name_or_filename:
        pathname = name_or_filename
        name = os.path.basename(name_or_filename)
    else:
        pathname = os.path.join(openvpndir, servicesdir, name_or_filename)
        name = name_or_filename
    lineno = 0
    svc = Service(name)
    errors = []

    def process_line(line):
        """Process a line. If it contains an endpoint definition, add it."""

        def error(message):
            return RuleError(pathname, lineno, line, message)

        definition = line.split("#", 1)[0].strip()
        if not definition:
            return                      # empty or comment-only line
        ports, *parts = definition.split(":")
        if len(parts) != 1:
            raise error("invalid endpoint definition")
        protocol = parts[0]
        if not check_proto(protocol):
            raise error("unknown protocol")
        for port_or_range in ports.split(","):
            if not check_port(port_or_range):
                raise error("invalid port or port range")
            # finally!
            svc.add_endpoint(Endpoint(protocol, *port_or_range.split("-")))

    with open(pathname) as f:
        for line in f:
            lineno += 1
            process_line(line.strip())
    return svc


# EOF
