
import random
import string

from .engine import Session
from .user import User
from .vendor import Vendor
from .reviews import Reviews


def weighted_starts_rating() -> int:
    return random.choices([1, 2, 3, 4, 5], weights=[0.5, 0.5, 1.5, 2.5, 5])[0]

def create_data():
    # Create a new session
    session = Session()

    # Create a user
    users_data = [
        {'username': 'John', 'email': "john.doe@example.com", "password": "password123"},
        {'username': 'Emily', 'email': "emily.smith@example.com", "password": "pass456"},
        {'username': 'Michael', 'email': "michael.johnson@example.com", "password": "securepass789"},
        {'username': 'Sarah', 'email': "sarah.williams@example.com", "password": "mypassword123"},
        {'username': 'David', 'email': "david.brown@example.com", "password": "password456!"},
        {'username': 'Jessica', 'email': "jessica.davis@example.com", "password": "qwerty123456"},
    ]

    for user_data in users_data:
        new_user = User(
            username=user_data['username'],
            email=user_data['email'],
        )
        new_user.set_password(user_data['password'])
        session.add(new_user)
        session.commit()


    # Create a bunch of vendors
    vendors_data = [
        {'name': 'Acme Inc.', 'description': 'A wedding cake baking company.', 'image_path': 'https://images.unsplash.com/photo-1604702433171-33756f3f3825', 'phone_number': '0722653964', 'email': 'info@acmeltd.co.ke', 'service_fee': '26000'},
        {'name': 'Floral Studio', 'description': 'A floral design studio.', 'image_path': 'https://images.unsplash.com/reserve/xd45Y326SvKzSR3Nanc8_MRJ_8125-1.jpg', 'phone_number': '0722653964', 'email': 'hello@fluralstudio.com', 'service_fee': '452000'},
        {'name': 'Cake Studio', 'description': 'A cake design studio.', 'image_path': 'https://images.unsplash.com/photo-1627580358573-ea0c4a2cb199', 'phone_number': '0722653964', 'email': 'joan@cakestudio.net', 'service_fee': '10000'},
        {'name': 'Bakery Studio', 'description': 'A bakery design studio.', 'image_path': 'https://images.unsplash.com/photo-1585779885249-e55411459cf7', 'phone_number': '0722653964', 'email': 'bake69@gmail.com', 'service_fee': '65000'},
        {'name': 'Wedding Studio', 'description': 'A wedding design studio.', 'image_path': 'https://images.unsplash.com/photo-1519741497674-611481863552', 'phone_number': '0722653964', 'email': 'contact@email.co.ze', 'service_fee': '15000'},
        {'name': 'Event Studio', 'description': 'An event design studio.', 'image_path': 'https://images.unsplash.com/photo-1501281668745-f7f57925c3b4', 'phone_number': '0722653964', 'email': 'all@email.com', 'service_fee': '25000'},
    ]


    for vendor_data in vendors_data:
        print(f"Creating new vendor: {vendor_data['name']}")
        
        new_vendor = Vendor(**vendor_data)
        session.add(new_vendor)
        session.commit()
        
        ## Create random reviews
        for i in range(random.randint(1, 500)):
            random_user = random.choice(session.query(User).all())
            print(f"Creating new review for {vendor_data['name']} from {random_user.username}")
            
            review = Reviews(
                rating=weighted_starts_rating(),
                comment=''.join(random.choices(string.ascii_letters + string.digits, k=100)),
                user=random_user,
                vendor=new_vendor
            )
            session.add(review)
            session.commit()
        
    
    session.close()


