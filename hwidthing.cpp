#include <iostream>
#include <map>
#include <string>
#include <windows.h>
#include <stdio.h>
#include <string.h>

using namespace std;

LRESULT CALLBACK WndProc(HWND hwnd, UINT msg, WPARAM wParam, LPARAM lParam) {
    static HWND hwndTextBox, hwndButton;
    static char hwidBuffer[256];

    switch (msg) {
        case WM_CREATE:
            hwndTextBox = CreateWindowExW(
                0, L"EDIT", L"", 
                WS_CHILD | WS_VISIBLE | WS_BORDER | ES_READONLY, 
                20, 20, 400, 25, hwnd, NULL, NULL, NULL
            );

            hwndButton = CreateWindowExW(
                0, L"BUTTON", L"Get HWID", 
                WS_CHILD | WS_VISIBLE | BS_PUSHBUTTON, 
                20, 60, 100, 30, hwnd, (HMENU)1, NULL, NULL
            );
            break;

        case WM_COMMAND:
            if (LOWORD(wParam) == 1) {
                HW_PROFILE_INFO hwProfileInfo;
                if (GetCurrentHwProfile(&hwProfileInfo)) {
                    char* hwid = hwProfileInfo.szHwProfileGuid;

                    if (hwid[0] == '{') {
                        hwid++; 
                    }
                    size_t len = strlen(hwid);
                    if (hwid[len - 1] == '}') {
                        hwid[len - 1] = '\0'; 
                    }

                    snprintf(hwidBuffer, sizeof(hwidBuffer), "%s", hwid);

                    SetWindowTextA(hwndTextBox, hwidBuffer);
                }
            }
            break;

        case WM_CLOSE:
            DestroyWindow(hwnd);
            break;

        case WM_DESTROY:
            PostQuitMessage(0);
            break;

        default:
            return DefWindowProcW(hwnd, msg, wParam, lParam);
    }
    return 0;
}

int main() {
    map<string, string> dict = { {"swig", "swig123"} };
    string username, password;
    cout << "Enter username: " << endl;
    cin >> username;
    cout << "Enter password: " << endl;
    cin >> password;
    if (dict.find(username) != dict.end() && dict[username] == password) {
        cout << "Login Successfully!" << endl;
        HINSTANCE hInstance = GetModuleHandle(NULL);

        WNDCLASSW wc = { };
        wc.lpfnWndProc = WndProc;
        wc.hInstance = hInstance;
        wc.lpszClassName = L"HWIDClient";

        RegisterClassW(&wc);

        wstring wUsername(username.begin(), username.end());
        wstring title = L"Goober Client V1.0 | " + wUsername;
        
        HWND hwnd = CreateWindowExW(
            0, L"HWIDClient", title.c_str(),
            WS_OVERLAPPEDWINDOW, CW_USEDEFAULT, CW_USEDEFAULT,
            500, 200, NULL, NULL, hInstance, NULL
        );

        if (!hwnd) return 0;

        ShowWindow(hwnd, SW_SHOWNORMAL);
        UpdateWindow(hwnd);

        MSG msg = { };
        while (GetMessageW(&msg, NULL, 0, 0) > 0) {
            TranslateMessage(&msg);
            DispatchMessageW(&msg);
        }
    } else {
        cout << "Invalid Credentials" << endl;
    }

    return 0;
}
