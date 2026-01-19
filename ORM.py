from typing import List, Optional 
from sqlalchemy import *
from sqlalchemy.orm import *

Base = declarative_base()

#parts
class Part(Base):
    __tablename__ = "parts"

    partName: Mapped[str] = mapped_column("part_name", String(80), nullable=False)
    partNumber: Mapped[str] = mapped_column("part_number", String(10), nullable=False)
    partType: Mapped[str] = mapped_column("part_type", String(50), nullable=False)

    componentUsages: Mapped[List["Usage"]] = relationship("Usage", back_populates="component")

#for subclasses in UML
    __mapper_args__ = {"polymorphic_on": partType, "polymorphic_identity": "part"}
#pk uniqueness and check constraints
    __table_args__ = (
        PrimaryKeyConstraint("part_name", name="parts_pk"),
        CheckConstraint("length(part_name) >= 3", name="part_name_length_check_01"),
        CheckConstraint("length(part_number) >= 1", name="part_number_min_check_01"),
        UniqueConstraint("part_number", name="parts_part_number_uk"),
    )

#validators which will be called for any insertion or update
    @validates("partName")
    def validatePartName(self, key, value: str) -> str:
        if value is None or len(value) < 3 or len(value) > 80:
            raise ValueError("\nPart Name must be between 3 and 80 characters long")
        return value

    @validates("partNumber")
    def validatePartNumber(self, key, value: str) -> str:
        if value is None or len(value) < 1 or len(value) > 10:
            raise ValueError("\nPart Number must be between 1 and 10 characters long")
        return value


class AssemblyPart(Part):
    __tablename__ = "assembly_parts"

    assemblyPartName: Mapped[str] = mapped_column("assembly_part_name", String(80), ForeignKey("parts.part_name", name="assembly_parts_parts_fk_01",), nullable=False,)

    assemblyUsages: Mapped[List["Usage"]] = relationship("Usage", back_populates="assembly")

    __mapper_args__ = {"polymorphic_identity": "assembly_part"}

    __table_args__ = (
        PrimaryKeyConstraint("assembly_part_name", name="assembly_parts_pk"),
    )


class PiecePart(Part):
    __tablename__ = "piece_parts"

    piecePartName: Mapped[str] = mapped_column("piece_part_name", String(80), ForeignKey("parts.part_name", name="piece_parts_parts_fk_01"), nullable=False)

    vendorSupplierName: Mapped[str] = mapped_column("vendors_supplier_name", String(80), ForeignKey("vendors.supplier_name"), nullable=False)
    
    vendor: Mapped["Vendor"] = relationship("Vendor", back_populates="pieceParts")

    __mapper_args__ = {"polymorphic_identity": "piece_part"}

    __table_args__ = (
        PrimaryKeyConstraint("piece_part_name", name="piece_parts_pk"),
    )


class Vendor(Base):
    __tablename__ = "vendors"

    supplierName: Mapped[str] = mapped_column("supplier_name", String(80), nullable=False)
    
    pieceParts: Mapped[List["PiecePart"]] = relationship("PiecePart", back_populates="vendor")

    __table_args__ = (
        PrimaryKeyConstraint("supplier_name", name="vendors_pk"),
        CheckConstraint("length(supplier_name) >= 3", name="supplier_name_check_01"),
    )

#validator for check constraint
    @validates("supplierName")
    def validateSupplierName(self, key, value: str) -> str:
        if value is None or len(value) < 3 or len(value) > 80:
            raise ValueError("\nSupplier Name must be between 3 and 80 characters long")
        return value


class Usage(Base):
    __tablename__ = "usages"

    assemblyPartName: Mapped[str] = mapped_column("assembly_parts_part_name", String(80), ForeignKey("assembly_parts.assembly_part_name", name="usages_assembly_parts_fk_01"), nullable=False)
    componentPartName: Mapped[str] = mapped_column("component_part_name", String(80), ForeignKey("parts.part_name", name="usages_parts_fk_01"), nullable=False)
    usageQuantity: Mapped[int] = mapped_column("usage_quantity", Integer, nullable=False)

    assembly: Mapped["AssemblyPart"] = relationship("AssemblyPart", back_populates="assemblyUsages", foreign_keys=[assemblyPartName])

    component: Mapped["Part"] = relationship("Part", back_populates="componentUsages", foreign_keys=[componentPartName])

    __table_args__ = (
        PrimaryKeyConstraint("assembly_parts_part_name", "component_part_name", name="usages_pk"),
        CheckConstraint("usage_quantity >= 1", name="ck_usages_usage_quantity"),
        CheckConstraint("assembly_parts_part_name != component_part_name", name="usages_assembly_component_diff_check_01"),
    )

    @validates("usageQuantity")
    def validateUsageQuantity(self, key, value: int) -> int:
        if value is None or value < 1 or value > 10:
            raise ValueError("\nUsage Quantity must be between 1 and 10")
        return value
