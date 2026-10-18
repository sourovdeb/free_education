# STRIP-LIST — streaming surface inventory (obs-lite)
Base: obs-studio master @ f1c0a116441bdb7a1de7896f810009ea487b8508
Branch: obs-lite @ d785ffe (plugin-level strip done)

## Done (commit d785ffe)
- plugins/obs-outputs: RTMP/FLV/librtmp/net-if gated behind ENABLE_STREAMING (default OFF); mp4/mov/null outputs kept (recording depends on them).
- plugins/rtmp-services, plugins/obs-webrtc: removed from build unless ENABLE_STREAMING.
- Conditional deps: MbedTLS, jansson, bpm (streaming only); ZLIB + happy-eyeballs + opts-parser kept.

## Remaining strip targets (frontend, step 5 — ~3.2k lines)
- frontend/widgets/OBSBasic_Streaming.cpp (479 L)
- frontend/widgets/OBSBasic_Service.cpp (128 L)
- frontend/settings/OBSBasicSettings_Stream.cpp (1868 L)
- frontend/wizards/AutoConfigStreamPage.cpp/.hpp (712 L) + forms/AutoConfigStreamPage.ui
- frontend/oauth/ (Twitch/Restream/YouTube auth), MultitrackVideo*, GoLiveAPI_*
- Build lists: frontend/cmake/ui-settings.cmake, ui-wizards.cmake, ui-widgets.cmake, ui-qt.cmake
- ~70 refs to StartStreaming/streamButton in OBSBasic.hpp/hotkeys/status bar/output handlers
- OBSBasicSettings.ui stream page; obs_get_service_properties("rtmp_common") ~15 sites

## Keep (explicit)
- obs-websocket (submodule @ e28f84975984340e84fc4879cfc05741cc0afde1) — vibe CLI bridge
- obs-browser (submodule @ 07227af86e0d9d6845bd5a583783a0d14c1025d2) — Excalidraw host (pending G5)
- obs-ffmpeg, obs-x264, win-capture, image-source, obs-filters, obs-transitions, frontend-tools, obs-text
- libobs obs_output_* / obs_service_* APIs (recording path)

## Submodule pointers (Windows fetches from upstream)
- obs-browser @ 07227af86e0d9d6845bd5a583783a0d14c1025d2
- obs-websocket @ e28f84975984340e84fc4879cfc05741cc0afde1
