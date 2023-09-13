from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, Table
from sqlalchemy.orm import relationship, sessionmaker, declarative_base
from sqlalchemy import func  

# Create the database engine
engine = create_engine('sqlite:///restaurant_reviews.db')
Base = declarative_base()
Session = sessionmaker(bind=engine)
session = Session()

# Define the association table
customer_restaurants = Table(
    'customer_restaurants',
    Base.metadata,
    Column('customer_id', Integer, ForeignKey('customers.id')),
    Column('restaurant_id', Integer, ForeignKey('restaurants.id'))
)

class Restaurant(Base):
    __tablename__ = 'restaurants'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    price = Column(Integer)

    # Define the relationship with Review
    reviews = relationship('Review', back_populates='restaurant', cascade='all, delete-orphan')    
    # Define the relationship with Customer
    customers = relationship('Customer', secondary= customer_restaurants, back_populates='restaurants')

    @classmethod
    def fanciest(cls):
        return session.query(cls).order_by(cls.price.desc()).first()

    def all_reviews(self):
        review_strings = [review.full_review() for review in self.reviews]
        return review_strings


class Customer(Base):
    __tablename__ = 'customers'

    id = Column(Integer, primary_key=True)
    first_name = Column(String)
    last_name = Column(String)

    # Define the relationship with Review
    reviews = relationship('Review', back_populates='customer', cascade='all, delete-orphan')
    # Define the relationship with Restaurant
    restaurants = relationship('Restaurant', secondary=customer_restaurants, back_populates='customers')

    def full_name(self):
        return f"{self.first_name} {self.last_name}"

    def favorite_restaurant(self):
        highest_rating = 0
        favorite_restaurant = None
        for review in self.reviews:
            if review.star_rating > highest_rating:
                highest_rating = review.star_rating
                favorite_restaurant = review.restaurant
        return favorite_restaurant

    def add_review(self, restaurant, rating):
        new_review = Review(customer=self, restaurant=restaurant, star_rating=rating)
        session.add(new_review)
        session.commit()

    def delete_reviews(self, restaurant):
        reviews_to_delete = [review for review in self.reviews if review.restaurant == restaurant]
        for review in reviews_to_delete:
            session.delete(review)
        session.commit()

class Review(Base):
    __tablename__ = 'reviews'

    id = Column(Integer, primary_key=True)
    star_rating = Column(Integer)

    restaurant_id = Column(Integer, ForeignKey('restaurants.id'))
    customer_id = Column(Integer, ForeignKey('customers.id'))

    restaurant = relationship('Restaurant', back_populates='reviews')
    customer = relationship('Customer', back_populates='reviews')

    def full_review(self):
        return f"Review for {self.restaurant.name} by {self.customer.full_name()}: {self.star_rating} stars."
