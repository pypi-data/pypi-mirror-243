"""
The Main program to commit the palo alto resources.

:author: Johan Lanzrein
:file: commit.py
"""
import difflib
import logging
import time
from multiprocessing.pool import ThreadPool as Pool

import requests
import xmltodict
from nagra_panorama_api.restapi import PanoramaClient
from nagra_panorama_api.xmlapi import XMLApi, etree_tostring
from panos import panorama

# PANORAMA = os.environ["PANOS_HOSTNAME"]
# URL = f"https://{PANORAMA}/api/"
# API_KEY = os.environ["PANOS_API_KEY"]
# BRANCH = os.environ["CI_COMMIT_REF_NAME"]
# ADMIN_PANOS = os.environ.get("PANOS_ADMIN_NAME", "svc-sec-group-IT")

log = logging.getLogger(__name__)


def api_call_status(response_dict: dict) -> str:
    """
    Get the api status.

    :param response_dict: the response from an XML api call
    :return: success or error
    """
    status = response_dict["response"]["@status"]
    if status in ("error", "success"):
        return status
    return None


def commit_all(
    url,
    api_key,
    device: str,
    branch=None,
    commit_sha=None,
    description=None,
) -> bool:
    """
    Commit all operation to the given device groups.

    :param device: The device to commit to
    :return:nothing
    """
    if not description:
        if commit_sha:
            description = (
                f"Palo Alto pipeline update from {branch} (Commit Sha {commit_sha})"
            )
        else:
            description = "Automatic Palo Alto pipeline update"

    failed = False
    pano = panorama.Panorama(url, api_key=api_key)
    description = f"Palo Alto pipeline update from {branch} (Commit Sha {commit_sha})"

    # Commit and wait if you don't want to wait and just fire and forget you can set sync and sync_all to false.
    # it's harder to see if there is any failures if you do that though.
    try:
        result = pano.commit_all(
            sync=True,
            sync_all=True,
            exception=True,
            devicegroup=device,
            description=description,
        )
        log.info(
            "Got answer for commit at {} : Success {} ; result : {}".format(
                device,
                result["success"],
                result["result"],
            ),
        )
        messages = result["messages"]
        if len(messages) > 0:
            log.info("""Got following messages:\n{"\n".join(messages)}""")
    except Exception as e:
        failed = True
        log.error(f"Got error : {e} while trying to commit on device {device}")
    return failed


def commit(
    url,
    api_key,
    admin: str,
    commit_type="normal",
    description="Terraform pipeline auto commit",
    verify=False,
    timeout=None,
) -> str:
    """
    Commit on the panorama
    :param admin: admin name under which to commit
    :param commit_type: the type of commit
    :return: error or success or same_config
    """
    api = XMLApi(url, api_key, verify=verify, timeout=timeout)
    # Check if there are changes pending to commit
    if commit_type != "all":
        cmd = "<check><pending-changes></pending-changes></check>"
        res = api.operations(cmd)
        contents = xmltodict.parse(etree_tostring(res))
        is_success = api_call_status(contents) == "success"
        if is_success and contents["response"]["result"] == "no":
            log.info("No changes to commit")
            return "error"
    description_tag = f"<description>{description}</description>"
    # Determine which type of commit is requested
    if commit_type == "partial":
        # Make a partial commit for a given admin.

        cmd = (
            "<commit><partial>"
            "<device-and-network>excluded</device-and-network>"
            "<shared-object>excluded</shared-object>"
            f"<admin><member>{admin}</member></admin>"
            f"{description_tag}"
            "</partial></commit>"
        )
    elif commit_type == "all":
        # This is NOT Working
        cmd = (
            "<commit-all><shared-policy><device-group><entry/></device-group>"
            f"{description_tag}</shared-policy></commit-all>"
        )
    elif commit_type == "partial-commit-network":
        # Payload for "partial" commit "device-and-network"
        cmd = (
            "<commit><partial><device-and-network>"
            "</device-and-network></partial></commit>"
        )
    elif commit_type == "partial-commit-policy":
        # Payload for partial commit "policy-and-objects"
        cmd = (
            "<commit><partial><policy-and-objects>"
            "</policy-and-objects></partial></commit>"
        )
    elif commit_type == "force-commit":
        # Payload for "force" commit
        cmd = "<commit><force></force></commit>"
    elif commit_type == "normal":
        # Payload for normal commit
        cmd = "<commit></commit>"

    # Send request to commit and parse response into dictionary
    res = api._commit_request(cmd)  # noqa
    contents = xmltodict.parse(etree_tostring(res))
    # TODO: Code should always return a value
    if api_call_status(contents) == "success":
        try:
            # Commit sent successfully
            line = contents["response"]["result"]["msg"]["line"]
            log.info(
                f"""Success: {line}""",
            )
            job_id = contents["response"]["result"]["job"]

            # Loop to check the job status every 20 seconds until the job
            # is completed, or up to 5 minutes (15 retries)
            for retry in range(15):
                log.info("Job pending - waiting 20 seconds to check status")
                time.sleep(20)
                # Send request and parse response in a dictionary
                res = api.get_jobs(job_id)
                contents = xmltodict.parse(etree_tostring(res))
                job = contents["response"]["result"]["job"]
                details = job["details"]["line"]
                if not isinstance(details, str):
                    details = details[0]
                result = job["result"]
                # If job is still pending, continue loop
                if result == "PEND":
                    job_progress = job["progress"]
                    log.warning(
                        f"Job pending: {job_progress}% completed",
                    )
                    retry += 1
                    if retry == 15:
                        log.info("Commit pending for 5 minutes - stopping script")
                        exit()
                elif result == "FAIL":
                    log.error(f"Commit FAILED: {details}")
                    return "fail"
                    # todo: Check details of commit, different path if commit to Panorama or commit to FW
                elif result == "OK":
                    log.info(f"Commit FAILED: {details}")
                    return "success"
                else:
                    log.error("ERROR")
                    return "error"
        except KeyError:
            # No pending changes to commit
            log.info(
                f"""Success: {contents["response"]["msg"]}""",
            )
            return "same_config"
    return None


