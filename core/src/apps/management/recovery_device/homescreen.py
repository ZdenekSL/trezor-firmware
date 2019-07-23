from trezor import loop, utils, wire
from trezor.crypto.hashlib import sha256
from trezor.errors import MnemonicError
from trezor.messages.Success import Success

from . import recover

from apps.common import mnemonic, storage
from apps.common.layout import show_success
from apps.management.recovery_device import layout


async def recovery_homescreen() -> None:
    try:
        await recovery_process()
    except Exception:
        # clear the loop state, so loop.run will exit and the device is soft-rebooted
        loop.clear()
        raise


async def recovery_process() -> Success:
    # recovery process does not communicate on the wire
    ctx = wire.DummyContext()

    try:
        result = await _continue_recovery_process(ctx)
    except recover.RecoveryAborted:
        dry_run = storage.device.is_recovery_dry_run()
        if dry_run:
            storage.device.end_recovery_progress()
        else:
            storage.wipe()
        raise wire.ActionCancelled("Cancelled")

    return result


async def _continue_recovery_process(ctx: wire.Context) -> Success:
    # gather the current recovery state from storage
    in_progress = storage.device.is_recovery_in_progress()
    word_count = storage.device.get_word_count()
    dry_run = storage.device.is_recovery_dry_run()

    if not in_progress:  # invalid and inconsistent state
        raise RuntimeError
    if not word_count:  # the first run, prompt word count from the user
        word_count = await _request_and_store_word_count(ctx, dry_run)

    mnemonic_type = mnemonic.type_from_word_count(word_count)

    secret = await _request_and_store_secret(ctx, word_count, mnemonic_type)

    if dry_run:
        result = await _finish_recovery_dry_run(ctx, secret, mnemonic_type)
    else:
        result = await _finish_recovery_real_run(ctx, secret, mnemonic_type)
    return result


async def _finish_recovery_dry_run(
    ctx: wire.Context, secret: bytes, mnemonic_type: int
) -> Success:
    digest_input = sha256(secret).digest()
    stored, _ = mnemonic.get()
    digest_stored = sha256(stored).digest()
    result = utils.consteq(digest_stored, digest_input)

    await layout.show_dry_run_result(ctx, result)

    storage.device.end_recovery_progress()

    if result:
        return Success("The seed is valid and matches the one in the device")
    else:
        raise wire.ProcessError("The seed does not match the one in the device")


async def _finish_recovery_real_run(
    ctx: wire.Context, secret: bytes, mnemonic_type: int
) -> Success:
    storage.device.store_mnemonic_secret(
        secret, mnemonic_type, needs_backup=False, no_backup=False
    )
    storage.device.end_recovery_progress()

    await show_success(ctx, ("You have successfully", "recovered your wallet."))

    return Success(message="Device recovered")


async def _request_and_store_word_count(ctx: wire.Context, dry_run: bool) -> int:
    homepage = layout.RecoveryHomescreen("Select number of words")
    await layout.homescreen_dialog(ctx, homepage, "Select")

    # ask for the number of words
    word_count = await layout.request_word_count(ctx, dry_run)

    # save them into storage
    storage.device.set_word_count(word_count)

    return word_count


async def _request_and_store_secret(
    ctx: wire.Context, word_count: int, mnemonic_type: int
):
    await _request_share_first_screen(ctx, word_count, mnemonic_type)

    secret = None
    while secret is None:
        # ask for mnemonic words one by one
        words = await layout.request_mnemonic(ctx, word_count, mnemonic_type)
        # process this seed share
        try:
            secret = recover.process_share(words, mnemonic_type)
        except MnemonicError:
            await layout.show_invalid_mnemonic(ctx, mnemonic_type)
            continue
        if secret is None:
            await _request_share_next_screen(ctx, mnemonic_type)

    return secret


async def _request_share_first_screen(
    ctx: wire.Context, word_count: int, mnemonic_type: int
):
    if mnemonic_type == mnemonic.TYPE_BIP39:
        content = layout.RecoveryHomescreen(
            "Enter recovery seed", "(%d words)" % word_count
        )
        await layout.homescreen_dialog(ctx, content, "Enter seed")
    elif mnemonic_type == mnemonic.TYPE_SLIP39:
        remaining = storage.slip39.get_remaining()
        if remaining:
            await _request_share_next_screen(ctx, mnemonic_type)
        else:
            content = layout.RecoveryHomescreen(
                "Enter any share", "(%d words)" % word_count
            )
            await layout.homescreen_dialog(ctx, content, "Enter share")
    else:
        raise RuntimeError


async def _request_share_next_screen(ctx: wire.Context, mnemonic_type: int):
    if mnemonic_type == mnemonic.TYPE_SLIP39:
        remaining = storage.slip39.get_remaining()
        if remaining == 1:
            text = "1 more share"
        else:
            text = "%d more shares" % remaining
        content = layout.RecoveryHomescreen(text, "needed to enter")
        await layout.homescreen_dialog(ctx, content, "Enter share")
    else:
        raise RuntimeError
