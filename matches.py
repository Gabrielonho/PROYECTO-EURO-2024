class Match:
    def __init__(self, home_team, away_team, datetime, stadium, match_id, number):
        self.home_team = home_team
        self.away_team = away_team
        self.datetime = datetime
        self.stadium = stadium
        self.match_id = match_id
        self.number = number
        self.VIP = self.stadium.capacity[1]
        self.GENERAL = self.stadium.capacity[0]
        self.attendance = 0

    def __str__(self): #formato general para mostrar partidos
        return f'{self.home_team.name} vs {self.away_team.name}\n{self.datetime} en {self.stadium.name}\nID: {self.match_id}\n'
    
    def validate_ticket(self, ticket_id): #valida que un ticket se encuentre en los tickets vendidos
        with open("ticket_sales.txt", "r") as file:
            for line in file:
                if f"ticket_id: {ticket_id}" in line:
                    return True
        return False
    
    def is_ticket_validated(self, ticket_id): # dice si un ticket ya ha sido validado para negar su entrada
        with open("validated_tickets.txt", "r")as file:
            for line in file:
                if f"ticket_id: {ticket_id}" in line:
                    return True
        return False

    def update_available_seats(self, ticket_type, quantity):
        if ticket_type == 'VIP':
            self.VIP -= quantity
        if ticket_type == 'GENERAL':
            self.GENERAL
        self.save_seats_status()

    def save_seats_status(self):
        with open("seats_status.txt", "w") as file:
            file.write(f"Match ID: {self.match_id}\n")
            file.write(f"VIP seats: {self.VIP}\n")
            file.write(f"General seats: {self.GENERAL}\n\n")

    def load_seats_status(self):
        try:
            with open("seats_status.txt", "r") as file:
                lines = file.readlines()
                for i, line in enumerate(lines):
                    if f"Match ID: {self.match_id}" in line:
                        self.VIP = int(lines[i + 1].split(": ")[1])
                        self.GENERAL = int(lines[i + 2].split(": ")[1])
        except FileNotFoundError:
            self.save_seats_status() #crea el archivo si no existe
    
    def register_validated_ticket(self, ticket_id): # registra los tickets ya validados en un archivo .txt
        with open("validated_tickets.txt", "a") as file:
            file.write(f"ticket_id {ticket_id}\n")

                

    

