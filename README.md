# 🧠 CareerMind AI

> **Job Market Intelligence powered by RAG + LangChain + Gemini**

CareerMind AI is a Retrieval-Augmented Generation (RAG) project that analyzes a collection of technical job descriptions to identify the skills employers ask for and extract salary/CTC patterns from the retrieved job-market data.

Instead of asking an LLM to guess what a role requires, CareerMind AI uses retrieved job descriptions as the primary evidence source.

---

## ✨ What CareerMind AI Does

Given a job role such as:

```text
Machine Learning Engineer
```

CareerMind AI can analyze retrieved job descriptions and produce:

- 🛠️ Important technical skills
- 📚 Tools and frameworks
- 🗄️ Databases and cloud technologies
- 🤝 Soft skills and other requirements
- 📊 Skill importance percentage
- 🎯 Skill priority
- 🔎 Evidence count across retrieved JDs
- 💰 Average CTC when sufficient salary data exists
- 📉 Minimum CTC
- 📈 Maximum CTC
- 📄 Number of job descriptions containing salary information
- 📝 A concise market summary

The LLM is explicitly instructed to avoid inventing unsupported skills or salary figures.

---

## 🏗️ Architecture

```text
                ┌──────────────────────┐
                │   Job Description    │
                │        PDFs           │
                └──────────┬───────────┘
                           │
                           ▼
                ┌──────────────────────┐
                │    PyPDFLoader       │
                └──────────┬───────────┘
                           │
                           ▼
                ┌──────────────────────┐
                │ RecursiveCharacter   │
                │     TextSplitter     │
                │  chunk=800 / overlap │
                │        =100          │
                └──────────┬───────────┘
                           │
                           ▼
                ┌──────────────────────┐
                │ Google Gemini        │
                │    Embeddings        │
                └──────────┬───────────┘
                           │
                           ▼
                ┌──────────────────────┐
                │      ChromaDB        │
                │    Vector Store      │
                └──────────┬───────────┘
                           │
                 Semantic Retrieval
                           │
                           ▼
                ┌──────────────────────┐
                │ PromptTemplate       │
                │ Job-role + Context   │
                └──────────┬───────────┘
                           │
                           ▼
                ┌──────────────────────┐
                │ Gemini Chat Model    │
                │   Market Analysis    │
                └──────────┬───────────┘
                           │
                           ▼
                ┌──────────────────────┐
                │ Structured JSON      │
                │ Skills + Salary      │
                └──────────────────────┘
```

---

## 🧰 Tech Stack

| Component | Technology |
|---|---|
| Language | Python |
| LLM | Google Gemini |
| Embeddings | `gemini-embedding-001` |
| RAG Framework | LangChain |
| Prompting | LangChain `PromptTemplate` |
| PDF Loading | `PyPDFLoader` |
| Text Splitting | `RecursiveCharacterTextSplitter` |
| Vector Database | Chroma |
| Environment Variables | `python-dotenv` |

---

## 📁 Suggested Project Structure

```text
CareerMind-AI/
│
├── main.py
├── docs.py
├── requirements.txt
├── README.md
├── .gitignore
├── .env.example
│
├── jd_dataset/
│   └── tech_jds_149.pdf
│
└── Vector-db/
    └── # Generated Chroma files
```

> Keep the actual `.env` file and generated vector database out of Git.

---

## ⚙️ How It Works

### 1. Load the job-description dataset

`docs.py` loads the PDF dataset using `PyPDFLoader`.

### 2. Split the documents

The current implementation uses:

```text
chunk_size = 800
chunk_overlap = 100
```

This converts the source PDF into smaller chunks suitable for embedding and retrieval.

### 3. Generate embeddings

The project uses Google's:

```text
gemini-embedding-001
```

to convert document chunks into vectors.

### 4. Store vectors in Chroma

The embeddings are stored in a persistent Chroma vector database.

The current collection name is:

```text
fin_splitter
```

### 5. Batch embedding

The current indexing script processes:

```text
BATCH_SIZE = 20
```

and waits between batches to reduce the chance of hitting API limits.

### 6. Analyze retrieved job descriptions

`main.py` defines a LangChain `PromptTemplate` that receives:

```text
job_role
context
```

The prompt instructs the model to use retrieved job descriptions as the primary evidence.

### 7. Generate structured analysis

The expected response contains:

