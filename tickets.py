from itertools import permutations
class Ticket:
    ticket_counter_vip = 1
    ticket_counter_general = 1

    def __init__(self, client_name, client_id, age, match, ticket_type):
        self.client_name = client_name
        self.client_id = client_id
        self.age = age
        self.match = match
        self.ticket_type = ticket_type
        self.price = self.calculate_price()
        self.id = self.generate_id()
        self.descuento = is_vampire_number(self.client_id)


    def calculate_price(self):
        base_price = 35 if self.ticket_type == 'GENERAL' else 75
        base_price_with_iva = base_price * 1.16
        if is_vampire_number(self.client_id):
            base_price_discounted = base_price * 0.5
            price_with_iva_discounted = base_price_discounted * 0.5
            return [base_price_discounted, price_with_iva_discounted]
        else:
            return [base_price, base_price_with_iva]
    
    def generate_id(self):
        if self.ticket_type == 'VIP':
            aux = (self.match.stadium.capacity[1]) - (self.match.VIP) + 1
            id = f"V.{aux}.{self.match.number}"
        elif self.ticket_type == "GENERAL":
            aux = (self.match.stadium.capacity[0]) - (self.match.GENERAL) + 1
            id = f"G.{aux} + 1.{self.match.number}"
        return id           

    def register_sale(self):
        with open("ticket_sales.txt", "a") as file:
            file.write(f"ticket_id: {self.id}, match: {self.match}type: {self.ticket_type}, price: {self.price}, client ID: {self.client_id}, client_age: {self.age}\n\n")

def is_vampire_number(number):
    # convertir el numero a un string para una manipulacion mas comoda
    number_str = str(number)
    length = len(number_str)

    # validación de que tiene una cantidad par de digitos
    if length % 2 != 0:
        return False

    # Generar todos los posibles pares de colmillos (la mitad de la longitud del numero original)
    half_length = length // 2
    potential_fangs = permutations(number_str, half_length)
    
    fangs_set = set()

    # revisar todos los pares de potenciales colmillos
    for fangs in potential_fangs:
        fangs_str = ''.join(fangs)
        # Asegurarse que ningun par de colmillos consiste en ser un cero a la izquierda
        if fangs_str[0] != '0':
            other_fangs = number_str
            for digit in fangs_str:
                other_fangs = other_fangs.replace(digit, '', 1)
            if other_fangs[0] != '0':
                # Convertir ambos pares de colmillos a numeros enteros
                fang1, fang2 = int(fangs_str), int(other_fangs)
                # Chequear si la multiplicacion de los colmillos es igual al numero original
                if fang1 * fang2 == number:
                    fangs_set.add((fang1, fang2))
    
    return bool(fangs_set)
