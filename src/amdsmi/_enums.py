# Auto-extracted enum definitions from ROCm/amdsmi (verbatim values).
from enum import IntEnum, Enum
from . import _constants as amdsmi_wrapper


class AmdSmiStatus(IntEnum):
    SUCCESS             = amdsmi_wrapper.AMDSMI_STATUS_SUCCESS
    INVAL               = amdsmi_wrapper.AMDSMI_STATUS_INVAL
    NOT_SUPPORTED       = amdsmi_wrapper.AMDSMI_STATUS_NOT_SUPPORTED
    NOT_YET_IMPLEMENTED = amdsmi_wrapper.AMDSMI_STATUS_NOT_YET_IMPLEMENTED
    FAIL_LOAD_MODULE    = amdsmi_wrapper.AMDSMI_STATUS_FAIL_LOAD_MODULE
    FAIL_LOAD_SYMBOL    = amdsmi_wrapper.AMDSMI_STATUS_FAIL_LOAD_SYMBOL
    DRM_ERROR           = amdsmi_wrapper.AMDSMI_STATUS_DRM_ERROR
    API_FAILED          = amdsmi_wrapper.AMDSMI_STATUS_API_FAILED
    TIMEOUT             = amdsmi_wrapper.AMDSMI_STATUS_TIMEOUT
    RETRY               = amdsmi_wrapper.AMDSMI_STATUS_RETRY
    NO_PERM             = amdsmi_wrapper.AMDSMI_STATUS_NO_PERM
    INTERRUPT           = amdsmi_wrapper.AMDSMI_STATUS_INTERRUPT
    IO                  = amdsmi_wrapper.AMDSMI_STATUS_IO
    ADDRESS_FAULT       = amdsmi_wrapper.AMDSMI_STATUS_ADDRESS_FAULT
    FILE_ERROR          = amdsmi_wrapper.AMDSMI_STATUS_FILE_ERROR
    OUT_OF_RESOURCES    = amdsmi_wrapper.AMDSMI_STATUS_OUT_OF_RESOURCES
    INTERNAL_EXCEPTION  = amdsmi_wrapper.AMDSMI_STATUS_INTERNAL_EXCEPTION
    INPUT_OUT_OF_BOUNDS = amdsmi_wrapper.AMDSMI_STATUS_INPUT_OUT_OF_BOUNDS
    INIT_ERROR          = amdsmi_wrapper.AMDSMI_STATUS_INIT_ERROR
    REFCOUNT_OVERFLOW   = amdsmi_wrapper.AMDSMI_STATUS_REFCOUNT_OVERFLOW
    DIRECTORY_NOT_FOUND = amdsmi_wrapper.AMDSMI_STATUS_DIRECTORY_NOT_FOUND
    BUSY                = amdsmi_wrapper.AMDSMI_STATUS_BUSY
    NOT_FOUND           = amdsmi_wrapper.AMDSMI_STATUS_NOT_FOUND
    NOT_INIT            = amdsmi_wrapper.AMDSMI_STATUS_NOT_INIT
    NO_SLOT             = amdsmi_wrapper.AMDSMI_STATUS_NO_SLOT
    DRIVER_NOT_LOADED   = amdsmi_wrapper.AMDSMI_STATUS_DRIVER_NOT_LOADED
    MORE_DATA           = amdsmi_wrapper.AMDSMI_STATUS_MORE_DATA
    NO_DATA             = amdsmi_wrapper.AMDSMI_STATUS_NO_DATA
    INSUFFICIENT_SIZE   = amdsmi_wrapper.AMDSMI_STATUS_INSUFFICIENT_SIZE
    UNEXPECTED_SIZE     = amdsmi_wrapper.AMDSMI_STATUS_UNEXPECTED_SIZE
    UNEXPECTED_DATA     = amdsmi_wrapper.AMDSMI_STATUS_UNEXPECTED_DATA
    NON_AMD_CPU         = amdsmi_wrapper.AMDSMI_STATUS_NON_AMD_CPU
    NO_ENERGY_DRV       = amdsmi_wrapper.AMDSMI_STATUS_NO_ENERGY_DRV
    NO_MSR_DRV          = amdsmi_wrapper.AMDSMI_STATUS_NO_MSR_DRV
    NO_HSMP_DRV         = amdsmi_wrapper.AMDSMI_STATUS_NO_HSMP_DRV
    NO_HSMP_SUP         = amdsmi_wrapper.AMDSMI_STATUS_NO_HSMP_SUP
    NO_HSMP_MSG_SUP     = amdsmi_wrapper.AMDSMI_STATUS_NO_HSMP_MSG_SUP
    HSMP_TIMEOUT        = amdsmi_wrapper.AMDSMI_STATUS_HSMP_TIMEOUT
    NO_DRV              = amdsmi_wrapper.AMDSMI_STATUS_NO_DRV
    FILE_NOT_FOUND      = amdsmi_wrapper.AMDSMI_STATUS_FILE_NOT_FOUND
    ARG_PTR_NULL        = amdsmi_wrapper.AMDSMI_STATUS_ARG_PTR_NULL
    AMDGPU_RESTART_ERR  = amdsmi_wrapper.AMDSMI_STATUS_AMDGPU_RESTART_ERR
    SETTING_UNAVAILABLE = amdsmi_wrapper.AMDSMI_STATUS_SETTING_UNAVAILABLE
    CORRUPTED_EEPROM    = amdsmi_wrapper.AMDSMI_STATUS_CORRUPTED_EEPROM
    MAP_ERROR           = amdsmi_wrapper.AMDSMI_STATUS_MAP_ERROR
    UNKNOWN_ERROR       = amdsmi_wrapper.AMDSMI_STATUS_UNKNOWN_ERROR


class AmdSmiInitFlags(IntEnum):
    INIT_ALL_PROCESSORS = amdsmi_wrapper.AMDSMI_INIT_ALL_PROCESSORS
    INIT_AMD_CPUS = amdsmi_wrapper.AMDSMI_INIT_AMD_CPUS
    INIT_AMD_GPUS = amdsmi_wrapper.AMDSMI_INIT_AMD_GPUS
    INIT_AMD_APUS = amdsmi_wrapper.AMDSMI_INIT_AMD_APUS
    INIT_NON_AMD_CPUS = amdsmi_wrapper.AMDSMI_INIT_NON_AMD_CPUS
    INIT_NON_AMD_GPUS = amdsmi_wrapper.AMDSMI_INIT_NON_AMD_GPUS


class AmdSmiContainerTypes(IntEnum):
    LXC = amdsmi_wrapper.AMDSMI_CONTAINER_LXC
    DOCKER = amdsmi_wrapper.AMDSMI_CONTAINER_DOCKER


