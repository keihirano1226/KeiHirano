#include <iostream>
#include <string>
#include <fstream>
#include <sstream>
#include <libfreenect2/libfreenect2.hpp>
#include <libfreenect2/frame_listener_impl.h>
#include <libfreenect2/registration.h>
#include <libfreenect2/packet_pipeline.h>
#include <libfreenect2/logger.h>
#include <opencv2/core.hpp>
#include <opencv2/highgui.hpp>
#include <opencv2/imgcodecs.hpp>
#include <opencv2/opencv.hpp>

int stoi(std::string str){
int ret;
std::stringstream ss;

ss << str;
ss >> ret;
return ret;
}

int main()
{
  bool enable_rgb = false;
  bool enable_depth =false;
  //libfreenect2::setGlobalLogger(libfreenect2::createConsoleLogger(libfreenect2::Logger::Debug));
  FILE *fp;
  //std::random_device rnd;
  libfreenect2::Freenect2 freenect2;
  libfreenect2::Freenect2Device *dev = 0;
  libfreenect2::PacketPipeline *pipeline = 0;
  libfreenect2::Freenect2Device::Config config;
  config.MinDepth = 0.5f;
  config.MaxDepth = 8.0f;
  float x,y,z;
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

  fp=fopen("/home/kei/document/experiments/KinectTest/randsave(25,400).csv","w");
  fprintf(fp,"r,c,j,x,y,z,\n");
  for ( int i = 500; i < 2000 ; ++i  ) {
    //int r = rand()%424;
    int r = 25;
    //int c = rand()%512;
    int c = 400;
    int j = 500 + rand()%7500;
    cv::Mat depthtest ;
    cv::Mat depthMat ;
    //depthtest =  cv::imread( "/home/kei/document/experiments/2019.06.25/data3/depth_mirror/" + oss.str() + ".png",2);
    depthtest = cv::Mat::ones(512, 424, CV_16UC1)*i;
    depthtest.convertTo(depthMat, CV_32FC1);
    libfreenect2::Frame depth(512, 424, 4, depthMat.data);
    registration->undistortDepth(&depth, &undistorted);
    registration->getPointXYZ(&undistorted,r,c,x,y,z);
    fprintf(fp,"%d,%d,%d,%f,%f,%f,\n",r,c,i,x,y,z);
    }




  return 0;
}
