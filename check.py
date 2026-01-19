from functools import wraps
import sqlalchemy as sa
from ORM import *
from db_connection import Session

#these are used to ensure uniqueness constraints get raised
def check_unique_constraint(sess, constraint, instance):
    python_class=instance.__class__
    mapper=sa.inspect(python_class)
    columns=mapper.c.keys()
    keys=mapper.attrs.keys()
    uk_cols=constraint["column_names"]
    filters=[]
    for key in uk_cols:
        attr_name=""
        for attribute_name in keys:
            if attribute_name in columns:
                if mapper.c[attribute_name].name==key:
                    attr_name=attribute_name
                    break
        if not attr_name:
            raise ValueError(f"Could not find mapped attribute for column '{key}' on {python_class.__name__}")
        filters.append(getattr(python_class,attr_name)==getattr(instance,attr_name))
    q=sess.query(python_class).filter(*filters)
    count=q.count()
    if count==1:
        return q.first()
    else:
        return None

#pk constraints
def check_unique(sess,class_instance):
    results=[]
    python_class=class_instance.__class__
    table_name=python_class.__table__.name
    bind=sess.get_bind()
    inspector=sa.inspect(bind)
    primary_key=inspector.get_pk_constraint(table_name)
    unique_constraints=inspector.get_unique_constraints(table_name)
    constraints=[{"name":primary_key["name"],"column_names":primary_key["constrained_columns"]}]
    for uk in unique_constraints:
        constraints.append({"name":uk["name"],"column_names":uk["column_names"]})
    for constraint in constraints:
        if check_unique_constraint(sess,constraint,class_instance):
            results.append(constraint)
    return results

#insertion; to hold referential integrity for migrated fks in piece parts and usages 
def validate_before_insert(sess,instance)->bool:
    violations=check_unique(sess,instance)
    if violations:
        names=[c["name"] for c in violations]
        print("Uniqueness constraint(s) violated:",", ".join(names))
        return False
    if isinstance(instance,PiecePart):
        vname=instance.vendorSupplierName
        exists=sess.query(Vendor).filter_by(supplierName=vname).first()
        if exists is None:
            print(f"\nError: Vendor '{vname}' does not exist.\Insert Failed\n")
            return False
    if not validate_before_up(sess,instance):
        return False
    return True

#for updating a usage, we need to ensure that the new assembly input and component input exists within the recorded parts
#referential integrity for vendors is implemented in updateOperations() of operations.py
def validate_before_up(sess,instance)->bool:
    if isinstance(instance,Usage):
        aname=instance.assemblyPartName
        cname=instance.componentPartName
        a_exists=sess.query(AssemblyPart).filter_by(assemblyPartName=aname).first()
        if a_exists is None:
            print(f"\nError: Assembly Part '{aname}' does not exist.\n")
            return False
        c_exists=sess.query(Part).filter_by(partName=cname).first()
        if c_exists is None:
            print(f"Error: Component Part '{cname}' does not exist.")
            return False
    return True

#when deleting a part reject any that populate a usage to prevent orphans
def deletePartSafetyCheck(name:str):
    with Session() as session:
        c=session.query(Usage).filter_by(componentPartName=name).first() is not None
        u=session.query(Usage).filter_by(assemblyPartName=name).first() is not None
        if c or u:
            print("Error!!!: Can not delete part; it is still referenced in one or more Usages")
            return False
    return True


#when deleting a vendor reject any that have piece parts to prevent orphans
def deleteVendorSafetyCheck(name:str):
    with Session() as session:
        p=session.query(PiecePart).filter_by(vendorSupplierName=name).first() is not None
        if p:
            print("Error!!!: Can not delete Vendor; it is still referenced in one or more Piece Parts")
            return False
    return True
