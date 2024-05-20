# Solution: Multiple.
# Result: Correct.

# Task could be submitted multiple times for points by answering the various questions.
# A couple questions have issues - Organizers admitted this. Eventually we got all points though. 



import pandas as pd
import sqlite3

con = sqlite3.connect("excercises/intel_3/Universum.db/universe.db")

# Not really required but a quick peak at the data
cursor = con.cursor()
cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
for table in cursor.fetchall():
   table = table[0]
   print("Tables:", table)
   _ = cursor.execute(f"SELECT * FROM {table};")
   print("Columns:", [col_schema[0] for col_schema in cursor.description])
   _ = cursor.execute(f"SELECT COUNT(*) FROM {table};")
   print("Rows:", cursor.fetchone()[0])

cursor.close()

# 1) Welk Zonnestelsel heeft het hoogste aantal planeten?
# Done & Correct!
# Extra info: Multiple correct answers, pick the one with the highest id.
# Solution: 1-cmsBWzdnIO

query = """
SELECT
   solar_systems.name,
   solar_systems.id,
   COUNT(planets.id) AS count
FROM planets
LEFT JOIN solar_systems ON solar_systems.id = planets.solar_system_id
GROUP BY solar_system_id
ORDER BY COUNT(planets.id) DESC;
"""

df = pd.read_sql_query(query, con)
# Should only be 1 option but issue with question.
flags = df[df['count'] == df['count'].max()]
# Get the name that belongs to the solar system with "the longest id" which should also be the highest.
print(f"1-{flags.name[flags.id.idxmax()]}")


# 2) Hoeveel Zonnestelsels hebben geen inwoners?
# DONE & Correct!
# Note, this is technically incorrect. Solar systems without planets are not considered.
# Solution: 2-633352

query = """
SELECT
   solar_system_id,
   SUM(inhabitants) AS n
FROM planets
GROUP BY solar_system_id
HAVING SUM(inhabitants) = 0
"""

df = pd.read_sql_query(query, con)
print(f"2-{df.shape[0]}")


# Not correct for the task but technically correct, includes solar systems with 0 planets.

query = """
SELECT
   solar_systems.id,
   SUM(inhabitants) AS n
FROM solar_systems
LEFT JOIN planets ON solar_systems.id = planets.solar_system_id
GROUP BY solar_systems.id
HAVING SUM(inhabitants) = 0 OR inhabitants IS NULL 
"""

df = pd.read_sql_query(query, con)
print(f"Alternative 2-{df.shape[0]}")


# 3) Welk Hypercluster heeft de planeet met de meeste inwoners?
# DONE and correct!
# Solution: 3-uZthRhZfne

# Not the most efficient way to do this...
df = pd.read_sql_query("SELECT MAX(inhabitants) AS n FROM planets LIMIT 1", con)
target = df.n[0]

df = pd.read_sql_query("SELECT solar_system_id, name FROM planets WHERE inhabitants = ?", con, params=(target,))
target = df.solar_system_id[0]

df = pd.read_sql_query("SELECT galaxy_id FROM solar_systems WHERE id = ?", con, params=(int(target),))
target = df.galaxy_id[0]

df = pd.read_sql_query("SELECT supercluster_id FROM galaxies WHERE id = ?", con, params=(int(target),))
target = df.supercluster_id[0]

df = pd.read_sql_query("SELECT hypercluster_id FROM superclusters WHERE id = ?", con, params=(int(target),))
target = df.hypercluster_id[0]

df = pd.read_sql_query("SELECT name FROM hyperclusters WHERE id = ?", con, params=(int(target),))
print(f"3-{df.name[0]}")


#4) Hoe zwaar is het Supercluster met de grootste totale massa (afgerond op gehele massa-eenheden)?
# DONE and correct!
# Solution: 4-460986

query = """
 SELECT superclusters.name AS cluster, planets.mass
 FROM superclusters 
 LEFT JOIN galaxies ON galaxies.supercluster_id =  superclusters.id
 LEFT JOIN solar_systems ON solar_systems.galaxy_id =  galaxies.id
 LEFT JOIN planets ON planets.solar_system_id =  solar_systems.id;
"""

df = pd.read_sql_query(query, con)

df_sums = df.groupby(["cluster"]).mass.sum()
target = df_sums[df_sums == df_sums.max()]
print(f"4-{round(target.iloc[0])}")



#5) Wat is het gemiddeld aantal zonnestelsels per Supercluster (afgerond op 2 decimalen)?
# DONE and correct.
# Answer again doesnt consider clusters with 0 galaxies and galaxies with 0 solarsystems.
# Solution: 5-5.30
query = """
   SELECT 
	 superclusters.id AS id,
    solar_systems.id AS solar_id
   FROM superclusters
   LEFT JOIN galaxies ON galaxies.supercluster_id =  superclusters.id
   LEFT JOIN solar_systems ON solar_systems.galaxy_id =  galaxies.id
"""

df = pd.read_sql_query(query, con)

# Correct
answer = round(df["id"].value_counts().mean(), 2)
print(f"5-{answer}0")
# Technically correct
answer = round(df.groupby("id").solar_id.count().mean(), 2)
print(f"5-{answer}0")



#6) Welk Zonnestelsel heeft de laagste gemiddelde massa per planeet?
# DONE and correct!
# Solution: 6-giUBWXGwdz 

# Use planets as a base, don't need to deal with solar systems without planets
query = """
 SELECT DISTINCT
 solar_systems.name AS solar,
 AVG(planets.mass) AS mass
 FROM planets 
 LEFT JOIN solar_systems ON planets.solar_system_id =  solar_systems.id
 GROUP BY solar
 ORDER BY mass
 LIMIT 5
"""

#7) Welke bewoonde planeet met minder dan 500 inwoners heeft de hoogste massa?
# Done and correct
# Solution: 7-YTlXCnqJaK
query = """
SELECT id, name, mass, inhabitants
FROM planets
WHERE inhabitants > 0 AND inhabitants < 500
ORDER BY mass DESC
LIMIT 5
"""

df = pd.read_sql_query(query, con)
planet = df["name"][0]
print(f"7-{planet}")


con.close()