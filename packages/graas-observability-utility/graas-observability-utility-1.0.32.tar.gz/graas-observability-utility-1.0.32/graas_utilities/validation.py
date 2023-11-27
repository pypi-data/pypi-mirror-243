import json
import os
import jsonschema
from .ref_Resolver import ExtendedRefResolver
from .configs import mappingObject
from pkg_resources import resource_filename


def executeValidateJson(data, schema):
    try:
        jsonschema.validate(
            data,
            schema,
            resolver=ExtendedRefResolver(
                base_uri=resource_filename(__name__, '/Schema'),
                referrer=schema,
            ),
        )
    except jsonschema.exceptions.ValidationError as err:
        return {"status": "SCHEMA_VALIDATION_FAILED", "message": err.message}
    return {
        "status": "SCHEMA_VALIDATION_SUCCESS",
        "message": "Schema successfully validated",
    }


def extract_data_from_file(schema_file):
    path_for_schema = resource_filename(__name__, '/Schema')

    with open(f"{path_for_schema}/{schema_file}.json", "r") as schema_file:
        schemaObj = json.load(schema_file)

    return schemaObj


def validateJson(dataJsonString, reportType):
    if reportType is None or not reportType:
        return {
            "status": "SCHEMA_VALIDATION_FAILED",
            "message": "Report type is Empty or None please enter valid string value!",
        }

    schema_file = mappingObject.get(reportType, "")

    if schema_file:
        try:
            jsonObject = json.loads(dataJsonString)
        except Exception as err:
            print("Error in converting data from string to json", err)
            return {
                "status": "SCHEMA_VALIDATION_FAILED",
                "message": "Error in converting data from string to json",
            }
        if jsonObject:
            schemaObject = extract_data_from_file(schema_file)
            isValidated = executeValidateJson(jsonObject, schemaObject)
            return isValidated
        else:
            return {
                "status": "SCHEMA_VALIDATION_FAILED",
                "message": "Object is empty please enter correct object",
            }
    else:
        return {
            "status": "SCHEMA_VALIDATION_FAILED",
            "message": "Report type which you have entered is not correct or empty please update and try again!",
        }
