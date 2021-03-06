message(STATUS "Finding Bitmain Decode")

set(BMDECODE_COMPONENTS
    bmvideo
    bmjpuapi
    bmjpulite)

set(BMDECODE_INCLUDE_DIRS
    ${BMDECODER_DIR}/include/decode)

foreach(ITEM ${BMDECODE_COMPONENTS})
  list(APPEND BMDECODE_LIBRARIES "${BMNNSDK2_PATH}/lib/decode/arm_pcie/lib${ITEM}.so")
endforeach()

if(BMDECODE_INCLUDE_DIRS AND BMDECODE_LIBRARIES)
    set(BMDECODE_FOUND TRUE)
    message(STATUS "Bitmain DECODE found")
else(BMDECODE_INCLUDE_DIRS AND BMDECODE_LIBRARIES)
    message(STATUS "Bitmain DECODE not found")
endif(BMDECODE_INCLUDE_DIRS AND BMDECODE_LIBRARIES)
