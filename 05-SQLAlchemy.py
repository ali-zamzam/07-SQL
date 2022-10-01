import sqlite3

import sqlalchemy
from IPython.display import Markdown, display
from sqlalchemy import (
    Column,
    ForeignKey,
    Integer,
    MetaData,
    String,
    Table,
    create_engine,
    inspect,
    text,
)

"""SQLAlchemy is a Python library widely used to connect to a relational database management system, it allows you to
 interpret SQL code.

We will use an SQLite database, which is lighter and easier to use than most other SGDBRs.

The first important object of this module is the engine. It allows us to connect to a database and perform SQL queries 
in text format. The create_engine function creates a connection with a database. If it does not exist, the function will 
create one. The argument is a character string in the following format: 'sqlite:///path_to_the_database.db'

a) Create a connection to the chinook.db database which you now know well"""

engine = create_engine("sqlite:///chinook.db", echo=True)
# En ajoutant l'argument echo = True, cela nous permet d'afficher la traduction en langage SQL des commandes du module

"""Une classe très pratique pour afficher des informations sur la base est l'Inspector, c'est un outil précieux pour 
comprendre à la fois le schéma des données ainsi que les contraintes qui s'opèrent entre elles.

b) Exécuter la cellule suivante afin d'instancier la classe Inspector dans une variable nommée inspector."""
inspector = inspect(engine)

"""A l'aide de cet objet, on va pouvoir récupérer le nom des différentes tables qui constituent la base de données. 
La méthode get_table_names nous permet de le faire.

c) Exécuter la cellule suivante pour afficher les différentes tables présentes dans la base de données."""
inspector.get_table_names()


"""La méthode get_columns de la classe Inspector permet d'afficher les caractéristiques des différents attributs d'une table passée en argument.

d) Afficher les attributs de la table albums à l'aide de la cellule suivante."""
inspector.get_columns(table_name="albums")

""" Remarquez que l'objet retourné est une liste de 3 éléments. Chacun de ces éléments regroupent les 
informations d'un attribut de la table. On peut y trouver le nom de la table mais aussi un argument 
**primary_key qui est fixé à 1** si l'attribut est une clé primaire."""


"""La méthode get_foreign_keys de l'objet inspector permet d'afficher les clés étrangères associées à une table passée en argument.

e) afficher les clés étrangères de la table albums à l'aide de la cellule suivante."""
inspector.get_foreign_keys(table_name="albums")


"""Pour effectuer des requêtes SQL, on a besoin d'une connexion avec l'objet engine. Pour cela on utilise la méthode connect qui renvoie une instance de la classe Connection.

f) Instancier la classe Connection dans une variable nommée conn."""
conn = engine.connect()


"""On peut désormais utiliser la méthode execute associée à une instance de la classe Connection crée précédemment.

Elle prend en argument une chaîne de caractères qui correspond à notre requête en langage SQL.

Pour obtenir le résultat de cette requête dans Python, on utilise la méthode fetchallassociée à cet objet.

g) Afficher 10 lignes de la colonne Title de la table Albums.
Afin de s'assurer que notre requête soit bien interprétée par SQLAlchemy on utilisera la fonction text précédemment importée."""

stmt = text("SELECT Title FROM albums LIMIT 10;")
result = conn.execute(stmt)
result.fetchall()


"""h) Pour chaque commande de la table invoices, le prix est identifié par Total. Afficher le montant total des commandes 
par identifiant client CustomerId à l'aide de la méthode GROUP BY, on pourra les trier par ordre décroissant."""

stmt = text(
    "SELECT invoices.CustomerId , SUM(Total) AS tot FROM invoices GROUP BY CustomerId ORDER BY tot DESC;"
)
result = conn.execute(stmt)
result.fetchall()
# ----------------------------------------------------------------------------------------------------------------
"""Création de table"""

"""Nous allons reprendre le notebook numéro 4 donc vous allez à nouveau voir comment alimenter la base college.db avec les parcours pédagogiques d'un établissement d'enseignement et les étudiants qui suivent des cours là-bas, mais en utilisant cette fois-ci la syntaxe SQLAlchemy.

L'objet créé par la fonction MetaData permet de regrouper plusieurs informations concernant une ou plusieurs bases de données, notamment des informations sur les tables qui la composent, on utilisera cet objet lors de leurs créations.

i) Créer une base de données college.db."""

engine = create_engine("sqlite:///college.db", echo=True)


"""j) instancier un objet de la classe MetaData nommé meta."""
meta = MetaData()


"""Pour créer une table on fait appel à la classe Table. Cette fonction est liée à l'objet engine. 
Les deux premiers arguments sont le nom de la table, ainsi que l'objet meta que l'on a créé précédemment. 
Les arguments restants sont des objets de type Column représentant chacun un attribut de la table. 
Le constructeur de cet objet prend en arguments un nom, le type de l'attribut (String, Integer, ...) 
et s'il s'agit d'une clé primaire ou pas (primary_key=True)."""

