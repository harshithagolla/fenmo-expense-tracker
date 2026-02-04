from fastapi import FastAPI

app = FastAPI(title="Expense Tracker API")


@app.get("/")
def health_check():
    return {"status": "ok"}


@app.get("/expenses")
def get_expenses():
    return []


@app.post("/expenses")
def create_expense():
    return {"message": "Not implemented yet"}
