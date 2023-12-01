class Constant:
    # Url method constants
    def POST_METHOD():
        return "post"

    def GET_METHOD():
        return "get"

    def PATCH_METHOD():
        return "patch"

    def PUT_METHOD():
        return "put"

    def DELETE_METHOD():
        return "delete"

    # Base URL constants
    def SANBOX_ENVIRONMENT():
        return "https://api-testing.gladefinance.co/"

    def PRODUCTION_ENVIRONMENT():
        return "https://api.gladefinance.co/"

    # Endpoint Constants
    def LINK_CHANNEL():
        return "link"

    def INVOICE_CHANNEL():
        return "invoice"

    def TICKET_CHANNEL():
        return "ticket"

    def RESOURCE_URL():
        return "resources"

    def BILL_URL():
        return "bills"

    def TRANSFER_URL():
        return "disburse"
