# Bill-Of-Materials-DBMS-Object-Relation-Mapping-Python-and-PostgreSQL

Bill of Materials (BOM) Management System:
A Python-based application built with SQLAlchemy ORM and PostgreSQL that simulates a real-world BOM and inventory structure. The system models hierarchical assemblies, vendor-supplied components, and usage constraints, reflecting how manufacturing systems manage, validate, and maintain structured production data.

Planning: System Design (UML and ERD) - Started with focusing on understanding general business rules and relationship requirements
- Created a UML class diagram and class/attribute definition sheet to model the object-oriented structure of the system
  - Identified core classes (Part, AssemblyPart, PiecePart, Vendor, Usage) and their general relationships, multiplicities and cardinality (excludes implementation detail)
    <img width="1701" height="1167" alt="image" src="https://github.com/user-attachments/assets/b5f20f10-ece9-45f5-bdd1-604bc457160c" />
- Designed an interactive Entity Relationship Diagram (ERD) to model the relational database schema including migrated keys, check, relationships, index, and unique key constraints to display and model db criteria given
<img width="1021" height="644" alt="BOM-2026-01-19_16-27" src="https://github.com/user-attachments/assets/2fc7ccf2-a246-4f96-8b4e-820505edf55b" />


Project Overview
This project provides a structured way to manage:
- Vendors
- Parts (assembly parts and piece parts)
- Usage relationships between assemblies and components
It demonstrates how relational databases handle hierarchical data, foreign key relationships, and constraint enforcement in a realistic domain.

Features
- Relational database schema implemented with SQLAlchemy ORM
-  complete CRUD functionality while preserving referential integrity through constraint checks and validators.
- Includes sample data to model CRUD functions on Motorcycle Parts, Vendors and Usages 
- Recursive traversal of assembly hierarchies to display the hierarchy of parts from sample data
  
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

├── data.py       # Sample data population

├── bom_simple.db      # Seeded database file

How to Run!

connect to db -> modify db_connection.py 
pip install sqlalchemy #download sqlalchemy
python data.py   # optional: delete bom_simple.db and run this command to restart + populate database with sample data 
python main.py
