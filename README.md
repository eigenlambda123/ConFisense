# ConFiSense

**Your intelligent financial analysis and decision-support tool.**  
ConFiSense helps you make sense of complex financial data with ease, providing AI-powered insights, interactive dashboards, and seamless export features.

---

## ✨ Features

- 🏠 **Simple Home Page** – Clean landing screen for quick access.
- 📊 **Interactive Dashboard** – Input your data with an intuitive interface.
- 📈 **Smart Outputs** – Visual insights presented clearly.
- 🤖 **AI-Powered Explanations** – Understand your results with contextual insights.
- 📤 **Easy Export** – Download reports and share them effortlessly.

---

## 📸 Demo Screenshots

Here’s a quick look at **ConFiSense in action**:  

| 🏠 Home Page | 📊 Dashboard (Inputs) | 📈 Dashboard (Outputs) |
|--------------|-----------------------|-------------------------|
| ![Home Page](demo_screenshots/home-page.png) | ![Dashboard with Inputs](demo_screenshots/dashboard-Winputs.png) | ![Dashboard with Outputs](demo_screenshots/dashboard-Woutputs.png) |

| 🤖 AI Explanation | 📤 Sample Export |
|-------------------|------------------|
| ![AI Explanation](demo_screenshots/dashboard-AIexplanation.png) | ![Sample Export](demo_screenshots/sample-export.png) |

---

### 1. Navigate to Project Root

```bash
cd ConFiSense
```

---

### 2. Set Up Python Virtual Environment

```bash
python -m venv venv
```

Then activate it:

- **On Windows**:

    ```bash
    venv\Scripts\activate
    ```

- **On Mac/Linux**:

    ```bash
    source venv/bin/activate
    ```


---

### 3. Install Backend Dependencies

```bash
pip install -r requirements.txt
```

---

### 4. Run the Backend (FastAPI)

```bash
uvicorn app.main:app --reload
```

> Backend will run at:  
> `http://127.0.0.1:8000`

---

### 5. Run the Frontend (Tailwind + HTML + JS)

```bash
cd app/frontend
npm install
npm run dev
```

This compiles Tailwind from `src/input.css` to `src/output.css` and watches for changes.

Then open this in your browser:

```
app/frontend/src/index.html
```

**S the frontend with a local server:**

- Go to `app/frontend` and then run:

```bash
npx serve .
```

> This will run at something like:  
> `http://localhost:3000`
