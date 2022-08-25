__all__ = ['PyPs']
__author__ = "Aslan Gurtsiev"

import os
import sys

import clr

SMA_Dir = (lambda s: s + os.listdir(s)[0])(
    r'C:\Windows\Microsoft.NET\assembly\GAC_MSIL\System.Management.Automation\\')
sys.path.append(SMA_Dir)

clr.AddReference(r"C:\Windows\Microsoft.NET\Framework64\v4.0.30319\System.Runtime.dll")
clr.AddReference("System.Management.Automation")
clr.AddReference('System.Collections')
clr.AddReference('System.Management')

from System import Guid
from System.Diagnostics.Eventing import EventProvider
from System.Management.Automation import RunspaceInvoke
from System.Management.Automation.Runspaces import RunspaceFactory
from System.Reflection import BindingFlags
from System.Text import StringBuilder


class PyPs:
    """This class allows you to run powershell commands from your python code.
    Accepts one parameter: (silent). If set, the script won't leave any traces
    in Powershell logs"""

    def __init__(self, silent=False):

        if silent:
            self._disable_logging()

    def _disable_logging(self):
        """Taken from:
        https://gist.github.com/benpturner/cb49sd37eb7eb3cfc0b6ea03dd00750c8"""

        newrunspace = RunspaceFactory.CreateRunspace()
        psEtwLogProvider = newrunspace.GetType().Assembly.GetType("System.Management.Automation.Tracing.PSEtwLogProvider")
        if psEtwLogProvider:
            etwProvider = psEtwLogProvider.GetField("etwProvider", BindingFlags.NonPublic | BindingFlags.Static)
            eventProvider = EventProvider(Guid.NewGuid())
            etwProvider.SetValue(None, eventProvider)

    @staticmethod
    def run_ps(command: str)   -> str:
        """Runs the powershell command/script"""

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
    # example: Running command "get=process" silently
    command = 'get-process | select-object -property name'
    output = PyPs(True).run_ps(command)
    print(output)
