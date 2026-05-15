#!/usr/bin/env python3
"""Fix init.c hunk #3 reject from ksun SUSFS combined patch.

The patch was built against an older KSU-Next without allow_shell.
Newer KSU-Next (f08381731+) added allow_shell between ksu_late_loaded
and kernelsu_init(), breaking patch context matching.

This removes what hunk #3 would have removed:
  - bool ksu_late_loaded;
  - #if defined(__x86_64__) ... #endif
  - #ifdef MODULE ... ksu_late_loaded ... #endif
"""
import re, sys, os

path = sys.argv[1] if len(sys.argv) > 1 else 'kernel/core/init.c'

if not os.path.exists(path):
    print(f"SKIP: {path} not found (already fixed or wrong cwd)")
    sys.exit(0)

with open(path) as f:
    c = f.read()

original = c
c = re.sub(r'bool ksu_late_loaded;\s*\n', '', c)
c = re.sub(r'#if defined\(__x86_64__\).*?#endif\s*\n', '', c, flags=re.DOTALL)
c = re.sub(r'#ifdef MODULE\s*\n\s*ksu_late_loaded.*?#endif\s*\n', '', c, flags=re.DOTALL)

if c != original:
    with open(path, 'w') as f:
        f.write(c)
    print(f"Fixed {path}: removed ksu_late_loaded, x86_64 check, late_loaded init")
else:
    print(f"SKIP: {path} already clean (no changes needed)")
