"""The generator implementation."""

import hashlib
import random
import re


class UnifiedFoundationalGenerator:
    """Generate deterministic, Python-esque institutional titles from a seed.

    Each instance owns its random-number generator, so using this class never
    changes the process-wide random state.
    """

    _TOKEN = re.compile(r"{{(\w+)}}")
    _VOWEL_SOUND = re.compile(r"^(?:[aeiou]|honest|honor|hour|heir)", re.I)

    _RESOLVE_TOKEN_MAP: dict[str, list[str]] = {
        "generated_proper_noun": ["name_title", "name_first", "name_last"],
        "enhanced_institution": ["institution_descriptor", "institution_base"],
        "generated_legal_action": ["legal_core_action", "legal_situational_pattern"],
        "generated_natural_philosophy_axiom": [
            "science_prefix",
            "science_property",
            "science_connector",
            "science_target",
            "science_constraint",
        ],
        "generated_academic_body": ["academic_body_modifier", "academic_body_noun"],
        "generated_logistics_action": ["logistics_tier", "logistics_vector"],
        "generated_academic_discipline": ["academic_prefix", "academic_subject_structure"],
        "noun_verbing": ["verbing_base_noun", "verbing_suffix_gerund"],
    }

    def __init__(self, seed: str = "The Larch") -> None:
        if not isinstance(seed, str):
            raise TypeError("seed must be a string")
        self._seed = seed
        self._rng = random.Random(int(hashlib.md5(seed.encode("utf-8")).hexdigest(), 16))
        self._grammar: dict[str, list[str]] = {
            "START": [
                "The {{enhanced_institution}}",
                "The {{generated_academic_body}}",
                "The {{ecclesiastical_body}}",
                "The {{abstracted_object}} {{enhanced_institution}}",
                "The {{abstracted_object}} {{generated_logistics_action}}",
                "The {{enhanced_institution}} of {{noun_verbing}} {{noun_plural}}",
                "The {{bureaucratic_rank}} {{enhanced_institution}} for {{noun_verbing}} {{noun_plural}}",
                "The {{botanical_item}} {{noun_verbing}} {{geography_sing}}",
                "No one {{verb_present}} the {{optional_nationality}} {{generated_academic_body}}",
                "A Brief {{academic_treatise}} on {{optional_modifier}} {{noun_plural}}",
                # Modular historical competition templates (replacing long 7-element template)
                "{{historical_competition_prefix}} {{historical_competition_middle}} {{historical_competition_suffix}}",
                "The {{historical_ordinal}} {{optional_annual}} {{competition}} Exhibition",
                "{{historical_ordinal}} Year {{competition}}: The {{optional_modifier}} Showcase",
                "A {{unladen_qualifier}} {{optional_nationality}} {{noun_singular}}",
                "The {{generated_proper_noun}} and {{generated_proper_noun}} {{generated_academic_body}}",
                "We Apologize for the {{optional_modifier}} {{noun_verbing}} of the {{noun_singular}}",
                "The {{geography_sing}} and {{geography_sing}} Cooperative {{enhanced_institution}}",
                "{{generated_proper_noun}}, Assistant Under-Secretary for {{noun_verbing}}",
                "A Audition for the Role of the {{optional_modifier}} {{noun_singular}}",
                "A {{theatrical_format}} Adaptation of the {{noun_verbing}} {{noun_singular}}",
                "The {{historical_ordinal}} Century Costumed {{theatrical_format}} on {{noun_verbing}}",
                # Modular legal templates (replacing long 6-7 element templates)
                "{{legal_authority}} {{legal_location}} {{legal_framework}}, {{generated_legal_action}} is {{prohibition}}",
                "By Order of {{bureaucratic_rank}} {{enhanced_institution}}, {{generated_legal_action}} shall be {{adverb}} {{prohibition}}",
                "According to {{legal_statute}} of {{geography_sing}}, No {{generated_legal_action}} permitted",
                # Modular academic position templates (replacing long 6-element template)
                "{{academic_title}} of {{generated_academic_discipline}} {{institution_affiliation}}",
                "Lead Researcher in {{generated_academic_discipline}} at the {{enhanced_institution}} of {{geography_sing}}",
                "Director of Studies for {{generated_academic_discipline}} within {{geography_sing}}",
                # Modular sports competition templates (replacing long 6-element template)
                "{{historical_ordinal}} {{sports_event}} of the {{optional_nationality}} {{generated_academic_discipline}}",
                "The {{optional_nationality}} {{generated_academic_discipline}} {{sports_clash}} Tournament",
                "{{historical_ordinal}} Annual {{generated_academic_discipline}} {{sports_clash}} Championship",
                # Enhanced templates with optional absurd elements for variety
                "The {{enhanced_institution}} of {{absurd_profession}}",
                "The {{bureaucratic_rank}} {{enhanced_institution}} for {{pointless_activity}} {{noun_plural}}",
                "The {{generated_academic_body}} Committee on {{ridiculous_goods}}",
                "A Brief {{academic_treatise}} on {{pointless_pursuit}} {{optional_modifier}}",
                "The Society for {{silly_occupation}} Advancement",
                "The Institute of {{useless_studies}} Research Division",
                "{{absurd_product}} Manufacturing Consortium",
                "The Guild of {{absurd_profession}} and {{ridiculous_workers}} Alliance",
                "We Apologize for the {{pointless_activity}} of the {{absurd_profession}}",
                "The {{optional_nationality}} Confederation of {{ridiculous_workers}}",
                "The Board of Directors for {{pointless_service}} Providers",
                "The Committee for Ethical Treatment of {{ridiculous_goods}}",
                "Academic Board of {{pointless_pursuit}} Studies",
                "The Tribunal of {{absurd_academic_topic}} Standards",
                "The Registry of {{useless_achievement}} Holders",
                "The Ministry of {{silly_occupation}} and {{pointless_pursuit}} Affairs",
                "The Society for Prevention of Cruelty to {{ridiculous_goods}}",
                "The Institute for Advanced {{pointless_theory}} Research",
                # New Monty Python-inspired absurdism templates (standalone options)
                "The Ministry of {{silly_occupation}}",
                "The Society for {{pointless_pursuit}}",
                "The Guild of {{absurd_profession}}",
                "The Union of {{ridiculous_workers}}",
                "The Institute of {{useless_studies}}",
                "{{absurd_product}} Emporium",
                "{{pointless_service}} Available Here",
                "We Sell {{absurd_commodity}}",
                "Specialists in {{pointless_activity}}",
                "Purveyors of {{ridiculous_goods}}",
                "Form {{form_number}}/{{absurd_form_name}}",
                "Application for {{pointless_permit}}",
                "License to {{absurd_activity}}",
                "Permit Required for {{ridiculous_action}}",
                "Certificate of {{useless_achievement}}",
                "{{absurd_entertainment}} Show",
                "{{pointless_celebrity}}'s {{absurd_talent}} Hour",
                "Starring in {{ridiculous_production}}",
                "Featuring the {{absurd_performance}}",
                "Presenting the {{pointless_spectacle}}",
                "The International Conference on {{pointless_theory}}",
                "Symposium on {{absurd_academic_topic}}",
                "Journal of {{ridiculous_research}}",
                "Proceedings of the {{absurd_college}}",
                "Treatise on {{pointless_philosophy}}",
                "The {{absurd_vehicle}} Rally",
                "{{pointless_journey}} Expedition",
                "Travel via {{ridiculous_transport}}",
                "Specialists in {{absurd_navigation}}",
                "Experts in {{pointless_routing}}",
                "The Board of Directors for {{abstracted_object}} {{generated_logistics_action}}",
                "The {{enhanced_institution}} for the {{generated_logistics_action}} of {{abstracted_object}}",
                "We Are Experiencing {{interruption_modifier}} {{bureaucratic_noun}} {{generated_academic_body}}",
                "The {{historical_ordinal}} Semi-Finals of the {{optional_nationality}} {{generated_academic_discipline}} {{sports_clash}}",
                "The Amalgamated Union of {{pejorative_plural}} and {{generated_academic_discipline}} Practitioners",
                "A Defensive Strategy for Countering an Attack by {{optional_modifier}} {{botanical_item}}",
                "The {{bureaucratic_rank}} Registry of Lethal {{abstracted_object}} Deployments",
                "The Annexation of {{optional_nationality}} {{geography_sing}} by the {{enhanced_institution}}",
                "The {{historical_ordinal}} {{ecclesiastical_body}} on the {{optional_modifier}} {{theological_crime}}",
                "A Decreed {{papal_edict}} Concerning the Excommunication of {{pejorative_plural}}",
                "The {{optional_nationality}} Inquisition into {{noun_verbing}}",
                "The Theory of the {{noun_singular}}, by {{generated_proper_noun}}",
                "A Fundamental Law of {{generated_natural_philosophy_axiom}} regarding {{noun_plural}}",
            ],
            "legal_core_action": [
                "{{noun_verbing}}",
                "The Silly-Walking of {{noun_plural}}",
                "The Unlicensed Placement of {{abstracted_object}}",
                "The Private Hoarding of {{abstracted_object}}",
            ],
            "legal_situational_pattern": [
                "after Dark",
                "during High Tea",
                "on Bank Holidays",
                "in a Public Wardrobe",
                "while {{noun_verbing}}",
                "while Escorting {{abstracted_object}}",
                "without {{bureaucratic_noun}}",
                "without Written Permission from the {{bureaucratic_rank}} {{academic_body_noun}}",
                "",
            ],
            "science_prefix": [
                "Relative",
                "Thermodynamic",
                "Gravitational",
                "Centrifugal",
                "Aerodynamic",
                "Submergence",
                "Larch-Centric",
                "",
            ],
            "science_property": [
                "Slippage",
                "Buoyancy",
                "Astronomy",
                "Deficit",
                "Velocity",
                "Dynamics",
                "Inertia",
                "Oscillation",
                "Elasticity",
            ],
            "science_connector": ["in", "of", "across", "between", "regarding"],
            "science_constraint": [
                "under Pressure",
                "at Low Altitudes",
                "after Dark",
                "in Free Fall",
                "during High Tea",
                "without a License",
                "",
            ],
            "science_target": ["{{noun_plural}}", "{{noun_singular}}", "{{botanical_item}}"],
            "academic_body_modifier": [
                "Argument",
                "Vocational Guidance",
                "Philosophy",
                "Logicians",
                "Brain-Drain",
                "Interruption",
                "Exposition",
                "Nudge-Nudge",
            ],
            "academic_body_noun": [
                "Clinic",
                "Office",
                "Faculty",
                "Council",
                "Laboratory",
                "Exhibition",
                "Inquisition",
            ],
            "logistics_tier": [
                "Retail",
                "Wholesale",
                "Black-Market",
                "Compulsory",
                "Industrial",
                "Unlicensed",
                "Bureaucratic",
                "Maritime",
            ],
            "logistics_vector": [
                "Procurement",
                "Smuggling",
                "Sourcing",
                "Allocation",
                "Accumulation",
                "Hoarding",
                "Distribution",
                "Consignment",
            ],
            "academic_prefix": [
                "Comparative",
                "Advanced",
                "Applied",
                "Pre-Renaissance",
                "Theoretical",
                "The Epistemology of",
                "Experimental Defense against",
                "",
            ],
            "academic_subject_structure": [
                "{{verbing_base_noun}}-{{verbing_suffix_gerund}}",
                "{{verbing_base_noun}} Morphology",
                "{{verbing_base_noun}} Selection",
                "Silly Walking",
                "Fresh Fruit",
            ],
            "abstracted_object": [
                "{{noun_plural}}",
                "{{noun_singular}}",
                "{{brand_mod}} {{noun_plural}}",
                "{{sensory_mod}} {{noun_plural}}",
                "{{brand_mod}} {{sensory_mod}} {{noun_plural}}",
                "{{brand_mod}} {{sensory_mod}} {{noun_singular}}",
            ],
            "optional_modifier": [
                "Silly",
                "Upper-Class",
                "Completely Non-Subversive",
                "Not-at-all-Absurd",
                "Dead",
                "Defending",
                "Exploding",
                "Defiant",
                "Runaway",
                "Luxury",
                "Highly Dangerous",
                "Self-Defending",
                "Lethal",
                "Bleeding-Heart",
                "Bourgeois",
                "Semiotical",
                "Sudden",
                "",
            ],
            "optional_nationality": [
                "Spanish",
                "French",
                "Norwegian",
                "British",
                "Roman",
                "Swallow-bound",
                "Australian",
                "Icelandic",
                "Welsh",
                "Transylvanian",
                "Hungarian",
                "Moustachistani",
                "Upper-Vannu",
                "Bratislavian",
                "San Serif",
                "Oolong-bound",
                "",
            ],
            "optional_annual": [
                "Annual",
                "Bi-Centennial",
                "Impromptu",
                "Quarterly",
                "Tri-Centennial",
                "",
            ],
            "brand_mod": [
                "Whizz-Bang",
                "Spring-Surprise",
                "Unlicensed",
                "Military-Grade",
                "Smuggled",
                "Gilded",
                "Royal",
                "Self-Defending",
                "Black-Market",
            ],
            "sensory_mod": [
                "Crunchy",
                "Cockroach-Infested",
                "Camel-Flavored",
                "Exploding",
                "Lethal",
                "Silly",
                "Luxury",
                "Aerodynamically Unstable",
                "Dead",
            ],
            "verbing_base_noun": [
                "Hamster",
                "Elderberry",
                "Fjord",
                "Parrot",
                "Whelk",
                "Frog",
                "Cheese",
                "Albatross",
                "Coconut",
                "Larch",
                "Bishop",
                "Snail",
                "Spam",
                "Sausage",
                "Camel",
                "Log",
            ],
            "verbing_suffix_gerund": [
                "Taunting",
                "Slapping",
                "Bashing",
                "Stretching",
                "Bothering",
                "Mongering",
                "Shifting",
                "Walking",
                "Exploding",
                "Stoneraising",
                "Lumberjacking",
                "Nudge-Nudging",
                "Spotting",
                "Cutting",
                "Lobbing",
            ],
            "noun_singular": [
                "Larch",
                "Fjord",
                "Spam",
                "Ex-Parrot",
                "Grail",
                "Brian",
                "Shrubbery",
                "Albatross",
                "Whelk",
                "Blancmange",
                "Herring",
                "Coconut Shell",
                "Sausage",
                "Hamster",
                "Elderberry",
                "Frog",
                "Cheese",
                "Bishop",
                "Snail",
                "Cushion",
                "Stick",
                "Log",
                "Salmon",
            ],
            "noun_plural": [
                "Eels",
                "Parrots",
                "Shrubberies",
                "Knights",
                "Albatrosses",
                "Elderberries",
                "Lumps",
                "Newts",
                "Frogs",
                "Spam-Eaters",
                "Gumbys",
                "Lumberjacks",
                "Bruces",
                "Whelks",
                "Chocolates",
                "Bonbons",
                "Clusters",
                "Lozenges",
                "Cushions",
                "Sticks",
                "Blancmanges",
                "Churns",
                "Bishops",
                "Snails",
                "Hamsters",
                "Philosophers",
            ],
            "botanical_item": [
                "Larch",
                "Horsetail Chestnut",
                "Weeping Fig",
                "Bristlecone Pine",
                "Monkey Puzzle Tree",
                "Slippery Elm",
                "Strangle-Weed",
                "Elderberry Bush",
            ],
            "institution_base": [
                "Ministry",
                "Department",
                "Royal Society",
                "Sub-Committee",
                "Brigade",
                "League",
                "Board of Inquiry",
                "Appeals Tribunal",
                "Amalgamated Union",
                "Regiment",
                "Consortium",
                "Task Force",
                "Advisory Council",
                "Guild",
                "Parish Council",
                "Truth Commission",
                "Study Group",
                "University",
                "Foundation",
                "Institute",
                "National Syndicate",
                "Commercial Cartel",
                "Cooperative Federation",
                "Wholesale Directorate",
            ],
            "institution_descriptor": [
                "Independent",
                "Official",
                "Empanelled",
                "Royal",
                "Joint",
                "Sanctioned",
                "Unorthodox",
                "Standing",
                "Interim",
                "Allocation",
                "",
            ],
            "bureaucratic_rank": [
                "Central",
                "Regional",
                "Imperial",
                "Joint-Chief",
                "Provisional",
                "Municipal",
                "",
            ],
            "bureaucratic_noun": [
                "License",
                "Permit",
                "Registration",
                "Regulation",
                "Taxation",
                "Sanitation",
                "Filing Fault",
                "System Breakdown",
            ],
            "academic_treatise": [
                "Discussion",
                "Treatise",
                "Symposium",
                "Monologue",
                "Disputation",
                "Tract",
            ],
            "ecclesiastical_body": [
                "Synod",
                "Conclave",
                "Ecumenical Council",
                "Tribunal of Heresy",
                "Consistory",
            ],
            "theological_crime": [
                "Heresy",
                "Blasphemy",
                "Schism",
                "Silly-Walking Apostasy",
                "Improper Shrubbery Veneration",
            ],
            "papal_edict": ["Papal Bull", "Encyclical", "Anathema", "Interdict"],
            "pejorative": [
                "Twit",
                "Gump",
                "Duffer",
                "Pill",
                "Rotter",
                "Burk",
                "Niddering",
                "Bounder",
                "Cloth-Ears",
                "Noodle",
                "Scoundrel",
                "Chump",
                "Ninny",
                "Toad-Eater",
                "Nuisance",
                "Wet",
                "Gilded Popinjay",
                "Milksop",
            ],
            "pejorative_plural": [
                "Twits",
                "Gumps",
                "Duffers",
                "Rotters",
                "Bounders",
                "Noodles",
                "Ninnies",
                "Milksops",
            ],
            "interruption_modifier": [
                "Temporary",
                "Unexpected",
                "Planned",
                "Unplanned",
                "Impromptu",
                "Intermittent",
                "Permanent",
                "Postponed",
                "Completely Silly",
                "Scheduled",
            ],
            "sports_clash": [
                "Cup Match",
                "Derby",
                "Showdown",
                "Heavyweight Bout",
                "Tournament",
                "Scrum",
            ],
            "competition": [
                "Competition",
                "Exhibition",
                "Gala",
                "Tribunal",
                "Showdown",
                "Audit",
                "Olympiad",
            ],
            "unladen_qualifier": [
                "Unladen",
                "Fully-Laden",
                "Slightly Weighted",
                "Over-Burdened",
                "Aerodynamically Unstable",
            ],
            "theatrical_format": [
                "Pantalloon",
                "Monologue",
                "Operetta",
                "Radio Drama",
                "Melodrama",
                "Puppet Play",
                "Documentary",
            ],
            "prohibition": [
                "Forbidden",
                "Prohibited by Law",
                "Subject to Heavy Taxation",
                "Deemed Entirely Too Silly",
            ],
            "name_title": [
                "Sir",
                "Inspector",
                "Cardinal",
                "Professor",
                "Mr.",
                "Mrs.",
                "Squire",
                "",
            ],
            "name_first": [
                "Arthur",
                "Gwen",
                "Biggus",
                "Tim",
                "Robin",
                "Brian",
                "Dennis",
                "Raymond",
                "Michael",
                "John",
                "Bruce",
            ],
            "name_last": [
                "Pewtey",
                "Dibley",
                "Dickus",
                "Luxury-Yacht",
                "Pither",
                "Ximénez",
                "Dim",
                "Cleese",
                "Palin",
                "Gumby",
            ],
            "geography_sing": ["Northumbria", "Wessex", "Finland", "Ruritania", "Basingstoke"],
            "verb_present": ["admires", "licenses", "questions", "understands", "inspects"],
            # Monty Python-inspired absurdist patterns
            "silly_occupation": [
                "Silly Walks",
                "Pointless Pursuits",
                "Job Interviewing",
                "Tea Making",
                "Shoe Fitting",
                "String Evaluating",
                "Knot Tying",
                "Teapot Designing",
                "Bird Calling",
                "Leaf Blowing",
                "Spoon Bending",
                "Clock Watching",
                "Grass Growing",
                "Paint Drying",
                "Waiting For",
                "Lost Cause Supporting",
            ],
            "pointless_pursuit": [
                "Extreme Ironing",
                "Competitive Napping",
                "Synchronized Sighing",
                "Professional Loitering",
                "Expert Queue Joining",
                "Advanced Staring",
                "Competitive Daydreaming",
                "Spoon Collecting",
                "Stone Skipping",
                "Cloud Shaping",
                "Shadow Chasing",
                "Echo Listening",
                "Wind Feeling",
                "Temperature Guessing",
                "Light Switching",
            ],
            "absurd_profession": [
                "Professional Chocolate Tasters",
                "Qualified Laughter Specialists",
                "Certified Sock Sorters",
                "Licensed Tea Bag Inspectors",
                "Registered Pencil Sharpeners",
                "Authorized Door Knockers",
                "Qualified Light Switch Operators",
                "Certified Elevator Button Pressers",
                "Licensed Fax Machine Operators",
                "Registered Stapler Refillers",
            ],
            "ridiculous_workers": [
                "Tea Bag Squeezers",
                "Sock Matchers",
                "Button Counters",
                "Lid Finders",
                "Spoon Polishers",
                "Napkin Folders",
                "Crumb Collectors",
                "Staple Removers",
                "Paper Clip Straighteners",
                "Pen Cap Finders",
                "Eraser Shredders",
                "Tape Dispenser Operators",
            ],
            "useless_studies": [
                "Sock Matching Theory",
                "Tea Bag Chemistry",
                "Button Statistics",
                "Lid Technology",
                "Spoon Aerodynamics",
                "Napkin Folding Art",
                "Crumb Analysis",
                "Staple Mechanics",
                "Paper Clip Metallurgy",
                "Pen Cap Physics",
                "Eraser Degradation Studies",
                "Tape Adhesion Research",
            ],
            "absurd_product": [
                "Left-Handed Sock Darners",
                "Tea Bag Squeezers",
                "Button Retrievers",
                "Lid Finders & Keepers",
                "Spoon Polishers & Shippers",
                "Napkin Folding Devices",
                "Crumb Collection Systems",
                "Staple Extraction Tools",
                "Paper Clip Straighteners",
                "Pen Cap Recovery Kits",
                "Eraser Revitalization Fluids",
                "Tape Dispenser Refillers",
            ],
            "pointless_service": [
                "Sock Matching Consultations",
                "Tea Bag Evaluation Services",
                "Button Counting & Verification",
                "Lid Compatibility Testing",
                "Spoon Polishing & Finishing",
                "Napkin Folding Instruction",
                "Crumb Analysis & Reporting",
                "Staple Removal Services",
                "Paper Clip Optimization Consulting",
                "Pen Cap Location Services",
                "Eraser Rejuvenation Treatments",
                "Tape Dispenser Calibration",
            ],
            "absurd_commodity": [
                "Individually Sorted Socks",
                "Premium Tea Bag Contents",
                "Factory-Fresh Buttons",
                "Guaranteed-Fit Container Lids",
                "Polished Serving Spoons",
                "Artistically Folded Napkins",
                "Laboratory-Grade Crumbs",
                "Quality-Controlled Staples",
                "Optimized Paper Clips",
                "Recovered Pen Caps",
                "Rejuvenated Erasers",
                "Calibrated Tape Dispensers",
            ],
            "pointless_activity": [
                "Sock Pairing",
                "Tea Bag Evaluation",
                "Button Counting",
                "Lid Matching",
                "Spoon Polishing",
                "Napkin Folding",
                "Crumb Collection",
                "Staple Removal",
                "Paper Clip Straightening",
                "Pen Cap Recovery",
                "Eraser Revitalization",
                "Tape Dispenser Maintenance",
            ],
            "ridiculous_goods": [
                "Mismatched Socks",
                "Used Tea Bags",
                "Odd Buttons",
                "Unmatched Container Lids",
                "Bent Spoons",
                "Crinkled Napkins",
                "Stale Crumbs",
                "Bent Staples",
                "Twisted Paper Clips",
                "Lost Pen Caps",
                "Worn Erasers",
                "Tangled Tape Dispensers",
            ],
            "form_number": [
                "FM-{{historical_ordinal}}",
                "FT-{{historical_ordinal}}",
                "FP-{{historical_ordinal}}",
                "FC-{{historical_ordinal}}",
                "FD-{{historical_ordinal}}",
                "FR-{{historical_ordinal}}",
                "FS-{{historical_ordinal}}",
                "FQ-{{historical_ordinal}}",
            ],
            "absurd_form_name": [
                "Application for Pointless Certification",
                "Request for Silly Walk Authorization",
                "Petition for Tea Making Privileges",
                "Claim for Button Counting Recognition",
                "Notification of Spoon Polishing Achievement",
                "Declaration of Napkin Folding Excellence",
                "Notice of Crumb Collection Merit",
                "Statement of Staple Removal Qualification",
            ],
            "pointless_permit": [
                "To Carry Spare Buttons",
                "For Tea Bag Transportation",
                "To Conduct Official Sock Inspections",
                "For Lid Evaluation Purposes",
                "To Practice Synchronized Spoon Polishing",
                "For Napkin Folding Demonstrations",
                "To Conduct Crumb Research Activities",
                "For Staple Analysis Work",
                "To Handle Paper Clip Distribution",
                "For Pen Custody Services",
                "To Operate Eraser Refurbishment Facilities",
                "For Tape Dispenser Calibration",
            ],
            "absurd_activity": [
                "Evaluating Tea Bag Quality",
                "Counting Factory-Sealed Buttons",
                "Matching Socks by Color & Wear",
                "Testing Container Lid Fit",
                "Polishing Serving Utensils",
                "Folding Napkins Artistically",
                "Collecting & Analyzing Table Crumbs",
                "Removing Office Staples",
                "Straightening Paper Clips in Bulk",
                "Recovering Lost Writing Implements",
                "Revitalizing Hardened Erasers",
                "Calibrating Adhesive Dispensers",
            ],
            "ridiculous_action": [
                "Wearing Socks on Hands",
                "Drinking Tea from Socks",
                "Using Buttons as Ear Plugs",
                "Holding Meetings in Tea Bags",
                "Eating Meals with Spoons Only",
                "Communicating via Napkin Folds",
                "Building Structures from Collected Crumbs",
                "Creating Art from Staples",
                "Constructing Devices from Paper Clips",
                "Writing with Recovered Pen Caps",
                "Drawing with Revitalized Erasers",
                "Measuring with Tape Dispensers",
            ],
            "useless_achievement": [
                "Outstanding Sock Matching Ability",
                "Expert Tea Bag Evaluation",
                "Master Button Counter Certification",
                "Advanced Lid Fitting Skills",
                "Professional Spoon Polishing Qualification",
                "Accomplished Napkin Folder",
                "Distinguished Crumb Collection Expertise",
                "Notable Staple Removal Technician",
                "Esteemed Paper Clip Optimization Specialist",
                "Renowned Pen Cap Recovery Agent",
                "Famous Eraser Revitalization Specialist",
                "Celebrated Tape Dispenser Calibrator",
            ],
            "absurd_entertainment": [
                "The Ministry of Silly Talent Show",
                "The Pointless Pursuit Parade",
                "The Button Counting Championships",
                "The Tea Making Competitions",
                "The Sock Matching Spectacular",
                "The Napkin Folding Expo",
                "The Crumb Collection Convention",
                "The Staple Removal Symposium",
                "The Paper Clip Optimization Forum",
                "The Pen Cap Recovery Seminar",
                "The Eraser Revitalization Conference",
                "The Tape Dispenser Calibration Summit",
            ],
            "pointless_celebrity": [
                "Sir Socks-a-Lot",
                "Madame Tea-Bag",
                "Professor Button",
                "Countess Lid-Fit",
                "Baron Spoon-Polish",
                "Duke Napkin-Fold",
                "Earl Crumb-Collector",
                "Viscount Staple-Remover",
                "Lord Paper-Clip",
                "Baronet Pen-Cap",
                "Sir Eraser-Revitalize",
                "Count Tape-Dispenser",
            ],
            "absurd_talent": [
                "Extreme Sock Matching",
                "Competitive Tea Bag Evaluation",
                "Professional Button Counting",
                "Expert Lid Fitting",
                "Master Spoon Polishing",
                "Champion Napkin Folding",
                "Grand Crumb Collection",
                "Expert Staple Removal",
                "Supreme Paper Clip Straightening",
                "Ultimate Pen Cap Recovery",
                "Ultimate Eraser Revitalization",
                "Ultimate Tape Dispenser Calibration",
            ],
            "ridiculous_production": [
                "Socks: The Musical",
                "Tea: A Love Story",
                "Buttons: The Sequel",
                "Lids: The Return",
                "Spoons: The Epic",
                "Napkins: The Saga",
                "Crumbs: The Chronicles",
                "Staples: The Trilogy",
                "Paper Clips: The Series",
                "Pen Caps: The Revenge",
                "Erasers: The Comeback",
                "Tape: The Finale",
            ],
            "absurd_performance": [
                "The One-Man Sock Show",
                "The Solo Tea Bag Recap",
                "The Button Counting Extravaganza",
                "The Lid Fitting Spectacle",
                "The Napkin Folding Fiesta",
                "The Crumb Collection Carnival",
                "The Staple Removal Jubilee",
                "The Paper Clip Straightening Fest",
                "The Pen Cap Recovery Celebration",
                "The Eraser Revitalization Bash",
                "The Tape Dispenser Calibration Blowout",
            ],
            "pointless_spectacle": [
                "A Display of Sock Matching Prowess",
                "An Exhibition of Tea Bag Expertise",
                "A Demonstration of Button Counting Mastery",
                "A Presentation of Lid Fitting Skill",
                "A Showcase of Spoon Polishing Excellence",
                "A Spectacle of Napkin Folding Art",
                "A Festival of Crumb Collection Achievement",
                "A Carnival of Staple Removal Skill",
                "A Fair of Paper Clip Optimization",
                "A Jubilee of Pen Cap Recovery",
                "A Bash of Eraser Revitalization",
                "A Blowout of Tape Dispenser Calibration",
            ],
            "pointless_theory": [
                "The Sock Matching Principle",
                "The Tea Bag Equilibrium Theorem",
                "The Button Conservation Law",
                "The Lid Compatibility Principle",
                "The Spoon Polishing Hypothesis",
                "The Napkin Folding Conjecture",
                "The Crumb Collection Principle",
                "The Staple Removal Theory",
                "The Paper Clip Optimization Law",
                "The Pen Cap Recovery Principle",
                "The Eraser Degradation Hypothesis",
                "The Tape Adhesion Conjecture",
            ],
            "absurd_academic_topic": [
                "Sock Symmetry Studies",
                "Tea Bag Rheology Research",
                "Button Distribution Analysis",
                "Lid Engineering Principles",
                "Spoon Aerodynamics Research",
                "Napkin Topology Studies",
                "Crumb Statistical Analysis",
                "Staple Mechanics Research",
                "Paper Clip Materials Science",
                "Pen Cap Recovery Techniques",
                "Eraser Polymer Studies",
                "Tape Adhesion Physics",
            ],
            "ridiculous_research": [
                "The Effect of Sock Color on Matching Speed",
                "The Influence of Tea Temperature on Bag Integrity",
                "The Relationship Between Button Size and Counting Accuracy",
                "The Impact of Lid Material on Sealing Effectiveness",
                "The Correlation Between Spoon Shape and Polishing Efficiency",
                "The Connection Between Napkin Fold Complexity and Aesthetic Value",
                "The Study of Crumb Size Distribution in Domestic Environments",
                "Research on Staple Geometry and Removal Force Requirements",
                "Investigation of Paper Clip Metallurgy and Elastic Properties",
                "Analysis of Pen Cap Geometry and Retrieval Success Rates",
                "Studies on Eraser Composition and Revitalization Methods",
                "Experiments on Tape Width and Adhesive Bond Strength",
            ],
            "absurd_college": [
                "College of Sock Science",
                "Institute of Tea Bag Technology",
                "Academy of Button Studies",
                "University of Lid Engineering",
                "School of Spoon Aerodynamics",
                "College of Napkin Design",
                "Institute of Crumb Analysis",
                "Academy of Staple Mechanics",
                "University of Paper Clip Technology",
                "College of Pen Cap Science",
                "Institute of Eraser Research",
                "School of Tape Adhesion Studies",
            ],
            "pointless_philosophy": [
                "The Meaning of Sock Matching",
                "The Purpose of Tea Bag Evaluation",
                "The Nature of Button Existence",
                "The Essence of Lid Function",
                "The Reality of Spoon Utility",
                "The Significance of Napkin Folding",
                "The Value of Crumb Collection",
                "The Purpose of Staple Existence",
                "The Meaning of Paper Clip Organization",
                "The Point of Pen Cap Recovery",
                "The Significance of Eraser Longevity",
                "The Purpose of Tape Adhesion",
            ],
            "absurd_vehicle": [
                "Sock-Powered Bicycle",
                "Tea Bag Propelled Scooter",
                "Button-Driven Skateboard",
                "Lid-Based Unicycle",
                "Spoon-Propelled Wheelchair",
                "Napkin-Folded Glider",
                "Crumb-Fueled Rocket",
                "Staple-Powered Catapult",
                "Paper Clip-Driven Helicopter",
                "Pen Cap-Powered Submarine",
                "Eraser-Propelled Sled",
                "Tape Dispenser-Launched Drone",
            ],
            "pointless_journey": [
                "The Quest for the Perfect Sock Pair",
                "The Pilgrimage to the Ideal Tea Bag",
                "The Expedition to Find Matching Buttons",
                "The Journey to the Perfect Lid Fit",
                "The Crusade for Ultimate Spoon Polish",
                "The Mission for Flawless Napkin Folding",
                "The Campaign for Complete Crumb Collection",
                "The Voyage for Total Staple Removal",
                "The Trek for Complete Paper Clip Straightening",
                "The Safari for Ultimate Pen Cap Recovery",
                "The Odyssey for Complete Eraser Revitalization",
                "The Cruise for Perfect Tape Calibration",
            ],
            "ridiculous_transport": [
                "Sock Monorail",
                "Tea Bag Cable Car",
                "Button Tramway",
                " Lid Gondola",
                "Spoon Chairlift",
                "Napkin Zip Line",
                "Crumb Conveyor Belt",
                "Staple Escalator",
                "Paper Clip Moving Walkway",
                "Pen Cap People Mover",
                "Escalator Eraser Transport",
                "Moving Tape Walkway",
            ],
            "absurd_navigation": [
                "Sock-Based Wayfinding",
                "Tea Bag Guided Tours",
                "Button-Compass Navigation",
                "Landmark-Based Lid Following",
                "Spoon-Direction Finding",
                "Napkin-Folded Route Planning",
                "Crumb Trail Navigation",
                "Staple-Based Orientation",
                "Paper Clip Guidance Systems",
                "Pen Cap Tracking Methods",
                "Eraser-Based Location Services",
                "Tape-Determined Positioning",
            ],
            "pointless_routing": [
                "Optimal Sock Distribution Pathways",
                "Tea Bag Delivery Route Optimization",
                "Button Collection Circuit Design",
                "Lid Allocation Network Planning",
                "Spoon Service Area Mapping",
                "Napkin Distribution Logistics Planning",
                "Crumb Collection Route Planning",
                "Staple Removal Service Routing",
                "Paper Clip Redistribution Systems",
                "Pen Cap Recovery Network Design",
                "Eraser Refurbishment Logistics",
                "Tape Dispenser Service Area Planning",
            ],
            # Modular components for deconstructed historical competition templates
            "historical_competition_prefix": [
                "The {{historical_ordinal}} {{optional_annual}}",
                "In the {{historical_ordinal}} {{optional_annual}} Year",
                "{{historical_ordinal}} {{optional_annual}} Edition of",
            ],
            "historical_competition_middle": [
                "{{optional_modifier}} {{pejorative}}",
                "{{pejorative}} {{optional_modifier}}",
                "{{optional_modifier}} Contender",
            ],
            "historical_competition_suffix": [
                "of the Year {{competition}}",
                "{{competition}} Champions",
                "Year-End {{competition}}",
            ],
            # Modular components for legal templates
            "legal_authority": [
                "Under Section",
                "According to Clause",
                "Per Regulation",
                "By Statute",
                "Pursuant to",
            ],
            "legal_location": [
                "{{historical_ordinal}} Subsection",
                "Section {{historical_ordinal}}",
                "Article {{historical_ordinal}}",
                "Paragraph {{historical_ordinal}}",
                "Clause {{historical_ordinal}}",
            ],
            "legal_framework": ["Act", "Code", "Ordinance", "Decree", "Statute"],
            "legal_statute": [
                "Statute {{historical_ordinal}}",
                "Regulation {{historical_ordinal}}",
                "Ordinance {{historical_ordinal}}",
                "Code Section {{historical_ordinal}}",
                "Bylaw {{historical_ordinal}}",
            ],
            "adverb": [
                "Strictly",
                "Absolutely",
                "Universally",
                "Categorically",
                "Definitively",
                "",
            ],
            # Modular components for academic position templates
            "academic_title": [
                "Chair of",
                "Head of Department for",
                "Director of Studies in",
                "Professor of",
                "Lead Researcher in",
                "Senior Fellow in",
            ],
            "institution_affiliation": [
                "at the {{enhanced_institution}}",
                "of {{enhanced_institution}}",
                "within {{enhanced_institution}}",
                "affiliated with {{enhanced_institution}}",
                "based at {{enhanced_institution}}",
            ],
            # Modular components for sports competition templates
            "sports_event": [
                "Semi-Finals",
                "Quarter-Finals",
                "Preliminary Round",
                "Qualifying Match",
                "Opening Round",
            ],
        }
        # Pre-calculate template complexities for performance
        self._template_complexities = self._calculate_template_complexities()

    def _calculate_template_complexities(self) -> list[int]:
        """
        Calculate the complexity (total number of tokens) for each START template.

        Recursively counts tokens in nested grammar references.

        Returns:
            List of integers representing the complexity of each template in START
        """
        complexities = []
        for template in self._grammar["START"]:
            token_count = self._count_total_tokens(template)
            complexities.append(token_count)
        return complexities

    def _count_total_tokens(self, pattern: str, visited: set[str] | None = None) -> int:
        """
        Recursively count all tokens in a pattern, including nested grammar references.

        Args:
            pattern: The pattern to count tokens in
            visited: Set of already visited tokens to avoid infinite recursion

        Returns:
            Total token count
        """
        if visited is None:
            visited = set()

        count = 0
        # Find all tokens in the pattern
        for match in self._TOKEN.finditer(pattern):
            token = match.group(1)
            count += 1

            if token in visited:
                continue

            visited.add(token)

            # If this token is handled by _resolve() (not directly in grammar),
            # recurse into its component grammar keys
            if token in self._RESOLVE_TOKEN_MAP:
                for grammar_key in self._RESOLVE_TOKEN_MAP[token]:
                    if grammar_key in self._grammar and grammar_key not in visited:
                        visited.add(grammar_key)
                        for option in self._grammar[grammar_key]:
                            if isinstance(option, str):
                                count += self._count_total_tokens(option, visited.copy())
            # If this token references a grammar entry that has tokens, count those too
            elif token in self._grammar:
                for option in self._grammar[token]:
                    if isinstance(option, str):
                        count += self._count_total_tokens(option, visited.copy())
        return count

    def _filter_templates_by_complexity(
        self, complexity: int | tuple[int, int] | None
    ) -> list[int]:
        """
        Get indices of START templates that match the complexity criteria.

        Args:
            complexity: None (all templates), int (exact count), or tuple (min, max) range

        Returns:
            List of template indices that match the complexity criteria
        """
        if complexity is None:
            # No filtering - all templates eligible
            return list(range(len(self._grammar["START"])))

        if isinstance(complexity, int):
            # Exact match
            return [i for i, count in enumerate(self._template_complexities) if count == complexity]

        if isinstance(complexity, tuple) and len(complexity) == 2:
            # Range match
            min_complexity, max_complexity = complexity
            return [
                i
                for i, count in enumerate(self._template_complexities)
                if min_complexity <= count <= max_complexity
            ]

        # Invalid complexity specification - fallback to all templates
        return list(range(len(self._grammar["START"])))

    def _generate_historical_ordinal(self) -> str:
        number = self._rng.randint(1, 14)
        suffix = "th" if 11 <= number <= 13 else {1: "st", 2: "nd", 3: "rd"}.get(number % 10, "th")
        return f"{number}{suffix}"

    def _build_proper_noun(self) -> str:
        title, first, last = (
            self._rng.choice(self._grammar[key])
            for key in ("name_title", "name_first", "name_last")
        )
        if self._rng.random() < 0.15:
            first = f"{first} 'The {self._rng.choice(self._grammar['pejorative'])}'"
        surname = last
        if self._rng.random() < 0.30:
            other = self._rng.choice(self._grammar["name_last"])
            while other == last:
                other = self._rng.choice(self._grammar["name_last"])
            surname = f"{last}-{other}"
        return f"{title} {first} {surname}".strip()

    def _resolve(self, token: str) -> str:
        if token == "historical_ordinal":
            return self._generate_historical_ordinal()
        if token == "generated_proper_noun":
            return self._build_proper_noun()
        if token == "enhanced_institution":
            descriptor = self._rng.choice(self._grammar["institution_descriptor"])
            base = self._rng.choice(self._grammar["institution_base"])
            return f"{descriptor} {base}".strip()
        if token == "generated_legal_action":
            return self._join(
                self._expand(self._rng.choice(self._grammar["legal_core_action"])),
                self._expand(self._rng.choice(self._grammar["legal_situational_pattern"])),
            )
        if token == "generated_natural_philosophy_axiom":
            prefix = self._rng.choice(self._grammar["science_prefix"])
            prop = self._rng.choice(self._grammar["science_property"])
            return self._join(
                prefix,
                prop,
                self._rng.choice(self._grammar["science_connector"]),
                self._expand(self._rng.choice(self._grammar["science_target"])),
                self._rng.choice(self._grammar["science_constraint"]),
            )
        if token == "generated_academic_body":
            if self._rng.random() < 0.20:
                return self._rng.choice(self._grammar["academic_body_noun"])
            return self._join(
                self._rng.choice(self._grammar["academic_body_modifier"]),
                self._rng.choice(self._grammar["academic_body_noun"]),
            )
        if token == "generated_logistics_action":
            if self._rng.random() < 0.30:
                return self._rng.choice(self._grammar["logistics_vector"])
            return self._join(
                self._rng.choice(self._grammar["logistics_tier"]),
                self._rng.choice(self._grammar["logistics_vector"]),
            )
        if token == "generated_academic_discipline":
            return self._join(
                self._rng.choice(self._grammar["academic_prefix"]),
                self._resolve("academic_subject_structure"),
            )
        if token == "noun_verbing":
            return f"{self._rng.choice(self._grammar['verbing_base_noun'])}-{self._rng.choice(self._grammar['verbing_suffix_gerund'])}"
        if token not in self._grammar:
            return token
        return self._expand(self._rng.choice(self._grammar[token]))

    def _expand(self, pattern: str) -> str:
        """Resolve all placeholders in a selected grammar pattern."""
        while match := self._TOKEN.search(pattern):
            pattern = pattern.replace(match.group(0), self._resolve(match.group(1)), 1)
        return pattern

    @staticmethod
    def _join(*parts: str) -> str:
        return " ".join(part for part in parts if part)

    @classmethod
    def _fix_indefinite_articles(cls, text: str) -> str:
        # Fix "a" -> "an" before vowel sounds
        text = re.sub(
            r"\b([Aa])\s+([\w-]+)",
            lambda m: (
                ("An" if m.group(1) == "A" else "an") + " " + m.group(2)
                if cls._VOWEL_SOUND.match(m.group(2))
                else m.group(0)
            ),
            text,
        )
        # Fix "an" -> "a" before consonant sounds
        text = re.sub(
            r"\b([Aa])n\s+([\w-]+)",
            lambda m: (
                ("A" if m.group(1) == "A" else "a") + " " + m.group(2)
                if not cls._VOWEL_SOUND.match(m.group(2))
                else m.group(0)
            ),
            text,
        )
        return text

    def _slugify(self, text: str) -> str:
        """
        Convert text to a URL-friendly slug.

        Improved slugification that:
        1. Converts to lowercase
        2. Handles common symbol-to-word conversions
        3. Handles basic Unicode transliteration
        4. Replaces non-alphanumeric with hyphens
        5. Normalizes multiple hyphens to single
        6. Trims leading/trailing hyphens

        Args:
            text: Input string to slugify

        Returns:
            URL-friendly slug string
        """
        if not text:
            return ""

        # Convert to lowercase
        result = text.lower()

        # Symbol to word mappings (basic set)
        symbol_map = {
            "&": "and",
            "$": "usd",
            "€": "eur",
            "£": "gbp",
            "¥": "jpy",
            "%": "pct",
            "@": "at",
            "+": "plus",
            "=": "eq",
            "<": "lt",
            ">": "gt",
        }

        # Replace symbols with words
        for symbol, word in symbol_map.items():
            result = result.replace(symbol, f" {word} ")

        # Basic Unicode transliteration (common accented characters)
        unicode_map = {
            "à": "a",
            "á": "a",
            "â": "a",
            "ã": "a",
            "ä": "a",
            "å": "a",
            "æ": "ae",
            "ç": "c",
            "è": "e",
            "é": "e",
            "ê": "e",
            "ë": "e",
            "ì": "i",
            "í": "i",
            "î": "i",
            "ï": "i",
            "ð": "d",
            "ñ": "n",
            "ò": "o",
            "ó": "o",
            "ô": "o",
            "õ": "o",
            "ö": "o",
            "ø": "o",
            "ù": "u",
            "ú": "u",
            "û": "u",
            "ü": "u",
            "ý": "y",
            "þ": "th",
            "ÿ": "y",
            "ă": "a",
            "ą": "a",
            "Ą": "A",
        }

        # Apply Unicode transliteration
        for unicode_char, ascii_char in unicode_map.items():
            result = result.replace(unicode_char, ascii_char)
            result = result.replace(unicode_char.upper(), ascii_char.upper())

        # Replace non-alphanumeric characters (except spaces) with hyphens
        result = re.sub(r"[^a-z0-9\s]", "-", result)

        # Replace multiple spaces/hyphens with single hyphen
        result = re.sub(r"[\s-]+", "-", result)

        # Remove leading/trailing hyphens
        result = result.strip("-")

        # Limit length to reasonable maximum (similar to WP)
        if len(result) > 100:
            result = result[:100].rstrip("-")

        return result

    def generate(
        self,
        slugify: bool = False,
        complexity: int | tuple[int, int] | None = None,
        allow_leading_the: bool = True,
    ) -> str | tuple[str, str]:
        """Return the next generated title; optionally return a URL-safe slug.

        Args:
            slugify: If True, return tuple of (title, slug), else just title
            complexity: None (any length), int (exact length), or tuple (min, max) range
            allow_leading_the: If False, strip leading "The " from result

        Returns:
            If slugify=False: str (title)
            If slugify=True: tuple of (title, slug)
        """
        # Get filtered template indices based on complexity
        eligible_indices = self._filter_templates_by_complexity(complexity)

        # If no templates match complexity criteria, fall back to all templates
        if not eligible_indices:
            eligible_indices = list(range(len(self._grammar["START"])))

        # Select a random template from eligible ones
        selected_index = self._rng.choice(eligible_indices)
        selected_template = self._grammar["START"][selected_index]

        # Generate the phrase
        phrase = self._fix_indefinite_articles(self._expand(selected_template))
        phrase = " ".join(phrase.split())

        # Apply leading "The" control
        if not allow_leading_the and phrase.startswith("The "):
            phrase = phrase[4:]  # Remove "The " prefix

        # Apply slugify if requested
        if slugify:
            slug = self._slugify(phrase)
            return (phrase, slug)
        return phrase

    def generate_multiple(
        self,
        count: int,
        slugify: bool = False,
        complexity: int | tuple[int, int] | None = None,
        allow_leading_the: bool = True,
    ) -> list[str | tuple[str, str]]:
        """
        Generate multiple titles at once.

        Args:
            count: Number of titles to generate
            slugify: If True, return list of (title, slug) tuples, else list of titles
            complexity: None (any length), int (exact length), or tuple (min, max) range
            allow_leading_the: If False, strip leading "The " from results

        Returns:
            If slugify=False: List[str] (titles)
            If slugify=True: List[Tuple[str, str]] (title, slug tuples)
        """
        if not isinstance(count, int) or count < 1:
            raise ValueError("count must be a positive integer")
        return [
            self.generate(
                slugify=slugify, complexity=complexity, allow_leading_the=allow_leading_the
            )
            for _ in range(count)
        ]

    def generate_unique(
        self,
        count: int = 10,
        slugify: bool = False,
        complexity: int | tuple[int, int] | None = None,
        allow_leading_the: bool = True,
    ) -> list[str | tuple[str, str]]:
        """
        Generate multiple unique titles (no duplicates).

        Args:
            count: Number of unique titles to generate
            slugify: If True, return list of (title, slug) tuples, else list of titles
            complexity: None (any length), int (exact length), or tuple (min, max) range
            allow_leading_the: If False, strip leading "The " from results

        Returns:
            If slugify=False: List[str] (titles)
            If slugify=True: List[Tuple[str, str]] (title, slug tuples)
        """
        if not isinstance(count, int) or count < 1:
            raise ValueError("count must be a positive integer")

        results: list[str | tuple[str, str]] = []
        # Generate extra to account for potential duplicates, but limit attempts
        max_attempts = count * 5  # Reasonable limit to avoid infinite loops
        attempts = 0

        while len(results) < count and attempts < max_attempts:
            result = self.generate(
                slugify=slugify, complexity=complexity, allow_leading_the=allow_leading_the
            )
            if result not in results:
                results.append(result)
            attempts += 1

        return results

    def get_seed(self) -> str:
        """
        Get the seed used to initialize this generator.

        Returns:
            The seed string
        """
        return self._seed

    def get_template_stats(self) -> dict[str, int]:
        """
        Get statistics about the grammar templates.

        Returns:
            Dictionary with template category names and their option counts
        """
        return {key: len(value) for key, value in self._grammar.items() if isinstance(value, list)}

    def list_templates(self, category: str | None = None) -> list[str] | dict[str, list[str]]:
        """
        List available templates or template categories.

        Args:
            category: Optional category name to list templates for.
                     If None, returns all categories and their templates.

        Returns:
            If category is specified: List of templates in that category
            If category is None: Dictionary of all categories and their templates
        """
        if category is None:
            return {key: value for key, value in self._grammar.items() if isinstance(value, list)}
        elif category in self._grammar and isinstance(self._grammar[category], list):
            return self._grammar[category]
        else:
            return []
