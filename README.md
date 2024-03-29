# Ancestry Service (BETA)

Signature-based Assemblyline service that focuses on file genealogy

## Signatures

(BETA) Signatures are defined as service configuration and each signature follows the following format:

```yaml
config:
  signatures:
    exe_from_office_document: # Signature name
      pattern: "document/office/.+,ROOT\\|executable/windows/(?:pe|dll)(?:32|64),EXTRACTED" # Regex pattern
      score: 1000 # Score associated to signature hit
```

Depending on the capabilities we want this service to have, this will be prone change when ready for production.

### What do signatures run on?

The signatures run on temporary information that the Assemblyline Dispatcher passes to the service. As such, for the time being, we've decided to format the data as pairs that include the filetype and it's relation to the parent file, if any, joined by `|`.

For example: A file zip file that has an embedded PE with a RSA certificate will look like:
`document/office/onenote,ROOT|executable/windows/pe64,EXTRACTED|certificate/rsa,EXTRACTED`
