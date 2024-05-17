"""
This solution uses cv2 and its matchTemplate function.
"""

import cv2

# pip install opencv-python

base = "2024/oqdrachtx/Verdediging_2/Bezoeker in Nood/"


sat_image = cv2.imread(base + "sat_beeld_1337.png")
target_image = cv2.imread(base + "suspicious_observation.png")

result = cv2.matchTemplate(target_image, sat_image, cv2.TM_SQDIFF)

closest_result = cv2.minMaxLoc(result)

print(f"You should check the pixel coords near {closest_result[2]}")
