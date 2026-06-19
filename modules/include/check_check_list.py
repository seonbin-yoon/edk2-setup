from utils import datatype

EDK_BASIC_CHECKS = [
        {
            "Check": "edk2_path",
            "Message": "edk2 설치 위치는 비어있을 수 없습니다."
        },
        {
            "Check": "tool_chain_tag",
            "Message": "빌드툴은 비어있을 수 없습니다."
        },
        {
            "Check": "function_in",
            "Message": "부트로더의 시작 함수 지점은 비어있을 수 없습니다."
        },
        {
            "Check": "loader_name",
            "Message": "부트로더의 이름은 비어있을 수 없습니다."
        },
        {
            "Check": "target_arch",
            "Message": "타겟 아키텍처는 비어있을 수 없습니다."
        },
        {
            "Check": "active_platform",
            "Message": "활성 플랫폼은 파일은 비어있을 수 없습니다. (.dsc)"
        },
        {
            "Check": "version",
            "Message": "부트로더의 버전은 비어있을 수 없습니다."
        },
]

EDK_EXTRA_CHECKS: list[datatype.Edk2Check] = [
    {
        "Message": "root 바로 밑에 edk2 폴더를 생성할 수 없습니다.",
        "Function": lambda: len(config["edk2_path"].split("/")) < 3,
        "Depends_on": "edk2_path"
    },
    {
        "Message": "아키텍쳐는 x64, i386 중에 설정해야 합니다.",
        "Function": lambda: config["target_arch"].lower() not in ["x64", "i386"],
        "Depends_on": "target_arch"
    },
]
