import subprocess, os
from pathlib import Path

vsdevcmd = Path(r'C:\Program Files (x86)\Microsoft Visual Studio\2022\BuildTools\Common7\Tools\VsDevCmd.bat')
cmd_str = f'call "{vsdevcmd}" -no_logo && set'
result = subprocess.run(cmd_str, shell=True, capture_output=True, text=True, errors='replace')
lines = result.stdout.splitlines()
path_lines = [l for l in lines if l.lower().startswith('path=')]
print('Path lines found:', len(path_lines))
if path_lines:
    print('Path[:400]:', path_lines[0][:400])
# Check for cl.exe anywhere in the output
cl_lines = [l for l in lines if 'MSVC' in l and 'x86' in l]
print('MSVC lines:', cl_lines[:3])
