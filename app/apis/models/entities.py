from sqlalchemy import create_engine, Column, String, Integer, DateTime, Float, Text, DECIMAL, ForeignKey, Boolean, func
from sqlalchemy.orm import relationship, declarative_base, sessionmaker
from app.core.database import Base

class User(Base):
    __tablename__ = 'user'
    
    id = Column(String(36), primary_key=True)
    name = Column(String(16), nullable=False)
    email = Column(String(255), nullable=False)
    password = Column(String(32), nullable=False)
    created_at = Column(DateTime, nullable=False)
    updated_at = Column(DateTime, nullable=False)
    suscripciones = relationship("Suscripcion", back_populates="user")

class Suscripcion(Base):
    __tablename__ = 'suscripcion'
    
    id = Column(String(36), primary_key=True)
    type = Column(String(16), nullable=False)
    created_at = Column(DateTime, nullable=False)
    updated_at = Column(DateTime, nullable=False)
    valid_until = Column(DateTime, nullable=False)
    user_id = Column(String(36), ForeignKey('user.id'), nullable=False)
    subscription_type_id = Column(Integer, ForeignKey('subscription_type.id'), nullable=False)
    
    user = relationship("User", back_populates="suscripciones")
    subscription_type = relationship("SubscriptionType", back_populates="suscripciones")

class SubscriptionType(Base):
    __tablename__ = 'subscription_type'
    
    id = Column(Integer, primary_key=True)
    name = Column(String(64), nullable=False)
    price_monthly = Column(Float(12, 2), nullable=False)
    price_semester = Column(Float(12, 2), nullable=False)
    price_annual = Column(Float(12, 2), nullable=False)
    suscripciones = relationship("Suscripcion", back_populates="subscription_type")

class Property(Base):
    __tablename__ = 'property'
    
    id = Column(String(36), primary_key=True)
    title = Column(String(255), nullable=False)
    generated_title = Column(String(255), nullable=False)
    price_amount = Column(DECIMAL(15, 2), nullable=False)
    price_currency = Column(String(3), nullable=False)
    expenses_amount = Column(DECIMAL(15, 2), nullable=False)
    expenses_currency = Column(String(3), nullable=False)
    total_area = Column(DECIMAL(10, 2), nullable=False)
    covered_area = Column(DECIMAL(10, 2), nullable=False)
    rooms = Column(Integer, nullable=False)
    bedrooms = Column(Integer, nullable=False)
    bathrooms = Column(Integer, nullable=False)
    age = Column(Integer, nullable=False)
    orientation = Column(String(50), nullable=False)
    luminosity = Column(Boolean, nullable=False)
    description = Column(Text, nullable=False)
    address = Column(String(255), nullable=False)
    neighborhood = Column(String(100), nullable=False)
    suburb = Column(String(100), nullable=False)
    city = Column(String(100), nullable=False)
    latitude = Column(DECIMAL(10, 8), nullable=False)
    longitude = Column(DECIMAL(10, 8), nullable=False)
    google_maps_link = Column(Text, nullable=False)
    reserved = Column(Boolean, nullable=False)
    status = Column(String(20), nullable=False)
    modified_date = Column(DateTime, nullable=False)
    created_at = Column(DateTime, nullable=False)
    updated_at = Column(DateTime, nullable=False)
    property_images = relationship("PropertyImage", back_populates="property")

class ImageType(Base):
    __tablename__ = 'image_type'
    
    id = Column(Integer, primary_key=True)
    name = Column(String(45), nullable=False)
    created_at = Column(DateTime, nullable=False)
    updated_at = Column(DateTime, nullable=False)
    property_images = relationship("PropertyImage", back_populates="image_type")

class PropertyImage(Base):
    __tablename__ = 'property_image'
    
    id = Column(String(36), primary_key=True)
    url = Column(Text, nullable=False)
    property_id = Column(String(36), ForeignKey('property.id'), nullable=False)
    image_type_id = Column(Integer, ForeignKey('image_type.id'), nullable=False)
    created_at = Column(DateTime, nullable=False)
    updated_at = Column(DateTime, nullable=False)
    
    property = relationship("Property", back_populates="property_images")
    image_type = relationship("ImageType", back_populates="property_images")
