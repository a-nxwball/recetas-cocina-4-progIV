from db_operations import (
    agregar_receta,
    actualizar_receta,
    eliminar_receta,
    listar_recetas,
    buscar_ingredientes
)

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