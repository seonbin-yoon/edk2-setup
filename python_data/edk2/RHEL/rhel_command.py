from utils import datatype

package_upgrade: datatype.Task = {
    "Message": "설치된 패키지 업데이트",
    "Path": "!Home",
    "Exec": [
        "sudo",
        "dnf",
        "upgrade",
        "-y"
        ]
}

package_install: datatype.Task = {
    "Message": "빌드용 필수 패키지 설치",
    "Path": "!Home",
    "Exec": [
        "sudo",
        "dnf",
        "install",
        "-y",
        "@development-tools",
        "gcc-c++",
        "libuuid-devel",
        "acpica-tools",
        "git",
        "nasm",
        "qemu-kvm",
        "libvirt",
        "virt-install",
        "virt-manager"
        ]
}

install_tasks: list[datatype.Task] = [
    package_upgrade,
    package_install
]
