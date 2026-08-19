# Input provenance

`database_inputs.sha256` binds the analysis to the processed CSV snapshot in the
unversioned sibling `Nanomem_Devices_Library/DATABASE/` directory. Run
`make inputs-check` before regenerating results.

This manifest is deliberately scoped. It covers the processed tables used by
the principal Chapter 3--5 analyses; it does not hash every raw Keithley file,
spectroscopy trace, lock-in capture, Chapter 2 source file, WESAD subject file,
or PhysioNet record. The raw experimental archive is not distributed with this
repository. Consequently, a matching manifest demonstrates which database
snapshot was used, not independent preservation or public availability of all
underlying measurements.
