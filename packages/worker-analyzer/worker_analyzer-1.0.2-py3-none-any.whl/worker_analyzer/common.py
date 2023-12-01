from datetime import datetime


class StorageFunctions:
    @staticmethod
    def date_to_isoformat(data):
        for key, value in data.items():
            if isinstance(value, datetime):
                data[key] = value.isoformat()
            elif isinstance(value, dict):
                data[key] = StorageFunctions.date_to_isoformat(value)
            elif isinstance(value, list):
                data[key] = [
                    StorageFunctions.date_to_isoformat(item)
                    if isinstance(item, dict)
                    else item
                    for item in value
                ]
        return data

    @staticmethod
    def isoformat_to_date(data):
        for key, value in data.items():
            if isinstance(value, str):
                try:
                    data[key] = datetime.fromisoformat(value)
                except ValueError:
                    pass
            elif isinstance(value, dict):
                data[key] = StorageFunctions.isoformat_to_date(value)
            elif isinstance(value, list):
                data[key] = [
                    StorageFunctions.isoformat_to_date(item)
                    if isinstance(item, dict)
                    else item
                    for item in value
                ]
        return data


class ValidateFunctions:
    @staticmethod
    def validate_dict(data: dict, verifications: list):
        if not isinstance(data, dict):
            raise TypeError("Expected dictionary for 'data'")

        if not isinstance(verifications, list):
            raise TypeError("Expected list for 'verifications'")

        if len(verifications) == 0:
            raise ValueError("Expected at least one verification")

        data_keys = data.keys()
        for verification in verifications:
            if verification[0] not in data_keys:
                raise Exception(f"Data missing required key: {verification}")

            if not isinstance(data[verification[0]], verification[1]):
                raise TypeError(f"Expected {verification[1]} for '{verification[0]}'")
