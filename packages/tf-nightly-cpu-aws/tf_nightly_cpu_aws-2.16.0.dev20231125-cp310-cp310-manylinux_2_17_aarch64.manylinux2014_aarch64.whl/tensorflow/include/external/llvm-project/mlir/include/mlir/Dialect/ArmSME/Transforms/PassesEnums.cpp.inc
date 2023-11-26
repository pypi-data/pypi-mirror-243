/*===- TableGen'erated file -------------------------------------*- C++ -*-===*\
|*                                                                            *|
|* Enum Utility Definitions                                                   *|
|*                                                                            *|
|* Automatically generated file, do not edit!                                 *|
|* From: Passes.td                                                            *|
|*                                                                            *|
\*===----------------------------------------------------------------------===*/

namespace mlir {
namespace arm_sme {
::llvm::StringRef stringifyArmStreamingMode(ArmStreamingMode val) {
  switch (val) {
    case ArmStreamingMode::Disabled: return "disabled";
    case ArmStreamingMode::Streaming: return "arm_streaming";
    case ArmStreamingMode::StreamingLocally: return "arm_locally_streaming";
  }
  return "";
}

::std::optional<ArmStreamingMode> symbolizeArmStreamingMode(::llvm::StringRef str) {
  return ::llvm::StringSwitch<::std::optional<ArmStreamingMode>>(str)
      .Case("disabled", ArmStreamingMode::Disabled)
      .Case("arm_streaming", ArmStreamingMode::Streaming)
      .Case("arm_locally_streaming", ArmStreamingMode::StreamingLocally)
      .Default(::std::nullopt);
}
::std::optional<ArmStreamingMode> symbolizeArmStreamingMode(uint32_t value) {
  switch (value) {
  case 0: return ArmStreamingMode::Disabled;
  case 1: return ArmStreamingMode::Streaming;
  case 2: return ArmStreamingMode::StreamingLocally;
  default: return ::std::nullopt;
  }
}

} // namespace arm_sme
} // namespace mlir

namespace mlir {
namespace arm_sme {
::llvm::StringRef stringifyArmZaMode(ArmZaMode val) {
  switch (val) {
    case ArmZaMode::Disabled: return "disabled";
    case ArmZaMode::NewZA: return "arm_new_za";
  }
  return "";
}

::std::optional<ArmZaMode> symbolizeArmZaMode(::llvm::StringRef str) {
  return ::llvm::StringSwitch<::std::optional<ArmZaMode>>(str)
      .Case("disabled", ArmZaMode::Disabled)
      .Case("arm_new_za", ArmZaMode::NewZA)
      .Default(::std::nullopt);
}
::std::optional<ArmZaMode> symbolizeArmZaMode(uint32_t value) {
  switch (value) {
  case 0: return ArmZaMode::Disabled;
  case 1: return ArmZaMode::NewZA;
  default: return ::std::nullopt;
  }
}

} // namespace arm_sme
} // namespace mlir

