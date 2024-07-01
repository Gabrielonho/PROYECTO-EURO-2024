import requests
from unidecode import unidecode
from teams import Team
from stadiums import Stadium
from matches import Match
from tickets import Ticket
from products import Product, Beverage, Food
from clients import Client
from products import is_perfect_number

def teams_record(): #Registra los equipos de la api en una lista de objetos team con sus respectivos atributos 
    response = requests.get('https://raw.githubusercontent.com/Algoritmos-y-Programacion/api-proyecto/main/teams.json')
    teams_data = response.json()
    teams = []
    for team_data in teams_data:
        team = Team(team_data['name'], team_data['code'], team_data['group'])
        teams.append(team)
    return teams

def stadium_record(): #Registra los estadios de la api en una lista de objetos stadium con sus respectivos atributos
    response = requests.get('https://raw.githubusercontent.com/Algoritmos-y-Programacion/api-proyecto/main/stadiums.json')
    stadiums_data = response.json()
    stadiums = []
    for stadium_data in stadiums_data:
        stadium = Stadium(stadium_data['name'], stadium_data['id'], stadium_data['city'], stadium_data['capacity'])
        stadiums.append(stadium)
    return stadiums

def matches_record(teams, stadiums): #Registra los partidos de la api en una lista de objetos match con sus respectivos atributos
    response = requests.get('https://raw.githubusercontent.com/Algoritmos-y-Programacion/api-proyecto/main/matches.json')
    matches_data = response.json()
    matches = []
    for match_data in matches_data:
        try:
            home_team = next(team for team in teams if team.code == match_data['home']['code'])
            away_team = next(team for team in teams if team.code == match_data['away']['code'])
            stadium = next(stadium for stadium in stadiums if stadium.id == match_data['stadium_id'])
        except StopIteration as e:
            print(f"Error: no se pudo encontrar un equipo o estadio que coincida con el partido: {match_data}.")
            continue
        match = Match(home_team, away_team, match_data['date'], stadium, match_data['id'], match_data['number'] )
        matches.append(match)
    return matches

def products_record():
    response = requests.get('https://raw.githubusercontent.com/Algoritmos-y-Programacion/api-proyecto/main/stadiums.json')
    stadiums_data = response.json()
    products = []

    for stadium_data in stadiums_data:
        for restaurant in stadium_data['restaurants']:
            for product in restaurant['products']:
                if 'alcoholic' in product['adicional']:
                    beverage = Beverage(product['name'], product['adicional'], product['price'], product['stock'])
                    products.append(beverage)
                elif 'package' in product['adicional'] or 'plate' in product['adicional']:
                    food = Food(product['name'], product['adicional'], product['price'], product['stock'])
                    products.append(food)
    return products

def display_products():
    response = requests.get('https://raw.githubusercontent.com/Algoritmos-y-Programacion/api-proyecto/main/stadiums.json')
    stadiums_data = response.json()

    stadium_input = input("Ingrese el nombre del estadio: ").strip().lower()
    selected_stadium = next((stadium for stadium in stadiums_data if stadium_input in unidecode(stadium['name'].strip().lower())), None)

    if not selected_stadium:
        print(f"No se encontró el estadio que estás buscando. Por favor inténtalo de nuevo.")
        return display_products()
    
    print(f"\nRestaurantes en el estadio {selected_stadium['name']}:\n")
    for index, restaurant in enumerate(selected_stadium['restaurants']):
        print(f"{index +1}. {restaurant['name']}")

    restaurant_input = int(input("\nSeleccione el número del restaurante que desea ver: ").strip())

    if restaurant_input < 1 or restaurant_input > len(selected_stadium['restaurants']):
        print("Número de restaurante inválido. Por favor, inténtelo de nuevo.")
        return display_products()

    selected_restaurant = selected_stadium['restaurants'][restaurant_input - 1]
    print(f"\nProductos en el restaurante {selected_restaurant['name']}:\n")
    for product in selected_restaurant['products']:
        if 'alcoholic' in product['adicional']:
            beverage = Beverage(product['name'], product['adicional'], product['price'], product['stock'])
            print(beverage)
        elif 'plate' in product['adicional'] or 'package' in product['adicional']:
            food = Food(product['name'], product['adicional'], product['price'], product['stock'])
            print(food)



