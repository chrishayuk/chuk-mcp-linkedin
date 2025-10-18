"""
Tests for TextTokens design tokens.
"""

from chuk_mcp_linkedin.tokens.text_tokens import TextTokens


class TestTextTokensConstants:
    """Test TextTokens constant values"""

    def test_max_length(self):
        """Test LinkedIn maximum post length"""
        assert TextTokens.MAX_LENGTH == 3000

    def test_truncation_point(self):
        """Test 'see more' truncation point"""
        assert TextTokens.TRUNCATION_POINT == 210

    def test_ideal_length_ranges(self):
        """Test ideal length ranges exist for all types"""
        expected_types = ["micro", "short", "medium", "long", "story"]
        for length_type in expected_types:
            assert length_type in TextTokens.IDEAL_LENGTH
            min_len, max_len = TextTokens.IDEAL_LENGTH[length_type]
            assert min_len < max_len
            assert min_len > 0

    def test_line_break_styles(self):
        """Test line break style values"""
        expected_styles = ["dense", "readable", "scannable", "dramatic", "extreme"]
        for style in expected_styles:
            assert style in TextTokens.LINE_BREAKS
            assert TextTokens.LINE_BREAKS[style] > 0

    def test_line_break_progression(self):
        """Test line breaks increase in order"""
        assert TextTokens.LINE_BREAKS["dense"] < TextTokens.LINE_BREAKS["readable"]
        assert TextTokens.LINE_BREAKS["readable"] < TextTokens.LINE_BREAKS["scannable"]
        assert TextTokens.LINE_BREAKS["scannable"] < TextTokens.LINE_BREAKS["dramatic"]
        assert TextTokens.LINE_BREAKS["dramatic"] < TextTokens.LINE_BREAKS["extreme"]


class TestEmojiTokens:
    """Test emoji usage tokens"""

    def test_emoji_levels_exist(self):
        """Test all emoji levels are defined"""
        expected_levels = ["none", "minimal", "moderate", "expressive", "heavy"]
        for level in expected_levels:
            assert level in TextTokens.EMOJI
            assert TextTokens.EMOJI[level] >= 0

    def test_emoji_progression(self):
        """Test emoji levels increase in order"""
        assert TextTokens.EMOJI["none"] < TextTokens.EMOJI["minimal"]
        assert TextTokens.EMOJI["minimal"] < TextTokens.EMOJI["moderate"]
        assert TextTokens.EMOJI["moderate"] < TextTokens.EMOJI["expressive"]
        assert TextTokens.EMOJI["expressive"] < TextTokens.EMOJI["heavy"]

    def test_calculate_emoji_count(self):
        """Test emoji count calculation"""
        word_count = 100

        # None level should return 0
        assert TextTokens.calculate_emoji_count(word_count, "none") == 0

        # Minimal (0.01) should return 1
        assert TextTokens.calculate_emoji_count(word_count, "minimal") == 1

        # Moderate (0.05) should return 5
        assert TextTokens.calculate_emoji_count(word_count, "moderate") == 5

        # Expressive (0.1) should return 10
        assert TextTokens.calculate_emoji_count(word_count, "expressive") == 10

    def test_calculate_emoji_count_scales(self):
        """Test emoji count scales with word count"""
        # 50 words with moderate (0.05) = 2.5 = 2 emojis
        assert TextTokens.calculate_emoji_count(50, "moderate") == 2

        # 200 words with moderate (0.05) = 10 emojis
        assert TextTokens.calculate_emoji_count(200, "moderate") == 10


class TestHashtagTokens:
    """Test hashtag strategy tokens"""

    def test_hashtag_counts_exist(self):
        """Test hashtag count ranges are defined"""
        expected_strategies = ["minimal", "optimal", "maximum", "over_limit"]
        for strategy in expected_strategies:
            assert strategy in TextTokens.HASHTAGS["count"]

    def test_optimal_hashtag_count(self):
        """Test optimal hashtag count is 3-5"""
        min_tags, max_tags = TextTokens.HASHTAGS["count"]["optimal"]
        assert min_tags == 3
        assert max_tags == 5

    def test_hashtag_placements(self):
        """Test hashtag placement options exist"""
        expected_placements = ["inline", "mid", "end", "first_comment"]
        for placement in expected_placements:
            assert placement in TextTokens.HASHTAGS["placement"]

    def test_hashtag_strategies(self):
        """Test hashtag strategies are defined"""
        expected_strategies = ["branded", "trending", "niche", "mixed"]
        for strategy in expected_strategies:
            assert strategy in TextTokens.HASHTAGS["strategy"]

    def test_get_hashtag_count(self):
        """Test get_hashtag_count method"""
        min_tags, max_tags = TextTokens.get_hashtag_count("optimal")
        assert min_tags == 3
        assert max_tags == 5

        # Test default to optimal
        min_tags, max_tags = TextTokens.get_hashtag_count("invalid_strategy")
        assert min_tags == 3
        assert max_tags == 5


