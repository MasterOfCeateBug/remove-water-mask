# -*- coding: utf8 -*-

__author__ = 'imagine'

import os
from removewatermask.removemask import threading_remove_mask

if __name__ == '__main__':
    target_dir = os.path.join(os.path.dirname(__file__), 'original_image_file')
    handle_image_file = os.path.join(os.path.dirname(__file__), 'handle_image_file')
    threading_remove_mask(target_dir, handle_image_file)
