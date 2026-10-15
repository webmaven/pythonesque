"""Integration tests for modular template components."""

from pythonesque import UnifiedFoundationalGenerator


class TestModularTemplates:
    """Tests for modular template components that compose larger templates."""

    def test_historical_competition_full_chain(self):
        """Test full historical competition template chain."""
        gen = UnifiedFoundationalGenerator("hist-comp-test")

        # The full template uses prefix + middle + suffix
        template = "{{historical_competition_prefix}} {{historical_competition_middle}} {{historical_competition_suffix}}"
        result = gen._expand(template)

        assert "{{" not in result
        assert "}}" not in result
        assert len(result) > 10

    def test_legal_template_full_chain(self):
        """Test full legal template chain."""
        gen = UnifiedFoundationalGenerator("legal-chain-test")

        # Legal template: authority + location + framework, action is prohibition
        template = "{{legal_authority}} {{legal_location}} {{legal_framework}}, {{generated_legal_action}} is {{prohibition}}"
        result = gen._expand(template)

        assert "{{" not in result
        assert "}}" not in result
        assert "is" in result
        assert any(
            p in result
            for p in [
                "Forbidden",
                "Prohibited by Law",
                "Subject to Heavy Taxation",
                "Deemed Entirely Too Silly",
            ]
        )

    def test_legal_template_by_order(self):
        """Test 'By Order of' legal template."""
        gen = UnifiedFoundationalGenerator("legal-order-test")

        template = "By Order of {{bureaucratic_rank}} {{enhanced_institution}}, {{generated_legal_action}} shall be {{adverb}} {{prohibition}}"
        result = gen._expand(template)

        assert "{{" not in result
        assert "}}" not in result
        assert "By Order of" in result

    def test_legal_template_according_to(self):
        """Test 'According to' legal template."""
        gen = UnifiedFoundationalGenerator("legal-according-test")

        template = "According to {{legal_statute}} of {{geography_sing}}, No {{generated_legal_action}} permitted"
        result = gen._expand(template)

        assert "{{" not in result
        assert "}}" not in result
        assert "According to" in result

    def test_academic_template_chair(self):
        """Test academic position template - Chair of."""
        gen = UnifiedFoundationalGenerator("academic-chair-test")

        template = (
            "{{academic_title}} of {{generated_academic_discipline}} {{institution_affiliation}}"
        )
        result = gen._expand(template)

        assert "{{" not in result
        assert "}}" not in result

    def test_academic_template_lead_researcher(self):
        """Test academic position template - Lead Researcher."""
        gen = UnifiedFoundationalGenerator("academic-lead-test")

        template = "Lead Researcher in {{generated_academic_discipline}} at the {{enhanced_institution}} of {{geography_sing}}"
        result = gen._expand(template)

        assert "{{" not in result
        assert "}}" not in result
        assert "Lead Researcher in" in result

    def test_academic_template_director(self):
        """Test academic position template - Director of Studies."""
        gen = UnifiedFoundationalGenerator("academic-director-test")

        template = (
            "Director of Studies for {{generated_academic_discipline}} within {{geography_sing}}"
        )
        result = gen._expand(template)

        assert "{{" not in result
        assert "}}" not in result
        assert "Director of Studies for" in result

    def test_sports_template_semifinals(self):
        """Test sports competition template."""
        gen = UnifiedFoundationalGenerator("sports-test")

        template = "{{historical_ordinal}} {{sports_event}} of the {{optional_nationality}} {{generated_academic_discipline}}"
        result = gen._expand(template)

        assert "{{" not in result
        assert "}}" not in result

    def test_sports_template_tournament(self):
        """Test sports tournament template."""
        gen = UnifiedFoundationalGenerator("sports-tourney-test")

        template = "The {{optional_nationality}} {{generated_academic_discipline}} {{sports_clash}} Tournament"
        result = gen._expand(template)

        assert "{{" not in result
        assert "}}" not in result
        assert "Tournament" in result

    def test_sports_template_championship(self):
        """Test sports championship template."""
        gen = UnifiedFoundationalGenerator("sports-champ-test")

        template = "{{historical_ordinal}} Annual {{generated_academic_discipline}} {{sports_clash}} Championship"
        result = gen._expand(template)

        assert "{{" not in result
        assert "}}" not in result
        assert "Championship" in result

    def test_absurdist_templates_resolve(self):
        """Test new Monty Python-inspired absurdist templates."""
        gen = UnifiedFoundationalGenerator("absurdist-test")

        # Test a sampling of absurdist grammar categories
        absurdist_keys = [
            "silly_occupation",
            "pointless_pursuit",
            "absurd_profession",
            "ridiculous_workers",
            "useless_studies",
            "absurd_product",
            "pointless_service",
            "absurd_commodity",
            "pointless_activity",
            "ridiculous_goods",
            "absurd_form_name",
            "pointless_permit",
            "absurd_activity",
            "ridiculous_action",
            "useless_achievement",
            "absurd_entertainment",
            "pointless_celebrity",
            "absurd_talent",
            "ridiculous_production",
            "absurd_performance",
            "pointless_spectacle",
            "pointless_theory",
            "absurd_academic_topic",
            "ridiculous_research",
            "absurd_college",
            "pointless_philosophy",
            "absurd_vehicle",
            "pointless_journey",
            "ridiculous_transport",
            "absurd_navigation",
            "pointless_routing",
        ]

        for key in absurdist_keys:
            for template in gen._grammar[key]:
                result = gen._expand(template)
                assert "{{" not in result, f"Absurdist {key} unresolved: {template}"
                assert len(result) > 0


class TestGrammarInterdependencies:
    """Tests for interdependencies between grammar categories."""

    def test_enhanced_institution_uses_descriptor_and_base(self):
        gen = UnifiedFoundationalGenerator("inst-test")
        result = gen._resolve("enhanced_institution")
        # Should combine descriptor + base
        bases = gen._grammar["institution_base"]
        # At least one word from each should appear (or descriptor could be empty)
        words = result.split()
        assert len(words) >= 1
        # Base should always be present
        assert any(base in result for base in bases)

    def test_generated_academic_body_structure(self):
        gen = UnifiedFoundationalGenerator("acad-body-test")
        results = [gen._resolve("generated_academic_body") for _ in range(50)]

        # 20% chance of just noun, 80% modifier + noun
        nouns = gen._grammar["academic_body_noun"]

        for result in results:
            assert "{{" not in result
            # Should end with a noun
            assert any(result.endswith(noun) or result == noun for noun in nouns)

    def test_generated_logistics_action_structure(self):
        gen = UnifiedFoundationalGenerator("logistics-test")
        results = [gen._resolve("generated_logistics_action") for _ in range(50)]

        vectors = gen._grammar["logistics_vector"]

        for result in results:
            assert "{{" not in result
            # Should contain a vector
            assert any(vector in result for vector in vectors)

    def test_generated_academic_discipline_structure(self):
        gen = UnifiedFoundationalGenerator("acad-disc-test")
        result = gen._resolve("generated_academic_discipline")

        assert "{{" not in result
        # Should have prefix + subject structure
        # At least one prefix word should be present (or empty string)
        words = result.split()
        assert len(words) >= 1
