import re
from typing import Pattern


def uuid_regex(base_url: str) -> Pattern:
    """Generate a compiled UUID regex for a specific base URL"""
    return re.compile(
        base_url
        + "ids/"  # Base URL
        +  # Always present in canonical ID URIs
        # Standard UUID regex
        "(?P<uuid>[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12})"
        + "/"  # Trailing slash
    )
