
// cube.cpp

// 实现一个简单的立方体旋转效果
// 通过终端打印实现3D立方体的旋转
// 使用ASCII字符来表示立方体

#include <ctime> // For clock()
#include <math.h>
#include <stdio.h>
#include <unistd.h>


// 延迟
const unsigned int delay_time = 50; // 延迟时间

const int screen_width  = 80; // 屏幕宽度
const int screen_height = 45; // 屏幕高度

const float sample_density = 0.15; // 采样密度

const float camera_distance_from_center = 100; // 相机距离旋转中心的距离
const float camera_distance_from_screen = 40;  // 相机距离屏幕的距离

float deep_buffer[screen_height][screen_width];   // 深度缓冲区
char  screen_buffer[screen_height][screen_width]; // 屏幕缓冲区

char background_ASCIICode = ' '; // 背景字符


struct Point3D
{
    float x, y, z = 0.0; // 3D坐标
};

class Rotation
{
    float A, B, C;    // 旋转角度
    float sinA, cosA; // 旋转角度的正弦和余弦值
    float sinB, cosB; // 旋转角度的正弦和余弦值
    float sinC, cosC; // 旋转角度的正弦和余弦值
public:
    Rotation(float a, float b, float c)
        : A(a)
        , B(b)
        , C(c)
    {
        sinA = sin(A), cosA = cos(A); // 计算正弦和余弦值
        sinB = sin(B), cosB = cos(B); // 计算正弦和余弦值
        sinC = sin(C), cosC = cos(C); // 计算正弦和余弦值
    }

    void
    Update(float a, float b, float c)
    {
        A = a, B = b, C = c; // 更新旋转角度
        // 计算正弦和余弦值
        sinA = sin(A), cosA = cos(A); // 计算正弦和余弦值
        sinB = sin(B), cosB = cos(B); // 计算正弦和余弦值
        sinC = sin(C), cosC = cos(C); // 计算正弦和余弦值
    }

    void
    UpdateDelta(float delta_a, float delta_b, float delta_c)
    {
        A += delta_a, B += delta_b, C += delta_c; // 更新旋转角度
        // 计算正弦和余弦值
        sinA = sin(A), cosA = cos(A); // 计算正弦和余弦值
        sinB = sin(B), cosB = cos(B); // 计算正弦和余弦值
        sinC = sin(C), cosC = cos(C); // 计算正弦和余弦值
    }

    // 线性变换
    Point3D
    Transform(const Point3D& p) const
    {
        return {
            p.y * sinA * sinB * cosC - p.z * cosA * sinB * cosC + p.y * cosA * sinC + p.z * sinA * sinC + p.x * cosB * cosC,
            p.y * cosA * cosC + p.z * sinA * cosC - p.y * sinA * sinB * sinC + p.z * cosA * sinB * sinC - p.x * cosB * sinC,
            p.z * cosA * cosB - p.y * sinA * cosB + p.x * sinB + camera_distance_from_center
        };
    }
};


/// 渲染点
void
Renderer(const Point3D& p, char ch)
{
    float ooz = 1 / p.z;                                                               // 1/z
    int   xp  = (int)(screen_width / 2 + camera_distance_from_screen * ooz * p.x * 2); // x坐标
    int   yp  = (int)(screen_height / 2 + camera_distance_from_screen * ooz * p.y);    // y坐标

    // 判断是否在屏幕范围内
    if(xp >= 0 && xp < screen_width && yp >= 0 && yp < screen_height)
    {
        // 判断深度缓冲区
        if(ooz > deep_buffer[yp][xp])
        {
            deep_buffer[yp][xp]   = ooz; // 更新深度缓冲区
            screen_buffer[yp][xp] = ch;  // 更新屏幕缓冲区
        }
    }
}


// 计算立方体的点，并更新缓冲区
void
CalculateCubePoint(const Rotation& r, float i, float j, float k, char ch)
{
    // 渲染点
    Renderer(r.Transform({ i, j, k }), ch); // 渲染点
}


