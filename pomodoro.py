import streamlit as st
import time

st.title("Pomodoro Timer ⏱️")

# Task input
chapter_name = st.text_input("📚 Enter Task:")
if chapter_name:
    st.success(f"✅ Task added: {chapter_name}")

estimatedwords = st.number_input("Enter the estimated words ", min_value=100)
if estimatedwords:
    pomosneeded = estimatedwords / 500
    if pomosneeded == 0:
        pomosneeded = 1  # Fixed typo
    st.info(f"Pomos needed would be {pomosneeded}")

# Initialize session state
if "mode" not in st.session_state:
    st.session_state.mode = "Work"
if "sessions" not in st.session_state:
    st.session_state.sessions = 0
if "time_running" not in st.session_state:
    st.session_state.time_running = False
if "timer" not in st.session_state:
    st.session_state.timer = 25  # Default 25 sec for testing
if "total_time" not in st.session_state:
    st.session_state.total_time = 25
if "history" not in st.session_state:
    st.session_state.history = []

# Buttons
start = st.button("▶️ Start Timer")
reset = st.button("🔁 Reset")

# Start logic
if start:
    if chapter_name:  # only start if task is entered
        st.session_state.time_running = True
    else:
        st.warning("⚠️ Please enter a task before starting.")

# Reset logic
if reset:
    st.session_state.mode = "Work"
    st.session_state.sessions = 0
    st.session_state.timer = 25
    st.session_state.total_time = 25
    st.session_state.time_running = False
    st.session_state.history = []

# Display mode and time
st.subheader(f"Current Mode: {st.session_state.mode}")
mins, secs = divmod(st.session_state.timer, 60)
st.markdown(f"## ⏳ Time left: {mins:02d}:{secs:02d}")

# Countdown logic
if st.session_state.time_running and st.session_state.timer > 0:
    time.sleep(1)
    st.session_state.timer -= 1
    progress_val = int(((st.session_state.total_time - st.session_state.timer) / st.session_state.total_time) * 100)
    st.progress(progress_val)
    st.rerun()

# When timer hits 0
if st.session_state.timer == 0 and st.session_state.time_running:
    st.session_state.time_running = False

    if st.session_state.mode == "Work":
        st.session_state.sessions += 1
        st.success("✅ Work session complete!")

        # Update history
        if chapter_name:
            found = False
            for item in st.session_state.history:
                if item["Task"] == chapter_name:
                    item["Pomodoros"] += 1
                    found = True
                    break
            if not found:
                st.session_state.history.append({"Task": chapter_name, "Pomodoros": 1})

        # Set break mode
        if st.session_state.sessions % 4 == 0:
            st.session_state.mode = "Long Break"
            st.session_state.total_time = 15
            st.session_state.timer = 15
        else:
            st.session_state.mode = "Short Break"
            st.session_state.total_time = 5
            st.session_state.timer = 5

    else:
        st.success("🕒 Break over! Time to work.")
        st.session_state.mode = "Work"
        st.session_state.total_time = 25
        st.session_state.timer = 25

    st.rerun()

# Save task history to a text file
if st.session_state.history:
    with open("tasks.txt", "w") as file:
        for item in st.session_state.history:
            file.write(f"Task: {item['Task']}, Pomodoros: {item['Pomodoros']}\n")

# Display saved task history and download button
with open("tasks.txt", "r") as file:
    content = file.read()
    st.write("Saved tasks: ", content)
    st.download_button("📥 Download Task History", data = content, file_name="tasks.txt")
   
# Display history table
if st.session_state.history:
    st.subheader("📈 Session History")
    st.table(st.session_state.history)
