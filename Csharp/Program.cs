using System;
using System.Collections.Generic;
using System.Text;
using System.Management.Automation.Runspaces;
using System.IO;
using System.Management.Automation;

namespace Program
{
    public class Class1
    {


        private static string command = "calc";
        public static StringBuilder StringBuilder = new StringBuilder();
        public static void Main(string[] args)
        {
            //.WriteLine(script);
            RunPS(command);
        }
        public static string RunPS(string commandS)
        {
            Runspace rs = RunspaceFactory.CreateRunspace();
            rs.Open();
            Pipeline pipeline = rs.CreatePipeline();
            pipeline.Commands.AddScript(commandS);

            foreach (PSObject line in pipeline.Invoke())
            {
                StringBuilder.AppendLine(line.ToString());

            }
            rs.Dispose();
            pipeline.Dispose();
            rs.Close();
            return StringBuilder.ToString();
        }
    }
}