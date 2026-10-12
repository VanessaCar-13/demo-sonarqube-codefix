"""Módulo legacy de autenticación (ANTES). Contiene fallos típicos que
SonarQube / SAST detectan: inyección SQL, credenciales en código,
hash débil, ejecución de comandos con shell=True y deserialización insegura."""
import hashlib
import pickle
import sqlite3
import subprocess

DB_PASSWORD = "admin123"          # S2068: credencial hardcodeada
API_KEY = "sk_live_51H8xExampleKey"  # S6418: secreto en el código


def get_user(conn, username):
    cursor = conn.cursor()
    # S3649: inyección SQL por concatenación de cadenas
    query = "SELECT * FROM users WHERE name = '" + username + "'"
    cursor.execute(query)
    return cursor.fetchone()


def hash_password(password):
    # S4790: algoritmo de hash débil (MD5)
    return hashlib.md5(password.encode()).hexdigest()


def ping_host(host):
    # S4721: inyección de comandos (shell=True con entrada del usuario)
    return subprocess.call("ping -c 1 " + host, shell=True)


def load_session(raw_bytes):
    # S5135: deserialización insegura de datos no confiables
    return pickle.loads(raw_bytes)
