from check import *
from ORM import *
from menu import *
from db_connection import Session, engine
from sqlalchemy.exc import IntegrityError


#Query Operations 

#using recursion
def print_hierarchy(session, parent, level=0):
    usages=session.query(Usage).filter_by(assemblyPartName=parent).all()
    children=[]
    for u in usages:
        part=session.query(Part).filter_by(partName=u.componentPartName).first()
        if part:children.append(part)
    children.sort(key=lambda p:p.partNumber)
    for part in children:
        indent="\t"*(level+1)
        print(f"{indent}{part.partNumber} - {part.partName}")
        if session.query(AssemblyPart).filter_by(assemblyPartName=part.partName).first():
            print_hierarchy(session, part.partName, level+1)

#just to list all of content from tables
def listVendors(engine):
    print("\n=== Vendor List ===")
    with Session() as session:
        vendors = session.query(Vendor).all()
        if not vendors:
            print("No vendors found.")
        else:
            for v in vendors:
                print(f'Name: {v.supplierName}')

def listAssemblyParts(engine):
    print("\n=== Assembly Parts List ===")
    with Session() as session:
        parts = session.query(AssemblyPart).all()
        if not parts:
            print("No parts found.")
        else:
            for p in parts:
                print(f'Name: {p.partName}\nNumber: {p.partNumber}\n')

def listPieceParts(engine):
    print("\n=== Piece Parts List ===")
    with Session() as session:
        parts = session.query(PiecePart).all()
        if not parts:
            print("No parts found.")
        else:
            for p in parts:
                print(f'Name: {p.partName} \nNumber: {p.partNumber}\nVendor Name: {p.vendorSupplierName}\n')

def listParts(engine):
    print("\n====Parts List====\n")
    with Session() as session:
        parts = session.query(Part).all()
        if not parts:
            print("No parts found.")
        else:
            for p in parts:
                print(f'Name: {p.partName} \nNumber: {p.partNumber}\n')
                
def listUsages(engine):
    print("\n=== Usages List ===")
    with Session() as session:
        usage = session.query(Usage).all()
        if not usage:
            print("No usages found.")
        else:
            for u in usage:
                print("Assembly:", u.assemblyPartName, "\nComponent:", u.componentPartName, "\nUsage Quantity:", u.usageQuantity,"\n")
                
#returns list of all of the assemblies with highest number of components
def findHighAssembly(engine):
    print("====List of Assembly Parts With Highest Number Of Component Parts=====")
    with Session() as session:
        assembly_counts=session.query(Usage.assemblyPartName,func.count(Usage.componentPartName)).group_by(Usage.assemblyPartName).all()
        if not assembly_counts:
            print("No usages found.");return
        maxCount=max(c for _,c in assembly_counts)
        topAssemblies=[n for n,c in assembly_counts if c==maxCount]
        for assemblyPartName in topAssemblies:
            part=session.query(Part).filter_by(partName=assemblyPartName).first()
            if not part:continue
            print(f"\nAssembly Part: {assemblyPartName}\nAssembly Number: {part.partNumber}\nNumber of Components: {maxCount}")

#if we want to view information from a specific row: Gets PK to retrieve info
def queryRow():
    print("Which table would you like to view a row from?")
    table = viewTableMenu()

    with Session() as session:
        if table == 1:
            name = input("Enter Vendor Name: ")
            row = session.query(Vendor).filter_by(supplierName=name).first()
            if row is None:
                print("Row Not Found...")
                return
            print("\n====== Vendor Row ======")
            print(f"Supplier Name: {row.supplierName}")
            return

        elif table == 2:
            name = input("Enter Assembly Name: ")
            row = session.query(AssemblyPart).filter_by(assemblyPartName=name).first()
            if row is None:
                print("Row Not Found...")
                return
            print("\n====== Assembly Part Row ======")
            print(f"Assembly Name: {row.assemblyPartName}")
            print(f"Part Name: {row.partName}")
            print(f"Part Number: {row.partNumber}")
            print(f"Part Type: {row.partType}")
            return

        elif table == 3:
            name = input("Enter Piece Name: ")
            row = session.query(PiecePart).filter_by(piecePartName=name).first()
            if row is None:
                print("Row Not Found...")
                return
            print("\n====== Piece Part Row ======")
            print(f"Piece Name: {row.piecePartName}")
            print(f"Part Name: {row.partName}")
            print(f"Part Number: {row.partNumber}")
            print(f"Part Type: {row.partType}")
            print(f"Vendor Supplier Name: {row.vendorSupplierName}")
            return

        elif table == 4:
            a = input("Enter Assembly Name: ")
            c = input("Enter Component Name: ")
            row = session.query(Usage).filter_by(assemblyPartName=a, componentPartName=c).first()
            if row is None:
                print("Row Not Found...")
                return
            print("\n====== Usage Row ======")
            print(f"Assembly Name: {row.assemblyPartName}")
            print(f"Component Name: {row.componentPartName}")
            print(f"Usage Quantity: {row.usageQuantity}")
            
        elif table == 5:
            name = input("Enter Part Name: ")
            row = session.query(Part).filter_by(partName = name).first()
            if row is None:
                print("Row Not Found...")
                return
            print("\n====== Part Row ======")
            print(f"Part Name: {row.partName}")
            print(f"Part Number: {row.partNumber}")
            print(f"Part Type: {row.partType}")
            return

