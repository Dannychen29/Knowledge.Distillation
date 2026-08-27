# Windows Game Bar adapter

The V1 adapter uses the Windows Xbox Game Bar shortcuts:

- `Win+Alt+R`: start or stop recording.
- `Win+Alt+M`: toggle microphone during recording.

The control script verifies that Game Bar, capture, system audio and microphone capture are enabled before start. It does not toggle the microphone blindly because a toggle could turn an already-enabled microphone off.

## Operational limitations

- Keep the target application in the foreground before starting.
- Desktop, File Explorer, protected windows and some applications may reject Game Bar capture.
- Multi-window workflows may need separate recordings.
- The script verifies that the resulting MP4 contains an audio track. This proves an audio stream exists, but cannot prove speech quality or that every spoken sentence is audible.
- If the adapter cannot meet the task, preserve the same Skill contract and replace only the recording provider with an approved tool such as OBS or an enterprise recorder.
