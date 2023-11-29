#pragma once

#include <cstdint>

namespace akida {
namespace soc {
namespace akd1500 {
// NSoC top level address
constexpr uint32_t kTopLevelRegBase = 0xFCC00000;
// registers region size
constexpr uint32_t kRegistersRegionSize = 1 * 1024 * 1024;

// Main memory offset in AKD1500
constexpr uint32_t kPcieDmaDescritorsSize = 256;
constexpr uint32_t kMainMemoryBase = 0x20000000 + kPcieDmaDescritorsSize;
// Main memory size is 1MB
constexpr uint32_t kMainMemorySize = 1 * 1024 * 1024 - kPcieDmaDescritorsSize;

}  // namespace akd1500

}  // namespace soc

}  // namespace akida
