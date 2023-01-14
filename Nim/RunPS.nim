import winim/clr
import sugar

import base64
let m = decode("U3lzdGVtLk1hbmFnZW1lbnQuQXV0b21hdGlvbg==")
var Automation = load(m)
dump Automation
let k = decode("U3lzdGVtLk1hbmFnZW1lbnQuQXV0b21hdGlvbi5SdW5zcGFjZXMuUnVuc3BhY2VGYWN0b3J5")
var RunspaceFactory = Automation.GetType(k)
dump RunspaceFactory

var runspace = @RunspaceFactory.CreateRunspace()
dump runspace
runspace.Open()

var pipeline = runspace.CreatePipeline()
dump pipeline
pipeline.Commands.AddScript("Get-Process")
pipeline.Commands.Add("Out-String")

var results = pipeline.Invoke()

for i in countUp(0, results.Count()-1):
    echo results.Item(i)

dump results
echo results.isType()
var t = results.GetType()
dump t
discard readLine(stdin)
echo t.isType()
echo t.unwrap.vt
runspace.Close()