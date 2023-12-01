from dataclasses import fields


def complete(a: object, b: object):
    """用a的值补全b缺失的值"""
    for f in fields(type(a)):
        b.__dict__[f.name] = b.__dict__[f.name] or a.__dict__[f.name]
    return b
