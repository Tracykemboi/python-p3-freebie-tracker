# Import necessary modules from SQLAlchemy
from sqlalchemy import Column, Integer, String, ForeignKey, Table
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

# Create a base class for declarative class definitions
Base = declarative_base()

# Define the association table for the many-to-many relationship between Company and Dev
company_dev = Table('company_dev', Base.metadata,
    Column('company_id', Integer, ForeignKey('companies.id')),
    Column('dev_id', Integer, ForeignKey('devs.id'))
)

# Define the Company model
class Company(Base):
    __tablename__ = 'companies'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    founding_year = Column(Integer)

    # Establish relationships
    freebies = relationship("Freebie", back_populates="company")
    devs = relationship("Dev", secondary=company_dev, back_populates="companies")

    # Method to give a freebie to a dev
    def give_freebie(self, dev, item_name, value):
        new_freebie = Freebie(item_name=item_name, value=value, dev=dev, company=self)
        return new_freebie

    # Class method to find the oldest company
    @classmethod
    def oldest_company(cls):
        from sqlalchemy.orm import Session
        from sqlalchemy import create_engine
        engine = create_engine('sqlite:///freebies.db')
        session = Session(engine)
        return session.query(cls).order_by(cls.founding_year).first()

# Define the Dev model
class Dev(Base):
    __tablename__ = 'devs'

    id = Column(Integer, primary_key=True)
    name = Column(String)

    # Establish relationships
    freebies = relationship("Freebie", back_populates="dev")
    companies = relationship("Company", secondary=company_dev, back_populates="devs")

    # Method to check if the dev has received a specific item
    def received_one(self, item_name):
        return any(freebie.item_name == item_name for freebie in self.freebies)

    # Method to give away a freebie to another dev
    def give_away(self, dev, freebie):
        if freebie in self.freebies:
            freebie.dev = dev
            return True
        return False

# Define the Freebie model
class Freebie(Base):
    __tablename__ = 'freebies'

    id = Column(Integer, primary_key=True)
    item_name = Column(String)
    value = Column(Integer)
    dev_id = Column(Integer, ForeignKey('devs.id'))
    company_id = Column(Integer, ForeignKey('companies.id'))

    dev = relationship("Dev", back_populates="freebies")
    company = relationship("Company", back_populates="freebies")

    def print_details(self):
        dev_name = self.dev.name if self.dev else "No owner"
        company_name = self.company.name if self.company else "Unknown company"
        return f"{dev_name} owns a {self.item_name} from {company_name}."