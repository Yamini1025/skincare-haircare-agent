import json
import google.generativeai as genai
import state


def get_skin_type_info(skin_type: str) -> dict:
    """ Get detailed characteristics, recommendations, and ingredients to avoid for a skin type.
        Do NOT use when user's skin type is unknown or not one of the above - ask them first.
    Args: 
        skin_type: The user's skin type MUST be one of: dry, oily, combination, sensitive, normal. 
    Returns a dictionary list of characteristics, as well as recommended ingredients and ingredients to avoid for that skin type.
    Example:
        get_skin_type_info("dry") -> {
            "characteristics": ["tight", "flaky", "dull"],
            "loves": ["hyaluronic acid", "ceramides", "shea butter"],
            "avoid": ["alcohol", "sulfates", "harsh cleansers"]
        }
    Edge case: get_skin_type_info("unknown") -> {
        Skin type not found in database, please provide a valid skin type.
    } - this is not a crash, handle it gracefully by asking the user for their skin type again or providing general skincare advice.
    """
    db = {
        "dry": {
            "characteristics": ["tight", "flaky", "dull"],
            "loves": ["hyaluronic acid", "ceramides", "shea butter"],
            "avoid": ["alcohol", "sulfates", "harsh cleansers"]
        },
        "oily": {
            "characteristics" : ["shiny", "enlarged pores", "acne-prone"],
            "loves": ["niacinamide", "salicylic acid", "lightweight moisturizers"],
            "avoid": ["heavy oils", "comedogenic ingredients"]
        },
        "combination": {
            "characteristics": ["oily T-zone", "dry cheeks"],
            "loves": ["gel moisturizers", "balancing toners"],
            "avoid": ["heavy creams on T-zone", "overly stripping cleansers"]
        },
        "sensitive": {
            "characteristics": ["redness", "reactive", "easily irritated"],
            "loves": ["centella asiatica", "aloe vera", "ceramides"],
            "avoid": ["fragrance", "harsh exfoliants", "alcohol"]
        },
        "normal": {
            "characteristics": ["balanced", "minimal concerns"],
            "loves": ["antioxidants", "SPF", "light hydration"],
            "avoid": ["over-stripping cleansers"]
        }
    }
    return db.get(skin_type, {"error": f"Unknown skin type: {skin_type}"})

def get_hair_type_info(hair_type: str) -> dict:
    """ Get detailed characteristics, recommendations, and ingredients to avoid for a hair type.
        Do NOT use when user's hair type is unknown or not one of the above - ask them first.
    Args: 
        hair_type: The user's hair type MUST be one of: straight, wavy, curly, coily.
    Returns a dictionary list of characteristics, as well as recommended ingredients and ingredients to avoid for that hair type.
    Example:
        get_hair_type_info("straight") -> {
            "characteristics": ["naturally smooth and shiny", "less volume", "can get greasy sometimes"],
            "loves": ["lightweight shampoos", "volumizing products", "light conditioners"],
            "avoid": ["heavy butters", "thick creams", "excessive oils"]
        }
    Edge case: get_hair_type_info("unknown") -> {
        Hair type not found in database, please provide a valid hair type.
    } - this is not a crash, handle it gracefully by asking the user for their hair type again or providing general hair care advice.
    """
    db = {
        "straight": {
            "characteristics": ["naturally smooth and shiny", "less volume", "can get greasy sometimes"],
            "loves": ["lightweight shampoos", "volumizing products", "light conditioners"],
            "avoid": ["heavy butters", "thick creams", "excessive oils"]
        },
        "wavy": {
            "characteristics" : ["S-shaped pattern", "prone to frizz", "between straight and curly"],
            "loves": ["lightweight curl creams", "sea salt sprays", "light hydrating products"],
            "avoid": ["heavy oils", "thick butters", "excessive layering of products"]
        },
        "curly": {
            "characteristics": ["defined curls/ringlets", "prone to dryness and frizz", "natural volume", "tangles more easily"],
            "loves": ["moisturizing conditioners", "curl creams", "leave-ins", "deep conditioning treatments"],
            "avoid": ["harsh sulfates", "excessive heat styling", "brushing when dry"]
        },
        "coily": {
            "characteristics": ["tight coils or zig-zag pattern", "most fragile hair type", "highest shrinkage", "prone to dryness and breakage"],
            "loves": ["rich moisturizers", "deep conditioners", "leave-ins", "protective styles", "sealing oils/butters"],
            "avoid": ["frequent heat styling and over-manipulation", "harsh detergents", "dry brushing"]
        }
    }
    return db.get(hair_type, {"error": f"Unknown hair type: {hair_type}"})

