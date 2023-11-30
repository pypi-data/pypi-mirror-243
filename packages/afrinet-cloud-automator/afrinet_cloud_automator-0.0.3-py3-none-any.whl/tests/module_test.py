from module.src.storage.stack_vault_class import DataStack
from module.src.storage.link_vault_class import DataLink
from module.src.storage.file_class import FileStore

from module.src.processing.duck_queue_class import DuckQueue
from module.src.processing.duck_priority_queue_class import PriorityDuckQueue
from module.src.processing.duck_deadletter_queue_class import DeadLetterQueue
from module.src.mailing.mail_class import SwiftSend
from module.src.iam.user_class import UserClass
from module.src.config.verification_class import Verify


# Example usage:
datastore = DataStack()

users = [
    {
        "reference_no": "dfofnsonds323",
        "name": "Eugene Parker",
        "username": "Eugene",
        "password": "P@ssw0rd",
        "status": True,
    },
    {
        "reference_no": "ronwrwrwew321",
        "name": "Maya Klaus",
        "username": "Maya",
        "password": "P@ssw0rd",
        "status": True,
    },
    {
        "reference_no": "dfeweweewe323",
        "name": "Jones Mensah",
        "username": "Jones",
        "password": "P@ssw0rd",
        "status": True,
    },
    {
        "reference_no": "ronssdswewe321",
        "name": "Paul Stunk",
        "username": "Paul",
        "password": "P@ssw0rd",
        "status": True,
    },
    {
        "reference_no": "dfoewweewws323",
        "name": "Diana Kelly",
        "username": "Diana",
        "password": "P@ssw0rd",
        "status": True,
    },
    {
        "reference_no": "ronwrdwewww321",
        "name": "Chi Onoye",
        "username": "Chi",
        "password": "P@ssw0rd",
        "status": True,
    },
]


# for user in users:
#     datastore.push(user)

# print("Peek:", datastore.peek())
# print("Size:", datastore.size())
# print("-----------------------------------------------------------------")
# print()

# print("Size:", datastore.data_collection)
# print("-----------------------------------------------------------------")
# print()


# popped_element = datastore.pop()
# print("Popped:", popped_element)
# print("-----------------------------------------------------------------")
# print()


# print("Size after pop:", datastore.size())  # Output: Size after pop: 2
# print("-----------------------------------------------------------------")
# print()


# # Search for a dictionary based on a key-value pair
# found_dict = datastore.search("name", "Eugene Parker")
# print("Found Data:", found_dict)  # Output: Found dictionary: {'id': 2, 'name': 'Jane'}
# print("-----------------------------------------------------------------")
# print()


# # Update a dictionary based on a key-value pair
# update_result = datastore.update("reference_no", "dfeweweewe323", 4)
# print("Update result:", update_result)
# print("-----------------------------------------------------------------")
# print()


# print("-----------------------------------------------------------------")
# print("-----------------------------------------------------------------")
# print()

# # Example usage:
# data_link = DataLink()

# for user in users:
#     data_link.append(user)


# data_link.display()
# print("-----------------------------------------------------------------")
# print()


# # Search for a dictionary
# search_result = data_link.search("name", "Jones Mensah")
# print(
#     "Search result:", search_result
# )  # Output: Search result: {'id': 2, 'name': 'Jane'}


# # Update a dictionary
# update_result = data_link.update("reference_no", 2, 4)
# print("Update result:", update_result)  # Output: Update result: True


# # Check if a specific dictionary exists
# contains_result = data_link.contains({"reference_no": 1, "name": "John"})
# print("Contains result:", contains_result)  # Output: Contains result: True


# # Get the size of the linked list
# print("Size:", data_link.size())  # Output: Size: 3


# Example usage:
# duck_queue = DuckQueue()

# Enqueue data
# duck_queue.quack_enqueue("Data 1")
# duck_queue.quack_enqueue("Data 2")
# duck_queue.quack_enqueue("Data 3")

# Dequeue data
# while not duck_queue.is_empty():
#     item = duck_queue.quack_dequeue()
#     print("Dequeued:", item)

# Check the size of the flock (queue)
# print("Flock size:", duck_queue.flock_size())


# Example usage:
# priority_duck_queue = PriorityDuckQueue()
# dead_letter_queue = DeadLetterQueue()

# # Enqueue data with priorities
# priority_duck_queue.quack_enqueue_with_priority("High Priority Data", 1)
# priority_duck_queue.quack_enqueue_with_priority("Medium Priority Data", 2)
# priority_duck_queue.quack_enqueue_with_priority("Low Priority Data", 3)


# # Enqueue data to Dead-Letter Queue
# dead_letter_queue.quack_enqueue_dead_letter("Failed Data")

# Clear Priority Duck Queue and Dead-Letter Queue
# priority_duck_queue.clear_priority()
# dead_letter_queue.clear_dead_letter()

# Peek at the front elements
# print("Peek Priority Queue:", priority_duck_queue.peek_priority())
# print("Peek Dead-Letter Queue:", dead_letter_queue.peek())


# Example usage:
# data_stack = DataStack()
# file_queue = DuckQueue()

# file_store = FileStore()

# # Enqueue user data to be stored
# user_data_1 = {"username": "user1", "user_data": "Data for user1"}
# user_data_2 = {"username": "user2", "user_data": "Data for user2"}
# data_stack.push(user_data_1)
# data_stack.push(user_data_2)

# # Enqueue usernames for file creation
# file_queue.quack_enqueue("user1")
# file_queue.quack_enqueue("user2")

# # Process data and store in files
# file_store.process_data_and_store()

# # Process file creation
# file_store.process_file_creation()


# swift_sender = SwiftSend()

# # Send a single email
# swift_sender.send_html_email(
#     "dreamshipultra@gmail.com",
#     "Swift Send Test",
#     "Hello, If you are receiving this because ypu have subscribed to this channel",
#     ["eugenio.parker3@gmail.com"],
#     ["aafrinet@gmail.com"],
# )


# Send multiple emails in parallel
# recipients = [
#     "eugenio.parker3@gmail.com",
#     "dreamshipultra@gmail.com",
#     "afrinett@gmail.com",
# ]
# swift_sender.send_multiple_emails(
#     recipients, "Subject", "Hello, this is a text email for multiple recipients."
# )


# Example usage:
user_instance = UserClass()
user = user_instance.create_user_account(
    "John Doe", "john_doe", "password123", "password123", "regular", True
)

# Access the user details stored in the dictionary
print(user_instance.users)


# Example Usage:
verification_class = Verify()
user_reference_no = user  # Replace with the actual user's reference_no


# Generate a verification link
verification_link = verification_class.generate_verification_link(user_reference_no)
print(f"Verification Link: {verification_link}")

hashed_token = verification_class.retrieve_secret_token()
# Assume the user clicks on the verification link, and the URL contains the reference_no and hashed_token
hashed_token_from_url = (
    hashed_token  # Replace with the actual hashed token from the URL
)


print(hashed_token)
# Verify the user's account based on the provided token
verification_class.verify_account(user_reference_no, hashed_token_from_url)
