"""Contenu du profil GitHub — source unique.

Modifie ce fichier (même directement sur github.com) : la GitHub Action
relance scripts/generate.py et régénère tous les visuels de assets/.
"""

LOGIN = "alejomendozahermida-png"
NAME_FIRST = "Alejandro"
NAME_LAST = "Mendoza"
ROLE = "Automatisation & IA appliquée au business"
SITE = "https://alejandro-mendoza.vercel.app/"
LINKEDIN = "https://www.linkedin.com/in/alejandro-mendoza-hermida-"
EMAIL = "alejomendozahermida@gmail.com"

# Étiquettes posées le long du sentier de la montagne (bas → sommet)
ROUTE = ["Python", "SQL", "n8n", "Claude API", "Agents IA"]

HIGHLIGHTS = [
    # (valeur, libellé ligne 1, libellé ligne 2, couleur)
    ("5", "projets", "livrés", "ice"),
    ("3+", "ans de terrain", "retail", "sand"),
    ("-85%", "de temps", "Content Engine", "sage"),
    ("x2", "taux de réponse", "cold email Automa", "terra"),
    ("1er", "prix étudiant", "Erasmus · UCLM", "rose"),
]

# status: (libellé, couleur) — cover: (couleur haut, couleur bas)
BUILDS = [
    {
        "slug": "content-engine",
        "title": "Content Engine",
        "subtitle": "Pipeline IA de contenu B2B",
        "icon": "✍️",
        "categories": ["AUTOMATION", "IA", "N8N"],
        "role": "Solo build",
        "status": ("WORKFLOW LIVE", "sage"),
        "cover": ("#3E6B5C", "#1E3A33"),
        "desc": "Une thématique en entrée, 4 publications en sortie (blog, LinkedIn, "
                "Instagram, visuel) en moins de 5 minutes. Claude rédige, GPT Image "
                "illustre, n8n orchestre et publie.",
        "metrics": ["12+ posts / semaine", "-85% de temps", "4 canaux"],
        "tags": ["n8n", "Claude API", "GPT Image"],
        "url": "https://alejandro-mendoza.vercel.app/",
    },
    {
        "slug": "automa",
        "title": "Automa",
        "subtitle": "Agence IA pour PME françaises",
        "icon": "🚀",
        "categories": ["B2B", "IA", "GROWTH"],
        "role": "Co-fondateur",
        "status": ("EN COURS", "ice"),
        "cover": ("#2F5C86", "#172E47"),
        "desc": "Offre B2B montée en moins de 2 mois : positionnement, pricing, landing, "
                "prospection. Acquisition automatisée (qualification, relances, suivi CRM) "
                "via n8n + Claude API.",
        "metrics": ["x2 taux de réponse", "3 angles testés", "< 2 mois"],
        "tags": ["n8n", "Claude API", "Cold email"],
        "url": "https://alejandro-mendoza.vercel.app/",
    },
    {
        "slug": "immo-pilot",
        "title": "Immo Pilot",
        "subtitle": "Agents IA pour agences immobilières",
        "icon": "🏠",
        "categories": ["SAAS", "MULTI-TENANT", "AGENTS"],
        "role": "Architecture & build",
        "status": ("EN BUILD", "sand"),
        "cover": ("#8A5A35", "#4A2F1C"),
        "desc": "Six agents spécialisés (prospection, estimation, annonce, qualification, "
                "visite, suivi) sur une seule base multi-tenant : un système qui évolue "
                "pour toutes les agences à la fois.",
        "metrics": ["6 agents", "multi-tenant", "RGPD by design"],
        "tags": ["Next.js", "FastAPI", "Supabase"],
        "url": "https://alejandro-mendoza.vercel.app/",
    },
    {
        "slug": "ali",
        "title": "Ali",
        "subtitle": "Santé mentale, guidée par l'IA",
        "icon": "🏔️",
        "categories": ["PRODUCT", "UX", "IA"],
        "role": "Product & design",
        "status": ("CONCEPT PRODUIT", "rose"),
        "cover": ("#5B6F9E", "#2B3557"),
        "desc": "Réduire la friction du premier pas vers un professionnel : un guide IA "
                "qui oriente sans remplacer le thérapeute, des modules éducatifs et "
                "zéro comparaison sociale.",
        "metrics": ["IA responsable", "build in public"],
        "tags": ["Product", "UX", "IA"],
        "url": "https://github.com/alejomendozahermida-png/Ali-app",
    },
]

