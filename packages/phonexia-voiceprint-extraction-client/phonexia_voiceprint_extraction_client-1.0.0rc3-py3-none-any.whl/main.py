#!/usr/bin/env python3

import argparse
import logging
import os
import pathlib
from typing import Iterator

import grpc
import phonexia.grpc.common.core_pb2 as phx_common
import phonexia.grpc.technologies.speaker_identification.v1.speaker_identification_pb2 as sid
import phonexia.grpc.technologies.speaker_identification.v1.speaker_identification_pb2_grpc as sid_grpc


def make_request(file: str) -> Iterator[sid.ExtractRequest]:
    chunk_size = 1024 * 1024
    request = sid.ExtractRequest(audio=phx_common.Audio())

    with open(file, mode="rb") as fd:
        while chunk := fd.read(chunk_size):
            request.audio.content = chunk
            yield request


def voiceprint_path(audio_path: str) -> str:
    suffix = ".ubj"
    return str(pathlib.Path(audio_path).with_suffix(suffix))


def write_voiceprint(path: str, content: bytes) -> None:
    with open(path, "wb") as f:
        f.write(content)


def write_result(audio_path: str, response: sid.ExtractResponse) -> None:
    vp_path = voiceprint_path(audio_path)
    logging.info(f"Writing voiceprint to {vp_path}")
    write_voiceprint(vp_path, response.result.voiceprint.content)

    print(
        f"Audio: {audio_path}\n"
        f"Total billed time: {response.processed_audio_length.ToTimedelta()}\n"
        "Voiceprint:\n"
        f" speech length: {response.result.speech_length.ToTimedelta()}\n"
        f" voiceprint file: {vp_path}",
        end="\n\n",
    )


def extract_vp(channel: grpc.Channel, file: str) -> None:
    logging.info(f"Extracting voiceprints from {file}")
    stub = sid_grpc.VoiceprintExtractionStub(channel)
    write_result(file, stub.Extract(make_request(file)))


def main():
    parser = argparse.ArgumentParser(
        description=(
            "Voiceprint extraction gRPC client. Extracts voiceprint from an input audio file."
        ),
    )
    parser.add_argument(
        "-H",
        "--host",
        type=str,
        default="localhost:8080",
        help="Server address, default: localhost:8080",
    )
    parser.add_argument(
        "-l",
        "--log_level",
        type=str,
        default="error",
        choices=["critical", "error", "warning", "info", "debug"],
    )
    parser.add_argument("--use_ssl", action="store_true", help="Use SSL connection")
    parser.add_argument("file", type=str, help="input audio file")

    args = parser.parse_args()

    logging.basicConfig(
        level=args.log_level.upper(),
        format="[%(asctime)s.%(msecs)03d] [%(levelname)s] %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )

    if not os.path.isfile(args.file):
        logging.error(f"no such file {args.file}")
        exit(1)

    try:
        logging.info(f"Connecting to {args.host}")
        if args.use_ssl:
            with grpc.secure_channel(
                target=args.host, credentials=grpc.ssl_channel_credentials()
            ) as channel:
                extract_vp(channel, args.file)
        else:
            with grpc.insecure_channel(target=args.host) as channel:
                extract_vp(channel, args.file)

    except grpc.RpcError:
        logging.exception("RPC failed")
        exit(1)
    except Exception:
        logging.exception("Unknown error")
        exit(1)


if __name__ == "__main__":
    main()
