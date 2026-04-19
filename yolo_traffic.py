import cv2
from ultralytics import YOLO
import time
from collections import deque

model = YOLO("best.pt")
cap = cv2.VideoCapture("traffic.mp4")

CONF = 0.05
SCALE = 0.2

UPDATE_INTERVAL = 3
last_update = time.time()

green_lane = "TOP"
green_duration = 8
last_switch = time.time()

history = {
    "TOP": deque(maxlen=5),
    "BOTTOM": deque(maxlen=5),
    "LEFT": deque(maxlen=5),
    "RIGHT": deque(maxlen=5)
}

print("🚦 Smart Traffic System (Accurate + Emergency)")

LANES = {
    "TOP":    (300, 0, 900, 300),
    "BOTTOM": (300, 500, 900, 900),
    "LEFT":   (0, 250, 350, 800),
    "RIGHT":  (900, 250, 1280, 800)
}

# Pre-calc ROI areas (for fairness)
LANE_AREA = {}
for k,(x1,y1,x2,y2) in LANES.items():
    LANE_AREA[k] = (x2-x1)*(y2-y1)

emergency_lane = None

while True:
    ret, frame = cap.read()
    if not ret:
        break

    display = cv2.resize(frame, None, fx=SCALE, fy=SCALE)

    raw = {"TOP":0,"BOTTOM":0,"LEFT":0,"RIGHT":0}

    results = model(frame, conf=CONF, verbose=False)[0]

    for box in results.boxes:
        x1,y1,x2,y2 = map(int, box.xyxy[0])
        cx = (x1+x2)//2
        cy = (y1+y2)//2

        for lane,(lx1,ly1,lx2,ly2) in LANES.items():
            if lx1 < cx < lx2 and ly1 < cy < ly2:
                raw[lane] += 1

        # draw car box + label
        x1=int(x1*SCALE); x2=int(x2*SCALE)
        y1=int(y1*SCALE); y2=int(y2*SCALE)
        cv2.rectangle(display,(x1,y1),(x2,y2),(0,255,0),2)
        cv2.putText(display,"CAR",(x1,y1-5),
                    cv2.FONT_HERSHEY_SIMPLEX,0.5,(0,255,0),2)

    # Normalize by lane size (THIS FIXES BOTTOM ISSUE)
    density = {
        k: raw[k] / LANE_AREA[k]
        for k in raw
    }

    for k in density:
        history[k].append(density[k])

    smooth = {k: sum(history[k])/len(history[k]) for k in history}

    # 🚑 Emergency override (press E + number)
    key = cv2.waitKey(1) & 0xFF
    if key == ord("1"): emergency_lane = "TOP"
    if key == ord("2"): emergency_lane = "BOTTOM"
    if key == ord("3"): emergency_lane = "LEFT"
    if key == ord("4"): emergency_lane = "RIGHT"
    if key == ord("n"): emergency_lane = None

    if emergency_lane:
        green_lane = emergency_lane
        last_switch = time.time()

    elif time.time() - last_update > UPDATE_INTERVAL:

        active = {k:v for k,v in smooth.items() if v > 0}

        if active:
            green_lane = max(active, key=active.get)

        green_duration = max(6, int(smooth[green_lane]*2000))
        last_update = time.time()
        last_switch = time.time()

    # Draw ROIs
    for lane,(x1,y1,x2,y2) in LANES.items():
        x1=int(x1*SCALE); x2=int(x2*SCALE)
        y1=int(y1*SCALE); y2=int(y2*SCALE)
        cv2.rectangle(display,(x1,y1),(x2,y2),(255,0,0),2)
        cv2.putText(display,lane,(x1+5,y1+20),
                    cv2.FONT_HERSHEY_SIMPLEX,0.6,(255,0,0),2)

    # Traffic lights
    lights = {
        "TOP": (600, 40),
        "BOTTOM": (600, 640),
        "LEFT": (40, 420),
        "RIGHT": (1000, 420)
    }

    for lane,(lx,ly) in lights.items():
        lx=int(lx*SCALE); ly=int(ly*SCALE)
        color = (0,255,0) if lane == green_lane else (0,0,255)
        cv2.circle(display,(lx,ly),12,color,-1)

    # Info
    y = 25
    for k in raw:
        cv2.putText(display,f"{k}: {raw[k]}",
                    (10,y),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.7,(0,255,0),2)
        y+=22

    cv2.putText(display,f"GREEN → {green_lane}",
                (240,30),
                cv2.FONT_HERSHEY_SIMPLEX,0.8,(0,255,0),2)

    if emergency_lane:
        cv2.putText(display,"🚑 EMERGENCY MODE",
                    (240,60),
                    cv2.FONT_HERSHEY_SIMPLEX,0.8,(0,0,255),2)

    cv2.imshow("Smart Traffic Control System", display)

    if key == 27:
        break

cap.release()
cv2.destroyAllWindows()