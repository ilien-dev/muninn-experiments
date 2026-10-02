#!/usr/bin/env python3
"""Loop 12 development scenarios: fifteen replacements a coding project might make.

Written by hand, from the kinds of choice this repository and its dependencies actually
involve, and deliberately *not* drawn from any held-out set. They exist so a rule can be
designed on them and then tested once, elsewhere.
"""
import json
S = [
 ("d12-pool",  "the connection pooler",              "PgBouncer",  "Supavisor"),
 ("d12-queue", "the background job queue",           "Sidekiq",    "Oban"),
 ("d12-http",  "the HTTP client in the service",     "reqwest",    "hyper"),
 ("d12-fmt",   "the log format",                     "logfmt",     "JSON lines"),
 ("d12-ci",    "where CI runs",                      "CircleCI",   "GitHub Actions"),
 ("d12-store", "the object store",                   "MinIO",      "Cloudflare R2"),
 ("d12-lint",  "the linter for the frontend",        "ESLint",     "Biome"),
 ("d12-orm",   "the database layer",                 "Diesel",     "SQLx"),
 ("d12-auth",  "how sessions are signed",            "HS256",      "EdDSA"),
 ("d12-test",  "the end-to-end test runner",         "Cypress",    "Playwright"),
 ("d12-pkg",   "the package manager",                "npm",        "pnpm"),
 ("d12-tpl",   "the template engine",                "Handlebars", "Tera"),
 ("d12-cache", "the cache eviction policy",          "LFU",        "LRU"),
 ("d12-proto", "the wire protocol between services", "REST",       "gRPC"),
 ("d12-obs",   "how traces are exported",            "Jaeger",     "OpenTelemetry Collector"),
]
STYLES = ["terse", "chatty", "Spanish"]
out = [{"key": f"{k}#{st}", "topic": t, "old": o, "new": n, "style": st}
       for (k, t, o, n) in S for st in STYLES]
print(json.dumps(out, indent=1))
