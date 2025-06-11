
// main.cpp

#include <fstream>
#include <iostream>
#include <sstream>
#include <windows.h>


void
SendSpecialKey(WORD vk)
{
    keybd_event(vk, 0, 0, 0);               // 按下键
    keybd_event(vk, 0, KEYEVENTF_KEYUP, 0); // 释放键
}

void
SendUnicodeChar(wchar_t ch)
{
    INPUT input      = { 0 };
    input.type       = INPUT_KEYBOARD;
    input.ki.wScan   = ch;
    input.ki.dwFlags = KEYEVENTF_UNICODE;
    SendInput(1, &input, sizeof(INPUT));

    // Key up
    input.ki.dwFlags = KEYEVENTF_UNICODE | KEYEVENTF_KEYUP;
    SendInput(1, &input, sizeof(INPUT));
}

// 监听键盘
bool
IsStop()
{
    // 检查是否按下 ESC 键
    return (GetAsyncKeyState(VK_ESCAPE) & 0x8000) != 0;
}

void
SendTextWithControl(const std::wstring& text, int delay = 0, int mode = 0)
{
    for(wchar_t ch : text)
    {
        if(IsStop())
        {
            std::cout << "检测到 ESC 键，停止发送文本。" << std::endl;
            return; // 如果按下 ESC 键，则停止发送
        }

        if(mode == 0)
        {
            switch(ch)
            {
            case L'\n':
                SendSpecialKey(VK_RETURN); // 模拟 Enter 键
                break;
            case L'\t':
                SendSpecialKey(VK_TAB); // 模拟 Tab 键
                break;
            default:
                SendUnicodeChar(ch); // 其他字符直接发 Unicode
            }
        }
        else if(mode == 1)
        {
            switch(ch)
            {
            case L'\n':
                SendSpecialKey(VK_SPACE);  // 模拟空格键
                SendSpecialKey(VK_DELETE); // 模拟删除键
                SendSpecialKey(VK_RETURN); // 模拟 Enter 键
                SendSpecialKey(VK_HOME);   // 然后模拟 home 键
                break;

            case L'\t':
                SendSpecialKey(VK_TAB); // 模拟 Tab 键
                break;

            case L'(':
            case L'[':
            case L'{':
                SendUnicodeChar(ch);       // 直接发送左括号
                SendSpecialKey(VK_DELETE); // 模拟删除键
                break;

            default:
                SendUnicodeChar(ch); // 其他字符直接发 Unicode
            }
        }
        Sleep(delay);
    }
}


std::wstring
ReadFile(const std::string& filePath)
{
    // 打开文件为文本输入流
    std::ifstream file(filePath, std::ios::in | std::ios::binary);
    if(!file)
    {
        throw std::runtime_error("无法打开文件: " + filePath);
    }

    // 读取整个文件内容到字符串
    std::ostringstream oss;
    oss << file.rdbuf();
    std::string utf8Str = oss.str();

    // 将 UTF-8 编码的 std::string 转换为 std::wstring（宽字符）
    int wideLen = MultiByteToWideChar(CP_UTF8, 0, utf8Str.c_str(), static_cast<int>(utf8Str.size()), nullptr, 0);
    if(wideLen == 0)
    {
        throw std::runtime_error("UTF-8 转换为宽字符失败");
    }
    std::wstring wideStr(wideLen, 0);
    MultiByteToWideChar(CP_UTF8, 0, utf8Str.c_str(), static_cast<int>(utf8Str.size()), &wideStr[0], wideLen);

    return wideStr;
}


void
print_help()
{
    printf("用法: copy_keyboard <文件路径> <模式> <延迟>\n");
}


int
main(int argc, char* argv[])
{
    int mode  = 0; // 默认模式
    int delay = 0; // 默认延迟

    if(argc < 4)
    {
        print_help();
        return 1;
    }

    try
    {
        mode  = std::stoi(argv[2]);
        delay = std::stoi(argv[3]);
    }
    catch(const std::exception& e)
    {
        printf("参数错误: %s\n", e.what());
        print_help();
        return 1;
    }

    std::string filePath = argv[1];

    std::wstring text = ReadFile(filePath);

    for(int i = 3; i > 0; --i)
    {
        printf("准备发送文本，%d 秒后开始...\r", i);
        Sleep(1000);
    }

    SendTextWithControl(text, delay, mode);

    printf("\n文本发送完成。\n");

    return 0;
}
