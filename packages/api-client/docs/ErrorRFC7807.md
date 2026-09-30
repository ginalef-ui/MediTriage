
# ErrorRFC7807


## Properties

Name | Type
------------ | -------------
`type` | string
`titulo` | string
`estatus` | number
`detalles` | string
`instancias` | string
`traceId` | string

## Example

```typescript
import type { ErrorRFC7807 } from ''

// TODO: Update the object below with actual values
const example = {
  "type": null,
  "titulo": null,
  "estatus": null,
  "detalles": null,
  "instancias": null,
  "traceId": null,
} satisfies ErrorRFC7807

console.log(example)

// Convert the instance to a JSON string
const exampleJSON: string = JSON.stringify(example)
console.log(exampleJSON)

// Parse the JSON string back to an object
const exampleParsed = JSON.parse(exampleJSON) as ErrorRFC7807
console.log(exampleParsed)
```

[[Back to top]](#) [[Back to API list]](../README.md#api-endpoints) [[Back to Model list]](../README.md#models) [[Back to README]](../README.md)