class AmdSmiDeviceType(IntEnum):
    UNKNOWN_DEVICE = amdsmi_wrapper.AMDSMI_PROCESSOR_TYPE_UNKNOWN
    AMD_GPU_DEVICE = amdsmi_wrapper.AMDSMI_PROCESSOR_TYPE_AMD_GPU
    AMD_CPU_DEVICE = amdsmi_wrapper.AMDSMI_PROCESSOR_TYPE_AMD_CPU
    NON_AMD_GPU_DEVICE = amdsmi_wrapper.AMDSMI_PROCESSOR_TYPE_NON_AMD_GPU
    NON_AMD_CPU_DEVICE = amdsmi_wrapper.AMDSMI_PROCESSOR_TYPE_NON_AMD_CPU


class AmdSmiMmIp(IntEnum):
    UVD = amdsmi_wrapper.AMDSMI_MM_UVD
    VCE = amdsmi_wrapper.AMDSMI_MM_VCE
    VCN = amdsmi_wrapper.AMDSMI_MM_VCN


class AmdSmiFwBlock(IntEnum):
    AMDSMI_FW_ID_SMU = amdsmi_wrapper.AMDSMI_FW_ID_SMU
    AMDSMI_FW_ID_CP_CE = amdsmi_wrapper.AMDSMI_FW_ID_CP_CE
    AMDSMI_FW_ID_CP_PFP = amdsmi_wrapper.AMDSMI_FW_ID_CP_PFP
    AMDSMI_FW_ID_CP_ME = amdsmi_wrapper.AMDSMI_FW_ID_CP_ME
    AMDSMI_FW_ID_CP_MEC_JT1 = amdsmi_wrapper.AMDSMI_FW_ID_CP_MEC_JT1
    AMDSMI_FW_ID_CP_MEC_JT2 = amdsmi_wrapper.AMDSMI_FW_ID_CP_MEC_JT2
    AMDSMI_FW_ID_CP_MEC1 = amdsmi_wrapper.AMDSMI_FW_ID_CP_MEC1
    AMDSMI_FW_ID_CP_MEC2 = amdsmi_wrapper.AMDSMI_FW_ID_CP_MEC2
    AMDSMI_FW_ID_RLC = amdsmi_wrapper.AMDSMI_FW_ID_RLC
    AMDSMI_FW_ID_SDMA0 = amdsmi_wrapper.AMDSMI_FW_ID_SDMA0
    AMDSMI_FW_ID_SDMA1 = amdsmi_wrapper.AMDSMI_FW_ID_SDMA1
    AMDSMI_FW_ID_SDMA2 = amdsmi_wrapper.AMDSMI_FW_ID_SDMA2
    AMDSMI_FW_ID_SDMA3 = amdsmi_wrapper.AMDSMI_FW_ID_SDMA3
    AMDSMI_FW_ID_SDMA4 = amdsmi_wrapper.AMDSMI_FW_ID_SDMA4
    AMDSMI_FW_ID_SDMA5 = amdsmi_wrapper.AMDSMI_FW_ID_SDMA5
    AMDSMI_FW_ID_SDMA6 = amdsmi_wrapper.AMDSMI_FW_ID_SDMA6
    AMDSMI_FW_ID_SDMA7 = amdsmi_wrapper.AMDSMI_FW_ID_SDMA7
    AMDSMI_FW_ID_VCN = amdsmi_wrapper.AMDSMI_FW_ID_VCN
    AMDSMI_FW_ID_UVD = amdsmi_wrapper.AMDSMI_FW_ID_UVD
    AMDSMI_FW_ID_VCE = amdsmi_wrapper.AMDSMI_FW_ID_VCE
    AMDSMI_FW_ID_ISP = amdsmi_wrapper.AMDSMI_FW_ID_ISP
    AMDSMI_FW_ID_DMCU_ERAM = amdsmi_wrapper.AMDSMI_FW_ID_DMCU_ERAM
    AMDSMI_FW_ID_DMCU_ISR = amdsmi_wrapper.AMDSMI_FW_ID_DMCU_ISR
    AMDSMI_FW_ID_RLC_RESTORE_LIST_GPM_MEM = amdsmi_wrapper.AMDSMI_FW_ID_RLC_RESTORE_LIST_GPM_MEM
    AMDSMI_FW_ID_RLC_RESTORE_LIST_SRM_MEM = amdsmi_wrapper.AMDSMI_FW_ID_RLC_RESTORE_LIST_SRM_MEM
    AMDSMI_FW_ID_RLC_RESTORE_LIST_CNTL = amdsmi_wrapper.AMDSMI_FW_ID_RLC_RESTORE_LIST_CNTL
    AMDSMI_FW_ID_RLC_V = amdsmi_wrapper.AMDSMI_FW_ID_RLC_V
    AMDSMI_FW_ID_MMSCH = amdsmi_wrapper.AMDSMI_FW_ID_MMSCH
    AMDSMI_FW_ID_PSP_SYSDRV = amdsmi_wrapper.AMDSMI_FW_ID_PSP_SYSDRV
    AMDSMI_FW_ID_PSP_SOSDRV = amdsmi_wrapper.AMDSMI_FW_ID_PSP_SOSDRV
    AMDSMI_FW_ID_PSP_TOC = amdsmi_wrapper.AMDSMI_FW_ID_PSP_TOC
    AMDSMI_FW_ID_PSP_KEYDB = amdsmi_wrapper.AMDSMI_FW_ID_PSP_KEYDB
    AMDSMI_FW_ID_DFC = amdsmi_wrapper.AMDSMI_FW_ID_DFC
    AMDSMI_FW_ID_PSP_SPL = amdsmi_wrapper.AMDSMI_FW_ID_PSP_SPL
    AMDSMI_FW_ID_DRV_CAP = amdsmi_wrapper.AMDSMI_FW_ID_DRV_CAP
    AMDSMI_FW_ID_MC = amdsmi_wrapper.AMDSMI_FW_ID_MC
    AMDSMI_FW_ID_PSP_BL = amdsmi_wrapper.AMDSMI_FW_ID_PSP_BL
    AMDSMI_FW_ID_CP_PM4 = amdsmi_wrapper.AMDSMI_FW_ID_CP_PM4
    AMDSMI_FW_ID_RLC_P = amdsmi_wrapper.AMDSMI_FW_ID_RLC_P
    AMDSMI_FW_ID_SEC_POLICY_STAGE2 = amdsmi_wrapper.AMDSMI_FW_ID_SEC_POLICY_STAGE2
    AMDSMI_FW_ID_REG_ACCESS_WHITELIST = amdsmi_wrapper.AMDSMI_FW_ID_REG_ACCESS_WHITELIST
    AMDSMI_FW_ID_IMU_DRAM = amdsmi_wrapper.AMDSMI_FW_ID_IMU_DRAM
    AMDSMI_FW_ID_IMU_IRAM = amdsmi_wrapper.AMDSMI_FW_ID_IMU_IRAM
    AMDSMI_FW_ID_SDMA_TH0 = amdsmi_wrapper.AMDSMI_FW_ID_SDMA_TH0
    AMDSMI_FW_ID_SDMA_TH1 = amdsmi_wrapper.AMDSMI_FW_ID_SDMA_TH1
    AMDSMI_FW_ID_CP_MES = amdsmi_wrapper.AMDSMI_FW_ID_CP_MES
    AMDSMI_FW_ID_MES_STACK = amdsmi_wrapper.AMDSMI_FW_ID_MES_STACK
    AMDSMI_FW_ID_MES_THREAD1 = amdsmi_wrapper.AMDSMI_FW_ID_MES_THREAD1
    AMDSMI_FW_ID_MES_THREAD1_STACK = amdsmi_wrapper.AMDSMI_FW_ID_MES_THREAD1_STACK
    AMDSMI_FW_ID_RLX6 = amdsmi_wrapper.AMDSMI_FW_ID_RLX6
    AMDSMI_FW_ID_RLX6_DRAM_BOOT = amdsmi_wrapper.AMDSMI_FW_ID_RLX6_DRAM_BOOT
    AMDSMI_FW_ID_RS64_ME = amdsmi_wrapper.AMDSMI_FW_ID_RS64_ME
    AMDSMI_FW_ID_RS64_ME_P0_DATA = amdsmi_wrapper.AMDSMI_FW_ID_RS64_ME_P0_DATA
    AMDSMI_FW_ID_RS64_ME_P1_DATA = amdsmi_wrapper.AMDSMI_FW_ID_RS64_ME_P1_DATA
    AMDSMI_FW_ID_RS64_PFP = amdsmi_wrapper.AMDSMI_FW_ID_RS64_PFP
    AMDSMI_FW_ID_RS64_PFP_P0_DATA = amdsmi_wrapper.AMDSMI_FW_ID_RS64_PFP_P0_DATA
    AMDSMI_FW_ID_RS64_PFP_P1_DATA = amdsmi_wrapper.AMDSMI_FW_ID_RS64_PFP_P1_DATA
    AMDSMI_FW_ID_RS64_MEC = amdsmi_wrapper.AMDSMI_FW_ID_RS64_MEC
    AMDSMI_FW_ID_RS64_MEC_P0_DATA = amdsmi_wrapper.AMDSMI_FW_ID_RS64_MEC_P0_DATA
    AMDSMI_FW_ID_RS64_MEC_P1_DATA = amdsmi_wrapper.AMDSMI_FW_ID_RS64_MEC_P1_DATA
    AMDSMI_FW_ID_RS64_MEC_P2_DATA = amdsmi_wrapper.AMDSMI_FW_ID_RS64_MEC_P2_DATA
    AMDSMI_FW_ID_RS64_MEC_P3_DATA = amdsmi_wrapper.AMDSMI_FW_ID_RS64_MEC_P3_DATA
    AMDSMI_FW_ID_PPTABLE = amdsmi_wrapper.AMDSMI_FW_ID_PPTABLE
    AMDSMI_FW_ID_PSP_SOC = amdsmi_wrapper.AMDSMI_FW_ID_PSP_SOC
    AMDSMI_FW_ID_PSP_DBG = amdsmi_wrapper.AMDSMI_FW_ID_PSP_DBG
    AMDSMI_FW_ID_PSP_INTF = amdsmi_wrapper.AMDSMI_FW_ID_PSP_INTF
    AMDSMI_FW_ID_RLX6_CORE1 = amdsmi_wrapper.AMDSMI_FW_ID_RLX6_CORE1
    AMDSMI_FW_ID_RLX6_DRAM_BOOT_CORE1 = amdsmi_wrapper.AMDSMI_FW_ID_RLX6_DRAM_BOOT_CORE1
    AMDSMI_FW_ID_RLCV_LX7 = amdsmi_wrapper.AMDSMI_FW_ID_RLCV_LX7
    AMDSMI_FW_ID_RLC_SAVE_RESTORE_LIST = amdsmi_wrapper.AMDSMI_FW_ID_RLC_SAVE_RESTORE_LIST
    AMDSMI_FW_ID_ASD = amdsmi_wrapper.AMDSMI_FW_ID_ASD
    AMDSMI_FW_ID_TA_RAS = amdsmi_wrapper.AMDSMI_FW_ID_TA_RAS
    AMDSMI_FW_ID_TA_XGMI = amdsmi_wrapper.AMDSMI_FW_ID_TA_XGMI
    AMDSMI_FW_ID_RLC_SRLG = amdsmi_wrapper.AMDSMI_FW_ID_RLC_SRLG
    AMDSMI_FW_ID_RLC_SRLS = amdsmi_wrapper.AMDSMI_FW_ID_RLC_SRLS
    AMDSMI_FW_ID_PM = amdsmi_wrapper.AMDSMI_FW_ID_PM
    AMDSMI_FW_ID_DMCU = amdsmi_wrapper.AMDSMI_FW_ID_DMCU
    AMDSMI_FW_ID_PLDM_BUNDLE = amdsmi_wrapper.AMDSMI_FW_ID_PLDM_BUNDLE


