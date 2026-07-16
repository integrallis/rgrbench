# URL decomposition into named parts

## Overview
Web tooling often needs a URL taken apart into its meaningful pieces rather than
handled as one opaque string. Given a URL, the system breaks it into protocol,
subdomain, domain, port, path, query string, and anchor. Missing pieces get sensible
values — well-known default ports per protocol, empty text for absent parts — and
URLs that do not fit the supported grammar are rejected with messages that name what
is wrong.

## User Stories

### US-1: Split a URL into protocol, subdomain, domain, and path
As a developer of web tooling, I want a URL decomposed into its host and path pieces, so that each piece can be inspected or routed on directly.

- AC-1.1: A URL splits into protocol, subdomain, domain, port, and path; the address "http://foo.bar.com/foobar.html" yields protocol "http", subdomain "foo", domain "bar.com", port 80, and path "foobar.html" (canonical worked example), while "https://www.foobar.com:8080/download/install.exe" keeps its explicit port 8080 and its full nested path.
- AC-1.2: Everything before the domain-plus-TLD is the subdomain, so a host "a.b.bar.com" has subdomain "a.b" and domain "bar.com".
- AC-1.3: A host with no labels before the domain has an empty subdomain.
- AC-1.4: A single-word local host name such as "localhost" is the domain itself, with an empty subdomain, and combines with explicit ports and paths.
- AC-1.5: A URL with no path at all, or with only a bare trailing slash, has an empty path.
- AC-1.6: For dotted hosts the recognised top-level domains are com, net, org, int, edu, gov, and mil.

### US-2: Apply and override well-known ports
As a developer of web tooling, I want the port filled in from the protocol when the URL leaves it out, so that consumers always see a concrete port number.

- AC-2.1: When no port is given, the protocol's default applies: 80 for http, 443 for https, 21 for ftp, and 22 for sftp.
- AC-2.2: An explicit port in the URL overrides the protocol default.

### US-3: Capture query string and anchor separately
As a developer of web tooling, I want the query string and anchor isolated from the path, so that navigation and parameters can be handled independently.

- AC-3.1: The text after "?" is the query string, captured verbatim as its own part and excluded from the path.
- AC-3.2: The text after "#" is the anchor, captured as its own part and excluded from the path; absent parts are empty text.
- AC-3.3: A query string and an anchor may both be present on one URL, alongside subdomain and domain.
- AC-3.4: A query string may follow the host directly with no path in between, leaving the path empty.
- AC-3.5: The protocol is split off at the first "://" only, so a full URL embedded inside the query string stays verbatim in the query and does not confuse the split.

### US-4: Reject URLs outside the supported grammar
As a developer of web tooling, I want unsupported or malformed URLs refused with a message naming the problem, so that bad addresses are caught at the boundary.

- AC-4.1: Only the protocols http, https, ftp, and sftp are supported; any other protocol is rejected with the message "Unsupported protocol: '<protocol>'" — for example "Unsupported protocol: 'gopher'".
- AC-4.2: A URL without the "://" marker is rejected with the message "Malformed URL, missing '://': '<the given text>'".
- AC-4.3: A dotted host whose last label is not a recognised top-level domain is rejected with the message "Unsupported top-level domain: '<that label>'", naming the host's last label even for multi-label hosts.
- AC-4.4: A non-numeric port is rejected; everything after the first colon in the host section counts as the port text, and the message reads "Invalid port: '<that text>'" — for example a host section "foo.com:8080:9090" gives "Invalid port: '8080:9090'".
- AC-4.5: A URL with nothing between "://" and the path is rejected with the message "Missing host".

## Traceability
```json
{
  "test_url_with_subdomain_and_default_http_port": ["AC-1.1", "AC-2.1"],
  "test_url_with_explicit_port_and_nested_path": ["AC-1.1", "AC-2.2"],
  "test_ftp_url_without_subdomain": ["AC-1.3"],
  "test_localhost_with_anchor": ["AC-1.4", "AC-2.1", "AC-3.2"],
  "test_sftp_default_port": ["AC-2.1"],
  "test_ftp_default_port": ["AC-2.1"],
  "test_explicit_port_overrides_default": ["AC-2.2"],
  "test_multi_level_subdomain": ["AC-1.2"],
  "test_url_without_path": ["AC-1.5"],
  "test_url_with_trailing_slash_has_empty_path": ["AC-1.5"],
  "test_query_string_is_captured_and_excluded_from_path": ["AC-3.1"],
  "test_anchor_is_captured_and_excluded_from_path": ["AC-3.2"],
  "test_query_string_and_anchor_together": ["AC-3.3"],
  "test_query_string_directly_after_host": ["AC-3.4"],
  "test_all_supported_top_level_domains": ["AC-1.6"],
  "test_unsupported_protocol_raises": ["AC-4.1"],
  "test_url_without_protocol_marker_raises": ["AC-4.2"],
  "test_unsupported_top_level_domain_raises": ["AC-4.3"],
  "test_local_hostname_with_port_and_path": ["AC-1.4"],
  "test_protocol_is_split_at_the_first_marker": ["AC-3.5"],
  "test_invalid_port_raises_naming_the_port_text": ["AC-4.4"],
  "test_url_with_empty_host_raises": ["AC-4.5"],
  "test_unsupported_tld_error_names_the_tld": ["AC-4.3"]
}
```

Machine-derived from the package's verified test suite, 2026; see requirements/PROTOCOL.md.
