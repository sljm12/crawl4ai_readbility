import argparse
import asyncio
import io
import json
import os
import sys

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding="utf-8", errors="replace")

from crawler import crawl_article, crawl_article_full


def main():
    parser = argparse.ArgumentParser(
        description="Crawl a URL and extract readable article content as Markdown."
    )
    parser.add_argument("url", help="URL of the article to crawl")
    fmt = parser.add_mutually_exclusive_group()
    fmt.add_argument(
        "--json",
        "-j",
        action="store_true",
        dest="json_output",
        help="Output the full JSON response",
    )
    fmt.add_argument(
        "--markdown",
        "-m",
        action="store_true",
        dest="markdown_only",
        help="Output Markdown only (default)",
    )
    parser.add_argument(
        "--output",
        "-o",
        help="Write output to file instead of stdout",
    )

    args = parser.parse_args()

    is_json = args.json_output

    async def run():
        if is_json:
            result = await crawl_article_full(args.url)
            text = json.dumps(result, indent=2, ensure_ascii=False)
        else:
            text = await crawl_article(args.url)

        if args.output:
            with open(args.output, "w", encoding="utf-8") as f:
                f.write(text)
                f.write("\n")
        else:
            print(text)

    try:
        asyncio.run(run())
    except RuntimeError as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"Unexpected error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
