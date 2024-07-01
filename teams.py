class Team:
    def __init__(self, name, code, group):
        self.name = name
        self.code = code
        self.group = group
    
    def __str__(self):
        return f'Equipo: {self.name}, Código FIFA: {self.code}, Grupo: {self.group}'

