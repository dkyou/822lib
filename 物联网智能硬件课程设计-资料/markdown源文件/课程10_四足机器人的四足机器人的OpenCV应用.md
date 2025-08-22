# 课程10 四足机器人的OpenCV应用

## 课程概述 
在这个课程中，你将会学习Mini Pupper结合OpenCV推出的强大相机OAK-D-Lite，应用轻量级神经网络MobileNet实现目标跟踪的功能。
 
  - 演示1：启动stereo demo
![在这里插入图片描述](https://img-blog.csdnimg.cn/5b7a7e8f210748b8addd92047458cfc7.png)

  
  - 演示2：mini pupper的目标跟踪
![**此处有动画演示，存储在课程的文件夹中**](https://img-blog.csdnimg.cn/6a48ece0878e458cbaea5e8646167585.gif)



## 关于课程 
按照规划，本课程需要花费大约2小时来完成，目标受众为四足机器人开发爱好者。
**note**
本课程是基于[Mangdang](https://www.mangdang.net/)的Mini Pupper系列产品搭建的。
本课程涉及的源代码托管在Github，你可以[点击此处访问](https://github.com/mangdangroboticsclub/mini_pupper_ros/tree/ros2)。

## 学习目标**此处有动画演示，存储在课程的文件夹中**
在这个课程中，你将会学到：
 - 如何配置OpenCV官方的相机硬件OAK-D-Lite
 - 如何使用OAK-D-Lite
 - 如何制作一个mini pupper的目标跟踪示例
## 课程细节
本课程将使用以下组件：
 - [Ubuntu](https://ubuntu.com/)是一个以桌面应用为主的Linux操作系统，具有良好的版本维护和社区环境
 - [ROS](https://www.ros.org/)是一个机器人通用的开发的平台，可帮助您方便地构建机器人应用程序
 - [Rviz](http://wiki.ros.org/rviz/UserGuide)是ROS体系下的 3D 数据可视化工具
 - [OpenCV](https://opencv.org/) is an open-source computer vision and machine learning software library designed to help developers create applications for image and video processing.
 -  [MobileNet](https://github.com/tensorflow/models/tree/master/research/slim/nets/mobilenet) is a type of convolutional neural network architecture designed for efficient processing on mobile and embedded devices.

## 准备材料
在开始这个课程前，你需要具备以下知识：
 - **对ROS的基本了解**

在开始这个课程前，你需要准备好以下材料：
 - **安装有Ubuntu22.04系统并配置好ROS2 Humble环境的笔记本电脑**
 - **能够访问Github等网站的良好网络状态**
 - **OAK-D-Lite相机**

Note: 你可以通过Mangdang购买原装正品的OAK-D-Lite相机



# 引言
在本文中，我们将使用OpenCV的OAK-D-Lite深度相机配合mini pupper来实现一个简单的目标追踪示例。该示例使用深度相机获取场景中的图像，应用了OpenCV图像处理库，并使用简单的目标追踪算法，使得mini pupper的视线追踪你设置的目标，比如人类和瓶子。通过这个示例，我们可以了解到如何使用OpenCV和OAK-D-Lite深度相机实现目标追踪，以及深度相机在计算机视觉应用中的作用。





## 整体步骤
1. [配置OAK-D-Lite](#step1)
1. [使用OAK-D-Lite相机](#step2)
1. [了解MobileNet](#step3)
1. [配置mini pupper环境](#step4)
1. [运行mini pupper的目标追踪示例](#step5)



# 任务1：配置并使用OAK-D-Lite深度相机


<span id="step1"></span>
## 第一步：配置OAK-D-Lite
在运行深度相机前，需要对相机作配置。
- Install dependencies
```bash
sudo wget -qO- https://raw.githubusercontent.com/luxonis/depthai-ros/main/install_dependencies.sh | sudo bash
```
![请添加图片描述](https://img-blog.csdnimg.cn/68742cd47acb4b65a0d8db847fe1a94e.png)

**图片1：安装依赖**
- install OpenCV
```bash
sudo apt install libopencv-dev
```
![请添加图片描述](https://img-blog.csdnimg.cn/ff78cb8e33484adaa55801e2e3f8e8bb.png)

**图片2：安装OpenCV库**
- clone depthai-ros

DepthAI-ROS is a set of ROS (Robot Operating System) nodes that enable integration of the DepthAI hardware into ROS-based robotic systems. DepthAI is a platform that combines a depth camera with a neural compute device to enable depth perception and AI inference on edge devices.


The DepthAI-ROS nodes provide a set of ROS interfaces for accessing the depth and AI inference capabilities of the DepthAI hardware. The nodes can be used to perform tasks such as object detection, object tracking, and depth mapping, which are essential for many robotic applications.


Overall, DepthAI-ROS provides an easy-to-use interface for integrating DepthAI into ROS-based robotic systems, enabling developers to build more intelligent and capable robots.

```bash
mkdir -p dai_ws/src
cd dai_ws/src
git clone --branch humble https://github.com/luxonis/depthai-ros.git
```
![请添加图片描述](https://img-blog.csdnimg.cn/0baf59a576854a6ba0ace7ca29a43620.png)

**图片3：克隆depthai-ros库**
- install package dependencies
```bash
cd ..
rosdep install --from-paths src --ignore-src -r -y
```
![请添加图片描述](https://img-blog.csdnimg.cn/d8a3aab14de14af09f47dcd1c09e410d.png)

**图片4：安装相关包依赖**
- build depthai-ros
```bash
source /opt/ros/humble/setup.bash
MAKEFLAGS="-j1 -l1" colcon build
echo "source ~/dai_ws/install/setup.bash" >> ~/.bashrc
```
![请添加图片描述](https://img-blog.csdnimg.cn/8bfd0a99d44d48de9ee28544283fb827.png)

**图片5：编译depthai-ros**
Note: If you are using a lower end PC or RPi, standard building may take a lot of RAM and clog your PC. To avoid that, you can use build.sh command from your workspace (it just wraps colcon commands): ./src/depthai-ros/build.sh



<span id="step2"></span>
## 第二步： 使用OAK-D-Lite相机

在确认已经完成task1中的所有配置，并且没有出现错误时，开始使用OAK-D-Lite相机。
- 连接相机与USB3.0数据线
值得注意的是，数据线应当使用USB3.0及以上版本，当使用USB2.0时通常会发生很多错误。

- 连接相机与电脑/mini pupper
如果你希望直接使用电脑连接深度相机，将USB3.0线的另一端连接到电脑。如果你希望使用mini pupper连接深度相机，将USB3.0线的另一端连接到mini pupper上的USB3.0端口，端口的内部通常是蓝色的。我们建议你在mini pupper上使用OAK-D-Lite，因为在后续的目标跟踪的任务中将用到mini pupper的实体。

- 启动stereo.launch.py
```bash
ros2 launch depthai_examples stereo.launch.py camera_model:=OAK-D-LITE
```
![请添加图片描述](https://img-blog.csdnimg.cn/46677eb73fa34a60b084640442463b28.png)

**图片6：启动stereo**

你将观察到OAK-D-Lite发布的Stereo信息，并在RViz中可视化Stereo信息。
![在这里插入图片描述](https://img-blog.csdnimg.cn/6c55897c0e8041aa94e118cf7e1c7df0.png)

**图片7：Stereo信息**
![在这里插入图片描述](https://img-blog.csdnimg.cn/bc937fcbd36f45fe8488280b1887ea83.png)

**图片8：点赞的Stereo信息**


<span id="step3"></span>

# 任务2：了解MobileNet
## 第三步：什么是MobileNet？
MobileNet是一种轻量级的神经网络架构，旨在在移动和嵌入式设备上进行实时图像分类和目标检测。它由Google团队开发，采用了深度可分离卷积（depthwise separable convolution）的结构，这种结构可以大幅减少网络参数数量，从而在保持准确性的同时大幅降低了计算和存储资源的需求。MobileNet可以在移动设备上实现高效的图像分类和目标检测，因此被广泛应用于计算机视觉领域的移动端应用。
- 了解depthai_ros中关于使用MobileNet的示例

mobilenet_publisher.cpp is a C++ program that uses the `depthai` library and `ROS2` to run object detection on an input camera stream using a MobileNet-based neural network. It creates a pipeline that connects a color camera node to a MobileNet detection network node and then an output XLink node. The program creates two publishers, one for the camera stream and one for the detected objects.

The `createPipeline` function creates a `depthai` pipeline with a `ColorCamera` node, a `MobileNetDetectionNetwork` node, and an `XLinkOut` node. It sets some properties for the `ColorCamera`, such as the preview size, the resolution, the color order, and the frames per second (FPS). It also sets the confidence threshold and the blob path for the `MobileNetDetectionNetwork`. The function then links the nodes together in the pipeline.

The `main` function initializes `ROS2` and creates a node with the name "mobilenet\_node". It declares and retrieves some parameters, such as the tf prefix, the camera parameter URI, the resource base folder, the sync NN flag, and the NN name. It uses these parameters to create the pipeline and the `depthai` device. It then gets the output queues for the camera stream and the detected objects.

The program creates two `BridgePublisher` objects, one for the camera stream and one for the detected objects. The `BridgePublisher` objects use `ROS2` to publish messages to topics. They convert the `depthai` messages to ROS2 messages using `ImageConverter` and `ImgDetectionConverter`, respectively. The `ImageConverter` converts `ImgFrame` messages to `sensor_msgs::msg::Image` messages, and the `ImgDetectionConverter` converts `ImgDetections` messages to `vision_msgs::msg::Detection2DArray` messages.

The `detectionPublish` and `rgbPublish` objects add a publisher callback to the output queues. They call the `BridgePublisher::publish` function when there is data in the output queue. The `spin` function in `rclcpp` is called to start the ROS2 event loop.

```bash

#include <cstdio>
#include <iostream>

#include "camera_info_manager/camera_info_manager.hpp"
#include "depthai_bridge/BridgePublisher.hpp"
#include "depthai_bridge/ImageConverter.hpp"
#include "depthai_bridge/ImgDetectionConverter.hpp"
#include "rclcpp/executors.hpp"
#include "rclcpp/node.hpp"
#include "sensor_msgs/msg/image.hpp"
#include "vision_msgs/msg/detection2_d_array.hpp"

// Inludes common necessary includes for development using depthai library
#include "depthai/device/DataQueue.hpp"
#include "depthai/device/Device.hpp"
#include "depthai/pipeline/Pipeline.hpp"
#include "depthai/pipeline/node/ColorCamera.hpp"
#include "depthai/pipeline/node/DetectionNetwork.hpp"
#include "depthai/pipeline/node/XLinkOut.hpp"

dai::Pipeline createPipeline(bool syncNN, std::string nnPath) {
    dai::Pipeline pipeline;
    auto colorCam = pipeline.create<dai::node::ColorCamera>();
    auto xlinkOut = pipeline.create<dai::node::XLinkOut>();
    auto detectionNetwork = pipeline.create<dai::node::MobileNetDetectionNetwork>();
    auto nnOut = pipeline.create<dai::node::XLinkOut>();

    xlinkOut->setStreamName("preview");
    nnOut->setStreamName("detections");

    colorCam->setPreviewSize(300, 300);
    colorCam->setResolution(dai::ColorCameraProperties::SensorResolution::THE_1080_P);
    colorCam->setInterleaved(false);
    colorCam->setColorOrder(dai::ColorCameraProperties::ColorOrder::BGR);
    colorCam->setFps(40);

    // testing MobileNet DetectionNetwork
    detectionNetwork->setConfidenceThreshold(0.5f);
    detectionNetwork->setBlobPath(nnPath);

    // Link plugins CAM -> NN -> XLINK
    colorCam->preview.link(detectionNetwork->input);
    if(syncNN)
        detectionNetwork->passthrough.link(xlinkOut->input);
    else
        colorCam->preview.link(xlinkOut->input);

    detectionNetwork->out.link(nnOut->input);
    return pipeline;
}

int main(int argc, char** argv) {
    rclcpp::init(argc, argv);
    auto node = rclcpp::Node::make_shared("mobilenet_node");

    std::string tfPrefix, resourceBaseFolder, nnPath;
    std::string cameraParamUri = "package://depthai_examples/params/camera";
    std::string nnName(BLOB_NAME);
    bool syncNN;
    int bad_params = 0;

    node->declare_parameter("tf_prefix", "oak");
    node->declare_parameter("camera_param_uri", cameraParamUri);
    node->declare_parameter("resourceBaseFolder", "");
    node->declare_parameter("sync_nn", syncNN);
    node->declare_parameter<std::string>("nnName", "");

    node->get_parameter("tf_prefix", tfPrefix);
    node->get_parameter("camera_param_uri", cameraParamUri);
    node->get_parameter("sync_nn", syncNN);
    node->get_parameter("resourceBaseFolder", resourceBaseFolder);

    if(resourceBaseFolder.empty()) {
        throw std::runtime_error("Send the path to the resouce folder containing NNBlob in \'resourceBaseFolder\' ");
    }
    // Uses the path from param if passed or else uses from BLOB_PATH from CMAKE
    std::string nnParam;
    node->get_parameter("nnName", nnParam);
    if(nnParam != "x") {
        node->get_parameter("nnName", nnName);
    }

    nnPath = resourceBaseFolder + "/" + nnName;
    dai::Pipeline pipeline = createPipeline(syncNN, nnPath);
    dai::Device device(pipeline);

    std::shared_ptr<dai::DataOutputQueue> previewQueue = device.getOutputQueue("preview", 30, false);
    std::shared_ptr<dai::DataOutputQueue> nNetDataQueue = device.getOutputQueue("detections", 30, false);

    std::string color_uri = cameraParamUri + "/" + "color.yaml";

    // TODO(sachin): Add option to use CameraInfo from EEPROM
    dai::rosBridge::ImageConverter rgbConverter(tfPrefix + "_rgb_camera_optical_frame", false);
    dai::rosBridge::BridgePublisher<sensor_msgs::msg::Image, dai::ImgFrame> rgbPublish(previewQueue,
                                                                                       node,
                                                                                       std::string("color/image"),
                                                                                       std::bind(&dai::rosBridge::ImageConverter::toRosMsg,
                                                                                                 &rgbConverter,  // since the converter has the same frame name
                                                                                                                 // and image type is also same we can reuse it
                                                                                                 std::placeholders::_1,
                                                                                                 std::placeholders::_2),
                                                                                       30,
                                                                                       color_uri,
                                                                                       "color");

    dai::rosBridge::ImgDetectionConverter detConverter(tfPrefix + "_rgb_camera_optical_frame", 300, 300, false);
    dai::rosBridge::BridgePublisher<vision_msgs::msg::Detection2DArray, dai::ImgDetections> detectionPublish(
        nNetDataQueue,
        node,
        std::string("color/mobilenet_detections"),
        std::bind(&dai::rosBridge::ImgDetectionConverter::toRosMsg, &detConverter, std::placeholders::_1, std::placeholders::_2),
        30);

    detectionPublish.addPublisherCallback();
    rgbPublish.addPublisherCallback();  // addPublisherCallback works only when the dataqueue is non blocking.

    rclcpp::spin(node);

    return 0;
}
```
这篇代码的版权为depthai所有，如果你希望查看他们构建的本篇相关完整代码和其他代码，请查看以下链接。
[参考链接： mobilenet_publisher](https://github.com/luxonis/depthai-ros/blob/humble/depthai_examples/src/mobilenet_publisher.cpp)
[参考链接： depthai-ros](https://github.com/luxonis/depthai-ros)


<span id="step4"></span>

# 任务3：运行目标追踪示例
## 第四步：配置mini pupper环境


Before we can start run object tracking on the Mini Pupper, we need to make sure our environment is configured. This task consists of two steps:

### Step 1: Configure the PC
PC Setup corresponds to PC (your desktop or laptop PC) for controlling Mini Pupper remotely or executing the simulator.

#### 1.1 ROS 2 installation
Please follow the [installation document for ROS Humble](https://docs.ros.org/en/humble/Installation/Ubuntu-Install-Debians.html) or use the [unofficial ROS 2 installation script](https:// github.com/Tiryoh/ros2_setup_scripts_ubuntu).

#### 1.2 Download the Mini Pupper ROS 2 & dependencies packages
After ROS 2 installation, download the Mini Pupper ROS package in the workspace.
```bash
mkdir -p ~/ros2_ws/src
cd ~/ros2_ws/src
git clone https://github.com/mangdangroboticsclub/mini_pupper_ros.git -b ros2
vcs import < mini_pupper_ros/.minipupper.repos --recursive # requires vcstool
```
**Notes:**
If you haven't installed vcstool, please install vcstool first.
```bash
sudo sh -c 'echo "deb http://packages.ros.org/ros/ubuntu $(lsb_release -sc) main" > /etc/apt/sources.list.d/ros-latest.list'
sudo apt install curl # if you haven't already installed curl
curl -s https://raw.githubusercontent.com/ros/rosdistro/master/ros.asc | sudo apt-key add -
sudo apt-get update
sudo apt-get install python3-vcstool
```
#### 1.3 Build and install all ROS packages
```bash
cd ~/ros2_ws
rosdep install --from-paths src --ignore-src -r -y
sudo apt-get install ros-humble-teleop-twist-keyboard
pip install transforms3d
colcon build --symlink-install
```
### Step 2: Configure Mini Pupper
Mini Pupper Setup corresponds to the Raspberry Pi on your Mini Pupper.
#### 2.1 mini_pupper_bsp installation
You should first install dependencies of servos, battery monitor, and display screen.
See [mini_pupper_bsp](https://github.com/mangdangroboticsclub/mini_pupper_bsp).

#### 2.2 ROS 2 installation
After installing the driver software, install ROS 2. ROS 2 Humble is required.
Please follow the [installation document for ROS Humble](https://docs.ros.org/en/humble/Installation/Ubuntu-Install-Debians.html) or use the [unofficial ROS 2 installation script](https:// github.com/Tiryoh/ros2_setup_scripts_ubuntu).

<span id="step5"></span>

## 第五步：运行mini pupper的目标追踪示例
mini pupper的目标追踪示例将从处理depthai_ros中发出的信息，并进行处理，转化为mini pupper的运动指令。其中用到了geometry_msgs.msg中的消息接口 Pose和vision_msgs.msg 中的消息接口 Detection2DArray。
- 了解geometry_msgs.msg中的消息接口 Pose
```bash
# A representation of pose in free space, composed of position and orientation.

Point position
	float64 x
	float64 y
	float64 z
Quaternion orientation
	float64 x 0
	float64 y 0
	float64 z 0
	float64 w 1

```
- 安装vision_msgs
vision_msgs并不是ROS2安装时就自带安装的消息类型，你需要打开命令行执行如下代码，并安装vision_msgs。

```bash
sudo apt install ros-humble-vision-msgs
```



- 了解vision_msgs.msg 中的消息接口 Detection2DArray

Detection2DArray interface consists of two message types: std_msgs/Header and Detection2D. 


The std_msgs/Header message contains fields for the message header, consisting of a time stamp (which includes fields for seconds and nanoseconds) and a frame_id string.


The Detection2D message contains fields for a list of detections generated by a multi-proposal detector, including the fields for the message header (again consisting of a time stamp and a frame_id). It also contains an array of ObjectHypothesisWithPose, where each ObjectHypothesisWithPose contains an ObjectHypothesis (which consists of a class_id string and a score float64) and a geometry_msgs/PoseWithCovariance message (which in turn consists of a geometry_msgs/pose message, a float64[36] covariance array, and a BoundingBox2D message). The BoundingBox2D message contains a vision_msgs/Pose2D message (which includes vision_msgs/Point2D message and a float64 theta) and size_x and size_y float64 values.

```bash
# A list of 2D detections, for a multi-object 2D detector.

std_msgs/Header header
	builtin_interfaces/Time stamp
		int32 sec
		uint32 nanosec
	string frame_id

# A list of the detected proposals. A multi-proposal detector might generate
#   this list with many candidate detections generated from a single input.
Detection2D[] detections
	#
	std_msgs/Header header
		builtin_interfaces/Time stamp
			int32 sec
			uint32 nanosec
		string frame_id
	ObjectHypothesisWithPose[] results
		ObjectHypothesis hypothesis
			string class_id
			float64 score
		geometry_msgs/PoseWithCovariance pose
			Pose pose
				Point position
					float64 x
					float64 y
					float64 z
				Quaternion orientation
					float64 x 0
					float64 y 0
					float64 z 0
					float64 w 1
			float64[36] covariance
	BoundingBox2D bbox
		vision_msgs/Pose2D center
			vision_msgs/Point2D position
				float64 x
				float64 y
			float64 theta
		float64 size_x
		float64 size_y
	string id
```



- 启动oak-d-lite mobile_publisher
mobile_publisher将发出/color/mobilenet_detections话题
```bash
ros2 launch depthai_examples mobile_publisher.launch.py camera_model:=OAK-D-LITE
```
![在这里插入图片描述](https://img-blog.csdnimg.cn/227e289c36de43d2bd24e99b56070ceb.png)

**图片9：启动oak-d-lite mobile_publisher**
- 启动mini pupper目标检测示例
```bash
ros2 launch mini_pupper_examples object_tracking.launch.py camera_model:=OAK-D-LITE
```
![在这里插入图片描述](https://img-blog.csdnimg.cn/a74008ddcbd74c65890847d4005c2b2d.gif)

如果希望了解具体的代码细节，可以查看以下链接。
[参考链接：mini_pupper_ros](https://github.com/mangdangroboticsclub/mini_pupper_ros/tree/ros2)



# 总结Summary

经过本课程的学习，你应该能达到以下水平：
| 知识点 | 内容 | 了解|熟悉|掌握|
|--|--|--|--|--|
OpenCV|应用OpenCV的视频流处理|&#10004;|||
OAK-D-Lite|OAK-D-Lite的使用|||&#10004;|
神经网络应用|MobileNet|&#10004;|||
目标跟踪|mini_pupper的目标跟踪应用||&#10004;||


<span id="backinfo"></span>
# 背景信息和资源Background Information and Resources
      
[参考链接：mini_pupper_ros](https://github.com/mangdangroboticsclub/mini_pupper_ros/tree/ros2)
[参考链接： depthai 二维码识别](https://github.com/luxonis/depthai-experiments/tree/master/gen2-qr-code-scanner)
[参考链接： depthai有趣的demo](https://github.com/luxonis/depthai-experiments)
[参考链接： depthai-ros](https://github.com/luxonis/depthai-ros)
[参考链接： mobilenet_publisher](https://github.com/luxonis/depthai-ros/blob/humble/depthai_examples/src/mobilenet_publisher.cpp)
[参考链接：depthai ObjectTracker](https://docs.luxonis.com/projects/api/en/latest/components/nodes/object_tracker/)
[参考链接：depthai官方文档](https://docs.luxonis.com/en/latest/)
[Reference : Mini Pupper Source Code on GitHub](https://github.com/mangdangroboticsclub/mini_pupper_ros/tree/ros2)

**版权信息：教材尚未完善，此处预留版权信息处理方式**
mini pupper相关内容可访问：[https://github.com/mangdangroboticsclub](https://github.com/mangdangroboticsclub)






