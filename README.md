# 🔗 Linkwala: Your Friendly Neighborhood Link Shortener

![Build Status](https://img.shields.io/badge/build-passing-brightgreen)

**Linkwala** is a powerful, self-hostable **URL shortening service** designed for **simplicity, speed, and scalability**.  
It provides a clean interface for creating short, memorable links, detailed analytics to track their performance, and a robust REST API for seamless integration.

Whether you're a developer needing a reliable link management tool, a marketer tracking campaign engagement, or simply someone who wants **full control of your data**, Linkwala delivers all essential features without the bloat.

---

## 🎥 Visual Demonstration

_Add screenshots, GIFs, or demo video links here._

---

## 🌟 Key Features

- 🚀 **Fast & Secure Redirection** – Optimized backend stack, HTTPS-only, SEO-friendly 301 redirects.  
- 🎨 **Custom Branded Links** – Personalize short links (e.g., `your.domain/my-campaign`).  
- 📊 **Detailed Click Analytics** – Track referrers, geo-location, devices, and trends.  
- 🔑 **Robust RESTful API** – Full CRUD operations for programmatic link management.  
- 📱 **QR Code Generation** – Instant high-resolution QR codes for any link.  
- 🔐 **API Key Management** – Secure, revocable API keys for granular control.  
- 🐳 **Self-Hostable & Docker-Ready** – One-command Docker deployment.  
- 🌐 **Link-in-Bio Pages** – Curated landing page for multiple links (perfect for social media).  

---

## ⚙️ Getting Started

You can run Linkwala in **two ways**:  
1. **Source Installation (manual setup)**  
2. **Docker Deployment (recommended for production)**  

### 📋 Prerequisites

- Git  
- Node.js v18+  
- Python v3.10+  
- Docker & Docker Compose (recommended)  
- PostgreSQL / Redis (depending on setup)  

---

## 🖥️ Installation from Source (Manual)

1. **Clone Repository**
   ```bash
   git clone https://github.com/hegdeshashank100/linkwala.git
   cd linkwala
   ```

2. **Backend Setup (FastAPI Example)**
   ```bash
   cd server
   python -m venv venv
   source venv/bin/activate   # Windows: venv\Scripts\activate
   pip install -r requirements.txt
   ```

3. **Frontend Setup (React Example)**
   ```bash
   cd ../client
   npm install
   ```

4. **Configure Environment**
   ```bash
   cp .env.example .env
   ```
   Edit `.env` with values for database, `SECRET_KEY`, and `BASE_URL`.

5. **Run Database Migrations**
   ```bash
   cd server
   alembic upgrade head
   ```

6. **Start Application**
   - Backend:  
     ```bash
     uvicorn main:app --reload --host 0.0.0.0 --port 8000
     ```  
   - Frontend:  
     ```bash
     cd client
     npm run dev
     ```  

   Access:  
   - Frontend → [http://localhost:3000](http://localhost:3000)  
   - Backend → [http://localhost:8000](http://localhost:8000)  

---

## 🐳 Deployment with Docker (Recommended)

1. **Clone Repository**
   ```bash
   git clone https://github.com/hegdeshashank100/linkwala.git
   cd linkwala
   ```

2. **Configure Docker Environment**
   ```bash
   cp .env.docker.example .env
   ```
   Update `SECRET_KEY`, `BASE_URL`, and database credentials.

3. **Launch with Docker Compose**
   ```bash
   docker-compose up -d
   ```

4. **Access Application**
   ```
   http://localhost:8080
   ```

---

## ⚙️ Configuration

Environment variables are managed via `.env` file:

| Variable         | Description | Required | Default |
|------------------|-------------|----------|---------|
| DATABASE_URL     | PostgreSQL connection string | ✅ Yes | - |
| REDIS_URL        | Redis connection string | ❌ No | - |
| SECRET_KEY       | Secure random string for tokens | ✅ Yes | `changeme` |
| BASE_URL         | Public base URL for instance | ✅ Yes | `http://localhost:8000` |
| API_KEY_LENGTH   | Length of generated API keys | ❌ No | 32 |
| SHORT_CODE_LENGTH| Default short code length | ❌ No | 7 |
| ALLOW_REGISTRATION | Enable/disable public signups | ❌ No | true |
| LOG_LEVEL        | Logging verbosity | ❌ No | INFO |
| CORS_ORIGINS     | Allowed CORS origins | ❌ No | * |
| RATE_LIMIT       | Requests per minute per IP | ❌ No | 200/minute |

---

## 📡 API Documentation

All API endpoints require **Bearer Token Authentication**.

**Example Header:**
```http
Authorization: Bearer your_secret_api_key_here
```

### Endpoints Overview

| Endpoint              | Method | Description |
|-----------------------|--------|-------------|
| `/api/v1/links`       | POST   | Create new short link |
| `/api/v1/links`       | GET    | List all links |
| `/api/v1/links/{id}`  | GET    | Get specific link + analytics |
| `/api/v1/links/{id}`  | PATCH  | Update link |
| `/api/v1/links/{id}`  | DELETE | Delete link |

**Example: Create a New Short Link**
```bash
curl -X POST 'http://localhost:8000/api/v1/links' -H 'Authorization: Bearer your_secret_api_key_here' -H 'Content-Type: application/json' -d '{
  "long_url": "https://github.com/hegdeshashank100/linkwala",
  "custom_backhalf": "linkwala-repo",
  "title": "Linkwala GitHub Repository"
}'
```

**Response (201 Created):**
```json
{
  "short_code": "linkwala-repo",
  "long_url": "https://github.com/hegdeshashank100/linkwala",
  "short_url": "http://localhost:8000/linkwala-repo",
  "title": "Linkwala GitHub Repository",
  "created_at": "2023-10-27T10:00:00Z",
  "clicks": 0
}
```

---

## 🤝 Contributing

We welcome contributions!

1. Fork the repo  
2. Create a branch: `git checkout -b feature/new-feature`  
3. Commit changes: `git commit -m "Add new feature"`  
4. Push branch: `git push origin feature/new-feature`  
5. Open a Pull Request  

- Follow the [Code of Conduct](CODE_OF_CONDUCT.md)  
- See [CONTRIBUTING.md](CONTRIBUTING.md) for details  

---

## 🐞 Issues & Feature Requests

- Report bugs via [GitHub Issues](https://github.com/hegdeshashank100/linkwala/issues)  
- Check existing issues before creating new ones  

---

## 📜 License

This project is licensed under the **MIT License**. See [LICENSE](LICENSE) for details.

---

## 🙏 Acknowledgments

Built with ❤️ on top of open-source tools and frameworks.  
See `requirements.txt` (backend) and `package.json` (frontend) for dependencies.

---

## 👨‍💻 Author

**Shashank Hegde**  
🔗 [GitHub Profile](https://github.com/hegdeshashank100)  
