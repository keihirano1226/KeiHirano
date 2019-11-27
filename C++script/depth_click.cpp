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

int main(int argc, const char *argv[])
{
    char filepath[256];
    string expath = argv[1];
    int i = atoi(argv[2]);
    ostringstream oss;
    oss << setfill( '0' ) << setw( 10 ) << i;
    cout << oss.str() << endl;
    mouseParam mouseEvent;
    FILE *fp;
    sprintf(filepath, "%s/depth_2d_points.csv", expath.c_str());
    fp=fopen( filepath, "w");
    //入力画像
    cv::Mat inputimg;
    inputimg = cv::imread( expath + "/depth/" + oss.str() + ".png",1);
    cv::Mat referenceimg;
    referenceimg = cv::imread(expath + "click.jpg",1);
    //表示するウィンドウ名
    cv::String showing_name1 = "input";
    cv::String showing_name2 = "reference";
    cv::namedWindow(showing_name1, cv::WINDOW_NORMAL);
    cv::imshow("input", inputimg);
    cv::namedWindow(showing_name2, cv::WINDOW_NORMAL);
    cv::imshow("reference", referenceimg);
    //コールバックの設定
    cv::setMouseCallback(showing_name1, CallBackFunc, &mouseEvent);
    int beforeX = 0;
    int beforeY = 0;
    while (1) {
        cv::waitKey(5);
        //左クリックがあったら表示
        if (mouseEvent.event == cv::EVENT_LBUTTONDOWN) {
            //クリック後のマウスの座標を出力
            std::cout << mouseEvent.x << " , " << mouseEvent.y << std::endl;
            if (beforeX != mouseEvent.x or beforeY != mouseEvent.y) {
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
