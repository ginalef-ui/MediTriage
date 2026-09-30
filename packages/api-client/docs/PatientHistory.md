
# PatientHistory


## Properties

Name | Type
------------ | -------------
`patientId` | string
`records` | [Array&lt;TriageOutput&gt;](TriageOutput.md)

## Example

```typescript
import type { PatientHistory } from ''

// TODO: Update the object below with actual values
const example = {
  "patientId": null,
  "records": null,
} satisfies PatientHistory

console.log(example)

// Convert the instance to a JSON string
const exampleJSON: string = JSON.stringify(example)
console.log(exampleJSON)

// Parse the JSON string back to an object
const exampleParsed = JSON.parse(exampleJSON) as PatientHistory
console.log(exampleParsed)
```

[[Back to top]](#) [[Back to API list]](../README.md#api-endpoints) [[Back to Model list]](../README.md#models) [[Back to README]](../README.md)


