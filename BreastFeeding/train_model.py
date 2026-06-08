"""
Breastfeeding Pose Detection - Model Training Script
=====================================================
ระบบเทรนโมเดลสำหรับตรวจจับท่าทางการให้นมบุตร

โครงสร้างข้อมูล:
  data/
    correct/      - ภาพท่าทางที่ถูกต้อง
    incorrect/    - ภาพท่าทางที่ไม่ถูกต้อง
    labels.csv    - ป้ายกำกับข้อมูลเพิ่มเติม (optional)

การใช้งาน:
  pip install -r requirements.txt
  python train_model.py

ผลลัพธ์:
  models/breastfeeding_classifier.pkl  - โมเดล Scikit-learn
  models/keypoints_scaler.pkl          - Scaler สำหรับ normalize keypoints
  models/label_encoder.pkl             - Label encoder
  models/training_report.json          - รายงานผลการเทรน
"""

import os
import cv2
import json
import time
import pickle
import logging
import numpy as np
import pandas as pd
from pathlib import Path
from datetime import datetime
from dataclasses import dataclass, asdict
from typing import Optional

import mediapipe as mp
from sklearn.ensemble import (
    RandomForestClassifier,
    GradientBoostingClassifier,
    VotingClassifier
)
from sklearn.svm import SVC
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.model_selection import (
    train_test_split,
    cross_val_score,
    StratifiedKFold
)
from sklearn.metrics import (
    classification_report,
    confusion_matrix,
    accuracy_score,
    roc_auc_score
)
from sklearn.pipeline import Pipeline

# ============================================================
# ตั้งค่า Logging
# ============================================================
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler("training.log", encoding="utf-8"),
    ],
)
logger = logging.getLogger(__name__)

# ============================================================
# Config
# ============================================================
@dataclass
class TrainingConfig:
    data_dir: str = "data"
    model_dir: str = "models"
    image_size: tuple = (640, 480)
    test_size: float = 0.2
    random_state: int = 42
    min_detection_confidence: float = 0.5
    min_tracking_confidence: float = 0.5
    n_estimators: int = 200
    cv_folds: int = 5
    augment_data: bool = True
    augment_count: int = 3


CONFIG = TrainingConfig()

# ============================================================
# Class Labels (ท่าทาง)
# ============================================================
POSE_LABELS = {
    "correct": {
        "cradle_hold":    "ท่าอุ้มขวาง (Cradle Hold)",
        "football_hold":  "ท่าอุ้มใต้แขน (Football Hold)",
        "cross_cradle":   "ท่าอุ้มขวางประยุกต์ (Cross-Cradle Hold)",
        "side_lying":     "ท่านอนตะแคง (Side-Lying)",
    },
    "incorrect": {
        "poor_latch":     "การดูดไม่ถูกต้อง",
        "wrong_angle":    "มุมทารกไม่ถูกต้อง",
        "tense_shoulder": "ไหล่ตึง / หลังงอ",
        "baby_nose_blocked": "จมูกทารกถูกปิดกั้น",
    }
}

# MediaPipe Pose landmark indices ที่สำคัญ
IMPORTANT_LANDMARKS = [
    0,   # nose
    2, 5,  # eyes
    7, 8,  # ears
    11, 12,  # shoulders
    13, 14,  # elbows
    15, 16,  # wrists
    23, 24,  # hips
    25, 26,  # knees
]