def ingredient_search(ingredient: str) -> dict:
        """ Get detailed information about a skincare or haircare ingredient, including its benefits, potential side effects, and recommended usage.
            Use when the user asks about a specific ingredient or when recommending products that contain certain ingredients.
        Args: 
            ingredient: The name of the skincare or haircare ingredient to look up.
        Returns a dictionary with the ingredient's benefits, potential side effects, and recommended usage.
        """
        try :
            ingredient_model = genai.GenerativeModel("gemini-3.5-flash")
            response = ingredient_model.generate_content(
                f"""Provide detailed and factual information about the skincare or haircare ingredient '{ingredient}', formatting the output in JSON format with the following structure: 
                {{
                    'benefits': [list of benefits],
                    'potential_side_effects': [list of potential side effects],
                    'recommended_usage': [list of recommended usage tips],
                    'suitable_for': [list of skin/hair types this ingredient is suitable for],
                    'avoid_for': [list of skin/hair types that should avoid this ingredient],
                    'can_combine_with': [list of other ingredients that can be safely combined with this ingredient],
                    'should_not_combine_with': [list of other ingredients that should not be combined with this ingredient],
                    'usage_frequency': [how often this ingredient can be used safely]
                }}
                For the fields "can_combine_with" and "should_not_combine_with":

                - Return ONLY ingredient names.
                - Do NOT include explanations.
                - Use lowercase.
                - One ingredient per array element.
                - Example:

                "can_combine_with": [
                "niacinamide",
                "ceramides",
                "hyaluronic acid"
                ],

                "should_not_combine_with": [
                "benzoyl peroxide",
                "vitamin c",
                "glycolic acid"
                ]""")
    
            clean_text = response.text.replace("```json", "").replace("```", "").strip()
            return json.loads(clean_text)
        except json.JSONDecodeError :
            return {"error": f"Could not parse ingredient info for: {ingredient}"}
        except Exception as e:
            return {"error": f"An error occurred while searching for ingredient info: {str(e)}"}
        
def product_search(product_type: str, skin_or_hair_type: str) -> dict:
    """ Search for products based on the user's skin or hair type and the type of product they are looking for (e.g., cleanser, moisturizer, shampoo, conditioner).
        Do NOT use when user's skin/hair type is unknown or not in the database - ask them first.
    Args: 
        product_type: The type of product the user is looking for (e.g., cleanser, moisturizer, shampoo, conditioner).
        skin_or_hair_type: The user's skin or hair type to tailor the product recommendations.
    Returns a list of products that do not contain any ingredients the user is allergic to. 
    """
    try:
        with open('products.json', 'r', encoding='utf-8') as file:

            product_dataset = json.load(file)
    except FileNotFoundError:
        return [{"isError" : True, "errorCategory" : "not_found", "isRetryable" : False, "context": {"attempted": f"Load products.json for {product_type} search"}}]
    
    filtered_products = []
    for item in product_dataset:
        skin = skin_or_hair_type.lower()
        if item.get("category", "").lower() == product_type.lower() and skin in [x.lower() for x in item.get("skin_types", [])] + [x.lower() for x in item.get("hair_types", [])]:
            filtered_products.append(item)
    if not filtered_products:
        return [{"isError" : False, "found" : False, "isRetryable" : False, "context": {"attempted": f"Search for {product_type} products for {skin_or_hair_type}"}}]
    else :
        filtered_products = filtered_products[:5]
        
    allergies = state.user_profile["known_allergies"]["value"]
    if isinstance(filtered_products, list):
        safe_products = []
        for product in filtered_products:
            product_name = product.get("name", "")
            ingredients = product.get("key_ingredients", [])
            if not any(allergy.lower() in [ingredient.lower() for ingredient in ingredients] for allergy in allergies):
                safe_products.append(product)
        filtered_products = safe_products
    if not filtered_products:
        return [{"isError" : False, "found" : False, "isRetryable" : False, "context": {"attempted": f"Search for {product_type} products for {skin_or_hair_type}"}}]
    else :
        filtered_products = filtered_products[:5]
        update_recommended_products(filtered_products)
    return filtered_products