#query menu and operations
def queryOperations():
    while True:
        print("\n★・✦ VIEW MENU ✦・★")
        print("----------------------------------------")
        print("  [1] View Part Hierarchy")
        print("  [2] View All Data From a Table")
        print("  [3] View Data From a Row")
        print("  [4] View Assemblies With Highest Number of Components")
        print("  [5] Back to Main Menu")
        print("----------------------------------------")

        try:
            choice = int(input("\nNumber Selection: "))
        except ValueError:
            print("Please enter a number from 1–5.")
            continue
        if choice < 1 or choice > 5:
            print("{choice} is not a valid menu option.")
            continue
        if choice == 1:
            with Session() as session:
                row = session.query(AssemblyPart).order_by(AssemblyPart.partNumber.asc()).first()
                if row is None:
                    print("No assembly parts found.")
                    continue
                print(f"0 - {row.partNumber} - {row.partName}")
                finalAssembly = row.assemblyPartName
                print_hierarchy(session, finalAssembly, level=0)
    
        if choice == 2:
            table = viewTableMenu()
            if table == 1:
                listVendors(engine)
            elif table == 2:
                listAssemblyParts(engine)
            elif table == 3:
                listPieceParts(engine)
            elif table == 4:
                listUsages(engine)
            elif table == 5:
                listParts(engine)
        if choice == 3:
            queryRow()
        if choice == 4:
            findHighAssembly(engine)
        if choice == 5:
            return

#insert operations: inserting into parts will still call either add assembly or piece to ensure all parts added are complete disjoint

def insert(table):
    if table.__tablename__ not in table.metadata.tables:
        raise ValueError(f"Table '{table.__tablename__}' does not exist in metadata.")

#decorator and wrapper to reuse function logic, check constraints, create objects and add to DB 
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            data = func(*args, **kwargs)
            with Session() as session:
                try:
                    obj = table(**data)
                    if not validate_before_insert(session, obj):
                        #checks "look up" table for vendors and if info for usages exists within assembly and parts
                        session.rollback()
                        return None
                    session.add(obj)
                    session.commit()
                    return obj
                except ValueError as e: 
                    #when validator violation raises; so logical errors in python
                    print(e)
                    return None
                except IntegrityError as e: #when uniqueness and check constraints get violated;
                    #these are the data base violations/rejections
                    print(e.orig)
                    session.rollback()
                    return None
        return wrapper
    return decorator

#expected values for insertion
@insert(Vendor)
def add_vendor(name: str):
    return {
        "supplierName": name,
    }

@insert(Part)
def add_part(name: str, number: str, partType: str):
    return {
        "partName": name,
        "partNumber": number,
        "partType": partType
    }

@insert(AssemblyPart)
def add_assembly(name: str, number: str):
    return {
        # Base Part fields
        "partName": name,
        "partNumber": number,
        "partType": "assembly_part",

        # AssemblyPart-specific field
        "assemblyPartName": name
    }

@insert(PiecePart)
def add_piece_part(name: str, number: str, vendor_name: str | None):
    return {
        # Base Part fields
        "partName": name,
        "partNumber": number,
        "partType": "piece_part",

        # PiecePart-specific fields
        "piecePartName": name,
        "vendorSupplierName": vendor_name
    }

@insert(Usage)
def add_usage(assemblyName: str, componentName: str, quantity: int):
    return {
        "assemblyPartName": assemblyName,
        "componentPartName": componentName,
        "usageQuantity": quantity
    }


