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
//椅子の座標変換用に点群を取得する場合，
//座面を囲うことが出来る2点
//背もたれを囲うための点を2点
//椅子，もしくはベッドの際を表す三次元点を6点
//クリックして取得する
//マウス入力用のパラメータ
using namespace std;
struct mouseParam {
    int x;
    int y;
    int event;
    int flags;
};

//コールバック関数
void CallBackFunc(int eventType, int x, int y, int flags, void* userdata)
{
    mouseParam *ptr = static_cast<mouseParam*> (userdata);

    ptr->x = x;
    ptr->y = y;
    ptr->event = eventType;
    ptr->flags = flags;
}

int main(void)
{
    char filepath[256];
    // const char expath[] = "/home/kei/document/experiments/Hamano/test/";
    const char expath[] = "/home/shoda/Documents/mitsu/";

    mouseParam mouseEvent;
    FILE *fp;
    sprintf(filepath, "%s/2DGround.csv", expath);
    fp=fopen( filepath, "w");
    //入力画像
    cv::Mat inputimg;
    inputimg = cv::imread( string(expath) + "/regi_mirror/0000000000.jpg",1);
    //表示するウィンドウ名
    cv::String showing_name = "input";
    
    cv::namedWindow(showing_name, cv::WINDOW_NORMAL);
    //画像の表示
    cv::imshow("input", inputimg);
    //コールバックの設定
    cv::setMouseCallback(showing_name, CallBackFunc, &mouseEvent);
    int beforeX = 0;
    int beforeY = 0;
    while (1) {
        cv::waitKey(5);
        //左クリックがあったら表示
        if (mouseEvent.event == cv::EVENT_LBUTTONDOWN) {
            //クリック後のマウスの座標を出力
            std::cout << mouseEvent.x << " , " << mouseEvent.y << std::endl;
            if (beforeX != mouseEvent.x and beforeY != mouseEvent.y) {
              fprintf(fp,"%d,%d\n",mouseEvent.x,mouseEvent.y);
              beforeX = mouseEvent.x;
              beforeY = mouseEvent.y;
            }


        }
        //右クリックがあったら終了
        else if (mouseEvent.event == cv::EVENT_RBUTTONDOWN) {
            break;
        }
    }
    return 0;
}
