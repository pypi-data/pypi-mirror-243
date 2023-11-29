#pragma once

#include <cstdint>
#include "infra/hardware_driver.h"
#include "infra/registers_common.h"

namespace akida {
namespace akd1500 {

static constexpr uint32_t SYS_CONFIG_CONTROL_SIGNALS_REG = 0xfce00018;
static constexpr RegDetail SYS_CONFIG_CONTROL_SIGNALS_EN_SPI_S2M(16);
static constexpr RegDetail SYS_CONFIG_CONTROL_SIGNALS_SPIM_DI_SWAP(21);

// Spi master controller registers
static constexpr uint32_t SPI_MASTER_CFG_BASE = 0xfcf20000;
static constexpr uint32_t SPI_MASTER_CFG_CTRLR0 = SPI_MASTER_CFG_BASE + 0x0;
static constexpr RegDetail SPI_MASTER_CFG_CTRLR0_DFS(0, 4);
static constexpr RegDetail SPI_MASTER_CFG_CTRLR0_SPI_FRF(22, 23);
static constexpr RegDetail SPI_MASTER_CFG_CTRLR0_SPI_HYPERBUS_EN(24);
static constexpr RegDetail SPI_MASTER_CFG_CTRLR0_SSI_IS_MST(31);

static constexpr uint32_t SPI_MASTER_CFG_SSIENR = SPI_MASTER_CFG_BASE + 0x8;
static constexpr RegDetail SPI_MASTER_CFG_SSIENR_SSIC_EN(0);

static constexpr uint32_t SPI_MASTER_CFG_SER = SPI_MASTER_CFG_BASE + 0x10;

static constexpr uint32_t SPI_MASTER_CFG_BAUDR = SPI_MASTER_CFG_BASE + 0x14;
static constexpr RegDetail SPI_MASTER_CFG_BAUDR_SCKDV(1, 15);

static constexpr uint32_t SPI_MASTER_CFG_SPI_CTRLR0 =
    SPI_MASTER_CFG_BASE + 0xf4;
static constexpr RegDetail SPI_MASTER_CFG_SPI_CTRLR0_TRANS_TYPE(0, 1);
static constexpr RegDetail SPI_MASTER_CFG_SPI_CTRLR0_ADDR_L(2, 5);
static constexpr RegDetail SPI_MASTER_CFG_SPI_CTRLR0_XIP_MD_BIT_EN(7);
static constexpr RegDetail SPI_MASTER_CFG_SPI_CTRLR0_INST_L(8, 9);
static constexpr RegDetail SPI_MASTER_CFG_SPI_CTRLR0_WAIT_CYCLES(11, 15);
static constexpr RegDetail SPI_MASTER_CFG_SPI_CTRLR0_SPI_DDR_EN(16);
static constexpr RegDetail SPI_MASTER_CFG_SPI_CTRLR0_INST_DDR_EN(17);
static constexpr RegDetail SPI_MASTER_CFG_SPI_CTRLR0_SPI_RXDS_EN(18);
static constexpr RegDetail SPI_MASTER_CFG_SPI_CTRLR0_XIP_INST_EN(20);
static constexpr RegDetail SPI_MASTER_CFG_SPI_CTRLR0_SPI_RXDS_SIG_EN(25);
static constexpr RegDetail SPI_MASTER_CFG_SPI_CTRLR0_XIP_MBL(26, 27);

static constexpr uint32_t SPI_MASTER_CFG_DDR_DRIVE_EDGE =
    SPI_MASTER_CFG_BASE + 0xf8;
static constexpr RegDetail SPI_MASTER_CFG_DDR_DRIVE_EDGE_TDE(0, 7);

static constexpr uint32_t SPI_MASTER_CFG_XIP_MODE_BITS =
    SPI_MASTER_CFG_BASE + 0xfc;
static constexpr RegDetail SPI_MASTER_CFG_XIP_MODE_BITS_XIP_MD_BITS(0, 15);

static constexpr uint32_t SPI_MASTER_CFG_XIP_INCR_INST =
    SPI_MASTER_CFG_BASE + 0x100;
static constexpr RegDetail SPI_MASTER_CFG_XIP_INCR_INST_INCR_INST(0, 15);

void init_spi_flash(HardwareDriver* driver);

}  // namespace akd1500
}  // namespace akida
