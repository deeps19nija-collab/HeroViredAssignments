import re
import string

def check_password_strength(password):
    issues = []
    # Check minimum length
    if(len(password) < 8):
        issues.append("Password must be at least 8 characters long. ")
    
    # Check for both uppercase and lowercase letters
    if not re.search(r'[A-Z]', password):
        issues.append("Password must contain at least one uppercase character. ")
    if not re.search(r'[a-z]', password):
        issues.append("Password must contain at least one lowercase character. ")

     # Check for at least one digit
    if not re.search(r'\d', password):
        issues.append("Password must contain at leas one digit. ")

    # Check for at least one special character
    if not re.search(f"[{re.escape(string.punctuation)}]", password):
        issues.append("Password must contain at least one special character (!@#$%^&* etc.). ")
    
    # If there are any issues found during password checks
    if issues:

        # Join all issue messages with newlines and print them
        print("\n".join(issues))

        # Return False to indicate the password is weak
        return False
    else:

        # If no issues, return True (password is strong)
        return True
    

if __name__ == "__main__": 

    # Prompt the user to enter a password
    user_password = input("Enter your Password :")

    # Call the password strength check function and act based on the result
    if(check_password_strength(user_password)):
        print("Hurray !! Strong Password Strength !!")
    else:
        print("Oops !! Weak Password Strength !! Please modify the password based on the feedback !! ")