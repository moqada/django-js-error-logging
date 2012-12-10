# -*- coding: utf-8 -*-


def get_browser_name(user_agent):
    """ get browser name from UserAgent
    """
    # FIXME: super lazy judgement
    if 'iPhone' in user_agent:
        return 'iPhone'
    if 'Android' in user_agent:
        return 'Android'
    if 'Firefox' in user_agent:
        return 'Firefox'
    if 'Chrome' in user_agent:
        return 'Chrome'
    if 'Safari' in user_agent:
        return 'Safari'
    if 'MSIE' in user_agent:
        return 'Internet Explorer'
    return 'Other'
