def get_skin_type_info(skin_type: str) -> dict:
    """ Get characteristics and recommednations for a skin type.
    Args: 
        skin_type: The user's skin type. One of: dry, oily, combination, sensitive, normal.
    """
    db = {
        "dry": {
            "characteristics": ["tight", "flaky", "dull"],
            "loves": ["hyaluronic acid", "ceramides", "shea butter"],
            "avoid": ["alcohol", "sulfates", "harsh cleansers"]
        },
        "oily": {
            "characteristics" : ["tight", "flaky", "dull"],
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
    """ Get characteristics and recommednations for a hair type.
    Args: 
        hair_type: The user's hair type. One of: straight, wavy, curly, coily.
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
            "loves": ["rich moisturizers", "deep conditioners", "leave-ins", "protextive styles", "sealing oils/butters"],
            "avoid": ["frequent heat styling and over-manipulation", "harsh detergents", "dry brushing"]
        }
    }
    return db.get(hair_type, {"error": f"Unknown skin type: {hair_type}"})