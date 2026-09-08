# Roadmap

This document outlines the planned evolution of QuoinAPI. It reflects the
current thinking of the maintainers and is subject to change based on community
feedback and shifting priorities.

!!! note
    This is a living document. Completed items are moved to
    [CHANGELOG.md](changelog.md).

## Status Legend

| Symbol | Meaning |
| :----- | :------ |
| ✅ | Completed (unreleased) |
| 🚧 | In Progress |
| 📋 | Planned |
| 💡 | Under Consideration |
| ❌ | Deferred / Won't Do |

The public API contract is locked. The pagination envelope, soft delete,
and the deprecation mechanism shipped in `0.9.0`; the API stability and
semver policy followed in `0.10.0`. `0.11.0` closed the request-path
correctness work — the transaction now commits *before* the response is
sent, an unhandled 500 carries the same headers as every other error,
`QUOIN_LOG_LEVEL` is wired to something, JWT claims are required rather
than merely verified, and production boot validates hosts as well as
OAuth.

**`0.10.0` was the last feature release before `1.0`.** What remains is
proof and rehearsal, not code: prove the template generates a project
that passes its own gate, rehearse the release once for real, then ship.
No backlog item is promoted into `0.12` — the backlog's bar ("a concrete
user is blocked") has not been met by anyone yet, and meeting it after
`1.0` costs nothing.

The backlog below is deliberately narrow: it lists only demand-gated
*features* — application code we would ship behind a feature flag or as
an example module when a concrete user is blocked. Operational and
deployer-specific concerns (alert thresholds, deploy/rollback workflows,
backup runbooks) and rot-prone checklists were dropped outright rather
than parked — they belong in your infrastructure repo, not a backend
code template. All observability follows OpenTelemetry and CNCF
standards — no vendor-specific tooling.

Features are dropped rather than parked on the same test: shipping them
would be wrong regardless of demand, because they are better solved at
the edge, depend on facts only the deployer knows, or would compete
badly with a mature product category. Rate limiting, a secrets-manager
adapter, PII encryption, feature flags, an audit table, and retention
jobs all failed it. ETag concurrency left the backlog too, but as a
[guide](../guides/optimistic-concurrency.md) rather than a deletion —
the pattern is worth documenting even though the code isn't worth
shipping.

---

## v0.12.0 — Proof

The last `0.x` release. It changes no application behaviour: every item
is a CI job or a document, so `copier update` from `0.11.0` should be
conflict-free end to end.

The theme is closing the gap between what the repository *promises* and
what it *verifies*. Two promises are still checked by a human running a
command from memory, and one is not written down at all.

| Status | Item | Why now |
| :----- | :--- | :------ |
| ✅ | **PR-gated scaffold smoke test** — a CI job that runs `copier copy --trust --vcs-ref=HEAD` into a temp directory, then `uv sync --all-groups && just check` inside the generated project | The largest open promise in the repo. The launch checklist has asked for this since `v0.9.0` and it has only ever been run by hand — which is how `0.11.0` shipped a template whose generated `metadata.py` failed its own `just lint`. Reuses the Postgres service already in `ci.yml`; pin one Python version to keep CI time down. Shipped with the fix for the defect it was expected to surface: substituting identifiers changes line length *and* import sort order, so five generated files arrived unformatted (`QUOINAPI_` splits a line `QUOIN_` fit, the shorter `AppError` joins one, and a renamed import moves in the sort). No hand-wrapping in the template can fix that — correct output genuinely differs per project name — so `copier_setup.py` now formats after substitution, and the job asserts the generated gate changes nothing |
| ✅ | **Scheduled dependency audit** — a weekly workflow running `just audit` and `just audit-prod`, opening an issue on failure | `just audit` exists and nothing runs it. Today a CVE surfaces only when a human remembers before a release, which makes the launch checklist's CVE item a point-in-time snapshot rather than a standing guarantee |
| 📋 | **`docs/guides/staying-current.md`** — how an adopter with their own modules takes a new template release: what `copier update` does, how to read a **manual reconciliation** note, and how to resolve a `.rej` | `0.11.0` is the first release to demand real reconciliation work (`SessionDep`, `fail_under = 100`, `validate_production_settings`, `QUOIN_ALLOWED_HOSTS`). The policy says *what* is breaking; nothing says *what to do about it* |
| 📋 | **Run `just check` after `copier update` in the update workflow** | `scripts/verify_template_update.py` deliberately proves only that the update applies cleanly — no `.rej`, answers file updated. Once the smoke job exists, asserting the *updated* project also passes its gate is a few lines, and it closes the other half of the guarantee |

### What is deliberately not in v0.12.0

