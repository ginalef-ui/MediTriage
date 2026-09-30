# DefaultApi

All URIs are relative to *https://api.meditriage.cl/v1*

| Method | HTTP request | Description |
|------------- | ------------- | -------------|
| [**createTriageRecord**](DefaultApi.md#createtriagerecord) | **POST** /triage | Registrar síntomas del paciente (US-01) |
| [**createUser**](DefaultApi.md#createuseroperation) | **POST** /admin/users | Gestión de usuarios y permisos (US-05) |
| [**getAuditLogs**](DefaultApi.md#getauditlogs) | **GET** /audit/logs | Auditoría de registros clínicos (US-04) |
| [**getPatientHistory**](DefaultApi.md#getpatienthistory) | **GET** /patients/{patientId}/history | Consultar historial clínico (US-03) |
| [**getTriageQueue**](DefaultApi.md#gettriagequeue) | **GET** /triage/queue | Visualizar cola de prioridad de pacientes (US-02) |



## createTriageRecord

> TriageOutput createTriageRecord(idempotencyKey, triageInput)

Registrar síntomas del paciente (US-01)

### Example

```ts
import {
  Configuration,
  DefaultApi,
} from '';
import type { CreateTriageRecordRequest } from '';

async function example() {
  console.log("🚀 Testing  SDK...");
  const config = new Configuration({ 
    // Configure HTTP bearer authorization: BearerAuth
    accessToken: "YOUR BEARER TOKEN",
  });
  const api = new DefaultApi(config);

  const body = {
    // string
    idempotencyKey: 38400000-8cf0-11bd-b23e-10b96e4ef00d,
    // TriageInput
    triageInput: ...,
  } satisfies CreateTriageRecordRequest;

  try {
    const data = await api.createTriageRecord(body);
    console.log(data);
  } catch (error) {
    console.error(error);
  }
}

// Run the test
example().catch(console.error);
```

### Parameters


| Name | Type | Description  | Notes |
|------------- | ------------- | ------------- | -------------|
| **idempotencyKey** | `string` |  | [Defaults to `undefined`] |
| **triageInput** | [TriageInput](TriageInput.md) |  | |

### Return type

[**TriageOutput**](TriageOutput.md)

### Authorization

[BearerAuth](../README.md#BearerAuth)

### HTTP request headers

- **Content-Type**: `application/json`
- **Accept**: `application/json`


### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
| **201** | Registro creado exitosamente |  -  |
| **422** | Error de validación |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#api-endpoints) [[Back to Model list]](../README.md#models) [[Back to README]](../README.md)


## createUser

> createUser(createUserRequest)

Gestión de usuarios y permisos (US-05)

### Example

```ts
import {
  Configuration,
  DefaultApi,
} from '';
import type { CreateUserOperationRequest } from '';

async function example() {
  console.log("🚀 Testing  SDK...");
  const config = new Configuration({ 
    // Configure HTTP bearer authorization: BearerAuth
    accessToken: "YOUR BEARER TOKEN",
  });
  const api = new DefaultApi(config);

  const body = {
    // CreateUserRequest
    createUserRequest: ...,
  } satisfies CreateUserOperationRequest;

  try {
    const data = await api.createUser(body);
    console.log(data);
  } catch (error) {
    console.error(error);
  }
}

// Run the test
example().catch(console.error);
```

### Parameters


| Name | Type | Description  | Notes |
|------------- | ------------- | ------------- | -------------|
| **createUserRequest** | [CreateUserRequest](CreateUserRequest.md) |  | |

### Return type

`void` (Empty response body)

### Authorization

[BearerAuth](../README.md#BearerAuth)

### HTTP request headers

- **Content-Type**: `application/json`
- **Accept**: Not defined


### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
| **201** | Usuario creado exitosamente |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#api-endpoints) [[Back to Model list]](../README.md#models) [[Back to README]](../README.md)


## getAuditLogs

> Array&lt;object&gt; getAuditLogs()

Auditoría de registros clínicos (US-04)

### Example

```ts
import {
  Configuration,
  DefaultApi,
} from '';
import type { GetAuditLogsRequest } from '';

async function example() {
  console.log("🚀 Testing  SDK...");
  const config = new Configuration({ 
    // Configure HTTP bearer authorization: BearerAuth
    accessToken: "YOUR BEARER TOKEN",
  });
  const api = new DefaultApi(config);

  try {
    const data = await api.getAuditLogs();
    console.log(data);
  } catch (error) {
    console.error(error);
  }
}

// Run the test
example().catch(console.error);
```

### Parameters

This endpoint does not need any parameter.

### Return type

**Array<object>**

### Authorization

[BearerAuth](../README.md#BearerAuth)

### HTTP request headers

- **Content-Type**: Not defined
- **Accept**: `application/json`


### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
| **200** | Registros inmutables de Azure SQL Ledger |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#api-endpoints) [[Back to Model list]](../README.md#models) [[Back to README]](../README.md)


## getPatientHistory

> PatientHistory getPatientHistory(patientId)

Consultar historial clínico (US-03)

### Example

```ts
import {
  Configuration,
  DefaultApi,
} from '';
import type { GetPatientHistoryRequest } from '';

async function example() {
  console.log("🚀 Testing  SDK...");
  const config = new Configuration({ 
    // Configure HTTP bearer authorization: BearerAuth
    accessToken: "YOUR BEARER TOKEN",
  });
  const api = new DefaultApi(config);

  const body = {
    // string
    patientId: patientId_example,
  } satisfies GetPatientHistoryRequest;

  try {
    const data = await api.getPatientHistory(body);
    console.log(data);
  } catch (error) {
    console.error(error);
  }
}

// Run the test
example().catch(console.error);
```

### Parameters


| Name | Type | Description  | Notes |
|------------- | ------------- | ------------- | -------------|
| **patientId** | `string` |  | [Defaults to `undefined`] |

### Return type

[**PatientHistory**](PatientHistory.md)

### Authorization

[BearerAuth](../README.md#BearerAuth)

### HTTP request headers

- **Content-Type**: Not defined
- **Accept**: `application/json`


### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
| **200** | Historial clínico del paciente |  -  |
| **404** | Paciente no encontrado |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#api-endpoints) [[Back to Model list]](../README.md#models) [[Back to README]](../README.md)


## getTriageQueue

> Array&lt;TriageOutput&gt; getTriageQueue()

Visualizar cola de prioridad de pacientes (US-02)

### Example

```ts
import {
  Configuration,
  DefaultApi,
} from '';
import type { GetTriageQueueRequest } from '';

async function example() {
  console.log("🚀 Testing  SDK...");
  const config = new Configuration({ 
    // Configure HTTP bearer authorization: BearerAuth
    accessToken: "YOUR BEARER TOKEN",
  });
  const api = new DefaultApi(config);

  try {
    const data = await api.getTriageQueue();
    console.log(data);
  } catch (error) {
    console.error(error);
  }
}

// Run the test
example().catch(console.error);
```

### Parameters

This endpoint does not need any parameter.

### Return type

[**Array&lt;TriageOutput&gt;**](TriageOutput.md)

### Authorization

[BearerAuth](../README.md#BearerAuth)

### HTTP request headers

- **Content-Type**: Not defined
- **Accept**: `application/json`


### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
| **200** | Lista de pacientes priorizados |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#api-endpoints) [[Back to Model list]](../README.md#models) [[Back to README]](../README.md)