# ============================================================
# Feature Extraction
# ============================================================
class PoseFeatureExtractor:
    """แปลง MediaPipe landmarks เป็น feature vector"""

    def __init__(self, config: TrainingConfig):
        self.config = config
        self.mp_pose = mp.solutions.pose
        self.pose = self.mp_pose.Pose(
            static_image_mode=True,
            model_complexity=2,
            min_detection_confidence=config.min_detection_confidence,
        )
        self.mp_holistic = mp.solutions.holistic
        self.holistic = self.mp_holistic.Holistic(
            static_image_mode=True,
            model_complexity=1,
            min_detection_confidence=config.min_detection_confidence,
        )

    def extract_from_image(self, image_path: str) -> Optional[np.ndarray]:
        """ดึง features จากภาพ"""
        img = cv2.imread(image_path)
        if img is None:
            logger.warning(f"ไม่สามารถอ่านภาพ: {image_path}")
            return None

        img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

        # ดึง full body pose
        pose_results = self.pose.process(img_rgb)
        holistic_results = self.holistic.process(img_rgb)

        if not pose_results.pose_landmarks:
            logger.debug(f"ไม่พบ pose ในภาพ: {image_path}")
            return None

        return self._build_feature_vector(
            pose_results, holistic_results, img.shape
        )

    def extract_from_frame_with_results(self, frame: np.ndarray) -> tuple:
        """ดึง features พร้อมส่งคืน raw results สำหรับนำไปวาดข้อต่อต่อ"""
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        pose_results = self.pose.process(frame_rgb)
        holistic_results = self.holistic.process(frame_rgb)

        if not pose_results.pose_landmarks:
            return None, None

        features = self._build_feature_vector(
            pose_results, holistic_results, frame.shape
        )
        return features, pose_results

    def _build_feature_vector(
        self,
        pose_results,
        holistic_results,
        img_shape: tuple
    ) -> np.ndarray:
        """สร้าง feature vector จาก landmarks"""
        features = []
        h, w = img_shape[:2]

        # 1) Raw landmark coordinates (x, y, z, visibility)
        landmarks = pose_results.pose_landmarks.landmark
        for idx in IMPORTANT_LANDMARKS:
            lm = landmarks[idx]
            features.extend([lm.x, lm.y, lm.z, lm.visibility])

        # 2) Computed angles (biomechanical features)
        features.extend(self._compute_angles(landmarks))

        # 3) Relative distances
        features.extend(self._compute_distances(landmarks))

        # 4) Symmetry scores
        features.extend(self._compute_symmetry(landmarks))

        # 5) Upper body bbox ratio (ประมาณตำแหน่งทารก)
        features.extend(self._compute_body_ratios(landmarks, w, h))

        return np.array(features, dtype=np.float32)

    def _compute_angles(self, landmarks) -> list:
        """คำนวณมุมข้อต่อสำคัญ"""
        def angle(a, b, c) -> float:
            """มุมที่จุด b ระหว่าง a-b-c"""
            a = np.array([a.x, a.y])
            b = np.array([b.x, b.y])
            c = np.array([c.x, c.y])
            ba = a - b
            bc = c - b
            cos_ang = np.dot(ba, bc) / (np.linalg.norm(ba) * np.linalg.norm(bc) + 1e-9)
            return float(np.degrees(np.arccos(np.clip(cos_ang, -1, 1))))

        lm = landmarks
        return [
            angle(lm[11], lm[13], lm[15]),  # left elbow
            angle(lm[12], lm[14], lm[16]),  # right elbow
            angle(lm[13], lm[11], lm[23]),  # left shoulder-hip
            angle(lm[14], lm[12], lm[24]),  # right shoulder-hip
            angle(lm[11], lm[23], lm[25]),  # left trunk
            angle(lm[12], lm[24], lm[26]),  # right trunk
            # ความเอียงของไหล่ (shoulder tilt)
            float(abs(lm[11].y - lm[12].y)),
        ]

    def _compute_distances(self, landmarks) -> list:
        """ระยะห่างระหว่างจุดสำคัญ"""
        def dist(a, b) -> float:
            return float(np.hypot(a.x - b.x, a.y - b.y))

        lm = landmarks
        return [
            dist(lm[15], lm[11]),   # left wrist-shoulder (ระยะแขน)
            dist(lm[16], lm[12]),   # right wrist-shoulder
            dist(lm[15], lm[16]),   # wrist-wrist (ความกว้างอุ้ม)
            dist(lm[11], lm[12]),   # shoulder width
            dist(lm[0],  lm[11]),   # nose-left shoulder (ก้มหน้า)
            dist(lm[15], lm[0]),    # wrist-nose (ระยะทารก)
            dist(lm[16], lm[0]),
            dist(lm[23], lm[11]),   # hip-shoulder (ความสูงลำตัว)
        ]

    def _compute_symmetry(self, landmarks) -> list:
        """ความสมมาตรระหว่างซ้าย-ขวา"""
        lm = landmarks
        return [
            abs(lm[11].x - (1 - lm[12].x)),  # shoulder symmetry
            abs(lm[13].x - (1 - lm[14].x)),  # elbow symmetry
            abs(lm[15].x - (1 - lm[16].x)),  # wrist symmetry
            abs(lm[11].y - lm[12].y),          # shoulder level
        ]

    def _compute_body_ratios(self, landmarks, w: int, h: int) -> list:
        """อัตราส่วนตำแหน่งร่างกาย"""
        lm = landmarks
        shoulder_mid_y = (lm[11].y + lm[12].y) / 2
        wrist_mid_y    = (lm[15].y + lm[16].y) / 2
        wrist_mid_x    = (lm[15].x + lm[16].x) / 2
        return [
            shoulder_mid_y,
            wrist_mid_y,
            wrist_mid_x,
            abs(wrist_mid_y - shoulder_mid_y),  # แนวตั้งของแขน
            lm[0].y,                              # ความสูงศีรษะ
        ]

    def get_feature_dim(self) -> int:
        return (
            len(IMPORTANT_LANDMARKS) * 4  # x,y,z,visibility
            + 7   # angles
            + 8   # distances
            + 4   # symmetry
            + 5   # ratios
        )

    def close(self):
        self.pose.close()
        self.holistic.close()


