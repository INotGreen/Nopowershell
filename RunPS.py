import os,sys,clr

SMA_Dir = (lambda s: s + os.listdir(s)[0])(r'C:\\Windows\\Microsoft.NET\\assembly\GAC_MSIL\\System.Management.Automation\\')
sys.path.append(SMA_Dir)

clr.AddReference(r"C:\\Windows\\Microsoft.NET\\Framework64\\v4.0.30319\\System.Runtime.dll")
clr.AddReference("System.Management.Automation")
clr.AddReference('System.Collections')
clr.AddReference('System.Management')

from System import Guid
from System.Diagnostics.Eventing import EventProvider
from System.Management.Automation import RunspaceInvoke
from System.Management.Automation.Runspaces import RunspaceFactory
from System.Reflection import BindingFlags
from System.Text import StringBuilder


def run_ps(command):
        runspace = RunspaceFactory.CreateRunspace()
        runspace.Open()
        RunspaceInvoke(runspace)
        pipeline = runspace.CreatePipeline()
        pipeline.Commands.AddScript(command)
        pipeline.Commands.Add("Out-String")
        result = pipeline.Invoke()
        runspace.Close()
        stringBuilder = StringBuilder()
        for each in result:
            stringBuilder.Append(each)
        return stringBuilder.ToString()

if __name__ == '__main__':
   
    command = 'calc'
    output = run_ps(command)
    print(output)
