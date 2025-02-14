import random
import string

# Generate a random password of length 10
def generate_password(length):
    characters = string.ascii_letters + string.digits + string.punctuation
    return ''.join(random.choices(characters, k=length))


used_usernames = set()

def generate_username():
    prefix = "izyane"
    infix = "inno"
    suffixes = ["solution", "labs", "tech", "systems"]

    while True:
        suffix = random.choice(suffixes)
        unique_id = random.randint(100000, 999999)  # Ensures a 6-digit unique number
        username = f"{prefix}{infix}{suffix}{unique_id}"

        if username not in used_usernames:
            used_usernames.add(username)
            return username