def display_team_info(matches): #Imprime los partidos del equipo que coloque el usuario
    team_input = input("Ingrese el nombre (en inglés) o el código FIFA del equipo de tu interés: ").strip()
    selected_team_code = next((team for team in teams if team_input.upper() in team.code), None)
    selected_team_name = next((team for team in teams if team_input.lower() in team.name.lower()), None) #estos son para poder encontrar lo que escriba el usuario, ya sea por codigo o por nombre
    if selected_team_code: 
        print(f"\nDatos del equipo {selected_team_code.name} (Código: {selected_team_code.code}):") #algunos datos del equipo cuando se encuentra por codigo
        print(f"Grupo: {selected_team_code.group}")
        print(f"\nPartidos de la fase de grupos:\n")
        for match in matches:
            if match.home_team.code == selected_team_code.code or match.away_team.code == selected_team_code.code: #los partidos del equipo
                print(f"- {match.home_team.name} vs {match.away_team.name}")
                print(f"En {match.stadium.name} el dia {match.datetime}")
                print(f"ID: {match.match_id}\n")
    elif selected_team_name:
        print(f"\nDatos del equipo {selected_team_name.name} (Código: {selected_team_name.code}):") # algunos datos cuando se busca por nombre
        print(f"Grupo: {selected_team_name.group}")
        print(f"\nPartidos de la fase de grupos:\n")
        for match in matches:
            if match.home_team.code == selected_team_name.code or match.away_team.code == selected_team_name.code: #los partidos del equipo
                print(f"- {match.home_team.name} vs {match.away_team.name}")
                print(f"En {match.stadium.name} el dia {match.datetime}")
                print(f"ID: {match.match_id}\n")
    else: 
        print(f"No se encontró el equipo con el código o nombre {team_input}. Por favor, inténtelo de nuevo.") #cuando no se encuentra un selected_team
        display_team_info(matches)

def display_matches_by_stadium(stadiums, matches): # busca los partidos que hay en el estadio que coloca el usuario
    stadium_input = input("Ingrese el nombre del estadio: ").strip().lower()
    selected_stadium = next((stadium for stadium in stadiums if stadium_input in unidecode(stadium.name.strip().lower())), None) #identifica el estadio colocado por el usuario
    if selected_stadium:
        print(f"\nPartidos en {selected_stadium}:") # imprime los partidos
        for match in matches:
            if match.stadium == selected_stadium:
                print(match)
    else: 
        print(f"No se encontró el equipo con el código o nombre {stadium_input}. Por favor, inténtelo de nuevo.") # para cuando no se encuentra el estadio
        display_matches_by_stadium()

def display_matches_by_date(matches): # muestra los partidos de la fecha en cuestion
    date_input = input("ingrese la fecha cumpliendo el formato (YYYY-MM-DD): ").strip()
    print(f"\nPartidos en la fecha {date_input}:\n")
    for match in matches: 
        if match.datetime.startswith(date_input): # imprime los partidos con la misma fecha que coloco el usuario
            print(match)
        else: 
            print(f"No se encontró ningún partido en la fecha {date_input} o la fecha está colocada en un distinto formato. Por favor inténtelo de nuevo.") # para cuando se coloca una fecha equivocada

def display_teams(teams): # imprime los objetos team de la lista teams
    for team in teams:
        print(team)

def display_matches(matches): # es para imprimir los partidos con un buen formato
    for match in matches:
        print(f"- {match.home_team.name} - {match.away_team.name}")
        print(f"En {match.stadium.name} el dia {match.datetime}")
        print(f"ID: {match.match_id}\n")

def display_stadiums(stadiums): # muestra los objteos stadium en la lista stadiums
    for stadium in stadiums:
        print(stadium)

