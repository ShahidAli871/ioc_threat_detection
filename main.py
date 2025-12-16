import argparse
from pipelines.phishing_pipeline import run_sync


def main():
    parser = argparse.ArgumentParser(description="Run phishing detection on .eml files")
    parser.add_argument("eml", help="Path to .eml file to analyze")
    args = parser.parse_args()

    report = run_sync(args.eml)
    print(f"Report written to: {report.get('output_path')}")


if __name__ == "__main__":
    main()
