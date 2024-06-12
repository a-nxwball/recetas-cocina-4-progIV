import redis

r_client = redis.Redis(host="localhost", port="6379", db=0)

def agregar_receta(nombre, ingredientes, pasos):
    id_receta = r_client.incr('next_receta_id')
    
    r_client.hmset(f'receta: {id_receta}', {'nombre': nombre, 'ingredientes': ingredientes, 'pasos': pasos})
    
    r_client.sadd('recetas', nombre)
    
    print('Receta agregada exitosamente.')

def actualizar_receta(id, nombre, ingredientes, pasos):
    if not r_client.exists(f'receta: {id}'):
        print(f'Receta con ID: {id}, no encontrada.')
        return
    
    r_client.hmset(f'receta: {id}', {'nombre': nombre, 'ingredientes': ingredientes, 'pasos': pasos})
    
    print('Receta actualizada exitosamente.')

def eliminar_receta(id):
    if not r_client.exists(f'receta: {id}'):
        print(f'Receta con ID: {id}, no encontrada.')
        return
    
    r_client.delete(f'receta: {id}')
    r_client.srem('recetas', id)
    
    print('Receta eliminada exitosamente.')
    
def listar_recetas():
    recetas = r_client.smembers('recetas')
    for i, nombre in enumerate(recetas, start = 1):
        print(f'{i}. {nombre.decode('utf-8')}')
        
def buscar_ingredientes(nombre):
    resultados = []
    for key in r_client.scan_iter(match = f'receta:*'):
        receta = r_client.hgetall(key)
        if nombre.lower() in receta['nombre'].decode('utf-8').lower():
            resultados.append({
                'ingredientes': receta['ingredientes'].decode('utf-8'),
                'pasos': receta['pasos'].decode('utf-8')
            })
    return resultados

def main():
    salir = False
    while not salir:
        print("\n--- Libro de Recetas ---")
        print("1. Agregar nueva receta")
        print("2. Actualizar receta existente")
        print("3. Eliminar receta existente")
        print("4. Ver listado de recetas")
        print("5. Buscar ingredientes y pasos de receta")
        print("6. Salir")
        print("------------------------")

        opcion = input("Selecciona una opción: ")

        if opcion == '1':
            nombre = input("\nNombre de la receta: ")
            ingredientes = input("Ingredientes (separados por comas): ")
            pasos = input("Pasos (separados por comas): ")
            agregar_receta(nombre, ingredientes, pasos)
        elif opcion == '2':
            id = input("\nID de la receta a actualizar: ")
            nombre = input("Nuevo nombre de la receta: ")
            ingredientes = input("Nuevos ingredientes (separados por comas): ")
            pasos = input("Nuevos pasos (separados por comas): ")
            actualizar_receta(id, nombre, ingredientes, pasos)
        elif opcion == '3':
            id = input("\nID de la receta a eliminar: ")
            eliminar_receta(id)
        elif opcion == '4':
            print("\n--- Listado de Recetas ---")
            listar_recetas()
        elif opcion == '5':
            nombre = input("\nNombre de la receta a buscar: ")
            resultados = buscar_ingredientes(nombre)
            for i, resultado in enumerate(resultados, start=1):
                print(f"\nReceta {i}:")
                print(f"Ingredientes: {resultado['ingredientes']}")
                print(f"Pasos: {resultado['pasos']}")
        elif opcion == '6':
            salir = True
            print("\nSaliendo del programa...")
        else:
            print("\nOpción no válida. Inténtalo de nuevo.")

if __name__ == "__main__":
    main()