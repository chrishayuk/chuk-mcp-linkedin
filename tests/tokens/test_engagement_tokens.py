"""
Tests for EngagementTokens design tokens.
"""

from chuk_mcp_linkedin.tokens.engagement_tokens import EngagementTokens


class TestHookTypes:
    """Test hook type tokens"""

    def test_all_hook_types_exist(self):
        """Test all hook types are defined"""
        expected_hooks = ["question", "stat", "story", "controversy", "list", "curiosity"]
        for hook_type in expected_hooks:
            assert hook_type in EngagementTokens.HOOKS

    def test_hook_has_required_fields(self):
        """Test each hook has required fields"""
        required_fields = ["power", "examples", "best_for", "templates"]
        for hook_type, hook_data in EngagementTokens.HOOKS.items():
            for field in required_fields:
                assert field in hook_data, f"{hook_type} missing {field}"

    def test_hook_power_ratings(self):
        """Test hook power ratings are valid"""
        for hook_type, hook_data in EngagementTokens.HOOKS.items():
            power = hook_data["power"]
            assert 0 <= power <= 1, f"{hook_type} power {power} not in 0-1 range"

    def test_hook_power_order(self):
        """Test hook power ratings are in expected order"""
        # Controversy should be highest
        assert EngagementTokens.HOOKS["controversy"]["power"] == 0.95
        # Stat should be high
        assert EngagementTokens.HOOKS["stat"]["power"] == 0.9
        # Story should be high
        assert EngagementTokens.HOOKS["story"]["power"] == 0.85

    def test_hook_examples_not_empty(self):
        """Test each hook type has examples"""
        for hook_type, hook_data in EngagementTokens.HOOKS.items():
            assert len(hook_data["examples"]) > 0, f"{hook_type} has no examples"

    def test_hook_templates_not_empty(self):
        """Test each hook type has templates"""
        for hook_type, hook_data in EngagementTokens.HOOKS.items():
            assert len(hook_data["templates"]) > 0, f"{hook_type} has no templates"

    def test_get_hook_power(self):
        """Test get_hook_power method"""
        assert EngagementTokens.get_hook_power("controversy") == 0.95
        assert EngagementTokens.get_hook_power("stat") == 0.9
        assert EngagementTokens.get_hook_power("story") == 0.85

    def test_get_hook_power_invalid(self):
        """Test get_hook_power with invalid type returns default"""
        power = EngagementTokens.get_hook_power("invalid")
        assert power == 0.5  # Default value

    def test_get_hook_examples(self):
        """Test get_hook_examples method"""
        examples = EngagementTokens.get_hook_examples("stat")
        assert len(examples) > 0
        assert isinstance(examples, list)

    def test_get_hook_examples_invalid(self):
        """Test get_hook_examples with invalid type returns empty list"""
        examples = EngagementTokens.get_hook_examples("invalid")
        assert examples == []


class TestCTAStyles:
    """Test CTA style tokens"""

    def test_all_cta_types_exist(self):
        """Test all CTA types are defined"""
        expected_ctas = ["direct", "curiosity", "action", "share", "poll", "soft"]
        for cta_type in expected_ctas:
            assert cta_type in EngagementTokens.CTA_STYLES

    def test_cta_has_required_fields(self):
        """Test each CTA has required fields"""
        required_fields = ["examples", "best_for", "power", "templates"]
        for cta_type, cta_data in EngagementTokens.CTA_STYLES.items():
            for field in required_fields:
                assert field in cta_data, f"{cta_type} missing {field}"

    def test_cta_power_ratings(self):
        """Test CTA power ratings are valid"""
        for cta_type, cta_data in EngagementTokens.CTA_STYLES.items():
            power = cta_data["power"]
            assert 0 <= power <= 1, f"{cta_type} power {power} not in 0-1 range"

    def test_cta_power_order(self):
        """Test CTA power ratings match expected hierarchy"""
        # Poll and Share should be highest
        assert EngagementTokens.CTA_STYLES["poll"]["power"] == 0.95
        assert EngagementTokens.CTA_STYLES["share"]["power"] == 0.9
        # Curiosity should be high
        assert EngagementTokens.CTA_STYLES["curiosity"]["power"] == 0.85

    def test_get_cta_power(self):
        """Test get_cta_power method"""
        assert EngagementTokens.get_cta_power("poll") == 0.95
        assert EngagementTokens.get_cta_power("share") == 0.9
        assert EngagementTokens.get_cta_power("curiosity") == 0.85

    def test_get_cta_power_invalid(self):
        """Test get_cta_power with invalid type returns default"""
        power = EngagementTokens.get_cta_power("invalid")
        assert power == 0.5

    def test_get_cta_examples(self):
        """Test get_cta_examples method"""
        examples = EngagementTokens.get_cta_examples("curiosity")
        assert len(examples) > 0
        assert isinstance(examples, list)


