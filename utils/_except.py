
class Edk2Except:
    """EDK2와 관련된 모든 에러"""

    class Edk2ExistsError(Exception):
        """EDK2 폴더가 이미 존재함"""
        pass

    class NotDockerError(Exception):
        """실행 환경이 Docker가 아님"""
        pass

class QemuExcept:
    """QEMU와 관련된 모든 에러"""
    class QemuExistsError(Exception):
        """QEMU가 이미 존재함"""
        pass

class RunExcept:
    """작업 실행과 관련된 모든 에러"""
    class FailedRunError(Exception):
        """작업 실행에 실패함"""
        pass

    class SudoError(Exception):
        """Sudo 인증 실패함"""
        pass

    class CancelError(Exception):
        """사용자가 작업을 취소함"""
        pass

class SettingError:
    """설정값과 관련된 모든 에러"""
    class InvalidSettingError(Exception):
        """설정값이 유효하지 않음"""
        pass

class InitError:
    """초기화와 관련된 모든 에러"""
    class UnsupportedOSError(Exception):
        """지원되지 않는 OS"""
        pass

    class ConfigNotFoundError(Exception):
        """설정 파일을 찾을 수 없음"""
        pass

    class HomePathNotFoundError(Exception):
        """홈 경로를 알 수 없음"""
        pass

