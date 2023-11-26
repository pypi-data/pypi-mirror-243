"""
Partially vendored(including required utility functions) Salt's verify utility module.

Source https://github.com/saltstack/salt/blob/v3004/salt/utils/verify.py
"""
import contextlib
import itertools
import logging
import os
import stat
import sys

import pytestskipmarkers.utils.platform

try:
    import pwd

    HAS_PWD = True
except ImportError:
    HAS_PWD = False

try:
    import grp

    HAS_GRP = True
except ImportError:
    HAS_GRP = False


try:
    LOGGING_TRACE_LEVEL = logging.TRACE
except AttributeError:
    # Salt's logging hasn't been setup yet
    LOGGING_TRACE_LEVEL = 5

EX_NOUSER = 67  # addressee unknown

log = logging.getLogger(__name__)


@contextlib.contextmanager
def set_umask(mask):
    """
    Temporarily set the umask and restore once the contextmanager exits.
    """
    if mask is None or pytestskipmarkers.utils.platform.is_windows():
        # Don't attempt on Windows, or if no mask was passed
        yield
    else:
        orig_mask = os.umask(mask)
        try:
            yield
        finally:
            os.umask(orig_mask)


def _get_pwnam(user):
    """
    Get the user from passwords database.
    """
    if HAS_PWD is False:
        return True
    try:
        return pwd.getpwnam(user)
    except KeyError:
        log.critical(
            "Failed to prepare the Salt environment for user %s. The user is not available.",
            user,
        )
        sys.exit(EX_NOUSER)


def get_group_list(user, include_default=True):
    """
    Returns a list of all of the system group names of which the user is a member.
    """
    if HAS_GRP is False or HAS_PWD is False:
        return []
    ugroups = set()
    group_names = [
        grp.getgrgid(grpid).gr_name for grpid in os.getgrouplist(user, pwd.getpwnam(user).pw_gid)
    ]

    if group_names is not None:
        ugroups.update(group_names)

    if include_default is False:
        # Historically, saltstack code for getting group lists did not
        # include the default group. Some things may only want
        # supplemental groups, so include_default=False omits the users
        # default group.
        try:
            default_group = grp.getgrgid(pwd.getpwnam(user).pw_gid).gr_name
            ugroups.remove(default_group)
        except KeyError:
            # If for some reason the user does not have a default group
            pass
    ugroups = sorted(ugroups)
    log.log(LOGGING_TRACE_LEVEL, "Group list for user '%s': %s", user, ugroups)
    return ugroups


def get_group_dict(user=None, include_default=True):
    """
    Returns a dict of all of the system groups as keys, and group ids as values, of which the user is a member.

    E.g.: {'staff': 501, 'sudo': 27}
    """
    if HAS_GRP is False or HAS_PWD is False:
        return {}
    group_dict = {}
    group_names = get_group_list(user, include_default=include_default)
    for group in group_names:
        group_dict.update({group: grp.getgrnam(group).gr_gid})
    return group_dict


def get_gid_list(user, include_default=True):
    """
    Returns a list of all of the system group IDs of which the user is a member.
    """
    if HAS_GRP is False or HAS_PWD is False:
        return []
    gid_list = list(get_group_dict(user, include_default=include_default).values())
    return sorted(set(gid_list))


def verify_env(dirs, user, permissive=False, pki_dir="", skip_extra=False, root_dir=None):
    """
    Verify that the named directories are in place and that the environment can shake the salt.
    """
    if root_dir is None:
        raise RuntimeError("'root_dir' must NOT be 'None'")

    if pytestskipmarkers.utils.platform.is_windows():
        import salt.utils.verify  # pylint: disable=import-outside-toplevel

        return salt.utils.verify.win_verify_env(
            root_dir, dirs, permissive=permissive, skip_extra=skip_extra
        )

    # after confirming not running Windows
    pwnam = _get_pwnam(user)
    uid = pwnam[2]
    gid = pwnam[3]
    groups = get_gid_list(user, include_default=False)

    for dir_ in dirs:
        if not dir_:
            continue
        if not os.path.isdir(dir_):
            try:
                with set_umask(0o022):
                    os.makedirs(dir_)
                # If starting the process as root, chown the new dirs
                if os.getuid() == 0:
                    os.chown(dir_, uid, gid)
            except OSError as err:
                msg = 'Failed to create directory path "{0}" - {1}\n'
                sys.stderr.write(msg.format(dir_, err))
                sys.exit(err.errno)

        mode = os.stat(dir_)
        # If starting the process as root, chown the new dirs
        if os.getuid() == 0:
            fmode = os.stat(dir_)
            if fmode.st_uid != uid or fmode.st_gid != gid:
                if permissive and fmode.st_gid in groups:
                    # Allow the directory to be owned by any group root
                    # belongs to if we say it's OK to be permissive
                    pass
                else:
                    # chown the file for the new user
                    os.chown(dir_, uid, gid)
            for subdir in [a for a in os.listdir(dir_) if "jobs" not in a]:
                fsubdir = os.path.join(dir_, subdir)
                if "{}jobs".format(os.path.sep) in fsubdir:
                    continue
                for root, dirs, files in os.walk(fsubdir):
                    for name in itertools.chain(files, dirs):
                        if name.startswith("."):
                            continue
                        path = os.path.join(root, name)
                        try:
                            fmode = os.stat(path)
                            if fmode.st_uid != uid or fmode.st_gid != gid:
                                if permissive and fmode.st_gid in groups:
                                    pass
                                else:
                                    # chown the file for the new user
                                    os.chown(path, uid, gid)
                        except OSError:
                            continue

        # Allow the pki dir to be 700 or 750, but nothing else.
        # This prevents other users from writing out keys, while
        # allowing the use-case of 3rd-party software (like django)
        # to read in what it needs to integrate.
        #
        # If the permissions aren't correct, default to the more secure 700.
        # If acls are enabled, the pki_dir needs to remain readable, this
        # is still secure because the private keys are still only readable
        # by the user running the master
        if dir_ == pki_dir:
            smode = stat.S_IMODE(mode.st_mode)
            if smode != 448 and smode != 488:
                if os.access(dir_, os.W_OK):
                    os.chmod(dir_, 448)
                else:
                    log.critical('Unable to securely set the permissions of "%s".', dir_)
