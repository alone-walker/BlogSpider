#! /bin/bash

function init() {
	[ -z "$PROXY" ] && {
		pip install -r requirements.txt
	} || {
		pip install --proxy http://${PROXY}:8888 -r requirements.txt
	}
	adduser --disabled-password --gecos '' www
	touch /var/log/www.log && chown www:www /var/log/www.log
}

function start_www() {
	id www &>/dev/null || init
	su -m www -c "uwsgi --ini-paste uwsgi.ini"
}

function stop_www() {
	kill -INT $(cat uwsgi.pid)
}

case "$1" in
	start)
		start_www
		;;
	stop)
		stop_www
		;;
	restart)
		stop_www
		start_www
		;;
esac
