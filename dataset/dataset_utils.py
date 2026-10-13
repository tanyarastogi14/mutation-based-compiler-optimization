import hashlib


def source_fingerprint(source_code: str) -> str:
    """Return a stable fingerprint for a source program."""

    normalized_source = "\n".join(
        line.strip()
        for line in source_code.strip().splitlines()
        if line.strip()
    )

    return hashlib.sha256(
        normalized_source.encode("utf-8")
    ).hexdigest()