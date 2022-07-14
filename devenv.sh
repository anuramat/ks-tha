#!/usr/bin/env bash
export $(cat .env | xargs)
export proj_path=$(pwd)
