#!/usr/bin/env python3
"""Word-timed transcript for a clip: ElevenLabs Scribe when a key is set (tight word timing, keeps "um"/"uh"),
else the free local Whisper via HyperFrames. Writes a flat word list: [{"text","start","end"}, ...].
Usage: python3 transcribe.py <video-or-audio> <out.json>
Key: ELEVENLABS_API_KEY in the environment, in <reels_home>/.env or in ~/.config/reels/.env (never pasted into chat)."""
import json, os, sys, tempfile, urllib.error, urllib.request, uuid
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import common

src, out = Path(sys.argv[1]).expanduser(), Path(sys.argv[2]).expanduser()

def key():
    if os.environ.get("ELEVENLABS_API_KEY"): return os.environ["ELEVENLABS_API_KEY"]
    for env in (common.reels_home(create=False) / ".env", Path.home() / ".config" / "reels" / ".env"):
        for line in (env.read_text(encoding="utf-8").splitlines() if env.exists() else []):
            if line.startswith("ELEVENLABS_API_KEY="): return line.split("=", 1)[1].strip()

def scribe(k):
    with tempfile.TemporaryDirectory() as tmp:
        audio = Path(tmp) / "a.mp3"   # mono 64 kbps: ~0.5 MB a minute, only the audio leaves the machine
        common.run([common.ffmpeg(), "-v", "error", "-y", "-i", src, "-vn", "-ac", "1", "-ar", "16000", "-b:a", "64k", audio], low=False)
        data = audio.read_bytes()
    for model in ("scribe_v2", "scribe_v1"):
        b = uuid.uuid4().hex
        body = b"".join([
            f"--{b}\r\nContent-Disposition: form-data; name=\"model_id\"\r\n\r\n{model}\r\n".encode(),
            f"--{b}\r\nContent-Disposition: form-data; name=\"timestamps_granularity\"\r\n\r\nword\r\n".encode(),
            f"--{b}\r\nContent-Disposition: form-data; name=\"tag_audio_events\"\r\n\r\nfalse\r\n".encode(),
            f"--{b}\r\nContent-Disposition: form-data; name=\"file\"; filename=\"a.mp3\"\r\nContent-Type: audio/mpeg\r\n\r\n".encode(),
            data, f"\r\n--{b}--\r\n".encode()])
        req = urllib.request.Request("https://api.elevenlabs.io/v1/speech-to-text", data=body, method="POST",
                                     headers={"xi-api-key": k, "Content-Type": f"multipart/form-data; boundary={b}"})
        try:
            with urllib.request.urlopen(req, timeout=300) as r:
                res = json.load(r)
            return model, [{"text": w["text"], "start": round(w["start"], 3), "end": round(w["end"], 3)}
                           for w in res.get("words", []) if w.get("type") == "word" and w["text"].strip()]
        except urllib.error.HTTPError as e:
            msg = e.read().decode(errors="replace")[:200]
            if e.code in (400, 422) and "model" in msg.lower(): continue      # model id not offered: try the older one
            sys.exit(f"ElevenLabs error {e.code}: {msg}")
    sys.exit("ElevenLabs: no usable Scribe model")

k = key()
if k:
    model, words = scribe(k)
    print(f"transcribed with ElevenLabs {model}: {len(words)} words")
else:
    d = out.parent / (out.stem + "_whisper")
    common.run(common.hyperframes("transcribe", src, "-d", d, "--json", "--model", "small.en"), capture=True)
    words = common.load_json(d / "transcript.json")
    print(f"transcribed with local Whisper (no ElevenLabs key): {len(words)} words - timing can drift ~0.3 s")
with open(out, "w", encoding="utf-8") as fh:
    json.dump(words, fh)
