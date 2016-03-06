# -*- coding: utf-8 -*-
"""
Get haiku from the guardian website.
"""
from guardian_haiku import guardian_haiku

if __name__ == "__main__":
    print(list(guardian_haiku.main()))
