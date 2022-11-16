from sqlalchemy import create_engine, MetaData, select
from faker import Faker
import sys
import random
import datetime
import configparser
from connect import engine

engine = engine
metadata = MetaData()
metadata.reflect(bind=engine)

# Instantiate faker object
faker = Faker()


Habitant = metadata.tables["Habitant"]
Adresse = metadata.tables["Adresse"]
roleVaccin = metadata.tables["roleVaccin"]
Infection = metadata.tables["Infection"]
regleVaccin = metadata.tables["regleVaccin"]
Vaccin = metadata.tables["Vaccin"]
Dose = metadata.tables["Dose"]
Maladie = metadata.tables["Maladie"]
etablissement = metadata.tables["etablissement"]

database=[]

try :
    database.append((Habitant,1000))
    database.append((Adresse,2000))
    database.append((roleVaccin,1000))
    database.append((Infection,1500))
    database.append((regleVaccin,1500))
    database.append((Vaccin,1500))
    database.append((Dose,1500))
    database.append((Maladie,1500))
    database.append((etablissement,1500))
except KeyError as err:
    print("error : Metadata.tables "+str(err)+" not found")

# product list
variant_list = ["BA1", "DELTA", "ORIGIN", "BA2", "OMICRON", "BA3", "BA4"]
etab_type_list = ['Laboratoire', 'Centre', 'Pharmacie', 'Medecin']

class GenerateData:
    """
    generate a specific number of records to a target table
    """

    def __init__(self,table):
        """
        initialize command line arguments
        """
        self.table = table[0]
        self.num_records = table[1]


    def create_data(self):
        """
        using faker library, generate data and execute DML
        """

        if self.table.name == "Habitant":
            with engine.begin() as conn:
                for _ in range(self.num_records):
                    insert_stmt = self.table.insert().values(

                    )
                    conn.execute(insert_stmt)

        if self.table.name == "Adresse":
            with engine.begin() as conn:
                for _ in range(self.num_records):
                    insert_stmt = self.table.insert().values(
                        voie = faker.address(),
                        code_postal = str(faker.random_int(10000,99000)),
                        numero = faker.random_int(1,1000),
                        ville = faker.city(),
                    )
                    conn.execute(insert_stmt)

        if self.table.name == "roleVaccin":
            with engine.begin() as conn:
                for _ in range(self.num_records):
                    insert_stmt = self.table.insert().values(
                        label=random.choice(conn.execute(select([Vaccin.c.id_vaccin])).fetchall())[0],
                    )
                    conn.execute(insert_stmt)

        if self.table.name == "Infection":
            with engine.begin() as conn:
                for _ in range(self.num_records):
                    insert_stmt = self.table.insert().values(
                        date_infection=faker.date_of_birth(minimum_age=0, maximum_age=5) #Sur les 5 dernieres annees
                    )
                    conn.execute(insert_stmt)

        if self.table.name == "regleVaccin":
            with engine.begin() as conn:
                for _ in range(self.num_records):
                    insert_stmt = self.table.insert().values(
                        label=random.choice(conn.execute(select([Vaccin.c.id_vaccin])).fetchall())[0],
                    )
                    conn.execute(insert_stmt)
        
        if self.table.name == "Dose":
            with engine.begin() as conn:
                for _ in range(self.num_records):
                    insert_stmt = self.table.insert().values(
                        date_administration=faker.date_of_birth(minimum_age=0, maximum_age=5), #Sur les 5 dernieres annees
                        id_vaccin=random.choice(conn.execute(select([Vaccin.c.id_vaccin])).fetchall())[0],
                    )
                    conn.execute(insert_stmt)

        if self.table.name == "Maladie":
            with engine.begin() as conn:
                for _ in range(self.num_records):
                    insert_stmt = self.table.insert().values(
                        variant=random.choice(variant_list)
                    )
                    conn.execute(insert_stmt)

        if self.table.name == "Etablissement":
            with engine.begin() as conn:
                for _ in range(self.num_records):
                    insert_stmt = self.table.insert().values(
                        type=random.choice(etab_type_list)
                    )
                    conn.execute(insert_stmt)


if __name__ == "__main__":
    for i in database:
        generate_data = GenerateData(i)
        generate_data.create_data()