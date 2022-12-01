from pytest import raises
from CpmCalculationService import CpmCalculationService


def test_activities_len_is_shorter():
    with raises(ValueError):
        # GIVEN
        activities = ['A', 'B', 'C', 'D', 'E', 'F', 'G']
        durations = [7, 9, 3, 8, 5, 4, 2, 1]
        predecessors = ['', 'A', 'A', 'B', 'C', 'C', 'DEF', 'G']
        calculation_service = CpmCalculationService()
        # THEN
        calculation_service.calculate(activities, durations, predecessors)

def test_durations_len_is_shorter():
    with raises(ValueError):
        # GIVEN
        activities = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H']
        durations = [7, 9, 3, 8, 5, 4, 2]
        predecessors = ['', 'A', 'A', 'B', 'C', 'C', 'DEF', 'G']
        calculation_service = CpmCalculationService()
        # THEN
        calculation_service.calculate(activities, durations, predecessors)

def test_predecessors_len_is_shorter():
    with raises(ValueError):
        # GIVEN
        activities = ['A', 'B', 'C', 'D', 'E', 'F', 'G']
        durations = [7, 9, 3, 8, 5, 4, 2, 1]
        predecessors = ['', 'A', 'A', 'B', 'C', 'C', 'DEF']
        calculation_service = CpmCalculationService()
        # THEN
        calculation_service.calculate(activities, durations, predecessors)
