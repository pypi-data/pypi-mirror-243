import unittest
import pytest

from pandas.testing import assert_series_equal

from mcda.utils import *
from mcda.utility_functions.aggregation import Aggregation

class TestAggregation(unittest.TestCase):

    @staticmethod
    def get_normalized_input_matrix():
        input_matrix = read_matrix("tests/resources/normalization/res_minmax_no0.csv")

        return input_matrix

    @staticmethod
    def get_normalized_input_matrix_w_0():
        input_matrix = read_matrix("tests/resources/normalization/res_minmax_01.csv")

        return input_matrix

    @staticmethod
    def get_weights():
        weights_non_norm = (0.5, 0.5, 0.5, 0.5, 0.5, 0.5)
        weights = [val/sum(weights_non_norm) for val in weights_non_norm]

        return weights

    def test_init(self):
        # Given
        weights = TestAggregation.get_weights()

        # When
        agg = Aggregation(weights)

        # Then
        assert sum(agg.weights) == pytest.approx(1, 0.1)


    def test_weighted_sum(self):
        # Given
        weights = TestAggregation.get_weights()
        normalized_matrix = TestAggregation.get_normalized_input_matrix()

        # When
        expected_res = (normalized_matrix*weights).sum(axis=1)
        agg = Aggregation(weights)
        res = agg.weighted_sum(normalized_matrix)

        # Then
        assert isinstance(res, pd.Series)
        assert_series_equal(res, expected_res, check_like=True)

    def test_geometric(self):
        # Given
        weights = TestAggregation.get_weights()
        normalized_matrix = TestAggregation.get_normalized_input_matrix()
        wrong_normalized_matrix = TestAggregation.get_normalized_input_matrix_w_0()

        # When
        expected_res = (normalized_matrix**np.asarray(weights)).product(axis=1)
        agg = Aggregation(weights)
        res = agg.geometric(normalized_matrix)

        # Then
        assert isinstance(res, np.ndarray)
        assert_series_equal(pd.Series(res), expected_res, check_like=True)
        with pytest.raises(ValueError):
            agg.geometric(wrong_normalized_matrix)

    def test_harmonic(self):
        # Given
        weights = TestAggregation.get_weights()
        normalized_matrix = TestAggregation.get_normalized_input_matrix()
        wrong_normalized_matrix = TestAggregation.get_normalized_input_matrix_w_0()

        # When
        expected_res = 1/((weights/normalized_matrix).sum(axis=1))
        agg = Aggregation(weights)
        res = agg.harmonic(normalized_matrix)

        # Then
        assert isinstance(res, np.ndarray)
        assert_series_equal(pd.Series(res), expected_res, check_like=True)
        with pytest.raises(ValueError):
            agg.harmonic(wrong_normalized_matrix)

    def test_minimum(self):
        # Given
        weights = TestAggregation.get_weights()
        normalized_matrix = TestAggregation.get_normalized_input_matrix()

        # When
        expected_res = normalized_matrix.min(axis=1)
        agg = Aggregation(weights)
        res = agg.minimum(normalized_matrix)

        # Then
        assert isinstance(res, pd.Series)
        assert_series_equal(res, expected_res, check_like=True)
