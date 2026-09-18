#!/bin/bash

IMAGE_NAME="bayrell/baylang-ai"
VERSION="0.1.0"

case $1 in
    
    docker)
        docker build -t $IMAGE_NAME:$VERSION .
    ;;
    
    browse)
        docker run -it --rm \
            -v ./src:/app \
            -p 8787:8787 \
            $IMAGE_NAME:$VERSION \
            pywrangler dev --ip 0.0.0.0 --port 8787
    ;;
    
    *)
        echo "$0 {docker|browse}"
    ;;
    
esac