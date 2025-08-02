# ConFiSense

## Project Setup Instructions (Frontend + Backend)

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

**Optional (recommended):** Serve the frontend with a local server:

```bash
npx serve src
```

> This will run at something like:  
> `http://localhost:3000`
