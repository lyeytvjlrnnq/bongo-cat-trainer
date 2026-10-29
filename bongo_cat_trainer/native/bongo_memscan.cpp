// bongo_memscan — native helper for Bongo Cat Trainer pattern scans.
#include <windows.h>
#include <vector>
#include <string>
#include <cstring>

struct ScanResult { uintptr_t address; int matches; };

static std::vector<uint8_t> read_region(HANDLE proc, uintptr_t addr, size_t size) {
    std::vector<uint8_t> buf(size);
    SIZE_T read = 0;
    ReadProcessMemory(proc, (LPCVOID)addr, buf.data(), size, &read);
    buf.resize(read);
    return buf;
}

extern "C" __declspec(dllexport)
int scan_pattern(DWORD pid, const char* pattern, size_t pattern_len, uintptr_t* out, int out_max) {
    HANDLE proc = OpenProcess(PROCESS_VM_READ | PROCESS_QUERY_INFORMATION, FALSE, pid);
    if (!proc) return -1;
    int found = 0;
    MEMORY_BASIC_INFORMATION mbi{};
    uintptr_t addr = 0x10000;
    while (VirtualQueryEx(proc, (LPCVOID)addr, &mbi, sizeof(mbi))) {
        if (mbi.State == MEM_COMMIT && (mbi.Protect & (PAGE_READWRITE | PAGE_READONLY))) {
            auto data = read_region(proc, (uintptr_t)mbi.BaseAddress, mbi.RegionSize);
            for (size_t i = 0; i + pattern_len <= data.size(); ++i) {
                if (std::memcmp(data.data() + i, pattern, pattern_len) == 0) {
                    if (found < out_max) out[found++] = (uintptr_t)mbi.BaseAddress + i;
                }
            }
        }
        addr = (uintptr_t)mbi.BaseAddress + mbi.RegionSize;
    }
    CloseHandle(proc);
    return found;
}