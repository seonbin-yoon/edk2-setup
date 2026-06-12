import os
import shutil

from utils import datatype


def make_qemu_dir(context: datatype.Contexts):
    qemu_path = os.path.join(context.config["qemu_path"], "hda-contents", "EFI", "BOOT")
    os.makedirs(qemu_path)

def copy_uefi_image(context: datatype.Contexts):
    uefi_image_path = os.path.join(context.program, "data", "bios.bin")
    qemu_path = context.config["qemu_path"]
    shutil.copy2(uefi_image_path, qemu_path)

install_tasks: list[datatype.Function] = [
    {
        "Message": "qemu 전용 폴더 생성",
        "Func": make_qemu_dir
    },
    {
        "Message": "UEFI 이미지 복사",
        "Func": copy_uefi_image
    }
]
