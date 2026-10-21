# Immunity range from the Punjab price list (Oct 2025) plus the 11 biofertilizer types covered by our NOC.
# No prices on the site: every product page asks for an enquiry. Product photos live in assets/img/products/<slug>.webp.
L4 = ["250 mL", "500 mL", "1 L", "5 L"]
GROUPS = [("specials", "Crop Specials", "One formula made for one crop."),
          ("allcrops", "For all crops", "General formulas for any crop."),
          ("finish", "Finishing stage", "For the last stage before harvest."),
          ("bio", "Biofertilizers", "Living microbes that feed the soil and the crop."),
          ("soil", "For soil", "Applied to the soil at planting.")]

def sp(slug, crop, name, line, made_for, story=""):
    return dict(slug=slug, group="specials", crop=crop, name=name, packs=L4, form="Liquid", line=line, made_for=made_for, story=story)

PRODUCTS = [
 sp("immunity-sugarcane-special", "sugarcane", "Immunity Sugarcane Special", "Made for sugarcane on tired soil: poor germination, gaps and uneven growth.",
    ["Poor germination and gaps", "Plants dying after germination", "Uneven growth", "Soil worn out by decades of sugarcane", "Falling yields despite new varieties"],
    "Developed with growers in South Gujarat, where much of the land has grown sugarcane for about five decades and many growers no longer broke even."),
 sp("immunity-potato-special", "potato", "Immunity Potato Special", "Made for potato growers seeing fewer, smaller tubers and rising fertilizer bills.",
    ["Fewer tubers per plant", "Small or uneven tubers", "Weak skin and quality", "More fertilizer every season"],
    "Developed with growers in Punjab and Haryana whose yields were falling while fertilizer needs kept rising."),
 sp("immunity-mango-special", "mango", "Immunity Mango Special", "Made for mango trees: decline, alternate bearing, fruit drop and small fruit.",
    ["Trees weakening or dying", "Poor flush after harvest", "Alternate bearing", "Flower and fruit drop", "Small fruit, poor quality"],
    "Several thousand mango growers across India have used it, according to our records."),
 sp("immunity-apple-special", "apple", "Immunity Apple Special", "Made for apple orchards: tree losses, low production and poor fruit quality.",
    ["Trees dying in the orchard", "Root problems", "Low production", "Small, poorly coloured fruit"],
    "Developed for growers in Himachal Pradesh and Jammu and Kashmir. Thousands of apple growers have used it, according to our records."),
 sp("immunity-banana-special", "banana", "Immunity Banana Special", "Made for banana: plant losses, weak growth and low bunch weight.",
    ["Plants dying in the field", "Weak growth", "Low bunch weight", "Poor finger quality"],
    "Developed with banana growers in Central Gujarat who faced heavy plant losses from wilt and leaf spot."),
 sp("immunity-citrus-special", "citrus", "Immunity Citrus Special", "Made for lemon, lime, orange and mosambi: dieback, fruit drop and weak trees.",
    ["Branches drying (dieback)", "Fruit drop", "Yellow leaves", "Declining trees"]),
 sp("immunity-coconut-special", "coconut", "Immunity Coconut Special", "Made for coconut palms: low nut yield, button shedding and weak palms.",
    ["Low nut yield", "Button (young nut) shedding", "Small nuts", "Weak palms"]),
 sp("immunity-cotton-special", "cotton", "Immunity Cotton Special", "Made for cotton: weak early growth, square and boll shedding.",
    ["Weak early growth", "Square and boll shedding", "Reddening of leaves", "Falling yields"]),
 sp("immunity-onion-special", "onion", "Immunity Onion Special", "Made for onion: small bulbs, uneven size and poor storage.",
    ["Small or uneven bulbs", "Weak roots", "Poor keeping quality", "Leaf tip drying"]),
 sp("immunity-pomegranate-special", "pomegranate", "Immunity Pomegranate Special", "Made for pomegranate: flower drop, fruit cracking and weak plants.",
    ["Flower and fruit drop", "Fruit cracking", "Poor fruit size and colour", "Weak plants"]),
 sp("immunity-paddy-special", "paddy", "Immunity Paddy Special", "Made for paddy: weak tillering, poor grain filling and yellowing.",
    ["Weak tillering", "Yellowing after transplanting", "Poor grain filling", "Chaffy grain"]),
 sp("immunity-maize-special", "maize", "Immunity Maize Special", "Made for maize: weak early growth, poor cob filling.",
    ["Weak early growth", "Poor cob size and filling", "Yellowing leaves", "Stress in dry spells"]),
 sp("immunity-tea-special", "tea", "Immunity Tea Special", "Made for tea gardens: slow flush and tired bushes.",
    ["Slow new flush", "Tired, ageing bushes", "Poor leaf quality", "Acidic, worn-out soil"]),
 sp("immunity-cumin-special", "cumin", "Immunity Cumin Special", "Made for cumin: weak plants, wilt-prone fields and low seed set.",
    ["Weak, patchy plants", "Plants wilting and dying", "Low seed set", "Poor seed quality"]),
 sp("immunity-chilli-special", "chilli", "Immunity Chilli (Mirchi) Special", "Made for chilli: flower drop, leaf curl stress and small fruit.",
    ["Flower and fruit drop", "Stress from leaf curl", "Small fruit", "Short picking season"]),
 sp("immunity-mungfali-special", "groundnut", "Immunity Mungfali (Groundnut) Special", "Made for groundnut: poor pegging, few pods and empty pods.",
    ["Few pegs and pods", "Empty or small pods", "Yellowing", "Weak roots"]),
 sp("immunity-dhanya-special", "cereals", "Immunity Dhanya Special", "Made for cereal crops: wheat, bajra, jowar and similar grains.",
    ["Weak tillering", "Poor grain filling", "Yellowing", "Stress in dry spells"]),
 sp("immunity-pulses-special", "pulses", "Immunity Pulses Special", "Made for pulses: tur, moong, urad, chana and other legumes.",
    ["Flower drop", "Few pods", "Weak nodulation", "Yellowing"]),
 sp("immunity-vegetable-special", "vegetables", "Immunity Vegetable Special", "Made for vegetables: tomato, brinjal, okra, cabbage, gourds and more.",
    ["Flower and fruit drop", "Small fruit", "Short harvest period", "Weak plants"]),
 sp("immunity-fruit-special", "fruits", "Immunity Fruit Special", "Made for fruit orchards: guava, chikoo, papaya, grapes and other fruit crops.",
    ["Flower and fruit drop", "Small fruit", "Poor colour and taste", "Weak trees"]),
 dict(slug="immunity-gold", group="allcrops", crop="", name="Immunity Gold", packs=L4, form="Liquid",
      line="Our general formula for all crops: field crops, vegetables, fruit and plantation crops.",
      made_for=["Crops without their own Special", "Weak growth and poor vigour", "Stress after heat, drought or waterlogging"], story=""),
 dict(slug="immunity-eleven", group="allcrops", crop="", name="Immunity Eleven", packs=L4, form="Liquid",
      line="A formula for all crops. Ask us which crops and stages it suits.", made_for=[], story=""),
 dict(slug="immunity-spices-mix", group="allcrops", crop="", name="Immunity Spices Mix", packs=L4, form="Liquid",
      line="A formula from the Immunity range. Ask us which crops and stages it suits.", made_for=[], story=""),
 dict(slug="immunity-finisher", group="finish", crop="", name="Immunity Finisher", packs=["1 L"], form="Liquid",
      line="For the last stage of the crop. Ask us when and how to use it on your crop.", made_for=[], story=""),
 dict(slug="immunity-granules", group="soil", crop="", name="Immunity Granules", packs=["8 kg bag"], form="Granules (soil applied)",
      line="Soil-applied granules that release slowly, for soil structure and soil life.",
      made_for=["Hard, compacted soil", "Soil with little life left", "Poor root growth", "More fertilizer needed every year"], story=""),
]

