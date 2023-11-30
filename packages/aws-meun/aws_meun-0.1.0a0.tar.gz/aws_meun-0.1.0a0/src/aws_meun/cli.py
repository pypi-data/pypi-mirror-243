import argparse
import hashlib
import sys
from importlib.metadata import version

import httpx

PROG = "aws-meun"


def unsubscribe(email: str, client: httpx.Client) -> httpx.Response:
    data = {
        "Email": email,
        "Unsubscribed": "yes",
        "UnsubscribedReason": "I already get email from another account",
        "unsubscribedReasonOther": "",
        "useCaseMultiSelect": "",
        "formid": "34006",
        "munchkinId": "112-TZM-766",
        "formVid": "34006",
    }

    checksum_fields = [
        "Email",
    ]

    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:120.0) Gecko/20100101 Firefox/120.0",
    }

    checksum_str = "|".join([data.get(field, "") for field in checksum_fields])

    checksum = hashlib.sha256(checksum_str.encode("utf-8")).hexdigest()

    data["checksumFields"] = ",".join(checksum_fields)
    data["checksum"] = checksum

    r = client.post(
        "https://pages.awscloud.com/index.php/leadCapture/save2",
        data=data,
        headers=headers,
    )
    r.raise_for_status()
    return r


def main():
    parser = argparse.ArgumentParser(
        prog=PROG, description="Unsubscribe from AWS Marketing emails"
    )
    parser.add_argument("--version", action="version", version=version(PROG))
    parser.add_argument("email", nargs="*", help="email address to unsubscribe")

    args = parser.parse_args()

    if not args.email and not sys.stdin.isatty():
        emails = [email.rstrip() for email in sys.stdin.readlines()]
    else:
        emails = args.email

    with httpx.Client() as client:
        for email in emails:
            try:
                r = unsubscribe(email, client)
                print(f"Unsubscribed {email} (HTTP {r.status_code})")
            except httpx.HTTPStatusError as e:
                print(f"Failed to unsubscribe {email} (HTTP {e.response.status_code})")
