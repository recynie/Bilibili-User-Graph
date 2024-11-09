import asyncio
import networkx as nx
from bilibili_api import user,Credential,errors
import json

with open('my_redential.json','r') as f:
    cre_param=json.load(f)
CRE=Credential(**cre_param)


async def get_follower_info(uid_list:list[int],
                            info_include:list[str]=['mid','uname'],
                            info_exclude:list[str]=[]
                            ):
    '''Get user information, using uid list.

    :param uid_list: list containing uid
    :param info_include: info keys to be included.
    Do not work with info_exclude not empty
    :param info_exclude: info keys to be excluded, defaults to []
    :return: dict with user info, orgnised into a list
    '''
    uid_ret=[]
    info_ret=[]
    for uid in uid_list:
        u=user.User(uid=uid,credential=CRE)
        try:
            resp=await u.get_followers()
        except errors.ResponseCodeException as e:
            return [],[]
        for fler_dct in resp['list']:
            uid_ret.append(fler_dct['mid'])
            if info_exclude:
                info_ret.append({k: fler_dct[k] for k in fler_dct.keys() if k not in info_exclude})
            else:
                info_ret.append({k: fler_dct[k] for k in info_include if k in fler_dct})
    return uid_ret,info_ret


async def get_following_info(uid_list:list[int],
                            info_include:list[str]=['mid','uname'],
                            info_exclude:list[str]=[]
                            ):
    '''Get user information, using uid list.
    Return [] when privacy setting is on.

    :param uid_list: list containing uid
    :param info_include: info keys to be included.
    Do not work with info_exclude not empty
    :param info_exclude: info keys to be excluded, defaults to []
    :return: dict with user info, orgnised into a list
    '''
    uid_ret=[]
    info_ret=[]
    for uid in uid_list:
        u=user.User(uid=uid,credential=CRE)
        resp=await u.get_followings()
        if not resp:
            return ([],[])
        for flin_dct in resp['list']:
            uid_ret.append(flin_dct['mid'])
            if info_exclude:
                info_ret.append({k: flin_dct[k] for k in flin_dct.keys() if k not in info_exclude})
            else:
                info_ret.append({k: flin_dct[k] for k in info_include if k in flin_dct})
    return uid_ret,info_ret

async def get_example_user():
    u=user.User(uid=176421741,credential=CRE)
    resp=await u.get_followers()
    return resp['list'][0] 
