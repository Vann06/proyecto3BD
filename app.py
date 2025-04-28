import streamlit as st
import psycopg2
import os

DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT = os.getenv("DB_PORT", "5432")
DB_NAME = os.getenv("DB_NAME", "projectdb")
DB_USER = os.getenv("DB_USER", "user")
DB_PASSWORD = os.getenv("DB_PASSWORD", "password")

def get_db_connection():
    """Establishes a connection to the PostgreSQL database."""
    try:
        conn = psycopg2.connect(
            host=DB_HOST,
            port=DB_PORT,
            dbname=DB_NAME,
            user=DB_USER,
            password=DB_PASSWORD
        )
        return conn
    except psycopg2.OperationalError as e:
        st.error(f"Error connecting to database: {e}")
        st.error(f"Connection details used: Host={DB_HOST}, Port={DB_PORT}, DB={DB_NAME}, User={DB_USER}")
        st.info("Ensure the database container is running (`docker-compose up -d db`).")
        st.info("Verify the environment variables in `docker-compose.yml` match the database settings.")
        return None
    except Exception as e:
        st.error(f"An unexpected error occurred during database connection: {e}")
        return None


st.set_page_config(layout="wide")
st.title("Database Connection Test")

st.write("Attempting to connect to the database...")

conn = get_db_connection()

if conn:
    st.success("Successfully connected to the database!")
    st.write(f"Connected to: {DB_HOST}:{DB_PORT}/{DB_NAME} as {DB_USER}")
    conn.close()
    st.info("Database connection closed.")
else:
    st.warning("Database connection failed. Please check the errors above.")

st.markdown("---")
st.header("How to Run")
st.code("docker-compose up --build", language="bash")
st.write("Then access the application in your browser, usually at http://localhost:8502")
