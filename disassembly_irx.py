from capstone import Cs, CS_ARCH_MIPS, CS_MODE_MIPS32, CS_MODE_LITTLE_ENDIAN

filename = "##"          # Masukkan path file IRX-nya
CODE_OFFSET = 0x800      # biasanya offset .text di IRX

with open(filename, "rb") as f:
    f.seek(CODE_OFFSET)
    code = f.read()

# Inisialisasi capstone untuk MIPS
md = Cs(CS_ARCH_MIPS, CS_MODE_MIPS32 + CS_MODE_LITTLE_ENDIAN)

with open("disasm_output.txt", "w") as out:
    count = 0
    for insn in md.disasm(code, CODE_OFFSET):
        out.write(f"0x{insn.address:08x}:\t{insn.mnemonic:<8}\t{insn.op_str}\n")
        count += 1
        if count >= 10000:
            break

print(f"Disassembly selesai! Saved ke 'disasm_output.txt'.")
