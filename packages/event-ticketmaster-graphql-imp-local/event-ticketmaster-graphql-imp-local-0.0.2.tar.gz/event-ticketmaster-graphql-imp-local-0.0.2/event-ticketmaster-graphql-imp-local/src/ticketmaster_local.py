from dotenv import load_dotenv
import os
import requests
import geohash2

# from logger_local.Logger import Logger
# from logger_local.LoggerComponentEnum import LoggerComponentEnum

load_dotenv()
#Setup the logger: change YOUR_REPOSITORY variable name and value
# YOUR_REPOSITORY_COMPONENT_ID = 246  # ask your team leader for this integer
# YOUR_REPOSITORY_COMPONENT_NAME = "event-ticketmaster-graphql-imp-local-python-package"
# DEVELOPER_EMAIL = "gil.a@circ.zone"
# object1 = {
#    'component_id': YOUR_REPOSITORY_COMPONENT_ID,
#    'component_name': YOUR_REPOSITORY_COMPONENT_NAME,
    # 'component_category': LoggerComponentEnum.ComponentCategory.Code.value,
    # 'developer_email': DEVELOPER_EMAIL
# }
# logger=Logger.create_logger(object=object1)


class TicketmasterLocal:
    def __init__(self) -> None:
        self.base_url=os.getenv("TICKETMASTER_BASE_URL")
        self.api_key=os.getenv("TICKETMASTER_API_KEY")
        self.discover_events=os.getenv("TICKETMASTER_DISCOVER_EVENTS")

    def get_events(self, query_params):
        query_params_string = "&".join([f"{key}={value}" for key, value in query_params.items()])

        url = f"{self.base_url}{self.discover_events}?apikey={self.api_key}&{query_params_string}"
        response = requests.get(url, params=None)
        return response.json()

    def get_event_by_name(self, name, num_of_events=1):
        query_params={
            "keyword":name,
            "size":num_of_events}
        
        return self.get_events(query_params)

    def get_events_by_radius(self, lat, lng, radius, unit):

        geopoint = geohash2.encode(lat, lng, precision=9)

        query_params={
            "geoPoint":geopoint,
            "radius":radius,
            "unit":unit}
        
        return self.get_events(query_params)

    def get_events_by_radius_km(self, lat, lng, radius):
        return self.get_events_by_radius(lat, lng, radius, "km")

    def get_events_by_radius_miles(self, lat, lng, radius):
        return self.get_events_by_radius(lat, lng, radius, "miles")
    



ticketmaster_local = TicketmasterLocal()
#print(restticketmaster.get_event_by_name("football"))
#print(restticketmaster.get_events_by_radius_km(	51.509865, -0.118092, 100))