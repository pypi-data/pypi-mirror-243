"""Testing nazca4sdk """
from nazca4sdk import SDK
from nazca4sdk.datahandling.file.file_storage import FileStorage

sdk = SDK()
# print(sdk.modules)


# file = sdk.file_storage.download_file("/siemka2.txt", "./siemka.txt")
sdk.file_storage.send_file('/Sodomita.txt', "./siemka.txt")
print("OK")
