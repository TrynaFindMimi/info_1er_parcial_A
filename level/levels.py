from importlib import import_module
import arcade
from characters.pig import Pig
from objects.column import Column
from objects.passiveObject import PassiveObject
from objects.sling import Sling
from characters.redBird import RedBird
from characters.blueBird import BlueBird
from characters.yellowBird import YellowBird

def load_level(level_id, space):
    try:
        #Importar el módulo correspondiente (level1, level2, level3)
        level_module = import_module(f"level.level{level_id}")
        
        #Verifica que el módulo tenga la función get_objects
        if not hasattr(level_module, "get_objects"):
            raise AttributeError(f"El módulo level.level{level_id} no define la función get_objects")
        
        #Obtiene los objetos del nivel
        objects = level_module.get_objects(space)
        
        #Define los tipos de objetos permitidos en el nivel
        allowed_types = (Pig, Column, PassiveObject, Sling, RedBird, BlueBird, YellowBird)
        #Valida que cada objeto sea un sprite y pertenezca a los tipos permitidos
        for obj in objects:
            if not isinstance(obj, arcade.Sprite):
                raise ValueError(f"Objeto en level.level{level_id} no es un arcade.Sprite: {type(obj)}")
            if not isinstance(obj, allowed_types):
                raise ValueError(f"Objeto inválido en level.level{level_id}: {type(obj)}. Se esperaba Pig, Column, PassiveObject, Sling o un pájaro")
        
        return objects
    
    except ImportError:
        #Lanza un error si el módulo del nivel no existe
        raise FileNotFoundError(f"No se encontró el módulo level.level{level_id}")
    except Exception as e:
        #Lanza un error genérico para cualquier otro problema durante la carga
        raise RuntimeError(f"Error al cargar el nivel {level_id}: {str(e)}")