def bio(slug, name, what, crops, packs=None, form="Liquid or carrier-based"):
    return dict(slug=slug, group="bio", crop="", name=name, packs=packs or [], form=form, line=what, made_for=crops, story="")

PRODUCTS += [
 bio("immunity-azotobacter", "Immunity Azotobacter", "Free-living bacteria that fix nitrogen from the air for the crop.", ["Cereals, vegetables, cotton, sugarcane and most non-legume crops"]),
 bio("immunity-azospirillum", "Immunity Azospirillum", "Bacteria that fix nitrogen around the roots of grasses and cereals.", ["Paddy, maize, wheat, sugarcane, millets"]),
 bio("immunity-rhizobium", "Immunity Rhizobium", "Bacteria that form nitrogen-fixing nodules on the roots of legumes.", ["Groundnut, soybean, chana, tur, moong, urad"]),
 bio("immunity-acetobacter", "Immunity Acetobacter", "Bacteria that fix nitrogen inside sugarcane and similar crops.", ["Sugarcane, sugar beet"]),
 bio("immunity-psb", "Immunity PSB (Phosphate Solubilising Bacteria)", "Bacteria that free locked phosphorus in the soil for the crop.", ["All crops"]),
 bio("immunity-kmb", "Immunity KMB (Potash Mobilising Bacteria)", "Bacteria that make potash in the soil available to the crop.", ["All crops"]),
 bio("immunity-zsb", "Immunity ZSB (Zinc Solubilising Bacteria)", "Bacteria that free locked zinc in the soil for the crop.", ["All crops, especially paddy, wheat, maize"]),
 bio("immunity-psf", "Immunity PSF (Phosphate Solubilising Fungi)", "Fungi that free locked phosphorus in the soil for the crop.", ["All crops"]),
 bio("immunity-mycorrhiza", "Immunity Mycorrhiza", "Root fungi that extend the root system to reach more water and nutrients.", ["Fruit trees, vegetables, field crops"], ["500 mL"], "Liquid"),
 bio("immunity-npk-consortia", "Immunity NPK Consortia", "A liquid mix of nitrogen-fixing, phosphate-solubilising and potash-mobilising microbes.", ["All crops"], None, "Liquid"),
 bio("immunity-consortia", "Immunity Consortia", "A carrier-based mix of beneficial soil microbes.", ["All crops"], None, "Carrier-based"),
]
PBY = {p["slug"]: p for p in PRODUCTS}
assert len(PRODUCTS) == 36, len(PRODUCTS)

# Other crops each formula is also used on (from Gujarat Bio Organics' field use)
ALSO = {"immunity-mango-special": "Chikoo (sapota), guava and similar fruit trees",
        "immunity-citrus-special": "Lemon, lime, orange, mosambi, malta and kinnow",
        "immunity-dhanya-special": "Wheat, bajra (pearl millet), jowar (sorghum) and other cereals"}
for _s, _t in ALSO.items(): PBY[_s]["also"] = _t
