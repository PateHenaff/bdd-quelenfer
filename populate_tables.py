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

serveur = metadata.tables["serveur"]
infrastructure = metadata.tables["infrastructure"]
utilisateur = metadata.tables["utilisateur"]
groupe = metadata.tables["groupe"]
switch_virtuel = metadata.tables["switch_virtuel"]
machine = metadata.tables["machine"]
relier = metadata.tables["relier"]

database=[]

try :
    database.append((serveur,1000))
    database.append((infrastructure,1000))
    database.append((utilisateur,1000))
    database.append((groupe,2000))
    database.append((switch_virtuel,1000))
    database.append((machine,1500))
    database.append((relier,1500))
except KeyError as err:
    print("error : Metadata.tables "+str(err)+" not found")

# product list
sexe_list = ["m","f"]
type_groupe_list=['type1', 'type2', 'type3']
os_list=['Windows10', 'Windows8', 'Debian10', 'Windows NT 4', 'MacOS10', 'Windows XP SP2', 'Windows Vista', 'kali','MacOS13']

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
        if self.table.name == "serveur":
            with engine.begin() as conn:
                for _ in range(self.num_records):
                    insert_stmt = self.table.insert().values(
                        #idServeur = faker.first_name(),
                    )
                    conn.execute(insert_stmt)

        if self.table.name == "infrastructure":
            with engine.begin() as conn:
                for _ in range(self.num_records):
                    insert_stmt = self.table.insert().values(
                        #idInfrastructure = faker.first_name(),
                        idServeur = random.choice(conn.execute(select([serveur.c.idServeur])).fetchall())[0]
                    )
                    conn.execute(insert_stmt)

        if self.table.name == "utilisateur":
            with engine.begin() as conn:
                for _ in range(self.num_records):
                    insert_stmt = self.table.insert().values(
                        #idUtilisateur = faker.first_name(),
                        nomUtilisateur = faker.last_name(),
                        prenomUtilisateur = faker.first_name(),
                        naissanceUtilisateur = faker.date_of_birth(minimum_age=13, maximum_age=80),
                        sexeUtilisateur = random.choice(sexe_list)
                    )
                    conn.execute(insert_stmt)

        if self.table.name == "groupe":
            with engine.begin() as conn:
                for _ in range(self.num_records):
                    insert_stmt = self.table.insert().values(
                        #idGroupe = random.choice(product_list),
                        typeGroupe = random.choice(type_groupe_list),
                        nomGroupe = faker.company()
                    )
                    conn.execute(insert_stmt)

        if self.table.name == "switch_virtuel":
            with engine.begin() as conn:
                for _ in range(self.num_records):
                    insert_stmt = self.table.insert().values(
                        #idSwitch = faker.address(),
                        idServeur = random.choice(conn.execute(select([serveur.c.idServeur])).fetchall())[0]
                    )
                    conn.execute(insert_stmt)

        if self.table.name == "machine":
            with engine.begin() as conn:
                for _ in range(self.num_records):
                    #date_obj = datetime.datetime.now() - datetime.timedelta(days=random.randint(0,30))
                    insert_stmt = self.table.insert().values(
                        #transaction_date=date_obj.strftime("%Y/%m/%d"),
                        #idMachine = faker.random_int(0,0)
                        nomMachine = faker.last_name(),
                        osMachien = random.choice(os_list),
                        ramMachine = faker.random_int(2,64),
                        coeurMachine = faker.random_int(2,32),
                        disqueDurMachine = faker.random_int(128,4096),
                        idInfrastructure = random.choice(conn.execute(select([infrastructure.c.idInfrastructure])).fetchall())[0],
                    )
                    conn.execute(insert_stmt)
        
        if self.table.name == "relier":
            with engine.begin() as conn:
                for _ in range(self.num_records):
                    date_obj = datetime.datetime.now() - datetime.timedelta(days=random.randint(0,30))

                    insert_stmt = self.table.insert().values(
                        idMachine=random.choice(conn.execute(select([infrastructure.c.idInfrastructure])).fetchall())[0],
                        idSwitch=random.choice(conn.execute(select([switch_virtuel.c.idSwitch])).fetchall())[0],
                        identifiant=faker.last_name()
                    )
                    conn.execute(insert_stmt)


if __name__ == "__main__":
    for i in database:
        generate_data = GenerateData(i)
        generate_data.create_data()
