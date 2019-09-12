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

  std::ifstream stream("/home/kei/document/experiments/BioEngen/PI09_1/test.csv");
  std::string line;
  //2dのOpenPoseでディテクトされた情報を格納するための配列
  //int data[460][50];
  //3dの推定した三次元座標を格納するための配列
  //float posedata[460][75];
  const std::string delim = ",";

  int row = 0;
  int row1 = 0;
  int col;
  puts("hello");

  //2dのOpenPoseでディテクトされた情報を格納するための配列
  int data[72][50];
  //3dの推定した三次元座標を格納するための配列
  float posedata[72][75];

  while ( getline(stream, line) ) {
    col = 0;
    // delimを区切り文字として切り分け、intに変換してdata[][]に格納する
    for ( std::string::size_type spos, epos = 0;
        (spos = line.find_first_not_of(delim, epos)) != std::string::npos;) {
      std::string token = line.substr(spos,(epos = line.find_first_of(delim, spos))-spos);
      data[row][col++] = stoi(token);
    }
    ++row;
  }

  // よめたかな?
  int j = 0;
  FILE *fp;
  fp=fopen("/home/kei/document/experiments/BioEngen/PI09_1/save.csv","w");
  for ( row1 = 0; row1 < row ; ++row1  ) {
    static int i = 2302;//抽出を始める画像の番号

    std::ostringstream oss;
    oss << std::setfill( '0' ) << std::setw( 10 ) << i++;
    for ( col = 0; col < 50; col = col + 2 ) {
      cv::Mat depthtest ;
      cv::Mat depthMat ;
      depthtest =  cv::imread( "/home/kei/document/experiments/BioEngen/PI09_1/depth_mirror/" + oss.str() + ".png",2);
      depthtest.convertTo(depthMat, CV_32FC1);
      //depthMat = depthMat * 255.0f;
      libfreenect2::Frame depth(512, 424, 4, depthMat.data);
      registration->undistortDepth(&depth, &undistorted);
      int c = data[row1][col];
      int r = data[row1][col + 1];
      //２次元座標が負の値だった場合は、x,y,zにそれぞれ0を代入する
      if ( r > 0 or c > 0 ){
        registration->getPointXYZ(&undistorted,r,c,x,y,z);
        posedata[row1][col] = x;
        posedata[row1][col + 1] = y;
        posedata[row1][col + 2] = z;
        fprintf(fp,"%f,%f,%f,",x,y,z);
        //printf("r = %d, c = %d\n",r,c);
        //printf("x = %f,y = %f,z = %f\n",x,y,z);
      }else{
        puts("x = 0,y = 0,z = 0\n");
        posedata[row1][col] = 0.0f;
        posedata[row1][col + 1] = 0.0f;
        posedata[row1][col + 2] = 0.0f;
        x = 0.0f;
        y = 0.0f;
        z = 0.0f;
        fprintf(fp,"%f,%f,%f,",x,y,z);
      }

      //std::cout << data[row][col] << " ";
    }printf("%d's Frame\n", j);
    j = j + 1;
    fprintf(fp,"\n");;

    std::cout << std::endl;
  }



  return 0;
}
