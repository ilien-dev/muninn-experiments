#!/usr/bin/env bash
# agentmemory-inject: the agentmemory arm with AGENTMEMORY_INJECT_CONTEXT=true (the documented
# switch), pre-registered as the secondary agentmemory arm. Same pin, same subcommands.
export AGENTMEMORY_ARM_INJECT=1
exec "$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)/../agentmemory/arm.sh" "$@"
