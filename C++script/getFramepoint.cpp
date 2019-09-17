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


  libfreenect2::Freenect2 freenect2;
  libfreenect2::Freenect2Device *dev = 0;
  libfreenect2::PacketPipeline *pipeline = 0;
  libfreenect2::Freenect2Device::Config config;
  config.MinDepth = 0.0f;
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
  std::ifstream stream("/home/kei/document/experiments/BioEngen/ana/2DGround.csv");
  std::string line;
  const std::string delim = ",";
  int row = 0;
  //int row1 = 0;
  int col;
  puts("hello");

  int data[5][2];
  while ( getline(stream, line) ) {
    col = 0;
    for ( std::string::size_type spos, epos = 0;
        (spos = line.find_first_not_of(delim, epos)) != std::string::npos;) {
      std::string token = line.substr(spos,(epos = line.find_first_of(delim, spos))-spos);
      data[row][col++] = stoi(token);
    }
    ++row;
  }
  FILE *fp;
  fp=fopen("/home/kei/document/experiments/BioEngen/ana/3points3d.csv","w");
  cv::Mat depthtest ;
  cv::Mat depthMat ;
  //depth画像を読み込む
  depthtest =  cv::imread( "/home/kei/document/experiments/BioEngen/MA330_11/depth_mirror/0000000750.png",2);
  depthtest.convertTo(depthMat, CV_32FC1);
  libfreenect2::Frame depth(512, 424, 4, depthMat.data);
  registration->undistortDepth(&depth, &undistorted);
  //printf("%d,%d\n",data[0][0],data[0][1]);
  //registration->getPointXYZ(&undistorted,data[0][0],data[0][1],x,y,z);
  //fprintf(fp,"%f,%f,%f\n",x,y,z);
  //registration->getPointXYZ(&undistorted,data[1][0],data[1][1],x,y,z);
  //fprintf(fp,"%f,%f,%f\n",x,y,z);
  //registration->getPointXYZ(&undistorted,data[2][0],data[2][1],x,y,z);
  //fprintf(fp,"%f,%f,%f\n",x,y,z);
  registration->getPointXYZ(&undistorted,data[0][1],data[0][0],x,y,z);
  fprintf(fp,"%f,%f,%f\n",x,y,z);
  registration->getPointXYZ(&undistorted,data[1][1],data[1][0],x,y,z);
  fprintf(fp,"%f,%f,%f\n",x,y,z);
  registration->getPointXYZ(&undistorted,data[2][1],data[2][0],x,y,z);
  fprintf(fp,"%f,%f,%f\n",x,y,z);
  registration->getPointXYZ(&undistorted,data[3][1],data[3][0],x,y,z);
  fprintf(fp,"%f,%f,%f\n",x,y,z);
  registration->getPointXYZ(&undistorted,data[4][1],data[4][0],x,y,z);
  fprintf(fp,"%f,%f,%f\n",x,y,z);
  //registration->getPointXYZ(&undistorted,data[2][1],data[2][0],x,y,z);
  //fprintf(fp,"%f,%f,%f\n",x,y,z);
  return 0;


}
