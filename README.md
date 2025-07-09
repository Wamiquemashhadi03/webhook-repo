
## 📦 webhook-repo (Backend Flask API)

This is the **backend server** that listens for GitHub Webhook events (push, pull request, and merge), processes them, and stores the relevant event data in MongoDB.

### 🔗 Live API Endpoint

* ["Returns the latest GitHub events in JSON format."](https://webhook-repo-three.vercel.app/events)
  

---

### 🧠 Tech Stack

* Python 3
* Flask
* PyMongo (MongoDB)
* dotenv
* CORS
* Vercel (Serverless Deployment)

---

### 🔄 Webhook Flow

1. GitHub sends a `POST` request to `/webhook` on any new push or pull request.
2. Flask backend parses the payload and extracts:

   * Author name
   * Event type (`PUSH`, `PULL_REQUEST`, or `MERGE`)
   * Branches
   * Timestamp
3. Data is stored in MongoDB Atlas.
4. `/events` route provides this data in JSON format.

---

### 🖥️ Frontend Link

View this data visually here:

* 🔗 [github-webhooks-ui (Frontend)](https://github.com/Wamiquemashhadi03/github-webhooks-ui)
* 🌐 [Live UI Deployment](https://github-webhooks-ui.vercel.app)

---

### 📁 Routes

| Method | Route      | Description                    |
| ------ | ---------- | ------------------------------ |
| GET    | `/`        | Health check                   |
| POST   | `/webhook` | Accepts GitHub webhook payload |
| GET    | `/events`  | Returns latest events as JSON  |

---

### ⚙️ Run Locally

```bash
git clone https://github.com/Wamiquemashhadi03/webhook-repo.git
cd webhook-repo
python -m venv venv
source venv/bin/activate  # or venv\Scripts\activate on Windows
pip install -r requirements.txt

# Create .env file
MONGO_URI=your_mongodb_uri_here

# Run
python app.py
```

---

### 📜 License

MIT License

---

### 👨‍💻 Author

Made by [Wamique Mashhadi](https://github.com/Wamiquemashhadi03)
