from unittest import TestCase

from chargebee_byte.parameters import generate_parameters, generate_sorting_parameters,\
    generate_date_parameters, generate_equals_parameters, generate_collection_parameters, \
    generate_comparison_parameters


class TestGenerateParameters(TestCase):
    def test_returns_list_of_all_possible_combinations_of_parameters_and_operators(self):
        ret = generate_parameters(['status', 'cancel_reason'], ['is', 'is_not', 'in', 'not_in'])

        self.assertCountEqual(ret, [
            'status[is]', 'status[is_not]',
            'status[in]', 'status[not_in]',
            'cancel_reason[is]', 'cancel_reason[is_not]',
            'cancel_reason[in]', 'cancel_reason[not_in]',
        ])


class TestGenerateSortingParameters(TestCase):
    def test_returns_list_of_parameters_with_all_possible_sorting_operators(self):
        ret = generate_sorting_parameters(['sort_by', 'banana'])

        self.assertCountEqual(ret, [
            'sort_by[asc]', 'sort_by[desc]',
            'banana[asc]', 'banana[desc]',
        ])


class TestGenerateDateParameters(TestCase):
    def test_returns_list_of_parameters_with_all_possible_date_operators(self):
        ret = generate_date_parameters(['created_at', 'activated_at'])

        self.assertCountEqual(ret, [
            'created_at[after]', 'created_at[before]',
            'created_at[on]', 'created_at[between]',
            'activated_at[after]', 'activated_at[before]',
            'activated_at[on]', 'activated_at[between]'
        ])


class TestGenerateEqualsParamaters(TestCase):
    def test_returns_list_of_parameters_with_all_possible_equals_operators(self):
        ret = generate_equals_parameters(['status', 'cancel_reason'])

        self.assertCountEqual(ret, [
            'status[is]', 'status[is_not]',
            'cancel_reason[is]', 'cancel_reason[is_not]'
        ])


class TestGenerateCollectionParameters(TestCase):
    def test_returns_list_of_parameters_with_all_possible_collection_operators(self):
        ret = generate_collection_parameters(['status', 'cancel_reason'])

        self.assertCountEqual(ret, [
            'status[in]', 'status[not_in]',
            'cancel_reason[in]', 'cancel_reason[not_in]'
        ])


class TestGenerateComparisonParameters(TestCase):
    def test_returns_list_of_parameters_with_all_possible_comparison_operators(self):
        ret = generate_comparison_parameters(['remaining_bonobos', 'remaining_bananas'])

        self.assertCountEqual(ret, [
            'remaining_bonobos[lt]', 'remaining_bonobos[lte]',
            'remaining_bonobos[gt]', 'remaining_bonobos[gte]',
            'remaining_bananas[lt]', 'remaining_bananas[lte]',
            'remaining_bananas[gt]', 'remaining_bananas[gte]',
        ])
