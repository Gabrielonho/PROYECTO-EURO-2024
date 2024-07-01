class Product:
    def __init__(self, name, classification, price, stock):
        self.name = name
        self.classification = classification
        self.price = price #FALTA AGREGAR IVA
        self.stock = stock
    
    def __str__(self):
        return f" Nombre: {self.name} Clase: {self.classification}\nPrecio: {self.price}"
    
class Beverage(Product):
    def __init__(self, name, is_alcoholic, price, stock):
        super().__init__(name, "Bebida", price, stock)
        self.is_alcoholic = "Sí" if is_alcoholic else "No"
        
    
    def __str__(self):
        return f"Nombre: {self.name}, Clase: Bebida, Alcohólica: {self.is_alcoholic}\nStock: {self.stock}\nPrecio: {self.price}"
    
class Food(Product):
    def __init__(self, name, packaging, price, stock):
        super().__init__(name, "Alimento", price, stock)
        self.packaging = "Empaquetado" if packaging == "package" else "En Plato"


    def __str__(self):
        return f"Nombre: {self.name}, Clase: Alimento, {self.packaging}\nStock{self.stock}\nPrecio: {self.price}"   


    def register_sale(self, quantity):
        if quantity <= self.stock:
            self.stock -= quantity
            return True
        else:
            return False
    
    def calculate_price(self, n):
        base_price = 123
        base_price_with_iva = base_price * 1.16
        if is_perfect_number(n):
            base_price_discounted = base_price * 0.5
            price_with_iva_discounted = base_price_discounted * 0.5
            return [base_price_discounted, price_with_iva_discounted]
        else:
            return [base_price, base_price_with_iva]        

def is_perfect_number(n):
    return n > 1 and sum(i for i in range(1, n) if n % i == 0) == n

    
