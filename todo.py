import streamlit as st

import pandas as pd
taskname = st.text_input("Enter your task")
addbutton = st.button("Add Task")
tasks = []



completed = [] 
incomplete = [] 
if "completed" not in st.session_state:
    st.session_state.completed = []
if "incomplete" not in st.session_state:
    st.session_state.incomplete = []

if addbutton and taskname:
    st.session_state.incomplete.append(taskname)
    st.success("Task Added")
all_tasks = st.session_state.get("completed", []) + st.session_state.get("incomplete", [])
statuses = ["Completed"] * len(st.session_state.get("completed", [])) + \
           ["Incomplete"] * len(st.session_state.get("incomplete", []))
df = pd.DataFrame({
    "Task": all_tasks,
    "Status": statuses,
   
})
for task in st.session_state.incomplete[:]:  # copy to avoid issues while removing
    if st.checkbox(task, key=task):
        st.session_state.incomplete.remove(task)
        st.session_state.completed.append(task)
        df.loc[df["Task"] == task, "Status"] = "Completed"
        st.success(f"Marked '{task}' as completed")


st.dataframe(df)






