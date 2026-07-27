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

The public API contract is locked — the pagination envelope, soft
delete, and deprecation mechanism shipped in `0.9.0`, and the API
stability and semver policy is now published (see the
[CHANGELOG](changelog.md)). The one remaining milestone below carries
QuoinAPI to template completeness; it is independently shippable, gated
by the launch checklist, `just check`, and the existing pre-push hook. It
may become `v1.0.0`.

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
[guide](docs/guides/optimistic-concurrency.md) rather than a deletion —
the pattern is worth documenting even though the code isn't worth
shipping.

---

## v0.10.0 — Template Completeness

The milestone that makes QuoinAPI a self-contained, production-ready
Copier template with a stability guarantee. JWT validation and RBAC remain
built-in: an API gateway complements service-level authorization rather
than replacing it. Whether this becomes `v1.0.0` will be decided once the
launch gate below is complete.

| Status | Feature |
| :----- | :------ |
| ✅ | **API stability + semver policy** — Public guarantee on what changes are breaking and how deprecations land |
| 📋 | **Launch checklist** — Every preceding phase verified complete (see [v1.0 Launch Checklist](#v10-launch-checklist)) |

---

## v1.0 Launch Checklist

This is a one-time repository release gate, not a deployment runbook for
generated projects. Check every item on the release candidate commit before
deciding whether to release `v1.0.0`.

### Template contract

- [ ] Review the [API Stability & SemVer Policy](docs/guides/api-stability.md)
    against every change since `v0.9.0`; classify any required consumer
    action in `CHANGELOG.md`.
- [ ] Confirm `copier.yml` prompts, `scripts/copier_setup.py.jinja`, and
    generated metadata still produce a de-branded project.
- [ ] Generate a clean project from the release candidate and run its full
    gate. Commit or stash everything first: Copier generates from the
    working tree, so a dirty checkout silently smoke-tests uncommitted
    changes instead of the release candidate.

    ```bash
    git status --porcelain   # must be empty
    uvx copier copy --trust . ../quoinapi-v1-smoke
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
    just verify-template-update v0.9.0 v1.0.0
    ```

### Behaviour and quality

- [ ] Run `just check` from a clean checkout and confirm 100% coverage.
- [ ] Run `just docb`; review the built site for broken links, navigation,
    API-reference rendering, and the current configuration tables.
- [ ] Start the local stack with `just dev`; verify `/health`, `/ready`,
    `/docs`, one authenticated request, and one denied request.
- [ ] Verify production configuration fails closed when the OAuth issuer,
    audience, or HTTPS JWKS URI is absent or invalid.
- [ ] Review the public OpenAPI document and RFC 9457 error examples for
    intentional endpoint, response, and security-scheme changes only.

### Security and distribution

- [ ] Confirm GitHub Actions remain SHA-pinned and Dependabot covers Python,
    Docker, and GitHub Actions dependencies.
- [ ] Run the CVE scan — it is deliberately not part of `just check`, so
    nothing else in the release path runs it. Every advisory left in
    `audit_ignore` needs a current dated justification in the
    [Dependency Scanning](docs/guides/dependency-scanning.md) guide.

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
- [ ] Record the final scope and all intentional deferrals in the
    `CHANGELOG.md` release section.
- [ ] Obtain maintainer approval that the template contract is stable enough
    for the `1.x` major-version promise.
- [ ] Follow the [Release Workflow](docs/guides/release-workflow.md) to bump,
    merge, tag, and publish the release.

Once complete, move this checklist to the release notes and replace the
`v0.10.0` milestone with the next demand-backed milestone.

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

---

## How to Contribute

1. Check if an issue already exists for the feature you want to work on.
2. Open a **Discussion** to align on approach before writing code.
3. Reference this roadmap item in your PR description.
4. Follow the [Contributing Guide](contributing.md) and ensure
   `just check` passes before requesting review.
