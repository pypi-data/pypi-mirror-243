from fiddler3.schemas.server_info import Version
from fiddler3.utils.version import match_semver


def test_match_semvar_version() -> None:
    assert match_semver(None, '>=22.9.0') is False
    assert match_semver(Version.parse('22.9.0'), '>=22.10.0') is False
    assert match_semver(Version.parse('22.10.0'), '>=22.10.0') is True
    assert match_semver(Version.parse('22.10.0'), '>22.10.0') is False
    assert match_semver(Version.parse('22.11.0'), '>=22.10.0') is True
    assert match_semver(Version.parse('22.11.0'), '>22.10.0') is True
    assert match_semver(Version.parse('22.10.0'), '<=22.10.0') is True
    assert match_semver(Version.parse('22.10.0'), '<22.10.0') is False
    assert match_semver(Version.parse('22.9.0'), '<22.10.0') is True
    assert match_semver(Version.parse('22.11.0-RC1'), '>=22.11.0') is True
