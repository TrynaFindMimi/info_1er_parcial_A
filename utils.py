import pymunk

def create_circle_body_and_shape(space, mass, radius, position, elasticity=0.8, friction=1, collision_type=0):
    #Calcula el momento de inercia para un cuerpo circular
    moment = pymunk.moment_for_circle(mass, 0, radius)
    #Crea un cuerpo físico con la masa y momento especificados
    body = pymunk.Body(mass, moment)
    #Establece la posición inicial del cuerpo
    body.position = position
    #Crea una forma circular asociada al cuerpo con el radio dado
    shape = pymunk.Circle(body, radius)
    #Configura las propiedades de elasticidad y fricción de la forma
    shape.elasticity = elasticity
    shape.friction = friction
    #Asigna un tipo de colisión para identificar interacciones
    shape.collision_type = collision_type
    #Añade el cuerpo y la forma al espacio físico
    space.add(body, shape)
    #Retorna el cuerpo y la forma creados
    return body, shape

def create_box_body_and_shape(space, mass, size, position, elasticity=0.8, friction=1, collision_type=0):
    #Calcula el momento de inercia para un cuerpo rectangular
    moment = pymunk.moment_for_box(mass, size)
    #Crea un cuerpo físico con la masa y momento especificados
    body = pymunk.Body(mass, moment)
    #Establece la posición inicial del cuerpo
    body.position = position
    #Crea una forma rectangular asociada al cuerpo con el tamaño dado
    shape = pymunk.Poly.create_box(body, size)
    #Configura las propiedades de elasticidad y fricción de la forma
    shape.elasticity = elasticity
    shape.friction = friction
    #Asigna un tipo de colisión para identificar interacciones
    shape.collision_type = collision_type
    #Añade el cuerpo y la forma al espacio físico
    space.add(body, shape)
    #Retorna el cuerpo y la forma creados
    return body, shape