FROM alpine:3.7

# install dependencies
RUN apk add --no-cache python3 openssh-client git

# copy scripts
COPY parse.py /usr/local/bin/parse
COPY build.sh /usr/local/bin/build

# make scripts executable
RUN chmod +x /usr/local/bin/parse
RUN chmod +x /usr/local/bin/build
