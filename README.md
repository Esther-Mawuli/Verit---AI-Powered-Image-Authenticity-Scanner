# Verit: AI-Powered Scam & Misinformation Scanner

## Overview

**Verit** is an AI-powered image authenticity and scam detection platform designed to help individuals and organizations verify images, detect fraudulent listings, and combat misinformation. Leveraging advanced forensic analysis, reverse image search, and cloud-based AI, Verit provides instant risk scoring and actionable insights for uploaded images.

---

## Features

- **Reverse Image Search:** Instantly check if an image appears elsewhere online.
- **Scam Pattern Detection:** Identify images reused in scams, fake listings, and fraudulent ads.
- **Domain Analysis:** Detect suspicious domains and scam indicators.
- **Image Metadata Extraction:** View technical details about uploaded images.
- **Risk Scoring:** Get a clear, actionable scam probability score.
- **Multi-Cloud Deployment:** Easily deploy on AWS, Azure, or Google Cloud using Terraform and Docker.

---

## Real-World Problems Solved

### Financial & Classifieds Scam Prevention
- Prevents monetary loss from fake rental listings, job offers, and online store scams.

### Political Misinformation & Electoral Integrity
- Supports journalists, election officials, and NGOs in verifying viral images and videos during elections.

### Public Health Misinformation
- Enables health workers and NGOs to debunk fake images and messages about diseases and cures.

---

## Why Africa Needs Verit

Africa faces unique challenges with online fraud and misinformation due to high mobile adoption, rapid digital growth, and frequent use of social platforms for commerce and communication. Verit’s mobile-first, lightweight design and support for local languages make it especially valuable for African users.

**Recommended Niche:**  
Start with Financial Scam Prevention for immediate impact and revenue, then expand to political and health misinformation.

---

## Multi-Cloud Deployment

Verit is designed for flexible deployment across AWS, Azure, and Google Cloud.  
- **AWS:** Use the provided `main.tf` Terraform script for EC2 deployment.
- **Azure/GCP:** Docker and Kubernetes support coming soon.

---

## Getting Started

### 1. Clone the Repository

```bash
git clone https://github.com/yourusername/verit-scanner.git
cd verit-scanner
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Run Locally

```bash
python app.py
```
Visit [http://127.0.0.1:5000](http://127.0.0.1:5000) in your browser.

### 4. Deploy on AWS (Terraform)

- Edit `main.tf` with your AWS credentials.
- Run:
  ```bash
  terraform init
  terraform apply
  ```
- Find your app’s public IP in the Terraform output.

---

## Project Structure

```
ScamScanner/
│
├── app.py
├── requirements.txt
├── main.tf
├── templates/
│   └── index.html
```

---

## Contributing

We welcome contributions from developers, researchers, and organizations passionate about fighting fraud and misinformation.  
See [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

---

## License

MIT License

---

**Verit: Protecting Truth, Preventing Fraud, Empowering Africa.**