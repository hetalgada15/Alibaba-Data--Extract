# Alibaba Scraper Project

## Overview
The **Alibaba Scraper Project** is a scalable, distributed web scraper designed to crawl and scrape product data from Alibaba. It uses Scrapy for scraping, RabbitMQ for message queuing, AWS S3 for storage, and Torpy for IP rotation to ensure anonymity and efficiency.

## Features
- **Category-Specific Crawling**: Dynamically crawls category pages to retrieve product URLs.
- **Queue-Based Architecture**: Uses RabbitMQ to manage tasks via category-specific queues.
- **Parallel Scraping**: Scrapes product details in parallel for efficient data collection.
- **IP Rotation**: Integrates Tor for anonymity and avoiding bans.
- **Scalable Deployment**: Docker-based infrastructure for easy scaling.
- **Data Storage**: Saves scraped data to AWS S3 in a structured format.

---

## Project Structure
```plaintext
alibaba_scraper/
├── alibaba_scraper/          # Core Scrapy project
│   ├── __init__.py
│   ├── items.py              # Data models for scraped items
│   ├── middlewares.py        # Scrapy middlewares, including TorProxyMiddleware
│   ├── pipelines.py          # Processes and stores scraped items
│   ├── settings.py           # Global settings for Scrapy
│   ├── spiders/              # Spiders for crawling and scraping
│   │   ├── __init__.py
│   │   ├── category_crawler.py  # Crawl category pages and push URLs to queues
│   │   ├── product_scraper.py   # Scrape product details and upload to S3
├── utils/                    # Utility modules
│   ├── __init__.py
│   ├── rabbitmq_helper.py    # RabbitMQ helper functions
│   ├── s3_helper.py          # AWS S3 integration
│   ├── tor_proxy_helper.py   # Tor proxy initialization and rotation
├── config/                   # Configuration files
│   ├── config.json           # Category configurations
├── docker/                   # Docker-related files
│   ├── Dockerfile            # Dockerfile for containerizing spiders
│   ├── docker-compose.yml    # Docker Compose configuration
├── requirements.txt          # Python dependencies
├── README.md                 # Documentation
└── .gitignore                # Git ignore rules
```

---

## Setup

### Prerequisites
1. **Python 3.8+** installed.
2. **Docker and Docker Compose** installed.
3. An **AWS account** with an S3 bucket configured.
4. RabbitMQ (via Docker Compose).

### Installation
1. Clone the repository:
   ```bash
   git clone https://github.com/your-username/alibaba-scraper.git
   cd alibaba-scraper
   ```

2. Set up a Python virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
   
---

## Usage

### 1. **Edit `config.json`**
Add categories and URLs for crawling:
```json
{
    "categories": [
        {
            "name": "electronics",
            "url": "https://example.com/electronics"
        },
        {
            "name": "fashion",
            "url": "https://example.com/fashion"
        }
    ]
}
```

### 2. **Run the Crawler**
Start the category crawler to fetch product URLs:
```bash
scrapy crawl category_crawler
```

### 3. **Run the Scraper**
Start the product scraper to process URLs and store data in S3:
```bash
scrapy crawl product_scraper
```

### 4. **Verify Data**
Check your S3 bucket to ensure scraped data is uploaded.

---

## Testing

### 1. **Test Tor Integration**
Verify Tor IP rotation:
```bash
python utils/tor_proxy_helper.py
```

---

## Deployment

1. Generate `docker-compose.yml` dynamically for all categories:
   ```bash
   python generate_docker_compose.py
   ```

2. Start all services:
   ```bash
   docker-compose up --build
   ```

---

## Git Branching Strategy

The project follows a structured Git branching strategy to ensure smooth collaboration and maintain code quality. The current branches are:

- **`origin/main`**: The production-ready branch containing stable and deployable code.
- **`develop`**: The integration branch where all features are merged and tested before being promoted to `main`.
- **Feature branches**: For individual tasks or features, create branches from `develop`.

### Workflow:
1. **Create a feature branch**:
   ```bash
   git checkout -b feature/your-feature develop
   ```
2. **Work on the feature and commit changes**:
   ```bash
   git add .
   git commit -m "Implement feature X"
   ```
3. **Push the feature branch**:
   ```bash
   git push origin feature/your-feature
   ```
4. **Create a pull request to `develop`**.
5. **Merge into `develop`** once approved.
6. Periodically merge `develop` into `main` for stable releases.

---

## License
This project is licensed under the [MIT License](LICENSE).

---

