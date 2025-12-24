def text_to_sql(text):
    text = text.lower()

    if "class 10" in text:
        return "SELECT * FROM students WHERE class = 10"

    if "marks above" in text:
        number = int(text.split("above")[-1].strip())
        return f"SELECT * FROM students WHERE marks > {number}"

    return "SELECT * FROM students"
