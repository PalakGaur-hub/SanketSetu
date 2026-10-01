import os
import re
import cv2
import numpy as np
from pathlib import Path
from collections import defaultdict

# ============================================================
# PATHS
# ============================================================

ROOT = Path(__file__).resolve().parent

RAW_PATH = ROOT / "dataset" / "raw" / "include"

OUTPUT_PATH = (
    ROOT
    / "frontend"
    / "assets"
    / "images"
    / "isl"
)

OUTPUT_PATH.mkdir(parents=True, exist_ok=True)


# ============================================================
# SETTINGS
# ============================================================

MIN_VIDEOS = 8

MAX_VIDEOS_PER_SIGN = 3
FRAMES_PER_VIDEO = 30

print("\n" + "=" * 70)
print("        SAN KET SETU — ISL IMAGE EXTRACTION")
print("=" * 70)


# ============================================================
# STEP 1 — BUILD EXACT DATASET SIGN LIST
# ============================================================

print("\n📂 Scanning dataset...")

sign_videos = defaultdict(list)

for part in sorted(RAW_PATH.iterdir()):

    if not part.is_dir():
        continue

    for category in sorted(part.iterdir()):

        if not category.is_dir():
            continue

        for sign_folder in sorted(category.iterdir()):

            if not sign_folder.is_dir():
                continue

            videos = []

            for video in sign_folder.iterdir():

                if video.suffix.lower() in {
                    ".mov",
                    ".mp4",
                    ".avi"
                }:
                    videos.append(video)

            if videos:

                # IMPORTANT:
                # Dataset mapping uses SIGN name
                sign_name = sign_folder.name

                sign_videos[sign_name].extend(videos)


print(f"📁 Unique signs found: {len(sign_videos)}")


# ============================================================
# STEP 2 — REPRODUCE NOTEBOOK 05 FILTER
# ============================================================

print("\n🔎 Applying the same >= 8 video filter...")

valid_signs = {
    sign: videos
    for sign, videos in sign_videos.items()
    if len(videos) >= MIN_VIDEOS
}

print(f"✅ Signs remaining: {len(valid_signs)}")


# ============================================================
# STEP 3 — REPRODUCE THE EXACT LABEL ORDER
# ============================================================
#
# Notebook 05:
#
# labels = sorted(dataset_df["Sign"].unique())
#
# label_to_id = {
#     label: idx
#     for idx, label in enumerate(labels)
# }
#
# Then classes with <8 videos are removed.
#
# LabelEncoder then re-encodes the remaining original labels.
#
# Therefore:
#       sorted(valid signs)
#       =
#       final 0 → 209 class order
#
# ============================================================

final_signs = sorted(valid_signs.keys())

if len(final_signs) != 210:

    print("\n❌ STOP")
    print(
        f"Expected 210 final signs, "
        f"but reconstructed {len(final_signs)}."
    )
    print(
        "\nWe are NOT extracting anything because "
        "the mapping would not be guaranteed correct."
    )
    raise SystemExit


label_to_sign = {
    idx: sign
    for idx, sign in enumerate(final_signs)
}


print("\n🎯 EXACT 210-CLASS MAPPING RECONSTRUCTED")

for idx in range(min(10, len(final_signs))):
    print(f"   {idx:3d} → {label_to_sign[idx]}")

print("   ...")

for idx in range(max(0, len(final_signs) - 5), len(final_signs)):
    print(f"   {idx:3d} → {label_to_sign[idx]}")


# ============================================================
# STEP 4 — SAFE FILENAME FUNCTION
# ============================================================

def clean_filename(sign):

    # Remove dataset number such as:
    # "48. Hello" → "Hello"

    name = re.sub(
        r"^\s*\d+\s*[\.\-_]\s*",
        "",
        sign
    )

    # Convert spaces / punctuation to hyphens
    name = name.strip().lower()

    name = re.sub(
        r"[^a-z0-9]+",
        "-",
        name
    )

    name = name.strip("-")

    return name


# ============================================================
# STEP 5 — SHARPNESS FUNCTION
# ============================================================

def sharpness(image):

    gray = cv2.cvtColor(
        image,
        cv2.COLOR_BGR2GRAY
    )

    return cv2.Laplacian(
        gray,
        cv2.CV_64F
    ).var()


# ============================================================
# STEP 6 — HAND-AWARE FRAME SELECTION
# ============================================================

