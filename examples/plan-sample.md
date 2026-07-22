# Add pagination to the items list endpoint

## Overview

`GET /items` returns the full table in one response, which grows unbounded and times out
on large accounts. Add offset / limit pagination with a stable sort and a total count so
clients can page through results. Small, backward-compatible change: no pagination params
keeps today's behavior for the first page.

## SOURCE ARTIFACTS

- Brief: `docs/nxs/briefs/YYYYMMDD-items-pagination-rnd.md`
- Tracker: PROJ-123

## ACCEPTANCE CRITERIA

- `GET /items?limit=20&offset=40` returns at most 20 items starting at offset 40.
- Response includes `total` (unfiltered row count) and echoes `limit` / `offset`.
- No params -> first page at the default limit; existing clients keep working.
- `limit` above the max is clamped to the max; negative `limit` / `offset` -> 400.
- Results are ordered by a stable key so pages do not overlap or skip rows.

## DEVELOPMENT APPROACH

default - tests written together with the code for each task.

## Implementation

### Task 1: Parse and validate pagination params

**Files:**
- Create: `src/items/pagination.py`
- Create: `tests/items/test_pagination.py`

**Test cases:**
- parse_page_params({}) -> limit=DEFAULT_LIMIT, offset=0
- parse_page_params({limit: 20, offset: 40}) -> limit=20, offset=40
- parse_page_params({limit: 5000}) -> limit clamped to MAX_LIMIT
- parse_page_params({limit: -1}) -> raises InvalidPageParams
- parse_page_params({offset: -1}) -> raises InvalidPageParams

- [ ] add `parse_page_params(query)` returning a validated `(limit, offset)` pair
- [ ] apply DEFAULT_LIMIT / MAX_LIMIT clamping and reject negative values
- [ ] write tests from Test cases above (defaults and valid input)
- [ ] write tests from Test cases above (clamping and rejection)
- [ ] run tests - must pass before task 2

Success: invalid params are rejected before any DB access; defaults match current behavior.

### Task 2: Apply pagination in the items repository query

**Files:**
- Modify: `src/items/repository.py`
- Modify: `tests/items/test_repository.py`

**Test cases:**
- list_items(limit=20, offset=40) -> returns rows 41..60 ordered by id
- list_items(limit=20, offset=40) -> also returns unfiltered total count
- list_items with offset past the end -> returns empty page, total unchanged

- [ ] add `limit` / `offset` and a stable `ORDER BY id` to the list query
- [ ] return the total row count alongside the page
- [ ] update / parametrize repository tests for the cases above
- [ ] run tests - must pass before task 3

Success: the query returns a bounded, stably ordered page plus an accurate total.

### Task 3: Wire pagination into the GET /items handler

**Files:**
- Modify: `src/items/handler.py`
- Modify: `tests/items/test_handler.py`

**Test cases:**
- GET /items?limit=20&offset=40 -> 200, <=20 items, body has total/limit/offset
- GET /items (no params) -> 200, first page at DEFAULT_LIMIT
- GET /items?limit=-1 -> 400 with an error body

- [ ] call parse_page_params, then the paginated repository query
- [ ] shape the response body with `items`, `total`, `limit`, `offset`
- [ ] map InvalidPageParams to a 400 response
- [ ] update / parametrize handler tests for the cases above
- [ ] run tests + lint - must pass; check against ACCEPTANCE CRITERIA
