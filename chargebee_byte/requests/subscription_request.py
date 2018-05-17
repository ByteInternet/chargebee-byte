from parameters import generate_sorting_parameters, generate_equals_parameters, generate_comparison_parameters, \
    generate_collection_parameters, generate_date_parameters, generate_parameters


class SubscriptionRequest(object):
    path = '/subscriptions'

    def __init__(self, parameters=None):
        parameters = parameters or {}

        self.allowed_parameters = self._generate_allowed_parameters()
        self._check_parameters(parameters)
        self.data = parameters

    def _generate_allowed_parameters(self):
        sorting_params = generate_sorting_parameters(['sort_by'])
        equals_params = generate_equals_parameters(['status', 'cancel_reason', 'id', 'customer_id', 'plan_id', 'remaining_billing_cycles'])
        collection_params = generate_collection_parameters(['status', 'cancel_reason', 'id', 'customer_id', 'plan_id'])
        comparison_params = generate_comparison_parameters(['remaining_billing_cycles'])
        date_params = generate_date_parameters(['created_at', 'activated_at', 'next_billing_at', 'cancelled_at', 'updated_at'])

        custom_params = generate_parameters(['has_scheduled_changes'], ['is'])
        custom_params += generate_parameters(['remaining_billing_cycles'], ['between'])
        custom_params += generate_parameters(['remaining_billing_cycles', 'activated_at', 'cancel_reason'], ['is_present'])
        custom_params += generate_parameters(['id', 'customer_id', 'plan_id'], ['starts_with'])

        return ['limit', 'offset', 'include_deleted'] + sorting_params + equals_params + collection_params + \
            comparison_params + date_params + custom_params

    def _check_parameters(self, parameters):
        parameter_keys = set(parameters.keys())
        correct_parameters = parameter_keys.intersection(self.allowed_parameters)
        incorrect_parameters = parameter_keys.symmetric_difference(correct_parameters)

        if incorrect_parameters:
            raise ValueError('The following parameters are not allowed: {}'.format(', '.join(incorrect_parameters)))
