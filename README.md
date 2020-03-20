Road detection by yolov3 (darknet/AlexeyAB), Image processing with OpenCV.

Firstly go to AlexeyAB repo and follow his instructions.

Then download my trained wheights from: https://drive.google.com/open?id=1KsE6PM0VY4pMUWoJWezdTAiQHrJ_6EAH

Then run: ./darknet detector test build/darknet/x64/data/obj.data cfg/yolo-obj.cfg yolo-obj_4000.weights -ext_output -dont_show -out result.json -thresh 0.15 test1.jpg

You will see the results at predictions.jpg

Finally run: python3 project.py

Check the output at dst.jpg


