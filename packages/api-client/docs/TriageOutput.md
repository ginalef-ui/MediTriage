
# TriageOutput


## Properties

Name | Type
------------ | -------------
`id` | string
`pacienterut` | string
`esiLevel` | number
`status` | string
`fecha` | Date

## Example

```typescript
import type { TriageOutput } from ''

// TODO: Update the object below with actual values
const example = {
  "id": null,
  "pacienterut": null,
  "esiLevel": null,
  "status": null,
  "fecha": null,
} satisfies TriageOutput

console.log(example)

// Convert the instance to a JSON string
const exampleJSON: string = JSON.stringify(example)
console.log(exampleJSON)

// Parse the JSON string back to an object
const exampleParsed = JSON.parse(exampleJSON) as TriageOutput
console.log(exampleParsed)
```

[[Back to top]](#) [[Back to API list]](../README.md#api-endpoints) [[Back to Model list]](../README.md#models) [[Back to README]](../README.md)