# ============================================================
# Data Augmentation
# ============================================================
class DataAugmenter:
    """เพิ่มปริมาณข้อมูลด้วยการแปลงภาพ"""

    @staticmethod
    def augment(image: np.ndarray) -> list:
        augmented = []

        # Flip horizontal
        augmented.append(cv2.flip(image, 1))

        # Brightness adjustment
        bright = cv2.convertScaleAbs(image, alpha=1.2, beta=20)
        augmented.append(bright)
        dark = cv2.convertScaleAbs(image, alpha=0.8, beta=-20)
        augmented.append(dark)

        # Gaussian blur (simulate motion blur)
        blurred = cv2.GaussianBlur(image, (3, 3), 0)
        augmented.append(blurred)

        # Slight rotation (-10 to +10 degrees)
        for angle in [-10, 10]:
            h, w = image.shape[:2]
            M = cv2.getRotationMatrix2D((w // 2, h // 2), angle, 1.0)
            rotated = cv2.warpAffine(image, M, (w, h))
            augmented.append(rotated)

        return augmented


# ============================================================
# Dataset Builder
# ============================================================
class BreastfeedingDataset:
    """รวบรวมและเตรียม dataset"""

    def __init__(self, config: TrainingConfig):
        self.config = config
        self.extractor = PoseFeatureExtractor(config)
        self.augmenter = DataAugmenter()

    def load_from_directory(self) -> tuple:
        """โหลดข้อมูลจาก directory structure"""
        data_path = Path(self.config.data_dir)
        X, y, metadata = [], [], []

        for label in ["correct", "incorrect"]:
            label_dir = data_path / label
            if not label_dir.exists():
                logger.warning(f"ไม่พบ directory: {label_dir}")
                continue

            # รองรับ sub-categories
            image_files = list(label_dir.rglob("*.jpg")) + \
                          list(label_dir.rglob("*.jpeg")) + \
                          list(label_dir.rglob("*.png"))

            logger.info(f"[{label}] พบภาพ {len(image_files)} ภาพ")

            for img_path in image_files:
                features = self.extractor.extract_from_image(str(img_path))
                if features is not None:
                    X.append(features)
                    y.append(label)
                    metadata.append({"path": str(img_path), "label": label})

                    # Data augmentation
                    if self.config.augment_data:
                        img = cv2.imread(str(img_path))
                        if img is not None:
                            aug_images = self.augmenter.augment(img)
                            for aug_img in aug_images[: self.config.augment_count]:
                                aug_feat = self._extract_from_numpy(aug_img)
                                if aug_feat is not None:
                                    X.append(aug_feat)
                                    y.append(label)
                                    metadata.append({
                                        "path": str(img_path) + "_aug",
                                        "label": label
                                    })

        self.extractor.close()

        if not X:
            raise ValueError("ไม่พบข้อมูลเพียงพอสำหรับการเทรน")

        return np.array(X), np.array(y), metadata

    def _extract_from_numpy(self, img: np.ndarray) -> Optional[np.ndarray]:
        img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        results = self.extractor.pose.process(img_rgb)
        holistic_results = self.extractor.holistic.process(img_rgb)
        if not results.pose_landmarks:
            return None
        return self.extractor._build_feature_vector(
            results, holistic_results, img.shape
        )


# ============================================================
# Model Trainer
# ============================================================
class BreastfeedingModelTrainer:
    """เทรนและประเมิน ensemble model"""

    def __init__(self, config: TrainingConfig):
        self.config = config
        os.makedirs(config.model_dir, exist_ok=True)

    def build_model(self) -> VotingClassifier:
        """สร้าง Ensemble model"""
        rf = RandomForestClassifier(
            n_estimators=self.config.n_estimators,
            max_depth=15,
            min_samples_split=4,
            random_state=self.config.random_state,
            n_jobs=-1,
        )
        gb = GradientBoostingClassifier(
            n_estimators=100,
            learning_rate=0.1,
            max_depth=5,
            random_state=self.config.random_state,
        )
        svc = SVC(
            kernel="rbf",
            probability=True,
            random_state=self.config.random_state,
        )
        ensemble = VotingClassifier(
            estimators=[("rf", rf), ("gb", gb), ("svc", svc)],
            voting="soft",
        )
        return ensemble

    def train(self, X: np.ndarray, y: np.ndarray) -> dict:
        """เทรนโมเดลและประเมินผล"""
        logger.info(f"ข้อมูลทั้งหมด: {len(X)} ตัวอย่าง | Features: {X.shape[1]}")
        logger.info(f"การแจกแจง: {dict(zip(*np.unique(y, return_counts=True)))}")

        # Encode labels
        le = LabelEncoder()
        y_encoded = le.fit_transform(y)

        # Train/test split
        X_train, X_test, y_train, y_test = train_test_split(
            X, y_encoded,
            test_size=self.config.test_size,
            random_state=self.config.random_state,
            stratify=y_encoded,
        )

        # Build pipeline (scaler + model)
        scaler = StandardScaler()
        model = self.build_model()

        pipeline = Pipeline([
            ("scaler", scaler),
            ("classifier", model),
        ])

        # Cross-validation
        logger.info("กำลัง Cross-validation...")
        cv = StratifiedKFold(
            n_splits=self.config.cv_folds,
            shuffle=True,
            random_state=self.config.random_state,
        )
        cv_scores = cross_val_score(pipeline, X_train, y_train, cv=cv, scoring="accuracy", n_jobs=-1)
        logger.info(f"CV Accuracy: {cv_scores.mean():.4f} ± {cv_scores.std():.4f}")

        # Final training
        logger.info("กำลังเทรน final model...")
        t0 = time.time()
        pipeline.fit(X_train, y_train)
        train_time = time.time() - t0
        logger.info(f"เทรนเสร็จใน {train_time:.1f} วินาที")

        # Evaluation
        y_pred = pipeline.predict(X_test)
        y_prob = pipeline.predict_proba(X_test)[:, 1]
        acc = accuracy_score(y_test, y_pred)
        report = classification_report(
            y_test, y_pred,
            target_names=le.classes_,
            output_dict=True,
        )
        conf_matrix = confusion_matrix(y_test, y_pred).tolist()

        logger.info(f"\nTest Accuracy: {acc:.4f}")
        logger.info(f"\n{classification_report(y_test, y_pred, target_names=le.classes_)}")

        # Save models
        model_path  = Path(self.config.model_dir) / "breastfeeding_classifier.pkl"
        scaler_path = Path(self.config.model_dir) / "keypoints_scaler.pkl"
        le_path     = Path(self.config.model_dir) / "label_encoder.pkl"

        with open(model_path,  "wb") as f: pickle.dump(pipeline, f)
        with open(le_path,     "wb") as f: pickle.dump(le, f)

        logger.info(f"บันทึกโมเดลที่: {model_path}")

        # Save report
        report_data = {
            "timestamp": datetime.now().isoformat(),
            "config": asdict(self.config),
            "dataset": {
                "total_samples": len(X),
                "train_samples": len(X_train),
                "test_samples": len(X_test),
                "feature_dim": X.shape[1],
                "class_distribution": dict(zip(*np.unique(y, return_counts=True))),
            },
            "results": {
                "cv_accuracy_mean": float(cv_scores.mean()),
                "cv_accuracy_std": float(cv_scores.std()),
                "test_accuracy": float(acc),
                "classification_report": report,
                "confusion_matrix": conf_matrix,
            },
            "model_paths": {
                "pipeline": str(model_path),
                "label_encoder": str(le_path),
            },
        }

        report_path = Path(self.config.model_dir) / "training_report.json"
        with open(report_path, "w", encoding="utf-8") as f:
            json.dump(report_data, f, ensure_ascii=False, indent=2)

        logger.info(f"รายงานบันทึกที่: {report_path}")
        return report_data


# ============================================================
# Real-time Inference Engine
# ============================================================
class BreastfeedingAnalyzer:
    """
    ใช้งาน real-time กับ webcam หรือ video stream
    ถูกเรียกใช้จาก web app ผ่าน API หรือ WebSocket
    """

    FEEDBACK_RULES = {
        "correct": [
            "✅ ท่าทางการให้นมถูกต้อง",
            "✅ ทารกอยู่ในตำแหน่งที่เหมาะสม",
        ],
        "incorrect": [
            "⚠️ ตรวจสอบมุมการอุ้มทารก — ให้ลำตัวทารกชิดอกมารดา",
            "⚠️ ไหล่ควรผ่อนคลาย ไม่ยกสูง",
            "⚠️ จมูกทารกควรโล่ง ไม่ถูกกดทับ",
            "⚠️ ปากทารกควรครอบคลุม areola ไม่ใช่เพียง nipple",
        ],
    }

    def __init__(self, model_dir: str = "models"):
        model_path = Path(model_dir) / "breastfeeding_classifier.pkl"
        le_path    = Path(model_dir) / "label_encoder.pkl"

        with open(model_path, "rb") as f:
            self.pipeline = pickle.load(f)
        with open(le_path, "rb") as f:
            self.label_encoder = pickle.load(f)

        self.extractor = PoseFeatureExtractor(TrainingConfig())
        self.mp_pose   = mp.solutions.pose
        self.mp_drawing = mp.solutions.drawing_utils

    def analyze_frame(self, frame: np.ndarray) -> dict:
        """วิเคราะห์ 1 frame และคืน result dict"""
        # เรียกใช้ฟังก์ชันใหม่ที่สร้างขึ้นด้านบน
        features, pose_results = self.extractor.extract_from_frame_with_results(frame)
        
        # เก็บผลลัพธ์ดิบไว้ใช้วาดในขั้นตอน draw_overlay
        self.current_pose_results = pose_results

        if features is None:
            return {
                "detected": False,
                "label": None,
                "confidence": 0.0,
                "feedback": ["กรุณาให้มองเห็นร่างกายอย่างชัดเจน"],
            }

        proba = self.pipeline.predict_proba([features])[0]
        pred_idx = np.argmax(proba)
        label = self.label_encoder.inverse_transform([pred_idx])[0]
        confidence = float(proba[pred_idx])

        feedback = self.FEEDBACK_RULES.get(label, [])

        return {
            "detected": True,
            "label": label,
            "label_th": "ถูกต้อง" if label == "correct" else "ไม่ถูกต้อง",
            "confidence": round(confidence * 100, 1),
            "all_probabilities": {
                self.label_encoder.inverse_transform([i])[0]: round(float(p) * 100, 1)
                for i, p in enumerate(proba)
            },
            "feedback": feedback,
        }

    def draw_overlay(self, frame: np.ndarray, result: dict) -> np.ndarray:
        """วาดโครงกระดูกและกล่องข้อความบน frame"""
        h, w = frame.shape[:2]

        # 1) วาดจุดข้อต่อและเส้นเชื่อม (Pose Landmarks) ถ้าตรวจเจอพิกัด
        if result["detected"] and self.current_pose_results and self.current_pose_results.pose_landmarks:
            # กำหนดสีของเส้นตามผลลัพธ์ (ถูกต้อง = เขียว, ไม่ถูกต้อง = แดง/ส้ม)
            line_color = (0, 200, 80) if result["label"] == "correct" else (0, 80, 220)
            
            self.mp_drawing.draw_landmarks(
                frame,
                self.current_pose_results.pose_landmarks,
                self.mp_pose.POSE_CONNECTIONS,
                self.mp_drawing.DrawingSpec(color=(255, 255, 255), thickness=2, circle_radius=2), # สีจุด (ขาว)
                self.mp_drawing.DrawingSpec(color=line_color, thickness=3, circle_radius=2)        # สีเส้นเชื่อม
            )

        # 2) วาดกล่องข้อความ UI (ส่วนหัวด้านบนของหน้าจอ)
        overlay = frame.copy()
        cv2.rectangle(overlay, (0, 0), (w, 80), (0, 0, 0), -1)
        cv2.addWeighted(overlay, 0.6, frame, 0.4, 0, frame)

        if result["detected"]:
            color = (0, 200, 80) if result["label"] == "correct" else (0, 80, 220)
            label_text = f"{result['label_th']}  {result['confidence']}%"
            cv2.putText(
                frame, label_text,
                (20, 50), cv2.FONT_HERSHEY_SIMPLEX, 1.2, color, 2
            )
            for i, fb in enumerate(result["feedback"][:2]):
                cv2.putText(
                    frame, fb,
                    (20, 90 + i * 30),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.6, (200, 200, 200), 1
                )
        else:
            cv2.putText(
                frame, "ไม่พบท่าทาง",
                (20, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (100, 100, 255), 2
            )
        return frame

    def run_webcam(self, camera_id: int = 0):
        """รัน real-time กับ webcam (สำหรับทดสอบ local)"""
        cap = cv2.VideoCapture(camera_id)
        cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
        cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)

        logger.info("เปิดกล้อง... กด 'q' เพื่อออก")
        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                break
            result = self.analyze_frame(frame)
            frame = self.draw_overlay(frame, result)
            cv2.imshow("Breastfeeding Pose Analyzer", frame)
            if cv2.waitKey(1) & 0xFF == ord("q"):
                break

        cap.release()
        cv2.destroyAllWindows()
        self.extractor.close()


# ============================================================
# Data Collection Helper
# ============================================================
class DataCollector:
    """
    ช่วยรวบรวม training data จาก webcam
    กด SPACE เพื่อบันทึกภาพ, กด 'q' เพื่อออก
    """

    def __init__(self, save_dir: str = "data", label: str = "correct"):
        self.save_dir = Path(save_dir) / label
        self.save_dir.mkdir(parents=True, exist_ok=True)
        self.label = label
        self.count = 0

    def collect(self, camera_id: int = 0):
        cap = cv2.VideoCapture(camera_id)
        logger.info(f"บันทึกข้อมูล [{self.label}] — SPACE=บันทึก, q=ออก")

        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                break

            display = frame.copy()
            cv2.putText(
                display,
                f"Label: {self.label} | Count: {self.count} | SPACE=save Q=quit",
                (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2
            )
            cv2.imshow("Data Collector", display)

            key = cv2.waitKey(1) & 0xFF
            if key == ord(" "):
                filename = self.save_dir / f"{self.label}_{self.count:04d}.jpg"
                cv2.imwrite(str(filename), frame)
                self.count += 1
                logger.info(f"บันทึก: {filename}")
            elif key == ord("q"):
                break

        cap.release()
        cv2.destroyAllWindows()
        logger.info(f"บันทึกทั้งหมด {self.count} ภาพ")


# ============================================================
# Main
# ============================================================
def create_demo_data():
    """สร้าง demo data structure (ใช้สำหรับทดสอบ pipeline)"""
    import random
    logger.info("สร้าง demo data structure...")
    for label in ["correct", "incorrect"]:
        os.makedirs(f"data/{label}", exist_ok=True)

    logger.info(
        "📁 วาง training images ที่:\n"
        "  data/correct/  — ภาพท่าทางที่ถูกต้อง\n"
        "  data/incorrect/ — ภาพท่าทางที่ไม่ถูกต้อง\n"
        "แล้วรัน: python train_model.py --train"
    )


def main():
    import argparse
    parser = argparse.ArgumentParser(description="Breastfeeding Pose Detection Trainer")
    parser.add_argument("--train",   action="store_true", help="เทรนโมเดล")
    parser.add_argument("--collect", action="store_true", help="รวบรวม training data")
    parser.add_argument("--label",   default="correct",   help="label สำหรับ collect (correct/incorrect)")
    parser.add_argument("--demo",    action="store_true", help="รัน webcam demo")
    parser.add_argument("--setup",   action="store_true", help="สร้าง data structure")
    args = parser.parse_args()

    if args.setup:
        create_demo_data()

    elif args.collect:
        collector = DataCollector(label=args.label)
        collector.collect()

    elif args.train:
        logger.info("=" * 60)
        logger.info(" Breastfeeding Pose Detection — Model Training")
        logger.info("=" * 60)

        dataset = BreastfeedingDataset(CONFIG)
        X, y, metadata = dataset.load_from_directory()

        trainer = BreastfeedingModelTrainer(CONFIG)
        results = trainer.train(X, y)

        logger.info("\n✅ การเทรนเสร็จสิ้น")
        logger.info(f"   Test Accuracy : {results['results']['test_accuracy']:.4f}")
        logger.info(f"   CV Accuracy   : {results['results']['cv_accuracy_mean']:.4f}")

    elif args.demo:
        analyzer = BreastfeedingAnalyzer()
        analyzer.run_webcam()

    else:
        parser.print_help()


if __name__ == "__main__":
    main()