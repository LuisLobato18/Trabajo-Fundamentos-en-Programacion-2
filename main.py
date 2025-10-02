from datetime import datetime
import uuid

VALID_PRIORIDADES = {'alta', 'media', 'baja'}
VALID_ESTADOS = {'pendiente', 'en proceso', 'cerrado'}

class Ticket:
    """
    Representa un ticket de incidencia.
    """
    def _init_(self, cliente, prioridad='media', comentario_inicial=None):
        self.id = str(uuid.uuid4())
        self.cliente = cliente
        self.tecnico = None
        self.prioridad = prioridad
        self.estado = 'pendiente'
        self.fecha_creacion = datetime.now()
        self.comentarios = []
        if comentario_inicial:
            self.agregar_comentario(comentario_inicial)

    def agregar_comentario(self, texto):
        self.comentarios.append(f"{texto}")

    def _repr_(self):
        return (f"Ticket(id={self.id}, cliente={self.cliente.nombre}, "
                f"tecnico={(self.tecnico.nombre if self.tecnico else 'Sin asignar')}, "
                f"prioridad={self.prioridad}, estado={self.estado})")

class User:
    def _init_(self, nombre, correo):
        self.nombre = nombre.strip()
        self.correo = correo.strip()

class Client(User):
    pass

class Technician(User):
    def _repr_(self):
        return f"Technician(nombre={self.nombre}, correo={self.correo})"

class TicketManager:
    def _init_(self):
        self.tickets = []
        self.tecnicos = []

    def registrar_tecnico(self, nombre, correo):
        if not nombre or not correo:
            print("Nombre y correo no pueden estar vacíos.")
            return None
        tecnico = Technician(nombre, correo)
        self.tecnicos.append(tecnico)
        print(f"Técnico registrado: {tecnico.nombre} ({tecnico.correo})")
        return tecnico

    def registrar_ticket(self, cliente_nombre, prioridad='media', comentario_inicial=None):
        if not cliente_nombre:
            print("El nombre del cliente no puede estar vacío.")
            return None
        if prioridad not in VALID_PRIORIDADES:
            print(f"Prioridad inválida. Use: {', '.join(VALID_PRIORIDADES)}")
            return None
        cliente = Client(cliente_nombre, '')
        ticket = Ticket(cliente, prioridad, comentario_inicial)
        self.tickets.append(ticket)
        print(f"Ticket registrado: {ticket.id} para cliente {cliente.nombre} con prioridad {prioridad} - Fecha: {ticket.fecha_creacion}")
        if comentario_inicial:
            print(f"  Comentario inicial agregado.")
        return ticket

    def asignar_tecnico(self, ticket_id, tecnico_nombre):
        ticket = self._buscar_ticket(ticket_id)
        tecnico = self._buscar_tecnico(tecnico_nombre)
        if ticket and tecnico:
            ticket.tecnico = tecnico
            print(f"Ticket {ticket.id} asignado a {tecnico.nombre}.")

    def actualizar_estado(self, ticket_id, nuevo_estado):
        ticket = self._buscar_ticket(ticket_id)
        if not ticket:
            return
        if nuevo_estado not in VALID_ESTADOS:
            print(f"Estado inválido. Use: {', '.join(VALID_ESTADOS)}")
            return
        ticket.estado = nuevo_estado
        print(f"Ticket {ticket.id} actualizado a estado '{ticket.estado}'.")

    def listar_tickets_por_tecnico(self, tecnico_nombre):
        tecnico = self._buscar_tecnico(tecnico_nombre)
        if not tecnico:
            return []
        asignados = [t for t in self.tickets if t.tecnico == tecnico]
        self._imprimir_lista(asignados, f"Tickets asignados a {tecnico.nombre}:")
        return asignados

    def listar_tickets_por_cliente(self, cliente_nombre):
        encontrados = [t for t in self.tickets if t.cliente.nombre == cliente_nombre]
        self._imprimir_lista(encontrados, f"Tickets del cliente {cliente_nombre}:")
        return encontrados

    def filtrar_tickets(self, estado=None, prioridad=None, tecnico_nombre=None):
        filtrados = self.tickets
        if estado:
            filtrados = [t for t in filtrados if t.estado == estado]
        if prioridad:
            filtrados = [t for t in filtrados if t.prioridad == prioridad]
        if tecnico_nombre:
            tecn = self._buscar_tecnico(tecnico_nombre)
            filtrados = [t for t in filtrados if t.tecnico == tecn]
        self._imprimir_lista(filtrados, "Tickets filtrados:")
        return filtrados

    def _buscar_ticket(self, ticket_id):
        ticket = next((t for t in self.tickets if t.id == ticket_id), None)
        if not ticket:
            print("Ticket no encontrado.")
        return ticket

    def _buscar_tecnico(self, nombre):
        tecnico = next((tech for tech in self.tecnicos if tech.nombre == nombre), None)
        if not tecnico:
            print("Técnico no encontrado.")
        return tecnico

    def _imprimir_lista(self, lista, titulo):
        print(titulo)
        if not lista:
            print("No se encontraron tickets.")
        for t in lista:
            print(t)
            if t.comentarios:
                print("  Comentarios:")
                for c in t.comentarios:
                    print(f"    - {c}")





def mostrar_menu():
    print("\n----- Q-Track Menu -----")
    print("1. Registrar técnico")
    print("2. Registrar ticket")
    print("3. Asignar técnico a ticket")
    print("4. Actualizar estado de ticket")
    print("5. Listar tickets por técnico")
    print("6. Listar tickets por cliente")
    print("7. Filtrar tickets")
    print("8. Salir")


def main():
    manager = TicketManager()
    while True:
        mostrar_menu()
        opcion = input("Seleccione una opción: ")
        if opcion == '1':
            nombre = input("Nombre del técnico: ")
            correo = input("Correo del técnico: ")
            manager.registrar_tecnico(nombre, correo)
        elif opcion == '2':
            cliente = input("Nombre del cliente: ")
            prioridad = input("Prioridad (alta/media/baja): ") or 'media'
            comentario = input("Comentario inicial (opcional): ") or None
            manager.registrar_ticket(cliente, prioridad, comentario)
        elif opcion == '3':
            ticket_id = input("ID del ticket: ")
            tecnico_nombre = input("Nombre del técnico a asignar: ")
            manager.asignar_tecnico(ticket_id, tecnico_nombre)
        elif opcion == '4':
            ticket_id = input("ID del ticket: ")
            estado = input("Nuevo estado (pendiente/en proceso/cerrado): ")
            manager.actualizar_estado(ticket_id, estado)
        elif opcion == '5':
            tecnico_nombre = input("Nombre del técnico: ")
            manager.listar_tickets_por_tecnico(tecnico_nombre)
        elif opcion == '6':
            cliente_nombre = input("Nombre del cliente: ")
            manager.listar_tickets_por_cliente(cliente_nombre)
        elif opcion == '7':
            estado = input("Filtrar por estado (o deje vacío): ") or None
            prioridad = input("Filtrar por prioridad (o deje vacío): ") or None
            tecnico = input("Filtrar por técnico (o deje vacío): ") or None
            manager.filtrar_tickets(estado, prioridad, tecnico)
        elif opcion == '8':
            print("Saliendo...")
            break
        else:
            print("Opción no válida. Intente nuevamente.")

if __name__ == '__main__':
    main()
