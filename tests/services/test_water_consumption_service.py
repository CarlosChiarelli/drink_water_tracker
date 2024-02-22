from datetime import date

from drink_water_tracker.services.water_consumption import WaterConsumptionService


def test_water_consumption_goal_calculation_service(water_consumption_one_user_on_db):
    service = WaterConsumptionService()
    goals = service.calculate_user_goals(
        water_consumption_on_db=water_consumption_one_user_on_db
    )

    assert goals[0] == {
        "consumption_date": date(2024, 2, 21),
        "day_goal_ml": 2450,
        "remaining_goal_ml": 0,
        "consumed_goal_ml": 2450,
        "consumed_goal_percentage": 100,
        "total_consumption_ml": 3000,
        "goal_reached": True,
    }
    assert goals[1] == {
        "consumption_date": date(2024, 2, 22),
        "day_goal_ml": 2450,
        "remaining_goal_ml": 2100,
        "consumed_goal_ml": 350,
        "consumed_goal_percentage": 14.3,
        "total_consumption_ml": 350,
        "goal_reached": False,
    }
