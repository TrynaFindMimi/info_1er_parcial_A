import pymunk

def create_circle_body_and_shape(space, mass, radius, position, elasticity=0.8, friction=1, collision_type=0):
    moment = pymunk.moment_for_circle(mass, 0, radius)
    body = pymunk.Body(mass, moment)
    body.position = position
    shape = pymunk.Circle(body, radius)
    shape.elasticity = elasticity
    shape.friction = friction
    shape.collision_type = collision_type
    space.add(body, shape)
    return body, shape

def create_box_body_and_shape(space, mass, size, position, elasticity=0.8, friction=1, collision_type=0):
    moment = pymunk.moment_for_box(mass, size)
    body = pymunk.Body(mass, moment)
    body.position = position
    shape = pymunk.Poly.create_box(body, size)
    shape.elasticity = elasticity
    shape.friction = friction
    shape.collision_type = collision_type
    space.add(body, shape)
    return body, shape