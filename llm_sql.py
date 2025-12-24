import ollama

def english_to_sql(question: str) -> str:
    prompt = f"""
You are an expert SQL generator.

Table:
students(id, name, class, marks)

Rules:
- Generate ONLY SELECT queries
- SQLite syntax only

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
