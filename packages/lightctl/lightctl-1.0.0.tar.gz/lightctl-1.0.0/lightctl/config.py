import os
from pathlib import Path

API_VERSION = "v1"

ACCESS_TOKEN_CACHE_FILE_PATH = os.environ.get(
    "CACHED_CREDENTIAL_PATH",
    os.path.join(str(Path.home()), ".lightup", ".access-token-cache"),
)

CREDENTIAL_FILE_PATH = os.environ.get(
    "LIGHTCTL_CREDENTIAL_PATH",
    os.path.join(str(Path.home()), ".lightup", "credential"),
)

BASE_WORKSPACE_UUID = os.environ.get(
    "LIGHTCTL_DEFAULT_WORKSPACE", "497d2c3e-2e24-47ec-b33a-dcf3999062a7"
)
