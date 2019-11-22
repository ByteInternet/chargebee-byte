from unittest.mock import Mock, patch

from chargebee_byte.requests import ChargebeeRequest
from tests.test import TestBase


class TestChargebeeRequest(TestBase):
    @patch('chargebee_byte.requests.ChargebeeRequest.generate_allowed_parameters')
    def test_path_is_none_by_default(self, _):
        self.assertIsNone(ChargebeeRequest().path)

    def test_generate_allowed_parameters_raises_not_implemented_error(self):
        with self.assertRaises(NotImplementedError):
            ChargebeeRequest.generate_allowed_parameters(Mock())

    @patch('chargebee_byte.requests.ChargebeeRequest.generate_allowed_parameters')
    def test_raises_value_error_with_message_specifying_invalid_parameters(self, generate_allowed_parameters):
        generate_allowed_parameters.return_value = ['sort_by[asc]']
        parameters = {'not_allowed': 'something', 'also_not_allowed': 'something',
                      'sort_by[asc]': 'something'}

        try:
            ChargebeeRequest(parameters)
        except ValueError as e:
            self.assertTrue(str(e).startswith('The following parameters are not allowed: '))
            self.assertTrue(str(e).endswith(('not_allowed, also_not_allowed',
                                             'also_not_allowed, not_allowed')))
        else:
            self.fail('Exception not raised')

    @patch('chargebee_byte.requests.ChargebeeRequest.generate_allowed_parameters')
    def test_does_not_raise_value_error_if_valid_parameters_supplied(self, generate_allowed_parameters):
        generate_allowed_parameters.return_value = ['sort_by[asc]', 'sort_by[desc]']
        parameters = {'sort_by[asc]': 'something', 'sort_by[desc]': 'something'}

        # Should not raise error
        ChargebeeRequest(parameters)

    @patch('chargebee_byte.requests.ChargebeeRequest.generate_allowed_parameters')
    def test_sets_data_to_parameters(self, generate_allowed_parameters):
        generate_allowed_parameters.return_value = ['sort_by[asc]', 'updated_at[on]']
        parameters = {'sort_by[asc]': 'created_at', 'updated_at[on]': 'something'}

        request = ChargebeeRequest(parameters)

        self.assertEqual(request.data, parameters)

    @patch('chargebee_byte.requests.ChargebeeRequest.generate_allowed_parameters')
    def test_sets_data_to_empty_dict_if_no_parameters(self, _):
        self.assertEqual(ChargebeeRequest().data, {})
