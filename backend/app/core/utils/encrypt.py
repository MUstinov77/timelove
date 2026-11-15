from pwdlib import PasswordHash
from starlette.concurrency import run_in_threadpool

password_hash = PasswordHash.recommended()

async def verify_password(plain_password, hashed_password):
    return await run_in_threadpool(
        password_hash.verify,
        plain_password,
        hashed_password
    )

async def get_hashed_password(password):
    return await run_in_threadpool(password_hash.hash, password)

