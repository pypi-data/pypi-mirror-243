#!/usr/bin/env python3

import argparse
import os
from itertools import zip_longest
import logging
from typing import Iterator

import grpc
import numpy as np
import phonexia.grpc.common.core_pb2 as phx_common
import phonexia.grpc.technologies.speaker_identification.v1.speaker_identification_pb2 as sid
import phonexia.grpc.technologies.speaker_identification.v1.speaker_identification_pb2_grpc as sid_grpc

MAX_BATCH_SIZE = 1024


def list_reader(list_path) -> Iterator[str]:
    logging.info(f"Opening file; {list_path}")
    with open(list_path) as file:
        for vp_path in file.read().splitlines():
            if os.path.exists(vp_path):
                yield vp_path


def parse_vp(path: str) -> phx_common.Voiceprint:
    logging.info(f"Opening voiceprint: {path}")
    with open(path, mode="rb") as file:
        return phx_common.Voiceprint(content=file.read())


def make_request(list_a: Iterator[str], list_b: Iterator[str]) -> Iterator[sid.CompareRequest]:
    batch_size = 0
    request = sid.CompareRequest()

    for file_a, file_b in zip_longest(list_a, list_b):
        if batch_size >= MAX_BATCH_SIZE:
            yield request
            batch_size = 0
            request = sid.CompareRequest()

        if file_a:
            vp = parse_vp(file_a)
            request.voiceprints_a.append(vp)
            batch_size += 1

        if file_b:
            vp = parse_vp(file_b)
            request.voiceprints_b.append(vp)
            batch_size += 1

    # Yield the last request if it contains any voiceprints
    if len(request.voiceprints_a) or len(request.voiceprints_b):
        yield request


def print_scores(row: int, cols: int, result: list) -> None:
    print("Score:")
    mat = np.array(result).reshape(row, cols)
    for row in mat:
        for val in row:
            print(f"{val:7.1f}", end=" ")
        print("")


def compare_one_to_one(file1: str, file2: str, channel: grpc.Channel) -> None:
    stub = stub = sid_grpc.VoiceprintComparisonStub(channel)
    result = stub.Compare(make_request(iter([file1]), iter([file2])))
    for res in result:
        print_scores(1, 1, [res.scores.values])


def compare_m_to_n(list1: Iterator[str], list2: Iterator[str], channel: grpc.Channel) -> None:
    stub = sid_grpc.VoiceprintComparisonStub(channel)
    n_rows = 0
    n_cols = 0
    scores = []
    requests = make_request(list1, list2)
    for result in stub.Compare(requests):
        if result.scores.rows_count:
            n_rows = result.scores.rows_count
            n_cols = result.scores.columns_count
        scores.extend(result.scores.values)

    print_scores(n_rows, n_cols, scores)


def main():
    parser = argparse.ArgumentParser(
        description="Voiceprint Comparison gRPC client. Compares voiceprints and returns scores.",
    )
    input_group = parser.add_mutually_exclusive_group(required=True)
    input_group.add_argument("--files", nargs=2, help="files for 1x1 comparison")
    input_group.add_argument("--lists", nargs=2, help="lists of files for MxN comparison")

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
    args = parser.parse_args()

    logging.basicConfig(
        level=args.log_level.upper(),
        format="[%(asctime)s.%(msecs)03d] [%(levelname)s] %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )

    try:
        logging.info(f"Connecting to {args.host}")
        if args.use_ssl:
            with grpc.secure_channel(
                target=args.host, credentials=grpc.ssl_channel_credentials()
            ) as channel:
                if args.files:
                    compare_one_to_one(args.files[0], args.files[1], channel)
                elif args.lists:
                    compare_m_to_n(list_reader(args.lists[0]), list_reader(args.lists[1]), channel)
        else:
            with grpc.insecure_channel(target=args.host) as channel:
                if args.files:
                    compare_one_to_one(args.files[0], args.files[1], channel)
                elif args.lists:
                    compare_m_to_n(list_reader(args.lists[0]), list_reader(args.lists[1]), channel)

    except grpc.RpcError:
        logging.exception("RPC failed")
        exit(1)
    except Exception:
        logging.exception("Unknown error")
        exit(1)


if __name__ == "__main__":
    main()
