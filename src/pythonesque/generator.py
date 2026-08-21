"""The generator implementation."""

import hashlib
import random
import re
from typing import Dict, List


class UnifiedFoundationalGenerator:
    """Generate deterministic, Python-esque institutional titles from a seed.

    Each instance owns its random-number generator, so using this class never
    changes the process-wide random state.
    """

    _TOKEN = re.compile(r"{{(\w+)}}")
    _VOWEL_SOUND = re.compile(r"^(?:[aeiou]|honest|honor|hour|heir)", re.I)

    def __init__(self, seed: str = "The Larch") -> None:
        if not isinstance(seed, str):
            raise TypeError("seed must be a string")
        self._rng = random.Random(int(hashlib.md5(seed.encode("utf-8")).hexdigest(), 16))
        self._grammar: Dict[str, List[str]] = {
            "START": [
                "The {{enhanced_institution}}", "The {{generated_academic_body}}", "The {{ecclesiastical_body}}",
                "The {{abstracted_object}} {{enhanced_institution}}", "The {{abstracted_object}} {{generated_logistics_action}}",
                "The {{enhanced_institution}} of {{noun_verbing}} {{noun_plural}}",
                "The {{bureaucratic_rank}} {{enhanced_institution}} for {{noun_verbing}} {{noun_plural}}",
                "The {{botanical_item}} {{noun_verbing}} {{geography_sing}}", "No one {{verb_present}} the {{optional_nationality}} {{generated_academic_body}}",
                "A Brief {{academic_treatise}} on {{optional_modifier}} {{noun_plural}}",
                "The {{historical_ordinal}} {{optional_annual}} {{optional_modifier}} {{pejorative}} of the Year {{competition}}",
                "A {{unladen_qualifier}} {{optional_nationality}} {{noun_singular}}", "The {{generated_proper_noun}} and {{generated_proper_noun}} {{generated_academic_body}}",
                "We Apologize for the {{optional_modifier}} {{noun_verbing}} of the {{noun_singular}}", "The {{geography_sing}} and {{geography_sing}} Cooperative {{enhanced_institution}}",
                "{{generated_proper_noun}}, Assistant Under-Secretary for {{noun_verbing}}", "A Audition for the Role of the {{optional_modifier}} {{noun_singular}}",
                "A {{theatrical_format}} Adaptation of the {{noun_verbing}} {{noun_singular}}", "The {{historical_ordinal}} Century Costumed {{theatrical_format}} on {{noun_verbing}}",
                "By Order of the {{bureaucratic_rank}} {{enhanced_institution}}, {{generated_legal_action}} is Strictly {{prohibition}}",
                "Under Subsection {{historical_ordinal}} of the {{geography_sing}} {{bureaucratic_noun}} Act, {{generated_legal_action}} is Prohibited",
                "The Chair of {{generated_academic_discipline}} at the {{enhanced_institution}} of {{geography_sing}}", "A Controversial Study in the Field of {{optional_modifier}} {{generated_academic_discipline}}",
                "The Board of Directors for {{abstracted_object}} {{generated_logistics_action}}", "The {{enhanced_institution}} for the {{generated_logistics_action}} of {{abstracted_object}}",
                "We Are Experiencing {{interruption_modifier}} {{bureaucratic_noun}} {{generated_academic_body}}", "The {{historical_ordinal}} Semi-Finals of the {{optional_nationality}} {{generated_academic_discipline}} {{sports_clash}}",
                "The Amalgamated Union of {{pejorative_plural}} and {{generated_academic_discipline}} Practitioners", "A Defensive Strategy for Countering an Attack by {{optional_modifier}} {{botanical_item}}",
                "The {{bureaucratic_rank}} Registry of Lethal {{abstracted_object}} Deployments", "The Annexation of {{optional_nationality}} {{geography_sing}} by the {{enhanced_institution}}",
                "The {{historical_ordinal}} {{ecclesiastical_body}} on the {{optional_modifier}} {{theological_crime}}", "A Decreed {{papal_edict}} Concerning the Excommunication of {{pejorative_plural}}",
                "The {{optional_nationality}} Inquisition into {{noun_verbing}}", "The Theory of the {{noun_singular}}, by {{generated_proper_noun}}", "A Fundamental Law of {{generated_natural_philosophy_axiom}} regarding {{noun_plural}}",
            ],
            "legal_core_action": ["{{noun_verbing}}", "The Silly-Walking of {{noun_plural}}", "The Unlicensed Placement of {{abstracted_object}}", "The Private Hoarding of {{abstracted_object}}"],
            "legal_situational_pattern": ["after Dark", "during High Tea", "on Bank Holidays", "in a Public Wardrobe", "while {{noun_verbing}}", "while Escorting {{abstracted_object}}", "without {{bureaucratic_noun}}", "without Written Permission from the {{bureaucratic_rank}} {{academic_body_noun}}", ""],
            "science_prefix": ["Relative", "Thermodynamic", "Gravitational", "Centrifugal", "Aerodynamic", "Submergence", "Larch-Centric", ""],
            "science_property": ["Slippage", "Buoyancy", "Astronomy", "Deficit", "Velocity", "Dynamics", "Inertia", "Oscillation", "Elasticity"], "science_connector": ["in", "of", "across", "between", "regarding"],
            "science_constraint": ["under Pressure", "at Low Altitudes", "after Dark", "in Free Fall", "during High Tea", "without a License", ""], "science_target": ["{{noun_plural}}", "{{noun_singular}}", "{{botanical_item}}"],
            "academic_body_modifier": ["Argument", "Vocational Guidance", "Philosophy", "Logicians", "Brain-Drain", "Interruption", "Exposition", "Nudge-Nudge"], "academic_body_noun": ["Clinic", "Office", "Faculty", "Council", "Laboratory", "Exhibition", "Inquisition"],
            "logistics_tier": ["Retail", "Wholesale", "Black-Market", "Compulsory", "Industrial", "Unlicensed", "Bureaucratic", "Maritime"], "logistics_vector": ["Procurement", "Smuggling", "Sourcing", "Allocation", "Accumulation", "Hoarding", "Distribution", "Consignment"],
            "academic_prefix": ["Comparative", "Advanced", "Applied", "Pre-Renaissance", "Theoretical", "The Epistemology of", "Experimental Defense against", ""], "academic_subject_structure": ["{{verbing_base_noun}}-{{verbing_suffix_gerund}}", "{{verbing_base_noun}} Morphology", "{{verbing_base_noun}} Selection", "Silly Walking", "Fresh Fruit"],
            "abstracted_object": ["{{noun_plural}}", "{{noun_singular}}", "{{brand_mod}} {{noun_plural}}", "{{sensory_mod}} {{noun_plural}}", "{{brand_mod}} {{sensory_mod}} {{noun_plural}}", "{{brand_mod}} {{sensory_mod}} {{noun_singular}}"],
            "optional_modifier": ["Silly", "Upper-Class", "Completely Non-Subversive", "Not-at-all-Absurd", "Dead", "Defending", "Exploding", "Defiant", "Runaway", "Luxury", "Highly Dangerous", "Self-Defending", "Lethal", "Bleeding-Heart", "Bourgeois", "Semiotical", "Sudden", ""], "optional_nationality": ["Spanish", "French", "Norwegian", "British", "Roman", "Swallow-bound", "Australian", "Icelandic", "Welsh", "Transylvanian", "Hungarian", "Moustachistani", "Upper-Vannu", "Bratislavian", "San Serif", "Oolong-bound", ""], "optional_annual": ["Annual", "Bi-Centennial", "Impromptu", "Quarterly", "Tri-Centennial", ""],
            "brand_mod": ["Whizz-Bang", "Spring-Surprise", "Unlicensed", "Military-Grade", "Smuggled", "Gilded", "Royal", "Self-Defending", "Black-Market"], "sensory_mod": ["Crunchy", "Cockroach-Infested", "Camel-Flavored", "Exploding", "Lethal", "Silly", "Luxury", "Aerodynamically Unstable", "Dead"],
            "verbing_base_noun": ["Hamster", "Elderberry", "Fjord", "Parrot", "Whelk", "Frog", "Cheese", "Albatross", "Coconut", "Larch", "Bishop", "Snail", "Spam", "Sausage", "Camel", "Log"], "verbing_suffix_gerund": ["Taunting", "Slapping", "Bashing", "Stretching", "Bothering", "Mongering", "Shifting", "Walking", "Exploding", "Stoneraising", "Lumberjacking", "Nudge-Nudging", "Spotting", "Cutting", "Lobbing"],
            "noun_singular": ["Larch", "Fjord", "Spam", "Ex-Parrot", "Grail", "Brian", "Shrubbery", "Albatross", "Whelk", "Blancmange", "Herring", "Coconut Shell", "Sausage", "Hamster", "Elderberry", "Frog", "Cheese", "Bishop", "Snail", "Cushion", "Stick", "Log", "Salmon"], "noun_plural": ["Eels", "Parrots", "Shrubberies", "Knights", "Albatrosses", "Elderberries", "Lumps", "Newts", "Frogs", "Spam-Eaters", "Gumbys", "Lumberjacks", "Bruces", "Whelks", "Chocolates", "Bonbons", "Clusters", "Lozenges", "Cushions", "Sticks", "Blancmanges", "Churns", "Bishops", "Snails", "Hamsters", "Philosophers"], "botanical_item": ["Larch", "Horsetail Chestnut", "Weeping Fig", "Bristlecone Pine", "Monkey Puzzle Tree", "Slippery Elm", "Strangle-Weed", "Elderberry Bush"],
            "institution_base": ["Ministry", "Department", "Royal Society", "Sub-Committee", "Brigade", "League", "Board of Inquiry", "Appeals Tribunal", "Amalgamated Union", "Regiment", "Consortium", "Task Force", "Advisory Council", "Guild", "Parish Council", "Truth Commission", "Study Group", "University", "Foundation", "Institute", "National Syndicate", "Commercial Cartel", "Cooperative Federation", "Wholesale Directorate"], "institution_descriptor": ["Independent", "Official", "Empanelled", "Royal", "Joint", "Sanctioned", "Unorthodox", "Standing", "Interim", "Allocation", ""],
            "bureaucratic_rank": ["Central", "Regional", "Imperial", "Joint-Chief", "Provisional", "Municipal", ""], "bureaucratic_noun": ["License", "Permit", "Registration", "Regulation", "Taxation", "Sanitation", "Filing Fault", "System Breakdown"], "academic_treatise": ["Discussion", "Treatise", "Symposium", "Monologue", "Disputation", "Tract"], "ecclesiastical_body": ["Synod", "Conclave", "Ecumenical Council", "Tribunal of Heresy", "Consistory"], "theological_crime": ["Heresy", "Blasphemy", "Schism", "Silly-Walking Apostasy", "Improper Shrubbery Veneration"], "papal_edict": ["Papal Bull", "Encyclical", "Anathema", "Interdict"],
            "pejorative": ["Twit", "Gump", "Duffer", "Pill", "Rotter", "Burk", "Niddering", "Bounder", "Cloth-Ears", "Noodle", "Scoundrel", "Chump", "Ninny", "Toad-Eater", "Nuisance", "Wet", "Gilded Popinjay", "Milksop"], "pejorative_plural": ["Twits", "Gumps", "Duffers", "Rotters", "Bounders", "Noodles", "Ninnies", "Milksops"], "interruption_modifier": ["Temporary", "Unexpected", "Planned", "Unplanned", "Impromptu", "Intermittent", "Permanent", "Postponed", "Completely Silly", "Scheduled"], "sports_clash": ["Cup Match", "Derby", "Showdown", "Heavyweight Bout", "Tournament", "Scrum"], "competition": ["Competition", "Exhibition", "Gala", "Tribunal", "Showdown", "Audit", "Olympiad"], "unladen_qualifier": ["Unladen", "Fully-Laden", "Slightly Weighted", "Over-Burdened", "Aerodynamically Unstable"], "theatrical_format": ["Pantalloon", "Monologue", "Operetta", "Radio Drama", "Melodrama", "Puppet Play", "Documentary"], "prohibition": ["Forbidden", "Prohibited by Law", "Subject to Heavy Taxation", "Deemed Entirely Too Silly"],
            "name_title": ["Sir", "Inspector", "Cardinal", "Professor", "Mr.", "Mrs.", "Squire", ""], "name_first": ["Arthur", "Gwen", "Biggus", "Tim", "Robin", "Brian", "Dennis", "Raymond", "Michael", "John", "Bruce"], "name_last": ["Pewtey", "Dibley", "Dickus", "Luxury-Yacht", "Pither", "Ximénez", "Dim", "Cleese", "Palin", "Gumby"],
            "geography_sing": ["Northumbria", "Wessex", "Finland", "Ruritania", "Basingstoke"], "verb_present": ["admires", "licenses", "questions", "understands", "inspects"],
        }

    def _generate_historical_ordinal(self) -> str:
        number = self._rng.randint(1, 14)
        suffix = "th" if 11 <= number <= 13 else {1: "st", 2: "nd", 3: "rd"}.get(number % 10, "th")
        return f"{number}{suffix}"

    def _build_proper_noun(self) -> str:
        title, first, last = (self._rng.choice(self._grammar[key]) for key in ("name_title", "name_first", "name_last"))
        if self._rng.random() < .15:
            first = f"{first} 'The {self._rng.choice(self._grammar['pejorative'])}'"
        surname = last
        if self._rng.random() < .30:
            other = self._rng.choice(self._grammar["name_last"])
            while other == last:
                other = self._rng.choice(self._grammar["name_last"])
            surname = f"{last}-{other}"
        return f"{title} {first} {surname}".strip()

    def _resolve(self, token: str) -> str:
        if token == "historical_ordinal": return self._generate_historical_ordinal()
        if token == "generated_proper_noun": return self._build_proper_noun()
        if token == "enhanced_institution":
            descriptor = self._rng.choice(self._grammar["institution_descriptor"])
            base = self._rng.choice(self._grammar["institution_base"])
            return f"{descriptor} {base}".strip()
        if token == "generated_legal_action": return self._join(self._expand(self._rng.choice(self._grammar["legal_core_action"])), self._expand(self._rng.choice(self._grammar["legal_situational_pattern"])))
        if token == "generated_natural_philosophy_axiom":
            prefix = self._rng.choice(self._grammar["science_prefix"]); prop = self._rng.choice(self._grammar["science_property"])
            return self._join(prefix, prop, self._rng.choice(self._grammar["science_connector"]), self._expand(self._rng.choice(self._grammar["science_target"])), self._rng.choice(self._grammar["science_constraint"]))
        if token == "generated_academic_body":
            if self._rng.random() < .20: return self._rng.choice(self._grammar["academic_body_noun"])
            return self._join(self._rng.choice(self._grammar["academic_body_modifier"]), self._rng.choice(self._grammar["academic_body_noun"]))
        if token == "generated_logistics_action":
            if self._rng.random() < .30: return self._rng.choice(self._grammar["logistics_vector"])
            return self._join(self._rng.choice(self._grammar["logistics_tier"]), self._rng.choice(self._grammar["logistics_vector"]))
        if token == "generated_academic_discipline": return self._join(self._rng.choice(self._grammar["academic_prefix"]), self._resolve("academic_subject_structure"))
        if token == "noun_verbing": return f"{self._rng.choice(self._grammar['verbing_base_noun'])}-{self._rng.choice(self._grammar['verbing_suffix_gerund'])}"
        if token not in self._grammar: return token
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
        return re.sub(r"\b([Aa])\s+([\w-]+)", lambda m: ("An" if m.group(1) == "A" else "an") + " " + m.group(2) if cls._VOWEL_SOUND.match(m.group(2)) else m.group(0), text)

    def generate(self, slugify: bool = False) -> str:
        """Return the next generated title; optionally return a URL-safe slug."""
        phrase = self._fix_indefinite_articles(self._resolve("START"))
        phrase = " ".join(phrase.split())
        if slugify:
            phrase = re.sub(r"[^a-zA-Z0-9\s-]", "", phrase).lower()
            return "-".join(phrase.split())
        return phrase