def check_pending_on_devices(
    devices: list,
    api_key,
    url,
    verify=False,
    timeout=None,
) -> bool:
    """
    Check if there is any pending changes specifically on a list of devices.

    :param devices: The devices to look up for
    :return: True if there are any pending changes.
    """
    if "DG1_GLOBAL" in devices:
        return True

    payload = {
        "type": "op",
        "key": api_key,
        "cmd": "<show><config><list><change-summary/></list></config></show>",
    }

    response = requests.request(
        "GET",
        url,
        params=payload,
        verify=verify,
        timeout=timeout,
    )
    xmlized = xmltodict.parse(response.text)

    # if there is no changes result is None -> return False
    result = xmlized["response"]["result"]
    if result is None:
        return False
    # get the device groups
    summary = result["summary"]
    # first check in the device group

    if "device-group" in summary:
        device_groups = summary["device-group"]
        for device in devices:
            if device in device_groups["member"]:
                return True
    # then check in the template to make sure its all clear.
    elif "template" in summary:
        template = summary["template"]
        for device in devices:
            if device in template["member"]:
                return True
    return False


def check_pending(url, api_key, verify=False, timeout=None) -> str:
    """
    Function to check if there are pending changes
    :return: "success" if changes are pending, return "error" if no changes
    """

    # Build URL
    api = XMLApi(url, api_key, verify=verify, timeout=timeout)
    pending = api.pending_changes().xpath("response/result/text()")
    return {
        "no": "error",
        "yes": "success",
    }.get(pending)


def config_diff(url, api_key, verify=False, timeout=None) -> str:
    """
    Function to compare candidate and running configurations

    :return: error string
    """
    if check_pending() == "error":
        log.info("No pending changes")
        return "error"

    api = XMLApi(url, api_key, verify=verify, timeout=timeout)
    # Send request for Candidate config, put response in a file
    candidate = etree_tostring(api.candidate_config())
    running = etree_tostring(api.running_config())

    # Running diff on the two files
    diff = difflib.context_diff(
        running.splitlines(),
        candidate.splitlines(),
        fromfile="Running",
        tofile="Candidate",
        n=3,
    )
    log.info("".join(list(diff)))
    return None


def revert_config(url, api_key, admin, verify=False, timeout=None) -> str:
    """
    Function to revert the pending changes (back to the running configuration)

    :param admin: The admin name under which to revert.
    """
    if check_pending() == "error":
        log.info("No changes to revert")
        return "error"

    # Payload to revert
    payload_revert = {
        "type": "op",
        "key": api_key,
        "cmd": f"<revert><config><partial><admin><member>{admin}</member></admin></partial></config></revert>",
    }
    # Send request and put output in a dictionary
    response = requests.get(url, params=payload_revert, verify=verify, timeout=timeout)
    contents = xmltodict.parse(response.text)
    if api_call_status(contents) == "success":
        result = contents["response"]["result"]
        log.info(
            f"SUCCESS: {result}",
        )
        return None
    if api_call_status(contents) == "error":
        log.error(f"Could not revert the config : {contents}")
        return None
    return None


def get_all_device_groups(url, api_key) -> list:
    """
    Function to get all devices registered in Panorama
    """
    client = PanoramaClient(url, api_key)
    return [g["@name"] for g in client.panorama.DeviceGroups.get()]


def push(device_group, branch=None):
    jobs = {}
    with Pool(len(device_group)) as pool:
        results = pool.map(lambda d: commit_all(d, branch=branch), device_group)
    if any(results):
        raise SystemError("ERROR: Push has failed on one or more Firewall")
    return jobs
