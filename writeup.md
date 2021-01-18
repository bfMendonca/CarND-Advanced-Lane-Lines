## Writeup Template

### You can use this file as a template for your writeup if you want to submit it as a markdown file, but feel free to use some other method and submit a pdf if you prefer.

---

**Advanced Lane Finding Project**

The goals / steps of this project are the following:

* Compute the camera calibration matrix and distortion coefficients given a set of chessboard images.
* Apply a distortion correction to raw images.
* Use color transforms, gradients, etc., to create a thresholded binary image.
* Apply a perspective transform to rectify binary image ("birds-eye view").
* Detect lane pixels and fit to find the lane boundary.
* Determine the curvature of the lane and vehicle position with respect to center.
* Warp the detected lane boundaries back onto the original image.
* Output visual display of the lane boundaries and numerical estimation of lane curvature and vehicle position.

[//]: # (Image References)

[image1]: ./camera_cal/calibration1.jpg "Distorted"
[image2]: ./output_images/calibrated1.jpg "Undistorted"

[image3]: ./test_images/straight_lines1.jpg "Undistorted Straight Lines"
[image4]: ./output_images/und_straight_lines1.jpg "Undistorted Straight Lines"

[image5]: ./output_images/thresholding_example.png "Thresholding Example"

[image6]: ./output_images/warp_example.png "Perpective Transform Example"

[image7]: ./output_images/poly_example.png "Poly search Example"

[image8]: ./output_images/pipeline_example.png "Pipeline example"

[image2]: ./test_images/test1.jpg "Road Transformed"
[image3]: ./examples/binary_combo_example.jpg "Binary Example"
[image4]: ./examples/warped_straight_lines.jpg "Warp Example"
[image5]: ./examples/color_fit_lines.jpg "Fit Visual"
[image6]: ./examples/example_output.jpg "Output"
[video1]: ./project_video.mp4 "Video"

## [Rubric](https://review.udacity.com/#!/rubrics/571/view) Points

### Here I will consider the rubric points individually and describe how I addressed each point in my implementation.  

---

### Writeup / README

#### 1. Provide a Writeup / README that includes all the rubric points and how you addressed each one.  You can submit your writeup as markdown or pdf.  [Here](https://github.com/udacity/CarND-Advanced-Lane-Lines/blob/master/writeup_template.md) is a template writeup for this project you can use as a guide and a starting point.  

All of the project implementation were made at the "project.ipynb" file. The sections were divided in order to best describe the proccess and methods that were written in order to address those points

### Camera Calibration

#### 1. Briefly state how you computed the camera matrix and distortion coefficients. Provide an example of a distortion corrected calibration image.

For the camera calibration the images located at 'camera_cal' directory. The checkboard type used were the 9x6, as the checkboard imagens contains checkboards with 10 squares in the width and 7 squares at height. This process is implemented at the "project.ipynb" file, in the second cell. 

The checkboard corners were found by using the opencv method, findChessboardCorners, and, next, the distortion compensation matrix was calculated using the method "calibrateCamera" and the result saved in the "mtx" variable. 

![alt text][image2]

### Pipeline (single images)

#### 1. Provide an example of a distortion-corrected image.

For distortion correction the 'test_images/straight_lines1.jpg' image was loaded using imread and undistorted using the cv2.undistort with the camera calibration matrix mtx obtained using the proccess described above

![alt text][image3]
![alt text][image4]

#### 2. Describe how (and identify where in your code) you used color transforms, gradients or other methods to create a thresholded binary image.  Provide an example of a binary image result.

The process for extracting the lanes is presented at 'threshold_pipeline.py' in lines 1 through 45. The process started by applying the distortion correction to the image at the line 3, and, using this corrected image, converte it to the HLS color space. First, for the white lanes, the L channel was thresholded for high values Lightness values, line 14.

Secondly the yellow lanes were extracted using an HLS filter for yellow colors. The process for filtering yellow colors is implemented in lines 26 through 36. It's important to point out that the values for filtering the yellow color was based on the implementation discussed on the following link: 
https://medium.com/@tjosh.owoyemi/finding-lane-lines-with-colour-thresholds-beb542e0d839

![alt text][image5]

#### 3. Describe how (and identify where in your code) you performed a perspective transform and provide an example of a transformed image.

The code for my perspective transform includes a function called `perspective_transform()`  in the 4rd code cell of the IPython notebook.  The `perspective_transform()` function takes as inputs an image (`image`). This function relies on the fact that, on this IPython noteebok, the methods `cv2.getPerspectiveTransform(src, dst)` and `cv2.getPerspectiveTransform(dst, src)` with their output, M and Minv, saved to be used inside the `perspective_transform()`.

The `src` and `dst` points used for the `getPerspectiveTransform(src, dst)` and `cv2.getPerspectiveTransform(dst, src)` were the following:

| Source        | Destination   | 
|:-------------:|:-------------:| 
| 553, 480      | 450, 0        | 
| 731, 480      | w-450, 0      |
| 258, 680      | 450, h        |
| 1040, 680     | w-450, 0      |

I verified that my perspective transform was working as expected by drawing the `src` and `dst` points onto a test image and its warped counterpart to verify that the lines appear parallel in the warped image.

![alt text][image6]

#### 4. Describe how (and identify where in your code) you identified lane-line pixels and fit their positions with a polynomial?

The process for identifying the lane pixels were done in two steps. Both are written at the 5th code cell of the IPython notebook `project.ipynb`. The first is written at the method `find_lane_pixels( binary_warped)`, from lines 1 through 90. This method is to be used for the first detection or when the detection is lost. It will perform the search for the lane pixels using the histogram and sliding window technique, and return the lane pixels for the left lane and right lane. 

The second step is described at the method `search_around_poly(binary_warped, left_fit, right_fit)` and, besides the binary image, it will rely on the previously fitted 2nd order polynomials passed as the `left_fit` and `right_fit` as arguments for this methods. It will use the hyperparemeter `margin`, line 97, to specify which is space in each side of the polynomials in which this method sould search for the lane pixels. 

![all text][[image7]]

#### 5. Describe how (and identify where in your code) you calculated the radius of curvature of the lane and the position of the vehicle with respect to center.

The proccess for calculating the radius is located at the `project.ipynb`, in the 2nd code cell in lines 63 through 74. The calcualted radius is saved for each lane in the variable radius_of_curvature.

#### 6. Provide an example image of your result plotted back down onto the road such that the lane area is identified clearly.

I implemented this step in lines # through # in my code in `yet_another_file.py` in the function `map_lane()`.  Here is an example of my result on a test image:

![alt text][image8]

---

### Pipeline (video)

#### 1. Provide a link to your final video output.  Your pipeline should perform reasonably well on the entire project video (wobbly lines are ok but no catastrophic failures that would cause the car to drive off the road!).

Here's a [link to my video result](./test_videos_output/project_video.mp4)

---

### Discussion

#### 1. Briefly discuss any problems / issues you faced in your implementation of this project.  Where will your pipeline likely fail?  What could you do to make it more robust?

Here I'll talk about the approach I took, what techniques I used, what worked and why, where the pipeline might fail and how I might improve it if I were going to pursue this project further.  
