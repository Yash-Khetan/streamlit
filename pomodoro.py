import streamlit as st
import time

st.title("Pomodoro Timer")


if "work_time" not in st.session_state:
    st.session_state.work_time = 25 
if "time_running" not in st.session_state:
    st.session_state.time_running = False

if "break_time" not in st.session_state:
    st.session_state.break_time = 0 
if st.button("Start Timer"):
    st.session_state.time_running = True

if st.button("Reset"):
    st.session_state.work_time = 25 
    st.session_state.time_running = False


if st.session_state.time_running and st.session_state.work_time > 0:
    time.sleep(1) 
    st.session_state.work_time -= 1
    st.rerun() 


if st.session_state.work_time == 0:
    st.success("🎉 Pomodoro Complete!")
    st.session_state.break_time = 5
    st.title("Break Time")
    


mins, secs = divmod(st.session_state.work_time, 60)
st.markdown(f"## ⏳ Time left: {mins:02d}:{secs:02d}")
