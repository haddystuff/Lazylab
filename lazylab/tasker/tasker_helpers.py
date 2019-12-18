"""Tasker helpers functions"""
import socket


def is_port_in_use(port):
    """This function returns True if socket in use and false if not"""
    
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        
        return s.connect_ex(('localhost', port)) == 0
        
