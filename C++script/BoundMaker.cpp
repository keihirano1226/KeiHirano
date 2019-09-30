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

//マウス入力用のパラメータ
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
    mouseParam mouseEvent;
    FILE *fp;
    fp=fopen("/home/kei/document/experiments/BioEngen/MA330_11/product/2DGround.csv","w");
    //入力画像
    cv::Mat inputimg;
    inputimg = cv::imread("/home/kei/document/experiments/BioEngen/MA330_11/regi_test/regi_test_flip.jpg",1);

    //表示するウィンドウ名
    cv::String showing_name = "input";

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