- **No application code.** If a change would alter a generated
  project's behaviour, it waits for `1.1`. `0.11.0` spent the
  breaking-change budget for the `0.x` line.
- **No backlog promotions.** See the bar above — and note that under
  semver a feature added *after* `1.0` is an ordinary minor bump, so
  nothing in the backlog gets cheaper by racing the freeze. The only
  changes that genuinely have to beat `1.0` are ones that would be
  **breaking** to make later; no backlog item qualifies.

### Notes from the release boundary

`v0.11.0` was the first tag where both sides of the comparison carried
`.copier-answers.yml`, so the `Copier Update Check` workflow had its
first meaningful run — `v0.10.0 → v0.11.0` applied cleanly. The update
*mechanism* is now proven across a real release. What is still unproven
is that the project on the far side of that update passes `just check`,
which is what the last two items above address.

---

## v1.0.0-rc.1 — Rehearsal

Cut a pre-release tag rather than a `0.13`. It costs nothing and buys
two things: the `v*` workflows run against a candidate that can still be
withdrawn, and the launch checklist below is executed once for real
before it counts.

Scope: **fixes only** — anything that fails the checklist becomes
`rc.2`. If the checklist passes clean, `1.0.0` is the same commit with a
version bump.

---

## v1.0 Launch Checklist

This is a one-time repository release gate, not a deployment runbook for
generated projects. Check every item on the release candidate commit before
deciding whether to release `v1.0.0`.

### Template contract

- [ ] Review the [API Stability & SemVer Policy](../guides/api-stability.md)
    against every change since `v0.9.0`; classify any required consumer
    action in `CHANGELOG.md`.
- [ ] Confirm `copier.yml` prompts, `scripts/copier_setup.py.jinja`, and
    generated metadata still produce a de-branded project.
- [ ] Generate a clean project from the release candidate and run its full
    gate. Pass `--vcs-ref=HEAD`: a local git template without it resolves
    to the latest *tag*, so the smoke test silently exercises the previous
    release instead of the candidate. `HEAD` includes uncommitted changes,
    so commit or stash first. Once the `v0.12.0` scaffold smoke job is in
    place this is a confirmation that CI is green, not a first run.

    ```bash
    git status --porcelain   # must be empty
    uvx copier copy --trust --vcs-ref=HEAD . ../quoinapi-v1-smoke
    cd ../quoinapi-v1-smoke
    uv sync --all-groups
    just check
    ```

- [ ] Confirm the generated project contains no QuoinAPI roadmap, release
    notes, contributor policy, or maintainer identity beyond the answers
    supplied to Copier.
- [ ] Verify the `copier update` path from the previous release *before*
    pushing the tag — the Copier Update Check workflow only runs on `v*`
    tags, so it reports after the release decision, not before it. Create
    the candidate tag locally, verify, then push. Both arguments must be
    real tags: the check compares the tag string against the `_commit`
    recorded in `.copier-answers.yml`, so `HEAD` or a branch name fails.

    ```bash
    git tag v1.0.0
    just verify-template-update v0.12.0 v1.0.0
    ```

- [ ] Confirm the generated project's `.copier-answers.yml` records the
    candidate tag after updating from `v0.12.0`.

### Behaviour and quality

- [ ] Run `just check` from a clean checkout and confirm 100% coverage.
- [ ] Run `just docb`; review the built site for broken links, navigation,
    API-reference rendering, and the current configuration tables.
- [ ] Start the local stack with `just dev`; verify `/health`, `/ready`,
    `/docs`, one authenticated request, and one denied request.
- [ ] Verify production configuration fails closed when the OAuth issuer,
    audience, or HTTPS JWKS URI is absent or invalid.
- [ ] Confirm a bare `ENV=production` (no `QUOIN_` prefix) fails fast
    rather than half-applying the production profile.
- [ ] Confirm `QUOIN_LOG_LEVEL=WARNING` visibly suppresses the access log
    in a `just dev` session.
- [ ] Confirm the problem-details contract hook and the commit-before-send
    test are present and green — they are the regression guards for the
    two high-severity bugs fixed in `0.11.0`.
- [ ] Review the public OpenAPI document and RFC 9457 error examples for
    intentional endpoint, response, and security-scheme changes only.

### Security and distribution

- [ ] Confirm GitHub Actions remain SHA-pinned and Dependabot covers Python,
    Docker, and GitHub Actions dependencies.
- [ ] Run the CVE scan — it is deliberately not part of `just check`, so
    nothing else in the release path runs it. Every advisory left in
    `audit_ignore` needs a current dated justification in the
    [Dependency Scanning](../guides/dependency-scanning.md) guide.

    ```bash
    just audit
    just audit-prod
    ```

