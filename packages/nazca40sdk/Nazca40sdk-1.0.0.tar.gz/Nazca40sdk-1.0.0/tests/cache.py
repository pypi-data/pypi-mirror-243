"""Testing nazca4sdk """

from nazca4sdk.sdk import SDK

sdk = SDK()

result = sdk.cache.write_keys("franek", 21474)
print(result)
result = sdk.cache.read_keys(['franek', "gruby:p4"])
print(result)
