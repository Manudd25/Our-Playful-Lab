from datetime import datetime

PROJECTS = [
    {
        "id": "excuse-generator",
        "title": "🎯 Excuse Generator",
        "description": "A witty excuse generator with creative responses and modern UI design. Perfect for those moments when you need a creative explanation.",
        "category": "Web App",
        "status": "Live Demo",
        "technologies": ["Flask", "Python", "CSS3", "HTML5"],
        "features": ["Random excuse generation", "Modern UI/UX", "Responsive design"],
        "link": "/excuse-generator",
        "github": "https://github.com/Manudd25/Our-Playful-Lab.git",
        "image": None,
        "priority": 1,
        "released_at": "2025-08-14",
    },
    {
        "id": "petname-generator",
        "title": "🐾 Pet Name Generator",
        "description": "Creative pet naming tool with categories and beautiful animations. Generate unique names for your furry friends. Try it out!",
        "category": "Web App",
        "status": "Interactive",
        "technologies": ["JavaScript", "CSS3", "HTML5", "APIs"],
        "features": ["Category-based generation", "Beautiful animations", "Responsive design"],
        "link": "/petname-generator",
        "github": "https://github.com/Manudd25/Our-Playful-Lab.git",
        "image": None,
        "priority": 2,
        "released_at": "2025-08-15",
    },
    {
        "id": "ai-image-generator",
        "title": "🖼️ AI Image Generator",
        "description": "Prompt-to-image generator powered by Colab backend. Create unique visuals from text prompts!",
        "category": "Web App",
        "status": "Live Demo",
        "technologies": ["Flask", "FastAPI", "Diffusers", "Colab", "React"],
        "features": ["Prompt input", "Colab backend", "Creative image results"],
        "link": "https://colabsite.z6.web.core.windows.net/",
        "github": "https://github.com/Manudd25/AI-Image-Generator",
        "image": None,
        "priority": 3,
        "released_at": "2025-08-20",
    },
]

def two_latest(projects):
    # by release date then priority
    def key(p):
        d = p.get("released_at")
        try:
            dt = datetime.fromisoformat(d) if d else datetime.min
        except Exception:
            dt = datetime.min
        return (dt, p.get("priority", 0))
    return sorted(projects, key=key)[-2:]
