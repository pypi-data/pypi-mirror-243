class Helpers:
    
    @staticmethod
    def validateMultiArray(array):
        array.sort(key=lambda x: x["sender_name"], reverse=True)
        if isinstance(array, list):
            if any(isinstance(sub_obj, (list, dict)) for sub_obj in array):
                return True
        elif isinstance(array, dict):
            if any(isinstance(value, (list, dict)) for value in array.values()):
                return True
        return False

    @staticmethod
    def validateBulkTransferArray(array_of_objects):
        transfer_data = ["amount", "accountnumber", "bankcode", "sender_name", "narration", "orderRef"]
        for array in array_of_objects:
            if any(key not in array for key in transfer_data):
                return False
        return True
    
    @staticmethod
    def handleSuccessResponse(responsePayload):
        response = {}
        response["code"] = responsePayload.status_code
        response["status"] = "success"
        response["data"] = responsePayload

        return response

    @staticmethod
    def handleFailureResponse(responsePayload):
        response = {}
        response["code"] = responsePayload.status_code
        response["status"] = "error"
        response["message"] = (
            "Ensure merchant key and merchant id is provided"
            if (response["code"] == 401 or response["code"] == "401")
            else responsePayload.json()["message"]
        )

        return response

    @staticmethod
    def handleCustomResponse(code, status, message):
        response = {}
        response["code"] = code
        response["status"] = status
        response["message"] = message
        return response
    
    @staticmethod
    def apiFailureResponse():
        return {
            "code": 500,
            "status": "error",
            "message": "Error retrieving data from API",
        }
    
    @staticmethod
    def exceptionsHandler(response):
        errortype = type(response).__name__
        if errortype == "ConnectionError":
            return Helpers.handleCustomResponse(404, "error", "Can not connect to API")
        elif  errortype == "Timeout":
            return Helpers.handleCustomResponse(408, "error", "API request timed out")
        elif  errortype == "RequestException":
            return Helpers.handleCustomResponse(404, "error", "API request failure")
        else:
            return Helpers.handleCustomResponse(400, "error", f"API request failure - ${errortype}")