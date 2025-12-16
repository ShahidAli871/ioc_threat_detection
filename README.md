# ioc_threat_detection

Will I be able to do anything in this. I am not sure but i have to try something 

This repository implements a minimal phishing detection pipeline: parse .eml, extract IOCs, query threat intelligence (stubbed), score risk, and write a JSON report.

Quick start
-----------

1. Create a Python virtualenv and install requirements:

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

2. Generate a sample email (optional):

```bash
python tests/generate_test_email.py
```

3. Run the pipeline:

```bash
python main.py tests/sample_emails/sample.eml
```

Report will be written to `data/output/` as JSON.

Next steps
----------
- Add real API integrations in `modules/threat_intel.py` (VirusTotal, AbuseIPDB, URLhaus).
- Improve IOC extraction and whitelisting in `modules/ioc_extractor.py`.
- Add unit tests and CI.
