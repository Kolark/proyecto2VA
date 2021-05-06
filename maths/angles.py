import numpy as np


class AnglesFromRig:
    """Clase para calcular los ángulos del rig"""

    @staticmethod
    def get_angles(rig):
        """
        Método para calcular y retornar los ángulos del rig respecto a la vertical
        """
        if len(rig) != 8:
            return (0, 0, 0, 0, 0)

        head = np.array(rig[1]) - np.array(rig[0])
        lArm = np.array(rig[2]) - np.array(rig[3])
        lFArm = np.array(rig[3]) - np.array(rig[4])
        rArm = np.array(rig[5]) - np.array(rig[6])
        rFArm = np.array(rig[6]) - np.array(rig[7])

        headAngle = np.rad2deg(np.arctan2(*head))
        lArmAngle = np.rad2deg(np.arctan2(*lArm))
        lFArmAngle = np.rad2deg(np.arctan2(*lFArm))
        rArmAngle = np.rad2deg(np.arctan2(*rArm))
        rFArmAngle = np.rad2deg(np.arctan2(*rFArm))

        return lArmAngle, lFArmAngle, rArmAngle, rFArmAngle, headAngle