def process_ticket_sale(): # es para hacer el procedimiento de compra de tickets
    subtotal = 0 # esta es la variable subtotal de precio
    available_matches = display_available_matches(matches) # llama a la funcion que imprime los partidos cuyos asientos disponibles son mayores a 0
    match_num = input("\nColoque el número del partido al que desea comprar entradas: ").strip() # pide el partido al que se quiere asistir
    try:
        match_num = int(match_num)
    except ValueError:
        print("Número de partido inválido. Por favor, inténtelo de nuevo.")
        return process_ticket_sale() # esto es para evitar errores por tipos de datos

    selected_match = next((match for match in available_matches if match.number == match_num), None) # selecciona un partido a partir del numero dado por el usuario
    if not selected_match:
        print("Número de partido inválido. Por favor, inténtelo de nuevo.") # para cuando no se necuentra un partido
        return process_ticket_sale()
    
    ticket_type = input('Ingrese el tipo de entrada que desea ("VIP" o "General"): ').strip().upper() # pide el tipo de entrada
    if ticket_type not in ['VIP', 'GENERAL']:
        print("Tipo de ticket inválido. Por favor, inténtelo de nuevo.")
        process_ticket_sale()
    try: 
        if ticket_type == 'VIP':                 # muestra los asientos disponibles segun el tipo de entrada
            print(f"La cantidad de asientos VIP disponibles son: {selected_match.VIP}.") 
        if ticket_type == 'GENERAL':
            print(f"La cantidad de asientos general(es) disponibles son: {selected_match.GENERAL}.")
    except ValueError:
        print("Entrada no válida. Por favor, ingrese un número.") # mas validaciones
        return process_ticket_sale()
    with open('clients.txt', 'r') as file:
        for line in file:
            client_name = line[0].strip().strip('[]').split(', ')
            client_id = line[1].strip().strip('[]').split(', ')
            client_age = line[2].strip().strip('[]').split(', ')
    ticket = Ticket(client_name, client_id, client_age, selected_match, ticket_type) # guarda el objeto ticket
    ticket.register_sale() # registra el ticket en el txt
    subtotal = ticket.price[0] # añade el precio al subtotal
    if ticket.descuento:
        print(f"¡Felicidades! Ha recibido un descuento. Una o varias de sus entradas han recibido un descuento del 50% ")
    print(f"El subtotal a pagar es {subtotal}.")
    print(f"El total a pagar (con IVA) es {subtotal*1.16}. ¿Desea realizar el pago? (S/N)")
    response = input().upper()
    if response == "S":
        print(f"¡Compra exitosa! Usted a comprado un ticket {ticket_type} para el partido {selected_match.home_team.name} vs {selected_match.away_team.name} en {selected_match.stadium.name} el {selected_match.datetime}.")
        selected_match.update_available_seats(ticket_type, 1)
        print(f"El ID de su boleto es: {ticket.id}")    # le muestra los datos de la compra al usuario y le enseña el id del ticket    
        return 
    if response == "N":
        print(f"Pago cancelado.")
        return
    else: 
        print("Por favor ingrese una respuesta válida (S/N).") # mas validaciones
        return 

def verify_existing_id(id):
    with open('clients.txt', 'r') as file:
        for line in file:
            data = line.strip().strip('[]').split(', ')
            if data[1] == str(id):
                return True
    return False

def register_client():
    answer = input("¿Ya estás registrado/a? (S/N): ").strip().upper()
    if answer == "S":
        id = int(input("Por favor ingrese su cedula (sólo números): "))
        if verify_existing_id(id):
            print("Sesión iniciada con éxito. ")
            return False
    elif answer == "N":
        with open('clients.txt', 'a') as file:
            client_name = input("Ingrese su nombre: ")        # pide todos los datos a los clientes
            try:
                client_id = int(input("Ingrese su cédula (Sólo números): "))
                client_age = int(input("Ingrese su edad(Sólo números):  "))
                if client_age <= 0 or client_id <= 0: 
                    print("La edad o la identificación del cliente no son válidas. ")
                    return
                elif verify_existing_id(client_id):
                    print("Esa identificación ya está registrada en el sistema.")
                    return
            except ValueError:
                print("Entrada no válida. Por favor, ingrese un número.") # aun mas validaciones
                return
            client = Client(client_name, client_id, client_age)
            file.write(f"[{client.name}, {client.id}, {client.age}]\n")
            print("¡Usuario registrado con éxito!")
    else:
        print("Respuesta inválida. Por favor, inténtelo de nuevo, recuerde, responda con 'S'/'N'.")
        return register_client()
    return False

def display_available_matches(matches): # muestra los partidos con asientos disponibles para la compra
    available_matches = [] 
    print("\nPartidos disponibles para la venta de tickets: \n")
    for match in matches:  #Hace una lista de los partidos con asientos disponibles
        if match.VIP > 0 or match.GENERAL > 0:
            available_matches.append(match)
    
    # Ordenar la lista por el número del partido
    available_matches.sort(key=lambda match: match.number)
    
    for match in available_matches: # imprime cada partido de la lista con un formato mas agradable
        print(f"{match.number}. {match.home_team.name} vs {match.away_team.name}")
        print(f"  En {match.stadium.name} el dia {match.datetime}")
        print(f"  Asientos VIP disponibles: {match.VIP}")
        print(f"  Asientos generales disponibles: {match.GENERAL}\n")
    
    return available_matches

def check_ticket_validity(matches): # revisa si el ticket ha sido comprado para validarlo
    ticket_id = input("Ingrese el código único del boleto de entrada: ")
    for match in matches: # valida que el ticket este en los tickets ya vendidos
        if match.validate_ticket(ticket_id):
            match.register_validated_ticket(ticket_id)
            match.attendance += 1
            with open("validated_tickets.txt", "r") as file: # revisa si ya ha sido validado antes
                for line in file:
                    if f"ticket_id: {ticket_id}" in line:
                        print("El boleto ya ha sido validado anteriomente. No puede pasar")
                print("¡El boleto es válido! Asistencia registrada.") # si no ha sido valiado anteriormente, se valida y se da acceso
                return
    print("No se encontró ningún partido asociado a ese boleto o el boleto no es válido.") # por si no se encuentra el id en los tickets vendidos
    return 

