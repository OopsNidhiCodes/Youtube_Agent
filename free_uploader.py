#!/usr/bin/env python3
"""
Free uploader utility

Provides zero-cost delivery by uploading generated files to transfer.sh
and returning a public download URL. No accounts, no API keys.
"""

import os
import mimetypes
import requests
from pathlib import Path
from logger import get_logger

logger = get_logger(__name__)

TRANSFER_SH_BASE = "https://transfer.sh"

def upload_to_transfer_sh(file_path: str, custom_name: str | None = None) -> str | None:
    """Upload a file to transfer.sh and return a public URL.

    Args:
        file_path: Local path to the file to upload.
        custom_name: Optional custom name to use in the URL.

    Returns:
        The public download URL, or None if upload failed.
    """
    try:
        path = Path(file_path)
        if not path.exists() or not path.is_file():
            logger.error(f"File not found for upload: {file_path}")
            return None

        name = custom_name if custom_name else path.name
        url = f"{TRANSFER_SH_BASE}/{name}"

        mime_type, _ = mimetypes.guess_type(str(path))
        headers = {"Content-Type": mime_type or "application/octet-stream"}

        logger.info(f"Uploading to transfer.sh: {name}")
        with open(path, "rb") as f:
            resp = requests.put(url, data=f, headers=headers, timeout=300)
            if resp.status_code in (200, 201):
                public_url = resp.text.strip()
                logger.info(f"Uploaded successfully: {public_url}")
                return public_url
            else:
                logger.error(f"Upload failed ({resp.status_code}): {resp.text[:200]}")
                return None

    except Exception as e:
        logger.error(f"Error uploading to transfer.sh: {e}")
        return None