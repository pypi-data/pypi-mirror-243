import logging
import time

import panos.errors
from panos import panorama

from .panorama import check_pending_on_devices

# PANORAMA = os.environ["PANOS_HOSTNAME"]
# URL = f"https://{PANORAMA}/api/"
# API_KEY = os.environ["PANOS_API_KEY"]
# FIREWALLS = (
#     os.environ["FIREWALLS"]
#     .replace("['", "")
#     .replace("']", "")
#     .replace("'", "")
#     .replace(" ", "")
#     .split(",")
# )

log = logging.getLogger("Panorama locker")


def check_lock(url, api_key, firewalls, max_tries=60) -> bool:
    panorama_instance = panorama.Panorama(url, api_key=api_key)
    # check if there is a pending change.
    for _ in range(max_tries):
        if check_pending_on_devices(firewalls, api_key, url):
            log.info("Pending changes. Trying in 1min again..")
            time.sleep(60)
            continue
        if (
            panorama_instance.check_config_locks()
        ):  # check_config_locks returns true if there is a lock.
            log.info("No changes but lock is already taken. Trying in 1 min.")
            time.sleep(60)
            continue
        return  # status unchanged AND panorama has no lock.
    raise TimeoutError(
        "Pending changes that need to be committed and pushed on the firewall. "
        f"Tried for {max_tries} min can not access firewall",
    )


def lock_pano(url, api_key, firewalls=None, comment="Terraform pipeline"):
    """
    if firewalls is specied, the lock is only put on the firewalls
    otherwise, the lock is put on all panorama
    """
    panorama_instance = panorama.Panorama(url, api_key=api_key)
    # we can now try and lock.
    if not firewalls:
        firewalls = [None]  # Don't provide a scope
    for fw in firewalls:
        panorama_instance.add_config_lock(
            scope=fw,
            comment=comment,
        )


def try_lock(url, api_key, firewalls, max_tries=60) -> bool:
    """
    Try to get the config lock of the panorama todo simplify
    :param max_tries: Maximum number of tries to get the config lock.
    :param panorama_instance: the panorama instance to lock
    :return: a status boolean
    """
    panorama_instance = panorama.Panorama(url, api_key=api_key)
    for _ in range(3):
        check_lock(url, api_key, firewalls, max_tries=max_tries)
        # we can now try and lock.
        lock_pano(panorama_instance, firewalls)

        log.info("Acquired the panorama config lock")
        # check for changes again if someone made some in the meanwhile..
        changed = check_pending_on_devices(firewalls, api_key, url)
        # if we were able to lock we can safely exit.
        if not changed:
            return True

        log.warn("Changes detected after locking the config")
        # we have pending changes !!!
        # release the lock and restart everything
        unlock_pano(panorama_instance)
    return False


def _unlock_pano(panorama_instance: panorama.Panorama, fw=None) -> bool:
    """
    Unlocks a config lock on a panorama. Raise excpetion if the lock can not be removed.
    :param panorama_instance: the panorama to unlock the config lock from.
    """
    try:
        if fw:
            res = panorama_instance.remove_config_lock(scope=fw)
        else:
            res = panorama_instance.remove_config_lock()
        if res:
            log.info(f"Successfully removed the lock for {fw}")
            return True
    except panos.errors.PanDeviceXapiError as e:
        log.error(e)
    log.error(f"Could not remove config lock for {fw}")
    return False


def unlock_pano(panorama_instance: panorama.Panorama, firewalls) -> bool:
    """
    Unlocks a config lock on a panorama. Raise excpetion if the lock can not be removed.
    :param panorama_instance: the panorama to unlock the config lock from.
    """
    if not firewalls:
        return _unlock_pano(panorama_instance)
    error = False
    for fw in firewalls:
        error &= _unlock_pano(panorama_instance, fw)
    return not error
