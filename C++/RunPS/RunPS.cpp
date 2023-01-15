#include "pch.h"
#using <System.dll>
#using <C:\Windows\Microsoft.NET\assembly\GAC_MSIL\System.Management.Automation\v4.0_3.0.0.0__31bf3856ad364e35\System.Management.Automation.dll>
#using <C:\Windows\Microsoft.NET\assembly\GAC_MSIL\System.Collections\v4.0_4.0.0.0__b03f5f7f11d50a3a\System.Collections.dll>

using namespace System;
using namespace System::Collections::ObjectModel;
using namespace System::Management::Automation;
using namespace System::Management::Automation::Runspaces;

int main(array<System::String^>^ args)
{
    try
    {
        Runspace^ runspace = RunspaceFactory::CreateRunspace();
        runspace->Open();
        Pipeline^ pipeline = runspace->CreatePipeline();
        pipeline->Commands->AddScript("& {calc}");
        Collection<PSObject^>^ results = pipeline->Invoke();

        for each (PSObject ^ result in results)
        {
            Console::WriteLine("Name: {0}", result->Properties["Name"]->Value);
            Console::WriteLine("ID: {0}", result->Properties["Id"]->Value);
        }
        //关闭空间运行
        runspace->Close();
    }
    catch (Exception^ e)
    {
        Console::WriteLine("Error: {0}", e->Message);
    }

    return 0;
}
