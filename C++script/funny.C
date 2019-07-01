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

int main()
{

  while(true){
    static int i = 1;
    std::ostringstream oss;
    oss << std::setfill( '0' ) << std::setw( 10 ) << i++;
    //画像フォルダがあるパスを指定する部分
    cv::Mat image = cv::imread( "/home/kei/document/experiments/2019.01.15/jpg2/" + oss.str() + ".jpg" );
    cv::Mat depth = cv::imread( "/home/kei/document/experiments/2019.01.15/depth/" + oss.str() + ".tiff" );
    //画像が無くなったらループを抜ける
    if( image.empty()){
      break;
    }
    cv::imshow( "depth", depth );
    cv::imshow( "image", image );
        if( cv::waitKey( 30 ) >= 0 ){
            break;
        }
  }

  cv::destroyAllWindows();
  return 0;
}
