"""
The State Library: SaltStack state documentor module.
"""
import logging
import os
import re

import salt.fileclient
import salt.utils.state

__virtualname__ = "tsl"

"""
_infotype_ contains the possible doc values, with a boolean 'required' flag
"""
_infotype_ = {
    "Author": True,
    "Description": True,
    "Syntax": True,
    "Pillars": False,
    "Grains": False,
}

__func_alias__ = {"list_": "list"}

log = logging.getLogger(__name__)


def __virtual__():
    return __virtualname__


def hello():
    """
    Check that the TSL is working.

    CLI Example:

    .. code-block:: bash

    salt '*' tsl.hello
    """
    return "Hi"


def _parse(state, saltenv=None):
    """
    Parse the document section of a state file.
    """
    filename = _path(state, saltenv=saltenv)
    if filename and __salt__["file.file_exists"](filename):
        content = __salt__["file.read"](filename)

        # Search for pillar
        finds = re.finditer(
            r"(pillar\[['\"]|salt\[['\"]pillar\.get['\"]\]\(['\"])(?P<pi>.+?)(['\"]\]|['\"]\))",
            content,
        )
        plist = sorted(list({f.group("pi") for f in finds}))

        # Search for grains
        finds = re.finditer(
            r"(grains\[['\"]|salt\[['\"]grains\.get['\"]\]\(['\"])(?P<gr>.+?)(['\"]\]|['\"]\))",
            content,
        )
        glist = sorted(list({f.group("gr") for f in finds}))

        # Search for include
        ilist = []
        included = False
        for line in content.splitlines():
            # Process file after include found
            if included:
                expr = re.match(r"^\s*-(.*)", line)
                if expr:
                    istate = expr.expand(r"\1").strip()
                    ilist.append(istate)
                else:
                    # End of includes
                    break
            else:
                # Process file to find include
                expr = re.match("include:", line)
                if expr:
                    included = True
        ilist = list(set(ilist))

        tsl = {}
        tsl["State_name"] = state
        tsl["File_name"] = filename
        if len(plist) > 0:
            tsl["Pillars"] = plist
        if len(glist) > 0:
            tsl["Grains"] = glist
        if len(ilist) > 0:
            tsl["Includes"] = ilist

        docs_section = re.findall("#START-DOC(.*?)#END-DOC", content, re.S)
        if docs_section:
            docs = docs_section[0].splitlines()
            exists, errors = [], []
            for line in docs:
                docval = re.match(r"#\s*([0-9a-zA-Z_]+):\s*(.*)", line)
                if docval:
                    name = docval.expand(r"\1")
                    value = docval.expand(r"\2")
                    # Check if this info is known to us
                    if name in _infotype_:
                        # Check duplicate info
                        if name in exists:
                            errors.append(
                                "Duplicated info: " + name + docval.expand(r" (\2)"),
                            )
                            continue
                        if name == "Pillars":
                            plist = sorted(list({v.strip() for v in value.split(",")}))
                            if name in tsl:
                                tsl[name] = sorted(list(set(tsl[name] + plist)))
                            else:
                                tsl[name] = plist
                        elif name == "Grains":
                            glist = sorted(list({v.strip() for v in value.split(",")}))
                            if name in tsl:
                                tsl[name] = sorted(list(set(tsl[name] + glist)))
                            else:
                                tsl[name] = glist
                        else:
                            tsl[name] = value
                        exists.append(name)
                    else:
                        errors.append(docval.expand(r"Unknown info: \1 "))
            # Look for missing info
            for typ, req in _infotype_.items():
                if req and typ not in exists:
                    errors.append("Missing info: " + typ)
            if errors:
                tsl["Errors"] = errors
        return True, tsl
    else:
        return False, "State does not exist on this minion."


def _format_doc(tsl):
    """
    Format the doc info section.
    """
    retval = {}
    retval["Doc Info"] = os.linesep.join(
        [
            f"{k}: {v}"
            if not isinstance(v, list)
            else os.linesep.join(["%s:" % k] + ["\t%s" % v_ for v_ in v])
            for k, v in tsl.copy().items()
            if k != "Errors"
        ]
    )
    if "Errors" in tsl:
        retval["Errors"] = tsl["Errors"]
    return retval


def _path(state, saltenv=None):
    """
    Return the cached .sls file path of the state.
    """
    saltenv = saltenv or __opts__.get("saltenv") or "base"
    opts = salt.utils.state.get_sls_opts(__opts__, saltenv=saltenv)

    with salt.fileclient.get_file_client(opts) as client:
        info = client.get_state(state, saltenv)
    # st_ = salt.state.HighState(opts)
    # info = st_.client.get_state(state, saltenv)

    if "dest" in info:
        path = info["dest"]
        return path
    else:
        return False


def doc(state, saltenv=None):
    """
    Show the document section of a state.

    CLI Example:

    .. code-block:: bash

    salt '*' tsl.doc state
    """
    status, ret = _parse(state, saltenv=saltenv)
    return _format_doc(ret) if status else ret


