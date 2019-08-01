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
  float my_x3y0 = dev->getColorCameraParams().my_x3y0;
  float my_x0y3 = dev->getColorCameraParams().my_x0y3;
  float my_x2y1 = dev->getColorCameraParams().my_x2y1;
  float my_x1y2 = dev->getColorCameraParams().my_x1y2;
  float my_x2y0 = dev->getColorCameraParams().my_x2y0;
  float my_x0y2 = dev->getColorCameraParams().my_x0y2;
  float my_x1y1 = dev->getColorCameraParams().my_x1y1;
  float my_x1y0 = dev->getColorCameraParams().my_x1y0;
  float my_x0y1 = dev->getColorCameraParams().my_x0y1;
  float my_x0y0 = dev->getColorCameraParams().my_x0y0;
  float fx = dev->getColorCameraParams().fx;
  float fy = dev->getColorCameraParams().fy;
  float cx = dev->getColorCameraParams().cx;
  float cy = dev->getColorCameraParams().cy;
  //printf("赤外線カメラのパラメータの中身は%f\n,%f\n,%f\n,%f\n,%f\n,%f\n,",my_x3y0,my_x0y3,my_x2y1,my_x1y2,my_x2y0,my_x0y2);
  printf("赤外線カメラのパラメータの中身は%f\n,%f\n,%f\n,%f\n",fx,fy,cx,cy);
  libfreenect2::Frame undistorted(512, 424, 4), registered(512, 424, 4), depth2rgb(1920, 1080 + 2, 4);;
  cv::Mat depthmatUndistorted, rgbd, rgbd2;

  return 0;
}
