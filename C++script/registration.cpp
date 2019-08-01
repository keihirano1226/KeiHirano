#include <libfreenect2/libfreenect2.hpp>
#include <libfreenect2/frame_listener_impl.h>
#include <libfreenect2/registration.h>
#include <libfreenect2/packet_pipeline.h>
#include <libfreenect2/logger.h>
#include <opencv2/core.hpp>
#include <opencv2/highgui.hpp>
#include <opencv2/imgcodecs.hpp>
#include <opencv2/opencv.hpp>
#include <string>
#include <sstream>
#include <iomanip>
#include <fstream>
#include <iostream>
#include <cstdio>
int main()
{
  bool enable_rgb = false;
  bool enable_depth =false;

  libfreenect2::Freenect2 freenect2;
  libfreenect2::Freenect2Device *dev = 0;
  libfreenect2::PacketPipeline *pipeline = 0;
  libfreenect2::Freenect2Device::Config config;
  config.MinDepth = 0.5f;
  config.MaxDepth = 8.0f;

  std::string serial = freenect2.getDefaultDeviceSerialNumber();
  if(freenect2.enumerateDevices() == 0)
  {
    std::cout << "no device connected!" << std::endl;
    return -1;
  }
  if (serial == "")
  {
    serial = freenect2.getDefaultDeviceSerialNumber();
  }
  printf("%s\n",serial.c_str());
  dev = freenect2.openDevice(serial);
  int types = 0;
  puts("TEST1");
  if (enable_rgb)
    types |= libfreenect2::Frame::Color;
    if (enable_depth)
      types |= libfreenect2::Frame::Ir | libfreenect2::Frame::Depth;
    libfreenect2::SyncMultiFrameListener listener(types);
    libfreenect2::FrameMap frames;
    dev->setConfiguration(config);
    dev->setColorFrameListener(&listener);
    dev->setIrAndDepthFrameListener(&listener);
    if (enable_rgb && enable_depth)
  {
    if (!dev->start()){
      puts("TEST1");
      return -1;
    }

  }
  else
  {
    if (!dev->startStreams(enable_rgb, enable_depth))
      return -1;
  }
  std::cout << "device serial: " << dev->getSerialNumber() << std::endl;
  std::cout << "device firmware: " << dev->getFirmwareVersion() << std::endl;
  libfreenect2::Registration* registration = new libfreenect2::Registration(dev->getIrCameraParams(), dev->getColorCameraParams());
  libfreenect2::Frame undistorted(512, 424, 4), registered(512, 424, 4), depth2rgb(1920, 1080 + 2, 4);;
  cv::Mat depthmatUndistorted, rgbd, rgbd2;
  while(true){
    static int i = 1;
    std::ostringstream oss;
    oss << std::setfill( '0' ) << std::setw( 10 ) << i++;

    //画像フォルダがあるパスを指定する部分
    cv::Mat rgbMat ;
    cv::Mat rgbtest ;
    cv::Mat depthtest ;
    cv::Mat depthMat ;
    cv::Mat Wrgbd ;
    rgbtest = cv::imread( "/home/kei/document/experiments/2019.07.10/color/" + oss.str() + ".jpg" );
    printf("%d\n", rgbtest.type());
    cv::cvtColor(rgbtest, rgbMat, cv::COLOR_BGR2BGRA);
    //depthtest =  cv::imread( "/home/kei/document/experiments/2019.06.25/data3/depth/" + oss.str() + ".png",2);
    depthtest =  cv::imread( "/home/kei/document/experiments/2019.07.10/depth/pngtest.png",2);
    depthtest.convertTo(depthMat, CV_32FC1);
    puts("color");
    printf("hello%i\n", depthMat.depth());
    libfreenect2::Frame rgb(rgbMat.cols, rgbMat.rows, 4, rgbMat.data);
    libfreenect2::Frame depth(512, 424, 4, depthMat.data);
    if(rgbMat.empty()){
      break;
    }
    // Register
    registration->apply(&rgb, &depth, &undistorted, &registered, true, &depth2rgb);
    registration->apply(&rgb, &depth, &undistorted, &registered);
    cv::Mat(undistorted.height, undistorted.width, CV_32FC1, undistorted.data).copyTo(depthmatUndistorted);
    cv::Mat(registered.height, registered.width, CV_8UC4, registered.data).copyTo(rgbd);
    cv::Mat(depth2rgb.height, depth2rgb.width, CV_32FC1, depth2rgb.data).copyTo(rgbd2);
    cv::imwrite("/home/kei/document/experiments/2019.07.10/regi/" + oss.str() + ".jpg",rgbd);
    rgbd2.convertTo(Wrgbd, CV_16UC1);
    printf("データ型は%d\n", Wrgbd.type());

  }
  cv::destroyAllWindows();
  return 0;
}