def choose_best_frame(video_path):

    cap = cv2.VideoCapture(str(video_path))

    if not cap.isOpened():
        return None, -1

    total_frames = int(
        cap.get(cv2.CAP_PROP_FRAME_COUNT)
    )

    if total_frames <= 0:
        cap.release()
        return None, -1

    # Sample frames throughout the video
    frame_indices = np.linspace(
        0,
        total_frames - 1,
        min(FRAMES_PER_VIDEO, total_frames),
        dtype=int
    )

    best_frame = None
    best_score = -1

    for frame_index in frame_indices:

        cap.set(
            cv2.CAP_PROP_POS_FRAMES,
            int(frame_index)
        )

        success, frame = cap.read()

        if not success:
            continue

        h, w = frame.shape[:2]

        # ----------------------------------------------------
        # Find sharpness in central region
        # ----------------------------------------------------

        gray = cv2.cvtColor(
            frame,
            cv2.COLOR_BGR2GRAY
        )

        overall_sharpness = cv2.Laplacian(
            gray,
            cv2.CV_64F
        ).var()

        # ----------------------------------------------------
        # Central region gets preference because the signer
        # is normally around the center of the frame.
        # ----------------------------------------------------

        x1 = int(w * 0.15)
        x2 = int(w * 0.85)

        y1 = int(h * 0.10)
        y2 = int(h * 0.90)

        central = frame[y1:y2, x1:x2]

        central_sharpness = sharpness(central)

        # ----------------------------------------------------
        # Score
        # ----------------------------------------------------

        score = (
            central_sharpness * 0.75
            + overall_sharpness * 0.25
        )

        if score > best_score:

            best_score = score
            best_frame = frame.copy()

    cap.release()

    return best_frame, best_score


# ============================================================
# STEP 7 — EXTRACT ONE IMAGE PER SIGN
# ============================================================

print("\n🖼️ Extracting representative images...")
print(
    f"Using up to {MAX_VIDEOS_PER_SIGN} videos/sign "
    f"and {FRAMES_PER_VIDEO} frames/video."
)

successful = 0
failed = []

for label, sign in label_to_sign.items():

    filename = clean_filename(sign)

    output_file = OUTPUT_PATH / f"{filename}.jpg"

    # Don't overwrite an already extracted image
    if output_file.exists():

        successful += 1

        print(
            f"[{label:3d}/209] "
            f"⏭️ {sign} — already exists"
        )

        continue

    videos = valid_signs[sign]

    # Sort for deterministic behavior
    videos = sorted(videos)

    # Limit number of videos
    videos = videos[:MAX_VIDEOS_PER_SIGN]

    best_frame = None
    best_score = -1

    for video in videos:

        frame, score = choose_best_frame(video)

        if frame is None:
            continue

        if score > best_score:

            best_score = score
            best_frame = frame

    if best_frame is None:

        failed.append(sign)

        print(
            f"[{label:3d}/209] ❌ {sign}"
        )

        continue

    # Save high-quality JPEG
    cv2.imwrite(
        str(output_file),
        best_frame,
        [
            cv2.IMWRITE_JPEG_QUALITY,
            95
        ]
    )

    successful += 1

    print(
        f"[{label:3d}/209] "
        f"✅ {sign} → {filename}.jpg"
    )


# ============================================================
# STEP 8 — SAVE THE MAPPING
# ============================================================

mapping_file = OUTPUT_PATH / "gesture_mapping.csv"

with open(
    mapping_file,
    "w",
    encoding="utf-8"
) as f:

    f.write("label,gesture,filename\n")

    for label, sign in label_to_sign.items():

        filename = clean_filename(sign)

        f.write(
            f'{label},"{sign}",{filename}.jpg\n'
        )


# ============================================================
# FINAL REPORT
# ============================================================

print("\n" + "=" * 70)
print("                 EXTRACTION COMPLETE")
print("=" * 70)

print(f"🎯 Model classes       : 210")
print(f"🖼️ Images extracted    : {successful}")
print(f"❌ Failed              : {len(failed)}")
print(f"📁 Output              : {OUTPUT_PATH}")
print(f"📄 Mapping             : {mapping_file}")

    if failed:

        print("\nFailed signs:")

        for sign in failed:
            print("  -", sign)

    print("=" * 70)