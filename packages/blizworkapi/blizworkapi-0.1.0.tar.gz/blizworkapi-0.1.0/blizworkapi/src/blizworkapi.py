from enum import Enum
import os
from dataclasses import dataclass
from requests import post
from pprint import pprint


@dataclass
class BlizWorkCallResponse:
    http_status: int
    blizwork_status: int
    message: str
    payload: any

    def is_ok(self):
        return self.http_status == 200 and self.blizwork_status == 0


class CaseDataLevel(Enum):
    '''Case data level'''
    CASE_ONLY = 0
    PLUS_USER_INFO = 1
    PLUS_CASE_HISTORY = 2
    PLUS_PROCESS_DEFINITION = 3
    PLUS_COMPANY_INFO = 4


API_BASE_URI = 'https://api.blizwork.com'  # Must NOT end with '/'
API_BASE_URI_STAGE = 'http://apì_stage.blizwork.com'
API_BASE_URI_DEV = 'http://localhost:3005'
OMIT_TOKEN = True


class BlizWorkAPIInstance:
    token: str = ''          # Valid BlizWork API token.
    userId: str = ''         # Authorized BlizWork user.

    def __init__(self, token: str, userId: str):
        self.token: str = token
        self.userId: str = userId
        self.last_response: BlizWorkCallResponse = None
        self.unforce_environment()

    def force_environment(self, environment: str):
        self.set_force_environment = True
        self.forced_environment = environment

    def unforce_environment(self):
        self.set_force_environment = False
        self.forced_environment = None

    def get_environment(self) -> str:
        if self.set_force_environment:
            environment = self.forced_environment
        else:
            environment = os.environ.get('NODE_ENV', 'development')
        return environment.lower()

    def get_uri(self, uri: str, omit_token: bool = False) -> str:
        uri = uri.strip()
        if len(uri) == 0:
            raise ValueError('Empty URI')
        if not uri.startswith('/'):
            uri = '/' + uri
        if not uri.endswith('/'):
            uri += '/'
        base_uri = API_BASE_URI
        if omit_token:
            full_uri = f'{base_uri}{uri}'
        else:
            full_uri = f"{base_uri}{uri}{self.token}/"
        return full_uri

    def get_utils_uri(self, operation: str, omit_token: bool = False) -> str:
        return self.get_uri(f'utils/{operation}', omit_token)

    def get_call_validation_uri(self, handshake_token) -> str:
        return self.get_utils_uri(f'validatecall/{handshake_token}')

    def get_upload_file_uri(self) -> str:
        return self.get_uri('attachment/upload')

    def get_process_uri(self, operation: str) -> str:
        return self.get_uri(f'process/{operation}')

    def get_process_caselist_uri(self) -> str:
        return self.get_process_uri('case-list')

    def get_process_casedata_uri(self) -> str:
        return self.get_process_uri('case')

    def get_case_uri(self, operation: str) -> str:
        return self.get_uri(f'/{operation}')

    def get_case_exec_uri(self) -> str:
        return self.get_case_uri('exec')

    def get_masterdata_uri(self, operation: str) -> str:
        return self.get_uri(f'master-data/{operation}')

    def get_masterdata_query_uri(self) -> str:
        return self.get_masterdata_uri('')

    def get_masterdata_upsert_uri(self) -> str:
        return self.get_masterdata_uri('upsert')

    def get_masterdata_delete_uri(self) -> str:
        return self.get_masterdata_uri('delete')

    def get_base_payload(self) -> dict:
        return {
            "userId": self.userId,
            "environment": 'production' if self.get_environment() == 'production' else 'draft'
        }

    def post(self, uri: str, payload: dict) -> BlizWorkCallResponse:
        os_environment = os.environ.get('NODE_ENV', 'development')
        if os_environment == 'development':
            pprint(f'POST {uri}')
            pprint(payload)
        r = post(uri, json=payload)
        if os_environment == 'development':
            pprint(f'{r.status_code}')
        if r.status_code < 200 or r.status_code > 299:
            call_response = BlizWorkCallResponse(
                http_status=r.status_code,
                blizwork_status=0,
                message=r.reason,
                payload=r.text)
        else:
            bw_response = r.json()
            rc = bw_response.get('resultCode', bw_response.get('status', 0))
            msg = bw_response.get(
                'resultMessage', bw_response.get('message', ''))
            call_response = BlizWorkCallResponse(
                http_status=r.status_code,
                blizwork_status=rc,
                message=msg,
                payload=bw_response.get('payload', None))
        self.last_response = call_response
        return call_response


