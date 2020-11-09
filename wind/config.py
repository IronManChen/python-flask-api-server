#! /usr/bin/env python3
#! -*- coding:utf-8 -*-

from oslo_config import cfg
from oslo_log import log

CONF = cfg.CONF

FILE_OPTIONS = {
    'DEFAULT':[
        cfg.StrOpt('log_file',
            default='./wind.log',
            help='Default log file.'),
    ],

    'server': [
        cfg.StrOpt('host',
            default='0.0.0.0',
            help='Server listening address.'),

        cfg.IntOpt('port',
            default=8080,
            help='Server listening port.'),

        cfg.BoolOpt('debug',
            default=True,
            help='Run in debug mode.'),
    ],

    'mysql': [
        cfg.StrOpt('windhost',
            default='127.0.0.1',
            help='wind mysql address.'),
        
        cfg.IntOpt('windport',
            default=3306,
            help='Wind mysql port.'),
        
        cfg.StrOpt('windusername',
            default="root",
            help='Wind mysql user.'),

        cfg.StrOpt('windpassword',
            default="root",
            help='Wind mysql password.'),

        cfg.StrOpt('windschema',
            default="wind",
            help='Wind mysql schema.'),


    ],


}


def setup_logging(project=""): 
    log.setup(CONF, project)

def configure(conf=None, version=None, config_files=None, 
              project="",
              pre_setup_logging_fn=lambda: None): 
    if conf is None: 
        conf = CONF

    for section in FILE_OPTIONS:
        for option in FILE_OPTIONS[section]: 
            if section:
                conf.register_cli_opt(option, group=section) 
            else:
                conf.register_cli_opt(option)

    set_default_for_default_log_levels()

    CONF(project=project, version=version, 
        default_config_files=config_files)

    pre_setup_logging_fn() 
    setup_logging(project=project)

def list_opts():
    return list(FILE.OPTIONS. items())

def set_default_for_default_log_levels(): 
    extra_log_level_defaults = []

    log.register_options(CONF)
    CONF.set_default("default_log_levels",
                    CONF.default_log_levels + extra_log_level_defaults)
