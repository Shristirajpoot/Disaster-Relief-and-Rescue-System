import numpy as np
import tensorflow as tf
import cv2
from tensorflow.keras.models import load_model

def make_gradcam_heatmap(img_array, model, last_conv_layer_name):
    grad_model = tf.keras.models.Model(
        [model.inputs], [model.get_layer(last_conv_layer_name).output, model.output]
    )

    with tf.GradientTape() as tape:
        conv_outputs, predictions = grad_model(img_arrayac)
        pred_index = tf.argmax(predictions[0])
        loss = predictions[:, pred_index]

    grads = tape.gradient(loss, conv_outputs)
    pooled_grads = tf.reduce_mean(grads, axis=(0, 1, 2))
    conv_outputs = conv_outputs[0]
    heatmap = tf.reduce_mean(conv_outputs * pooled_grads, axis=-1)
    heatmap = tf.maximum(heatmap, 0) / (tf.reduce_max(heatmap) + tf.keras.backend.epsilon())
    return heatmap.numpy()

def generate_gradcam_image(model_path, frame, output_filename):
    """Generates Grad-CAM for a live frame."""
    model = load_model(model_path)
    conv_layers = [layer.name for layer in model.layers if 'conv' in layer.name]
    if not conv_layers:
        print("⚠️ No conv layer found.")
        return
    last_conv_layer = conv_layers[-1]

    img_array = cv2.resize(frame, (224, 224))
    img_array = np.expand_dims(img_array / 255.0, axis=0)

    heatmap = make_gradcam_heatmap(img_array, model, last_conv_layer)
    heatmap = cv2.resize(heatmap, (frame.shape[1], frame.shape[0]))
    heatmap = np.uint8(255 * heatmap)
    heatmap_color = cv2.applyColorMap(heatmap, cv2.COLORMAP_JET)
    superimposed = cv2.addWeighted(frame, 0.6, heatmap_color, 0.4, 0)

    cv2.imwrite(output_filename, superimposed)
    print(f"✅ Grad-CAM saved: {output_filename}")