- [ ] Confirm the Docker image builds, starts as the non-root `quoin` user,
    passes its health check, and disables docs and OpenAPI in production.
- [ ] Review `.env.example`, the Configuration guide, and the Security and
    Deployment guides together; every supported `QUOIN_*` setting must be
    documented without committing a credential.
- [ ] Confirm the security policy names `main` and the latest tag as the
    supported template versions and provides a private reporting route.

### Release decision

- [ ] Triage every open issue and pull request as release-blocking,
    explicitly deferred, or post-`v1.0.0` work.
- [ ] Confirm the **Known Correctness Issues** table below is empty.
- [ ] Record the final scope and all intentional deferrals in the
    `CHANGELOG.md` release section.
- [ ] Obtain maintainer approval that the template contract is stable enough
    for the `1.x` major-version promise.
- [ ] Follow the [Release Workflow](../guides/release-workflow.md) to bump,
    merge, tag, and publish the release.

Once complete, move this checklist to the release notes and replace the
milestone above with the next demand-backed milestone.

---

## Known Correctness Issues

A confirmed bug fits neither the launch checklist above (a one-time
release gate) nor the backlog below (demand-gated features) — without
a lane of its own it tends to get triaged as one or the other and
lost. This table is that lane: add a row when a review or an incident
confirms a correctness bug that isn't fixed in the same change, and
remove the row once the fix ships (credit it in `CHANGELOG.md`
instead). Empty is the steady state, not a gap in review.

| Status | Issue | Found |
| :----- | :---- | :---- |
| — | *(none currently open)* | — |

---

## Backlog

Documented now so they aren't lost. Promoted into a milestone only when
real demand surfaces — the bar is "a concrete user is blocked on this",
not "it would be nice to have".

| Status | Feature | Why deferred |
| :----- | :------ | :----------- |
| 💡 | **Idempotency keys (DB-backed store)** | Significant scope (replay logic, TTL semantics, key collision handling). Retry-safe idempotent verbs (`PUT`, `DELETE`) + client-supplied request IDs cover most cases. Build when actually needed. |
| 💡 | **OTel Metrics + `/metrics` endpoint** | RED metrics can be derived from the existing OTLP trace stream in the OTel Collector. Direct Prometheus scrape is duplicate plumbing unless a deployer specifically needs it. |
| 💡 | **Schemathesis contract testing in CI** | Pays off when external consumers lock against the schema. Adds CI minutes and flaky-test risk before that point. |
| 💡 | **Cursor-based pagination** | Premature unless a module hits million-row tables. Offset pagination is sufficient through `1.0`. |
| 💡 | **Background task worker** | Persistent async task queue for emails, webhooks, and long-running work; evaluate Arq (asyncio-native) vs Dramatiq (broker-agnostic). |
| 💡 | **Redis cache layer** | Shared Redis client and caching helpers; replaces DB-backed idempotency store at scale. |
| 💡 | **Multi-tenancy pattern** | Tenant-scoped query pattern with an example module. |
| 💡 | **Organizations + memberships + scopes** | Richer authorization model beyond `require_roles`. |
| 💡 | **API keys** | Hashed at rest, scoped, rotatable; for service-to-service callers. |
| 💡 | **Read-replica routing** | Repository-layer routing of reads to replicas. Pool sizing itself is already tunable via `QUOIN_DB_POOL_*`. |

Of these, the most plausible promotions in rough order of likelihood
are: background worker, API keys, Redis cache, multi-tenancy. Nothing
currently blocks a known user on any of them.

---

## After 1.0

Intent, not commitments — this section exists so that work deferred
*until* `1.0` isn't confused with work deferred *pending demand*.

- **Boring is the brand.** Strict semver, quarterly minors, security
  patches immediately, and every minor verifies `copier update` from
  the previous two tags rather than only the last one.
- **The update path is the differentiator.** The verify script, the
  scaffold smoke job, and `staying-current.md` are the assets worth
  investing in; a template nobody can upgrade is a snapshot.
- **The agentic workflow is a product feature.** Twelve skills, two
  subagents, and five hooks are more than any comparable template
  ships. Package them as a Claude Code plugin once the template
  surface is frozen, so they can version independently of the code.
- **Never extract a `quoin-core` package.** The
  [API stability guide](../guides/api-stability.md) states this as a
  non-goal; a template you can read end to end is the point.

---

## How to Contribute

1. Check if an issue already exists for the feature you want to work on.
2. Open a **Discussion** to align on approach before writing code.
3. Reference this roadmap item in your PR description.
4. Follow the [Contributing Guide](contributing.md) and ensure
   `just check` passes before requesting review.
