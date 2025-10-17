"""
TFLite to ONNX converter using tflite2onnx library.

This script converts a TensorFlow Lite model to ONNX format.
Note: tf.py_function approach doesn't work because EagerPyFunc is not supported in ONNX.
      We need to use a dedicated TFLite to ONNX converter instead.
"""

try:
    from tflite2onnx import convert
    print("Using tflite2onnx library for conversion")
    
    # Path to the TFLite model
    tflite_model_path = "models/hand_landmark_full.tflite"
    onnx_model_path = "models/hand_landmark_full.onnx"
    
    # Convert TFLite model to ONNX
    print(f"Converting {tflite_model_path} to ONNX...")
    onnx_model = convert(tflite_model_path, onnx_model_path)
    
    print(f"✓ Model successfully converted and saved to {onnx_model_path}")
    
    # Verify the converted model
    import onnx
    model = onnx.load(onnx_model_path)
    print(f"\n=== Model Info ===")
    print(f"IR version: {model.ir_version}")
    print(f"Producer: {model.producer_name}")
    print(f"Number of nodes: {len(model.graph.node)}")
    print(f"\nInput:")
    for inp in model.graph.input:
        shape = [dim.dim_value for dim in inp.type.tensor_type.shape.dim]
        print(f"  - {inp.name}: {shape}")
    print(f"\nOutput:")
    for out in model.graph.output:
        shape = [dim.dim_value for dim in out.type.tensor_type.shape.dim]
        print(f"  - {out.name}: {shape}")
    
except ImportError:
    print("\n❌ tflite2onnx library is not installed.")
    print("\nPlease install it using:")
    print("  pip install tflite2onnx")
    print("\nAlternatively, you can try:")
    print("  pip install tf2onnx onnx-tf")
    exit(1)
except Exception as e:
    print(f"\n❌ Conversion failed: {e}")
    print("\n=== Troubleshooting ===")
    print("TFLite to ONNX conversion can be challenging. Here are some alternatives:")
    print("1. Use tflite2onnx: pip install tflite2onnx")
    print("2. Use ai-edge-torch if the original model is PyTorch")
    print("3. Re-export from the original framework (TensorFlow/PyTorch) to ONNX directly")
    exit(1)
