class SatelliteProblem:
    def __init__(self, satellites, instruments, objectives):
        self.satellites = satellites  # Lista de satélites
        self.instruments = instruments  # Lista de instrumentos por satélite
        self.objectives = objectives  # Lista de objetivos
        self.state = {
            "posiciones": {sat: None for sat in satellites},  # Posición actual de cada satélite
            "calibrado": {sat: {inst: False for inst in instruments[sat]} for sat in satellites},
            "capturado": {obj: False for obj in objectives},
        }

    # Acción: Rotar el satélite
    def rotate(self, satellite, objective):
        self.state["posiciones"][satellite] = objective
        print(f"{satellite} rotado para apuntar a {objective}")

    # Acción: Calibrar un instrumento
    def calibrate(self, satellite, instrument):
        if self.state["posiciones"][satellite]:
            self.state["calibrado"][satellite][instrument] = True
            print(f"Instrumento {instrument} de {satellite} calibrado")
        else:
            print(f"{satellite} no apunta a ningún objetivo; calibración fallida")

    # Acción: Capturar una imagen o medición
    def capture(self, satellite, instrument, objective, resolution):
        if self.state["posiciones"][satellite] == objective and self.state["calibrado"][satellite][instrument]:
            self.state["capturado"][objective] = True
            self.state["calibrado"][satellite][instrument] = False
            print(f"Captura completada por {satellite} con {instrument} en resolución {resolution}")
        else:
            print(f"Error: {satellite} no está en posición o {instrument} no está calibrado")

    # Verificar si todos los objetivos han sido cumplidos
    def all_capturado(self):
        return all(self.state["capturado"].values())

# Ejemplo de uso
satellites = ["Sat1", "Sat2"]
instruments = {
    "Sat1": ["Cam1", "Med1"],
    "Sat2": ["Cam2", "Med2"]
}
objectives = ["Obj1", "Obj2"]

# Crear el problema
problem = SatelliteProblem(satellites, instruments, objectives)

# Planificación manual
problem.rotate("Sat1", "Obj1")
problem.calibrate("Sat1", "Cam1")
problem.capture("Sat1", "Cam1", "Obj1", "Alta")

problem.rotate("Sat2", "Obj2")
problem.calibrate("Sat2", "Med2")
problem.capture("Sat2", "Med2", "Obj2", "Baja")

# Verificar si todos los objetivos fueron cumplidos
if problem.all_capturado():
    print("Todos los objetivos han sido cumplidos")
else:
    print("Faltan objetivos por cumplir")
