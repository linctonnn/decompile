import re

def mips_to_c(asm_lines):
    c_lines = []

    for line in asm_lines:
        match = re.match(r'0x[0-9a-f]+:\s+(\w+)\s+(.*)', line)
        if not match:
            continue

        instr, args = match.groups()
        args = args.replace(',', '').split()

        if instr == 'bnez':
            c_lines.append(f"if ({args[0]} != 0) goto LABEL_{args[1]};")
        elif instr == 'beqz':
            c_lines.append(f"if ({args[0]} == 0) goto LABEL_{args[1]};")
        elif instr == 'addiu':
            c_lines.append(f"{args[0]} = {args[1]} + {args[2]};")
        elif instr == 'move':
            c_lines.append(f"{args[0]} = {args[1]};")
        elif instr == 'sw':
            c_lines.append(f"*({args[1]}) = {args[0]};")
        elif instr == 'lw':
            c_lines.append(f"{args[0]} = *({args[1]});")
        elif instr == 'jr' and args[0] == '$ra':
            c_lines.append("return;")
        elif instr == 'nop':
            c_lines.append("// nop")
        elif instr == "bne":
            c_lines.append(f"if ({args[0]} != {args[1]}) goto LABEL_{args[2]};")
        elif instr == "addu":
            c_lines.append(f"{args[0]} = {args[1]} + {args[2]};")
        elif instr == "jal":
            c_lines.append(f"{args[0]}();")
        else:
            c_lines.append(f"// {instr} {' '.join(args)}")

    return c_lines

with open("disasm_output.txt") as f:
    asm_lines = f.readlines()

pseudo_c = mips_to_c(asm_lines)

with open("output_pseudocode.c", "w") as f:
    for line in pseudo_c:
        f.write(line + "\n")

print("Pseudocode saved to output_pseudocode.c")
