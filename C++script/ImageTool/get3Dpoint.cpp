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

using namespace std;

int stoi(string str){
  int ret;
  stringstream ss;
  ss << str;
  ss >> ret;
  return ret;
}

int main(int argc, const char *argv[])
{
  char filepath[256];
  string expath = argv[1];
//   int length =  atoi(argv[2]);
  bool enable_rgb = false;
  bool enable_depth =false;
  //libfreenect2::setGlobalLogger(libfreenect2::createConsoleLogger(libfreenect2::Logger::Debug));

  //デバイス初期化
  libfreenect2::Freenect2 freenect2;
  libfreenect2::Freenect2Device *dev = 0;
  libfreenect2::PacketPipeline *pipeline = 0;
  libfreenect2::Freenect2Device::Config config;
  config.MinDepth = 0.5f;
  config.MaxDepth = 8.0f;
  float x,y,z;
  string serial = freenect2.getDefaultDeviceSerialNumber();

  //デバイス検出
  if(freenect2.enumerateDevices() == 0)
  {
    cout << "no device connected!" << endl;
    return -1;
  }
  if (serial == "")
  {
    serial = freenect2.getDefaultDeviceSerialNumber();
  }
  printf("%s\n",serial.c_str());

  //デバイスを開いて構成する
  dev = freenect2.openDevice(serial);
  int types = 0;
  puts("Device 構成中");
  if (enable_rgb)
    types |= libfreenect2::Frame::Color;
  if (enable_depth)
    types |= libfreenect2::Frame::Ir | libfreenect2::Frame::Depth;
  libfreenect2::SyncMultiFrameListener listener(types);
  libfreenect2::FrameMap frames;
  dev->setConfiguration(config);
  dev->setColorFrameListener(&listener);
  dev->setIrAndDepthFrameListener(&listener);

  //デバイスを起動する
  puts("Device 起動中");
  if (enable_rgb && enable_depth)
  {
    if (!dev->start()){
      return -1;
    }
  }
  else
  {
    if (!dev->startStreams(enable_rgb, enable_depth))
      return -1;
  }
  cout << "device serial: " << dev->getSerialNumber() << endl;
  cout << "device firmware: " << dev->getFirmwareVersion() << endl;

  //カメラパラメータ割り当て
  libfreenect2::Registration* registration = new libfreenect2::Registration(dev->getIrCameraParams(), dev->getColorCameraParams());
  libfreenect2::Frame undistorted(512, 424, 4), registered(512, 424, 4), depth2rgb(1920, 1080 + 2, 4);;
  cv::Mat depthmatUndistorted, rgbd, rgbd2;

  cv::Mat depthtest;
  cv::Mat depthMat;
  //depth画像を読み込む
  // depthtest =  cv::imread( string(expath) + "/depth_mirror/0000000160.png",2);
//   /home/shoda/Documents/Image_processing/semaseg
  depthtest =  cv::imread( expath + "/depth/0000000000.tiff",2);
  depthtest.convertTo(depthMat, CV_32FC1);

  // 最終的な出力ファイル
  FILE *fp;
  sprintf(filepath, "%s/product_xyz.csv", expath.c_str());
  fp=fopen( filepath, "w");

  sprintf(filepath, "%s/product3Dpoints.csv", expath.c_str());
  ifstream stream(filepath);
  std::string line;
  int row = 0;
  int col = 0;
  int num = 5048;
  int data[num][3];
  while(getline(stream, line))
  {
      string tmp = "";
      istringstream stream(line);

      // 区切り文字がなくなるまで文字を区切っていく
      while (getline(stream, tmp, ','))
      {
          // 区切られた文字がtmpに入る
          data[row][col] = stoi(tmp);
          col++;
      }

      col = 0;
      row++;  // 次の人の配列に移る
  }

  int i = 0;
  for (i = 0; i < num ; ++i ){
      libfreenect2::Frame depth(512, 424, 4, depthMat.data);
      registration->undistortDepth(&depth, &undistorted);
      registration->getPointXYZ(&undistorted, data[i][0], data[i][1],x,y,z);
      if (isnan(x) != true){
          fprintf(fp,"%f,%f,%f\n",x,y,z);
      }
  }

  return 0;
}
