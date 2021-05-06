import cv2
import numpy as np

from maths.angles import AnglesFromRig
from maths.predictive_filter import PredictiveFilter


class PoseEstimation:
    """
    Clase para calcular la pose
    """

    def __init__(self):
        """
        Constructor de la clase

        :param pose_type: Enenumerador del tipo de pose a calcular
        """

        MODE = "COCO"

        if MODE == "COCO":
            proto_file = "pose/coco/pose_deploy_linevec.prototxt"
            weights_file = "pose/coco/pose_iter_440000.caffemodel"
            self.n_points = 8

        elif MODE == "MPI":
            proto_file = "pose/mpi/pose_deploy_linevec_faster_4_stages.prototxt"
            weights_file = "pose/mpi/pose_iter_160000.caffemodel"
            self.n_points = 8

        self.IN_WIDTH = 168
        self.IN_HEIGHT = 168
        self.THRESHOLD = 0.2

        PREDICTIVE_DEPTH = 1

        self.net = cv2.dnn.readNetFromCaffe(proto_file, weights_file)

        self.pdv_l_arm = PredictiveFilter(PREDICTIVE_DEPTH)
        self.pdv_l_farm = PredictiveFilter(PREDICTIVE_DEPTH)
        self.pdv_r_arm = PredictiveFilter(PREDICTIVE_DEPTH)
        self.pdv_r_farm = PredictiveFilter(PREDICTIVE_DEPTH)
        self.pdv_head = PredictiveFilter(PREDICTIVE_DEPTH)

    def is_in_pose(self, frame):
        """
        Calcula si la pose es correcta

        :param frame: Frame de la cámara
        :returns: Bool de si la pose es correcta o no dependiendo del tipo de pose dado en el constructor
        """

        frame_width = frame.shape[1]
        frame_height = frame.shape[0]

        input_blob = cv2.dnn.blobFromImage(
            frame, 1.0 / 255, (self.IN_WIDTH, self.IN_HEIGHT), (0, 0, 0), swapRB=False, crop=False)
        self.net.setInput(input_blob)
        output = self.net.forward()
        H = output.shape[2]
        W = output.shape[3]

        points = []  # Empty list to store the detected keypoints

        for i in range(self.n_points):
            # confidence map of corresponding body's part.
            probMap = output[0, i, :, :]
            # Find global maxima of the probMap.
            _, prob, _, point = cv2.minMaxLoc(probMap)
            # Scale the point to fit on the original image
            x = int(frame_width * point[0] / W)
            # Scale the point to fit on the original image
            y = int(frame_height * point[1] / H)

            if prob > self.THRESHOLD:
                points.append((x, y))

        self.l_arm_angle, self.l_farm_angle, self.r_arm_angle, self.r_farm_angle, self.head_angle = AnglesFromRig.get_angles(
            points)

        self.l_arm_angle = self.pdv_l_arm.update(self.l_arm_angle)
        self.l_farm_angle = self.pdv_l_farm.update(self.l_farm_angle)
        self.r_arm_angle = self.pdv_r_arm.update(self.r_arm_angle)
        self.r_farm_angle = self.pdv_r_farm.update(self.r_farm_angle)
        self.head_angle = self.pdv_head.update(self.head_angle)

        # Calcula si está en la pose de brazos cruzados
        is_pose = (135 < self.l_arm_angle < 175 and
                   -40 > self.l_farm_angle > -90 and
                   -135 > self.r_arm_angle > -175 and
                   40 < self.r_farm_angle < 90 )

        return is_pose
