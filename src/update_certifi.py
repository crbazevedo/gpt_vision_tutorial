import os
import ssl
import certifi
import shutil

def install_certifi():
    # Get the path to certifi's cacert.pem
    certifi_path = certifi.where()
    print(f"Certifi cacert.pem path: {certifi_path}")

    # Get the default OpenSSL CA file path
    openssl_cafile_path = ssl.get_default_verify_paths().openssl_cafile
    print(f"Default OpenSSL cacert.pem path: {openssl_cafile_path}")

    # Make a backup of the original OpenSSL CA file
    backup_cafile_path = openssl_cafile_path + ".bak"
    if not os.path.exists(backup_cafile_path):
        shutil.copy(openssl_cafile_path, backup_cafile_path)
        print(f"Backup of original cacert.pem created at: {backup_cafile_path}")

    # Copy certifi's cacert.pem to the OpenSSL path
    shutil.copy(certifi_path, openssl_cafile_path)
    print(f"Certifi's cacert.pem copied to: {openssl_cafile_path}")

if __name__ == "__main__":
    install_certifi()
