from pythonnet import load
load("coreclr")
import sys
import os
import clr

class FormulaInterface:
    def __init__(self):
        process_path = ""
        if sys.platform.startswith("win"):
            # handle windows
            process_path = os.path.expanduser('~') + r'\.dotnet\tools\.store\vuisis.formula.x64\1.0.0\vuisis.formula.x64\1.0.0\tools\net6.0\any\VUISIS.Formula.x64.dll'
        elif sys.platform.startswith("darwin"):
            # handle macos
            if os.uname().machine == 'arm64':
                process_path = os.path.expanduser('~') + r'/.dotnet/tools/.store/vuisis.formula.arm64/1.0.0/vuisis.formula.arm64/1.0.0/tools/net6.0/any/VUISIS.Formula.ARM64.dll'
            else:
                process_path = os.path.expanduser('~') + r'/.dotnet/tools/.store/vuisis.formula.x64/1.0.0/vuisis.formula.x64/1.0.0/tools/net6.0/any/VUISIS.Formula.x64.dll'
        else:
            # handle linux 
            process_path = os.path.expanduser('~') + r'/.dotnet/tools/.store/vuisis.formula/1.0.0/vuisis.formula/1.0.0/tools/net6.0/any/VUISIS.Formula.dll'

        clr.AddReference(process_path)

        from Microsoft.Formula.CommandLine import CommandInterface, CommandLineProgram
        from System.IO import StringWriter
        from System import Console

        sink = CommandLineProgram.ConsoleSink()
        chooser = CommandLineProgram.ConsoleChooser()
        self.ci = CommandInterface(sink, chooser)

        self.sw = StringWriter()
        Console.SetOut(self.sw)
        Console.SetError(self.sw)

        self.run_command("wait on")

        self.run_command("unload *")

    def run_command(self, cmd: str) -> str:
        if not self.ci.DoCommand(cmd):
            raise Exception("Unload command failed.")
        output = self.sw.ToString()
        self.sw.GetStringBuilder().Clear()
        return output
