from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database import Restaurant, Customer, Review

# Create the database engine
engine = create_engine('sqlite:///restaurant_reviews.db')

# Create tables if they don't exist
Restaurant.metadata.create_all(engine)
Customer.metadata.create_all(engine)
Review.metadata.create_all(engine)

# Create a session to interact with the database
Session = sessionmaker(bind=engine)
session = Session()

# Create new restaurant and customer instances
restaurant1 = Restaurant(name='Restaurant A', price=3)
restaurant2 = Restaurant(name='Restaurant B', price=2)
customer1 = Customer(first_name='John', last_name='Doe')
customer2 = Customer(first_name='Jane', last_name='Smith')

# Add the instances to the session and commit to save them to the database
session.add_all([restaurant1, restaurant2, customer1, customer2])
session.commit()

# Close the session when you're done
session.close()
