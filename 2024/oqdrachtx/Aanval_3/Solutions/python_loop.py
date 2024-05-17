base = "2024/oqdrachtx/Aanval_3/Galactisch Krachtveld/"

with open(base + "force_fields_log.txt", "r") as fin:
    lines = fin.readlines()[8:]


class Planet:
    def __init__(self, name):
        self.name = name
        self.BO = False
        self.BA = False
        self.BE = False


planets = {}

for line in lines:
    timestamp, code, planet, *args = line.split(", ")

    if planet not in planets:
        planets[planet] = Planet(planet)
    p = planets[planet]

    if "BO" in code:
        p.BO = True
    if "BA" in code:
        p.BA = True
    if "BE" in code:
        p.BE = True

possible_planets = []
for name, planet in planets.items():
    if planet.BE and planet.BO and planet.BA:
        possible_planets.append(name)

possible_planets.sort()
print(f"The targeted planets should be: {','.join(possible_planets)}")
