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
    """Carga un nivel desde level/level{level_id}.py y devuelve una lista de sprites."""
    try:
        # Importar el módulo correspondiente (level1, level2, level3)
        level_module = import_module(f"level.level{level_id}")
        
        # Verificar que el módulo tenga la función get_objects
        if not hasattr(level_module, "get_objects"):
            raise AttributeError(f"El módulo level.level{level_id} no define la función get_objects")
        
        # Obtener los objetos del nivel
        objects = level_module.get_objects(space)
        
        # Validar que los objetos sean instancias de arcade.Sprite y clases permitidas
        allowed_types = (Pig, Column, PassiveObject, Sling, RedBird, BlueBird, YellowBird)
        for obj in objects:
            if not isinstance(obj, arcade.Sprite):
                raise ValueError(f"Objeto en level.level{level_id} no es un arcade.Sprite: {type(obj)}")
            if not isinstance(obj, allowed_types):
                raise ValueError(f"Objeto inválido en level.level{level_id}: {type(obj)}. Se esperaba Pig, Column, PassiveObject, Sling o un pájaro")
        
        return objects
    
    except ImportError:
        raise FileNotFoundError(f"No se encontró el módulo level.level{level_id}")
    except Exception as e:
        raise RuntimeError(f"Error al cargar el nivel {level_id}: {str(e)}")