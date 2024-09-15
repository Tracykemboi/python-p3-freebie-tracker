#!/usr/bin/env python3
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Base, Company, Dev, Freebie

# Create engine and session
engine = create_engine('sqlite:///freebies.db')
Session = sessionmaker(bind=engine)
session = Session()

# Clear existing data
session.query(Freebie).delete()
session.query(Company).delete()
session.query(Dev).delete()
session.commit()

# Create sample companies
company1 = Company(name="TechCorp", founding_year=2000)
company2 = Company(name="CodeCo", founding_year=2010)

# Create sample devs
dev1 = Dev(name="Alice")
dev2 = Dev(name="Bob")

# Add companies and devs to the session
session.add_all([company1, company2, dev1, dev2])
session.commit()

# Create sample freebies
freebie1 = company1.give_freebie(dev1, "T-shirt", 20)
freebie2 = company2.give_freebie(dev1, "Mug", 10)
freebie3 = company1.give_freebie(dev2, "Sticker", 5)

# Add freebies to the session
session.add_all([freebie1, freebie2, freebie3])
session.commit()

print("Database seeded successfully!")

# Close the session
session.close()
