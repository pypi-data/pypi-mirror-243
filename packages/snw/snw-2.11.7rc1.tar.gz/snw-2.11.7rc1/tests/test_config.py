from app.routes import adapt_distribution_proportions, get_parent_formula_distribution_proportions, \
    get_client_formula_distribution_proportions
import json

config_path = 'tests/config/{}'


def get_sample_dist(config):
    if not isinstance(config, dict):
        return config

    return config.get('data', config).get('sample_dist', config)


def compare_config(expected_config, config, get_config):
    current_expected_config = get_config(expected_config)
    current_config = get_config(config)

    assert len(current_config) == len(current_expected_config)

    for index in range(len(current_config)):
        assert current_config[index] == current_expected_config[index]


def check_config_distribution_proportions(config, expect_config, client_value,
                                          formula_distribution_proportions_function, is_parent=True):
    with open(config, ) as json_file, open(expect_config, ) as expected_json_file:
        json_config = json.load(json_file)
        expected_json_config = json.load(expected_json_file)

        sample_dists = get_sample_dist(json_config)

        result_sample_dist = adapt_distribution_proportions(sample_dists,
                                                            formula_distribution_proportions_function,
                                                            client_value, is_parent=is_parent)

        compare_config(expected_json_config, result_sample_dist, get_sample_dist)


def test_parent_config_distribution_proportions():
    client_ratio = 70
    check_config_distribution_proportions(config_path.format('config_to_adapt.json'),
                                          config_path.format('expected_parent_config_after_adaptation.json'),
                                          client_ratio,
                                          get_parent_formula_distribution_proportions)


def test_client_config_distribution_proportions():
    client_weight = 3
    check_config_distribution_proportions(config_path.format('config_to_adapt.json'),
                                          config_path.format('expected_client_config_after_adaptation.json'),
                                          client_weight,
                                          get_client_formula_distribution_proportions,
                                          is_parent=False)