class AmdSmiClkType(IntEnum):
    SYS = amdsmi_wrapper.AMDSMI_CLK_TYPE_SYS
    GFX = amdsmi_wrapper.AMDSMI_CLK_TYPE_GFX
    DF = amdsmi_wrapper.AMDSMI_CLK_TYPE_DF
    DCEF = amdsmi_wrapper.AMDSMI_CLK_TYPE_DCEF
    SOC = amdsmi_wrapper.AMDSMI_CLK_TYPE_SOC
    MEM = amdsmi_wrapper.AMDSMI_CLK_TYPE_MEM
    PCIE = amdsmi_wrapper.AMDSMI_CLK_TYPE_PCIE
    VCLK0 = amdsmi_wrapper.AMDSMI_CLK_TYPE_VCLK0
    VCLK1 = amdsmi_wrapper.AMDSMI_CLK_TYPE_VCLK1
    DCLK0 = amdsmi_wrapper.AMDSMI_CLK_TYPE_DCLK0
    DCLK1 = amdsmi_wrapper.AMDSMI_CLK_TYPE_DCLK1

class AmdSmiClkLimitType(IntEnum):
    MIN = amdsmi_wrapper.CLK_LIMIT_MIN
    MAX = amdsmi_wrapper.CLK_LIMIT_MAX

