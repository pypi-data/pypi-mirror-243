An SDMX mapping utility to generate partial key maps for referential metadata.
Although not designed to do that, data mappings are also possible.
The package is structured in such a way that it can be used as a package without the FASTAPI overhead.

Three methods are available:
- *map_withFile* GET method (receiving the mapping source and mapping rules both as file references)
- *map_withURN* GET method (receiving the mapping source  as file and the mapping rules as SDMX registry endpoint + mapping ID)
- *map_json_withURN* POST method (receiving the mapping source as the body of the request in json - pandas dataframe dictionary style - and mapping rules as SDMX registry endpoint + mapping ID) (added in version 0.1.1)

A typical usage example in package mode:

```python
    from mappings_utility.sdmx_mapping_utility import SDMXMappingUtility 
    
    mf = Path('to-mapping-artefacts.xml')
    sf = Path('to-file-to-be-mapped.csv')
    mu = SDMXMappingUtility.initialise_with_file(mf, sf, sid_based=False)
    df = mu.generate_mappings_partial_keys(
        includeSourceColumns=False,
        includeAttributesMeasures=False,
        nulledFixedTargets=True,
        writeTargetStructInfo=False,
        dropInvalid=False,
        sid_based=False
        )
    df.to_csv(Path('mapped-file.csv'), index=False)
```
The parameters fine-tune the output file:
- includeSourceColumns: True/False; when set to True the resulting file would include the fields of the source csv file  
- includeAttributesMeasures: True/False; when True it will include the attribute columns and obs_value, otherwise it will suppress those from the output (this is needed for referential metadata partial key mappings)
- nulledFixedTargets: True/False, when True fixed values in the target mapping will be set to Null, also a partial-key mapping motivated feature
- writeTargetStructInfo: True/False, when True it adds or maps columns necessary for the output to be SDMX-CSV compliant
- dropInvalid: True/False, when set to True the output only contains valid mappings (although validity checks are lazy), invalid rows are ommitted; with False the returned dataframe will contain cells with a special string highlighting the positions where the target value could not be determined
- sid_based: True/False, when set to True the resulting file will contain a Series ID (SID) field with the dimensions of the target data model dot-concatenated