class BlizWorkUtils:
    '''Encapsulates BlizWork Utils'''
    bw_api: BlizWorkAPIInstance = None

    def __init__(self, bw_api_instance: BlizWorkAPIInstance):
        self.bw_api = bw_api_instance

    def validate_call(self, post_payload) -> BlizWorkCallResponse:
        env: str = post_payload.get('environment', 'draft')
        if env == 'draft':
            return BlizWorkCallResponse(
                http_status=200,
                blizwork_status=0,
                message='OK',
                payload={})
        hsToken: str = post_payload.get('handshakeToken', '')
        if hsToken == '':
            raise ValueError('Missing hsToken')
        return self.bw_api.post(self.bw_api.get_call_validation_uri(hsToken), {})

    def get_field_from_call(self, post_payload: dict, field_name: str, default: any = None) -> any:
        fields = post_payload.get('fields', None)
        if fields is None:
            raise ValueError('Missing fields in payload')
        if default is None:
            return fields[field_name]
        else:
            return fields.get(field_name, default)

    def upload_file(self, userId: str, file_name: str, file_content: bytes) -> BlizWorkCallResponse:
        payload = {
            'userId': userId,
            'module': 'form',
            'filename': file_name,
            'file': file_content
        }
        return self.bw_api.post(self.bw_api.get_upload_file_uri(), payload)


class BlizWorkProcess:
    '''Encapsulates a BlizWork process'''
    bw_api: BlizWorkAPIInstance = None
    processId: str = ''

    def __init__(self, bw_api_instance: BlizWorkAPIInstance, processId: str):
        self.bw_api = bw_api_instance
        self.processId = processId

    def get_base_payload(self) -> dict:
        return self.bw_api.get_base_payload() | {
            'processId': self.processId
        }

    def case_summary_list(self, filter: object) -> []:
        payload = self.get_base_payload() | {
            'filter': filter
        }
        return self.bw_api.post(self.bw_api.get_process_caselist_uri(), payload)

    def case(self, case_number: int, from_draft: bool = False, additional_info: int = 0) -> dict:
        payload = self.get_base_payload() | {
            'processId': self.processId,
            'caseNumber': case_number,
            'include': additional_info,
            'environment': 'draft' if from_draft else 'production'
        }
        return self.bw_api.post(self.bw_api.get_process_casedata_uri(), payload)

    def get_case(self, case_number: int, from_draft: bool = False, additional_info: int = 0) -> 'BlizWorkCase':
        case_response = self.case(case_number, from_draft, additional_info)
        if case_response.is_ok():
            return BlizWorkCase(case_response.payload, self, additional_info)
        else:
            raise RuntimeError(
                f'Case {self.processId} #{case_number} not found in {"draft" if from_draft else "production"}: {case_response.message}')

    def get_case_from_draft(self, case_number: int, additional_info: int = 0) -> dict:
        return self.get_case(case_number, True, additional_info)

    def get_case_from_production(self, case_number: int, additional_info: int = 0) -> dict:
        return self.get_case(case_number, False, additional_info)


