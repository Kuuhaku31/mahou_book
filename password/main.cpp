
// amin.cpp

#include <chrono>
#include <cstdlib>
#include <string>


char 输出目录[] = "output_directory";

// 调用 7-Zip 测试密码是否正确
inline bool
test_password(const char* 文件地址, int 解压密码)
{
    static char command[256];
    // 构造命令：7z t ./def.rar -p"密码"
    sprintf(command, "7z t \"%s\" -p%d >nul 2>nul", 文件地址, 解压密码);
    return std::system(command); // 返回值为 0 表示密码正确
}

// 调用 7-Zip 解压文件
inline void
extract_rar_with_7zip(const char* 文件地址, int 解压密码)
{
    static char command[256];
    // 构造命令：7z x ./def.rar -p"密码" -o"output_directory" -y
    sprintf(command, "7z x \"%s\" -p%d -o\"%s\" -y >nul 2>nul", 文件地址, 解压密码, 输出目录);
    std::system(command);
}


int
main()
{
    char 文件地址[] = "./def.rar";

    // 记录开始时间
    int  循环次数   = 0;
    auto start_time = std::chrono::high_resolution_clock::now();
    while(test_password(文件地址, 循环次数)) 循环次数++;
    auto end_time = std::chrono::high_resolution_clock::now();
    // 5.2秒

    std::chrono::duration<double> elapsed = end_time - start_time;
    printf("密码为：%d，耗时: %.2f 秒\n", 循环次数, elapsed.count());

    // 解压文件
    extract_rar_with_7zip(文件地址, 循环次数);

    return 0;
}