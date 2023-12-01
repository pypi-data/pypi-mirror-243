from pathlib import Path

DEFAULT_GIT_DIR = Path("./working_git").resolve()
DEFAULT_TERRAFORM_PATH = DEFAULT_GIT_DIR / "data/addresses.yml"

IP_REGEX_STR = (
    "([0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5])\.){3}"
    "([0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5])"
)
SUBNET_REGEX_STR = IP_REGEX_STR + "(\-(3[0-2]|[1-2][0-9]|[0-9]))"
