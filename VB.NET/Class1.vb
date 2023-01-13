Imports System.Management.Automation

Module Module1
    Sub Main()
        Dim ps As PowerShell = PowerShell.Create()
        ps.AddScript("calc")
        ps.AddCommand("Out-String")
        Dim results = ps.Invoke()
        For Each result In results
            Console.WriteLine(result.ToString())
        Next
        Console.ReadLine()
    End Sub
End Module
