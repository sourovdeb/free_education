cmake_minimum_required(VERSION 3.28...3.30)

option(ENABLE_STREAMING "Enable streaming outputs (RTMP/FLV)" OFF)

if(ENABLE_STREAMING)
  find_package(MbedTLS 3...<4 REQUIRED)
  find_package(jansson REQUIRED)
endif()
find_package(ZLIB REQUIRED)

if(NOT TARGET OBS::opts-parser)
  add_subdirectory("${CMAKE_SOURCE_DIR}/shared/opts-parser" "${CMAKE_BINARY_DIR}/shared/opts-parser")
endif()

if(ENABLE_STREAMING AND NOT TARGET OBS::bpm)
  add_subdirectory("${CMAKE_SOURCE_DIR}/shared/bpm" bpm)
endif()

if(NOT TARGET OBS::happy-eyeballs)
  add_subdirectory("${CMAKE_SOURCE_DIR}/shared/happy-eyeballs" "${CMAKE_BINARY_DIR}/shared/happy-eyeballs")
endif()

add_library(obs-outputs MODULE)
add_library(OBS::outputs ALIAS obs-outputs)

target_sources(
  obs-outputs
  PRIVATE
    $<$<AND:$<BOOL:${ENABLE_STREAMING}>,$<BOOL:${ENABLE_HEVC}>>:rtmp-hevc.c>
    $<$<AND:$<BOOL:${ENABLE_STREAMING}>,$<BOOL:${ENABLE_HEVC}>>:rtmp-hevc.h>
    $<$<BOOL:${ENABLE_STREAMING}>:flv-mux.c>
    $<$<BOOL:${ENABLE_STREAMING}>:flv-mux.h>
    $<$<BOOL:${ENABLE_STREAMING}>:flv-output.c>
    $<$<BOOL:${ENABLE_STREAMING}>:librtmp/amf.c>
    $<$<BOOL:${ENABLE_STREAMING}>:librtmp/amf.h>
    $<$<BOOL:${ENABLE_STREAMING}>:librtmp/bytes.h>
    $<$<BOOL:${ENABLE_STREAMING}>:librtmp/cencode.c>
    $<$<BOOL:${ENABLE_STREAMING}>:librtmp/cencode.h>
    $<$<BOOL:${ENABLE_STREAMING}>:librtmp/handshake.h>
    $<$<BOOL:${ENABLE_STREAMING}>:librtmp/hashswf.c>
    $<$<BOOL:${ENABLE_STREAMING}>:librtmp/http.h>
    $<$<BOOL:${ENABLE_STREAMING}>:librtmp/log.c>
    $<$<BOOL:${ENABLE_STREAMING}>:librtmp/log.h>
    $<$<BOOL:${ENABLE_STREAMING}>:librtmp/md5.c>
    $<$<BOOL:${ENABLE_STREAMING}>:librtmp/md5.h>
    $<$<BOOL:${ENABLE_STREAMING}>:librtmp/parseurl.c>
    $<$<BOOL:${ENABLE_STREAMING}>:librtmp/rtmp.c>
    $<$<BOOL:${ENABLE_STREAMING}>:librtmp/rtmp.h>
    $<$<BOOL:${ENABLE_STREAMING}>:librtmp/rtmp_sys.h>
    $<$<BOOL:${ENABLE_STREAMING}>:net-if.c>
    $<$<BOOL:${ENABLE_STREAMING}>:net-if.h>
    $<$<BOOL:${ENABLE_STREAMING}>:rtmp-av1.c>
    $<$<BOOL:${ENABLE_STREAMING}>:rtmp-av1.h>
    $<$<BOOL:${ENABLE_STREAMING}>:rtmp-helpers.h>
    $<$<BOOL:${ENABLE_STREAMING}>:rtmp-stream.c>
    $<$<BOOL:${ENABLE_STREAMING}>:rtmp-stream.h>
    $<$<BOOL:${ENABLE_STREAMING}>:rtmp-windows.c>
    mp4-mux-internal.h
    mp4-mux.c
    mp4-mux.h
    mp4-output.c
    null-output.c
    obs-output-ver.h
    obs-outputs.c
    utils.h
)

if(ENABLE_STREAMING)
  target_compile_definitions(obs-outputs PRIVATE USE_MBEDTLS CRYPTO ENABLE_STREAMING)
endif()

target_compile_options(
  obs-outputs
  PRIVATE
    $<$<COMPILE_LANG_AND_ID:C,AppleClang,Clang>:-Wno-comma>
    $<$<AND:$<PLATFORM_ID:Linux,FreeBSD,OpenBSD>,$<COMPILE_LANG_AND_ID:C,Clang>>:-Wno-error=unreachable-code>
)

target_link_libraries(
  obs-outputs
  PRIVATE
    OBS::libobs
    OBS::happy-eyeballs
    OBS::opts-parser
    $<$<BOOL:${ENABLE_STREAMING}>:OBS::bpm>
    $<$<BOOL:${ENABLE_STREAMING}>:MbedTLS::mbedtls>
    ZLIB::ZLIB
    $<$<BOOL:${ENABLE_STREAMING}>:jansson::jansson>
    $<$<PLATFORM_ID:Windows>:OBS::w32-pthreads>
    $<$<BOOL:${ENABLE_STREAMING}>:$<$<PLATFORM_ID:Windows>:crypt32>>
    $<$<BOOL:${ENABLE_STREAMING}>:$<$<PLATFORM_ID:Windows>:iphlpapi>>
    $<$<PLATFORM_ID:Windows>:winmm>
    $<$<PLATFORM_ID:Windows>:ws2_32>
    "$<$<PLATFORM_ID:Darwin>:$<LINK_LIBRARY:FRAMEWORK,Foundation.framework>>"
    "$<$<PLATFORM_ID:Darwin>:$<LINK_LIBRARY:FRAMEWORK,Security.framework>>"
)

if(OS_WINDOWS)
  configure_file(cmake/windows/obs-module.rc.in obs-outputs.rc)
  target_sources(obs-outputs PRIVATE obs-outputs.rc)
endif()

set_target_properties_obs(obs-outputs PROPERTIES FOLDER plugins/obs-outputs PREFIX "")
