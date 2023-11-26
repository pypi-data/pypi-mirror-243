import enum


class PushType(enum.Enum):
    alert = "alert"
    background = "background"
    voip = "voip"
    complication = "complication"
    file_provider = "fileprovider"
    mdm = "mdm"
    unknown = "unknown"
    push_to_talk = "pushtotalk"


class AuthenticationMethod(enum.Enum):
    P8 = "p8"  # you get the AuthKey.p8 file from the Apple Developer Portal
    PEM = "pem"  # convert the exported .p12 file to .pem file using 'openssl pkcs12 -clcerts -legacy -nodes -in Certificates.p12 -out AuthKey.pem'


class InterruptionLevel(enum.Enum):
    active = "active"
    time_sensitive = "time-sensitive"
    critical = "critical"

    def __str__(self):
        if self == InterruptionLevel.active:
            return "Active"
        elif self == InterruptionLevel.time_sensitive:
            return "Time Sensitive"
        elif self == InterruptionLevel.critical:
            return "Critical"
        else:
            return "n/a"
