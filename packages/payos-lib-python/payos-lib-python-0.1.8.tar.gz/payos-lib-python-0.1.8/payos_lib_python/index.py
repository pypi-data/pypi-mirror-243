from payos_lib_python.constants import ERROR_MESSAGE, ERROR_CODE, PAYOS_BASE_URL
from payos_lib_python.utils import createSignatureFromObj, createSignatureOfPaymentRequest
from payos_lib_python.custom_error import PayOSError 
import requests
from payos_lib_python.type import PaymentData, ItemData
class PayOS:
    def __init__(self, client_id, api_key, checksum_key) -> None:
        # Kiểm tra kiểu dữ liệu của client_id
        if not isinstance(client_id, str):
            raise TypeError("client_id must be a string.")

        # Kiểm tra kiểu dữ liệu của api_key
        if not isinstance(api_key, str):
            raise TypeError("api_key must be a string.")

        # Kiểm tra kiểu dữ liệu của checksum_key
        if not isinstance(checksum_key, str):
            raise TypeError("checksum_key must be a string.")
        
        self.__client_id = client_id
        self.__api_key = api_key
        self.__checksum_key = checksum_key

    def createPaymentLink(self, paymentData: PaymentData):
        if not isinstance(paymentData, PaymentData):
            raise ValueError(f"{ERROR_MESSAGE['INVALID_PARAMETER']} paymentData is not a PaymentData Type")
        
        url = f"{PAYOS_BASE_URL}/v2/payment-requests"
        paymentData.signature = createSignatureOfPaymentRequest(paymentData, self.__checksum_key)
        headers = {
                "Content-Type": "application/json",  # Loại nội dung của body
                "x-client-id": self.__client_id,
                "x-api-key": self.__api_key,
            }
        paymentLinkRes = requests.post(url, data=paymentData.to_json(), headers=headers)
        if paymentLinkRes.status_code == 200:
            paymentLinkRes = paymentLinkRes.json()
            if(paymentLinkRes["code"] == "00"):
                paymentLinkResSignature = createSignatureFromObj(paymentLinkRes["data"], self.__checksum_key)
                if paymentLinkResSignature != paymentLinkRes["signature"]:
                    raise Exception(ERROR_MESSAGE['DATA_NOT_INTEGRITY'])
                if paymentLinkRes["data"] is not None:
                    return paymentLinkRes["data"]
                raise PayOSError(code=paymentLinkRes["code"], message=paymentLinkRes["desc"])
            else:
                raise PayOSError(code=paymentLinkRes["code"], message=paymentLinkRes["desc"])
        raise PayOSError(ERROR_CODE['INTERNAL_SERVER_ERROR'], ERROR_MESSAGE['INTERNAL_SERVER_ERROR'])
        
    def getPaymentLinkInfomation(self, orderId: str | int):
        if type(orderId) not in [str, int]:
            raise ValueError(ERROR_MESSAGE["INVALID_PARAMETER"])
        url = f"{PAYOS_BASE_URL}/v2/payment-requests/{orderId}"
        headers = {
                "Content-Type": "application/json",  # Loại nội dung của body
                "x-client-id": self.__client_id,
                "x-api-key": self.__api_key,
            }
        paymentLinkInfoRes = requests.get(url, headers=headers)
        if paymentLinkInfoRes.status_code == 200:
            paymentLinkInfoRes = paymentLinkInfoRes.json()
            if paymentLinkInfoRes["code"] == "00":
                paymentLinkInfoResSignature = createSignatureFromObj(paymentLinkInfoRes["data"], self.__checksum_key)
                if paymentLinkInfoResSignature != paymentLinkInfoRes["signature"]:
                    raise Exception(ERROR_MESSAGE['DATA_NOT_INTEGRITY'])
                if paymentLinkInfoRes["data"] is not None:
                    return paymentLinkInfoRes["data"]
                raise PayOSError(code=paymentLinkInfoRes["code"], message=paymentLinkInfoRes["desc"])
            else:
                raise PayOSError(code=paymentLinkInfoRes["code"], message=paymentLinkInfoRes["desc"])
        raise PayOSError(ERROR_CODE['INTERNAL_SERVER_ERROR'], ERROR_MESSAGE['INTERNAL_SERVER_ERROR'])
        
    def confirmWebhook(self, webhookUrl: str):
        if webhookUrl is None or len(webhookUrl) == 0:
            raise ValueError(ERROR_MESSAGE["INVALID_PARAMETER"])
        
        url = f"{PAYOS_BASE_URL}/confirm-webhook"
        data = {
            "webhookUrl": webhookUrl
        }
        headers = {
                "Content-Type": "application/json",  # Loại nội dung của body
                "x-client-id": self.__client_id,
                "x-api-key": self.__api_key,
            }
        responseConfirm = requests.post(url=url, json=data, headers=headers)
        if responseConfirm.status_code == 200:
            return webhookUrl
        elif responseConfirm.status_code == 404:
            raise PayOSError(ERROR_CODE["INTERNAL_SERVER_ERROR"], ERROR_MESSAGE["WEBHOOK_URL_INVALID"])
        elif responseConfirm.status_code == 401:
            raise PayOSError(ERROR_CODE["UNAUTHORIZED"], ERROR_MESSAGE["UNAUTHORIZED"])
        raise PayOSError(ERROR_CODE['INTERNAL_SERVER_ERROR'], ERROR_MESSAGE['INTERNAL_SERVER_ERROR'])

    def cancelPaymentLink(self, orderId: int, cancellationReason: str=None):
        if type(orderId) not in [str, int]:
            raise ValueError(ERROR_MESSAGE["INVALID_PARAMETER"])
        url = f"{PAYOS_BASE_URL}/v2/payment-requests/{orderId}/cancel"
        cancellationReason = {"cancellationReason" : cancellationReason} if cancellationReason is not None else None
        headers = {
            "Content-Type": "application/json",  # Loại nội dung của body
            "x-client-id": self.__client_id,
            "x-api-key": self.__api_key,
        }
        cancelPaymentLinkResponse = requests.post(url, headers=headers, json=cancellationReason)
        if cancelPaymentLinkResponse.status_code == 200:
            cancelPaymentLinkResponse = cancelPaymentLinkResponse.json()
            if cancelPaymentLinkResponse["code"] == "00":
                paymentLinkInfoResSignature = createSignatureFromObj(cancelPaymentLinkResponse["data"], self.__checksum_key)
                if paymentLinkInfoResSignature != cancelPaymentLinkResponse["signature"]:
                    raise Exception(ERROR_MESSAGE["DATA_NOT_INTEGRITY"])
                if cancelPaymentLinkResponse["data"] is not None:
                    return cancelPaymentLinkResponse["data"]
                raise PayOSError(code=cancelPaymentLinkResponse["code"], message=cancelPaymentLinkResponse["desc"])
            else:
                raise PayOSError(code=cancelPaymentLinkResponse["code"], message=cancelPaymentLinkResponse["desc"])
        raise PayOSError(ERROR_CODE['INTERNAL_SERVER_ERROR'], ERROR_MESSAGE['INTERNAL_SERVER_ERROR'])
        
    def verifyPaymentWebhookData(self, webhookBody):
        data = webhookBody["data"]
        signature = webhookBody["signature"]
        if data is None:
            raise ValueError(ERROR_MESSAGE["NO_DATA"])
        if signature is None:
            raise ValueError(ERROR_MESSAGE["NO_SIGNATURE"])
        signData = createSignatureFromObj(data=data, key=self.__checksum_key)

        if signData != signature:
            raise Exception(ERROR_MESSAGE["DATA_NOT_INTEGRITY"])
        return data
                       

