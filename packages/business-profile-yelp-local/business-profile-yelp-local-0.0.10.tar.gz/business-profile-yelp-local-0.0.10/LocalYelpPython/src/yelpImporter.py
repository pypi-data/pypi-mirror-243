import json
import os

from dotenv import load_dotenv
from gql import Client, gql
from gql.transport.requests import RequestsHTTPTransport

load_dotenv()
from logger_local.Logger import Logger  # noqa: E402

YELP_API_ENDPOINT = 'https://api.yelp.com/v3/graphql'
LOCAL_YELP_COMPONENT_ID = 156


class YelpImporter:
    def __init__(self):
        self.logger = Logger(object={'component_id': LOCAL_YELP_COMPONENT_ID})

    def get_data(self, business_type: str, location: str, total_entries: int = 10):
        self.logger.start("Fetching business data from Yelp GraphQL",
                          object={"component_id": LOCAL_YELP_COMPONENT_ID, "component_name": "Local yelp importer"})

        query = gql('''
          query ($term: String!, $location: String!, $limit: Int!, $offset: Int!) {
            search(term: $term, location: $location, limit: $limit, offset: $offset) {
              business {
                name
                rating
                location {
                  address1
                  city
                  state
                  country
                  postal_code
                }
                phone
                photos
                coordinates {
                  latitude
                  longitude
                }
                hours {
                  hours_type
                  is_open_now
                  open {
                    day
                    is_overnight
                    end
                    start
                  }
                }
              }
              total
            }
          }
        ''')

        # Define GraphQL transport
        transport = RequestsHTTPTransport(
            url=YELP_API_ENDPOINT,
            headers={'Authorization': f'Bearer {os.getenv("YELP_API_KEY")}'},
            use_json=True,
        )

        # Define GraphQL client
        graphql_client = Client(
            transport=transport,
            fetch_schema_from_transport=False,
        )

        max_per_iteration = 50
        offset = 0
        data = {"results": []}

        while offset < total_entries:
            limit = min(max_per_iteration, total_entries - offset)
            try:
                # TODO We should add the API Management In Direct
                response = graphql_client.execute(query, variable_values={'term': business_type, 'location': location,
                                                                          'limit': limit, 'offset': offset})
                for business in response['search']['business']:
                    self.logger.info(object={"Business_dict": business})
                    dictionary = dict()
                    # reformat dictionary to fit generic template
                    dictionary["name"] = business["name"]
                    dictionary["location"] = {"coordinates": business["coordinates"],
                                              "address_local_language": business["location"]["address1"],
                                              "city": business["location"]["city"],
                                              "country": business["location"]["country"],
                                              "postal_code": business["location"]["postal_code"]
                                              }
                    dictionary["phone"] = {"number_original": business["phone"]},
                    dictionary["storage"] = {"path": business["photos"]},
                    dictionary["reaction"] = {"value": business["rating"], "reaction_type": "Rating"},
                    dictionary["operational_hours"] = []
                    if len(business["hours"]) > 0:
                        for day_dict in business["hours"][0]["open"]:
                            dictionary["operational_hours"].append(
                                {"day_of_week": day_dict["day"], "from": self.reformat_time_string(day_dict["start"]),
                                 "until": self.reformat_time_string(day_dict["end"])})

                    data["results"].append(dictionary)

                offset += limit
                total_entries = min(total_entries, response['search']['total'])
                self.logger.info(f"Retrieved data for {offset} businesses so far")

            except Exception as e:
                self.logger.exception("Exception during retrieving businesses from yelp", object=e)
                break

        self.logger.end(f"retrieved {offset} businesses from yelp")
        return json.dumps(data, ensure_ascii=False)

    # TODO: We insert a profile into the database
    #  and we send the profile_id to the importer to record what is the source of this profile
    # def insert_profile_and_update_importer(self, conn = connect()):
    # entity_id = profile generic package
    #   my_importer = importer.Importer("Yelp.com GraphQL", 1)

    #   my_importer.insert_record_data_source(
    #           "United States", "Business Profile", entity_id, "https://api.yelp.com/v3/graphql")

    # TODO Let's move this to python-sdk repo time.py
    @staticmethod
    def reformat_time_string(input_str: str) -> str:
        hours = input_str[:2]
        minutes = input_str[2:]
        time_format = f"{hours}:{minutes}:00:00"
        return time_format
