import tensorflow as tf
import numpy as np
import onnx
from onnx import helper, TensorProto
import os

# Path to the TFLite model
tflite_model_path = "models/hand_landmark_full.tflite"
onnx_model_path = "models/hand_landmark_full.onnx"

# Load the TFLite model and allocate tensors
interpreter = tf.lite.Interpreter(model_path=tflite_model_path)
interpreter.allocate_tensors()

# Get input and output tensor details
input_details = interpreter.get_input_details()
output_details = interpreter.get_output_details()

print(f"Input details: {input_details}")
print(f"Output details: {output_details}")

# Convert TFLite to SavedModel first (intermediate step)
saved_model_path = "models/hand_landmark_full_saved"

# Create a concrete function from the TFLite interpreter
def inference_fn(input_tensor):
    interpreter.set_tensor(input_details[0]['index'], input_tensor.numpy())
    interpreter.invoke()
    
    outputs = []
    for output_detail in output_details:
        outputs.append(interpreter.get_tensor(output_detail['index']))
    
    if len(outputs) == 1:
        return tf.constant(outputs[0])
    else:
        return tuple(tf.constant(o) for o in outputs)

# Create a wrapper tf.function for the inference
@tf.function(input_signature=[
    tf.TensorSpec(shape=tuple(input_details[0]['shape']), dtype=input_details[0]['dtype'])
])
def inference(input_tensor):
    # Use py_function to wrap the TFLite inference
    return tf.py_function(
        func=lambda x: inference_fn(x),
        inp=[input_tensor],
        Tout=[tf.float32 for _ in output_details]
    )

# Create concrete function and save as SavedModel
concrete_func = inference.get_concrete_function(
    tf.ones(shape=tuple(input_details[0]['shape']), dtype=input_details[0]['dtype'])
)
tf.saved_model.save(concrete_func, saved_model_path)

print(f"Saved model created at {saved_model_path}")

# Now convert SavedModel to ONNX using tf2onnx
import tf2onnx

# Use the updated tf2onnx API - pass the tf.function, not the concrete function
model_proto, _ = tf2onnx.convert.from_function(
    inference,
    input_signature=[
        tf.TensorSpec(shape=tuple(input_details[0]['shape']), dtype=input_details[0]['dtype'])
    ],
    opset=13
)

# Save the ONNX model
with open(onnx_model_path, "wb") as f:
    f.write(model_proto.SerializeToString())

print(f"Model converted and saved to {onnx_model_path}")

# Clean up the temporary SavedModel
import shutil
shutil.rmtree(saved_model_path)
print(f"Cleaned up temporary SavedModel")
