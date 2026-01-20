# Bill-Of-Materials-DBMS-Object-Relation-Mapping-Python-and-PostgreSQL

Bill of Materials (BOM) Management System: Relational Database design -> Object Relation Mapping + automating database operations; 


A Python-based application built with SQLAlchemy ORM and PostgreSQL that simulates a BOM and inventory structure: models hierarchical assemblies, vendor-supplied components, and usage constraints, reflecting how manufacturing systems can manage, validate, and maintain structured production data! 

This project provides a simple interface and structured way to manage data while maintaining data/referential integrity and adherance to business rules:
- Vendors
- Parts (assembly parts and piece parts)
- Usage relationships between assemblies and components
- It allows a user to create, view, update, and delete parts, assemblies, vendors, and their relationships while enforcing data correctness through both Python logic and database constraints.



# Planning: System Design : UML and ERD 
I started with focusing on understanding general business rules and relationship requirements!
Created a UML class diagram and class/attribute definition sheet to model the object-oriented structure of the system (ignoring implementation details)
    <img width="1701" height="1167" alt="image" src="https://github.com/user-attachments/assets/b5f20f10-ece9-45f5-bdd1-604bc457160c" />
Designed an interactive/shareable Entity Relationship Diagram (ERD) to model the relational database schema including migrated keys, check, relationships, index, and unique key constraints to display and model db criteria given
<img width="1021" height="644" alt="BOM-2026-01-19_16-27" src="https://github.com/user-attachments/assets/2fc7ccf2-a246-4f96-8b4e-820505edf55b" />




# Object Relation Mapping with SQLAlchemy library features: 

- Relational database schema and ERD design is implemented with SQLAlchemy 
-  complete CRUD (CREATE, READ, UPDATE, DELETE) functionality while preserving referential integrity through constraint checks and validators.
    - Automated :
       • Database connection management
      
      • table creation from ORM models and CRUD/software instructs database (reducing the need for mnual and repetitive SQL inputs)

       • Transaction handling (commit / rollback) -> ORM syncs operations to DB
- Includes sample data to model CRUD functions on Motorcycle Parts, Vendors and Usages
- Recursive traversal of assembly hierarchies to display the hierarchy of parts from sample data



  
# Considerations
- Primary key and unique constraints
- Foreign key relationships
- Check constraints + application-level validations with error diagnosis
- Safe delete operations to prevent orphaned records
- Interactive command-line menu system
- Preloaded seed data for demonstration and testing
- better communication with user; alongside diagnosing invalid inputs/operations or non-existent data when querying; the UI allows the user to retry entries for an rejected operation or cancel the operation entirely
  


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

#How to Run!

connect to db -> modify db_connection.py 
pip install sqlalchemy #download sqlalchemy
python data.py   # optional: delete bom_simple.db and run this command to restart + populate database with sample data 
python main.py



#Takeaways from Object Relation Mapping Design and it's Significance for managing data and automating DML in a Business context
- Developers can focus on business logic rather than writing and optimizing SQL queries, due to features like automatic CRUD operations and schema generation.
- User interface: Guides users through safe workflows with menu options to ensure users can only perform valid actions in the correct order. Python application rejects invalid data before attempting to commit to database; reducing errors and confusion (updating employee record, inserting a part, viewing data, etc). 
-  Instead of cryptic SQL error messages, users receive understandable business rule violation error messages when operation is rejected. Relationships like “an assembly must reference valid components” or “a vendor cannot be deleted if it is still in use” are enforced by the application.
- Changes to the database schema or business logic can often be managed and rewritten within the ORM layer, reducing the risk of breaking the application; and it is flexible across multiple RDBMS
-  Improves trust in data: When data integrity is enforced automatically, stakeholders can rely on the system for planning, inventory management, and analysis.
-   Allows focus on decisions, not mechanics: Users spend time managing components and assemblies rather than worrying about how data is stored or related.



