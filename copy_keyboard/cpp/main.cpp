#include <codecvt>
#include <fstream>
#include <iostream>
#include <locale>
#include <sstream>
#include <string>
#include <vector>
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

void
SendTextWithControl(const std::wstring& text, int delay = 0)
{
    for(wchar_t ch : text)
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
    std::wstring_convert<std::codecvt_utf8_utf16<wchar_t>> converter;

    std::wstring wideStr = converter.from_bytes(utf8Str);

    return wideStr;
}


int
main()
{
    printf("test\n");


    std::string  filePath = "../ignore/context.txt";
    std::wstring text     = ReadFile(filePath);
    if(text.empty())
    {
        std::wcerr << L"No text to send." << std::endl;
        return 1;
    }

    std::wcout << L"Text to send: " << text << std::endl;

    Sleep(1000); // Wait for a second before sending text

    SendTextWithControl(text);

    return 0;
}