#insert to each of the tables
def insertOperations():
    repeat = 0 
    while repeat == 0:
        print("Which table would you like to record new information on?")
    
        table = viewTableMenu()
            
        if table == 1:
            print("Add a Vendor")
            name = input("Enter Vendor Name: ")
            if add_vendor(name):
                print (f"Vendor: {name} successfully added")
                listVendors(engine)  
        if table == 2:
            print("Add a assembly part")
            assemblyName = input("Enter Assembly Name: ")
            assemblyNumber = input("Enter Assembly Number: ")
            if add_assembly(assemblyName, assemblyNumber):
                print(f"assembly part: {assemblyName} added to assembly parts table and parts table")
                listAssemblyParts(engine)
        if table == 3:
            print("Add a piece part")
            pieceName = input("Enter Piece Name: ")
            pieceNumber = input("Enter Piece Number: ")
            vendor = input("Enter Vendor Name: ")
            if add_piece_part(pieceName, pieceNumber, vendor):
                print(f"piece part: {pieceName} added to piece parts table and parts table")  
                listPieceParts(engine)
                
        if table == 4:
            print ("Add a Usage")
            assembly = input("Enter Assembly Name: ")
            component = input("Enter Component Name: ")
            usage = (int(input("Enter Usage Quantity: ")))
            if add_usage(assembly, component, usage):
                print(f"Quantity: {usage} of {component} for {assembly} added to Usages")
                listUsages(engine)
        if table == 5:
            print("Add a part")
            partName = input("(Enter Part Name: ")
            partNumber = input("Enter Part Number: ")
            try:
                ptype = int(input("is it an [1] assembly or [2] piece piece part?\n"))
            except ValueError:
                print("Must enter 1 or 2")
                session.rollback()
            if ptype == 1:
                if add_assembly(partName, partNumber):
                    print("assembly part: {partName} added")
                    listAssemblyParts(engine)
            elif ptype == 2:
                vendor = input("\nEnter Vendor Name: ")
                if add_piece_part(partName, partNumber, vendor):
                    print(f"piece part: {partName} added")  
                    listPieceParts(engine)
                
        if table == 6:
            print("returning to Main Menu ...")
            repeat = 1
            break
        if repeat == 0:
            repeat = input("Would you like to record new rows?: Y/N\n")
            if repeat == "Y" or repeat == "y":
                repeat = 0
            else:
                print("returning to Main Menu ...")
                repeat = 1


#delete; different from insertion, I call the delete check functions from check.py 
# to prevent orphans in the deleteOperations method
#decorator and wrapper to reuse logic
def delete(table):
    if table.__tablename__ not in table.metadata.tables:
        raise ValueError(f"Table '{table.__tablename__}' does not exist in metadata.")

    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            key = func(*args, **kwargs)
            with Session() as session:
                row = session.query(table).filter_by(**key).first()
                if row is None:
                        print("Row Not Found...")
                        return None
                session.delete(row)
                session.commit()
                print("Row successfully deleted.")
                return row
        return wrapper
    return decorator


@delete(Vendor)
def delete_vendor(name: str):
    return{
        "supplierName": name
    }
    
@delete(Part)
def delete_part(name: str):
    return{
        "partName": name
    }

@delete(AssemblyPart)
def delete_assembly(name: str):
    return{
        "assemblyPartName": name
    }

@delete(PiecePart)
def delete_piece_part(name: str):
    return{
        "piecePartName": name
    }

@delete(Usage)
def delete_usage(assembly:str, component:str):
    return{
        "assemblyPartName": assembly,
        "componentPartName": component
        }


#deletion operations
#include parts because type is not really required to delete 

def deleteOperations():
    print("Which table would you like to delete a row from?\n")
    table = viewTableMenu();
    if table == 1:
        v = input("Enter the name of the Vendor that you would like to delete:\n")
        if deleteVendorSafetyCheck(v): #does the vendor have piece parts referencing them?
            if delete_vendor(v):#if false the error will print and exit
                listVendors(engine)
                print(f"{v} has been successfully deleted!\n")
    elif table == 2:
        a = input("Enter the name of the assembly part that you would like to delete: ") 
        if deletePartSafetyCheck(a): #existing usages = reject
            if delete_assembly(a):
                listAssemblyParts(engine)
                print(f"{a} has been successfully deleted!\n")
            else: return
    elif table ==3:
        p = input("Enter the name of the piece part that you would like to delete: ") 
        if deletePartSafetyCheck(p):
            if delete_piece_part(p):
                listPieceParts(engine)
                print(f"{p} has been successfully deleted!\n")
            else: return
    elif table == 4:
        ua = input("Enter the name of the assembly part for the usage you would like to delete: ") 
        uc = input("Enter the name of the component part that you would like to delete: ") 
        if delete_usage(ua, uc): #usage is not a parent table so no worries about orphans
            listUsages(engine)
            print(f"Usage has been successfully deleted!\n")
    elif table == 5:
        p = input("Enter the name of the Part that you would like to delete: ")
        if deletePartSafetyCheck(p):
            if delete_part(p):
                listParts(engine)
                print(f"{p} has been successfully deleted!\n")
    return
        
    
