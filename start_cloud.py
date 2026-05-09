from __future__ import annotations

import os

from cloud_app import DEFAULT_HOST, DEFAULT_PORT, run_server


def main() -> None:
    host = os.getenv("HOST", DEFAULT_HOST)
    port = int(os.getenv("PORT", str(DEFAULT_PORT)))
    run_server(host=host, port=port)


if __name__ == "__main__":
    main()