class TestVisualElements:
    """Test visual element tokens"""

    def test_symbols_exist(self):
        """Test visual symbols are defined"""
        expected_symbols = [
            "arrow",
            "bullet",
            "checkmark",
            "cross",
            "lightning",
            "bulb",
            "target",
            "pin",
        ]
        for symbol in expected_symbols:
            assert symbol in TextTokens.SYMBOLS
            assert len(TextTokens.SYMBOLS[symbol]) > 0

    def test_separators_exist(self):
        """Test separator styles are defined"""
        expected_separators = ["line", "dots", "wave", "heavy"]
        for separator in expected_separators:
            assert separator in TextTokens.SEPARATORS
            assert len(TextTokens.SEPARATORS[separator]) > 0


class TestTextTokensMethods:
    """Test TextTokens class methods"""

    def test_get_length_range(self):
        """Test get_length_range method"""
        min_len, max_len = TextTokens.get_length_range("medium")
        assert min_len == 300
        assert max_len == 800

    def test_get_length_range_invalid(self):
        """Test get_length_range with invalid type defaults to medium"""
        min_len, max_len = TextTokens.get_length_range("invalid")
        assert min_len == 300
        assert max_len == 800

    def test_get_line_break_count(self):
        """Test get_line_break_count method"""
        assert TextTokens.get_line_break_count("scannable") == 3
        assert TextTokens.get_line_break_count("readable") == 2
        assert TextTokens.get_line_break_count("dense") == 1

    def test_get_line_break_count_invalid(self):
        """Test get_line_break_count with invalid style defaults to 2"""
        assert TextTokens.get_line_break_count("invalid") == 2


class TestParagraphLength:
    """Test paragraph length tokens"""

    def test_paragraph_lengths_exist(self):
        """Test paragraph length ranges are defined"""
        expected_lengths = ["tight", "standard", "loose"]
        for length in expected_lengths:
            assert length in TextTokens.PARAGRAPH_LENGTH
            min_sentences, max_sentences = TextTokens.PARAGRAPH_LENGTH[length]
            assert min_sentences < max_sentences

    def test_paragraph_length_progression(self):
        """Test paragraph lengths increase"""
        tight = TextTokens.PARAGRAPH_LENGTH["tight"]
        standard = TextTokens.PARAGRAPH_LENGTH["standard"]
        loose = TextTokens.PARAGRAPH_LENGTH["loose"]

        assert tight[1] < standard[1]
        assert standard[1] < loose[1]


class TestEdgeCases:
    """Test edge cases and validation"""

    def test_emoji_count_zero_words(self):
        """Test emoji count with zero words"""
        assert TextTokens.calculate_emoji_count(0, "moderate") == 0

    def test_emoji_count_large_number(self):
        """Test emoji count with very large word count"""
        result = TextTokens.calculate_emoji_count(10000, "minimal")
        assert result == 100  # 10000 * 0.01 = 100

    def test_all_ideal_lengths_valid(self):
        """Test all ideal length ranges are valid"""
        for length_type, (min_len, max_len) in TextTokens.IDEAL_LENGTH.items():
            assert min_len < max_len, f"{length_type} min >= max"
            assert min_len > 0, f"{length_type} min <= 0"
            assert max_len <= TextTokens.MAX_LENGTH, f"{length_type} exceeds max"

    def test_truncation_point_reasonable(self):
        """Test truncation point is reasonable"""
        assert TextTokens.TRUNCATION_POINT < TextTokens.MAX_LENGTH
        assert TextTokens.TRUNCATION_POINT > 100  # Should be meaningful preview
