from sqlalchemy import create_engine, MetaData, \
    Column, Integer, Numeric, String, Date, Table, ForeignKey
import configparser
from connect import engine

engine = engine
metadata = MetaData()
metadata.reflect(bind=engine)


# DDL for customers, products, stores, and transactions
adherent_table = Table(
    "adherant",
    metadata,
    Column("num_inscription", Integer, primary_key=True),
    Column("date_inscription", Date, nullable=False)
    
)

historique_table = Table(
    "historique",
    metadata,
    Column("id_historique", Integer, primary_key=True),
    Column("gain", Integer, nullable=False),
    Column("num_inscription", ForeignKey("adherent.num_inscription"), nullable=False)
)

choix_table = Table(
    "choix",
    metadata,
    Column("id_choix", Integer, primary_key=True),
    Column("choix", Integer, nullable=True),
    Column("id_historique", ForeignKey("historique.id_historique"), nullable=False)
)

partie_table = Table(
    "partie",
    metadata,
    Column("num_tournois", Integer, primary_key=True),
    Column("date_tournois", Date, nullable=False),
    Column("num_inscription", ForeignKey("adherent.num_inscription"), nullable=False),
    Column("id_historique", ForeignKey("historique.id_historique"), nullable=False)
)
tour_table = Table(
    "tour",
    metadata,
    Column("tour", Integer, primary_key=True),
    Column("gain_tour", Integer, nullable=False),
    Column("num_tournois", ForeignKey("partie.num_tournois"), nullable=False),
    Column("num_inscription", ForeignKey("adherant.num_inscription"), nullable=False)
)
tour_table = Table(
    "tour",
    metadata,
    Column("tour", Integer, primary_key=True),
    Column("gain_tour", Integer, nullable=False),
    Column("num_tournois", ForeignKey("partie.num_tournois"), nullable=False),
    Column("num_inscription", ForeignKey("adherant.num_inscription"), nullable=False)
)
resultat_table = Table(
    "resultat",
    metadata,
    Column("resultat", Integer, primary_key=True),
    Column("tour", ForeignKey("tour.tour"), nullable=False)
)

# Start transaction to commit DDL to postgres database
with engine.begin() as conn:
    metadata.create_all(conn)

    for table in metadata.tables.keys():
        print(f"{table} successfully created")
