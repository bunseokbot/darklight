"""Collect the single onion URL configured for the classroom."""

from urllib.parse import urlparse

from .base import SourceBase

from utils.logging.log import Log


class ConfiguredOnionCollector(SourceBase):
    """Load exactly one approved target from ``config.ini``."""

    cycle = 1440
    name = "configured onion"

    def collect(self):
        target = (self.ini.read("SOURCE", "ONION_URL") or "").strip()

        if not target:
            Log.e("Set one approved URL in SOURCE.ONION_URL")
            return

        if any(character.isspace() for character in target):
            raise ValueError("SOURCE.ONION_URL must contain one URL")

        parsed = urlparse(target)
        if parsed.scheme not in ("http", "https") or not parsed.hostname:
            raise ValueError("SOURCE.ONION_URL must be an http(s) URL")
        if parsed.username or parsed.password:
            raise ValueError("SOURCE.ONION_URL must not contain credentials")

        try:
            port = parsed.port
        except ValueError:
            raise ValueError("SOURCE.ONION_URL contains an invalid port")

        if port is not None:
            raise ValueError("SOURCE.ONION_URL must not contain an explicit port")
        if not parsed.hostname.lower().endswith(".onion"):
            raise ValueError("SOURCE.ONION_URL must point to an .onion host")

        self.urls = [target]
        Log.i("Loaded the configured onion URL")
