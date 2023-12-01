class RideSharingApp:
    def __init__(self):
        self.users = {}

    def register_user(self, name, gender, email, phonenumber, destination):
        user_id = len(self.users) + 1  # Generate a unique user ID (can be more sophisticated)
        user_data = {
            'name': name,
            'gender': gender,
            'email': email,
            'phonenumber': phonenumber,
            'destination': destination,
        }
        self.users[user_id] = user_data
        return user_id

    def get_user_details(self, user_id):
        return self.users.get(user_id)
    
    

# Example usage:
if __name__ == "__main__":
    ride_share_app = RideSharingApp()

    # Register a user
    user_id = ride_share_app.register_user('John Doe', 'male', 'john@example.com', '1234567890', 'ireland')
    print("User registered with ID:", user_id)

    # Get user details
    user_details = ride_share_app.get_user_details(user_id)
    if user_details:
        print("User Details:", user_details)
    else:
        print("User not found.")