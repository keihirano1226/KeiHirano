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

int main()
{
  char filepath[256];
  const char expath[] = "/home/shoda/Documents/mitsu";
  bool isFixed = true; //アフィン変換されているか否か
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

  if (isFixed) sprintf(filepath, "%s/test_fixed.csv", expath);
  else sprintf(filepath, "%s/test.csv", expath);

  ifstream stream(filepath);
  string line;
  //2dのOpenPoseでディテクトされた情報を格納するための配列
  //int data[460][50];
  //3dの推定した三次元座標を格納するための配列
  //float posedata[460][75];
  const string delim = ",";

  int row = 0;
  int col = 0;
  puts("hello");

  //2dのOpenPoseでディテクトされた情報を格納するための配列
  int data[200][50];
  //3dの推定した三次元座標を格納するための配列
  float posedata[200][75];

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
  puts("hello");
  printf("%d\n",data[0][1]);
  FILE *fp;
  
  if (isFixed) sprintf(filepath, "%s/save_fixed.csv", expath);
  else sprintf(filepath, "%s/save.csv", expath);

  fp=fopen( filepath, "w");
  for ( int row1 = 0; row1 < row ; ++row1  ) {
    static int i = 1;//抽出を始める画像の番号
    ostringstream oss;
    oss << setfill( '0' ) << setw( 10 ) << i++;
    for ( col = 0; col < 50; col = col + 2 ) {
      cv::Mat depthtest ;
      cv::Mat depthMat ;
      depthtest =  cv::imread( string(expath) + "/depth_mirror/" + oss.str() + ".tiff",2);
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

      //cout << data[row][col] << " ";
    }printf("%d's Frame\n", row1);
    fprintf(fp,"\n");

  }

  return 0;
}
