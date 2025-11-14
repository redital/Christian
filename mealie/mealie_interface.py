from mealie.recipe import get_recipes_by_categories, get_recipe
from mealie.category import get_all_categories
from mealie.mealie_base_module import *


  
def get_random_recipe_from_categories(categories, api_url=mealie_url, token=api_token):    
    """
    Ottiene una ricetta casuale tra quelle che appartengono alle categorie specificate.
    :param categories: Lista delle categorie
    :return: Una ricetta casuale
    """
    recipes = [i["slug"] for i in get_recipes_by_categories(categories, require_all_categories=True, api_url=api_url, token=token)]
    if recipes:
        # Scegli una ricetta casuale
        random_recipe = random.choice(recipes)
        print(f"Ricetta casuale: {random_recipe}")
        return get_recipe(random_recipe, api_url=api_url, token=token)
    else:
        print("Nessuna ricetta trovata con le categorie specificate.")
        return None
    