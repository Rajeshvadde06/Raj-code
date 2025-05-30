import re
import os

def generate_testbench(verilog_file):
    with open(verilog_file, 'r') as file:
        code = file.read()

    # Extract module name
    module_name = re.search(r'module\s+(\w+)', code).group(1)

    # Extract ports
    ports = re.findall(r'(input|output|inout)\s+(?:\[.*?\]\s*)?(\w+)', code)

    inputs = [name for direction, name in ports if direction == 'input']
    outputs = [name for direction, name in ports if direction == 'output']

    tb_name = f"{module_name}_tb"
    tb_filename = f"{tb_name}.v"

    with open(tb_filename, 'w') as tb:
        tb.write(f"module {tb_name};\n\n")
        for i in inputs:
            tb.write(f"    reg {i};\n")
        for o in outputs:
            tb.write(f"    wire {o};\n")

        tb.write(f"\n    {module_name} uut (\n")
        for port in inputs + outputs:
            tb.write(f"        .{port}({port}),\n")
        tb.write(f"    );\n\n")

        tb.write("    initial begin\n")
        tb.write('        $display("' + " ".join(inputs + outputs) + '");\n')
        tb.write('        $monitor("' + " ".join(['%b']*len(inputs + outputs)) +
                 '", ' + ", ".join(inputs + outputs) + ');\n\n')

        for i in range(4):
            for var in inputs:
                tb.write(f"        {var} = {i % 2};\n")
            tb.write("        #10;\n")

        tb.write("        $finish;\n")
        tb.write("    end\n\nendmodule\n")

    print(f"✅ Testbench generated: {tb_filename}")


# 🔹 Example Usage:
generate_testbench("mux3to1.v.txt")