class AmdSmiTemperatureType(IntEnum):
    EDGE = amdsmi_wrapper.AMDSMI_TEMPERATURE_TYPE_EDGE
    HOTSPOT = amdsmi_wrapper.AMDSMI_TEMPERATURE_TYPE_HOTSPOT
    JUNCTION = amdsmi_wrapper.AMDSMI_TEMPERATURE_TYPE_JUNCTION
    VRAM = amdsmi_wrapper.AMDSMI_TEMPERATURE_TYPE_VRAM
    HBM_0 = amdsmi_wrapper.AMDSMI_TEMPERATURE_TYPE_HBM_0
    HBM_1 = amdsmi_wrapper.AMDSMI_TEMPERATURE_TYPE_HBM_1
    HBM_2 = amdsmi_wrapper.AMDSMI_TEMPERATURE_TYPE_HBM_2
    HBM_3 = amdsmi_wrapper.AMDSMI_TEMPERATURE_TYPE_HBM_3
    PLX = amdsmi_wrapper.AMDSMI_TEMPERATURE_TYPE_PLX

    # GPU Board Node temperature
    GPUBOARD_NODE_RETIMER_X = amdsmi_wrapper.AMDSMI_TEMPERATURE_TYPE_GPUBOARD_NODE_RETIMER_X  # Retimer X temperature
    GPUBOARD_NODE_OAM_X_IBC = amdsmi_wrapper.AMDSMI_TEMPERATURE_TYPE_GPUBOARD_NODE_OAM_X_IBC         # OAM X IBC temperature
    GPUBOARD_NODE_OAM_X_IBC_2 = amdsmi_wrapper.AMDSMI_TEMPERATURE_TYPE_GPUBOARD_NODE_OAM_X_IBC_2       # OAM X IBC 2 temperature
    GPUBOARD_NODE_OAM_X_VDD18_VR = amdsmi_wrapper.AMDSMI_TEMPERATURE_TYPE_GPUBOARD_NODE_OAM_X_VDD18_VR    # OAM X VDD 1.8V voltage regulator temperature
    GPUBOARD_NODE_OAM_X_04_HBM_B_VR = amdsmi_wrapper.AMDSMI_TEMPERATURE_TYPE_GPUBOARD_NODE_OAM_X_04_HBM_B_VR # OAM X 0.4V HBM B voltage regulator temperature
    GPUBOARD_NODE_OAM_X_04_HBM_D_VR = amdsmi_wrapper.AMDSMI_TEMPERATURE_TYPE_GPUBOARD_NODE_OAM_X_04_HBM_D_VR # OAM X 0.4V HBM D voltage regulator temperature
    GPUBOARD_NODE_LAST = amdsmi_wrapper.AMDSMI_TEMPERATURE_TYPE_GPUBOARD_NODE_LAST

    # GPU Board VR (Voltage Regulator) temperature
    GPUBOARD_VDDCR_VDD0 = amdsmi_wrapper.AMDSMI_TEMPERATURE_TYPE_GPUBOARD_VDDCR_VDD0        # VDDCR VDD0 voltage regulator temperature
    GPUBOARD_VDDCR_VDD1 = amdsmi_wrapper.AMDSMI_TEMPERATURE_TYPE_GPUBOARD_VDDCR_VDD1        # VDDCR VDD1 voltage regulator temperature
    GPUBOARD_VDDCR_VDD2 = amdsmi_wrapper.AMDSMI_TEMPERATURE_TYPE_GPUBOARD_VDDCR_VDD2        # VDDCR VDD2 voltage regulator temperature
    GPUBOARD_VDDCR_VDD3 = amdsmi_wrapper.AMDSMI_TEMPERATURE_TYPE_GPUBOARD_VDDCR_VDD3        # VDDCR VDD3 voltage regulator temperature
    GPUBOARD_VDDCR_SOC_A = amdsmi_wrapper.AMDSMI_TEMPERATURE_TYPE_GPUBOARD_VDDCR_SOC_A       # VDDCR SOC A voltage regulator temperature
    GPUBOARD_VDDCR_SOC_C = amdsmi_wrapper.AMDSMI_TEMPERATURE_TYPE_GPUBOARD_VDDCR_SOC_C       # VDDCR SOC C voltage regulator temperature
    GPUBOARD_VDDCR_SOCIO_A = amdsmi_wrapper.AMDSMI_TEMPERATURE_TYPE_GPUBOARD_VDDCR_SOCIO_A     # VDDCR SOCIO A voltage regulator temperature
    GPUBOARD_VDDCR_SOCIO_C = amdsmi_wrapper.AMDSMI_TEMPERATURE_TYPE_GPUBOARD_VDDCR_SOCIO_C     # VDDCR SOCIO C voltage regulator temperature
    GPUBOARD_VDD_085_HBM = amdsmi_wrapper.AMDSMI_TEMPERATURE_TYPE_GPUBOARD_VDD_085_HBM       # VDD 0.85V HBM voltage regulator temperature
    GPUBOARD_VDDCR_11_HBM_B = amdsmi_wrapper.AMDSMI_TEMPERATURE_TYPE_GPUBOARD_VDDCR_11_HBM_B    # VDDCR 1.1V HBM B voltage regulator temperature
    GPUBOARD_VDDCR_11_HBM_D = amdsmi_wrapper.AMDSMI_TEMPERATURE_TYPE_GPUBOARD_VDDCR_11_HBM_D    # VDDCR 1.1V HBM D voltage regulator temperature
    GPUBOARD_VDD_USR = amdsmi_wrapper.AMDSMI_TEMPERATURE_TYPE_GPUBOARD_VDD_USR           # VDD USR voltage regulator temperature
    GPUBOARD_VDDIO_11_E32 = amdsmi_wrapper.AMDSMI_TEMPERATURE_TYPE_GPUBOARD_VDDIO_11_E32      # VDDIO 1.1V E32 voltage regulator temperature
    GPUBOARD_VR_LAST = amdsmi_wrapper.AMDSMI_TEMPERATURE_TYPE_GPUBOARD_VR_LAST

    # Baseboard System temperature
    BASEBOARD_UBB_FPGA = amdsmi_wrapper.AMDSMI_TEMPERATURE_TYPE_BASEBOARD_UBB_FPGA       # UBB FPGA temperature
    BASEBOARD_UBB_FRONT = amdsmi_wrapper.AMDSMI_TEMPERATURE_TYPE_BASEBOARD_UBB_FRONT         # UBB front temperature
    BASEBOARD_UBB_BACK = amdsmi_wrapper.AMDSMI_TEMPERATURE_TYPE_BASEBOARD_UBB_BACK          # UBB back temperature
    BASEBOARD_UBB_OAM7 = amdsmi_wrapper.AMDSMI_TEMPERATURE_TYPE_BASEBOARD_UBB_OAM7          # UBB OAM7 temperature
    BASEBOARD_UBB_IBC = amdsmi_wrapper.AMDSMI_TEMPERATURE_TYPE_BASEBOARD_UBB_IBC           # UBB IBC temperature
    BASEBOARD_UBB_UFPGA = amdsmi_wrapper.AMDSMI_TEMPERATURE_TYPE_BASEBOARD_UBB_UFPGA         # UBB UFPGA temperature
    BASEBOARD_UBB_OAM1 = amdsmi_wrapper.AMDSMI_TEMPERATURE_TYPE_BASEBOARD_UBB_OAM1          # UBB OAM1 temperature
    BASEBOARD_OAM_0_1_HSC = amdsmi_wrapper.AMDSMI_TEMPERATURE_TYPE_BASEBOARD_OAM_0_1_HSC       # OAM 0-1 HSC temperature
    BASEBOARD_OAM_2_3_HSC = amdsmi_wrapper.AMDSMI_TEMPERATURE_TYPE_BASEBOARD_OAM_2_3_HSC       # OAM 2-3 HSC temperature
    BASEBOARD_OAM_4_5_HSC = amdsmi_wrapper.AMDSMI_TEMPERATURE_TYPE_BASEBOARD_OAM_4_5_HSC       # OAM 4-5 HSC temperature
    BASEBOARD_OAM_6_7_HSC = amdsmi_wrapper.AMDSMI_TEMPERATURE_TYPE_BASEBOARD_OAM_6_7_HSC       # OAM 6-7 HSC temperature
    BASEBOARD_UBB_FPGA_0V72_VR = amdsmi_wrapper.AMDSMI_TEMPERATURE_TYPE_BASEBOARD_UBB_FPGA_0V72_VR  # UBB FPGA 0.72V voltage regulator temperature
    BASEBOARD_UBB_FPGA_3V3_VR = amdsmi_wrapper.AMDSMI_TEMPERATURE_TYPE_BASEBOARD_UBB_FPGA_3V3_VR   # UBB FPGA 3.3V voltage regulator temperature
    BASEBOARD_RETIMER_0_1_2_3_1V2_VR = amdsmi_wrapper.AMDSMI_TEMPERATURE_TYPE_BASEBOARD_RETIMER_0_1_2_3_1V2_VR  # Retimer 0-1-2-3 1.2V voltage regulator temperature
    BASEBOARD_RETIMER_4_5_6_7_1V2_VR = amdsmi_wrapper.AMDSMI_TEMPERATURE_TYPE_BASEBOARD_RETIMER_4_5_6_7_1V2_VR  # Retimer 4-5-6-7 1.2V voltage regulator temperature
    BASEBOARD_RETIMER_0_1_0V9_VR = amdsmi_wrapper.AMDSMI_TEMPERATURE_TYPE_BASEBOARD_RETIMER_0_1_0V9_VR # Retimer 0-1 0.9V voltage regulator temperature
    BASEBOARD_RETIMER_4_5_0V9_VR= amdsmi_wrapper.AMDSMI_TEMPERATURE_TYPE_BASEBOARD_RETIMER_4_5_0V9_VR # Retimer 4-5 0.9V voltage regulator temperature
    BASEBOARD_RETIMER_2_3_0V9_VR = amdsmi_wrapper.AMDSMI_TEMPERATURE_TYPE_BASEBOARD_RETIMER_2_3_0V9_VR # Retimer 2-3 0.9V voltage regulator temperature
    BASEBOARD_RETIMER_6_7_0V9_VR = amdsmi_wrapper.AMDSMI_TEMPERATURE_TYPE_BASEBOARD_RETIMER_6_7_0V9_VR # Retimer 6-7 0.9V voltage regulator temperature
    BASEBOARD_OAM_0_1_2_3_3V3_VR = amdsmi_wrapper.AMDSMI_TEMPERATURE_TYPE_BASEBOARD_OAM_0_1_2_3_3V3_VR # OAM 0-1-2-3 3.3V voltage regulator temperature
    BASEBOARD_OAM_4_5_6_7_3V3_VR = amdsmi_wrapper.AMDSMI_TEMPERATURE_TYPE_BASEBOARD_OAM_4_5_6_7_3V3_VR # OAM 4-5-6-7 3.3V voltage regulator temperature
    BASEBOARD_IBC_HSC = amdsmi_wrapper.AMDSMI_TEMPERATURE_TYPE_BASEBOARD_IBC_HSC           # IBC HSC temperature
    BASEBOARD_IBC = amdsmi_wrapper.AMDSMI_TEMPERATURE_TYPE_BASEBOARD_IBC               # IBC temperature
    BASEBOARD_LAST = amdsmi_wrapper.AMDSMI_TEMPERATURE_TYPE_BASEBOARD_LAST
    BASEBOARD__MAX = amdsmi_wrapper.AMDSMI_TEMPERATURE_TYPE__MAX # Maximum per GPU temperature type


