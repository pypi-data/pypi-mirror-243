from typing import List, Optional, Union
from ua_alarm import types
from aiohttp import ClientSession


class Client:
    """
    A client to interact with the UkraineAlert API, providing methods to access various endpoints.

    Attributes:
        base_url (str): The base URL for UkraineAlert API.
        headers (dict): The headers required for authorization in API requests.

    Methods:
        __init__(api_token: str): Initialize the UkraineAlertApiClient with an API token.
        _make_request(method: str, endpoint: str, params: Optional[dict] = None, data: Optional[dict] = None) -> Union[types.AlertRegionModel, types.AlertModification, types.RegionAlarmsHistory, types.RegionsViewModel, types.WebHook]: Make a request to the UkraineAlert API.
        get_alerts() -> List[types.AlertRegionModel]: Get a list of alerts.
        get_region_alerts(region_id: str|int) -> List[types.AlertRegionModel]: Get alerts for a specific region.
        get_alert_status() -> types.AlertModification: Get the status of alerts.
        get_region_history(region_id: str|int) -> types.RegionAlarmsHistory: Get the history of alerts for a specific region.
        get_regions() -> types.RegionsViewModel: Get information about regions.
        subscribe_to_webhook(webhook_data: dict) -> types.WebHook: Subscribe to a webhook.
        update_webhook(webhook_data: dict) -> None: Update an existing webhook.
        unsubscribe_from_webhook(webhook_data: dict) -> None: Unsubscribe from a webhook.
    """

    _ALERTS_ENDPOINT = "/api/v3/alerts"
    _ALERT_STATUS_ENDPOINT = "/api/v3/alerts/status"
    _REGION_HISTORY_ENDPOINT = "/api/v3/alerts/regionHistory"
    _REGIONS_ENDPOINT = "/api/v3/regions"
    _WEBHOOK_ENDPOINT = "/api/v3/webhook"

    def __init__(self, api_token: str):
        """
        Initializes the UkraineAlertApiClient with the provided API token.

        Args:
            api_token (str): The API token required for authorization.
        """
        self.base_url = "https://api.ukrainealarm.com"
        self.headers = {"Authorization": api_token}

    async def _make_request(
            self,
            method: str,
            endpoint: str,
            params: Optional[dict] = None,
            data: Optional[dict] = None,
    ) -> Union[
        types.AlertRegionModel,
        types.AlertModification,
        types.RegionAlarmsHistory,
        types.RegionsViewModel,
        types.WebHook,
    ]:
        """
        Makes a request to the UkraineAlert API.

        Args:
            method (str): The HTTP method for the request (e.g., GET, POST, PATCH, DELETE).
            endpoint (str): The specific API endpoint to access.
            params (Optional[dict]): Optional parameters for the request.
            data (Optional[dict]): Optional data payload for the request.

        Returns:
            Union[types.AlertRegionModel, types.AlertModification, types.RegionAlarmsHistory, types.RegionsViewModel, types.WebHook]: The response from the API based on the endpoint accessed.
        """
        url = f"{self.base_url}{endpoint}"
        async with ClientSession(headers=self.headers) as session:
            async with session.request(
                    method, url, params=params, json=data
            ) as response:
                response_json = await response.json()

                # Determine and return the appropriate model object based on the endpoint accessed
                if endpoint == self._ALERT_STATUS_ENDPOINT:
                    return types.AlertModification(**response_json)
                elif endpoint == self._REGION_HISTORY_ENDPOINT:
                    return [types.RegionAlarmsHistory(**item) for item in response_json]
                elif endpoint == self._REGIONS_ENDPOINT:
                    return types.RegionsViewModel(**response_json)
                elif endpoint == self._WEBHOOK_ENDPOINT:
                    return types.WebHook(**response_json)
                elif self._ALERTS_ENDPOINT in endpoint:
                    return [types.AlertRegionModel(**item) for item in response_json]

    async def get_alerts(self, region_id: str | int = None) -> List[types.AlertRegionModel]:
        """
        Retrieves alerts from the UkraineAlert API.

        Args:
            region_id (str or int, optional): The ID of the region for which alerts are requested. Defaults to None.

        Returns:
            List[types.AlertRegionModel]: A list of types.AlertRegionModel objects.
        """
        endpoint = self._ALERTS_ENDPOINT if not region_id else f"{self._ALERTS_ENDPOINT}/{region_id}"
        return await self._make_request("GET", endpoint)

    async def get_alert_status(self) -> types.AlertModification:
        """
        Retrieves the status of alerts from the UkraineAlert API.

        Returns:
            types.AlertModification: An object representing the status of alerts.
        """
        return await self._make_request("GET", self._ALERT_STATUS_ENDPOINT)

    async def get_region_history(
            self, region_id: str | int
    ) -> types.RegionAlarmsHistory:
        """
        Retrieves the history of alerts for a specific region from the UkraineAlert API.

        Args:
            region_id (str or int): The ID of the region for which the history of alerts is requested.

        Returns:
            types.RegionAlarmsHistory: An object representing the history of alerts for the specified region.
        """
        params = {"regionId": region_id}
        return await self._make_request(
            "GET", self._REGION_HISTORY_ENDPOINT, params=params
        )

    async def get_regions(self) -> types.RegionsViewModel:
        """
        Retrieves information about regions from the UkraineAlert API.

        Returns:
            types.RegionsViewModel: An object representing information about regions.
        """
        return await self._make_request("GET", self._REGIONS_ENDPOINT)

    async def subscribe_to_webhook(self, webhook_data: dict) -> types.WebHook:
        """
        Subscribes to a webhook in the UkraineAlert API.

        Args:
            webhook_data (dict): Data required for subscribing to the webhook.

        Returns:
            types.WebHook: An object representing the subscribed webhook.
        """
        return await self._make_request(
            "POST", self._WEBHOOK_ENDPOINT, data=webhook_data
        )

    async def update_webhook(self, webhook_data: dict) -> None:
        """
        Updates an existing webhook in the UkraineAlert API.

        Args:
            webhook_data (dict): Data required for updating the webhook.
        """
        await self._make_request("PATCH", self._WEBHOOK_ENDPOINT, data=webhook_data)

    async def unsubscribe_from_webhook(self, webhook_data: dict) -> None:
        """
        Unsubscribes from a webhook in the UkraineAlert API.

        Args:
            webhook_data (dict): Data required for unsubscribing from the webhook.
        """
        await self._make_request("DELETE", self._WEBHOOK_ENDPOINT, data=webhook_data)
