import streamlit as st
import requests
import uuid
import pandas as pd

# ---------------- CONFIG ----------------

API_BASE_URL = "https://fenmo-expense-tracker.onrender.com"

st.set_page_config(page_title="Expense Tracker", layout="centered")

st.title("💰 Expense Tracker")


# ---------------- HELPERS ----------------

def fetch_expenses(category=None, sort=None):
    params = {}

    if category:
        params["category"] = category

    if sort:
        params["sort"] = sort

    try:
        res = requests.get(
            f"{API_BASE_URL}/expenses",
            params=params,
            timeout=5,
        )

        res.raise_for_status()
        return res.json()

    except Exception:
        st.error("Could not load expenses. Please try again.")
        return []


def create_expense(data):

    # Reuse same request id during session
    if "request_id" not in st.session_state:
        st.session_state.request_id = str(uuid.uuid4())

    headers = {
        "X-Request-ID": st.session_state.request_id
    }

    try:
        res = requests.post(
            f"{API_BASE_URL}/expenses",
            json=data,
            headers=headers,
            timeout=5,
        )

        res.raise_for_status()
        return res.json()

    except Exception:
        st.error("Failed to save expense.")
        return None


# ---------------- FORM ----------------

st.subheader("➕ Add Expense")

with st.form("expense_form", clear_on_submit=True):

    amount = st.number_input(
        "Amount (₹)",
        min_value=0.01,
        format="%.2f"
    )

    category = st.selectbox(
        "Category",
        ["Food", "Travel", "Shopping", "Bills", "Other"]
    )

    description = st.text_input("Description")

    date = st.date_input("Date")

    submitted = st.form_submit_button("Add Expense")

    if submitted:

        if amount <= 0:
            st.warning("Amount must be greater than 0.")

        elif not description.strip():
            st.warning("Description is required.")

        elif not date:
            st.warning("Date is required.")

        else:

            payload = {
                "amount": amount,
                "category": category,
                "description": description,
                "date": str(date),
            }

            with st.spinner("Saving..."):
                result = create_expense(payload)

            if result:
                st.success("Expense added!")

                # Reset request id after success
                if "request_id" in st.session_state:
                    del st.session_state["request_id"]


st.divider()


# ---------------- FILTERS ----------------

st.subheader("📋 Expenses")

col1, col2 = st.columns(2)

with col1:
    filter_category = st.selectbox(
        "Filter by Category",
        ["All", "Food", "Travel", "Shopping", "Bills", "Other"]
    )

with col2:
    sort_desc = st.checkbox("Newest First")


# ---------------- DATA ----------------

category_param = None
if filter_category != "All":
    category_param = filter_category

sort_param = "date_desc" if sort_desc else None

expenses = fetch_expenses(
    category=category_param,
    sort=sort_param
)


# ---------------- TABLE ----------------

if expenses:

    df = pd.DataFrame(expenses)

    df["date"] = pd.to_datetime(df["date"]).dt.date
    df["created_at"] = pd.to_datetime(df["created_at"])

    df = df[
        ["date", "category", "description", "amount"]
    ]

    st.dataframe(df, width="stretch")

    # ---------------- TOTAL ----------------

    # Convert amount safely to number
    df["amount"] = pd.to_numeric(df["amount"], errors="coerce")

    # Replace invalid values with 0
    df["amount"] = df["amount"].fillna(0.0)

    total = float(df["amount"].sum())

    st.metric("Total", f"₹ {total:.2f}")

    st.subheader("📊 Summary by Category")

    summary = (
        df.groupby("category")["amount"]
        .sum()
        .reset_index()
    )

    summary.columns = ["Category", "Total Amount"]

    st.table(summary)


else:
    st.info("No expenses found.")
