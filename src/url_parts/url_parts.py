"""URL Parts kata.

Requirements summary (paraphrased): decompose a URL into its parts using only
plain string handling — no built-in URI classes and no regular expressions.
The parts are: protocol (one of http, https, ftp or sftp), optional subdomain,
domain (host name plus top-level domain), port (explicit, or the protocol's
default of 80/443/21/22 when omitted), path without its leading slash, query
string and anchor. Query string and anchor are captured separately and never
included in the path. Only the top-level domains .com, .net, .org, .int,
.edu, .gov and .mil are supported, while local host names such as
``localhost`` have no TLD and no subdomain. Unsupported protocols or
top-level domains and structurally broken URLs raise ``ValueError``.

Kata catalogued at tddbuddy.com/katas/url-parts; implementation and tests original (MIT),
machine-authored from the specification, 2026.
"""

from __future__ import annotations

from dataclasses import dataclass

DEFAULT_PORTS: dict[str, int] = {"http": 80, "https": 443, "ftp": 21, "sftp": 22}
SUPPORTED_TLDS: frozenset[str] = frozenset(
    {"com", "net", "org", "int", "edu", "gov", "mil"}
)

_PROTOCOL_MARKER = "://"


@dataclass(frozen=True)
class UrlParts:
    """The constituent parts of a parsed URL."""

    protocol: str
    subdomain: str
    domain: str
    port: int
    path: str
    query: str
    anchor: str


def parse_url(url: str) -> UrlParts:
    """Parse ``url`` into a :class:`UrlParts` value."""
    protocol, rest = _split_protocol(url)
    rest, anchor = _split_off(rest, "#")
    rest, query = _split_off(rest, "?")
    host_and_port, path = _split_off(rest, "/")
    host, port = _split_port(host_and_port, protocol)
    subdomain, domain = _split_host(host)
    return UrlParts(protocol, subdomain, domain, port, path, query, anchor)


def _split_protocol(url: str) -> tuple[str, str]:
    index = url.find(_PROTOCOL_MARKER)
    if index == -1:
        raise ValueError(f"Malformed URL, missing '://': {url!r}")
    protocol = url[:index].lower()
    if protocol not in DEFAULT_PORTS:
        raise ValueError(f"Unsupported protocol: {url[:index]!r}")
    return protocol, url[index + len(_PROTOCOL_MARKER) :]


def _split_off(text: str, separator: str) -> tuple[str, str]:
    head, _, tail = text.partition(separator)
    return head, tail


def _split_port(host_and_port: str, protocol: str) -> tuple[str, int]:
    if ":" not in host_and_port:
        return host_and_port, DEFAULT_PORTS[protocol]
    host, _, port_text = host_and_port.partition(":")
    if not port_text.isdigit():
        raise ValueError(f"Invalid port: {port_text!r}")
    return host, int(port_text)


def _split_host(host: str) -> tuple[str, str]:
    if not host:
        raise ValueError("Missing host")
    if "." not in host:
        return "", host
    labels = host.split(".")
    if labels[-1].lower() not in SUPPORTED_TLDS:
        raise ValueError(f"Unsupported top-level domain: {labels[-1]!r}")
    return ".".join(labels[:-2]), ".".join(labels[-2:])
