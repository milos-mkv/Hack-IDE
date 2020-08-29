"""
------------------------------------------------------------------------------
    @file       log_system.py
    @author     Milos Milicevic (milosh.mkv@gmail.com)
    @brief      Log system form IDE.
    @version    0.1
    @date       2020-08-29
    @copyright 	Copyright (c) 2020
    
    Distributed under the MIT software license, see the accompanying
    file COPYING or http://www.opensource.org/licenses/mit-license.php.
------------------------------------------------------------------------------
"""

import colorama, datetime
from colorama import Fore, Back, Style

class LogSystem(object):

    @staticmethod
    def initialize(): 
        """ Initialize colorama. """
        colorama.init(autoreset=True)

    @staticmethod
    def error(message): 
        """
        Print any text in red color and will also show that this message was an error message.
        """
        print(Fore.RED + Style.BRIGHT + "[-] [ " + str(datetime.datetime.now()) + " ] " + str(message))

    @staticmethod
    def information(message): 
        """
        Print any text in blue color and will also show that this message was an information message.
        """
        print(Fore.BLUE + Style.BRIGHT+ "[*] [ " + str(datetime.datetime.now()) +" ] " + str(message))

    @staticmethod
    def success(message): 
        """
        Print any text in green color and will also show that this message was an success message.
        """
        print(Fore.GREEN + Style.BRIGHT + "[+] [ " + str(datetime.datetime.now()) + " ] " + str(message))

    @staticmethod
    def warning(message): 
        """
        Print any text in yellow color and will also show that this message was an warning message.
        """
        print(Fore.YELLOW + Style.BRIGHT+ "[!] [ " + str(datetime.datetime.now()) + " ] " + str(message))
