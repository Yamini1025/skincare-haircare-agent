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