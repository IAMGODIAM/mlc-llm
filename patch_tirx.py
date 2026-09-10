import tvm.tirx, os
p = os.path.join(os.path.dirname(tvm.tirx.__file__), "__init__.py")
with open(p, "a") as f:
    f.write("\n\ndef is_buffer_var(param):\n")
    f.write("    from tvm.tirx import Buffer\n")
    f.write("    return isinstance(param, Buffer)\n")
print("patched", p)