// 模拟立方体的旋转
void
Cube(const Rotation& r)
{
    const float cube_width = 40; // 立方体的宽度

    // 遍历立方体表面的每个点
    for(float i = -cube_width / 2; i < cube_width / 2; i += sample_density)
    {
        for(float j = -cube_width / 2; j < cube_width / 2; j += sample_density)
        {
            CalculateCubePoint(r, i, j, -cube_width / 2, '@'); // 前面
            CalculateCubePoint(r, i, j, cube_width / 2, '#');  // 后面
            CalculateCubePoint(r, -cube_width / 2, i, j, '$'); // 左面
            CalculateCubePoint(r, cube_width / 2, i, j, '%');  // 右面
            CalculateCubePoint(r, i, -cube_width / 2, j, '&'); // 上面
            CalculateCubePoint(r, i, cube_width / 2, j, '*');  // 下面
        }
    }
}

// 模拟锥体的旋转
void
Cone(const Rotation& r)
{
    // 棱长
    const float cone_width = 40;

    const float square3 = sqrt(3); // 平方根3

    // 遍历锥体表面的每个点

    // 一个面
    for(float i = 0.0; i < cone_width; i += sample_density)
    {
        float j_max = -i + cone_width;
        for(float j = 0.0; j < j_max; j += sample_density)
        {
            float x = i;
            float y = j;
            float z = cone_width - i - j;

            // 第一象限
            CalculateCubePoint(r, x, y, z, '@');  // 高处的点
            CalculateCubePoint(r, x, y, -z, '#'); // 底部的点

            // 第二象限
            CalculateCubePoint(r, -x, y, z, '$');  // 高处的点
            CalculateCubePoint(r, -x, y, -z, '%'); // 底部的点

            // 第三象限
            CalculateCubePoint(r, -x, -y, z, '&');  // 高处的点
            CalculateCubePoint(r, -x, -y, -z, '*'); // 底部的点

            // 第四象限
            CalculateCubePoint(r, x, -y, z, '!');  // 高处的点
            CalculateCubePoint(r, x, -y, -z, '^'); // 底部的点
        }
    }
}

void
Line(const Rotation& r)
{
    // 计算线段的点，并更新缓冲区
    for(float i = 0.0; i < 100; i += sample_density)
    {
        CalculateCubePoint(r, i, 0, 0, '|');
        CalculateCubePoint(r, -i, 0, 0, '|');

        CalculateCubePoint(r, 0, i, 0, '-');
        CalculateCubePoint(r, 0, -i, 0, '-');
    }
}


int
main()
{
    Rotation rot_cube(0, 0, 0); // 旋转对象
    Rotation rot_cone(0, 0, 0); // 旋转对象

    unsigned int delta_time = 0; // 时间差

    // 清除屏幕
    printf("\x1b[2J");
    // 设置光标不可见
    printf("\x1b[?25l");

    // 主循环
    while(true)
    {
        // 计算时间差
        delta_time = clock(); // 开始时间

        // 清除深度缓冲区和屏幕缓冲区
        memset(deep_buffer, 0, sizeof(deep_buffer)); // 0表示距离无限远
        memset(screen_buffer, background_ASCIICode, sizeof(screen_buffer));

        // 计算模拟
        Cone(rot_cone);
        Cube(rot_cube); // 计算立方体的点
        Line(rot_cone); // 计算线段的点

        // 打印输出缓冲区
        // 光标移动到home位置，并打印屏幕缓冲区
        printf("\x1b[H"); // 将光标移动到左上角
        for(int i = 0; i < screen_height; i++)
        {
            fwrite(screen_buffer[i], sizeof(char), screen_width, stdout); // 一次性输出一行
            putchar('\n');                                                // 换行
        }

        // 刷新角度
        rot_cube.UpdateDelta(0.05, 0.05, 0.001);
        rot_cone.UpdateDelta(0.03, 0.01, 0.002);

        delta_time = clock() - delta_time; // 计算时间差

        if(delta_time < delay_time) usleep((delay_time - delta_time) * 1000); // 延迟
    }

    return 0;
}