class AmdSmiDevPerfLevel(IntEnum):
    AUTO = amdsmi_wrapper.AMDSMI_DEV_PERF_LEVEL_AUTO
    LOW = amdsmi_wrapper.AMDSMI_DEV_PERF_LEVEL_LOW
    HIGH = amdsmi_wrapper.AMDSMI_DEV_PERF_LEVEL_HIGH
    MANUAL = amdsmi_wrapper.AMDSMI_DEV_PERF_LEVEL_MANUAL
    STABLE_STD = amdsmi_wrapper.AMDSMI_DEV_PERF_LEVEL_STABLE_STD
    STABLE_PEAK = amdsmi_wrapper.AMDSMI_DEV_PERF_LEVEL_STABLE_PEAK
    STABLE_MIN_MCLK = amdsmi_wrapper.AMDSMI_DEV_PERF_LEVEL_STABLE_MIN_MCLK
    STABLE_MIN_SCLK = amdsmi_wrapper.AMDSMI_DEV_PERF_LEVEL_STABLE_MIN_SCLK
    DETERMINISM = amdsmi_wrapper.AMDSMI_DEV_PERF_LEVEL_DETERMINISM
    UNKNOWN = amdsmi_wrapper.AMDSMI_DEV_PERF_LEVEL_UNKNOWN


class AmdSmiEventGroup(IntEnum):
    XGMI = amdsmi_wrapper.AMDSMI_EVNT_GRP_XGMI
    XGMI_DATA_OUT = amdsmi_wrapper.AMDSMI_EVNT_GRP_XGMI_DATA_OUT
    GRP_INVALID = amdsmi_wrapper.AMDSMI_EVNT_GRP_INVALID


class AmdSmiEventType(IntEnum):
    XGMI_0_NOP_TX = amdsmi_wrapper.AMDSMI_EVNT_XGMI_0_NOP_TX
    XGMI_0_REQUEST_TX = amdsmi_wrapper.AMDSMI_EVNT_XGMI_0_REQUEST_TX
    XGMI_0_RESPONSE_TX = amdsmi_wrapper.AMDSMI_EVNT_XGMI_0_RESPONSE_TX
    XGMI_0_BEATS_TX = amdsmi_wrapper.AMDSMI_EVNT_XGMI_0_BEATS_TX
    XGMI_1_NOP_TX = amdsmi_wrapper.AMDSMI_EVNT_XGMI_1_NOP_TX
    XGMI_1_REQUEST_TX = amdsmi_wrapper.AMDSMI_EVNT_XGMI_1_REQUEST_TX
    XGMI_1_RESPONSE_TX = amdsmi_wrapper.AMDSMI_EVNT_XGMI_1_RESPONSE_TX
    XGMI_1_BEATS_TX = amdsmi_wrapper.AMDSMI_EVNT_XGMI_1_BEATS_TX
    XGMI_DATA_OUT_0 = amdsmi_wrapper.AMDSMI_EVNT_XGMI_DATA_OUT_0
    XGMI_DATA_OUT_1 = amdsmi_wrapper.AMDSMI_EVNT_XGMI_DATA_OUT_1
    XGMI_DATA_OUT_2 = amdsmi_wrapper.AMDSMI_EVNT_XGMI_DATA_OUT_2
    XGMI_DATA_OUT_3 = amdsmi_wrapper.AMDSMI_EVNT_XGMI_DATA_OUT_3
    XGMI_DATA_OUT_4 = amdsmi_wrapper.AMDSMI_EVNT_XGMI_DATA_OUT_4
    XGMI_DATA_OUT_5 = amdsmi_wrapper.AMDSMI_EVNT_XGMI_DATA_OUT_5


