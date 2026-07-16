"""URL Parts kata: decompose URLs into protocol, subdomain, domain, port, path,
query and anchor without built-in URI helpers.

Kata catalogued at tddbuddy.com/katas/url-parts; implementation and tests original (MIT),
machine-authored from the specification, 2026.
"""

from url_parts.url_parts import DEFAULT_PORTS, SUPPORTED_TLDS, UrlParts, parse_url

__all__ = ["DEFAULT_PORTS", "SUPPORTED_TLDS", "UrlParts", "parse_url"]