def list_(saltenv=None):
    """
    Show the document section state files recursively for a minion.

    saltenv
        Salt fileserver environment

    CLI Example:

    .. code-block:: bash

    salt 'minion' tsl.list
    salt 'minion' tsl.list saltenv=dev
    """

    saltenv = saltenv or __opts__.get("saltenv")
    opts = salt.utils.state.get_sls_opts(__opts__, saltenv=saltenv)
    st_ = salt.state.HighState(opts)
    states = st_.compile_state_usage()

    tsl = {"Unused states": {}, "Used in Highstate": {}}
    for env, data in states.items():
        used = data["used"]
        unused = data["unused"]
        try:
            used.remove("top")
        except ValueError:
            pass
        try:
            unused.remove("top")
        except ValueError:
            pass
        if unused:
            tsl["Unused states"][env] = unused
        if used:
            tsl["Used in Highstate"][env] = used

    return tsl


def list_simple(saltenv=None):
    """
    Show used and unused state files for a minion.

    saltenv
        Salt fileserver environment

    CLI Example:

    .. code-block:: bash

    salt 'minion' tsl.list
    salt 'minion' tsl.list saltenv=dev
    """

    saltenv = saltenv or __opts__.get("saltenv")
    opts = salt.utils.state.get_sls_opts(__opts__, saltenv=saltenv)
    st_ = salt.state.HighState(opts)
    states = st_.compile_state_usage()

    tsl = {}
    for env, data in states.items():
        stl = data["used"] + data["unused"]
        try:
            stl.remove("top")
        except ValueError:
            pass
        tsl[env] = stl

    return tsl


def list_full(saltenv=None):
    """
    Show the document section of states for a minion.

    saltenv
        Salt fileserver environment

    CLI Example:

    .. code-block:: bash

    salt 'minion' tsl.list_full
    salt 'minion' tsl.list_full saltenv=dev
    """

    saltenv = saltenv or __opts__.get("saltenv")
    opts = salt.utils.state.get_sls_opts(__opts__, saltenv=saltenv)
    st_ = salt.state.HighState(opts)
    states = st_.compile_state_usage()

    tsl = {"Doc section": {}, "Unused states": {}, "Used in Highstate": {}}
    for env, data in states.items():
        for state in data["used"]:
            if state == "top":
                continue
            if env not in tsl["Doc section"]:
                tsl["Doc section"][env] = {}
            if env not in tsl["Used in Highstate"]:
                tsl["Used in Highstate"][env] = {}
            status, ret = _parse(state, saltenv=env)
            tsl["Doc section"][env][state] = _format_doc(ret) if status else ret
            tsl["Used in Highstate"][env][state] = {
                "name": state,
                "path": ret["File_name"] if status else None,
            }

        for state in data["unused"]:
            if state == "top":
                continue
            if env not in tsl["Unused states"]:
                tsl["Unused states"][env] = {}
            status, ret = _parse(state, saltenv=env)
            tsl["Unused states"][env][state] = {
                "name": state,
                "path": ret["File_name"] if status else None,
            }

    return tsl


def search(term, saltenv=None):
    """
    Search for term in the document section of states for a minion.

    term
        Search term

    CLI Example:

    .. code-block:: bash

    salt 'minion' tsl.search term
    salt 'minion' tsl.search term saltenv=dev
    """

    # Get the states of minion
    saltenv = saltenv or __opts__.get("saltenv")
    opts = salt.utils.state.get_sls_opts(__opts__, saltenv=saltenv)
    st_ = salt.state.HighState(opts)
    states = st_.compile_state_usage()

    # return ','.join(states)
    tsl = {}
    # Lookup all statefiles
    for env, data in states.items():
        for state in list(set(data["used"] + data["unused"])):
            if state == "top":
                continue
            if state.find(term) != -1:
                if env not in tsl:
                    tsl[env] = {}
                tsl[env][state] = ["Module: " + state]
            # Parse the states' doc section and search for term
            status, doc_ = _parse(state, saltenv=env)
            if status:
                doc_ = _format_doc(doc_)
                doc_info = doc_.get("Doc Info", "")
                for info in doc_info.splitlines():
                    if info.find(term) != -1:
                        if env not in tsl:
                            tsl[env] = {}
                        if state not in tsl[env]:
                            tsl[env][state] = []
                        tsl[env][state].append(info)

    return tsl


def pillars(state, saltenv=None):
    """
    List of used pillars in a state for a minion.

    state
        State name

    saltenv
        Salt fileserver environment from which to retrieve the file

    CLI Example:

    .. code-block:: bash

    salt 'minion' tsl.pillars state
    salt 'minion' tsl.pillars state saltenv=dev
    """
    saltenv = saltenv or "base"
    status, ret = _parse(state, saltenv=saltenv)
    return ret.get("Pillars", []) if status else ret


def grains(state, saltenv=None):
    """
    List of used grains in a state for a minion.

    state
        State name

    saltenv
        Salt fileserver environment from which to retrieve the file

    CLI Example:

    .. code-block:: bash

    salt 'minion' tsl.grains state
    salt 'minion' tsl.grains state saltenv=dev
    """

    saltenv = saltenv or "base"
    status, ret = _parse(state, saltenv=saltenv)
    return ret.get("Grains", []) if status else ret


def includes(state, saltenv=None):
    """
    List of included state files for a minion.

    state
        State name

    saltenv
        Salt fileserver environment from which to retrieve the file

    CLI Example:

    .. code-block:: bash

    salt 'minion' tsl.includes state
    salt 'minion' tsl.includes state saltenv=dev
    """

    saltenv = saltenv or "base"
    status, ret = _parse(state, saltenv=saltenv)
    return ret.get("Includes", []) if status else ret
