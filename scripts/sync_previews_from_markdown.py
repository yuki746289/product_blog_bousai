# Created: 2026-09-09 14:52 JST
# Updated: 2026-09-09 15:14 JST
"""Compatibility wrapper around the preview synchronizer.

B003/B008/B010/B058 were omitted from the original synchronization set even
though Markdown is the editorial source of truth. Keep the reviewed core
unchanged and extend its target set here so CI, local deploy and production
deploy all use the same correction without duplicating the large renderer
implementation.
"""

from __future__ import annotations

try:  # package import used by tests
    from . import sync_previews_core as _core
    from .sync_previews_core import *  # noqa: F401,F403
except ImportError:  # direct script execution: python scripts/...
    import sync_previews_core as _core
    from sync_previews_core import *  # type: ignore # noqa: F401,F403

EXTRA_SYNC_ARTICLE_IDS = {"B003", "B008", "B010", "B058"}
_core.SYNC_ARTICLE_IDS.update(EXTRA_SYNC_ARTICLE_IDS)
SYNC_ARTICLE_IDS = _core.SYNC_ARTICLE_IDS


def main() -> int:
    return _core.main()


if __name__ == "__main__":
    raise SystemExit(main())