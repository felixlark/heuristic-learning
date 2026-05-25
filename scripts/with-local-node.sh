#!/usr/bin/env bash
set -euo pipefail

# Codex Desktop exposes its own signed Node binary ahead of the user's shell
# PATH. On macOS, that binary cannot dlopen Rollup's third-party native
# optional dependency because of library-validation Team ID checks. Prefer the
# local developer Node when it exists; other environments keep their PATH.
if [[ "$(uname -s)" == "Darwin" && -x /opt/homebrew/bin/node ]]; then
  case "$(command -v node 2>/dev/null || true)" in
    /Applications/Codex.app/*)
      export PATH="/opt/homebrew/bin:$PATH"
      ;;
  esac
fi

exec "$@"
