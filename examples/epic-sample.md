# Epic: usage-based billing

- Date: YYYY-MM-DD
- Status: active
- Tracker: PROJ-100

## Destination

Customers are billed by metered usage: billable actions are recorded per account, aggregated
into invoice lines, and visible to the customer before the invoice is issued.

## Notes

- Domain: billing; significant money-path choices go through the `decision-log` gate.
- Payment provider docs are external knowledge - research items, not code reading.

## Frontier

### Choose the usage aggregation window

- Type: decide
- Mode: HITL
- Blocked by: none
- Question: hourly or daily rollups - what granularity do invoices and the customer view actually need?

### Payment provider metering API limits

- Type: research
- Mode: AFK
- Blocked by: none
- Question: what rate limits and batch sizes does the provider's metering API allow for usage ingestion?

## Tasks

### Record usage events per account

- Goal: every billable action lands as a usage event with account, kind, and quantity - the raw material every later step aggregates.
- Blocked by: none
- Tracker: PROJ-101
- Status: done
- Plan: docs/plans/YYYYMMDD-PROJ-101-usage-events.md

### Customer usage view

- Goal: the customer sees current-period usage before the invoice is issued, from the same events billing will use.
- Blocked by: Record usage events per account
- Status: ready

### Aggregate usage into invoice lines

- Goal: turn recorded events into per-account invoice lines at the chosen window, so an invoice can be assembled from them.
- Blocked by: Record usage events per account, Choose the usage aggregation window
- Tracker: PROJ-102
- Status: blocked

## Decisions so far

- Event store choice -> reuse the existing `events` table with a `billing` kind instead of a new store (docs/epics/YYYYMMDD-PROJ-100-usage-based-billing/event-store-spike.md)
- Billing currency -> invoices are issued in the account's own currency, no conversion

## Not yet specified

- How refunds and credits offset metered usage - hangs on the aggregation window decision.

## Out of scope

- Migrating legacy fixed-price contracts - past the destination; existing contracts keep their current billing.
