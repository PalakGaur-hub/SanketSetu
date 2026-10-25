import cv2
import numpy as np
import mediapipe as mp


# --------------------------------------------------
# SanketSetu preprocessing configuration
# --------------------------------------------------

MAX_FRAMES = 154
FEATURES_PER_FRAME = 63


# --------------------------------------------------
# MediaPipe Hands
# --------------------------------------------------

mp_hands = mp.solutions.hands

hands = mp_hands.Hands(
    static_image_mode=False,
    max_num_hands=2,
    min_detection_confidence=0.5,
    min_tracking_confidence=0.5
)


# --------------------------------------------------
# Extract landmarks from one frame
# --------------------------------------------------

def extract_landmarks(frame):
    """
    Extract the first detected hand from one video frame.

    Returns:
        numpy array of shape (63,)
        21 landmarks × (x, y, z)

    If no hand is detected, returns 63 zeros.
    """

    frame_landmarks = np.zeros(
        FEATURES_PER_FRAME,
        dtype=np.float32
    )

    # MediaPipe expects RGB

    frame = cv2.resize(frame, (320, 240))
    rgb_frame = cv2.cvtColor(
        frame,
        cv2.COLOR_BGR2RGB
    )

    results = hands.process(rgb_frame)

    if results.multi_hand_landmarks:
        hand = results.multi_hand_landmarks[0]

        coords = []

        for point in hand.landmark:
            coords.extend([
                point.x,
                point.y,
                point.z
            ])

        frame_landmarks = np.array(
            coords,
            dtype=np.float32
        )

    return frame_landmarks


# --------------------------------------------------
# Build a 154-frame sequence
# --------------------------------------------------

def prepare_sequence(frames):
    """
    Convert a collection of video frames into
    the model's expected shape: (154, 63).

    Frames beyond 154 are truncated.
    Sequences shorter than 154 are zero-padded.
    """

    sequence = []

    for frame in frames:
        landmarks = extract_landmarks(frame)
        sequence.append(landmarks)

    sequence = np.asarray(
        sequence,
        dtype=np.float32
    )

    # Create fixed-size sequence
    padded = np.zeros(
        (MAX_FRAMES, FEATURES_PER_FRAME),
        dtype=np.float32
    )

    length = min(
        sequence.shape[0],
        MAX_FRAMES
    )

    if length > 0:
        padded[:length] = sequence[:length]

    return padded


# --------------------------------------------------
# Cleanup
# --------------------------------------------------

def close_hands():
    """Release the MediaPipe Hands resources."""
    hands.close()