# Best Practice Analyzer integration

The local checker is not a BPA engine and does not evaluate Dynamic LINQ. The
repository's examples/bpa/metadata-rules.json contains two independently authored
rule examples. They require validation in your installed Tabular Editor version.
Static META101/META102 findings are not evidence that these BPA expressions ran.

TE2's documented command-line analyzer can inspect a compatible BIM file:

```powershell
& 'C:\Tools\TabularEditor\TabularEditor.exe' '.\model.bim' -A '.\metadata-rules.json' -V
```

Run against a local disposable model, inspect console warnings and exit status,
and retain results. This is a documented command example, not an integration test.
Do not pass a TMDL directory to TE2 on the assumption it supports that format.
Do not use deployment, script-fix, or save flags for a read-only audit.

- [TE2 CLI](https://docs.tabulareditor.com/te2/Command-line-Options.html)
- [BPA rule authoring](https://docs.tabulareditor.com/te2/Best-Practice-Analyzer.html)
