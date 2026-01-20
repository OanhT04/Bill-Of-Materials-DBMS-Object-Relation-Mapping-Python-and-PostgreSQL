# Bill-Of-Materials-DBMS-Object-Relation-Mapping-Python-and-PostgreSQL

Bill of Materials (BOM) Management System

Step 1: System Design (UML and ERD)
- Created a UML class diagram to model the object-oriented structure of the system
  - Identified core classes (Part, AssemblyPart, PiecePart, Vendor, Usage) and their responsibilities
- Designed an Entity Relationship Diagram (ERD) to model the relational database schema including migrated keys, check, relationships, index, and unique key constraints accordingly to business rule criteria


A Python-based Bill of Materials (BOM) Management System built using SQLAlchemy ORM and SQLite.
The application models manufacturing data, supporting hierarchical assemblies, component relationships, and strict data integrity rules through a command-line interface.

Project Overview
This project provides a structured way to manage:
- Vendors
- Parts (assembly parts and piece parts)
- Usage relationships between assemblies and components
It demonstrates how relational databases handle hierarchical data, foreign key relationships, and constraint enforcement in a realistic domain.

Features
- Relational database schema implemented with SQLAlchemy ORM
- Full CRUD functionality (Create, Read, Update, Delete)
- Includes sample data on Motorcycle Parts, Vendors and Usages 
- Recursive traversal of assembly hierarchies

Enforced data integrity:
- Primary key and unique constraints
- Foreign key relationships
- Check constraints + application-level validations for smooth user interaction
- Safe delete operations to prevent orphaned records
- Interactive command-line menu system
- Preloaded seed data for demonstration and testing

Tech Stack
- Python 3
- SQLAlchemy
- PostgreSQL

Command Line Interface (CLI)

Project Structure

├── main.py            # Application entry point

├── ORM.py             # Database models

├── operations.py      # Query, insert, update, delete logic

├── check.py           # Validation and integrity checks

├── menu.py            # CLI menus

├── db_connection.py   # Database engine and session setup

├── seed_data.py       # Sample data population

├── bom_simple.db      # SQLite database file

How to Run
pip install sqlalchemy

python seed_data.py   # optional: populate database with sample data 

python main.py
