#r "System.Management.Automation"
open System.Management.Automation
open System.Management.Automation.Runspaces

let runspace = RunspaceFactory.CreateRunspace()
runspace.Open()

let pipeline = runspace.CreatePipeline()
pipeline.Commands.AddScript("Get-Process")
pipeline.Commands.AddScript("")
pipeline.Commands.AddScript("calc")
let results = pipeline.Invoke()

for result in results do
    printfn "%A" result.Properties

runspace.Close()

//fsc.exe --target:exe --standalone -o RunPS.exe -r:C:\Windows\Microsoft.NET\assembly\GAC_MSIL\System.Management.Automation\v4.0_3.0.0.0__31bf3856ad364e35\System.Management.Automation.dll RunPS.fsx