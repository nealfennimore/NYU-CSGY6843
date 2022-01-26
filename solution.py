from hashlib import md5

### welcome_assignment_answers
### Input - All eight questions given in the assignment.
### Output - The right answer for the specific question.
no = [
    "Are encoding and encryption the same? - Yes/No",
    "Is it possible to decrypt a message without a key? - Yes/No",
    "Is a hashed message supposed to be un-hashed? - Yes/No",
    "Is MD5 a secured hashing algorithm? - Yes/No",
]
yes = [
    "Is it possible to decode a message without a key? - Yes/No",
]
secret = "In Slack, what is the secret passphrase posted in the #lab-python-getting-started channel posted by a TA?"
md5hash = "What is the MD5 hashing value to the following message: 'NYU Computer Networking' - Use MD5 hash generator and use the answer in your code"
dhcp = "What layer from the TCP/IP model the protocol DHCP belongs to? - The answer should be a numeric number"
tcp = "What layer of the TCP/IP model the protocol TCP belongs to? - The answer should be a numeric number"

def welcome_assignment_answers(question):
    if question in no:
        return 'No'
    
    if question in yes:
        return 'Yes'

    if question == secret:
        return 'mtls'

    if question == md5hash:
        return md5('NYU Computer Networking'.encode('utf-8')).hexdigest()

    if question == dhcp:
        return 1
    
    if question == tcp:
        return 3

if __name__ == "__main__":
    #use this space to debug and verify that the program works
    debug_question = "Are encoding and encryption the same? - Yes/No"
    print(welcome_assignment_answers(debug_question))

###Questions:
