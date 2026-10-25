import cv2
from preprocessing import prepare_sequence, close_hands
from flask import Flask, jsonify, request, send_file, abort
from flask_cors import CORS

import os
import subprocess
import tempfile
import numpy as np


app = Flask(__name__)
CORS(app)


# ================= PROJECT PATHS =================

BASE_DIR = os.path.dirname(
    os.path.dirname(os.path.abspath(__file__))
)

RAW_DATASET_DIR = os.path.join(
    BASE_DIR, "dataset", "raw", "include"
)

MEDIAPIPE_PYTHON = os.path.join(
    BASE_DIR, ".venv_mediapipe", "Scripts", "python.exe"
)

TRAIN_PYTHON = os.path.join(
    BASE_DIR, ".venv_train", "Scripts", "python.exe"
)

SINGLE_FRAME_WORKER = os.path.join(
    BASE_DIR, "app", "mediapipe_worker.py"
)

SEQUENCE_WORKER = os.path.join(
    BASE_DIR, "app", "mediapipe_sequence_worker.py"
)

PREDICT_SCRIPT = os.path.join(
    BASE_DIR, "app", "predict_sequence.py"
)


# ================= HOME =================

@app.route("/")
def home():
    return "SanketSetu backend is running!"


# ================= STATUS =================

@app.route("/api/status")
def status():
    return jsonify({
        "status": "ok",
        "message": "SanketSetu API is ready"
    })


# ================= BASIC POST TEST =================

@app.route("/api/test", methods=["POST"])
def test():
    return jsonify({
        "status": "ok",
        "message": "Data received by SanketSetu backend"
    })


# ================= SINGLE FRAME =================

@app.route("/api/frame", methods=["POST"])
def receive_frame():

    if "frame" not in request.files:
        return jsonify({
            "status": "error",
            "message": "No frame received"
        }), 400

    frame = request.files["frame"]
    temp_path = None

    try:
        with tempfile.NamedTemporaryFile(
            suffix=".jpg",
            delete=False
        ) as temp_file:
            temp_path = temp_file.name
            frame.save(temp_path)

        result = subprocess.run(
            [
                MEDIAPIPE_PYTHON,
                SINGLE_FRAME_WORKER,
                temp_path
            ],
            capture_output=True,
            text=True,
            timeout=60
        )

        if result.returncode != 0:
            app.logger.error(
                "Single-frame MediaPipe worker failed: %s",
                result.stderr
            )
            return jsonify({
                "status": "error",
                "message": "MediaPipe worker failed",
                "error": result.stderr
            }), 500

        output_lines = result.stdout.splitlines()

        try:
            start_index = output_lines.index("LANDMARKS_START")
            end_index = output_lines.index("LANDMARKS_END")
        except ValueError:
            return jsonify({
                "status": "error",
                "message": "Could not parse MediaPipe landmarks",
                "output": result.stdout
            }), 500

        landmark_text = "".join(
            output_lines[start_index + 1:end_index]
        )

        try:
            landmarks = [
                float(value)
                for value in landmark_text.split(",")
                if value.strip()
            ]
        except ValueError:
            return jsonify({
                "status": "error",
                "message": "Invalid landmark values returned"
            }), 500

        if len(landmarks) != 63:
            return jsonify({
                "status": "error",
                "message": (
                    f"Expected 63 landmarks, got {len(landmarks)}"
                )
            }), 500

        return jsonify({
            "status": "ok",
            "message": "Frame processed successfully",
            "landmarks": landmarks
        })

    except subprocess.TimeoutExpired:
        return jsonify({
            "status": "error",
            "message": "MediaPipe worker timed out"
        }), 504

    except Exception:
        app.logger.exception("Error processing single frame")
        return jsonify({
            "status": "error",
            "message": "Unexpected error processing frame"
        }), 500

    finally:
        if temp_path and os.path.exists(temp_path):
            os.remove(temp_path)


# ================= 154-FRAME BI-LSTM V2 PIPELINE =================

@app.route("/api/sequence_frames", methods=["POST"])
def receive_sequence_frames():

    frames = request.files.getlist("frames")

    if len(frames) == 0:
        return jsonify({
            "status": "error",
            "message": "No frames received"
        }), 400

    if len(frames) > 154:
        return jsonify({
            "status": "error",
            "message": (
                f"Maximum 154 frames allowed, got {len(frames)}"
            )
        }), 400

    # Confirm the required environments and scripts exist.
    required_paths = [
        MEDIAPIPE_PYTHON,
        TRAIN_PYTHON,
        SEQUENCE_WORKER,
        PREDICT_SCRIPT
    ]

    missing_paths = [
        path for path in required_paths
        if not os.path.isfile(path)
    ]

    if missing_paths:
        return jsonify({
            "status": "error",
            "message": "Required pipeline file not found",
            "missing_paths": missing_paths
        }), 500

    temp_dir = tempfile.mkdtemp(prefix="sanketsetu_frames_")
    sequence_path = os.path.join(temp_dir, "sequence.npy")

    try:
        # Save uploaded frames in the temporary directory.
        for index, frame in enumerate(frames):
            frame_path = os.path.join(
                temp_dir,
                f"frame_{index}.jpg"
            )
            frame.save(frame_path)

        app.logger.info(
            "Received %s frames. Starting V2 extraction.",
            len(frames)
        )

        # ---------- MEDIAPIPE: RAW (154, 128) SEQUENCE ----------

        result = subprocess.run(
            [
                MEDIAPIPE_PYTHON,
                SEQUENCE_WORKER,
                temp_dir,
                sequence_path
            ],
            capture_output=True,
            text=True,
            timeout=180
        )

        if result.returncode != 0:
            app.logger.error(
                "Sequence worker failed: %s",
                result.stderr
            )
            return jsonify({
                "status": "error",
                "message": "MediaPipe sequence processing failed",
                "error": result.stderr[-6000:]
            }), 500

        if not os.path.isfile(sequence_path):
            return jsonify({
                "status": "error",
                "message": "Sequence worker did not create output"
            }), 500

        sequence = np.load(sequence_path, allow_pickle=False)

        if sequence.shape != (154, 128):
            return jsonify({
                "status": "error",
                "message": (
                    f"Expected sequence shape (154, 128), "
                    f"got {sequence.shape}"
                )
            }), 500

        if not np.isfinite(sequence).all():
            return jsonify({
                "status": "error",
                "message": "Sequence contains non-finite values"
            }), 500

        # ---------- BI-LSTM V2 PREDICTION ----------

        app.logger.info(
            "V2 extraction successful. Running BiLSTM prediction."
        )

        prediction_result = subprocess.run(
            [
                TRAIN_PYTHON,
                PREDICT_SCRIPT,
                sequence_path
            ],
            capture_output=True,
            text=True,
            timeout=180
        )

        if prediction_result.returncode != 0:
            app.logger.error(
                "BiLSTM prediction failed: %s",
                prediction_result.stderr
            )
            return jsonify({
                "status": "error",
                "message": "BiLSTM V2 prediction failed",
                "error": prediction_result.stderr[-6000:]
            }), 500

        predicted_class = None
        gesture = None
        confidence = None

        for line in prediction_result.stdout.splitlines():
            if line.startswith("Predicted class:"):
                predicted_class = int(
                    line.split(":", 1)[1].strip()
                )

            elif line.startswith("Gesture:"):
                gesture = line.split(":", 1)[1].strip()

            elif line.startswith("Confidence:"):
                confidence = float(
                    line.split(":", 1)[1].strip()
                )

        if (
            predicted_class is None
            or gesture is None
            or confidence is None
        ):
            return jsonify({
                "status": "error",
                "message": "Could not parse BiLSTM V2 output",
                "output": prediction_result.stdout[-6000:]
            }), 500

        app.logger.info(
            "BiLSTM prediction: class=%s, gesture=%s, confidence=%.4f",
            predicted_class,
            gesture,
            confidence
        )

        return jsonify({
            "status": "ok",
            "message": (
                "Sequence processed and BiLSTM V2 prediction successful"
            ),
            "frames_received": len(frames),
            "frames_processed": 154,
            "features": 128,
            "predicted_class": predicted_class,
            "gesture": gesture,
            "confidence": confidence
        })

    except subprocess.TimeoutExpired as error:
        app.logger.error("Pipeline subprocess timed out: %s", error)
        return jsonify({
            "status": "error",
            "message": "Sequence processing timed out"
        }), 504

    except Exception:
        app.logger.exception("Sequence pipeline failed")
        return jsonify({
            "status": "error",
            "message": "Unexpected sequence-processing error"
        }), 500

    finally:
        if os.path.isdir(temp_dir):
            import shutil
            shutil.rmtree(temp_dir, ignore_errors=True)



# ================= TRANSFORMER V5.2 TEST-SAMPLE DEMO =================

_TRANSFORMER_MODEL = None
_TRANSFORMER_MEAN = None
_TRANSFORMER_STD = None
_TRANSFORMER_MAPPING = None
_X_TEST = None
_Y_TEST = None

def _first_existing(*paths):
    for path in paths:
        if path and os.path.isfile(path):
            return path
    return None

def _load_transformer_demo_assets():
    """Load existing V5.2 artifacts once, using common project locations."""
    global _TRANSFORMER_MODEL, _TRANSFORMER_MEAN, _TRANSFORMER_STD
    global _TRANSFORMER_MAPPING, _X_TEST, _Y_TEST
    if _TRANSFORMER_MODEL is not None:
        return

    model_path = _first_existing(
        os.path.join(BASE_DIR, "models", "best_transformer_v5_2.keras"),
        os.path.join(os.path.dirname(os.path.abspath(__file__)), "models", "best_transformer_v5_2.keras"),
        os.path.join(BASE_DIR, "best_transformer_v5_2.keras")
    )
    mean_path = _first_existing(
        os.path.join(BASE_DIR, "outputs", "v5_2_train_mean.npy"),
        os.path.join(BASE_DIR, "v5_2_train_mean.npy")
    )
    std_path = _first_existing(
        os.path.join(BASE_DIR, "outputs", "v5_2_train_std.npy"),
        os.path.join(BASE_DIR, "v5_2_train_std.npy")
    )
    mapping_path = _first_existing(
        os.path.join(BASE_DIR, "outputs", "class_mapping.json"),
        os.path.join(BASE_DIR, "class_mapping.json")
    )
    x_path = _first_existing(
        os.path.join(BASE_DIR, "dataset", "training", "X_test.npy"),
        os.path.join(BASE_DIR, "X_test.npy")
    )
    y_path = _first_existing(
        os.path.join(BASE_DIR, "dataset", "training", "y_test.npy"),
        os.path.join(BASE_DIR, "y_test.npy")
    )
    missing = [name for name, path in {
        "Transformer model": model_path, "training mean": mean_path,
        "training std": std_path, "class mapping": mapping_path,
        "X_test.npy": x_path, "y_test.npy": y_path
    }.items() if path is None]
    if missing:
        raise FileNotFoundError(
            "Missing Transformer demo assets: " + ", ".join(missing) +
            ". Keep the model in models/ and mapping/normalization in outputs/, "
            "and test arrays in dataset/training/."
        )

    import json
    from tensorflow import keras
    _TRANSFORMER_MODEL = keras.models.load_model(model_path, compile=False)
    _TRANSFORMER_MEAN = np.load(mean_path, allow_pickle=False)
    _TRANSFORMER_STD = np.load(std_path, allow_pickle=False)
    with open(mapping_path, "r", encoding="utf-8") as handle:
        _TRANSFORMER_MAPPING = json.load(handle)
    _X_TEST = np.load(x_path, mmap_mode="r", allow_pickle=False)
    _Y_TEST = np.load(y_path, mmap_mode="r", allow_pickle=False)

@app.route("/api/test-sample", methods=["POST"])
def predict_test_sample():
    """Predict one already-preprocessed X_test sequence with Transformer V5.2."""
    try:
        body = request.get_json(silent=True) or {}
        try:
            sample_index = int(body.get("index", 0))
        except (TypeError, ValueError):
            return jsonify({"status": "error", "message": "Sample index must be an integer."}), 400

        _load_transformer_demo_assets()
        if sample_index < 0 or sample_index >= len(_X_TEST):
            return jsonify({"status": "error", "message": f"Index must be between 0 and {len(_X_TEST)-1}."}), 400

        sequence = np.asarray(_X_TEST[sample_index], dtype=np.float32)
        expected_id = int(_Y_TEST[sample_index])
        if sequence.shape != (154, 63):
            return jsonify({"status": "error", "message": f"Expected sample shape (154, 63), got {sequence.shape}."}), 500

        # Apply the same saved training statistics used by the Transformer demo.
        normalized = (sequence[None, ...] - _TRANSFORMER_MEAN) / np.maximum(_TRANSFORMER_STD, 1e-7)
        probabilities = np.asarray(_TRANSFORMER_MODEL.predict(normalized, verbose=0))[0]
        predicted_id = int(np.argmax(probabilities))

        def label_for(class_id):
            return str(_TRANSFORMER_MAPPING.get(str(class_id), f"Class {class_id}"))

        top_ids = np.argsort(probabilities)[-3:][::-1]
        top_predictions = [{"class_id": int(class_id), "gesture": label_for(int(class_id)), "confidence": float(probabilities[class_id])} for class_id in top_ids]
        return jsonify({
            "status": "ok", "sample_index": sample_index,
            "expected_class": expected_id, "expected_label": label_for(expected_id),
            "predicted_class": predicted_id, "gesture": label_for(predicted_id),
            "confidence": float(probabilities[predicted_id]),
            "top_predictions": top_predictions
        })
    except FileNotFoundError as error:
        return jsonify({"status": "error", "message": str(error)}), 500
    except Exception as error:
        app.logger.exception("Transformer test-sample prediction failed")
        return jsonify({"status": "error", "message": f"Transformer prediction failed: {error}"}), 500


import re
from pathlib import Path
from urllib.parse import quote

VIDEO_EXTENSIONS = {".mp4", ".avi", ".mov", ".mkv", ".webm"}


def clean_gesture_name(folder_name):
    """Convert '1. loud' into 'loud' for display."""
    return re.sub(r"^\s*\d+\.\s*", "", folder_name).strip()


def discover_gestures():
    """Discover actual gesture folders, excluding nested folders like Extra."""
    if not os.path.isdir(RAW_DATASET_DIR):
        raise FileNotFoundError(
            f"Raw dataset folder not found: {RAW_DATASET_DIR}"
        )

    gestures = []

    for category_path in sorted(Path(RAW_DATASET_DIR).rglob("*")):
        if not category_path.is_dir():
            continue

        videos = sorted(
            (
                path for path in category_path.iterdir()
                if path.is_file()
                and path.suffix.lower() in VIDEO_EXTENSIONS
            ),
            key=lambda path: path.name.casefold()
        )

        if not videos:
            continue

        # Skip folders nested inside another gesture folder,
        # such as "Extra" inside "5. Beautiful".
        relative_folder = category_path.relative_to(
            Path(RAW_DATASET_DIR)
        )
        parts = relative_folder.parts

        if any(
            part.casefold() == "extra"
            for part in parts
        ):
            continue

        gesture_id = relative_folder.as_posix()

        gestures.append({
            "id": gesture_id,
            "name": clean_gesture_name(category_path.name),
            "category": category_path.parent.name,
            "video": f"/api/learn/video/{quote(gesture_id, safe='/')}"
        })

    return gestures


# ================= TRANSFORMER V5.2 VIDEO PREDICTION =================

@app.route("/api/predict-video", methods=["POST"])
def predict_video():
    temp_path = None

    try:
        if "video" not in request.files:
            return jsonify({
                "status": "error",
                "message": "Please upload a video file."
            }), 400

        video = request.files["video"]

        if not video.filename:
            return jsonify({
                "status": "error",
                "message": "No video file selected."
            }), 400

        allowed_extensions = {".mp4", ".mov", ".avi", ".mkv", ".webm"}
        extension = os.path.splitext(video.filename)[1].lower()

        if extension not in allowed_extensions:
            return jsonify({
                "status": "error",
                "message": "Unsupported video format."
            }), 400

        with tempfile.NamedTemporaryFile(
            suffix=extension,
            delete=False
        ) as temp_file:
            temp_path = temp_file.name
            video.save(temp_path)

        cap = cv2.VideoCapture(temp_path)

        if not cap.isOpened():
            return jsonify({
                "status": "error",
                "message": "Could not decode this video. Try MP4."
            }), 400

        frames = []

        try:
            while True:
                ok, frame = cap.read()
                if not ok:
                    break
                frames.append(frame)
        finally:
            cap.release()

        if not frames:
            return jsonify({
                "status": "error",
                "message": "The uploaded video contains no readable frames."
            }), 400

        # Use the existing preprocessing.py implementation.
        sequence = prepare_sequence(frames)

        if sequence.shape != (154, 63):
            return jsonify({
                "status": "error",
                "message": (
                    f"Expected (154, 63), got {sequence.shape}."
                )
            }), 500

        if not np.isfinite(sequence).all():
            return jsonify({
                "status": "error",
                "message": "Extracted sequence contains invalid values."
            }), 500

        # Load the existing Transformer V5.2 assets.
        _load_transformer_demo_assets()

        normalized = (
            sequence[np.newaxis, ...] - _TRANSFORMER_MEAN
        ) / np.maximum(_TRANSFORMER_STD, 1e-7)

        probabilities = np.asarray(
            _TRANSFORMER_MODEL.predict(normalized, verbose=0)
        )[0]

        predicted_id = int(np.argmax(probabilities))

        def label_for(class_id):
            return str(
                _TRANSFORMER_MAPPING.get(
                    str(class_id), f"Class {class_id}"
                )
            )

        top_ids = np.argsort(probabilities)[-3:][::-1]

        top_predictions = [
            {
                "class_id": int(class_id),
                "gesture": label_for(int(class_id)),
                "confidence": float(probabilities[class_id])
            }
            for class_id in top_ids
        ]

        return jsonify({
            "status": "ok",
            "gesture": label_for(predicted_id),
            "predicted_class": predicted_id,
            "confidence": float(probabilities[predicted_id]),
            "top_predictions": top_predictions,
            "sequence_shape": list(sequence.shape),
            "decoded_frames": len(frames)
        })

    except FileNotFoundError as error:
        return jsonify({
            "status": "error",
            "message": str(error)
        }), 500

    except Exception as error:
        app.logger.exception("Transformer video prediction failed")
        return jsonify({
            "status": "error",
            "message": f"Video prediction failed: {error}"
        }), 500

    finally:
        if temp_path and os.path.exists(temp_path):
            try:
                os.remove(temp_path)
            except OSError:
                app.logger.warning(
                    "Could not remove temporary uploaded video."
                )


@app.route("/api/learn/gestures", methods=["GET"])
def learn_gestures():
    try:
        return jsonify({
            "status": "ok",
            "count": len(discover_gestures()),
            "gestures": discover_gestures()
        })
    except FileNotFoundError as error:
        app.logger.error("%s", error)
        return jsonify({
            "status": "error",
            "message": "Raw gesture dataset folder not found."
        }), 500


@app.route("/api/learn/video/<path:gesture_id>", methods=["GET"])
def learn_gesture_video(gesture_id):
    # Resolve only a folder discovered under the configured dataset root.
    root = Path(RAW_DATASET_DIR).resolve()
    folder = (root / gesture_id).resolve()

    if not folder.is_relative_to(root) or not folder.is_dir():
        abort(404)

    videos = sorted(
        (
            path for path in folder.iterdir()
            if path.is_file()
            and path.suffix.lower() in VIDEO_EXTENSIONS
        ),
        key=lambda path: path.name.casefold()
    )

    if not videos:
        abort(404)

    return send_file(videos[0], conditional=True)


# ================= RUN SERVER =================

if __name__ == "__main__":
    app.run(debug=True)
