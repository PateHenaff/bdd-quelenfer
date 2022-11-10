from sqlalchemy import create_engine, MetaData, \
    Column, Integer, Numeric, String, Date, Table, ForeignKey
import configparser
from connect import engine

engine = engine
metadata = MetaData()
metadata.reflect(bind=engine)


# DDL for customers, products, stores, and transactions
Habitant_table = Table(
    "Habitant",
    metadata,
    Column("id_secu", String(35), primary_key=True)
)

Adresse_table = Table(
    "Adresse",
    metadata,
    Column("voie", String(35), primary_key=True),
    Column("Code Postale", String(35), nullable=False),
    Column("Numéro", Integer, nullable=False),
    Column("Ville", String(35), nullable=False)
)

roleVaccin_table = Table(
    "roleVaccin",
    metadata,
    Column("id_role", String(35), primary_key=True),
    Column("label", ForeignKey("Vaccin.id_vaccin"), nullable=False)
)

Infection_table = Table(
    "Infection",
    metadata,
    Column("date_infection", String(35), primary_key=True)
)

regleVaccin_table = Table(
    "regleVaccin",
    metadata,
    Column("id_regle", String(35), primary_key=True),
    Column("label", ForeignKey("Vaccin.id_vaccin"), nullable=False)
)

Vaccin_table = Table(
    "Vaccin",
    metadata,
    Column("id_Vaccin", String(35), primary_key=True),
    Column("label", String(35), nullable=False)
)

Dose_table = Table(
    "Dose",
    metadata,
    Column("date_administration", String(35), primary_key=True)
)

Maladie_table = Table(
    "Maladie",
    metadata,
    Column("id_maladie", String(35), primary_key=True),
    Column("variant", String(35), nullable=False)
)

etablissement_table = Table(
    "etablissement",
    metadata,
    Column("code_indentification", String(35), primary_key=True),
    Column("type", String(35), nullable=False)
)

# Start transaction to commit DDL to postgres database
with engine.begin() as conn:
    metadata.create_all(conn)

    for table in metadata.tables.keys():
        print(f"{table} successfully created")
