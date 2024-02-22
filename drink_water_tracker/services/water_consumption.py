from datetime import date
from typing import Dict, List, Union

from numpy import where
from pandas import DataFrame  # type: ignore

from drink_water_tracker.db.models import WaterConsumption


class WaterConsumptionService:
    def __init__(self) -> None:
        pass

    def calculate_user_goals(
        self, water_consumption_on_db: List[WaterConsumption]
    ) -> List[Dict[str, Union[date, float, bool]]]:

        data_wc = [
            {
                "weight": wc_on_db.user.weight,
                "drink_date": wc_on_db.drink_date,
                "amount_ml": wc_on_db.cup_size.amount_ml,
            }
            for wc_on_db in water_consumption_on_db
        ]

        df = DataFrame(data_wc)

        df_gols = df.groupby("drink_date").amount_ml.sum().reset_index()

        df_gols.rename(
            columns={
                "drink_date": "consumption_date",
                "amount_ml": "total_consumption_ml",
            },
            inplace=True,
        )

        df_gols["day_goal_ml"] = 35 * df.weight.loc[0]

        df_gols["remaining_goal_ml"] = (
            df_gols.day_goal_ml - df_gols.total_consumption_ml
        ).apply(lambda x: x if x >= 0 else 0)

        df_gols["consumed_goal_ml"] = where(
            df_gols.total_consumption_ml < df_gols.day_goal_ml,
            df_gols.total_consumption_ml,
            df_gols.day_goal_ml,
        )

        df_gols["consumed_goal_percentage"] = (
            ((df_gols["consumed_goal_ml"] / df_gols["day_goal_ml"]) * 100)
            .astype(float)
            .round(1)
        )

        df_gols["goal_reached"] = df_gols["consumed_goal_percentage"] == 100

        return df_gols.to_dict("records")