"""Il est possible que des erreurs surviennent dans ce module puisque vous allez créer, modifier et supprimer des 
éléments d'une base de données, reset le kernel ne suffira pas à réinitialiser la base. Si un problème survient, 
le plus simple est de supprimer les tables que vous avez créées et qui posent problème avec 
la commande sql = text('DROP TABLE IF EXISTS parcours;') et result = engine.execute(sql) et de vous réferer ensuite 
aux cellules de correction. Cette manipulation sera détaillée davantage dans la dernière section de ce cours.
"""
"""
k) Créer une table parcours qui permettra d'identifier la filière de l'étudiant au sein de l'établissement. 
Cette table aura comme attributs l'identifiant id du parcours qui sera une clé primaire et son nom name.
l) utiliser la méthode create_all associée à l'objet meta pour sauvegarder les changements sur la base de donneés 
(l'argument pris par cette fonction est un objet engine).
"""

parcours = Table(
    "parcours", meta, Column("id", Integer, primary_key=True), Column("name", String)
)

meta.create_all(engine)


"""m) créer une table students ayant comme attributs un identifiant id qui en sera la clé primaire, un prénom firstname 
au format String, un nom lastname au format String, ainsi que l'identifiant parcours_id du parcours suivi qui est 
une clé étrangère.
On pourra préciser une clé étrangère en utilisant la syntaxe suivante :"""

Column("colonne_name", type, ForeignKey("table_name.colonne_name"))


students = Table(
    "students",
    meta,
    Column("id", Integer, primary_key=True),
    Column("firstname", String),
    Column("lastname", String),
    Column("parcours_id", Integer, ForeignKey("parcours.id")),
)

meta.create_all(engine)
# ----------------------------------------------------------------------------------------------------------------
"""Modifications de table"""

"""Lorsque l'on modifie ou effectue une ou plusieurs opération(s) importante(s) sur une table, il est nécessaire de 
se prévenir de toute erreur de manipulation. Pour créer une transaction il faut connecter la machine à l'aide de la 
méthode connect de l'engine."""

"""Une transaction a un début et une fin. Le début de la transaction est indiqué par la fonction begin associée à 
l'objet précédemment créé par la méthode connect.

Via cet objet, on pourra appeller la fonction rollback dans le cas où une opération de la transaction 
n'a pas été autorisée : on revient à l'état initial de la table.

La fonction commit permet elle de valider la transaction le cas échéant. En Python, cela nous donne la structure suivante:"""

# on crée la connection
with engine.connect() as connection:
    # début de la transaction
    with connection.begin() as transaction:
        # on tente d'éxécuter une transaction
        try:
            connection.execute(instruction)
        # si la transaction échoue
        except:
            transaction.rollback()
            raise
        # si la transaction réussit
        else:
            transaction.commit()

"""L'argument instruction correspond à l'opération qui sera effectuée au sein de la transaction.

Lorsqu'on effectue une requête, qui est la forme de transaction la plus simple, ce fonctionnement est fait implicitement."""
# **************
"""Insertion de lignes
Dans une table, on peut insérer ou supprimer des lignes. Ces opérations sont considérées comme des transactions et sont 
donc soumises aux règles qui assurent la cohérence de la base de données.

Pour insérer des tuples, on doit d'abord créer une liste qui contient des tuples. Ces tuples doivent représenter 
les valeurs des différents attributs de la table : la liste a donc la longueur du nombre de lignes qu'on veut 
insérer et chaque tuple a le même nombre d'entrées que la table."""

"""n) Créer une liste values1 contenant les informations des 2 parcours de la table parcours, on les identifiera par 
(1, "Data Engineering") et (2, "Data Science"). Créer une liste values2 contenant les informations de 2 étudiants de 
la table students, on choisira les noms et prénoms que l'on souhaite. Attention cependant à bien respecter les 
contraintes liées à l'unicité de la clé primaire et à l'existence de la clé étrangère."""

values1 = [
    (1, "Data Engineering"),
    (2, "Data Science"),
]

values2 = [
    (1, "Jean", "Dubois", 1),
    (2, "Martin", "Dupont", 2),
]