class TestFirstHourTargets:
    """Test first hour engagement targets"""

    def test_first_hour_targets_exist(self):
        """Test all first hour targets are defined"""
        expected_targets = ["minimum", "good", "great", "viral"]
        for target in expected_targets:
            assert target in EngagementTokens.FIRST_HOUR_TARGETS

    def test_first_hour_progression(self):
        """Test first hour targets increase in order"""
        targets = EngagementTokens.FIRST_HOUR_TARGETS
        assert targets["minimum"] < targets["good"]
        assert targets["good"] < targets["great"]
        assert targets["great"] < targets["viral"]

    def test_first_hour_values(self):
        """Test first hour target values"""
        assert EngagementTokens.FIRST_HOUR_TARGETS["minimum"] == 10
        assert EngagementTokens.FIRST_HOUR_TARGETS["good"] == 50
        assert EngagementTokens.FIRST_HOUR_TARGETS["great"] == 100
        assert EngagementTokens.FIRST_HOUR_TARGETS["viral"] == 200


class TestCommentResponse:
    """Test comment response strategy tokens"""

    def test_comment_response_timing_exists(self):
        """Test comment response timing is defined"""
        assert "timing" in EngagementTokens.COMMENT_RESPONSE
        timing = EngagementTokens.COMMENT_RESPONSE["timing"]
        assert "critical_window" in timing
        assert "recommended" in timing
        assert "maximum" in timing

    def test_comment_response_timing_progression(self):
        """Test timing windows make sense"""
        timing = EngagementTokens.COMMENT_RESPONSE["timing"]
        assert timing["recommended"] < timing["critical_window"]
        assert timing["critical_window"] < timing["maximum"]

    def test_comment_response_depth_levels(self):
        """Test depth levels are defined"""
        depth = EngagementTokens.COMMENT_RESPONSE["depth"]
        expected_levels = ["minimal", "standard", "meaningful", "deep"]
        for level in expected_levels:
            assert level in depth
            assert len(depth[level]) > 0

    def test_comment_response_best_practices(self):
        """Test best practices are defined"""
        practices = EngagementTokens.COMMENT_RESPONSE["best_practices"]
        assert len(practices) > 0
        assert isinstance(practices, list)


class TestTimingOptimization:
    """Test timing optimization tokens"""

    def test_best_days_exist(self):
        """Test best posting days are defined"""
        best_days = EngagementTokens.TIMING["best_days"]
        assert len(best_days) > 0
        assert "tuesday" in best_days
        assert "wednesday" in best_days
        assert "thursday" in best_days

    def test_worst_days_exist(self):
        """Test worst posting days are defined"""
        worst_days = EngagementTokens.TIMING["worst_days"]
        assert len(worst_days) > 0
        assert "saturday" in worst_days
        assert "sunday" in worst_days

    def test_best_hours_exist(self):
        """Test best posting hours are defined"""
        best_hours = EngagementTokens.TIMING["best_hours"]
        expected_periods = ["morning", "lunch", "evening"]
        for period in expected_periods:
            assert period in best_hours
            start, end = best_hours[period]
            assert 0 <= start < 24
            assert 0 <= end <= 24
            assert start < end

    def test_posting_frequency(self):
        """Test posting frequency guidelines"""
        frequency = EngagementTokens.TIMING["posting_frequency"]
        assert frequency["minimum"] == 3
        assert frequency["optimal"] == (4, 5)
        assert frequency["maximum"] == 7
        assert frequency["over_limit"] == 10

    def test_is_optimal_posting_time(self):
        """Test is_optimal_posting_time method"""
        # Tuesday at 8 AM should be optimal
        assert EngagementTokens.is_optimal_posting_time("tuesday", 8)

        # Tuesday at 1 PM should be optimal (lunch)
        assert EngagementTokens.is_optimal_posting_time("tuesday", 13)

        # Saturday at any time should not be optimal
        assert not EngagementTokens.is_optimal_posting_time("saturday", 8)

        # Tuesday at 3 AM should not be optimal
        assert not EngagementTokens.is_optimal_posting_time("tuesday", 3)

    def test_is_optimal_posting_time_case_insensitive(self):
        """Test day names are case-insensitive"""
        assert EngagementTokens.is_optimal_posting_time("Tuesday", 8)
        assert EngagementTokens.is_optimal_posting_time("TUESDAY", 8)


