#!/usr/bin/env python3

import base64
import os
import sys
import time

from selenium import webdriver


def main():
    session_id = os.getenv('SERVICE_SMART_BOT_SESSION_ID', '<error>')
    html = base64.b64decode(sys.argv[1].encode()).decode()
    with webdriver.Firefox() as ff:
        ff.get(
            'data:text/html;charset=utf-8,'
            + html
            + '<!-- Generated by smart_bot, session_id = {} -->'.format(session_id)
        )
        time.sleep(3.5)



if __name__ == '__main__':
    main()