"""La syntaxe SQL pour ajouter un tuple dans une table est la suivante :

INSERT INTO nom_table 
VALUES tuple;
Cette commande est en langage SQL, et sera donc au format texte sous python si on souhaite l'exécuter.

On note 'INSERT INTO {tablename} VALUES ({markers})' où tablename sera le nom de la table et markers sera une variable 
explicitant le format des tuples que l'on injectera dans la table.

Une fois le tablename et le markers définis, on peut mettre à jour notre requête SQL en modifiant son format à l'aide 
de la méthode format de Python (doc) permettant des substitutions de valeurs et des mises en forme à l'intérieur de 
chaînes de caractères.

Cela permet que tablename et markers ne soit pas considéré comme une chaîne de caractères mais bien un argument.

Pour définir correctement un markers, on peut utiliser la fonction suivante ','.join( '?' * len(values[0])) qui 
 permet de définir un format correspondant à un tuple de la bonne longueur.

o) Exécuter la cellule suivante pour insérer dans la table parcours les valeurs précédemment définies dans la liste values1."""
# on crée la connection
with engine.connect() as connection:
    # début de la transaction
    with connection.begin() as transaction:
        # on tente d'éxécuter une transaction
        try:
            # On indique le format d'un tuple de cette table
            markers = ",".join("?" * len(values1[0]))

            # On utilise le langage SQL en format texte où markers est le format d'un tuple
            ins = "INSERT INTO {tablename} VALUES ({markers})"

            # On précise ce format particulier grâce à la fonction membre format
            ins = ins.format(tablename=parcours.name, markers=markers)

            # Enfin on peut utiliser les tuples créés en éxécutant la commande SQL
            connection.execute(ins, values1)
        # si la transaction échoue
        except:
            transaction.rollback()
            raise
        # si la transaction réussit
        else:
            transaction.commit()
#  Si vous exécutez 2 fois le code précédent, une erreur apparaîtra car les tuples sont déjà présent dans la base.
# La contrainte d'unicité de la clé primaire n'est alors plus respectée.

"""p) En utilisant une transaction SQLAlchemy, insérer dans la table students les valeurs précédemment définies dans 
la liste values2."""

# Solution

with engine.connect() as connection:
    with connection.begin() as transaction:
        try:
            markers = ",".join("?" * len(values2[0]))
            ins = "INSERT INTO {tablename} VALUES ({markers})"

            ins = ins.format(tablename=students.name, markers=markers)
            connection.execute(ins, values2)
        except:
            transaction.rollback()
            raise
        else:
            transaction.commit()


"""q) Vous pouvez lancer la cellule suivante pour voir les éléments contenus dans les bases."""
# Exécuter cette cellule
with engine.connect() as connection:
    results = connection.execute("SELECT * FROM students;")
    print(results.fetchall())

with engine.connect() as connection:
    results = connection.execute("SELECT * FROM parcours;")
    print(results.fetchall())
# ------------------------------------------------------------------------------------------------
"""Suppression de table"""

"""Si l'on souhaite supprimer des lignes, il faut faire attention à la cohérence de la base de données. 
Dans notre exemple, on ne peut pas suprimer uniquement le tuple d'un des deux parcours de la table parcours. 
En effet, dans la table students un des attributs fait référence à la clé primaire d'un parcours. Cet attribut n'aurait 
donc plus de sens, et les transactions ACID nous permettent d'interdire ce genre de transaction.

Si un parcours est retiré du programme de l'université et doit être retiré de la base, il faut aussi supprimer 
 les lignes des étudiants associés (ici les étudiants suivent 1 seul cursus et sont donc malheureusement mis à la porte...) 
 dans la table students. Pour supprimer ou modifier une ligne en particulier, il faut utiliser vos connaissances 
 en langage SQL, notamment en ce qui concerne la recherche de tuple vérifiant une condition
On va procéder plus simplement ici et supprimer la table students.

r) Supprimer la table students de la base de donnée à l'aide des connaissances acquises jusqu'ici en SQL et SQLAlchemy. 
Puis vérifier qu'elle est bien supprimée en essayant d'y insérer un tuple.
"""
sql = text("DROP TABLE IF EXISTS students;")
result = engine.execute(sql)

###Vérification que la table students n'existe plus en réutilisant le code d'insertion de tuple

# values = [
#    (1,"Jean", "Dubois", 1),
#    (2,"Martin", "Dupont", 2),
#    ]
#
# with engine.connect() as connection:
#    with connection.begin() as transaction:
#        try:
#            markers = ','.join('?' * len(values[0]))
#            ins = 'INSERT INTO students VALUES ({markers})'
#            ins = ins.format(tablename=students.name, markers=markers)
#            connection.execute(ins, values)
#        except:
#            transaction.rollback()
#            raise
#        else:
#            transaction.commit()

# ------------------------------------------------------------------------------------------------
"""Conclusion
Dans ce cours nous avons vu la structure à utiliser pour se connecter à une base de données et effectuer des requêtes sur une base de données relationnelles, ce qu'il faut retenir :

la structure de connection à une base de données avec SQLAlchemy
la syntaxe pour effectuer des requêtes SQL à l'aide de SQLAlchemy
la syntaxe pour créer, modifier ou supprimer une table en SQL"""
