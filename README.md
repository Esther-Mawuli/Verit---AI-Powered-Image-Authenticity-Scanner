# Verit: AI-Powered Scam & Misinformation Scanner

## Overview

Verit is an AI-powered image authenticity and scam detection platform designed to help individuals and organizations verify images, detect fraudulent listings, and combat misinformation. Leveraging advanced forensic analysis, reverse image search, and cloud-based AI, Verit provides instant risk scoring and actionable insights for uploaded images.

---

## Multi-Cloud Deployment

Verit is designed for hybrid cloud deployment using:
- **Google Cloud Vision API:** Set up a Google Cloud Project, enable the Vision API, and obtain an API key for advanced image analysis.
- **AWS ECS with EBS Volume:** The backend is containerized and deployed on AWS Elastic Container Service (ECS), with persistent storage managed via Elastic Block Store (EBS).

This approach ensures high availability, scalability, and resilience, allowing organizations to leverage both Google Cloud's AI capabilities and AWS's robust infrastructure.

---

## Features

- **Reverse Image Search:** Instantly check if an image appears elsewhere online.
- **Scam Pattern Detection:** Identify images reused in scams, fake listings, and fraudulent ads.
- **Domain Analysis:** Detect suspicious domains and scam indicators.
- **Image Metadata Extraction:** View technical details about uploaded images.
- **Risk Scoring:** Get a clear, actionable scam probability score.
- **Hybrid Cloud Deployment:** Easily deploy using Google Cloud Vision API and AWS EC2 with EBS.

---

## Real-World Problems Solved

### Financial & Classifieds Scam Prevention
- Prevents monetary loss from fake rental listings, job offers, and online store scams.

### Political Misinformation & Electoral Integrity
- Supports journalists, election officials, and NGOs in verifying viral images and videos during elections.

### Public Health Misinformation
- Enables health workers and NGOs to debunk fake images and messages about diseases and cures.

---

## Importance for Companies

- **Fraud Reduction:** Companies in e-commerce, real estate, and recruitment can reduce losses and protect their customers by integrating Verit into their platforms.
- **Brand Trust:** By proactively fighting scams and misinformation, organizations build trust and credibility with their users.
- **Regulatory Compliance:** Verit helps companies meet growing regulatory requirements for content authenticity and user protection.
- **Scalable Security:** Hybrid cloud deployment ensures Verit can scale with business needs and remain resilient against attacks.

---

## Real-World Applications

- **E-commerce Platforms:** Automatically scan product images for scam patterns before listings go live.
- **Real Estate Agencies:** Verify property photos to prevent fake rental and sale listings.
- **Newsrooms & Fact-Checkers:** Rapidly analyze viral images and videos for authenticity.
- **Government & NGOs:** Monitor and counteract misinformation during elections and health campaigns.
- **Individual Users:** Empower anyone to check images before sending money or sharing content.

---

## Why Africa Needs Verit

Africa faces unique challenges with online fraud and misinformation due to high mobile adoption, rapid digital growth, and frequent use of social platforms for commerce and communication. Verit’s mobile-first, lightweight design and support for local languages make it especially valuable for African users.

**Recommended Niche:**  
Start with Financial Scam Prevention for immediate impact and revenue, then expand to political and health misinformation.

---

## Industry Context

Verit joins a global movement for content provenance and deepfake detection, alongside efforts by Google, Microsoft, Adobe, Meta, and leading startups. While the problem is vast and evolving, Verit’s focused approach—starting with financial scam prevention—offers a practical, high-impact solution for Africa and beyond.

---

## Getting Started

### Clone the repository

```bash
git clone https://github.com/yourusername/verit-scanner.git
```

### Deploy on your preferred cloud

- Set up a Google Cloud Project, enable the Vision API, and obtain an API key.
- Deploy the backend on AWS ECS with EBS volume for persistent storage.

### Run locally

```bash
pip install -r requirements.txt
python app.py
```
Visit [http://127.0.0.1:5000](http://127.0.0.1:5000) in your browser.

---

## Contributing

We welcome contributions from developers, researchers, and organizations passionate about fighting fraud and misinformation.  
See [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

---

## License

MIT License

---

**Verit: Protecting Truth, Preventing Fraud, Empowering Africa.**