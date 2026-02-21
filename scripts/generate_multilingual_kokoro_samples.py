#!/usr/bin/env python3
from __future__ import annotations

import subprocess
from dataclasses import dataclass
from pathlib import Path

import numpy as np
import soundfile as sf
from kokoro import KPipeline


@dataclass(frozen=True)
class SampleSpec:
    lang_code: str
    voice: str
    output_base: str
    text: str


SAMPLES: list[SampleSpec] = [
    SampleSpec(
        lang_code="e",
        voice="ef_dora",
        output_base="sample-spanish-dora",
        text=(
            "Hola. Esta es una demostracion de voz en espanol para Mayari. "
            "Convierte tus documentos en audio y escucha mientras estudias."
        ),
    ),
    SampleSpec(
        lang_code="f",
        voice="ff_siwis",
        output_base="sample-french-siwis",
        text=(
            "Bonjour. Ceci est une demonstration vocale francaise pour Mayari. "
            "Transformez vos documents en audio et ecoutez pendant votre lecture."
        ),
    ),
    SampleSpec(
        lang_code="h",
        voice="hf_alpha",
        output_base="sample-hindi-alpha",
        text=(
            "नमस्ते। यह Mayari के लिए हिंदी वॉइस डेमो है। "
            "आप अपने दस्तावेज़ों को ऑडियो में बदलकर सुन सकते हैं।"
        ),
    ),
    SampleSpec(
        lang_code="i",
        voice="if_sara",
        output_base="sample-italian-sara",
        text=(
            "Ciao. Questa e una demo vocale italiana per Mayari. "
            "Trasforma i documenti in audio e ascolta mentre studi."
        ),
    ),
    SampleSpec(
        lang_code="j",
        voice="jf_nezumi",
        output_base="sample-japanese-nezumi",
        text=(
            "こんにちは。これは Mayari の日本語ボイスデモです。"
            "ドキュメントを音声に変換して、学習中に聞くことができます。"
        ),
    ),
    SampleSpec(
        lang_code="p",
        voice="pf_dora",
        output_base="sample-portuguese-dora",
        text=(
            "Ola. Esta e uma demonstracao de voz em portugues brasileiro para Mayari. "
            "Transforme documentos em audio e escute enquanto estuda."
        ),
    ),
    SampleSpec(
        lang_code="z",
        voice="zf_xiaobei",
        output_base="sample-mandarin-xiaobei",
        text=(
            "你好。这是 Mayari 的中文语音演示。"
            "你可以把文档转换成音频，在学习时收听。"
        ),
    ),
]


def synthesize_to_mp3(output_dir: Path) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)

    pipeline_cache: dict[str, KPipeline] = {}

    for sample in SAMPLES:
        if sample.lang_code not in pipeline_cache:
            pipeline_cache[sample.lang_code] = KPipeline(lang_code=sample.lang_code)
        pipeline = pipeline_cache[sample.lang_code]

        audio_chunks = []
        for _, _, audio in pipeline(
            sample.text,
            voice=sample.voice,
            speed=1.0,
            split_pattern=r"\n+",
        ):
            audio_chunks.append(audio)

        if not audio_chunks:
            raise RuntimeError(f"No audio generated for {sample.output_base}")

        merged = np.concatenate(audio_chunks)

        wav_path = output_dir / f"{sample.output_base}.wav"
        mp3_path = output_dir / f"{sample.output_base}.mp3"
        sf.write(wav_path, merged, 24000)

        subprocess.run(
            [
                "ffmpeg",
                "-y",
                "-i",
                str(wav_path),
                "-codec:a",
                "libmp3lame",
                "-q:a",
                "5",
                str(mp3_path),
            ],
            check=True,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )
        wav_path.unlink(missing_ok=True)
        print(f"generated {mp3_path.name} via {sample.voice} ({sample.lang_code})")


def main() -> None:
    root = Path(__file__).resolve().parents[1]
    output_dir = root / "audio"
    synthesize_to_mp3(output_dir)


if __name__ == "__main__":
    main()
