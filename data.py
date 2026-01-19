# seed_data.py
from db_connection import Session
from ORM import Vendor, PiecePart, AssemblyPart, Usage

def seed():
    with Session() as session:
        vendors=[
            "Helical International","Plates R Us","Wholey Rollers",
            "Jack Daniels Belts","Engine Accessories","Comp USA",
            "Unharnessed at Large","Get a Grip","Telegraph Inc.",
            "Radio Shack","Starbucks","Michaels","OSH"
        ]
        for name in vendors:
            session.add(Vendor(supplierName=name))
            
        piece_parts_data=[
            ("1.1.1.1","Springs","Helical International"),
            ("1.1.1.2","Torque","Plates R Us"),
            ("1.1.2.1","Rollers","Wholey Rollers"),
            ("1.1.3","Belt","Jack Daniels Belts"),
            ("1.2.1","Pistons","Engine Accessories"),
            ("1.2.2","Rings","Engine Accessories"),
            ("1.3.1","ECU","Comp USA"),
            ("1.3.2.1.1","Stator Wiring","Unharnessed at Large"),
            ("2.1.1","Grips","Get a Grip"),
            ("2.1.2.1","Cables","Telegraph Inc."),
            ("2.1.3","Kill Switch","Radio Shack"),
            ("2.2.1","Foam","Starbucks"),
            ("2.2.2","Fabric","Michaels"),
            ("2.3.1","Bulb","OSH"),
            ("2.3.2","Headlight Wiring","Unharnessed at Large")
        ]
        for num,name,vendor in piece_parts_data:
            session.add(
                PiecePart(
                    partName=name,
                    partNumber=num,
                    partType="piece_part",
                    piecePartName=name,
                    vendorSupplierName=vendor
                )
            )

        assemblies=[
            ("1","Engine"),("1.1","Transmission"),("1.1.1","Clutch"),
            ("1.1.2","Variator"),("1.2","Head"),("1.3","Battery"),
            ("1.3.2","Starter"),("1.3.2.1","Stator"),("2","Frame"),
            ("2.1","Handlebars"),("2.1.2","Throttle"),("2.2","Seat"),
            ("2.3","Headlight"),("0","Motorcycle")
        ]
        for num,name in assemblies:
            session.add(
                AssemblyPart(
                    partName=name,
                    partNumber=num,
                    partType="assembly_part",
                    assemblyPartName=name
                )
            )

        usages_data=[
            ("Engine","Transmission",1),
            ("Engine","Head",2),
            ("Engine","Battery",1),
            ("Transmission","Clutch",1),
            ("Transmission","Variator",1),
            ("Transmission","Belt",1),
            ("Clutch","Springs",4),
            ("Clutch","Torque",1),
            ("Variator","Rollers",5),
            ("Head","Pistons",2),
            ("Head","Rings",2),
            ("Battery","ECU",1),
            ("Battery","Starter",1),
            ("Starter","Stator",1),
            ("Stator","Stator Wiring",1),
            ("Frame","Handlebars",1),
            ("Frame","Seat",1),
            ("Frame","Headlight",1),
            ("Handlebars","Grips",2),
            ("Handlebars","Throttle",1),
            ("Handlebars","Kill Switch",1),
            ("Throttle","Cables",1),
            ("Seat","Foam",1),
            ("Seat","Fabric",1),
            ("Headlight","Bulb",1),
            ("Headlight","Headlight Wiring",1),
            ("Motorcycle","Engine",1),
            ("Motorcycle","Frame",1)
        ]
        for a,c,q in usages_data:
            session.add(
                Usage(
                    assemblyPartName=a,
                    componentPartName=c,
                    usageQuantity=q
                )
            )

        session.commit()
        print("Database seeded successfully.")

if __name__=="__main__":
    seed()