class AmdSmiCounterCommand(IntEnum):
    CMD_START = amdsmi_wrapper.AMDSMI_CNTR_CMD_START
    CMD_STOP = amdsmi_wrapper.AMDSMI_CNTR_CMD_STOP


class AmdSmiEvtNotificationType(IntEnum):
    NONE = amdsmi_wrapper.AMDSMI_EVT_NOTIF_NONE
    VMFAULT = amdsmi_wrapper.AMDSMI_EVT_NOTIF_VMFAULT
    THERMAL_THROTTLE = amdsmi_wrapper.AMDSMI_EVT_NOTIF_THERMAL_THROTTLE
    GPU_PRE_RESET = amdsmi_wrapper.AMDSMI_EVT_NOTIF_GPU_PRE_RESET
    GPU_POST_RESET = amdsmi_wrapper.AMDSMI_EVT_NOTIF_GPU_POST_RESET
    MIGRATE_START = amdsmi_wrapper.AMDSMI_EVT_NOTIF_MIGRATE_START
    MIGRATE_END = amdsmi_wrapper.AMDSMI_EVT_NOTIF_MIGRATE_END
    PAGE_FAULT_START = amdsmi_wrapper.AMDSMI_EVT_NOTIF_PAGE_FAULT_END
    PAGE_FAULT_END = amdsmi_wrapper.AMDSMI_EVT_NOTIF_PAGE_FAULT_END
    QUEUE_EVICTION = amdsmi_wrapper.AMDSMI_EVT_NOTIF_QUEUE_EVICTION
    QUEUE_RESTORE = amdsmi_wrapper.AMDSMI_EVT_NOTIF_QUEUE_RESTORE
    UNMAP_FROM_GPU = amdsmi_wrapper.AMDSMI_EVT_NOTIF_UNMAP_FROM_GPU
    PROCESS_START = amdsmi_wrapper.AMDSMI_EVT_NOTIF_PROCESS_START
    PROCESS_END = amdsmi_wrapper.AMDSMI_EVT_NOTIF_PROCESS_END


class AmdSmiTemperatureMetric(IntEnum):
    CURRENT = amdsmi_wrapper.AMDSMI_TEMP_CURRENT
    MAX = amdsmi_wrapper.AMDSMI_TEMP_MAX
    MIN = amdsmi_wrapper.AMDSMI_TEMP_MIN
    MAX_HYST = amdsmi_wrapper.AMDSMI_TEMP_MAX_HYST
    MIN_HYST = amdsmi_wrapper.AMDSMI_TEMP_MIN_HYST
    CRITICAL = amdsmi_wrapper.AMDSMI_TEMP_CRITICAL
    CRITICAL_HYST = amdsmi_wrapper.AMDSMI_TEMP_CRITICAL_HYST
    EMERGENCY = amdsmi_wrapper.AMDSMI_TEMP_EMERGENCY
    EMERGENCY_HYST = amdsmi_wrapper.AMDSMI_TEMP_EMERGENCY_HYST
    CRIT_MIN = amdsmi_wrapper.AMDSMI_TEMP_CRIT_MIN
    CRIT_MIN_HYST = amdsmi_wrapper.AMDSMI_TEMP_CRIT_MIN_HYST
    OFFSET = amdsmi_wrapper.AMDSMI_TEMP_OFFSET
    LOWEST = amdsmi_wrapper.AMDSMI_TEMP_LOWEST
    HIGHEST = amdsmi_wrapper.AMDSMI_TEMP_HIGHEST


class AmdSmiVoltageMetric(IntEnum):
    CURRENT = amdsmi_wrapper.AMDSMI_VOLT_CURRENT
    MAX = amdsmi_wrapper.AMDSMI_VOLT_MAX
    MIN_CRIT = amdsmi_wrapper.AMDSMI_VOLT_MIN_CRIT
    MIN = amdsmi_wrapper.AMDSMI_VOLT_MIN
    MAX_CRIT = amdsmi_wrapper.AMDSMI_VOLT_MAX_CRIT
    AVERAGE = amdsmi_wrapper.AMDSMI_VOLT_AVERAGE
    LOWEST = amdsmi_wrapper.AMDSMI_VOLT_LOWEST
    HIGHEST = amdsmi_wrapper.AMDSMI_VOLT_HIGHEST


class AmdSmiVoltageType(IntEnum):
    VDDGFX = amdsmi_wrapper.AMDSMI_VOLT_TYPE_VDDGFX
    VDDBOARD = amdsmi_wrapper.AMDSMI_VOLT_TYPE_VDDBOARD
    INVALID = amdsmi_wrapper.AMDSMI_VOLT_TYPE_INVALID

class AmdSmiAcceleratorPartitionResourceType(IntEnum):
    XCC = amdsmi_wrapper.AMDSMI_ACCELERATOR_XCC
    ENCODER = amdsmi_wrapper.AMDSMI_ACCELERATOR_ENCODER
    DECODER = amdsmi_wrapper.AMDSMI_ACCELERATOR_DECODER
    DMA = amdsmi_wrapper.AMDSMI_ACCELERATOR_DMA
    JPEG = amdsmi_wrapper.AMDSMI_ACCELERATOR_JPEG
    MAX = amdsmi_wrapper.AMDSMI_ACCELERATOR_MAX


class AmdSmiAcceleratorPartitionType(IntEnum):
    SPX = amdsmi_wrapper.AMDSMI_ACCELERATOR_PARTITION_SPX
    DPX = amdsmi_wrapper.AMDSMI_ACCELERATOR_PARTITION_DPX
    TPX = amdsmi_wrapper.AMDSMI_ACCELERATOR_PARTITION_TPX
    QPX = amdsmi_wrapper.AMDSMI_ACCELERATOR_PARTITION_QPX
    CPX = amdsmi_wrapper.AMDSMI_ACCELERATOR_PARTITION_CPX
    INVALID = amdsmi_wrapper.AMDSMI_ACCELERATOR_PARTITION_INVALID


class AmdSmiComputePartitionType(IntEnum):
    SPX = amdsmi_wrapper.AMDSMI_COMPUTE_PARTITION_SPX
    DPX = amdsmi_wrapper.AMDSMI_COMPUTE_PARTITION_DPX
    TPX = amdsmi_wrapper.AMDSMI_COMPUTE_PARTITION_TPX
    QPX = amdsmi_wrapper.AMDSMI_COMPUTE_PARTITION_QPX
    CPX = amdsmi_wrapper.AMDSMI_COMPUTE_PARTITION_CPX
    INVALID = amdsmi_wrapper.AMDSMI_COMPUTE_PARTITION_INVALID


