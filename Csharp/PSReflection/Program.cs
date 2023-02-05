// Author: Lee Christensen
// License: BSD 3-Clause

using System;
using System.Diagnostics;
using System.IO;
using System.Linq;
using System.Reflection;
using System.Runtime.InteropServices;
using System.Text;

namespace RandomCSharp
{
    public class Program
    {
        public static MethodInfo GetMethod(MethodInfo[] methods, string Name)
        {
            foreach (var method in methods)
            {
                if (method.Name == Name)
                {
                    return method;
                }
            }
            return null;
        }
        [DllImport("kernel32")]
        public static extern IntPtr GetProcAddress(IntPtr hModule, string procName);
        [DllImport("kernel32")]
        public static extern IntPtr LoadLibrary(string name);
        
        public static void Main()
        {

            Console.WriteLine("PID: " + Process.GetCurrentProcess().Id);
            string command = @"[System.Reflection.Assembly]::LoadWithPartialName('System.Windows.Forms'); [System.Windows.Forms.MessageBox]::Show('Pop pop!');";

            byte[] AutomationDllByets = File.ReadAllBytes(@"1.bin");
            var AutomationAssembly = Assembly.Load(AutomationDllByets);

            Type PowerShellClassType = AutomationAssembly.GetType("System.Management.Automation.PowerShell");
            var PublicStaticMethods = PowerShellClassType.GetMethods((BindingFlags.Public | BindingFlags.Static));
            var PublicMethods = PowerShellClassType.GetMethods((BindingFlags.Public | BindingFlags.Instance));

            var CreateMethod = GetMethod(PublicStaticMethods, "Create");
            var AddScriptMethod = GetMethod(PublicMethods, "AddScript");
            var InvokeMethod = GetMethod(PublicMethods, "Invoke");

            var PowerShellInstance = CreateMethod.Invoke(PowerShellClassType, new object[] { });

            AddScriptMethod.Invoke(PowerShellInstance, new object[] { command });
            InvokeMethod.Invoke(PowerShellInstance, new object[] { });
        }
    }
}
