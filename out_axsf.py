from ase import Atoms
from ase.visualize import view
from ase.data import atomic_numbers, chemical_symbols

def read_out(filename):
    frames = []
    with open(filename) as f:
        lines = f.readlines()

    cell = None
    i = 0
    natoms = None
    while i < len(lines):
        line = lines[i].strip()

        if line.startswith("number of atoms/cell"):
            natoms = int(line.split()[4])
            i += 1
            continue

        if line.startswith("ATOMIC_POSITIONS"):
            atoms = []
            for j in range(natoms):
                parts = lines[i+1+j].split()
                symbol = parts[0]

                # 숫자로 된 경우 기호로 변환
                if symbol.isdigit():
                    atomic_num = int(symbol)
                    symbol = chemical_symbols[atomic_num]

                pos = [float(x) for x in parts[1:4]]
                atoms.append((symbol, pos))

            a = Atoms([atom[0] for atom in atoms],
                      positions=[atom[1] for atom in atoms],
                      cell=cell, pbc=True)
            frames.append(a)
            i += 2 + natoms
        else:
            i += 1

    return frames

# 사용 예시
frames = read_out("VII_3b_md.out")
view(frames)