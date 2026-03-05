#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PY_SCRIPT="${SCRIPT_DIR}/gitlab_ops.py"

if [[ ! -f "${PY_SCRIPT}" ]]; then
  echo "ERROR: missing ${PY_SCRIPT}" >&2
  exit 1
fi

cmd="${1:-help}"
if [[ $# -gt 0 ]]; then
  shift
fi

case "${cmd}" in
  help|-h|--help)
    exec python3 "${PY_SCRIPT}" --help
    ;;
  init|init-config)
    exec python3 "${PY_SCRIPT}" init-config "$@"
    ;;
  ls|list|list-projects)
    exec python3 "${PY_SCRIPT}" list-projects "$@"
    ;;
  lsj|list-json)
    exec python3 "${PY_SCRIPT}" list-projects --json "$@"
    ;;
  url|get-url|get-clone-url)
    exec python3 "${PY_SCRIPT}" get-clone-url "$@"
    ;;
  clone)
    exec python3 "${PY_SCRIPT}" clone "$@"
    ;;
  cg|create-group)
    exec python3 "${PY_SCRIPT}" create-group "$@"
    ;;
  cp|create-project)
    exec python3 "${PY_SCRIPT}" create-project "$@"
    ;;
  push)
    exec python3 "${PY_SCRIPT}" push "$@"
    ;;
  wf|workflow)
    exec python3 "${PY_SCRIPT}" workflow "$@"
    ;;
  *)
    echo "ERROR: unsupported alias '${cmd}'" >&2
    echo "Aliases: help, init, ls, lsj, url, clone, cg, cp, push, wf" >&2
    exit 2
    ;;
esac
