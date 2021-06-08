import cv2
import time
import numpy as np
net = cv2.dnn_DetectionModel("./yolov4-tiny.cfg", "yolov4-tiny.weights")
net.setInputSize(416, 416)
net.setInputScale(1.0 / 255)
net.setInputSwapRB(True)

import numpy as np
import time
import cv2
import os

labelsPath =  "coco.names"
LABELS = None
with open(labelsPath,'rt') as f:
    LABELS = f.read().rstrip('\n').split("\n")

np.random.seed(42)
COLORS = np.random.randint(0, 255, size=(len(LABELS), 3),dtype="uint8")

weightsPath = "yolov4.weights"
configPath = "yolo-coco/yolov4.cfg"
net = cv2.dnn.readNetFromDarknet(configPath, weightsPath)


frame = cv2.imread('./yolo.png')
cv2.imshow("frame",frame)
cv2.waitKey(0)
with open('./coco.names', 'rt') as f:
	names = f.read().rstrip('\n').split('\n')
print(names)

ln = net.getLayerNames()
ln = [ln[i[0] - 1] for i in net.getUnconnectedOutLayers()]
blob = cv2.dnn.blobFromImage(frame, 1 / 255.0, (416, 416),swapRB=True, crop=False)
net.setInput(blob)
start = time.time()
layerOutputs = net.forward(ln)
end = time.time()

print("[INFO] YOLO took {:.6f} seconds".format(end - start))

boxes = []
confidences = []
classIDs = []

for output in layerOutputs:
	for detection in output:
		scores = detection[5:]
		classID = np.argmax(scores)
		confidence = scores[classID]
		if confidence > 0.5:
			box = detection[0:4] * np.array([W, H, W, H])
			(centerX, centerY, width, height) = box.astype("int")
			x = int(centerX - (width / 2))
			y = int(centerY - (height / 2))
			boxes.append([x, y, int(width), int(height)])
			confidences.append(float(confidence))
			classIDs.append(classID)

idxs = cv2.dnn.NMSBoxes(boxes, confidences, 0.5,0.4)
if len(idxs) > 0:
	for i in idxs.flatten():
		(x, y) = (boxes[i][0], boxes[i][1])
		(w, h) = (boxes[i][2], boxes[i][3])
		color = [int(c) for c in COLORS[classIDs[i]]]
		cv2.rectangle(image, (x, y), (x + w, y + h), color, 2)
		text = "{}: {:.4f}".format(LABELS[classIDs[i]], confidences[i])
		cv2.putText(image, text, (x, y - 5), cv2.FONT_HERSHEY_SIMPLEX,
			0.5, color, 2)

cv2.imshow("Image", image)
cv2.waitKey(0)


startTime = time.time()
classes, confidences, boxes = net.detect(frame, confThreshold=0.1, nmsThreshold=0.1)
print(classes)
print(confidences)
print(boxes)
endTime = time.time()
print("Time: {}s".format(endTime-startTime))
for classId, confidence, box in zip(classes.flatten(), confidences.flatten(), boxes):
	label = '%.2f' % confidence
	label = '%s: %s' % (names[classId], label)
	labelSize, baseLine = cv.getTextSize(label, cv.FONT_HERSHEY_SIMPLEX, 0.5, 1)
	left, top, width, height = box
	top = max(top, labelSize[1])
	cv2.rectangle(frame, box, color=(0, 255, 0), thickness=3)
	cv2.rectangle(frame, (left, top - labelSize[1]), (left + labelSize[0], top + baseLine), (255, 255, 255), cv.FILLED)
	cv2.putText(frame, label, (left, top), cv.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0))

cv2.imshow('out', frame)
cv2.waitKey(0)