JOURNEY = [
    {
        "title": "Co-fondateur — Product & Growth Marketing",
        "org": "AUTOMA",
        "type": "Entrepreneuriat",
        "period": "2025 — présent",
        "current": True,
        "color": "terra",
        "line": "Offre B2B en moins de 2 mois · cold email : taux de réponse x2 · acquisition n8n + Claude API",
        "tags": ["n8n", "Claude API", "Growth"],
    },
    {
        "title": "Conseiller de vente — référent Salle de Bain",
        "org": "CASTORAMA",
        "type": "Retail",
        "period": "Sept. 2025 — 2026",
        "current": False,
        "color": "ice",
        "line": "Accompagnement de projets clients de A à Z · vendeur référent de l'équipe",
        "tags": ["Conseil", "Vente"],
    },
    {
        "title": "Vendeur sport omni-commerçant",
        "org": "DÉCATHLON",
        "type": "Retail",
        "period": "2024 — 2025",
        "current": False,
        "color": "sky",
        "line": "Magasin test des stratégies nationales (Porte de Montreuil) · parcours omnicanal",
        "tags": ["Omnicanal", "Retail"],
    },
    {
        "title": "Conseiller rénovation énergétique",
        "org": "GROUPE ENERVY",
        "type": "Terrain",
        "period": "2024",
        "current": False,
        "color": "sage",
        "line": "Conseil aux particuliers sur leurs projets de rénovation énergétique",
        "tags": ["Conseil", "B2C"],
    },
]

EDUCATION = [
    {
        "title": "MSc IA appliquée au business",
        "org": "EUGENIA SCHOOL",
        "type": "Alternance",
        "period": "2026 — 2028",
        "current": True,
        "color": "terra",
        "line": "Parcours architecte IA · rythme 4 jours entreprise / 1 jour école",
        "tags": ["Agents IA", "Data"],
    },
    {
        "title": "Mobilité Erasmus — 1er prix étudiant",
        "org": "UNIVERSIDAD DE CASTILLA-LA MANCHA",
        "type": "Espagne",
        "period": "2025",
        "current": False,
        "color": "sand",
        "line": "Semestre à l'étranger, récompensé par le 1er prix étudiant",
        "tags": ["International"],
    },
    {
        "title": "Licence Administration & Échanges Internationaux",
        "org": "UPEC",
        "type": "Parcours Europe",
        "period": "2022 — 2025",
        "current": False,
        "color": "rose",
        "line": "Commerce international, gestion, droit et économie européenne",
        "tags": ["Business", "International"],
    },
]

# niveau : 3 = au quotidien · 2 = à l'aise · 1 = en apprentissage
STACK = [
    ("IA & AUTOMATION", "terra", [("n8n", 3), ("Claude API", 3), ("Prompt engineering", 3),
                                  ("Agents IA", 2), ("Claude Code", 2), ("APIs & webhooks", 2)]),
    ("DATA", "ice", [("Python", 1), ("SQL", 1), ("Reporting & KPIs", 2), ("Google Analytics", 2)]),
    ("PRODUCT & BUILD", "sage", [("Figma", 2), ("Next.js", 1), ("FastAPI", 1), ("Supabase", 1)]),
    ("GROWTH & MARKETING", "sand", [("Copywriting B2B", 3), ("Cold email", 2), ("HubSpot", 2),
                                    ("Meta & Google Ads", 2)]),
    ("LANGUES", "rose", [("Español — C2", 3), ("Français — C2", 3), ("English — B2", 2)]),
]
