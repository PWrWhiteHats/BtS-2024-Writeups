hvm compile main.hvm && \
cd main && \
cargo b && \
cd - && \
cp main/target/debug/main bin
