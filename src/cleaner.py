import re

# This script is used to clean the text of articles from various websites.
SITE_REGEX_CLEANERS = {
    # Needs to be update whenever a new website is added to  feeds/feeds.txt
    "Numerama": [
        r"Lecture Zen",  # En-tête inutile
        r"Résumer l'article",  # Idem

        # Bloc complet d'abonnement / publicité / soutien
        r"C'est pourquoi nous maintenons.*?S'abonner à Numerama\+",

        # Blocs additionnels fréquents
        r"Découvrez les bonus Numerama\+.*?",
        r"Vous avez lu \d+ articles sur Numerama.*?",
        r"Il y a une bonne raison.*?rejoignez Numerama\+.*?",
        r"Ajoutez Numerama.*?",
        r"Toute l'actu tech.*?",

        # Mentions légales / RGPD
        r"Les données transmises par.*?dédié\.",

        # Balises sources / mentions décoratives
        r"Source\s?:\s?.*",
        r"//\s?.*",  
    ],
    "The Verge": [
        r"Sign up for Verge Deals.*?(?=\n|$)",  
        r"Subscribe to.*?newsletter.*?",        
        r"Check your inbox for a welcome email.*?",  
        r"Related.*?",                          
        r"More from The Verge.*?",              
        r"The Verge is a vox media.*?",         
        r"Photography by.*?",                   
        r"Update.*?:",                         
        r"Filed under.*?",                      
        r"Email.*?Twitter.*?Flipboard.*?",      
        r"Disclosure:.*?",                      
    ]
}

def clean_text(text:str, source:str = "")->str:
    """
    Cleans the text of an article by removing unwanted patterns and characters.
    @param text: The text to be cleaned.
    @param source: The website's name which the text comes from.
    @return: The cleaned text.
    """
    
    # Specific cleaning for each site
    regexes = SITE_REGEX_CLEANERS.get(source, [])
    for pattern in regexes:
        text = re.sub(pattern, "", text, flags=re.IGNORECASE | re.DOTALL)


    # Regex pour enlever la section concernant l'auteur ou une description de l'auteur
    text = re.sub(r"^is a .*\n", "", text)  # On enlève tout texte commençant par "is a"
    
    text = re.sub(r"^By.*\n", "", text)  # On supprime les lignes qui commencent par "By"
    
    # Supprimer les autres mentions inutiles comme les crédits photo, la source, etc.
    text = re.sub(r"Photography by .*", "", text)  # Crédit photo
    text = re.sub(r"Filed under.*", "", text)  # Section "Filed under"
    
    # Regular cleaning
    text = re.sub(r"<[^>]+>", "", text) # Erase HTML tags
    text = re.sub(r"\n+", "\n", text) # Erase unnecessary lines
    text = re.sub(r"\s+", " ", text) # Erase unnecessary spaces

    return text.strip()