class BlizWorkCase:
    '''Encapsulates a BlizWork process case'''
    case_document = None

    def __init__(self, case_state: dict, parent_process: BlizWorkProcess = None, info_level: int = 0):
        if not bool(case_state):
            raise ValueError('Case state cannot be {}')
        self.case_document = case_state
        self.parent_process = parent_process
        self.info_level = info_level

    def companyId(self):
        return self.case_document['companyId']

    def environment(self):
        return self.case_document['environment']

    def process(self):
        return self.case_document['processSlug']

    def version(self):
        return self.case_document['processVersion']

    def number(self):
        return self.case_document['caseNumber']

    def initiator(self):
        if (self.case_document.get('history', None) is not None) and (len(self.case_document['history']) > 0):
            return self.case_document['history'][0]['updatedBy']
        return self.case_document['createAudit']['user']

    def history(self) -> []:
        return self.case_document.get('history', None)

    def form(self, form_id: str) -> []:
        if self.case_document.get('history', None) is None:
            raise KeyError('Case has no history')
        found_forms = [
            f for f in self.case_document['history'] if f['currentActivity']['formId'] == form_id]
        return found_forms

    def latest_form(self, form_id: str) -> dict:
        form_list = self.form(form_id)
        if len(form_list) > 0:
            return form_list[-1]
        raise RuntimeError(f'Form "{form_id}" not found!')

    def get_form_execution_date(self, form: dict) -> str:
        if form is not None and form != {}:
            return form['updatedOn'][0:10]
        return ''

    def current_form(self) -> dict:
        if self.case_document.get('history', None) is None:
            raise KeyError('Case has no history')
        return self.case_document['history'][-1]

    def get_field_value(self, field_name: str, default: any = None) -> any:
        if default is not None:
            return self.case_document['fields'].get(field_name, default)
        else:
            return self.case_document['fields'][field_name]

    def get_download_url(self, field_name: str) -> any:
        foundFieldValue = [
            entry for entry in self.case_document['fieldValues'] if entry['slug'] == field_name]
        if len(foundFieldValue) > 0:
            return foundFieldValue[0]['fileUrl']
        return None

    def exec(self, action: str, data: dict, skipExtensions: bool = False, companyId: str = None, bw_api: BlizWorkAPIInstance = None) -> 'BlizWorkCase':
        if companyId is None:
            process_def = self.case_document.get('processDefinition', None)
            if process_def is None:
                raise ValueError('Missing processDefinition')
            cId = process_def.get('companyId', None)
            if cId is None:
                raise ValueError('Missing companyId')
        else:
            cId = companyId
        if self.parent_process is None:
            if bw_api is None:
                raise ValueError('Missing BlizWork API instance')
            else:
                api_instance = bw_api
        else:
            api_instance = self.parent_process.bw_api
        payload = api_instance.get_base_payload() | {
            'environment': self.environment(),
            'companyId': cId,
            'workflowId': self.process(),
            'caseNumber': self.number(),
            'formId': self.current_form()['nextActivity']['formId'],
            'nextFormId': action,
            'formData': data,
            'skipExtensions': skipExtensions
        }
        exec_result = api_instance.post(
            api_instance.get_case_exec_uri(), payload)
        if exec_result.is_ok():
            if self.parent_process is not None:
                return self.parent_process.get_case(self.number(), self.environment() == 'draft', self.info_level)
        else:
            raise RuntimeError(
                f'Error executing {self.process()} #{self.number()} in {self.environment()}: {exec_result.message}')


class BlizWorkMasterDataTable:
    '''Encapsulates a BlizWork master data table'''
    bw_api: BlizWorkAPIInstance = None  # API Instance.
    table: str = ''                     # Master data table name.

    def __init__(self, bw_api_instance: BlizWorkAPIInstance, table_name: str):
        self.bw_api = bw_api_instance
        self.table = table_name

    def get_base_payload(self) -> dict:
        return self.bw_api.get_base_payload() | {
            'table': self.table
        }

    def get_records(self, filter: dict) -> BlizWorkCallResponse:
        payload = self.get_base_payload() | {
            'filter': filter
        }
        return self.bw_api.post(self.bw_api.get_masterdata_query_uri(), payload)

    def get_dictionary(self, filter: dict, key: str) -> dict:
        records_response = self.get_records(filter)
        if records_response.is_ok():
            result_dict = {}
            records = records_response.payload
            for rec in records:
                result_dict[rec[key]] = rec
            return result_dict
        raise RuntimeError(records_response.message)

    def upsert(self, filter: dict, update: dict) -> BlizWorkCallResponse:
        payload = self.get_base_payload() | {
            'filter': filter,
            'update': update
        }
        return self.bw_api.post(self.bw_api.get_masterdata_upsert_uri(), payload)

    def delete(self, filter: dict) -> BlizWorkCallResponse:
        payload = self.get_base_payload() | {
            'filter': filter
        }
        return self.bw_api.post(self.bw_api.get_masterdata_delete_uri(), payload)
