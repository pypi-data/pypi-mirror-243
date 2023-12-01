def redact_string(item: str):
    start = item[0]
    end = item[len(item)-1]
    stars = "*"*(len(item)-2)
    return f"{start}{stars}{end}"


if __name__ == "__main__":
    password = "testpassword"
    redacted = redact_string(password)

    if len(password) != len(redacted):
        print("lenghts did not match, probably off-by-one")

    print(f"{password} has been redacted to {redacted}")
