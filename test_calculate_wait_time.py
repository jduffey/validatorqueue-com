import pytest

from build import calculate_wait_time


# scaling = [0, 327680, 393216, 458752, 524288, 589824, 655360, 720896, 786432, 851968, 917504, 983040, 1048576, 1114112, 1179648, 1245184, 1310720, 1376256, 1441792, 1507328,
        #    1572864, 1638400, 1703936, 1769472, 1835008, 1900544, 1966080, 2031616, 2097152, 2162688, 2228224, 2293760, 2359296, 2424832, 2490368, 2555904, 2621440, 2686976, 2752512]


@pytest.mark.parametrize("validator_count, expected0, expected1, expected2, expected3, expected4", [
    [0, '0 minutes', 0.0, 9, 9, 0],
    [1, '0 minutes', 0.0, 4, 4, 0],
    [327679, '0 minutes', 0.0, 4, 4, 0],
    [327680, '0 minutes', 0.0, 4, 4, 0],
    [327681, '0 minutes', 0.0, 5, 5, 0],
    [393215, '0 minutes', 0.0, 5, 5, 0],
    [393216, '0 minutes', 0.0, 5, 5, 0],
    [393217, '0 minutes', 0.0, 6, 6, 0],
    [458751, '0 minutes', 0.0, 6, 6, 0],
    [458752, '0 minutes', 0.0, 6, 6, 0],
    [458753, '0 minutes', 0.0, 7, 7, 0],
    [524287, '0 minutes', 0.0, 7, 7, 0],
    [524288, '0 minutes', 0.0, 7, 7, 0],
    [524289, '0 minutes', 0.0, 8, 8, 0],
    [589823, '0 minutes', 0.0, 8, 8, 0],
    [589824, '0 minutes', 0.0, 8, 8, 0],
    [589825, '0 minutes', 0.0, 9, 9, 0],
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
    [1, '14 minutes', 0.01, 4, 4.0, 0.01],
    [327679, '13 minutes', 0.00900462962962963, 4, 4.9, 0.009000000000000001],
    [327680, '13 minutes', 0.008888888888888889, 4, 5.0, 0.008888888888888889],
    [327681, '13 minutes', 0.008888888888888889, 5, 5.0, 0.008888888888888889],
    [393215, '11 minutes', 0.00755787037037037, 5, 5.9, 0.007555555555555556],
    [393216, '11 minutes', 0.007407407407407408, 5, 6.0, 0.007407407407407408],
    [393217, '11 minutes', 0.007407407407407408, 6, 6.0, 0.007407407407407408],
    [458751, '9 minutes', 0.006458333333333333, 6, 6.9, 0.006455026455026455],
    [458752, '9 minutes', 0.006354166666666667, 6, 7.0, 0.006349206349206349],
    [458753, '9 minutes', 0.006354166666666667, 7, 7.0, 0.006349206349206349],
    [524287, '8 minutes', 0.005636574074074074, 7, 7.9, 0.005634920634920635],
    [524288, '8 minutes', 0.005555555555555556, 7, 8.0, 0.005555555555555556],
    [524289, '8 minutes', 0.005555555555555556, 8, 8.0, 0.005555555555555556],
    [589823, '7 minutes', 0.005, 8, 8.9, 0.005],
    [589824, '7 minutes', 0.00494212962962963, 8, 9.0, 0.0049382716049382715],
    [589825, '7 minutes', 0.00494212962962963, 9, 9.0, 0.0049382716049382715],
])
def test_calculate_wait_time_small_queue(validator_count, expected0, expected1, expected2, expected3, expected4):
    queue_length = 10

    formatted_wait_time, waiting_time_days_raw, current_churn, ave_churn, churn_time_days = calculate_wait_time(
        validator_count, queue_length)
    print(validator_count, calculate_wait_time(validator_count, queue_length))

    assert formatted_wait_time == expected0
    assert waiting_time_days_raw == expected1
    assert current_churn == expected2
    assert ave_churn == expected3
    assert churn_time_days == expected4


@pytest.mark.parametrize("validator_count, expected0, expected1, expected2, expected3, expected4", [
    [0, '12 days, 8 hours', 12.345, 9, 4.0, 12.345],
    [1, '12 days, 8 hours', 12.345, 4, 4.0, 12.345],
    [327679, '10 days, 23 hours', 10.973449074074074, 4, 5.0, 10.973444444444445],
    [327680, '10 days, 23 hours', 10.973333333333333, 4, 5.0, 10.973333333333333],
    [327681, '10 days, 23 hours', 10.973333333333333, 5, 5.0, 10.973333333333333],
    [393215, '9 days, 3 hours', 9.144594907407408, 5, 6.0, 9.144592592592593],
    [393216, '9 days, 3 hours', 9.144444444444444, 5, 6.0, 9.144444444444444],
    [393217, '9 days, 3 hours', 9.144444444444444, 6, 6.0, 9.144444444444444],
    [458751, '7 days, 20 hours', 7.838206018518519, 6, 7.0, 7.838201058201059],
    [458752, '7 days, 20 hours', 7.838090277777778, 6, 7.0, 7.838095238095238],
    [458753, '7 days, 20 hours', 7.838090277777778, 7, 7.0, 7.838095238095238],
    [524287, '6 days, 21 hours', 6.858414351851851, 7, 8.0, 6.858412698412699],
    [524288, '6 days, 21 hours', 6.858333333333333, 7, 8.0, 6.858333333333333],
    [524289, '6 days, 21 hours', 6.858333333333333, 8, 8.0, 6.858333333333333],
    [589823, '6 days, 2 hours', 6.096354166666667, 8, 9.0, 6.096358024691358],
    [589824, '6 days, 2 hours', 6.0962962962962965, 8, 9.0, 6.0962962962962965],
    [589825, '6 days, 2 hours', 6.0962962962962965, 9, 9.0, 6.0962962962962965],
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
