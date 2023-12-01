from .api_requests import APIRequests
from .glade_constants import Constant
from .helpers import Helpers

class Glade:
    def __init__(self, merchantId=None, merchantKey=None, isProduction=False):        
        self.merchantId = merchantId
        self.merchantKey = merchantKey
        self.baseUrl = (
            Constant.SANBOX_ENVIRONMENT()
            if isProduction == False
            else Constant.PRODUCTION_ENVIRONMENT()
        )
        
        self.apiCall = APIRequests(self.merchantId, self.merchantKey, self.baseUrl)

    def bvnValidation(self, bvnNumber):
        return self.apiCall.makeApiCall(
            Constant.PUT_METHOD(),
            Constant.RESOURCE_URL(),
            {"inquire": "bvn", "bvn": bvnNumber},
        )

    def supportedChargeableBanks(self):
        return self.apiCall.makeApiCall(
            Constant.PUT_METHOD(),
            Constant.RESOURCE_URL(),
            {"inquire": "supported_chargable_banks"},
        )

    def bankList(self):
        return self.apiCall.makeApiCall(
            Constant.PUT_METHOD(), Constant.RESOURCE_URL(), {"inquire": "banks"}
        )

    def verifyAccountName(self, accountNumer, bankCode, bankName):
        return self.apiCall.makeApiCall(
            Constant.PUT_METHOD(),
            Constant.RESOURCE_URL(),
            {
                "inquire": "accountname",
                "accountnumber": accountNumer,
                "bankcode": bankCode,
                "bankname": bankName,
            },
        )

    def personalizedAccount(
        self, accountName, accountEmail, accountBvn, reference, channel="providus"
    ):
        return self.apiCall.makeApiCall(
            Constant.PUT_METHOD(),
            Constant.RESOURCE_URL(),
            {
                "request": "personalized-accounts",
                "name": accountName,
                "reference": reference,
                "email": accountEmail,
                "bvn": accountBvn,
                "bank": channel,
            },
        )

    def createCustomer(self, name, email, phoneNumber, address):
        return self.apiCall.makeApiCall(
            Constant.PUT_METHOD(),
            Constant.RESOURCE_URL(),
            {
                "request": "customer",
                "address": address,
                "email": email,
                "name": name,
                "phone": phoneNumber,
            },
        )

    def getCustomers(self):
        return self.apiCall.makeApiCall(
            Constant.PUT_METHOD(), Constant.RESOURCE_URL(), {"inquire": "customer"}
        )

    def getCustomerDetail(self, customerId):
        return self.apiCall.makeApiCall(
            Constant.PUT_METHOD(),
            Constant.RESOURCE_URL(),
            {"inquire": "customer_detail", "customer_id": customerId},
        )

    def getBillCategory(self, category=None):
        data = {"action": "pull"}
        if category:
            data["category"] = category

        return self.apiCall.makeApiCall(
            Constant.PUT_METHOD(), Constant.BILL_URL(), data
        )

    def getBillById(self, billId):
        return self.apiCall.makeApiCall(
            Constant.PUT_METHOD(),
            Constant.BILL_URL(),
            {"action": "pull", "bills_id": billId},
        )

    def resolveBill(self, payCode, reference):
        return self.apiCall.makeApiCall(
            Constant.PUT_METHOD(),
            Constant.BILL_URL(),
            {"action": "resolve", "paycode": payCode, "reference": reference},
        )

    def purchaseBill(self, payCode, amount, reference, orderReference=None):
        return self.apiCall.makeApiCall(
            Constant.PUT_METHOD(),
            Constant.BILL_URL(),
            {
                "action": "resolve",
                "paycode": payCode,
                "reference": reference,
                "amount": amount,
                "orderRef": orderReference,
            },
        )

    def verifyBillPurchase(self, transactionReference):
        return self.apiCall.makeApiCall(
            Constant.PUT_METHOD(),
            Constant.BILL_URL(),
            {"action": "verify", "txnRef": transactionReference},
        )

    def transfer(
        self,
        amount,
        receiverAccountNumber,
        receiverBankCode,
        senderName,
        reference,
        narration,
    ):
        return self.apiCall.makeApiCall(
            Constant.PUT_METHOD(),
            Constant.TRANSFER_URL(),
            {
                "action": "transfer",
                "amount": amount,
                "accountnumber": receiverAccountNumber,
                "bankcode": receiverBankCode,
                "sender_name": senderName,
                "narration": narration,
                "orderRef": reference,
            },
        )

    def verifySingleTransfer(self, reference):
        return self.apiCall.makeApiCall(
            Constant.PUT_METHOD(),
            Constant.TRANSFER_URL(),
            {
                "action": "verify",
                "txnRef": reference,
            },
        )

    def bulkTransfer(self, transferObjects):
        if not Helpers.validateMultiArray(transferObjects):
            return Helpers.handleCustomResponse(
                400, "error", "object must be a multidimensional array"
            )

        if not Helpers.validateBulkTransferArray(transferObjects):
            return Helpers.handleCustomResponse(
                400,
                "error",
                "Data structure does not match required data, please refer to documentation",
            )

        return self.apiCall.makeApiCall(
            Constant.PUT_METHOD(),
            Constant.TRANSFER_URL(),
            {"action": "transfer", "type": "bulk", "data": transferObjects},
        )

    def createPaymentLink(
        self,
        title,
        description,
        amount,
        ptype,
        payerBearsFees,
        acceptNumber,
        notificationEmail,
        customLink=None,
        redirectUrl=None,
        customMessage=None,
        frequency=None,
    ):
        return self.apiCall.makeApiCall(
            Constant.PUT_METHOD(),
            Constant.RESOURCE_URL(),
            {
                "request": "paylink",
                "title": title,
                "description": description,
                "amount": amount,
                "currency": "NGN",
                "type": ptype,
                "payer_bears_fees": payerBearsFees,
                "accept_number": acceptNumber,
                "custom_link": customLink,
                "redirect_url": redirectUrl,
                "custom_message": customMessage,
                "notification_email": notificationEmail,
                "frequency": frequency,
            },
        )

    def createTicket(
        self,
        title,
        description,
        amount,
        ttype,
        payerBearsFees,
        acceptNumber,
        notificationEmail,
        ticketData,
        customLink=None,
        redirectUrl=None,
        customMessage=None,
        frequency=None,
    ):
        return self.apiCall.makeApiCall(
            Constant.PUT_METHOD(),
            Constant.RESOURCE_URL(),
            {
                "request": "ticket",
                "title": title,
                "description": description,
                "amount": amount,
                "currency": "NGN",
                "type": ttype,
                "payer_bears_fees": payerBearsFees,
                "accept_number": acceptNumber,
                "custom_link": customLink,
                "redirect_url": redirectUrl,
                "custom_message": customMessage,
                "notification_email": notificationEmail,
                "frequency": frequency,
                "ticket_data": ticketData,
            },
        )

    def invoice(
        self,
        customerId,
        chargeUser,
        shipping,
        vat,
        dueDate,
        allowedDiscount,
        invoiceItems,
        note,
        discountType=None,
        invoiceId=None,
    ):
        return self.apiCall.makeApiCall(
            Constant.PUT_METHOD(),
            Constant.RESOURCE_URL(),
            {
                "request": "invoice",
                "invoice_id": invoiceId,
                "currency": "NGN",
                "customer_id": customerId,
                "date_due": dueDate,
                "discount_type": discountType,
                "discount": allowedDiscount,
                "shipping": shipping,
                "vat": vat,
                "note": note,
                "charge_user": chargeUser,
                "items": invoiceItems,
            },
        )
