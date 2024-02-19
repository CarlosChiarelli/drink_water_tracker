from pydantic import BaseModel


class CustomBaseModel(BaseModel):
    def dict(self, *args, **kwargs) -> dict:
        """Remove pairs with a value of None.

        Returns:
            dict: dict without pairs with a value of None.
        """
        d = super().model_dump(*args, **kwargs)
        d = {k: v for k, v in d.items() if v}
        return d
