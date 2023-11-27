import json
import os
import jsonschema
from jsonschema.exceptions import ValidationError
from pkg_resources import resource_filename

def health_check():
    return "Hello World!"

def validate_json_data(data_string, type):
    result_obj = {
        "status": "",
        "message": ""
    }
    schema_file = ''
    if type == "onsite_campaigns":
        schema_file = resource_filename(__name__, '/schemas/Onsite_campaigns/Onsite_campaign.json')
        
    # isValidSchema = validate_schema(data_string)
    
    # if isValidSchema:
    if schema_file != '':
        # Load the JSON schema from the schema file
        with open(schema_file, "r") as schema_file:
            schema = json.load(schema_file)

        try:
            data_obj = json.loads(data_string)
            jsonschema.validate(data_obj, schema)
            result_obj["status"] = "SCHEMA_VALIDATION_SUCCESS"
            result_obj["message"] = "Schema successfully validated"
            
            # return True  # Data matches the schema
        except ValidationError as e:
            print("Error", e)
            result_obj["status"] = "SCHEMA_VALIDATION_FAILED"
            result_obj["message"] = e.message
            return result_obj
            # return False  # Data does not match the schema
    else:
        return result_obj
    # else:
    #     result_obj["status"] = "SCHEMA_VALIDATION_FAILED"
    #     result_obj["message"] = "Schema validation failed due to lint error"

    return result_obj
    
def validate_schema(json_string):
    try:
        return json.loads(json_string)
    except ValueError:
        print("  Is valid?: False")
        return False

# file_path = os.path.abspath(__file__)
# base_uri = f"file:{file_path}"
# print(f"\nbase uri = '{base_uri}'\n")
# File paths for the schema and data files
# schema_file_path = os.path.join(os.getcwd(), "schemas/Onsite_campaigns/Onsite_campaign.json")
# data_file_path = os.path.join(
#     os.getcwd(), "Data_for_testing/AABCW_Campaign_onsite_lazada.json"
# )

# jsonstr = '[{"merchantID":"AAANV","siteNickNameId":"shopee-2","countryCode":"SG","currencyCode":"SGD","result":[{"Sequence":1,"Product_Name_Ad_Name":"(Pack of 2) Cif Scrub Mommy Kitchen Sponge, Original Pink Sponge","Status":"Ongoing","Product_ID":20743773418.0,"Ads_Type":"Discovery Ads","Placement_Keyword":"All","Start_Date":"16-05-2023 00:00","End_Date":"Unlimited","Impression":1918,"Clicks":33,"CTR":1.72,"Conversions":0,"Direct_Conversions":0,"Conversion_Rate":0.0,"Direct_Conversion_Rate":0.0,"Cost_per_Conversion":{"amount":0,"currencyCode":"SGD"},"Cost_per_Direct_Conversion":{"amount":0,"currencyCode":"SGD"},"Items_Sold":0,"Direct_Items_Sold":0,"GMV":{"amount":0,"currencyCode":"SGD"},"Direct_GMV":{"amount":0,"currencyCode":"SGD"},"Expense":{"amount":685,"currencyCode":"SGD"},"ROAS":0.0,"Direct_ROAS":0.0,"ACOS":0.0,"Direct_ACOS":0.0,"Product_Impressions":0,"Product_Clicks":0,"Product_CTR":0.0,"Date":"04-11-2023"}]}]'
# jsonstr = {"property1":"value1"}
# validate_schema(jsonstr)
# jsonstr = json.loads(jsonstr)
# print(type(jsonstr))

# validation_result = validate_json_data(jsonstr, "onsite_campaigns")
# print(validation_result)