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