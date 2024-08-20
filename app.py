# import install_dependencies
from flask import Flask, Response
import cv2

# from flask import Flask, Response, request, jsonify
# # from flask_cors import CORS
# # import cv2
# # import mediapipe as mp
# import numpy as np
# from io import BytesIO
# import firebase_admin
# from firebase_admin import credentials, storage
# # import face_recognition
# from PIL import Image


# # Initialize Firebase Admin
# cred = credentials.Certificate('config/ramsproject321-75e29-firebase-adminsdk-x4imw-6e12dd9db2.json')
# firebase_admin.initialize_app(cred, {'storageBucket': 'ramsproject321-75e29.appspot.com'})

app = Flask(__name__)
# # CORS(app)  # Enable CORS



current_frame = None
camera = None
is_camera_running = False


def generate_frames():
    
    global current_frame
    global camera
    # camera = cv2.VideoCapture(0)
    # cap = cv2.VideoCapture(0)
    try:
        while is_camera_running:
            success, frame = camera.read()
            if not success:
                break
            
            current_frame = frame.copy() 
            
            # Convert frame to RGB
            rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            # Detect faces
            # results = face_detection.process(rgb_frame)
            # if results.detections:
            #     for detection in results.detections:
            #         bboxC = detection.location_data.relative_bounding_box
            #         h, w, _ = frame.shape
            #         bbox = int(bboxC.xmin * w), int(bboxC.ymin * h), \
            #             int(bboxC.width * w), int(bboxC.height * h)
            #         cv2.rectangle(frame, bbox, (0, 255, 0), 2)
            # Encode the frame in JPEG format
            ret, buffer = cv2.imencode('.jpg', frame)
            frame = buffer.tobytes()
            yield (b'--frame\r\n'
                b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')        
    finally:
        print("Final Camera Close")


@app.route('/start_camera', methods=['GET'])
def start_camera():
    global camera, is_camera_running
    if not is_camera_running:
        camera = cv2.VideoCapture(0)
        is_camera_running = True
    return "Camera started", 200


@app.route('/video_feed',methods=['GET'])
def video_feed():
    global is_camera_running
    global camera
    if is_camera_running:
        return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')
    else:
        return "Camera is not running", 400
    

@app.route('/stop_camera', methods=['GET'])
def stop_camera():
    global camera, is_camera_running
    if camera is not None:
        camera.release()
        camera = None
    is_camera_running = False
    return "Camera stopped", 200


@app.route('/hello', methods=['GET'])
def hello():
    return Response("Hello")





@app.route('/')
def method_01():
    return "It is Working Very Well"


# if __name__ == '__main__':
#     app.run(debug=True)




# # mp_face_detection = mp.solutions.face_detection
# # face_detection = mp_face_detection.FaceDetection()



# current_frame = None
# camera = None
# is_camera_running = False


# def fetch_images_from_firebase():
#     bucket = storage.bucket()
#     blobs = bucket.list_blobs()
#     images = []

#     for blob in blobs:
#         image_data = blob.download_as_bytes()
#         image_np = np.frombuffer(image_data, np.uint8)
#         image_np = cv2.imdecode(image_np, cv2.IMREAD_COLOR)
        
#         if image_np is not None:
#             encodings = face_recognition.face_encodings(image_np)
#             if encodings:
#                 images.append((blob.name, encodings[0]))

#     return images

# known_faces = fetch_images_from_firebase()




        
# def generate_frames():
    
#     global current_frame
#     global camera
#     # camera = cv2.VideoCapture(0)
#     # cap = cv2.VideoCapture(0)
#     try:
#         while is_camera_running:
#             success, frame = camera.read()
#             if not success:
#                 break
            
#             current_frame = frame.copy() 
            
#             # Convert frame to RGB
#             rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
#             # Detect faces
#             results = face_detection.process(rgb_frame)
#             if results.detections:
#                 for detection in results.detections:
#                     bboxC = detection.location_data.relative_bounding_box
#                     h, w, _ = frame.shape
#                     bbox = int(bboxC.xmin * w), int(bboxC.ymin * h), \
#                         int(bboxC.width * w), int(bboxC.height * h)
#                     cv2.rectangle(frame, bbox, (0, 255, 0), 2)
#             # Encode the frame in JPEG format
#             ret, buffer = cv2.imencode('.jpg', frame)
#             frame = buffer.tobytes()
#             yield (b'--frame\r\n'
#                 b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')        
#     finally:
#         print("Final Camera Close")


# @app.route('/start_camera', methods=['GET'])
# def start_camera():
#     global camera, is_camera_running
#     if not is_camera_running:
#         camera = cv2.VideoCapture(0)
#         is_camera_running = True
#     return "Camera started", 200


# @app.route('/video_feed')
# def video_feed():
#     global is_camera_running
#     global camera
#     if is_camera_running:
#         return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')
#     else:
#         return "Camera is not running", 400
    

# @app.route('/stop_camera', methods=['GET'])
# def stop_camera():
#     global camera, is_camera_running
#     if camera is not None:
#         camera.release()
#         camera = None
#     is_camera_running = False
#     return "Camera stopped", 200


# @app.route('/capture', methods=['POST'])
# def capture():
#     global current_frame
#     # success, frame = camera.read()
#     if current_frame is None:
#         return jsonify({"error": "No frame available"})


#     username = request.form.get('username')
#     if not username:
#         return jsonify({"error": "Username is required"})
    
#     rgb_frame = cv2.cvtColor(current_frame, cv2.COLOR_BGR2RGB)
#     face_locations = face_recognition.face_locations(rgb_frame)
#     # results = face_detection.process(rgb_frame)
#     # print(len(face_locations))
#     if len(face_locations) == 1:
#         filename = f"{username}.jpg"
#         cv2.imwrite(f"captured_images/{filename}", current_frame)
#         bucket = storage.bucket()
#         blob = bucket.blob(f"captured_images/{filename}")
#         blob.upload_from_filename(f"captured_images/{filename}")
#         print("Image_Uploaded in firebase.")
#         image_url = blob.public_url
#         print(image_url)
#         return jsonify({"message": "stored", "image_url": image_url})
#     else:
#         return jsonify({"error": "No face or multiple faces detected"})
    
    
    
    



# @app.route('/recognize', methods=['POST'])
# def recognize():
#     global current_frame
#     if current_frame is None:
#         return jsonify({"error": "No frame available"})

#     # Detect faces in the current frame
#     face_locations = face_recognition.face_locations(current_frame)
#     face_encodings = face_recognition.face_encodings(current_frame, face_locations)

#     recognized_names = []
#     for face_encoding in face_encodings:
#         matches = face_recognition.compare_faces([encoding for _, encoding in known_faces], face_encoding)
#         name = "Unknown"

#         if True in matches:
#             first_match_index = matches.index(True)
#             name = known_faces[first_match_index][0]

#         recognized_names.append(name[16:])

#     return jsonify({"names": recognized_names})




