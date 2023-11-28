"""Integration test for Python-related Protobuf setup"""
import subprocess
import sys
import tempfile
import os

def test_pwm_proto_serialization():
    """Tests protobuf installation, import, and correct serialization/deserialization"""

    # Build the package
    subprocess.check_call([sys.executable, "-m", "pip", "install", "build"])
    subprocess.check_call([sys.executable, "-m", "build", "python_rpc"])

    # Get the wheel
    wheel_file = next(
        (file for file in os.listdir("python_rpc/dist") if file.endswith(".whl")), None
    )
    assert wheel_file, "Wheel file not found"

    # Install the package from the wheel
    with tempfile.TemporaryDirectory() as temp_dir:
        subprocess.check_call(
            [
                sys.executable,
                "-m",
                "pip",
                "install",
                os.path.join("python_rpc/dist", wheel_file),
                "--target",
                temp_dir,
            ]
        )
        sys.path.append(temp_dir)

        # pylint: disable=import-error, wrong-import-position, import-outside-toplevel
        from rpc_generated_protobufs.pwm_pb2 import GetFrequency

        # Test functionality
        pwm_msg = GetFrequency()
        pwm_msg.frequency = 2000

        serialized_message = pwm_msg.SerializeToString()

        new_pwm_msg = GetFrequency()
        new_pwm_msg.ParseFromString(serialized_message)

        assert new_pwm_msg.frequency == pwm_msg.frequency