```json
{
  "job_role": "...",
  "skills": [],
  "salary_analysis": {},
  "summary": "..."
}
```

---

## 🔐 Environment Variables

Create a local `.env` file:

```env
GOOGLE_API_KEY=your_google_api_key
```

Do **not** commit your real API key.

A template is provided in:

```text
.env.example
```

---

## 🚀 Installation

### 1. Clone the repository

```bash
git clone https://github.com/akashgoswami139/CareerMind-AI.git
cd CareerMind-AI
```

### 2. Create a virtual environment

Windows PowerShell:

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
```

Windows CMD:

```cmd
python -m venv .venv
.venv\Scripts\activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure environment variables

Create `.env`:

```env
GOOGLE_API_KEY=your_google_api_key
```

### 5. Build the vector database

Make sure the dataset exists at:

```text
jd_dataset/tech_jds_149.pdf
```

Then run:

```bash
python docs.py
```

This creates the persistent Chroma database under:

```text
Vector-db/
```

---

## 🧪 Current Prompt Logic

CareerMind AI uses evidence-based rules for skill importance:

| Percentage | Priority |
|---:|---|
| 75–100% | Critical |
| 50–74% | Important |
| 25–49% | Useful |
| 0–24% | Optional |

The prompt asks the model to base percentages on the retrieved job descriptions rather than simply guessing them.

Salary analysis is only produced when the retrieved data contains enough salary information.

---

## ⚠️ Important Limitations

- The quality of the analysis depends on the quality and coverage of the JD dataset.
- Salary results are dataset-derived estimates, not guaranteed market salaries.
- Missing salary information can result in insufficient salary analysis.
- Skill percentages depend on the retrieved documents and retrieval quality.
- API quotas/rate limits can affect embedding and generation.
- The current repository is a learning/project implementation rather than a production-grade job-market analytics platform.

---

## 🔧 Recommended Next Improvements

These are useful next steps if you want to take CareerMind AI from a basic RAG implementation toward a stronger portfolio project:

### 1. Add a real retriever

Connect Chroma to a proper retriever:

```python
retriever = vector_db.as_retriever(
    search_kwargs={"k": 10}
)
```

Then retrieve only the most relevant JDs for the requested role.

### 2. Add a LangChain retrieval chain

Build a complete flow:

```text
Job Role
   ↓
Retriever
   ↓
Relevant JDs
   ↓
Prompt
   ↓
Gemini
   ↓
Structured Output
```

### 3. Use structured output

Instead of relying only on prompt formatting, define a Pydantic schema and use LangChain structured output.

### 4. Add metadata filtering

Store metadata such as:

```text
role
company
location
experience
salary
source
```

This can enable more targeted retrieval.

### 5. Add evaluation

Create a small evaluation dataset containing:

```text
job_role
expected_skills
expected_salary_range
```

Then evaluate retrieval and generation quality.

### 6. Add a UI

A Streamlit interface could provide:

```text
Enter Job Role
      ↓
Retrieve JDs
      ↓
Analyze Market
      ↓
Skills Dashboard
      ↓
Salary Dashboard
```

---

## 📌 Example Use Case

Input:

```text
Data Scientist
```

Possible output structure:

```json
{
  "job_role": "Data Scientist",
  "skills": [
    {
      "skill": "Python",
      "importance_percentage": 91,
      "priority": "Critical",
      "evidence_count": 45
    }
  ],
  "salary_analysis": {
    "average_ctc_lpa": 7.2,
    "minimum_ctc_lpa": 4.0,
    "maximum_ctc_lpa": 12.0,
    "salary_data_count": 25,
    "currency": "INR",
    "unit": "LPA",
    "confidence": "Medium"
  },
  "summary": "..."
}
```

> The numbers above are illustrative. CareerMind AI should calculate values from the retrieved dataset rather than copying example values.

---

## 🎯 Project Goal

CareerMind AI is designed to demonstrate practical understanding of:

- Retrieval-Augmented Generation
- Document ingestion
- Text chunking
- Embeddings
- Vector databases
- Semantic retrieval
- Prompt engineering
- Structured LLM output
- Evidence-based LLM analysis
- Job-market intelligence

---

## 👨‍💻 Author

**Akash Goswami**

AI & Machine Learning Engineer

- GitHub: https://github.com/akashgoswami139
- LinkedIn: https://linkedin.com/in/akashgoswami-/

---

## 📄 License

This project is intended for educational and portfolio use.