def verify_vip_purchase(client_id):
    with open('ticket_sales.txt', 'r') as file:
        for line in file:
            try:
                data = line.strip().strip('[]').split(', ')
                if len(data) >= 2 and data[1] == str(client_id) and "VIP" in data:
                    return True
            except ValueError:
                continue
    return False  # esto me esta dando problemas, no supe como saber si se habia comprado vip o no :(

def process_restaurant_sale():
    client_id = int(input("Ingrese su cédula: ").strip())
    with open('clients.txt', 'r') as file:
        for line in file:
            data = line.strip().strip('[]').split(', ')
            client_age = data[2]

     #if not verify_vip_purchase(client_id):
        #print("Usted no ha comprado una entrada VIP. Por lo tanto no puede realizar compras en los restaurante.")
        #return
    selected_products = []
    total_amount = 0

    while True:
        product_name = input("Ingrese el nombre del producto que desea comprar (o 'fin' para terminar): ").strip()
        if product_name.lower() == 'fin':
            return

        product = next((p for p in products if p.name.lower() == product_name.lower()), None)
        if not product:
            print("Producto no encontrado. Intente nuevamente.")
            continue

        if isinstance(product, Beverage) and product.is_alcoholic and client_age < 18:
            print("No puede comprar bebidas alcohólicas si es menor de 18 años.")
            continue

        quantity = int(input(f"Ingrese la cantidad de {product_name} que desea comprar: ").strip())
        if not product.register_sale(quantity):
            print(f"No hay suficiente stock de {product_name}. Stock disponible: {product.stock}")
            continue

        selected_products.append((product, quantity))
        total_amount += product.price * quantity

    if is_perfect_number(client_id):
        discount = total_amount * 0.15
    else:
        discount = 0

    total_with_discount = total_amount - discount

    print("\nResumen de su compra:")
    for product, quantity in selected_products:
        print(f"{product.name} x{quantity} - Precio: {product.price:.2f} c/u")

    print(f"Subtotal: {total_amount:.2f}")
    if discount > 0:
        print(f"Descuento: -{discount:.2f}")
    print(f"Total a pagar: {total_with_discount:.2f}")

    response = input("¿Desea proceder con el pago? (S/N): ").strip().upper()
    if response == 'S':
        print("¡Pago exitoso! Gracias por su compra.")
    else:
        print("Compra cancelada. Los productos no se descontarán del inventario.")

# Asume que ya tienes una lista de productos cargada en `products`
products = products_record()

def first_time():  #es para que el usuario se tenga que registrar solo la primera vez que ejecuta el programa 
    if register_client() == True:
        return True
    else:
        return False
    
def menu(): # todo el menu de inicio
    if first_time():
        register_client()
    while True:
        print("\n⚽️ Bienvenido al sistema oficial de la Eurocopa ⚽️")
        print("1. Ver equipos")
        print("2. Ver estadios")
        print("3. Ver partidos")
        print("4. Buscar equipo")
        print("5. Buscar estadio")
        print("6. Buscar partidos por fecha")
        print("7. Comprar entradas")
        print("8. Validar ticket")
        print("9. Ver productos de un restaurante")
        print("10. Comprar en un restaurante")
        print("11. Registrar nuevo usuario")
        print("x. Salir")
        option = int(input("Elige una opción: ").strip())
        if option == 1:
            display_teams(teams)
        elif option == 2:
            display_stadiums(stadiums)
        elif option == 3:
            display_matches(matches)
        elif option == 4:
            display_team_info(matches)
        elif option == 5:
            display_matches_by_stadium(stadiums, matches)
        elif option == 6:
            display_matches_by_date(matches)
        elif option == 7:
            process_ticket_sale()
        elif option == 8:
            check_ticket_validity(matches)
        elif option == 9:
            display_products()
        elif option == 10:
            process_restaurant_sale()
        elif option == 11:
            register_client()                           
        elif option == "x":
            print("Hasta luego, muchas gracias por utilizar el sistema oficial de la Euro.")
            break
        else: 
            print("Opción no válida. Por favor, inténtalo de nuevo.")
            return

teams = teams_record() # guarda los objetos team de la funcion en una lista teams
stadiums = stadium_record() # guarda los objetos stadium de la funcion en una lista stadiums
matches = matches_record(teams, stadiums) # guarda los objetos match de la funcion en una lista matches
for match in matches:    # esto es para cargar el estado de los asientos de cada partido del .txt
    match.load_seats_status()
menu()