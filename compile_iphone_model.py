"""Compile iPhone model library on Linux (no iOS SDK needed for this part)."""
import json
import sys
from pathlib import Path

# Compat shim: mlc_llm 0.26.dev6 expects tvm.tirx.is_buffer_var, which is missing
# from mlc-ai 0.26.dev246. Implement it based on usage in mlc_llm.
import tvm.tirx as tirx

def _is_buffer_var(param):
    """Check if a PrimFunc param is a buffer (vs a scalar var)."""
    # In tirx, buffer params are tirx.Buffer objects; scalar params are tirx.Var
    return isinstance(param, tirx.Buffer)

if not hasattr(tirx, 'is_buffer_var'):
    tirx.is_buffer_var = _is_buffer_var
    print("Applied is_buffer_var compat shim", flush=True)

from mlc_llm.interface.package import build_model_library, validate_model_lib

def main():
    package_config_path = Path(sys.argv[1])
    output = Path(sys.argv[2])
    
    with open(package_config_path) as f:
        package_config = json.load(f)
    
    device = package_config["device"]
    assert device == "iphone", f"Expected iphone, got {device}"
    
    bundle_dir = output / "bundle"
    app_config_path = bundle_dir / "mlc-app-config.json"
    
    # Step 1: Download model + JIT compile for iPhone (produces .tar)
    model_lib_map = build_model_library(package_config, device, bundle_dir, app_config_path)
    print(f"Model libs: {model_lib_map}", flush=True)
    
    # Step 2: Create libmodel_iphone.a from the TARs
    validate_model_lib(app_config_path, package_config_path, model_lib_map, device, output)
    print(f"Done. Output in {output}", flush=True)
    print(f"  bundle: {list((output/'bundle').iterdir())}", flush=True)
    print(f"  lib: {list((output/'lib').iterdir())}", flush=True)

if __name__ == "__main__":
    main()
