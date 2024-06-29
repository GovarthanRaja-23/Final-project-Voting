import mysql.connector
from datetime import datetime
import smtplib

# Function to create the database if not exists
def create_database():
    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="12345"
    )
    cursor = conn.cursor()
    cursor.execute("CREATE DATABASE IF NOT EXISTS voting_db")
    cursor.close()
    conn.close()
# Function to initialize the database and table
def initialize_database():
    conn = mysql.connector.connect(
        host="localhost",
        user="root",    
        password="12345",
        database="voting_db"
    )
    cursor = conn.cursor()
    cursor.execute("CREATE TABLE IF NOT EXISTS candidates (name VARCHAR(255) PRIMARY KEY,vote_count INT DEFAULT 0)")
    
    # Read candidates name from a text file here
    with open("candidate.txt", "r") as file:
        for line in file:
            candidate_names = [name.strip() for name in line.strip().split(',')]
            for candidate in candidate_names:
                cursor.execute("INSERT IGNORE INTO candidates (name, vote_count) VALUES (%s, %s)", (candidate, 0))
    conn.commit()
    cursor.close()
    conn.close()

# Function to record a vote
def count_vote(voter_name, voter_age, voter_email, candidate_choice):
    if voter_age < 18:
        print("You are not eligible to vote.")
        return
    
    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="12345",
        database="voting_db"
    )
    cursor = conn.cursor()

    print(f"Recording {voter_name}'s vote for: {candidate_choice}")
    
    cursor.execute("UPDATE candidates SET vote_count = vote_count + 1 WHERE name = %s", (candidate_choice,))
    conn.commit()
    
    # Verify that the vote count is updated
    cursor.execute("SELECT vote_count FROM candidates WHERE name = %s", (candidate_choice,))
    vote_count = cursor.fetchone()
    
    if vote_count:
        print(f"Updated vote count for {candidate_choice}: {vote_count[0]}")
    else:
        print(f"No candidate found with the name: {candidate_choice}")

    cursor.close()
    conn.close()
    
    time_voted = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    receipt = f"Voter: {voter_name}\nAge: {voter_age}\nEmail: {voter_email}\nDate & Time: {time_voted}\n\n"
    
    with open('vote_receipts.txt', 'a') as file:
        file.write(receipt)
    def mail():
        try:                       
            vt=smtplib.SMTP("smtp.gmail.com",587)
            vt.starttls()

            #please enter Mail I'D and app password to run this code
            vt.login("","")

            subject = "Regarding Voting in Today Election"
            body = f"Subject: {subject}\n\nTHANKS FOR VOTING IN THE ELECTION YOU HAVE DONE YOUR ROLE AS A CITIZEN \n\nVoting Time: {time_voted}"

            #Enter the mail I'D you provided above to run this code
            vt.sendmail("",voter_email,body)

            vt.quit()
            print("------>MAIL IS SENT TO THE VOTER<------")
        except Exception as e:
            print("MAIL IS NOT SENT TO THE VOTER BECAUSE OF INVALID EMAIL ID")
    mail()
    print("Your vote has been recorded. Thank you!")

# Function to display candidates
def display_namecandidate():
    conn = mysql.connector.connect(
        host="localhost",
        user="root",    
        password="12345",
        database="voting_db"
    )
    cursor = conn.cursor()
    
    cursor.execute("SELECT * FROM candidates")
    candidates = cursor.fetchall()
    
    print("Candidates:")
    for i, candidate in enumerate(candidates):
        print(f"{i + 1}. {candidate[0]}")
    
    cursor.close()
    conn.close()

# Main voting function
def main():
    create_database()
    initialize_database()
    
    voter_name = input("Enter your name: ")
    voter_age = int(input("Enter your age: "))
    voter_email = input("Enter your email: ")
    
    display_namecandidate()
    
    candidate_choice_num = int(input("Enter the number of the candidate you want to vote for: "))
    
    # From the DataBase table Match the candidate's name directly from the list
    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="12345",
        database="voting_db"
    )
    cursor = conn.cursor()
    cursor.execute("SELECT name FROM candidates")
    candidates = cursor.fetchall()
    cursor.close()
    conn.close()

    # Convert the list of tuples to a list of names
    candidate_names = [candidate[0] for candidate in candidates]

    if 1 <= candidate_choice_num <= len(candidate_names):
        candidate_choice = candidate_names[candidate_choice_num - 1]
        count_vote(voter_name, voter_age, voter_email, candidate_choice)
    else:
        print("Invalid candidate number. Please try again.")

if __name__ == "__main__":
    main()