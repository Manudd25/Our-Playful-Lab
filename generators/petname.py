# generators/petname.py
import random

PET_CATS = ["cute", "royal", "mythic", "sci_fi", "rock", "foodie", "nature", "quirky"]

def make_pet_name(category: str | None = None, rng: random.Random | None = None) -> tuple[str, str]:
    """
    Returns (used_category, generated_name).
    Pass an RNG if you want reproducible output (e.g., random.Random(seed)).
    """
    rng = rng or random
    pick = rng.choice
    cat = category if category in PET_CATS else pick(PET_CATS)

    if cat == "cute":
        name = pick(["Fluffy","Bubbles","Pumpkin","Pebble","Noodle","Coco"]) + pick(["kins","paws","tail","boo","bean"])
    elif cat == "royal":
        name = f"{pick(['Sir','Lady','Duke','Princess'])} {pick(['Whiskers','Velvet','Onyx','Aurora'])}"
    elif cat == "mythic":
        name = f"{pick(['Nyx','Astra','Orion','Lyra'])} {pick(['Stormpaw','Moonwhisk','Skydancer'])}"
    elif cat == "sci_fi":
        name = f"{pick(['Nova','Pixel','Quark','Cosmo'])} {pick(['X','RX','MK'])}-{rng.randint(1,99)}"
    elif cat == "rock":
        name = f"{pick(['Riff','Axel','Jett','Storm'])} {pick(['Thunder','Blaze','Viper'])}"
    elif cat == "foodie":
        name = f"{pick(['Mocha','Sushi','Taco','Cookie'])} {pick(['Bean','Bite','Roll','Chip'])}"
    elif cat == "nature":
        name = f"{pick(['Willow','River','Moss','Clover'])} {pick(['Leaf','Stone','Bloom'])}"
    else:
        name = f"{pick(['Velvet','Golden','Midnight','Indigo'])} {pick(['Pixel','Gizmo','Sprinkle','Nimbus'])}"

    return cat, name