class AmdSmiMemoryPartitionType(IntEnum):
    NPS1 = amdsmi_wrapper.AMDSMI_MEMORY_PARTITION_NPS1
    NPS2 = amdsmi_wrapper.AMDSMI_MEMORY_PARTITION_NPS2
    NPS4 = amdsmi_wrapper.AMDSMI_MEMORY_PARTITION_NPS4
    NPS8 = amdsmi_wrapper.AMDSMI_MEMORY_PARTITION_NPS8
    UNKNOWN = amdsmi_wrapper.AMDSMI_MEMORY_PARTITION_UNKNOWN


class AmdSmiPowerProfilePresetMasks(IntEnum):
    CUSTOM_MASK = amdsmi_wrapper.AMDSMI_PWR_PROF_PRST_CUSTOM_MASK
    VIDEO_MASK = amdsmi_wrapper.AMDSMI_PWR_PROF_PRST_VIDEO_MASK
    POWER_SAVING_MASK = amdsmi_wrapper.AMDSMI_PWR_PROF_PRST_POWER_SAVING_MASK
    COMPUTE_MASK = amdsmi_wrapper.AMDSMI_PWR_PROF_PRST_COMPUTE_MASK
    VR_MASK = amdsmi_wrapper.AMDSMI_PWR_PROF_PRST_VR_MASK
    THREE_D_FULL_SCR_MASK = amdsmi_wrapper.AMDSMI_PWR_PROF_PRST_3D_FULL_SCR_MASK
    BOOTUP_DEFAULT = amdsmi_wrapper.AMDSMI_PWR_PROF_PRST_BOOTUP_DEFAULT
    INVALID = amdsmi_wrapper.AMDSMI_PWR_PROF_PRST_INVALID


class AmdSmiGpuBlock(IntEnum):
    INVALID = amdsmi_wrapper.AMDSMI_GPU_BLOCK_INVALID
    UMC = amdsmi_wrapper.AMDSMI_GPU_BLOCK_UMC
    SDMA = amdsmi_wrapper.AMDSMI_GPU_BLOCK_SDMA
    GFX = amdsmi_wrapper.AMDSMI_GPU_BLOCK_GFX
    MMHUB = amdsmi_wrapper.AMDSMI_GPU_BLOCK_MMHUB
    ATHUB = amdsmi_wrapper.AMDSMI_GPU_BLOCK_ATHUB
    PCIE_BIF = amdsmi_wrapper.AMDSMI_GPU_BLOCK_PCIE_BIF
    HDP = amdsmi_wrapper.AMDSMI_GPU_BLOCK_HDP
    XGMI_WAFL = amdsmi_wrapper.AMDSMI_GPU_BLOCK_XGMI_WAFL
    DF = amdsmi_wrapper.AMDSMI_GPU_BLOCK_DF
    SMN = amdsmi_wrapper.AMDSMI_GPU_BLOCK_SMN
    SEM = amdsmi_wrapper.AMDSMI_GPU_BLOCK_SEM
    MP0 = amdsmi_wrapper.AMDSMI_GPU_BLOCK_MP0
    MP1 = amdsmi_wrapper.AMDSMI_GPU_BLOCK_MP1
    FUSE = amdsmi_wrapper.AMDSMI_GPU_BLOCK_FUSE
    MCA = amdsmi_wrapper.AMDSMI_GPU_BLOCK_MCA
    VCN = amdsmi_wrapper.AMDSMI_GPU_BLOCK_VCN
    JPEG = amdsmi_wrapper.AMDSMI_GPU_BLOCK_JPEG
    IH = amdsmi_wrapper.AMDSMI_GPU_BLOCK_IH
    MPIO = amdsmi_wrapper.AMDSMI_GPU_BLOCK_MPIO
    RESERVED = amdsmi_wrapper.AMDSMI_GPU_BLOCK_RESERVED


class AmdSmiRasErrState(IntEnum):
    NONE = amdsmi_wrapper.AMDSMI_RAS_ERR_STATE_NONE
    DISABLED = amdsmi_wrapper.AMDSMI_RAS_ERR_STATE_DISABLED
    PARITY = amdsmi_wrapper.AMDSMI_RAS_ERR_STATE_PARITY
    SING_C = amdsmi_wrapper.AMDSMI_RAS_ERR_STATE_SING_C
    MULT_UC = amdsmi_wrapper.AMDSMI_RAS_ERR_STATE_MULT_UC
    POISON = amdsmi_wrapper.AMDSMI_RAS_ERR_STATE_POISON
    ENABLED = amdsmi_wrapper.AMDSMI_RAS_ERR_STATE_ENABLED
    INVALID = amdsmi_wrapper.AMDSMI_RAS_ERR_STATE_INVALID


class AmdSmiCperNotifyType(Enum):
    CMC = amdsmi_wrapper.AMDSMI_CPER_NOTIFY_TYPE_CMC
    CPE = amdsmi_wrapper.AMDSMI_CPER_NOTIFY_TYPE_CPE
    MCE = amdsmi_wrapper.AMDSMI_CPER_NOTIFY_TYPE_MCE
    PCIE = amdsmi_wrapper.AMDSMI_CPER_NOTIFY_TYPE_PCIE
    INIT = amdsmi_wrapper.AMDSMI_CPER_NOTIFY_TYPE_INIT
    NMI = amdsmi_wrapper.AMDSMI_CPER_NOTIFY_TYPE_NMI
    BOOT = amdsmi_wrapper.AMDSMI_CPER_NOTIFY_TYPE_BOOT
    DMAr = amdsmi_wrapper.AMDSMI_CPER_NOTIFY_TYPE_DMAR
    SEA =  amdsmi_wrapper.AMDSMI_CPER_NOTIFY_TYPE_SEA
    SEI = amdsmi_wrapper.AMDSMI_CPER_NOTIFY_TYPE_SEI
    PEI = amdsmi_wrapper.AMDSMI_CPER_NOTIFY_TYPE_PEI
    CXL_COMPONENT = amdsmi_wrapper.AMDSMI_CPER_NOTIFY_TYPE_CXL_COMPONENT


class AmdSmiMemoryType(IntEnum):
    VRAM = amdsmi_wrapper.AMDSMI_MEM_TYPE_VRAM
    VIS_VRAM = amdsmi_wrapper.AMDSMI_MEM_TYPE_VIS_VRAM
    GTT = amdsmi_wrapper.AMDSMI_MEM_TYPE_GTT


class AmdSmiFreqInd(IntEnum):
    MIN = amdsmi_wrapper.AMDSMI_FREQ_IND_MIN
    MAX = amdsmi_wrapper.AMDSMI_FREQ_IND_MAX
    INVALID = amdsmi_wrapper.AMDSMI_FREQ_IND_INVALID


