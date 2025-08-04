import re
import string

def check_password_strength(password):
    issues = []

    if(len(password) < 8):
        issues.append("Password must be at least 8 characters long. ")
    if not re.search(r'[A-Z]', password):
        issues.append("Password must contain at least one uppercase character. ")
    if not re.search(r'[a-z]', password):
        issues.append("Password must contain at least one lowercase character. ")
    if not re.search(r'\d', password):
        issues.append("Password must contain at leas one digit. ")
    if not re.search(f"[{re.escape(string.punctuation)}]", password):
        issues.append("Password must contain at least one special character (!@#$%^&* etc.). ")
    
    if issues:
        print("\n".join(issues))
        return False
    else:
        return True
    
    
user_password = input("Enter your Password :")
if(check_password_strength(user_password)):
    print("Hurray !! Strong Password Strength !!")
else:
    print(" Oops !! Weak Password Strength !!")