## Conventions

<rules every task follows - style, naming, a repeated step, a standing preference. /dev:exec passes this
section to every worker, so what is missing here does not reach the code. Do not copy in what the project's
CLAUDE.md already says: exec passes the project rules separately, and a duplicate only inflates every worker
prompt. No such rules, no section.>

## Implementation

### Task 1: A visitor registers with an email and lands in the database

**Files:**
- Create: migrations/0007_users.sql
- Create: src/auth/hash.go
- Modify: src/users/service.go
- Modify: src/api/routes.go

- [ ] add the users migration with a unique index on email
- [ ] add HashPassword in src/auth/hash.go (bcrypt, configurable cost)
- [ ] add service.Register: normalize, hash, persist, ErrEmailTaken on a duplicate
- [ ] wire POST /api/users to the service and map errors to 201 / 409 / 422
- [ ] write tests: fresh email stores a hash and never the plaintext, duplicate gives 409, malformed gives 422
- [ ] run `go test ./users/... ./api/...`