def update_user_profile(skin_type: str = None, hair_type: str = None, add_concerns: list[str] = None, add_allergies: list[str] = None, price_preference: str = None, confidence: str = None) -> str:
    """ Update the user's profile with new information about their skin type, hair type, concerns, known allergies, and price preference.
    Args:
        skin_type: The user's skin type (dry, oily, combination, sensitive, normal).
        hair_type: The user's hair type (straight, wavy, curly, coily).
        add_concerns: A list of new concerns to add to the user's profile.
        add_allergies: A list of known allergies to add to the user's profile.
        price_preference: The user's price preference for products (e.g., budget, mid-range, premium).
        confidence: The confidence level of the information provided (e.g., "verified", "inferred", "estimated").
    Returns a confirmation message indicating that the user's profile has been updated.
    """
    
    if skin_type: state.user_profile["skin_type"] = {"value": skin_type, "confidence": confidence}
    if hair_type: state.user_profile["hair_type"] = {"value": hair_type, "confidence": confidence}
    if price_preference: state.user_profile["price_preference"] = {"value": price_preference, "confidence": confidence}
    
    if add_concerns:
        state.user_profile["concerns"] = {"value": list(set(state.user_profile["concerns"]["value"] + list(add_concerns))), "confidence": confidence}
    if add_allergies:
        state.user_profile["known_allergies"] = {"value": list(set(state.user_profile["known_allergies"]["value"] + list(add_allergies))), "confidence": confidence}
    return "User profile updated successfully."

def update_recommended_products(products: object) -> str:
    """ Add recommended product names to the user's profile.
        Call this after calling product_search() and getting a product recommendation.
    Args:
        products: Either a product dict, a list of product dicts, or a list of product names.
    Returns a confirmation message indicating that the recommended products have been updated.
    """
    def extract_product_name(item):
        if isinstance(item, str):
            return item
        if isinstance(item, dict):
            return item.get("name") or item.get("title") or None
        return None

    # If a dict was passed, normalize to a single item list.
    if isinstance(products, dict):
        products = [products]

    if isinstance(products, list):
        for item in products:
            name = extract_product_name(item)
            if name and name not in state.user_recommended_products:
                state.user_recommended_products.append(name)
    else:
        name = extract_product_name(products)
        if name and name not in state.user_recommended_products:
            state.user_recommended_products.append(name)

    return "Recommended products updated successfully."

def update_user_routine(routine_type : str, am_list : list, pm_list : list) -> str:
    """ Update the user's routine with new AM and PM steps.
    Args:
        am_list: A list of steps for the user's morning routine.
        pm_list: A list of steps for the user's evening routine.
    Returns a confirmation message indicating that the user's routine has been updated.
    """
    if routine_type == 'skin' : 
        if am_list:
            state.user_routine["skin_am"] = list(am_list)
        if pm_list:
            state.user_routine["skin_pm"] = list(pm_list)
    elif routine_type == 'hair' :
        if am_list:
            state.user_routine["hair_am"] = list(am_list)
        if pm_list:
            state.user_routine["hair_pm"] = list(pm_list)
    return "User routine updated successfully."