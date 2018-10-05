import re

PRIVATE_KEY_LENGTH = 64
PRIVATE_KEY_PATTERN = re.compile(r"^[0-9a-f]{64}$")
PUBLIC_KEY_LENGTH = 66
PUBLIC_KEY_PATTERN = re.compile(r"^[0-9a-f]{66}$")
SIGNATURE_LENGTH = 128
SIGNATURE_PATTERN = re.compile(r"^[0-9a-f]{128}$")
