import cv2
import pickle
import numpy

path = r"C:\Users\Brian\Desktop\BCS YR 2 NOTES\COMPUTER VISION\CarParking detection\pmparklot.jpg"
img = cv2.imread(path)
width, height = 110, 45
postList = []

# Load previously saved parking spots if available
try:
    with open("CarParkPos.pkl", "rb") as f:
        postList = pickle.load(f)
except FileNotFoundError:
    print("No previous annotations found.")
except pickle.UnpicklingError as e:
    print(f"Error loading pickle file: {e}")
    postList = []

def mouseClick(event, x, y, flags, params):
    global postList
    
    if event == cv2.EVENT_LBUTTONDOWN:  # Left mouse button clicked
        postList.append((x, y))
        print(f"Added parking spot at ({x}, {y})")
    
    elif event == cv2.EVENT_RBUTTONDOWN:  # Right mouse button clicked
        for i, pos in enumerate(postList):
            x1, y1 = pos
            if x1 < x < x1 + width and y1 < y < y1 + height:
                postList.pop(i)
                print(f"Removed parking spot at ({x1}, {y1})")
                break
    
    # Saving the updated postList to a pickle file
    with open("CarParkPos.pkl", "wb") as f:
        pickle.dump(postList, f)

# Create a named window and set mouse callback
cv2.namedWindow("Image")
cv2.setMouseCallback("Image", mouseClick)

while True:
    imgCopy = img.copy()
    
    # Draw rectangles on the image for each parking spot in postList
    for pos in postList:
        x1, y1 = pos
        cv2.rectangle(imgCopy, (x1, y1), (x1 + width, y1 + height), (255, 0, 255), 2)
    
    # Display the image with rectangles
    cv2.imshow("Image", imgCopy)
    cv2.waitKey(0)==ord('q')
    break

# Close all OpenCV windows
cv2.destroyAllWindows()