class TestFormattingTokens:
    """Test formatting tokens"""

    def test_bold_usage_levels(self):
        """Test bold usage levels are defined"""
        bold = EngagementTokens.FORMATTING["bold_usage"]
        expected_levels = ["none", "key_phrases", "emphasis", "heavy"]
        for level in expected_levels:
            assert level in bold
            assert 0 <= bold[level] <= 1

    def test_bold_usage_progression(self):
        """Test bold usage increases"""
        bold = EngagementTokens.FORMATTING["bold_usage"]
        assert bold["none"] < bold["key_phrases"]
        assert bold["key_phrases"] < bold["emphasis"]
        assert bold["emphasis"] < bold["heavy"]

    def test_white_space_ratios(self):
        """Test white space ratio levels"""
        ws = EngagementTokens.FORMATTING["white_space_ratio"]
        expected_levels = ["dense", "balanced", "airy"]
        for level in expected_levels:
            assert level in ws
            assert 0 <= ws[level] <= 1

    def test_white_space_progression(self):
        """Test white space increases"""
        ws = EngagementTokens.FORMATTING["white_space_ratio"]
        assert ws["dense"] < ws["balanced"]
        assert ws["balanced"] < ws["airy"]


class TestIntegration:
    """Integration tests for engagement tokens"""

    def test_all_power_ratings_reasonable(self):
        """Test all power ratings are reasonable"""
        # Collect all power ratings
        hook_powers = [h["power"] for h in EngagementTokens.HOOKS.values()]
        cta_powers = [c["power"] for c in EngagementTokens.CTA_STYLES.values()]

        all_powers = hook_powers + cta_powers

        # All should be between 0 and 1
        for power in all_powers:
            assert 0 <= power <= 1

        # Should have some variation
        assert len(set(all_powers)) > 1

    def test_controversy_is_highest_hook(self):
        """Test controversy hook has highest power"""
        max_power = max(h["power"] for h in EngagementTokens.HOOKS.values())
        assert EngagementTokens.HOOKS["controversy"]["power"] == max_power

    def test_poll_cta_is_highest(self):
        """Test poll CTA has highest or tied-highest power"""
        max_power = max(c["power"] for c in EngagementTokens.CTA_STYLES.values())
        assert EngagementTokens.CTA_STYLES["poll"]["power"] == max_power


class TestEdgeCases:
    """Test edge cases"""

    def test_invalid_hook_type_graceful(self):
        """Test invalid hook type returns default value"""
        power = EngagementTokens.get_hook_power("nonexistent")
        assert power == 0.5

    def test_invalid_cta_type_graceful(self):
        """Test invalid CTA type returns default value"""
        power = EngagementTokens.get_cta_power("nonexistent")
        assert power == 0.5

    def test_invalid_day_in_timing_check(self):
        """Test invalid day returns False"""
        assert not EngagementTokens.is_optimal_posting_time("invalidday", 8)

    def test_edge_hours_in_timing_check(self):
        """Test edge case hours"""
        # Hour 0 (midnight)
        result = EngagementTokens.is_optimal_posting_time("tuesday", 0)
        assert isinstance(result, bool)

        # Hour 23 (11 PM)
        result = EngagementTokens.is_optimal_posting_time("tuesday", 23)
        assert isinstance(result, bool)
