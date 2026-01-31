import streamlit as st
import pandas as pd

st.title("Cafe Staffing Insight Tool")

st.write("Enter sales and staff data for each time slot.")

# Create initial table
data = {
    "Time Slot": ["12-2", "2-4", "4-6", "6-8", "8-10"],
    "Sales (₹)": [0, 0, 0, 0, 0],
    "Staff Count": [1, 1, 1, 1, 1]

}

df = pd.DataFrame(data)

# SINGLE editable table
edited_df = st.data_editor(df, num_rows="fixed")

# ---- CALCULATIONS ----
hours_per_slot = 2

edited_df["Revenue per Staff Hour"] = (
    edited_df["Sales (₹)"] / (edited_df["Staff Count"] * hours_per_slot)
)

average_efficiency = edited_df["Revenue per Staff Hour"].mean()

def get_status(value):
    if value < 0.8 * average_efficiency:
        return "Overstaffed"
    elif value > 1.2 * average_efficiency:
        return "Understaffed"
    else:
        return "Optimal"

edited_df["Status"] = edited_df["Revenue per Staff Hour"].apply(get_status)

st.subheader("Staffing Analysis")
st.write(edited_df[["Time Slot", "Revenue per Staff Hour", "Status"]])

# ---- ONE CLEAR INSIGHT ----
problem_slots = edited_df[edited_df["Status"] == "Overstaffed"]

if not problem_slots.empty:
    slot = problem_slots.iloc[0]["Time Slot"]
    st.success(
        f"You are likely overstaffed during {slot}. Consider reducing 1 staff member."
    )
else:
    st.success("Your staffing looks balanced today.")
