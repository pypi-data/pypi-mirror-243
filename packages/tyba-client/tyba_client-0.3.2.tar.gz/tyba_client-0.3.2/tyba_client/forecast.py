from datetime import datetime, time


class Forecast(object):
    def __init__(self, client):
        self.client = client

    def get(self, route, params=None):
        response = self.client.get(f"forecasts/{route}", params=params)
        response.raise_for_status()
        return response.json()

    def most_recent(self, object_name: str, product: str, start_time: datetime, end_time: datetime):
        return self.get("most_recent_forecast", params={"object_name": object_name,
                                                        "product": product,
                                                        "start_time": start_time,
                                                        "end_time": end_time})

    def vintaged(self, object_name: str, product: str, start_time: datetime, end_time: datetime, days_ago: int,
                 before_time: time, exact_vintage: bool = False):
        return self.get("vintaged_forecast",
                        params={
                            "object_name": object_name,
                            "product": product,
                            "start_time": start_time,
                            "end_time": end_time,
                            "days_ago": days_ago,
                            "before_time": before_time,
                            "exact_vintage": exact_vintage,
                        })

    def actuals(self, object_name: str, product: str, start_time: datetime, end_time: datetime):
        return self.get("actuals", params={"object_name": object_name,
                                           "product": product,
                                           "start_time": start_time,
                                           "end_time": end_time})
