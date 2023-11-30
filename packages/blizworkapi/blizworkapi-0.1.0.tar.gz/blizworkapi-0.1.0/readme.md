# BlizWork API
This module wraps the HTTP rest-like API for the BlizWork platform.

Detailed method documentation for the API can be found at https://www.blizwork.com/docs

# Developer's Quick Guide
## Tokens
To use this API you will need two tokens and an email:
- The Company Id: This is a unique company identifier. As all of the API methods operate over account processes and activities, this Id defines the context on which each API call is operating. This number can be obtained from the "My Account" ("Mi Cuenta") menu option, in the "Mi Company" ("Mi Empresa").
- The API token: This token is provided by BlizWork. It has an expiration date, ususally it lasts one year. This API token is required as a parameter for every API invocation.
- The email performing the operations.

Both tokens are 34 character alphanumeric strings.

The API token/email used must have privileges to perform the requested operation in the Company with the specified Id. If your performing operations assigned to the "Cutosmer" role, there are no special requirements, but for other roles, the API key/email must have permissions to perform the operation in that Company.

Some methods allow you to specify another user (email) to perform the operation.

## NODE_ENV Environment Variable
The API library will act differently depending on the `NODE_ENV` environment variable value as follows:
- "production": It will perform any operation in the production BlizWork environment. This is the setting you should usually use.
- Any other value: It will try to perform operations in a local instance of the BlizWork API server. You shouldn't use this setting.

## Quick Start
First, you have to create a BlizWorkAPIInstance with a valid API Id. After that, you pass that instance to other task specific instances.

See the code below:
```Python
from BlizWorkAPI import BlizWorkAPIInstance, BlizWorkProcess, CaseDataLevel

bwapi_instance = BlizWorkAPIInstance('abcdef123456789012345678', 'email@company.com')
process = BlizWorkProcess(bwapi_instance, 'my-process')
process_case = process.get_case_from_production(1, CaseDataLevel.PLUS_PROCESS_DEFINITION.value)
some_value = process_case.get_field_value('some_field')
print(f'Field some_field value is {some_value}')
```

You can browse this Python API source code to see which methods from the web API has been implemented.

## Extensions (Web Hook)
If you are implementing an extension, your code will be invoked as a web service using the **POST** method. In the request body you will receive a JSON like the following:
```JSON
{
  "environment": "draft",
  "processId": "sales-process",
  "processVersion": 1,
  "caseNumber": 39,
  "handshakeToken": "642c8f141be17c78c05bcb4c"
}
```

- **environment**: It's 'production' if the extension has been invoked from a published process case. If the invokation comes from a case belonging to a process draft version, it will have the 'draft' value.
- **processId**: It contains the process unique developer-friendly Id. Don't confuse it with the process name, which is a end-user friendly name.
- **processVersion**: It's the process version.
- **caseNumber**: It contains the case number that triggered the invocation.
- **handshakeTok**: It's a one time 24 character Id that can be used to verify it's a valid invocation. This helps to avoid DDoS attacks on your web service by ignoring invications that cannot be validated.

The following code is a sample of how a Extension invocation is handled using Falcon/GUnicorn:
```Python
import BlizWorkAPI as bw

class sample_extension:

    def on_post(self, req, res):
        call = json.load(req.bounded_stream)
        caseNumber = call["caseNumber"]
        environment = call['environment']
        result += f'Processing case {caseNumber} in {environment}.\n'
        bw_api = bw.BlizWorkAPIInstance('abcdef123456789012345678', 'user@company.com')
        bw_utils = bw.BlizWorkUtils(bw_api)
        validcall_test = bw_utils.validate_call(call)
        if not validcall_test.is_ok():
            msg = f'Invalid call: {validcall_test.message}'
            log.error(msg)
            res.status = falcon.HTTP_401
            res.text = msg
            return
        log.info('Valid call.')
            res.text = 'Ok'
            res.status = falcon.HTTP_200

```

## Dependencies
The only external module requirement is the `requests` module which can be installed with the following command:
```Shell
pip install requests
```

If you have installed the default `urllib` nodule version, you may experience an incompatibility error message:
```Shell
ImportError: urllib3 v2.0 only supports OpenSSL 1.1.1+, currently the 'ssl' module is compiled with LibreSSL 2.8.3.
```

To remediate this situation simply upgrade the current `urllib` module with the following command:
```Shell
pip install urllib3==1.26.6
```