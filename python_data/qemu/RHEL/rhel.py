from utils import datatype

package_install: datatype.ShellTask = {
    "Message": "Qemu용 패키지 설치",
    "Path": "!Home",
    "Exec": [
        "sudo",
        "dnf",
        "install",
        "-y",
        "qemu-kvm",
        "libvirt",
        "virt-install",
        "virt-manager"
        ]
}

install_tasks: list[datatype.ShellTask] = [
    package_install
]
