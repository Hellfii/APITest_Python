import requests
import streamlit as st
import pandas as pd


url = "http://localhost:8000/tasks"

def get_tasks():
    response = requests.get(url)
    tasks = response.json()
    return tasks

# Page d'accueil Streamlit
def homepage():
    st.title("Tasks")
    st.write("")
    st.write("")

    tasks = get_tasks()
    if len(tasks) > 0:
        df = pd.DataFrame(tasks)
        df = df.drop(columns=['id'])
        st.write(df)
    else:
        st.write("No tasks found.")

if __name__ == "__main__":
    homepage()