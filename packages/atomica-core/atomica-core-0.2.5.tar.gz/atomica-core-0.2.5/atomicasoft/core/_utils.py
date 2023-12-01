import base64, os, logging, time

def b64encode(message):
    return base64.b64encode(message).decode()

def b64decode(message):
    return base64.b64decode(message)

def secure_file_opener(path, flags):
    return os.open(path, flags, 0o600)

def secure_executable_opener(path, flags):
    return os.open(path, flags, 0o700)

def stubborn_do(target, args = (), kwargs = {}, sleep_time = 3.0, n_attempts = 100, timeout = 120):
    i_attempt = 0
    timeout_time = time.time() + timeout
    while i_attempt < n_attempts:
        try:
            return target(*args, **kwargs)
        except Exception as err:
            i_attempt += 1
            if i_attempt == n_attempts or timeout_time < time.time():
                raise err
            time.sleep(min(sleep_time, timeout_time - time.time()))

def stubborn_open(path, mode, timeout = 120):
    return stubborn_do(open, (str(path), mode), timeout = timeout)

def stubborn_read(file, timeout = 120):
    return stubborn_do(file.__class__.read, (file,), timeout = timeout)

def stubborn_write(file, contents, timeout = 120):
    return stubborn_do(file.__class__.write, (file,contents), timeout = timeout)

def stubborn_unlink(path, timeout = 120):
    stubborn_do(path.__class__.unlink, (path,), timeout = timeout)

def stubborn_rename(path_old, path_new, timeout = 120):
    return stubborn_do(path_old.__class__.rename, (path_old, path_new), timeout = timeout)

