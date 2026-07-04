# SPDX-FileCopyrightText: Copyright (c) 2026 NVIDIA CORPORATION & AFFILIATES. All rights reserved.
# SPDX-License-Identifier: Apache-2.0

TROUBLESHOOTING_URL = "https://nvidia.github.io/cuda-python/cuda-pathfinder/latest/troubleshooting.html"


def append_troubleshooting_url(message: str) -> str:
    return f"{message.rstrip()}\n\nPlease see {TROUBLESHOOTING_URL}"
