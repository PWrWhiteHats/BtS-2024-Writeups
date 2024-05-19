from subprocess import run, PIPE
import re


def brute_force():
    flag = "BtSCTF{"
    regex = re.compile(r"\(\d* (\d)\)")

    while True:
        for candidate in range(0x20, 128):
            stdout = run(
                ["../challenge/bin", "run"],
                stdout=PIPE,
                text=True,
                input=flag + chr(candidate),
            ).stdout

            if regex.match(stdout.splitlines()[-2]).group(1) == "1":
                flag += chr(candidate)
                print(f"Currently known flag characters: {flag}")
                if "CorrectFlag" in stdout:
                    return flag
                break


print(f"The flag is: {brute_force()}")
