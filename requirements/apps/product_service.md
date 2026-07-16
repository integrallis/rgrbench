# Product catalog web service with optimistic concurrency

## Overview
An HTTP service maintaining a product catalog. Clients create, read, update, and delete
products (name and quantity) over a JSON API. Every product carries a version used for
optimistic concurrency control: reads and writes exchange the version through entity-tag
headers, updates must present the current version, and stale updates are rejected as
conflicts. The service reports its own health.

## User Stories

### US-1: Service health
As an operator, I want a health endpoint, so that I can verify the service is up.

- AC-1.1: A health request succeeds and reports the service as healthy.

### US-2: Manage products
As a catalog manager, I want to create, view, and delete products, so that the catalog reflects inventory.

- AC-2.1: Creating a product returns a created status, the stored product, and an entity tag carrying version 1.
- AC-2.2: A product can be fetched by its identifier, returning its data and current version tag.
- AC-2.3: Fetching, updating, or deleting a nonexistent product reports not-found.
- AC-2.4: Deleting a product succeeds, after which it can no longer be fetched.

### US-3: Optimistic concurrency
As a catalog manager, I want versioned updates, so that concurrent edits cannot silently overwrite each other.

- AC-3.1: An update presenting the product's current version succeeds and increments the version, returning the new tag.
- AC-3.2: An update presenting a stale version is rejected as a conflict and changes nothing.

## Traceability
```json
{
  "test_health_check_returns_200": ["AC-1.1"],
  "test_get_product_by_id_found": ["AC-2.2"],
  "test_get_product_by_id_not_found": ["AC-2.3"],
  "test_create_product": ["AC-2.1"],
  "test_update_product_with_version": ["AC-3.1"],
  "test_delete_product": ["AC-2.4"],
  "test_update_product_version_conflict": ["AC-3.2"],
  "test_update_product_not_found": ["AC-2.3"],
  "test_delete_product_not_found": ["AC-2.3"]
}
```

Machine-derived from the package's verified test suite, 2026; see requirements/PROTOCOL.md.
