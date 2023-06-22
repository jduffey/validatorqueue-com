import pytest

from build import calculate_wait_time


scaling = [0, 327680, 393216, 458752, 524288, 589824, 655360, 720896, 786432, 851968, 917504, 983040, 1048576, 1114112, 1179648, 1245184, 1310720, 1376256, 1441792, 1507328,
           1572864, 1638400, 1703936, 1769472, 1835008, 1900544, 1966080, 2031616, 2097152, 2162688, 2228224, 2293760, 2359296, 2424832, 2490368, 2555904, 2621440, 2686976, 2752512]


@pytest.mark.parametrize("validator_count, expected0, expected1, expected2, expected3, expected4", [
    [0, '0 minutes', 0.0, 9, 9, 0],
    [327680, '0 minutes', 0.0, 4, 4, 0],
    [393216, '0 minutes', 0.0, 5, 5, 0],
    [458752, '0 minutes', 0.0, 6, 6, 0],
    [524288, '0 minutes', 0.0, 7, 7, 0],
    [589824, '0 minutes', 0.0, 8, 8, 0],
])
def test_calculate_wait_time_no_queue(validator_count, expected0, expected1, expected2, expected3, expected4):
    queue_length = 0

    formatted_wait_time, waiting_time_days_raw, current_churn, ave_churn, churn_time_days = calculate_wait_time(
        validator_count, queue_length)

    assert formatted_wait_time == expected0
    assert waiting_time_days_raw == expected1
    assert current_churn == expected2
    assert ave_churn == expected3
    assert churn_time_days == expected4


@pytest.mark.parametrize("validator_count, expected0, expected1, expected2, expected3, expected4", [
    [0, '14 minutes', 0.01, 9, 4.0, 0.01],
    [327680, '13 minutes', 0.008888888888888889, 4, 5.0, 0.008888888888888889],
    [393216, '11 minutes', 0.007407407407407408, 5, 6.0, 0.007407407407407408],
    [458752, '9 minutes', 0.006354166666666667, 6, 7.0, 0.006349206349206349],
    [524288, '8 minutes', 0.005555555555555556, 7, 8.0, 0.005555555555555556],
    [589824, '7 minutes', 0.00494212962962963, 8, 9.0, 0.0049382716049382715],
])
def test_calculate_wait_time_small_queue(validator_count, expected0, expected1, expected2, expected3, expected4):
    queue_length = 10

    formatted_wait_time, waiting_time_days_raw, current_churn, ave_churn, churn_time_days = calculate_wait_time(
        validator_count, queue_length)

    assert formatted_wait_time == expected0
    assert waiting_time_days_raw == expected1
    assert current_churn == expected2
    assert ave_churn == expected3
    assert churn_time_days == expected4


@pytest.mark.parametrize("validator_count, expected0, expected1, expected2, expected3, expected4", [
    [0, '12 days, 8 hours', 12.345, 9, 4.0, 12.345],
    [327680, '10 days, 23 hours', 10.973333333333333, 4, 5.0, 10.973333333333333],
    [393216, '9 days, 3 hours', 9.144444444444444, 5, 6.0, 9.144444444444444],
    [458752, '7 days, 20 hours', 7.838090277777778, 6, 7.0, 7.838095238095238],
    [524288, '6 days, 21 hours', 6.858333333333333, 7, 8.0, 6.858333333333333],
    [589824, '6 days, 2 hours', 6.0962962962962965, 8, 9.0, 6.0962962962962965],
])
def test_calculate_wait_time_big_queue(validator_count, expected0, expected1, expected2, expected3, expected4):
    queue_length = 12345

    formatted_wait_time, waiting_time_days_raw, current_churn, ave_churn, churn_time_days = calculate_wait_time(
        validator_count, queue_length)

    assert formatted_wait_time == expected0
    assert waiting_time_days_raw == expected1
    assert current_churn == expected2
    assert ave_churn == expected3
    assert churn_time_days == expected4
