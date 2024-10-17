FROM python:3.12.7-alpine3.20

RUN apk add bash build-base cmake git linux-headers zlib zlib-dev

RUN pip install mypy-protobuf

RUN git clone --recurse-submodules --shallow-submodules --depth 1 -b v4.25.5 https://github.com/protocolbuffers/protobuf.git

WORKDIR ./protobuf

RUN cmake -DCMAKE_BUILD_TYPE=Release -Dprotobuf_BUILD_TESTS=OFF -Dprotobuf_BUILD_SHARED_LIBS=OFF -Dprotobuf_BUILD_LIBPROTOC=ON .

RUN make

RUN make install
