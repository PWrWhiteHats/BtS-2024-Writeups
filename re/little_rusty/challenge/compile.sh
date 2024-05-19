#!/bin/bash

# ELF static, debug + strip (leave only symbols)
env -u CARGO_TARGET_DIR cargo b --target x86_64-unknown-linux-musl