#update operations: validator/db constraints checked through try, except ValueError, exceptIntegrityError, and
def updateOperations():
    print("Which table would you like to update a row from?\n")
    table=opTableMenu()
    if table==1:
        old=input("Enter the current Vendor name: ")
        with Session() as session:
            v=session.query(Vendor).filter_by(supplierName=old).first()
            if v:
                try:
                    new=input("Enter the new Vendor name: ")
                    v.supplierName=new
                    session.query(PiecePart).filter_by(vendorSupplierName = old).update({"vendorSupplierName": new})
                    session.commit()
                    listVendors(engine)
                    print(f"{old} has been successfully updated to {new}!\n")
                except ValueError as e: #validator
                    session.rollback()
                    print(e)
                except IntegrityError as e: #DB constraints
                    session.rollback()
                    print("Error Update Fail: ", e.orig)
            else:
                print(f"Vendor: {old} not found...")
    elif table==2:
        old=input("Enter the current Assembly Part name: ")
        #update through parts and partType 
        with Session() as session:
            a=session.query(Part).filter_by(partName=old, partType="assembly_part").first()
            if a:
                try: #will automatically update assembly table
                    new=input("Enter the new Assembly Part name: ")
                    newNum=input("Enter the new Assembly Part number: ")
                    a.partName=new
                    a.partNumber=newNum
                    a.partType = "assembly_part"
                    
                    session.query(AssemblyPart).filter_by(assemblyPartName=old).update({"assemblyPartName":new})
                    session.query(Usage).filter_by(assemblyPartName=old).update({"assemblyPartName":new})
                    session.query(Usage).filter_by(componentPartName=old).update({"componentPartName":new})
                    session.commit()
                    listAssemblyParts(engine)
                    print(f"{old} has been successfully updated to {new}!\n")
                except ValueError as e:
                    session.rollback()
                    print(f"\nValidation Error Fail '{old}': {e}\n")

                except IntegrityError as e:
                    session.rollback()
                    print(f"\nDB Error Fail '{old}': {e.orig}\n")
            else:
                print(f"\nError: '{old}' is not an Assembly Part or does not exist.\n")

    elif table==3:
        old=input("Enter the Piece Part name: ")
        with Session() as session:
            p=session.query(Part).filter_by(partName=old,partType="piece_part").first()
            if p:
                try: #will update piece part table
                    new=input("Enter the new Piece Part name: ")
                    newNum=input("Enter the new Piece Part number: ")
                    newV=input("Enter New Vendor Name: ")
                    vCheck = session.query(Vendor).filter_by(supplierName = newV).first()
                    #vendor check
                    if vCheck is None:
                        print("Error: Entered Vendor does not exist....")
                        session.rollback()
                        return

                    p.partName=new
                    p.partNumber=newNum
                    p.partType = "piece_part"
                    session.query(PiecePart).filter_by(piecePartName=old).update({"piecePartName": new,"vendorSupplierName": newV})
                    
                    session.query(Usage).filter_by(componentPartName=old).update({"componentPartName":new})
                    session.commit()
                    listPieceParts(engine)
                    print(f"{old} has been successfully updated to {new}!\n")
                except ValueError as e:
                    session.rollback()
                    print(f"\nValidation Error Update Fail: {e}\n")
                except IntegrityError as e:
                    session.rollback()
                    print(f"\nDB Error Update Fail: {e.orig}\n")
            else:
                print(f"\nError: '{old}' is not a Piece Part or does not exist.\n")
                return


    elif table==4:
        a=input("Enter the Assembly Part name: ")
        c=input("Enter the Component Part name: ")
        with Session() as session:
            u=session.query(Usage).filter_by(assemblyPartName=a,componentPartName=c).first()
            if u:
                try:
                    try:
                        qty=int(input("Enter the new quantity: "))
                    except ValueError:
                        print("\nError: quantity must be a number.\n")
                        return
                    
                    na = input("Enter updated Assembly: ")
                    nc = input("Enter updated component: ")
                    #update
                    u.usageQuantity=qty
                    u.assemblyPartName = na
                    u.componentPartName = nc
                    if not validate_before_up(session, u): #check py: assembly and component must be already recorded in parts
                        print("\nUpdate aborted due to invalid references.\n")
                        return
                    session.commit()
                    listUsages(engine)
                    print(f"Usage quantity has been successfully updated to {qty}!\n")
                except ValueError as e:
                    session.rollback()
                    print(e)
                except IntegrityError as e:
                    session.rollback()
                    print(f"\nDB Error Update Fail: {e.orig}\n")
            else:
                print("Usage row not found....\n")
    elif table==5:
        return

    
