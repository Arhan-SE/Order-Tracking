import streamlit as st
import requests
from supabase import create_client, Client

# Configure Supabase client
SUPABASE_URL = "https://apuoavrnicfjbdotbgju.supabase.co"
SUPABASE_API_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImFwdW9hdnJuaWNmamJkb3RiZ2p1Iiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTc0MjU2NTc1NiwiZXhwIjoyMDU4MTQxNzU2fQ.MRjzYVIDvnaAg6C4yqsfAxMb6D2GNP6K-U6SG2UXCxM"
supabase: Client = create_client(SUPABASE_URL, SUPABASE_API_KEY)

def add_user_to_database(email, password):
    response = supabase.from_("users").insert({"email": email, "password": password}).execute()
    return response

def generate_user_id(email):
    return f"user_{hash(email)}"

def main():
    st.title("User Authentication System")

    menu = ["Login", "SignUp"]
    choice = st.sidebar.selectbox("Menu", menu)
    
    if choice == "Login":
        st.subheader("Login Section")

        email = st.text_input("Email")
        password = st.text_input("Password", type='password')

        if st.button("Login"):
            # Check user credentials in Supabase
            response = supabase.from_("users").select("*").eq("email", email).execute()
            if response.data and response.data[0]['password'] == password:
                st.success(f"Logged In as {email}")

                # Generate user_id
                user_id = generate_user_id(email)

                # Use user_id in memory configuration, etc.
            else:
                st.warning("Incorrect Username/Password")
    
    elif choice == "SignUp":
        st.subheader("Create New Account")

        new_email = st.text_input("Email")
        new_password = st.text_input("Password", type='password')

        if st.button("SignUp"):
            # Insert new user into Supabase
            res = add_user_to_database(new_email, new_password)
            if res.status_code == 201:
                st.success("You have successfully created an account")
            else:
                st.warning("Error occurred. Please try again later.")

if __name__ == '__main__':
    main()