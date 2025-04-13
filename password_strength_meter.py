import streamlit as st
import random
import string

# Define a list of blacklisted common passwords
BLACKLISTED_PASSWORDS = {"password", "password123", "123456", "qwerty", "letmein", "admin"}

def evaluate_password(password: str) -> tuple[int, str, list]:
    """
    Evaluates the password strength and returns a score, overall rating, and feedback messages.

    Returns:
        score (int): Score from 1 to 5.
        strength (str): "Weak", "Moderate", or "Strong".
        feedback (list): List of suggestions to improve the password.
    """
    feedback = []
    score = 0

    # Check blacklist
    if password.lower() in BLACKLISTED_PASSWORDS:
        feedback.append("This password is too common. Please choose a more unique one.")
        return 1, "Weak", feedback

    # 1. Length check (>= 8)
    if len(password) >= 8:
        score += 1
    else:
        feedback.append("Increase password length to at least 8 characters.")

    # 2. Uppercase letter check
    if any(char.isupper() for char in password):
        score += 1
    else:
        feedback.append("Add at least one uppercase letter.")

    # 3. Lowercase letter check
    if any(char.islower() for char in password):
        score += 1
    else:
        feedback.append("Add at least one lowercase letter.")

    # 4. Digit check
    if any(char.isdigit() for char in password):
        score += 1
    else:
        feedback.append("Include at least one digit (0-9).")

    # 5. Special character check
    special_characters = "!@#$%^&*"
    if any(char in special_characters for char in password):
        score += 1
    else:
        feedback.append(f"Include at least one special character: {special_characters}")

    # Determine strength level
    if score <= 2:
        strength = "Weak"
    elif 3 <= score <= 4:
        strength = "Moderate"
    else:
        strength = "Strong"
        feedback = ["Great job! Your password meets all the criteria."]

    return score, strength, feedback

def generate_strong_password(length: int = 12) -> str:
    """
    Generates a random strong password that meets the criteria.
    
    Args:
        length (int): Length of the password. Default is 12.
        
    Returns:
        str: A strong password.
    """
    if length < 8:
        length = 8  # Enforce minimum length

    # Ensure that each category is represented
    password_chars = [
        random.choice(string.ascii_uppercase),
        random.choice(string.ascii_lowercase),
        random.choice(string.digits),
        random.choice("!@#$%^&*")
    ]

    # Fill the rest of the password length with a mix of all character types
    all_chars = string.ascii_letters + string.digits + "!@#$%^&*"
    remaining_length = length - len(password_chars)
    password_chars += random.choices(all_chars, k=remaining_length)

    # Shuffle the result to avoid predictable patterns
    random.shuffle(password_chars)
    return ''.join(password_chars)

# Streamlit UI
st.title("🔐 Password Strength Meter")

# Input password from the user
password_input = st.text_input("Enter your password:", type="password")

if st.button("Check Password Strength"):
    if password_input:
        score, strength, feedback = evaluate_password(password_input)
        st.write(f"**Password Strength:** {strength} (Score: {score})")
        st.write("**Feedback:**")
        for note in feedback:
            st.write(f"- {note}")
    else:
        st.warning("Please enter a password to evaluate.")

# Provide a feature to generate a strong password
if st.button("Generate a Strong Password"):
    new_password = generate_strong_password()
    st.write("**Suggested Strong Password:**")
    st.code(new_password)
    st.info("You can use this password or modify it further.")

# Optionally, display the criteria for a strong password
with st.expander("Password Strength Criteria"):
    st.markdown("""
    - **Minimum Length:** 8 characters
    - **Uppercase & Lowercase Letters**
    - **At Least One Digit (0-9)**
    - **At Least One Special Character:** `!@#$%^&*`
    - **Blacklist Check:** Avoid common passwords like `password123`
    """)


# Add a footer with a link to the GitHub repository

st.markdown("------------")

st.markdown("Made with ❤️ by [Muhammad Wasif](https://github.com/wasifsoomro/)