class AmdSmiXgmiStatus(IntEnum):
    NO_ERRORS = amdsmi_wrapper.AMDSMI_XGMI_STATUS_NO_ERRORS
    ERROR = amdsmi_wrapper.AMDSMI_XGMI_STATUS_ERROR
    MULTIPLE_ERRORS = amdsmi_wrapper.AMDSMI_XGMI_STATUS_MULTIPLE_ERRORS


class AmdSmiMemoryPageStatus(IntEnum):
    RESERVED = amdsmi_wrapper.AMDSMI_MEM_PAGE_STATUS_RESERVED
    PENDING = amdsmi_wrapper.AMDSMI_MEM_PAGE_STATUS_PENDING
    UNRESERVABLE = amdsmi_wrapper.AMDSMI_MEM_PAGE_STATUS_UNRESERVABLE


class AmdSmiLinkType(IntEnum):
    AMDSMI_LINK_TYPE_INTERNAL = amdsmi_wrapper.AMDSMI_LINK_TYPE_INTERNAL
    AMDSMI_LINK_TYPE_XGMI = amdsmi_wrapper.AMDSMI_LINK_TYPE_XGMI
    AMDSMI_LINK_TYPE_PCIE = amdsmi_wrapper.AMDSMI_LINK_TYPE_PCIE
    AMDSMI_LINK_TYPE_NOT_APPLICABLE = amdsmi_wrapper.AMDSMI_LINK_TYPE_NOT_APPLICABLE
    AMDSMI_LINK_TYPE_UNKNOWN = amdsmi_wrapper.AMDSMI_LINK_TYPE_UNKNOWN


class AmdSmiUtilizationCounterType(IntEnum):
    COARSE_GRAIN_GFX_ACTIVITY = amdsmi_wrapper.AMDSMI_COARSE_GRAIN_GFX_ACTIVITY
    COARSE_GRAIN_MEM_ACTIVITY = amdsmi_wrapper.AMDSMI_COARSE_GRAIN_MEM_ACTIVITY
    COARSE_DECODER_ACTIVITY = amdsmi_wrapper.AMDSMI_COARSE_DECODER_ACTIVITY
    FINE_GRAIN_GFX_ACTIVITY = amdsmi_wrapper.AMDSMI_FINE_GRAIN_GFX_ACTIVITY
    FINE_GRAIN_MEM_ACTIVITY = amdsmi_wrapper.AMDSMI_FINE_GRAIN_MEM_ACTIVITY
    FINE_DECODER_ACTIVITY = amdsmi_wrapper.AMDSMI_FINE_DECODER_ACTIVITY
    UTILIZATION_COUNTER_FIRST = amdsmi_wrapper.AMDSMI_UTILIZATION_COUNTER_FIRST
    UTILIZATION_COUNTER_LAST = amdsmi_wrapper.AMDSMI_UTILIZATION_COUNTER_LAST


class AmdSmiProcessorType(IntEnum):
    UNKNOWN = amdsmi_wrapper.AMDSMI_PROCESSOR_TYPE_UNKNOWN
    AMD_GPU = amdsmi_wrapper.AMDSMI_PROCESSOR_TYPE_AMD_GPU
    AMD_CPU = amdsmi_wrapper.AMDSMI_PROCESSOR_TYPE_AMD_CPU
    NON_AMD_GPU = amdsmi_wrapper.AMDSMI_PROCESSOR_TYPE_NON_AMD_GPU
    NON_AMD_CPU = amdsmi_wrapper.AMDSMI_PROCESSOR_TYPE_NON_AMD_CPU
    AMD_CPU_CORE = amdsmi_wrapper.AMDSMI_PROCESSOR_TYPE_AMD_CPU_CORE
    AMD_APU = amdsmi_wrapper.AMDSMI_PROCESSOR_TYPE_AMD_APU


class AmdSmiRegType(IntEnum):
    XGMI = amdsmi_wrapper.AMDSMI_REG_XGMI
    WAFL = amdsmi_wrapper.AMDSMI_REG_WAFL
    PCIE = amdsmi_wrapper.AMDSMI_REG_PCIE
    USR = amdsmi_wrapper.AMDSMI_REG_USR
    USR1 = amdsmi_wrapper.AMDSMI_REG_USR1


class AmdSmiVirtualizationMode(IntEnum):
    UNKNOWN = amdsmi_wrapper.AMDSMI_VIRTUALIZATION_MODE_UNKNOWN
    BAREMETAL = amdsmi_wrapper.AMDSMI_VIRTUALIZATION_MODE_BAREMETAL
    HOST = amdsmi_wrapper.AMDSMI_VIRTUALIZATION_MODE_HOST
    GUEST = amdsmi_wrapper.AMDSMI_VIRTUALIZATION_MODE_GUEST
    PASSTHROUGH = amdsmi_wrapper.AMDSMI_VIRTUALIZATION_MODE_PASSTHROUGH


class AmdSmiVramType(IntEnum):
    UNKNOWN = amdsmi_wrapper.AMDSMI_VRAM_TYPE_UNKNOWN
    HBM = amdsmi_wrapper.AMDSMI_VRAM_TYPE_HBM
    HBM2 = amdsmi_wrapper.AMDSMI_VRAM_TYPE_HBM2
    HBM2E = amdsmi_wrapper.AMDSMI_VRAM_TYPE_HBM2E
    HBM3 = amdsmi_wrapper.AMDSMI_VRAM_TYPE_HBM3
    DDR2 = amdsmi_wrapper.AMDSMI_VRAM_TYPE_DDR2
    DDR3 = amdsmi_wrapper.AMDSMI_VRAM_TYPE_DDR3
    DDR4 = amdsmi_wrapper.AMDSMI_VRAM_TYPE_DDR4
    GDDR1 = amdsmi_wrapper.AMDSMI_VRAM_TYPE_GDDR1
    GDDR2 = amdsmi_wrapper.AMDSMI_VRAM_TYPE_GDDR2
    GDDR3 = amdsmi_wrapper.AMDSMI_VRAM_TYPE_GDDR3
    GDDR4 = amdsmi_wrapper.AMDSMI_VRAM_TYPE_GDDR4
    GDDR5 = amdsmi_wrapper.AMDSMI_VRAM_TYPE_GDDR5
    GDDR6 = amdsmi_wrapper.AMDSMI_VRAM_TYPE_GDDR6
    GDDR7 = amdsmi_wrapper.AMDSMI_VRAM_TYPE_GDDR7
    MAX = amdsmi_wrapper.AMDSMI_VRAM_TYPE__MAX


class AmdSmiAffinityScope(IntEnum):
    NUMA_SCOPE = amdsmi_wrapper.AMDSMI_AFFINITY_SCOPE_NODE
    SOCKET_SCOPE = amdsmi_wrapper.AMDSMI_AFFINITY_SCOPE_SOCKET


class AmdSmiPowerCapType(IntEnum):
    PPT0 = amdsmi_wrapper.AMDSMI_POWER_CAP_TYPE_PPT0
    PPT1 = amdsmi_wrapper.AMDSMI_POWER_CAP_TYPE_PPT1

