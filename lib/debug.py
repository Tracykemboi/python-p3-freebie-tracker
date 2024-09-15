#!/usr/bin/env python3

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Company, Dev, Freebie, Base

if __name__ == '__main__':
    # Create engine and session
    engine = create_engine('sqlite:///freebies.db')
    Session = sessionmaker(bind=engine)
    session = Session()

# Add test data if the database is empty
    if session.query(Company).count() == 0 and session.query(Dev).count() == 0:
        print("Adding test data...")
        company1 = Company(name="TechCorp", founding_year=2000)
        company2 = Company(name="CodeCo", founding_year=2010)
        dev1 = Dev(name="Alice")
        dev2 = Dev(name="Bob")
        session.add_all([company1, company2, dev1, dev2])
        session.commit()
        print("Test data added.")


    # Print some information about our database
    print("Database Info:")
    print(f"Number of companies: {session.query(Company).count()}")
    print(f"Number of devs: {session.query(Dev).count()}")
    print(f"Number of freebies: {session.query(Freebie).count()}")

    # Test some of our methods
    print("\nTesting methods:")

    # Test Company.oldest_company()
    oldest_company = Company.oldest_company()
    if oldest_company:
        print(f"Oldest company: {oldest_company.name}, founded in {oldest_company.founding_year}")
    else:
        print("No companies found in the database.")

    # Test Dev.received_one()
    dev = session.query(Dev).first()
    if dev:
        print(f"\nTesting Dev.received_one() for {dev.name}:")
        print(f"Received a T-shirt: {dev.received_one('T-shirt')}")
        print(f"Received a Laptop: {dev.received_one('Laptop')}")
    else:
        print("No devs found in the database.")

    # Test Freebie.print_details()
    freebie = session.query(Freebie).first()
    if freebie:
        print(f"\nTesting Freebie.print_details():")
        print(freebie.print_details())
        print(f"Freebie details: item_name={freebie.item_name}, value={freebie.value}")
        print(f"Associated Dev: {freebie.dev.name if freebie.dev else 'None'}")
        print(f"Associated Company: {freebie.company.name if freebie.company else 'None'}")
    else:
        print("No freebies found in the database.")

    # Test Company.give_freebie()
    company = session.query(Company).first()
    dev = session.query(Dev).first()
    if company and dev:
        print(f"\nTesting Company.give_freebie():")
        new_freebie = company.give_freebie(dev, "Water Bottle", 15)
        session.add(new_freebie)
        session.commit()
        print(f"New freebie created: {new_freebie.print_details()}")
    else:
        print("Company or Dev not found in the database.")

    # Test creating and querying a Freebie
    print("\nTesting Freebie creation and querying:")
    new_freebie = Freebie(item_name="T-shirt", value=20)
    session.add(new_freebie)
    session.commit()

    queried_freebie = session.query(Freebie).filter_by(item_name="T-shirt").first()
    if queried_freebie:
        print(f"Queried freebie: {queried_freebie.item_name}, value: {queried_freebie.value}")
        print(f"Associated Dev: {queried_freebie.dev.name if queried_freebie.dev else 'None'}")
        print(f"Associated Company: {queried_freebie.company.name if queried_freebie.company else 'None'}")
    else:
        print("Failed to create or query the new Freebie.")

    # Start an interactive IPython debugger session
    import ipdb; ipdb.set_trace()

    # Don't forget to close the session when you're done
    session.close()