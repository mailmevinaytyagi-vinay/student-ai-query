def english_to_sql(question: str) -> str:
    """
    Converts English question to SQL.
    Uses Ollama locally if available.
    Falls back to rule-based logic on Streamlit Cloud.
    """

    # -----------------------------
    # TRY LOCAL LLM (OLLAMA)
    # -----------------------------
    try:
        import ollama  # imported ONLY if available

        prompt = f"""
You are an expert SQL generator.

Table:
students(id, name, class, marks)

Rules:
- Generate ONLY SELECT queries
- SQLite syntax only
- Output SQL only

Question:
{question}

SQL:
"""
        response = ollama.chat(
            model="mistral",
            messages=[{"role": "user", "content": prompt}]
        )

        sql = response["message"]["content"].strip()
        if not sql.lower().startswith("select"):
            raise ValueError("Only SELECT queries allowed")

        return sql

    # -----------------------------
    # FALLBACK (CLOUD / NO OLLAMA)
    # -----------------------------
    except Exception:
        q = question.lower()

        if "class 10" in q:
            return "SELECT * FROM students WHERE class = 10"

        if "marks above" in q:
            try:
                num = int(q.split("above")[-1].strip())
                return f"SELECT * FROM students WHERE marks > {num}"
            except:
                pass

        return "SELECT * FROM students"
