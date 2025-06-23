import pytest
import re

SUDO_PACKAGE_NAME = "sudo"
SUDO_CONFIG_PATH = "/etc/sudoers"

def test_sudo_installed(host):
    package = host.package(SUDO_PACKAGE_NAME)
    assert package.is_installed, "Pakiet sudo nie jest zainstalowany!"

@pytest.mark.parametrize("distro, expected_entry", [
    ("ubuntu", r"%sudo\s+ALL=\(ALL:ALL\)\s+NOPASSWD:ALL"),
    ("almalinux", r"%wheel\s+ALL=\(ALL:ALL\)\s+NOPASSWD:ALL"),
    ("alpine", r"%wheel\s+ALL=\(ALL:ALL\)\s+NOPASSWD:ALL"),
])
def test_sudoers_configuration(host, distro, expected_entry):
    os_name = host.system_info.distribution

    if distro in os_name:
        sudoers_content = host.run("sudo cat "+SUDO_CONFIG_PATH).stdout            
        assert re.search(expected_entry, sudoers_content), f"Błąd! Wpis '{expected_entry}' nie istnieje w /etc/sudoers dla {os_name}"

def test_sudoers_superusers_configuration(host):
    os_name = host.system_info.distribution
    expected_entry = r"%superusers\s+ALL=\(ALL:ALL\)\s+NOPASSWD:ALL"
    sudoers_content = host.run("sudo cat "+SUDO_CONFIG_PATH).stdout            
    assert re.search(expected_entry, sudoers_content), f"Błąd! Wpis '{expected_entry}' nie istnieje w /etc/sudoers dla {os_name}"