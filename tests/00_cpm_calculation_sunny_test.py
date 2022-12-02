from unittest.mock import patch
from CpmCalculationService import CpmCalculationService


def test_zad1():
    with patch('matplotlib.pyplot.savefig'):
        # GIVEN
        activities = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H']
        durations = [7, 9, 3, 8, 5, 4, 2, 1]
        predecessors = ['', 'A', 'A', 'B', 'C', 'C', 'DEF', 'G']
        expected_value = ['Edges:', 'A->B', 'A->C', 'B->D', 'C->E', 'C->F', 'D->G', 'E->G', 'F->G', 'G->H',
                          'self.successors:', 'BC', 'D', 'EF', 'G', 'G', 'G', 'H', '', '-----------ES-----------', 0, 7, 7,
                          16, 10, 10, 24, 26, '-----------EF-----------', 7, 16, 10, 24, 15, 14, 26, 27, 'Start', 'IN',
                          'IN', 'IN', 'IN', 'IN', 'IN', 'IN', '-----------LS-----------', 0, 7, 16, 16, 19, 20, 24, 26,
                          '-----------LF-----------', 7, 16, 19, 24, 24, 24, 26, 27, '-----------SK-----------', 0, 0, 9, 0,
                          9, 10, 0, 0]
        calculation_service = CpmCalculationService()
        # WHEN
        result = calculation_service.calculate(activities, durations, predecessors)
        # THEN
        assert expected_value == result


def test_zad2():
    with patch('matplotlib.pyplot.savefig'):
        # GIVEN
        activities = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J']
        durations = [3, 4, 6, 7, 1, 2, 3, 4, 1, 2]
        predecessors = ['', 'A', 'A', 'B', 'D', 'ECH', 'C', 'G', 'F', 'I']
        expected_value = None
        calculation_service = CpmCalculationService()
        # WHEN
        result = calculation_service.calculate(activities, durations, predecessors)
        # THEN
        assert expected_value == result


def test_zad3():
    with patch('matplotlib.pyplot.savefig'):
        # GIVEN
        activities = ['A', 'B', 'C', 'D', 'E', 'F']
        durations = [5, 3, 4, 6, 4, 3]
        predecessors = ['', 'A', '', 'A', 'D', 'BCD']
        expected_value = None
        calculation_service = CpmCalculationService()
        # WHEN
        result = calculation_service.calculate(activities, durations, predecessors)
        # THEN
        assert expected_value == result
