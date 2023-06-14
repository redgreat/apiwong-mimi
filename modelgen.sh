#!/usr/bin/env sh

sqlacodegen --outfile ./app/models/db.py --tables carlocdaily,watchdaily 'mysql+pymysql://2VGr71AdbLZb9Ms.root:Mm19890425@gateway01.ap-northeast-1.prod.aws.tidbcloud.com:4000/dailywong?charset=utf8mb4&ssl_ca=/etc/ssl/cert.pem&ssl_check_hostname=false'

